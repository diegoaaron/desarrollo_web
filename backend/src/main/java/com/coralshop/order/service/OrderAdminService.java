package com.coralshop.order.service;

import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.dto.PageRequest;
import com.coralshop.common.dto.PageResponse;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.InvalidRequestException;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.order.dto.AdminOrderSummaryView;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.dto.StatusChangeRequest;
import com.coralshop.order.model.OrderHeader;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.model.StockMovement;
import com.coralshop.order.repository.OrderRepository;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Bandeja de pedidos del administrador y avance por la máquina de estados. */
@Service
public class OrderAdminService {

    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final OrderStatusPolicy statusPolicy;
    private final OrderDetailAssembler detailAssembler;

    public OrderAdminService(OrderRepository orderRepository, ProductRepository productRepository,
                             OrderStatusPolicy statusPolicy, OrderDetailAssembler detailAssembler) {
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
        this.statusPolicy = statusPolicy;
        this.detailAssembler = detailAssembler;
    }

    @Transactional(readOnly = true)
    public PageResponse<AdminOrderSummaryView> orders(String status, PageRequest page) {
        OrderStatus filter = status == null || status.isBlank() ? null : parseStatus(status);
        List<AdminOrderSummaryView> items = orderRepository.findAdminPage(filter, page.size(), page.offset());
        return PageResponse.of(items, page.page(), page.size(), orderRepository.countAdmin(filter));
    }

    @Transactional(readOnly = true)
    public OrderDetailView order(long orderId) {
        return detailAssembler.assemble(orderId, true);
    }

    /** Cambia el estado según la máquina de estados; cancelar devuelve el stock. */
    @Transactional
    public OrderDetailView changeStatus(long adminId, long orderId, StatusChangeRequest request) {
        OrderStatus next = parseStatus(request.status());
        OrderHeader order = orderRepository.lockById(orderId)
                .orElseThrow(() -> new NotFoundException("Pedido no encontrado"));
        statusPolicy.requireAdminTransition(order.status(), next);
        if (!orderRepository.updateStatus(orderId, order.status(), next)) {
            throw new ConflictException("El pedido cambió mientras lo editabas; recárgalo e inténtalo de nuevo");
        }
        String comment = request.comment() == null || request.comment().isBlank() ? null : request.comment().trim();
        orderRepository.insertHistory(orderId, order.status(), next, adminId, comment);
        if (statusPolicy.restocks(next)) {
            for (StockMovement movement : orderRepository.findStockMovements(orderId)) {
                productRepository.incrementStock(movement.variantId(), movement.quantity());
            }
        }
        return detailAssembler.assemble(orderId, true);
    }

    private static OrderStatus parseStatus(String value) {
        return OrderStatus.parse(value)
                .orElseThrow(() -> new InvalidRequestException("Estado de pedido desconocido: " + value));
    }
}
