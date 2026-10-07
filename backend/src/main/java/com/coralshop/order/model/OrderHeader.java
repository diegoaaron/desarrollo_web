package com.coralshop.order.model;

import java.math.BigDecimal;

/** Lo mínimo de un pedido para cambiar su estado o cobrarlo. */
public record OrderHeader(Long id, String orderCode, Long userId, OrderStatus status, BigDecimal totalAmount) {
}
