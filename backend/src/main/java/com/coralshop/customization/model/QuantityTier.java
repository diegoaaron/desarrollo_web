package com.coralshop.customization.model;

import java.math.BigDecimal;

/** Escala de mayoreo: desde min_quantity unidades de un mismo diseño se aplica el descuento. */
public record QuantityTier(int minQuantity, String label, BigDecimal discountPercent) {
}
