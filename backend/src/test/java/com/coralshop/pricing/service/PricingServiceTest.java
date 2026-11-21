package com.coralshop.pricing.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyCollection;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coralshop.catalog.model.PurchasableProduct;
import com.coralshop.catalog.model.PurchasableVariant;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.customization.model.QuantityTier;
import com.coralshop.customization.model.Technique;
import com.coralshop.customization.model.ZoneRule;
import com.coralshop.customization.repository.CustomizationRepository;
import com.coralshop.pricing.dto.QuoteResponse;
import com.coralshop.pricing.model.LineSpec;
import com.coralshop.pricing.model.LineSpec.ItemSpec;
import com.coralshop.pricing.model.PricedLine;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Reglas de cotización (fases.md §2.1) sobre repositorios simulados: el precio lo calcula
 * siempre el servidor (D10) a partir del catálogo, la técnica, las zonas y la escala (D2).
 */
class PricingServiceTest {

    private static final long POLO_ID = 10L;
    private static final long POLO_TYPE_ID = 1L;
    private static final long ESTAMPADO_ID = 1L;
    private static final long BORDADO_ID = 2L;

    private static final List<QuantityTier> TIERS = List.of(
            new QuantityTier(1, "Unidad", new BigDecimal("0.00")),
            new QuantityTier(3, "Paquete de 3", new BigDecimal("5.00")),
            new QuantityTier(6, "Paquete de 6", new BigDecimal("10.00")),
            new QuantityTier(12, "Docena", new BigDecimal("15.00")));

    private static final PurchasableVariant POLO_S = variant(101L, POLO_ID, "S", 20);
    private static final PurchasableVariant POLO_M = variant(102L, POLO_ID, "M", 20);
    private static final PurchasableVariant POLO_L = variant(103L, POLO_ID, "L", 3);

    private final ProductRepository productRepository = mock(ProductRepository.class);
    private final CustomizationRepository customizationRepository = mock(CustomizationRepository.class);
    private final PricingService service = new PricingService(productRepository, customizationRepository,
            new QuantityPolicy());

    @BeforeEach
    void catalog() {
        when(customizationRepository.findTiers()).thenReturn(TIERS);
        when(productRepository.findPurchasable(anyLong())).thenReturn(Optional.empty());
        when(productRepository.findPurchasable(POLO_ID)).thenReturn(Optional.of(polo(true, true)));
        when(productRepository.findVariantsByIds(anyCollection())).thenReturn(List.of(POLO_S, POLO_M, POLO_L));
        when(customizationRepository.findActiveTechnique("BORDADO")).thenReturn(Optional.of(
                new Technique(BORDADO_ID, "BORDADO", "Bordado", "Bordado a hilo", new BigDecimal("15.00"))));
        when(customizationRepository.findActiveTechnique("ESTAMPADO")).thenReturn(Optional.of(
                new Technique(ESTAMPADO_ID, "ESTAMPADO", "Estampado", "DTF", new BigDecimal("8.00"))));
        when(customizationRepository.findZoneRules(POLO_TYPE_ID)).thenReturn(List.of(
                zone(BORDADO_ID, "BORDADO", 1L, "PECHO_IZQ", "8.00"),
                zone(ESTAMPADO_ID, "ESTAMPADO", 1L, "PECHO_IZQ", "5.00"),
                zone(ESTAMPADO_ID, "ESTAMPADO", 3L, "ESPALDA", "15.00")));
    }

    /** Historia de referencia: 12 polos bordados en el pecho, 4 S + 4 M + 4 L, a S/ 35. */
    @Test
    void pricesTheReferenceStoryWithTheDozenDiscount() {
        PricedLine line = service.price(spec("BORDADO", List.of("PECHO_IZQ"), 7L,
                new ItemSpec(101L, 4), new ItemSpec(102L, 4), new ItemSpec(103L, 4)));

        // 35 + (15 de bordado + 8 de la zona) = 58 por unidad; 58 × 12 = 696; 15 % = 104.40.
        assertThat(line.tier().minQuantity()).isEqualTo(12);
        assertThat(line.amounts().unitCustomizationPrice()).isEqualByComparingTo("23.00");
        assertThat(line.amounts().unitPrice()).isEqualByComparingTo("58.00");
        assertThat(line.amounts().grossAmount()).isEqualByComparingTo("696.00");
        assertThat(line.amounts().discountAmount()).isEqualByComparingTo("104.40");
        assertThat(line.amounts().lineTotal()).isEqualByComparingTo("591.60");
        assertThat(line.items()).hasSize(3);
    }

    @Test
    void addsTheSurchargeOfEveryChosenZone() {
        PricedLine line = service.price(spec("ESTAMPADO", List.of("PECHO_IZQ", "ESPALDA"), 7L,
                new ItemSpec(101L, 1)));

        // 8 de estampado + 5 del pecho + 15 de la espalda.
        assertThat(line.amounts().unitCustomizationPrice()).isEqualByComparingTo("28.00");
        assertThat(line.amounts().discountAmount()).isEqualByComparingTo("0.00");
    }

