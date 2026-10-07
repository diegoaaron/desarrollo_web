package com.coralshop.pricing.model;

import com.coralshop.catalog.model.PurchasableProduct;
import com.coralshop.catalog.model.PurchasableVariant;
import com.coralshop.customization.model.QuantityTier;
import com.coralshop.customization.model.Technique;
import java.math.BigDecimal;
import java.util.List;

/** Línea validada y con precios recalculados en el servidor (D10). technique es null si no se personaliza. */
public record PricedLine(PurchasableProduct product, Technique technique, List<PricedZone> zones, Long designId,
                         List<PricedItem> items, QuantityTier tier, LineAmounts amounts) {

    public record PricedZone(Long zoneId, String code, String name, BigDecimal surcharge) {
    }

    public record PricedItem(PurchasableVariant variant, int quantity) {

        public boolean inStock() {
            return variant.stock() >= quantity;
        }
    }
}
