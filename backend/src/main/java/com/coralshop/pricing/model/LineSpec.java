package com.coralshop.pricing.model;

import java.util.List;

/**
 * Lo que el cliente pide en una línea: un producto, opcionalmente personalizado con una
 * técnica, unas zonas y un diseño, repartido entre variantes (tallas y colores).
 */
public record LineSpec(Long productId, String techniqueCode, List<String> zoneCodes, Long designId,
                       List<ItemSpec> items) {

    public record ItemSpec(Long variantId, int quantity) {
    }

    public boolean customized() {
        return techniqueCode != null;
    }

    public int quantityTotal() {
        return items.stream().mapToInt(ItemSpec::quantity).sum();
    }
}
