package com.coralshop.catalog.model;

import java.math.BigDecimal;

/** Datos de un producto que se necesitan para cotizarlo y venderlo. */
public record PurchasableProduct(Long id, String name, BigDecimal basePrice, boolean active, boolean customizable,
                                 Long productTypeId, String productTypeCode) {
}
