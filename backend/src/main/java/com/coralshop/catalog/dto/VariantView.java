package com.coralshop.catalog.dto;

public record VariantView(Long id, String sku, Long sizeId, String size, Long colorId, String color, String colorHex,
                          int stock, boolean isActive) {
}
