package com.coralshop.order.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

/** Fila de «Mis pedidos». */
public record OrderSummaryView(String orderCode, String status, BigDecimal totalAmount, int units,
                               OffsetDateTime createdAt) {
}
