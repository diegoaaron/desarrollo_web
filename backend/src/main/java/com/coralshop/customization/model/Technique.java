package com.coralshop.customization.model;

import java.math.BigDecimal;

public record Technique(Long id, String code, String name, String description, BigDecimal baseCost) {
}
