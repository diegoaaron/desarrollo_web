package com.coralshop.catalog.client;

import java.util.List;

/** Página de resultados de búsqueda de CJ, ya traducida desde su JSON. */
public record CjSearchPage(List<Item> items, int totalPages) {

    public record Item(String pid, String name, String imageUrl, String sellPrice) {
    }
}
