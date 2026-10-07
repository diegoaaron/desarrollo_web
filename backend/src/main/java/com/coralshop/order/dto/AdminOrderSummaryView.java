package com.coralshop.order.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

/** Fila de la bandeja de pedidos del administrador. */
public record AdminOrderSummaryView(Long id, String orderCode, String customerName, String customerEmail,
                                    BigDecimal totalAmount, String status, int units, OffsetDateTime createdAt) {
}
