package com.coralshop.customization.service;

import com.coralshop.catalog.model.PurchasableProduct;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.customization.dto.CustomizationOptionsResponse;
import com.coralshop.customization.dto.CustomizationOptionsResponse.Preview;
import com.coralshop.customization.dto.CustomizationOptionsResponse.TechniqueOption;
import com.coralshop.customization.dto.CustomizationOptionsResponse.TierOption;
import com.coralshop.customization.dto.CustomizationOptionsResponse.ZoneOption;
import com.coralshop.customization.model.Technique;
import com.coralshop.customization.model.ZoneRule;
import com.coralshop.customization.repository.CustomizationRepository;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Opciones de personalización de un producto según su tipo. */
@Service
@Transactional(readOnly = true)
public class CustomizationService {

    private final ProductRepository productRepository;
    private final CustomizationRepository customizationRepository;

    public CustomizationService(ProductRepository productRepository, CustomizationRepository customizationRepository) {
        this.productRepository = productRepository;
        this.customizationRepository = customizationRepository;
    }

    public CustomizationOptionsResponse optionsFor(Long productId) {
        PurchasableProduct product = productRepository.findPurchasable(productId)
                .filter(PurchasableProduct::active)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado"));
        List<TierOption> tiers = customizationRepository.findTiers().stream()
                .map(tier -> new TierOption(tier.minQuantity(), tier.label(), tier.discountPercent()))
                .toList();
        String typeCode = product.productTypeCode();

        if (!product.customizable()) {
            return new CustomizationOptionsResponse(productId, typeCode, false, List.of(), tiers);
        }

        Map<String, List<ZoneRule>> rulesByTechnique = customizationRepository.findZoneRules(product.productTypeId())
                .stream().collect(Collectors.groupingBy(ZoneRule::techniqueCode));
        List<TechniqueOption> techniques = customizationRepository.findActiveTechniques().stream()
                .filter(technique -> rulesByTechnique.containsKey(technique.code()))
                .map(technique -> toOption(technique, rulesByTechnique.get(technique.code())))
                .toList();
        return new CustomizationOptionsResponse(productId, typeCode, true, techniques, tiers);
    }

    private static TechniqueOption toOption(Technique technique, List<ZoneRule> rules) {
        List<ZoneOption> zones = rules.stream()
                .map(rule -> new ZoneOption(rule.zoneCode(), rule.zoneName(), rule.surcharge(), rule.maxWidthCm(),
                        rule.maxHeightCm(), new Preview(rule.previewX(), rule.previewY(), rule.previewW(),
                        rule.previewH())))
                .toList();
        return new TechniqueOption(technique.code(), technique.name(), technique.description(), technique.baseCost(),
                zones);
    }
}
