package com.coralshop.pricing.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.customization.model.QuantityTier;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class QuantityPolicyTest {

    private static final List<QuantityTier> TIERS = List.of(
            new QuantityTier(1, "Unidad", new BigDecimal("0.00")),
            new QuantityTier(3, "Paquete de 3", new BigDecimal("5.00")),
            new QuantityTier(6, "Paquete de 6", new BigDecimal("10.00")),
            new QuantityTier(12, "Docena", new BigDecimal("15.00")));

    private final QuantityPolicy policy = new QuantityPolicy();

    /** Tabla de D2: se aplica la escala más alta alcanzada. */
    @ParameterizedTest
    @CsvSource({"1,1", "2,1", "3,3", "4,3", "5,3", "6,6", "9,6", "11,6", "12,12", "15,12", "100,12"})
    void appliesHighestTierReached(int quantity, int expectedTier) {
        assertEquals(expectedTier, policy.tierFor(quantity, TIERS).minQuantity());
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1})
    void rejectsQuantitiesBelowOne(int quantity) {
        assertThrows(BusinessRuleException.class, () -> policy.validate(quantity));
        assertThrows(BusinessRuleException.class, () -> policy.tierFor(quantity, TIERS));
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 7})
    void doesNotDependOnTierOrder(int quantity) {
        List<QuantityTier> shuffled = List.of(TIERS.get(2), TIERS.get(0), TIERS.get(3), TIERS.get(1));
        assertEquals(policy.tierFor(quantity, TIERS), policy.tierFor(quantity, shuffled));
    }
}
