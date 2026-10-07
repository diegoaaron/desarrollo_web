package com.coralshop.catalog.model;

import java.math.BigDecimal;
import java.util.List;

/**
 * Cambios validados de un producto existente. Las variantes con id se actualizan; las que
 * no lo tienen se agregan. Las variantes que no aparecen no se tocan.
 */
public record ProductUpdate(String name, String description, BigDecimal basePrice, Long categoryId,
                            Long productTypeId, boolean customizable, String imageUrl, boolean active,
                            List<Variant> variants) {

    public record Variant(Long id, Long sizeId, Long colorId, String sku, int stock, boolean active) {
    }
}
