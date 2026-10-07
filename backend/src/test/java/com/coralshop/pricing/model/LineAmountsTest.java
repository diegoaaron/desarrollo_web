package com.coralshop.pricing.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class LineAmountsTest {

    /** Historia de la demo: 12 polos de S/ 35 con logo bordado en el pecho (15 + 8), escala docena 15 %. */
    @Test
    void computesDozenOfEmbroideredPolos() {
        LineAmounts amounts = LineAmounts.of(new BigDecimal("35.00"), new BigDecimal("23.00"), 12,
                new BigDecimal("15.00"));

        assertEquals(new BigDecimal("58.00"), amounts.unitPrice());
        assertEquals(new BigDecimal("696.00"), amounts.grossAmount());
        assertEquals(new BigDecimal("104.40"), amounts.discountAmount());
        assertEquals(new BigDecimal("591.60"), amounts.lineTotal());
    }

    @Test
    void roundsDiscountToCentsHalfUp() {
        // 3 × 10.15 = 30.45; 5 % = 1.5225 → 1.52
        LineAmounts amounts = LineAmounts.of(new BigDecimal("10.15"), BigDecimal.ZERO, 3, new BigDecimal("5.00"));

        assertEquals(new BigDecimal("30.45"), amounts.grossAmount());
        assertEquals(new BigDecimal("1.52"), amounts.discountAmount());
        assertEquals(new BigDecimal("28.93"), amounts.lineTotal());
    }

    @Test
    void totalIsAlwaysGrossMinusDiscount() {
        LineAmounts amounts = LineAmounts.of(new BigDecimal("19.99"), new BigDecimal("4.01"), 7,
                new BigDecimal("10.00"));

        assertEquals(amounts.grossAmount().subtract(amounts.discountAmount()), amounts.lineTotal());
        assertEquals(2, amounts.lineTotal().scale());
    }
}
