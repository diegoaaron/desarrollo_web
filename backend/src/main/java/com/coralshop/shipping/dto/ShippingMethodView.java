package com.coralshop.shipping.dto;

import java.math.BigDecimal;

public record ShippingMethodView(Long id, String code, String name, BigDecimal cost, int estimatedDays,
                                 boolean requiresAddress) {
}
