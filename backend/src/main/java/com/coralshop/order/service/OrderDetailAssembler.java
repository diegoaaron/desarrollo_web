package com.coralshop.order.service;

import com.coralshop.common.exception.NotFoundException;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.repository.OrderRepository;
import com.coralshop.order.repository.OrderRepository.LineItem;
import com.coralshop.order.repository.OrderRepository.LineZone;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

/** Arma el detalle de un pedido (cabecera, líneas con zonas e ítems, historial y pagos). */
@Component
public class OrderDetailAssembler {

    private final OrderRepository orderRepository;
    private final OrderStatusPolicy statusPolicy;

    public OrderDetailAssembler(OrderRepository orderRepository, OrderStatusPolicy statusPolicy) {
        this.orderRepository = orderRepository;
        this.statusPolicy = statusPolicy;
    }

    /** forAdmin agrega los estados a los que el administrador puede llevar el pedido. */
    public OrderDetailView assemble(long orderId, boolean forAdmin) {
        OrderDetailView header = orderRepository.findDetail(orderId)
                .orElseThrow(() -> new NotFoundException("Pedido no encontrado"));
        Map<Long, List<OrderDetailView.Zone>> zones = orderRepository.findZones(orderId).stream()
                .collect(Collectors.groupingBy(LineZone::lineId,
                        Collectors.mapping(LineZone::zone, Collectors.toList())));
        Map<Long, List<OrderDetailView.Item>> items = orderRepository.findItems(orderId).stream()
                .collect(Collectors.groupingBy(LineItem::lineId,
                        Collectors.mapping(LineItem::item, Collectors.toList())));
        List<OrderDetailView.Line> lines = orderRepository.findLines(orderId).stream()
                .map(line -> line.withParts(zones.getOrDefault(line.id(), List.of()),
                        items.getOrDefault(line.id(), List.of())))
                .toList();
        List<String> next = forAdmin
                ? statusPolicy.adminNextStatuses(OrderStatus.valueOf(header.status())).stream().map(Enum::name).toList()
                : List.of();
        return header.withParts(lines, orderRepository.findHistory(orderId), orderRepository.findPayments(orderId),
                next);
    }
}
