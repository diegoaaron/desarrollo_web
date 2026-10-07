package com.coralshop.order.model;

/** Unidades de una variante que un pedido tomó del inventario. */
public record StockMovement(Long variantId, int quantity) {
}
