package com.coralshop.pricing.service;

import com.coralshop.catalog.model.PurchasableProduct;
import com.coralshop.catalog.model.PurchasableVariant;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.customization.model.QuantityTier;
import com.coralshop.customization.model.Technique;
import com.coralshop.customization.model.ZoneRule;
import com.coralshop.customization.repository.CustomizationRepository;
import com.coralshop.pricing.dto.QuoteResponse;
import com.coralshop.pricing.dto.QuoteResponse.QuotedLine;
import com.coralshop.pricing.dto.QuoteResponse.QuotedZone;
import com.coralshop.pricing.dto.QuoteResponse.Tier;
import com.coralshop.pricing.model.LineAmounts;
import com.coralshop.pricing.model.LineSpec;
import com.coralshop.pricing.model.PricedLine;
import com.coralshop.pricing.model.PricedLine.PricedItem;
import com.coralshop.pricing.model.PricedLine.PricedZone;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Valida cada línea contra el catálogo y la personalización vigentes y recalcula sus
 * precios (D10): el navegador nunca envía importes.
 */
@Service
public class PricingService {

    private final ProductRepository productRepository;
    private final CustomizationRepository customizationRepository;
    private final QuantityPolicy quantityPolicy;

    public PricingService(ProductRepository productRepository, CustomizationRepository customizationRepository,
                          QuantityPolicy quantityPolicy) {
        this.productRepository = productRepository;
        this.customizationRepository = customizationRepository;
        this.quantityPolicy = quantityPolicy;
    }

    /** Cotiza el carrito: los errores de una línea no impiden cotizar las demás. */
    @Transactional(readOnly = true)
    public QuoteResponse quote(List<LineSpec> lines) {
        List<QuantityTier> tiers = customizationRepository.findTiers();
        List<QuotedLine> quoted = new ArrayList<>();
        BigDecimal subtotal = BigDecimal.ZERO.setScale(2);
        BigDecimal discount = BigDecimal.ZERO.setScale(2);
        boolean valid = true;
        for (int index = 0; index < lines.size(); index++) {
            LineSpec spec = lines.get(index);
            try {
                PricedLine line = price(spec, tiers);
                List<String> errors = line.items().stream()
                        .filter(item -> !item.inStock())
                        .map(item -> "Stock insuficiente para " + describe(item.variant())
                                + ": quedan " + item.variant().stock())
                        .toList();
                if (errors.isEmpty()) {
                    subtotal = subtotal.add(line.amounts().grossAmount());
                    discount = discount.add(line.amounts().discountAmount());
                } else {
                    valid = false;
                }
                quoted.add(toQuoted(index, line, errors));
            } catch (BusinessRuleException exception) {
                valid = false;
                quoted.add(new QuotedLine(index, spec.productId(), null, spec.techniqueCode(), List.of(),
                        spec.quantityTotal(), null, null, null, null, null, null, null,
                        List.of(exception.getMessage())));
            }
        }
        return new QuoteResponse(quoted, subtotal, discount, subtotal.subtract(discount), valid);
    }

    /** Valida y valoriza una línea; lanza {@link BusinessRuleException} si no se puede vender así. */
    @Transactional(readOnly = true)
    public PricedLine price(LineSpec spec) {
        return price(spec, customizationRepository.findTiers());
    }

