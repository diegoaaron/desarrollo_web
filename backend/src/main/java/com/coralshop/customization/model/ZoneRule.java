package com.coralshop.customization.model;

import java.math.BigDecimal;

/** Una zona que admite una técnica en un tipo de producto, con sus medidas, recargo y vista previa. */
public record ZoneRule(Long techniqueId, String techniqueCode, Long zoneId, String zoneCode, String zoneName,
                       BigDecimal maxWidthCm, BigDecimal maxHeightCm, BigDecimal surcharge,
                       BigDecimal previewX, BigDecimal previewY, BigDecimal previewW, BigDecimal previewH) {
}
