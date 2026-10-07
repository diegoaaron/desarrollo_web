package com.coralshop.catalog.dto;

import java.util.List;

public record CjProductResponse(String pid, String name, String imageUrl, String supplierPrice,
                                List<Variant> variants, boolean alreadyImported) {

    public record Variant(String vid, String sku, String optionKey, String supplierPrice) {
    }
}
