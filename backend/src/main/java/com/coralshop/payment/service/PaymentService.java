package com.coralshop.payment.service;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.order.model.OrderHeader;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.repository.OrderRepository;
import com.coralshop.order.service.OrderStatusPolicy;
import com.coralshop.payment.dto.PaymentRequest;
import com.coralshop.payment.dto.PaymentResponse;
import com.coralshop.payment.model.PaymentCharge;
import com.coralshop.payment.model.PaymentResult;
import com.coralshop.payment.repository.PaymentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Cobro de un pedido pendiente a través de la {@link PaymentGateway} configurada. */
@Service
public class PaymentService {

    private static final String CURRENCY = "PEN";

    private final PaymentGateway paymentGateway;
    private final PaymentRepository paymentRepository;
    private final OrderRepository orderRepository;
    private final OrderStatusPolicy statusPolicy;

    public PaymentService(PaymentGateway paymentGateway, PaymentRepository paymentRepository,
                          OrderRepository orderRepository, OrderStatusPolicy statusPolicy) {
        this.paymentGateway = paymentGateway;
        this.paymentRepository = paymentRepository;
        this.orderRepository = orderRepository;
        this.statusPolicy = statusPolicy;
    }

    /**
     * El pedido queda bloqueado (SELECT … FOR UPDATE) durante el cobro, así que dos pagos
     * simultáneos del mismo pedido no pueden aprobarse ambos. El importe sale siempre de la
     * base (D10). Con la pasarela real (fase 6) el cobro se confirmará por webhook.
     */
    @Transactional
    public PaymentResponse pay(long userId, String orderCode, PaymentRequest request) {
        OrderHeader order = orderRepository.lockByCode(orderCode)
                .filter(found -> found.userId() == userId)
                .orElseThrow(() -> new NotFoundException("Pedido no encontrado"));
        if (order.status() != OrderStatus.PENDIENTE_PAGO) {
            throw new BusinessRuleException(order.status() == OrderStatus.CANCELADO
                    ? "El pedido está cancelado y ya no se puede pagar"
                    : "El pedido ya está pagado");
        }

        PaymentResult result = paymentGateway.charge(
                new PaymentCharge(order.orderCode(), order.totalAmount(), CURRENCY, request.toCard()));
        paymentRepository.insert(order.id(), paymentGateway.provider(), result.providerReference(),
                order.totalAmount(), CURRENCY, result.approved());

        OrderStatus orderStatus = order.status();
        if (result.approved()) {
            statusPolicy.requireTransition(order.status(), OrderStatus.PAGADO);
            if (!orderRepository.updateStatus(order.id(), order.status(), OrderStatus.PAGADO)) {
                throw new ConflictException("El pedido cambió durante el pago; recárgalo");
            }
            orderRepository.insertHistory(order.id(), order.status(), OrderStatus.PAGADO, userId,
                    "Pago aprobado (" + result.providerReference() + ")");
            orderStatus = OrderStatus.PAGADO;
        }
        return new PaymentResponse(order.orderCode(), result.approved() ? "APROBADO" : "RECHAZADO",
                orderStatus.name(), result.providerReference(), order.totalAmount(), result.message());
    }
}
