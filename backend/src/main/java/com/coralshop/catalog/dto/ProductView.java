package com.coralshop.catalog.dto;

import java.math.BigDecimal;
import java.util.List;

public record ProductView(
        Long id,
        String name,
        String description,
        BigDecimal basePrice,
        Long categoryId,
        String categoryName,
        String brandName,
        String imageUrl,
        int totalStock,
        boolean isActive,
        List<VariantView> variants
) {

    public ProductView withVariants(List<VariantView> productVariants) {
        return new ProductView(id, name, description, basePrice, categoryId, categoryName, brandName, imageUrl,
                totalStock, isActive, productVariants);
    }
}
