package com.coralshop.catalog.dto;

import java.util.List;

public record CjSearchResponse(List<Item> items, int totalPages) {

    public record Item(String pid, String name, String imageUrl, String supplierPrice) {
    }
}
