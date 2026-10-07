package com.coralshop.catalog.model;

/** Variante con lo que se copia al pedido (SKU, talla, color) y su stock actual. */
public record PurchasableVariant(Long id, Long productId, String sku, String sizeName, String colorName, int stock,
                                 boolean active) {
}
