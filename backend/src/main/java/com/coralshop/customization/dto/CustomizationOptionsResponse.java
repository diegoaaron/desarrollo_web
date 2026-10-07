package com.coralshop.customization.dto;

import java.math.BigDecimal;
import java.util.List;

/**
 * Lo que necesita el personalizador de un producto: técnicas con sus zonas válidas
 * (recargo, medidas y recuadro de vista previa en % de la imagen) y escalas de mayoreo.
 */
public record CustomizationOptionsResponse(Long productId, String productTypeCode, boolean isCustomizable,
                                           List<TechniqueOption> techniques, List<TierOption> tiers) {

    public record TechniqueOption(String code, String name, String description, BigDecimal baseCost,
                                  List<ZoneOption> zones) {
    }

    public record ZoneOption(String code, String name, BigDecimal surcharge, BigDecimal maxWidthCm,
                             BigDecimal maxHeightCm, Preview preview) {
    }

    public record Preview(BigDecimal x, BigDecimal y, BigDecimal width, BigDecimal height) {
    }

    public record TierOption(int minQuantity, String label, BigDecimal discountPercent) {
    }
}
