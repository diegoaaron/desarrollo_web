package com.coralshop.catalog.client;

import java.util.List;

/** Detalle de un producto de CJ, ya traducido desde su JSON. */
public record CjProduct(String pid, String name, String imageUrl, String sellPrice, List<Variant> variants) {

    public record Variant(String vid, String sku, String optionKey, String sellPrice) {
    }
}
