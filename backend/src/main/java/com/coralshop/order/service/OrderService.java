package com.coralshop.order.service;

import com.coralshop.address.dto.AddressView;
import com.coralshop.address.service.AddressService;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.design.repository.DesignRepository;
import com.coralshop.order.dto.CreateOrderRequest;
import com.coralshop.order.dto.CreatedOrderResponse;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.dto.OrderSummaryView;
import com.coralshop.order.model.NewOrder;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.repository.OrderRepository;
import com.coralshop.pricing.dto.CartLineRequest;
import com.coralshop.pricing.model.LineSpec;
import com.coralshop.pricing.model.PricedLine;
import com.coralshop.pricing.service.PricingService;
import com.coralshop.shipping.dto.ShippingMethodView;
import com.coralshop.shipping.service.ShippingService;
import com.coralshop.user.model.User;
import com.coralshop.user.repository.UserRepository;
import java.math.BigDecimal;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Pedidos del cliente: creación y consulta. */
@Service
public class OrderService {

    /** Sin 0/O ni 1/I para que el código se pueda dictar sin confusiones. */
    private static final char[] CODE_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ".toCharArray();
    private static final int CODE_LENGTH = 8;

    private final PricingService pricingService;
    private final ShippingService shippingService;
    private final AddressService addressService;
    private final DesignRepository designRepository;
    private final ProductRepository productRepository;
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final OrderDetailAssembler detailAssembler;
    private final SecureRandom random = new SecureRandom();

    public OrderService(PricingService pricingService, ShippingService shippingService, AddressService addressService,
                        DesignRepository designRepository, ProductRepository productRepository,
                        OrderRepository orderRepository, UserRepository userRepository,
                        OrderDetailAssembler detailAssembler) {
        this.pricingService = pricingService;
        this.shippingService = shippingService;
        this.addressService = addressService;
        this.designRepository = designRepository;
        this.productRepository = productRepository;
        this.orderRepository = orderRepository;
        this.userRepository = userRepository;
        this.detailAssembler = detailAssembler;
    }

    /**
     * Crea el pedido en una sola transacción (fases.md §2.1): valida y valoriza cada línea en
     * el servidor, descuenta el stock con actualizaciones condicionales y registra el pedido en
     * PENDIENTE_PAGO. Cualquier error deshace todo, incluido el stock ya descontado.
     */
    @Transactional
    public CreatedOrderResponse create(long userId, CreateOrderRequest request) {
        ShippingMethodView shipping = shippingService.requireActive(request.shippingMethodCode());
        NewOrder.Recipient recipient = recipient(userId, shipping, request);

        List<PricedLine> lines = new ArrayList<>();
        for (int index = 0; index < request.lines().size(); index++) {
            lines.add(priceLine(userId, index, request.lines().get(index)));
        }

        reserveStock(lines);

        BigDecimal subtotal = lines.stream().map(line -> line.amounts().grossAmount())
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        BigDecimal discount = lines.stream().map(line -> line.amounts().discountAmount())
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        BigDecimal shippingCost = shipping.cost();
        BigDecimal total = subtotal.subtract(discount).add(shippingCost);

        String note = request.customerNote() == null || request.customerNote().isBlank()
                ? null : request.customerNote().trim();
        NewOrder order = new NewOrder(newOrderCode(), userId, subtotal, discount, shippingCost, total, shipping.id(),
                recipient, note);
        long orderId = orderRepository.insertOrder(order);
        for (PricedLine line : lines) {
            orderRepository.insertLine(orderId, line);
        }
        orderRepository.insertHistory(orderId, null, OrderStatus.PENDIENTE_PAGO, userId, "Pedido creado");
        return new CreatedOrderResponse(order.orderCode(), total, OrderStatus.PENDIENTE_PAGO.name());
    }

    @Transactional(readOnly = true)
    public List<OrderSummaryView> myOrders(long userId) {
        return orderRepository.findSummariesByUser(userId);
    }

    /** El cliente solo ve sus pedidos; uno ajeno responde 404 como si no existiera. */
    @Transactional(readOnly = true)
    public OrderDetailView myOrder(long userId, String orderCode) {
        long orderId = orderRepository.findIdByCodeAndUser(orderCode, userId)
                .orElseThrow(() -> new NotFoundException("Pedido no encontrado"));
        return detailAssembler.assemble(orderId, false);
    }

    private PricedLine priceLine(long userId, int index, CartLineRequest request) {
        String prefix = "Línea " + (index + 1) + ": ";
        LineSpec spec = request.toSpec();
        PricedLine line;
        try {
            line = pricingService.price(spec);
        } catch (BusinessRuleException exception) {
            throw new BusinessRuleException(prefix + exception.getMessage(), exception);
        }
        if (spec.customized()) {
            if (spec.designId() == null) {
                throw new BusinessRuleException(prefix + "sube el diseño que quieres estampar o bordar");
            }
            if (!designRepository.isOwnedBy(spec.designId(), userId)) {
                throw new BusinessRuleException(prefix + "el diseño " + spec.designId() + " no existe en tu cuenta");
            }
        }
        return line;
    }

    /**
     * Descuenta el stock de cada variante (sumando todas las líneas) con
     * UPDATE … WHERE stock >= ?. En orden de id para que dos compras simultáneas no se bloqueen
     * mutuamente.
     */
    private void reserveStock(List<PricedLine> lines) {
        Map<Long, Integer> quantities = new TreeMap<>();
        Map<Long, String> names = new TreeMap<>();
        for (PricedLine line : lines) {
            for (PricedLine.PricedItem item : line.items()) {
                quantities.merge(item.variant().id(), item.quantity(), Integer::sum);
                names.putIfAbsent(item.variant().id(), PricingService.describe(item.variant()));
            }
        }
        for (Map.Entry<Long, Integer> entry : quantities.entrySet()) {
            if (!productRepository.decrementStock(entry.getKey(), entry.getValue())) {
                throw new ConflictException("Stock insuficiente para " + names.get(entry.getKey())
                        + ": pediste " + entry.getValue());
            }
        }
    }

    private NewOrder.Recipient recipient(long userId, ShippingMethodView shipping, CreateOrderRequest request) {
        if (shipping.requiresAddress()) {
            if (request.addressId() == null) {
                throw new BusinessRuleException("Elige la dirección de entrega");
            }
            AddressView address = addressService.get(userId, request.addressId());
            return new NewOrder.Recipient(address.receiverName(), address.phone(), address.department(),
                    address.province(), address.district(), address.street(), address.reference());
        }
        // Recojo en tienda: no se guarda dirección, solo quién recoge y su teléfono.
        if (request.addressId() != null) {
            AddressView address = addressService.get(userId, request.addressId());
            return new NewOrder.Recipient(address.receiverName(), address.phone(), null, null, null, null, null);
        }
        if (request.contactPhone() == null || request.contactPhone().isBlank()) {
            throw new BusinessRuleException("Indica un teléfono de contacto para el recojo");
        }
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalStateException("No existe el usuario " + userId));
        String name = (user.getFirstName() + " " + user.getLastName()).strip();
        return new NewOrder.Recipient(name, request.contactPhone().trim(), null, null, null, null, null);
    }

    private String newOrderCode() {
        StringBuilder code = new StringBuilder("CS-");
        for (int i = 0; i < CODE_LENGTH; i++) {
            code.append(CODE_ALPHABET[random.nextInt(CODE_ALPHABET.length)]);
        }
        return code.toString();
    }
}
