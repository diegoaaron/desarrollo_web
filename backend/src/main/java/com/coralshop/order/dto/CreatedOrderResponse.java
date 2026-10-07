package com.coralshop.order.dto;

import java.math.BigDecimal;

public record CreatedOrderResponse(String orderCode, BigDecimal total, String status) {
}