    private PricedLine price(LineSpec spec, List<QuantityTier> tiers) {
        PurchasableProduct product = productRepository.findPurchasable(spec.productId())
                .filter(PurchasableProduct::active)
                .orElseThrow(() -> new BusinessRuleException("El producto " + spec.productId() + " no está disponible"));

        Technique technique = null;
        List<PricedZone> zones = List.of();
        if (spec.customized()) {
            technique = customizationRepository.findActiveTechnique(spec.techniqueCode())
                    .orElseThrow(() -> new BusinessRuleException("La técnica " + spec.techniqueCode() + " no existe"));
            zones = validZones(product, technique, spec.zoneCodes());
        } else if (!spec.zoneCodes().isEmpty()) {
            throw new BusinessRuleException("Elige una técnica para personalizar las zonas");
        } else if (spec.designId() != null) {
            throw new BusinessRuleException("Elige una técnica y al menos una zona para tu diseño");
        }

        List<PricedItem> items = validItems(product, spec.items());
        int quantityTotal = spec.quantityTotal();
        QuantityTier tier = quantityPolicy.tierFor(quantityTotal, tiers);

        BigDecimal customizationPrice = technique == null ? BigDecimal.ZERO
                : zones.stream().map(PricedZone::surcharge).reduce(technique.baseCost(), BigDecimal::add);
        LineAmounts amounts = LineAmounts.of(product.basePrice(), customizationPrice, quantityTotal,
                tier.discountPercent());
        return new PricedLine(product, technique, zones, spec.designId(), items, tier, amounts);
    }

    private List<PricedZone> validZones(PurchasableProduct product, Technique technique, List<String> zoneCodes) {
        if (!product.customizable()) {
            throw new BusinessRuleException("«" + product.name() + "» no se puede personalizar");
        }
        if (zoneCodes.isEmpty()) {
            throw new BusinessRuleException("Elige al menos una zona para el diseño");
        }
        if (new HashSet<>(zoneCodes).size() != zoneCodes.size()) {
            throw new BusinessRuleException("Hay zonas repetidas");
        }
        Map<String, ZoneRule> allowed = customizationRepository.findZoneRules(product.productTypeId()).stream()
                .filter(rule -> rule.techniqueId().equals(technique.id()))
                .collect(Collectors.toMap(ZoneRule::zoneCode, Function.identity()));
        List<PricedZone> zones = new ArrayList<>();
        for (String code : zoneCodes) {
            ZoneRule rule = allowed.get(code);
            if (rule == null) {
                throw new BusinessRuleException("La zona " + code + " no admite " + technique.name().toLowerCase()
                        + " en «" + product.name() + "»");
            }
            zones.add(new PricedZone(rule.zoneId(), rule.zoneCode(), rule.zoneName(), rule.surcharge()));
        }
        return zones;
    }

    private List<PricedItem> validItems(PurchasableProduct product, List<LineSpec.ItemSpec> specs) {
        if (specs.isEmpty()) {
            throw new BusinessRuleException("Indica al menos una talla y color");
        }
        Set<Long> ids = new HashSet<>();
        for (LineSpec.ItemSpec item : specs) {
            if (!ids.add(item.variantId())) {
                throw new BusinessRuleException("La misma talla y color aparece dos veces en la línea");
            }
        }
        Map<Long, PurchasableVariant> variants = productRepository.findVariantsByIds(ids).stream()
                .collect(Collectors.toMap(PurchasableVariant::id, Function.identity()));
        List<PricedItem> items = new ArrayList<>();
        for (LineSpec.ItemSpec item : specs) {
            PurchasableVariant variant = variants.get(item.variantId());
            if (variant == null || !variant.productId().equals(product.id()) || !variant.active()) {
                throw new BusinessRuleException("La variante " + item.variantId() + " no está disponible para «"
                        + product.name() + "»");
            }
            items.add(new PricedItem(variant, item.quantity()));
        }
        return items;
    }

    private static QuotedLine toQuoted(int index, PricedLine line, List<String> errors) {
        LineAmounts amounts = line.amounts();
        return new QuotedLine(index, line.product().id(), line.product().name(),
                line.technique() == null ? null : line.technique().code(),
                line.zones().stream().map(zone -> new QuotedZone(zone.code(), zone.name(), zone.surcharge())).toList(),
                amounts.quantityTotal(),
                new Tier(line.tier().minQuantity(), line.tier().label(), line.tier().discountPercent()),
                amounts.unitBasePrice(), amounts.unitCustomizationPrice(), amounts.unitPrice(),
                amounts.grossAmount(), amounts.discountAmount(), amounts.lineTotal(), errors);
    }

    public static String describe(PurchasableVariant variant) {
        return variant.sku() + " (" + variant.sizeName() + ", " + variant.colorName() + ")";
    }
}
