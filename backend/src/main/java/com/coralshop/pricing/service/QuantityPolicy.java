package com.coralshop.pricing.service;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.customization.model.QuantityTier;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Component;

/**
 * Regla de cantidad (D2, opción A): se acepta cualquier cantidad ≥ 1 de un mismo diseño y
 * se aplica la escala más alta alcanzada.
 */
@Component
public class QuantityPolicy {

    public void validate(int quantityTotal) {
        if (quantityTotal < 1) {
            throw new BusinessRuleException("La cantidad de un diseño debe ser al menos 1");
        }
    }

    /** Escala con mayor min_quantity que no supere la cantidad. */
    public QuantityTier tierFor(int quantityTotal, List<QuantityTier> tiers) {
        validate(quantityTotal);
        return tiers.stream()
                .filter(tier -> tier.minQuantity() <= quantityTotal)
                .max(Comparator.comparingInt(QuantityTier::minQuantity))
                .orElseThrow(() -> new IllegalStateException("No hay una escala de mayoreo para 1 unidad"));
    }
}
