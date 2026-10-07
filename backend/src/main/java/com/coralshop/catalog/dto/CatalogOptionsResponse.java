package com.coralshop.catalog.dto;

import java.util.List;

public record CatalogOptionsResponse(List<OptionView> sizes, List<OptionView> colors) {
}