    @Test
    void sellsAPlainProductWithoutCustomizationCost() {
        PricedLine line = service.price(spec(null, List.of(), null, new ItemSpec(101L, 3), new ItemSpec(102L, 1)));

        assertThat(line.technique()).isNull();
        assertThat(line.tier().minQuantity()).isEqualTo(3);
        assertThat(line.amounts().unitPrice()).isEqualByComparingTo("35.00");
        assertThat(line.amounts().lineTotal()).isEqualByComparingTo("133.00");
    }

    @Test
    void rejectsAZoneThatDoesNotAcceptTheTechnique() {
        assertThatThrownBy(() -> service.price(spec("BORDADO", List.of("ESPALDA"), 7L, new ItemSpec(101L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessageContaining("ESPALDA");
    }

    @Test
    void rejectsRepeatedZones() {
        assertThatThrownBy(() -> service.price(spec("ESTAMPADO", List.of("PECHO_IZQ", "PECHO_IZQ"), 7L,
                new ItemSpec(101L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessage("Hay zonas repetidas");
    }

    @Test
    void rejectsZonesWithoutATechnique() {
        assertThatThrownBy(() -> service.price(spec(null, List.of("PECHO_IZQ"), null, new ItemSpec(101L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessage("Elige una técnica para personalizar las zonas");
    }

    @Test
    void rejectsCustomizingAProductThatDoesNotAllowIt() {
        when(productRepository.findPurchasable(POLO_ID)).thenReturn(Optional.of(polo(true, false)));

        assertThatThrownBy(() -> service.price(spec("ESTAMPADO", List.of("PECHO_IZQ"), 7L, new ItemSpec(101L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessageContaining("no se puede personalizar");
    }

    @Test
    void rejectsAnInactiveProduct() {
        when(productRepository.findPurchasable(POLO_ID)).thenReturn(Optional.of(polo(false, true)));

        assertThatThrownBy(() -> service.price(spec(null, List.of(), null, new ItemSpec(101L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessageContaining("no está disponible");
    }

    @Test
    void rejectsAVariantOfAnotherProduct() {
        when(productRepository.findVariantsByIds(anyCollection())).thenReturn(List.of(variant(901L, 99L, "S", 5)));

        assertThatThrownBy(() -> service.price(spec(null, List.of(), null, new ItemSpec(901L, 1))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessageContaining("La variante 901");
    }

    @Test
    void rejectsTheSameVariantTwiceInALine() {
        assertThatThrownBy(() -> service.price(spec(null, List.of(), null,
                new ItemSpec(101L, 1), new ItemSpec(101L, 2))))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessageContaining("aparece dos veces");
    }

    /** La cotización no se detiene en la primera línea con error: informa cada una y marca el carrito inválido. */
    @Test
    void quoteReportsEachInvalidLineAndExcludesItFromTheTotals() {
        QuoteResponse quote = service.quote(List.of(
                spec(null, List.of(), null, new ItemSpec(101L, 2)),
                spec(null, List.of(), null, new ItemSpec(103L, 5)),
                new LineSpec(999L, null, List.of(), null, List.of(new ItemSpec(101L, 1)))));

        assertThat(quote.valid()).isFalse();
        assertThat(quote.lines()).hasSize(3);
        assertThat(quote.lines().get(0).errors()).isEmpty();
        assertThat(quote.lines().get(1).errors()).singleElement().asString().contains("quedan 3");
        assertThat(quote.lines().get(2).errors()).singleElement().asString().contains("no está disponible");
        assertThat(quote.subtotal()).isEqualByComparingTo("70.00");
        assertThat(quote.total()).isEqualByComparingTo("70.00");
    }

    private static LineSpec spec(String technique, List<String> zones, Long designId, ItemSpec... items) {
        return new LineSpec(POLO_ID, technique, zones, designId, List.of(items));
    }

    private static PurchasableProduct polo(boolean active, boolean customizable) {
        return new PurchasableProduct(POLO_ID, "Polo clásico", new BigDecimal("35.00"), active, customizable,
                POLO_TYPE_ID, "POLO");
    }

    private static PurchasableVariant variant(Long id, Long productId, String size, int stock) {
        return new PurchasableVariant(id, productId, "POLO-NEG-" + size, size, "Negro", stock, true);
    }

    private static ZoneRule zone(Long techniqueId, String techniqueCode, Long zoneId, String zoneCode,
                                 String surcharge) {
        BigDecimal ten = BigDecimal.TEN;
        return new ZoneRule(techniqueId, techniqueCode, zoneId, zoneCode, zoneCode, ten, ten,
                new BigDecimal(surcharge), ten, ten, ten, ten);
    }
}
