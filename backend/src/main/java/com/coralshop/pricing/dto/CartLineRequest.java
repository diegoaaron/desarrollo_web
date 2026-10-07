package com.coralshop.pricing.dto;

import com.coralshop.pricing.model.LineSpec;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import java.util.List;
import java.util.Locale;

/** Línea del carrito tal como la envía el navegador (cotización y pedido). Sin precios: los pone el servidor. */
public record CartLineRequest(
        @NotNull @Positive Long productId,
        @Size(max = 30) String techniqueCode,
        @Size(max = 10) List<@NotBlank @Size(max = 30) String> zoneCodes,
        @Positive Long designId,
        @NotEmpty @Size(max = 100) @Valid List<Item> items
) {
    public record Item(
            @NotNull @Positive Long variantId,
            @NotNull @Min(1) @Max(10000) Integer quantity
    ) {
    }

    public LineSpec toSpec() {
        String technique = techniqueCode == null || techniqueCode.isBlank()
                ? null : techniqueCode.trim().toUpperCase(Locale.ROOT);
        List<String> zones = zoneCodes == null ? List.of()
                : zoneCodes.stream().map(code -> code.trim().toUpperCase(Locale.ROOT)).toList();
        return new LineSpec(productId, technique, zones, designId,
                items.stream().map(item -> new LineSpec.ItemSpec(item.variantId(), item.quantity())).toList());
    }
}
