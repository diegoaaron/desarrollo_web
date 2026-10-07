package com.coralshop.catalog.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.util.List;

/** Edición de un producto. Las variantes con id se modifican y las que no lo tienen se agregan. */
public record UpdateProductRequest(
        @NotBlank @Size(max = 180) String name,
        String description,
        @NotNull @DecimalMin("0.00") @Digits(integer = 10, fraction = 2) BigDecimal basePrice,
        @NotNull @Positive Long categoryId,
        @Positive Long productTypeId,
        boolean isCustomizable,
        @NotBlank @Pattern(regexp = "https?://.+", message = "La imagen debe ser una URL HTTP(S)") String imageUrl,
        boolean isActive,
        @NotNull @Valid List<Variant> variants
) {
    public record Variant(
            @Positive Long id,
            @NotNull @Positive Long sizeId,
            @NotNull @Positive Long colorId,
            @NotBlank @Size(max = 80) String sku,
            @NotNull @PositiveOrZero Integer stock,
            boolean isActive
    ) {
    }
}
