package com.coralshop.catalog.model;

import java.math.BigDecimal;
import java.util.List;

/** Producto validado y normalizado, listo para registrarse en el catálogo. */
public record NewProduct(String name, String description, BigDecimal basePrice, Long categoryId,
                         Long productTypeId, boolean customizable, String imageUrl, boolean active,
                         List<Variant> variants) {

    public record Variant(Long sizeId, Long colorId, String sku, int stock) {
    }
}
