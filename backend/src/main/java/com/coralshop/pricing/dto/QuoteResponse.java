package com.coralshop.pricing.dto;

import java.math.BigDecimal;
import java.util.List;

/**
 * Cotización del carrito. Cada línea trae sus precios recalculados o, si no se puede
 * vender tal como está, la lista de errores (y los importes en null). Los totales suman
 * solo las líneas válidas; valid indica si todo el carrito se puede comprar.
 */
public record QuoteResponse(List<QuotedLine> lines, BigDecimal subtotal, BigDecimal discountAmount,
                            BigDecimal total, boolean valid) {

    public record QuotedLine(int index, Long productId, String productName, String techniqueCode,
                             List<QuotedZone> zones, int quantityTotal, Tier tier, BigDecimal unitBasePrice,
                             BigDecimal unitCustomizationPrice, BigDecimal unitPrice, BigDecimal grossAmount,
                             BigDecimal discountAmount, BigDecimal lineTotal, List<String> errors) {
    }

    public record QuotedZone(String code, String name, BigDecimal surcharge) {
    }

    public record Tier(int minQuantity, String label, BigDecimal discountPercent) {
    }
}
