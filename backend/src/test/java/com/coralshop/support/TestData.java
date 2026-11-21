package com.coralshop.support;

import com.coralshop.auth.dto.RegisterRequest;
import com.coralshop.auth.service.DevAdminService;
import com.coralshop.auth.service.RegistrationService;
import com.coralshop.catalog.dto.CreateProductRequest;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductTypeView;
import com.coralshop.catalog.dto.VariantView;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.catalog.service.ProductAdminService;
import com.coralshop.user.repository.UserRepository;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.springframework.boot.test.context.TestComponent;

/**
 * Prepara los datos de cada prueba a través de los mismos servicios que usa la API, para
 * que respeten las reglas del negocio. Todo lleva un sufijo aleatorio y no choca con otras
 * pruebas que compartan la base.
 */
@TestComponent
public class TestData {

    public static final String PASSWORD = "Clave-de-prueba-1";

    private final RegistrationService registrationService;
    private final DevAdminService adminService;
    private final ProductAdminService productAdminService;
    private final CatalogOptionRepository optionRepository;
    private final UserRepository userRepository;

    public TestData(RegistrationService registrationService, DevAdminService adminService,
                    ProductAdminService productAdminService, CatalogOptionRepository optionRepository,
                    UserRepository userRepository) {
        this.registrationService = registrationService;
        this.adminService = adminService;
        this.productAdminService = productAdminService;
        this.optionRepository = optionRepository;
        this.userRepository = userRepository;
    }

    /** Cuenta de cliente; devuelve su correo (el nombre con que se autentica). */
    public String customer() {
        String email = "cliente." + suffix() + "@prueba.pe";
        registrationService.register(new RegisterRequest("Cliente", "De Prueba", email, PASSWORD));
        return email;
    }

    public String admin() {
        String email = "admin." + suffix() + "@prueba.pe";
        adminService.ensureAdmin("Admin", "De Prueba", email, PASSWORD);
        return email;
    }

    public long idOf(String email) {
        return userRepository.findByEmailIgnoreCase(email).orElseThrow().getId();
    }

    /** Polo personalizable, a S/ 35, con una variante negra por talla y el stock indicado para cada una. */
    public Product polo(String... sizesWithStock) {
        Long typeId = optionRepository.findActiveProductTypes().stream()
                .filter(type -> type.code().equals("POLO")).map(ProductTypeView::id).findFirst().orElseThrow();
        Long categoryId = optionRepository.findActiveCategories().getFirst().id();
        Long black = idByName(optionRepository.findColors(), "Negro");
        String code = suffix();
        List<CreateProductRequest.Variant> variants = new ArrayList<>();
        for (String sizeWithStock : sizesWithStock) {
            String[] parts = sizeWithStock.split("=");
            variants.add(new CreateProductRequest.Variant(idByName(optionRepository.findSizes(), parts[0]), black,
                    "TEST-" + code + "-" + parts[0], Integer.parseInt(parts[1])));
        }
        long id = productAdminService.create(new CreateProductRequest("Polo de prueba " + code, null,
                new BigDecimal("35.00"), categoryId, typeId, true, "https://example.com/polo.png", true, variants));
        return new Product(id, productAdminService.product(id).variants());
    }

    public int stockOf(Product product, String size) {
        return productAdminService.product(product.id()).variants().stream()
                .filter(variant -> variant.size().equals(size)).findFirst().orElseThrow().stock();
    }

    private static Long idByName(List<OptionView> options, String name) {
        return options.stream().filter(option -> option.name().equals(name)).map(OptionView::id)
                .findFirst().orElseThrow();
    }

    private static String suffix() {
        return UUID.randomUUID().toString().substring(0, 8);
    }

    public record Product(long id, List<VariantView> variants) {

        public long variant(String size) {
            return variants.stream().filter(variant -> variant.size().equals(size)).findFirst().orElseThrow().id();
        }
    }
}
