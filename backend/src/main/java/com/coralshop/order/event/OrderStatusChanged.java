package com.coralshop.order.event;

import com.coralshop.order.model.OrderStatus;
import java.time.Instant;
import java.util.UUID;

/**
 * Evento de dominio: un pedido cambió de estado (fases.md, fase 4). Lo publican los servicios
 * que mueven la máquina de estados y lo consumen la auditoría y las notificaciones, sin que el
 * publicador sepa quién escucha.
 *
 * @param fromStatus {@code null} cuando el pedido se acaba de crear
 * @param changedBy  usuario que provocó el cambio (cliente o administrador)
 */
public record OrderStatusChanged(UUID eventId, long orderId, String orderCode, long customerId,
                                 OrderStatus fromStatus, OrderStatus toStatus, Long changedBy, String comment,
                                 Instant occurredAt) {

    public static OrderStatusChanged of(long orderId, String orderCode, long customerId, OrderStatus fromStatus,
                                        OrderStatus toStatus, Long changedBy, String comment) {
        return new OrderStatusChanged(UUID.randomUUID(), orderId, orderCode, customerId, fromStatus, toStatus,
                changedBy, comment, Instant.now());
    }
}
