package com.coralshop.pricing.model;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Importes de una línea:
 * <pre>
 * unit_price      = unit_base_price + unit_customization_price
 * gross_amount    = unit_price × quantity_total
 * discount_amount = gross_amount × discount_percent / 100   (redondeo a céntimos, mitad hacia arriba)
 * line_total      = gross_amount − discount_amount
 * </pre>
 */
public record LineAmounts(BigDecimal unitBasePrice, BigDecimal unitCustomizationPrice, BigDecimal unitPrice,
                          int quantityTotal, BigDecimal discountPercent, BigDecimal grossAmount,
                          BigDecimal discountAmount, BigDecimal lineTotal) {

    private static final BigDecimal HUNDRED = BigDecimal.valueOf(100);

    public static LineAmounts of(BigDecimal unitBasePrice, BigDecimal unitCustomizationPrice, int quantityTotal,
                                 BigDecimal discountPercent) {
        BigDecimal base = money(unitBasePrice);
        BigDecimal customization = money(unitCustomizationPrice);
        BigDecimal unitPrice = base.add(customization);
        BigDecimal gross = money(unitPrice.multiply(BigDecimal.valueOf(quantityTotal)));
        BigDecimal discount = money(gross.multiply(discountPercent).divide(HUNDRED, 2, RoundingMode.HALF_UP));
        return new LineAmounts(base, customization, unitPrice, quantityTotal, discountPercent, gross, discount,
                gross.subtract(discount));
    }

    private static BigDecimal money(BigDecimal amount) {
        return amount.setScale(2, RoundingMode.HALF_UP);
    }
}
