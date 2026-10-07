package com.coralshop.pricing.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import java.util.List;

public record QuoteRequest(@NotEmpty @Size(max = 50) @Valid List<CartLineRequest> lines) {
}
