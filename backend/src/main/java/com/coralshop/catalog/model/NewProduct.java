package com.coralshop.catalog.model;

import java.math.BigDecimal;
import java.util.List;

/**
 * Producto listo para registrarse en el catálogo, venga del alta manual o de CJ.
 * {@code cjProductId} y {@code Variant.cjVariantId} son nulos en el alta manual.
 */
public record NewProduct(String name, String description, BigDecimal basePrice, Long categoryId,
                         String imageUrl, boolean active, String cjProductId, List<Variant> variants) {

    public record Variant(Long sizeId, Long colorId, String sku, int stock, String cjVariantId) {
    }
}
