package com.coralshop.demo.service;

import com.coralshop.address.dto.AddressRequest;
import com.coralshop.address.service.AddressService;
import com.coralshop.auth.dto.RegisterRequest;
import com.coralshop.auth.service.DevAdminService;
import com.coralshop.auth.service.RegistrationService;
import com.coralshop.catalog.dto.CatalogOptionsResponse;
import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.CreateProductRequest;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductTypeView;
import com.coralshop.catalog.dto.VariantView;
import com.coralshop.catalog.service.CatalogService;
import com.coralshop.catalog.service.ProductAdminService;
import com.coralshop.design.service.DesignService;
import com.coralshop.order.dto.CreateOrderRequest;
import com.coralshop.order.dto.StatusChangeRequest;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.repository.OrderRepository;
import com.coralshop.order.service.OrderAdminService;
import com.coralshop.order.service.OrderService;
import com.coralshop.payment.dto.PaymentRequest;
import com.coralshop.payment.service.PaymentService;
import com.coralshop.pricing.dto.CartLineRequest;
import com.coralshop.user.repository.UserRepository;
import java.awt.Color;
import java.math.BigDecimal;
import java.time.Year;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Carga los datos de demostración (fase 5.2): catálogo de los cuatro tipos de producto,
 * clientes ficticios con su dirección y su logo, y pedidos en todos los estados.
 * <p>
 * No escribe SQL: todo pasa por los mismos servicios que usa la API, así que los datos
 * cumplen las reglas del negocio, descuentan stock, registran pagos simulados y publican los
 * eventos que dejan auditoría y notificaciones. Corre en una sola transacción: o se carga
 * todo o nada, y si ya existe el primer cliente demo no hace nada (es idempotente).
 */
@Service
public class DemoDataService {

    private static final Logger log = LoggerFactory.getLogger(DemoDataService.class);

    /** Correo del primer cliente demo: si existe, la demo ya se cargó. */
    static final String MARKER_EMAIL = "renzo.paredes@demo.coralshop.pe";

    private static final String APPROVED_CARD = "4111 1111 1111 1111";
    private static final String DECLINED_CARD = "4000 0000 0000 0002";

    private final DevAdminService adminService;
    private final RegistrationService registrationService;
    private final UserRepository userRepository;
    private final ProductAdminService productAdminService;
    private final CatalogService catalogService;
    private final AddressService addressService;
    private final DesignService designService;
    private final OrderService orderService;
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final OrderAdminService orderAdminService;

    public DemoDataService(DevAdminService adminService, RegistrationService registrationService,
                           UserRepository userRepository, ProductAdminService productAdminService,
                           CatalogService catalogService, AddressService addressService, DesignService designService,
                           OrderService orderService, OrderRepository orderRepository, PaymentService paymentService,
                           OrderAdminService orderAdminService) {
        this.adminService = adminService;
        this.registrationService = registrationService;
        this.userRepository = userRepository;
        this.productAdminService = productAdminService;
        this.catalogService = catalogService;
        this.addressService = addressService;
        this.designService = designService;
        this.orderService = orderService;
        this.orderRepository = orderRepository;
        this.paymentService = paymentService;
        this.orderAdminService = orderAdminService;
    }

    @Transactional
    public void load(String adminEmail, String adminPassword, String customerPassword) {
        if (userRepository.existsByEmailIgnoreCase(MARKER_EMAIL)) {
            log.info("Datos demo ya cargados ({} existe); no se modifican", MARKER_EMAIL);
            return;
        }
        adminService.ensureAdmin("Administración", "Coral Shop", adminEmail, adminPassword);
        long adminId = userRepository.findByEmailIgnoreCase(adminEmail).orElseThrow().getId();

        Catalog catalog = new Catalog(productAdminService.catalogOptions(), catalogService.activeCategories());
        Products products = createProducts(catalog);
        Customers customers = createCustomers(customerPassword);
        createOrders(adminId, products, customers);
        log.info("Datos demo cargados: 8 productos, 5 clientes y 8 pedidos");
    }

    // ---------------------------------------------------------------------------------
    // Catálogo
    // ---------------------------------------------------------------------------------

    private Products createProducts(Catalog c) {
        long unisex = c.category("Unisex");
        long hombre = c.category("Hombre");
        long mujer = c.category("Mujer");
        List<String> tallas = List.of("S", "M", "L", "XL");

        Product poloClasico = product(c, "Polo clásico de algodón",
                "Polo de algodón peinado 30/1, cuello redondo y costuras reforzadas. La base ideal para estampar o "
                        + "bordar el logo de tu equipo, tu marca o tu promoción.",
                "35.00", unisex, "POLO", true, "/demo/polo-clasico.png", "POLO-CLA",
                stock(tallas, List.of("Negro", "Blanco", "Azul"), 30));
        Product poloOversize = product(c, "Polo oversize",
                "Corte holgado de hombro caído en algodón de 200 g. Pensado para estampados grandes en el pecho o la "
                        + "espalda.",
                "45.00", unisex, "POLO", true, "/demo/polo-oversize.png", "POLO-OVS",
                stock(tallas, List.of("Beige", "Negro"), 20));
        Product poloLima = product(c, "Polo Coral Edición Lima",
                "Edición limitada con el isotipo de Coral Shop ya estampado. Se vende tal cual, sin personalizar.",
                "49.00", hombre, "POLO", false, "/demo/polo-edicion-lima.png", "POLO-LIM",
                Map.of("S|Blanco", 6, "M|Blanco", 4, "L|Blanco", 2, "XL|Blanco", 0));
        Product poleraCapucha = product(c, "Polera con capucha",
                "Polera de franela perchada con capucha, bolsillo canguro y puños acanalados. Admite estampado en "
                        + "pecho, espalda y mangas, o bordado en el pecho.",
                "89.00", unisex, "POLERA", true, "/demo/polera-capucha.png", "POLERA-CAP",
                stock(tallas, List.of("Rojo", "Negro"), 15));
        Product poleraCuello = product(c, "Polera cuello redondo",
                "Polera sin capucha en franela ligera, ideal para uniformes de equipo y promociones.",
                "75.00", mujer, "POLERA", true, "/demo/polera-cuello-redondo.png", "POLERA-CR",
                stock(tallas, List.of("Azul", "Beige"), 15));
        Product gorraTrucker = product(c, "Gorra trucker",
                "Gorra de cinco paneles con malla trasera y broche regulable. Frente rígido para bordado o "
                        + "estampado.",
                "39.00", unisex, "GORRA", true, "/demo/gorra-trucker.png", "GORRA-TRK",
                stock(List.of("Única"), List.of("Negro", "Blanco"), 40));
        Product gorraDad = product(c, "Gorra dad hat",
                "Gorra de drill lavado, copa baja y visera curva. Luce mejor con un bordado pequeño al frente.",
                "35.00", unisex, "GORRA", true, "/demo/gorra-dad-hat.png", "GORRA-DAD",
                stock(List.of("Única"), List.of("Beige", "Azul"), 40));
        Product tote = product(c, "Tote bag de lona",
                "Bolsa de lona cruda de 12 oz con asas largas. Dos caras para estampar; bordado solo en la cara A.",
                "25.00", unisex, "TOTE", true, "/demo/tote-lona.png", "TOTE-LON",
                stock(List.of("Única"), List.of("Beige", "Negro"), 60));
        return new Products(poloClasico, poloOversize, poloLima, poleraCapucha, poleraCuello, gorraTrucker, gorraDad,
                tote);
    }

    private Product product(Catalog c, String name, String description, String price, long categoryId,
                            String typeCode, boolean customizable, String imageUrl, String skuPrefix,
                            Map<String, Integer> stockBySizeAndColor) {
        List<CreateProductRequest.Variant> variants = new ArrayList<>();
        stockBySizeAndColor.forEach((key, stock) -> {
            String[] parts = key.split("\\|");
            String sku = "DEMO-" + skuPrefix + "-" + parts[1].substring(0, 3).toUpperCase() + "-"
                    + (parts[0].equals("Única") ? "U" : parts[0]);
            variants.add(new CreateProductRequest.Variant(c.size(parts[0]), c.color(parts[1]), sku, stock));
        });
        long id = productAdminService.create(new CreateProductRequest(name, description, new BigDecimal(price),
                categoryId, c.type(typeCode), customizable, imageUrl, true, variants));
        return new Product(id, productAdminService.product(id).variants());
    }

    /** Mismo stock para cada talla y color, en orden (LinkedHashMap) para que los SKU salgan ordenados. */
    private static Map<String, Integer> stock(List<String> sizes, List<String> colors, int units) {
        Map<String, Integer> stock = new LinkedHashMap<>();
        for (String color : colors) {
            for (String size : sizes) {
                stock.put(size + "|" + color, units);
            }
        }
        return stock;
    }

    // ---------------------------------------------------------------------------------
    // Clientes (ficticios: nombres, correos, teléfonos y direcciones inventados)
    // ---------------------------------------------------------------------------------

    private Customers createCustomers(String password) {
        Customer renzo = customer("Renzo", "Paredes Salazar", MARKER_EMAIL, password,
                new AddressRequest("Renzo Paredes Salazar", "987 654 321", "Lima", "Lima", "Miraflores",
                        "Av. Malecón de la Reserva 610, dpto. 302", "Frente al parque Salazar", true),
                DemoLogoFactory.badge("CV", "RUNNING CLUB", new Color(0x3C6E8F), new Color(0xFFB347)), "logo-club.png");
        Customer valeria = customer("Valeria", "Quispe Huamán", "valeria.quispe@demo.coralshop.pe", password,
                new AddressRequest("Valeria Quispe Huamán", "912 345 678", "Lima", "Lima", "San Miguel",
                        "Jr. Los Cedros 245", null, true),
                DemoLogoFactory.badge("VQ", "ILUSTRACIÓN", new Color(0x6D2E46), new Color(0xD9AFAF)), "firma.png");
        Customer lucia = customer("Lucía", "Fernández Cornejo", "lucia.fernandez@demo.coralshop.pe", password,
                new AddressRequest("Lucía Fernández Cornejo", "958 112 233", "Arequipa", "Arequipa", "Yanahuara",
                        "Calle Jerusalén 118", "Portón verde", true),
                DemoLogoFactory.badge("FA", "FERIA ECO", new Color(0x4E7A5A), new Color(0xECE2D0)), "feria.png");
        Customer mateo = customer("Mateo", "Rojas Villanueva", "mateo.rojas@demo.coralshop.pe", password,
                new AddressRequest("Mateo Rojas Villanueva", "934 567 890", "Lima", "Lima", "Surco",
                        "Av. Primavera 1450, of. 5", null, true),
                DemoLogoFactory.badge("MR", "BARBERÍA", new Color(0x26232A), new Color(0xFF5331)), "barberia.png");
        Customer camila = customer("Camila", "Torres Ancajima", "camila.torres@demo.coralshop.pe", password,
                new AddressRequest("Camila Torres Ancajima", "976 543 210", "Lima", "Lima", "Jesús María",
                        "Av. Salaverry 2020", null, true),
                DemoLogoFactory.badge("CT", "PROMO 2026", new Color(0x8A6D3B), new Color(0xFBF7F2)), "promo.png");
        return new Customers(renzo, valeria, lucia, mateo, camila);
    }

    private Customer customer(String firstName, String lastName, String email, String password,
                              AddressRequest address, byte[] logo, String logoName) {
        long id = registrationService.register(new RegisterRequest(firstName, lastName, email, password)).id();
        long addressId = addressService.create(id, address).id();
        long designId = designService.upload(id, logoName, logo).id();
        return new Customer(id, addressId, designId);
    }

    // ---------------------------------------------------------------------------------
    // Pedidos: uno o más en cada estado de la máquina (fases.md §1.5)
    // ---------------------------------------------------------------------------------

    private void createOrders(long adminId, Products p, Customers c) {
        // Historia de referencia: 12 polos con el logo bordado en el pecho (4 S, 4 M, 4 L), hasta ENTREGADO.
        String reference = order(c.renzo(), "LIMA_METROPOLITANA", "Para el club de running del malecón",
                line(p.poloClasico(), "BORDADO", List.of("PECHO_IZQ"), c.renzo().designId(),
                        item(p.poloClasico(), "S", "Negro", 4), item(p.poloClasico(), "M", "Negro", 4),
                        item(p.poloClasico(), "L", "Negro", 4)));
        pay(c.renzo(), reference, APPROVED_CARD);
        advance(adminId, c.renzo(), reference, "Diseño aprobado; pasa a bordado",
                "Bordado y control de calidad listos", "Entregado al courier", "Recibido por el cliente");

        String valeria = order(c.valeria(), "LIMA_METROPOLITANA", null,
                line(p.poleraCapucha(), "ESTAMPADO", List.of("ESPALDA"), c.valeria().designId(),
                        item(p.poleraCapucha(), "M", "Negro", 1)));
        pay(c.valeria(), valeria, APPROVED_CARD);
        advance(adminId, c.valeria(), valeria, "Arte revisado; en impresión DTF");

        String lucia = order(c.lucia(), "PROVINCIAS", "Bolsas para el stand de la feria",
                line(p.tote(), "ESTAMPADO", List.of("TOTE_CARA_A"), c.lucia().designId(),
                        item(p.tote(), "Única", "Beige", 6)));
        pay(c.lucia(), lucia, APPROVED_CARD);
        advance(adminId, c.lucia(), lucia, null, null, "Enviado por agencia a Arequipa");

        String mateo = order(c.mateo(), "RECOJO_TIENDA", null,
                line(p.gorraTrucker(), "BORDADO", List.of("GORRA_FRENTE"), c.mateo().designId(),
                        item(p.gorraTrucker(), "Única", "Negro", 3)));
        pay(c.mateo(), mateo, APPROVED_CARD);
        advance(adminId, c.mateo(), mateo, null, "Listo para recoger en tienda");

        // Compra sin personalizar, pagada y aún sin pasar a producción.
        String lima = order(c.mateo(), "LIMA_METROPOLITANA", null,
                line(p.poloLima(), null, List.of(), null, item(p.poloLima(), "M", "Blanco", 1)));
        pay(c.mateo(), lima, APPROVED_CARD);

        // Pendiente: el primer intento de pago fue rechazado (tarjeta terminada en 0002).
        String camila = order(c.camila(), "LIMA_METROPOLITANA", "Polos para la promoción del colegio",
                line(p.poloOversize(), "ESTAMPADO", List.of("PECHO_CENTRO"), c.camila().designId(),
                        item(p.poloOversize(), "M", "Beige", 2)));
        pay(c.camila(), camila, DECLINED_CARD);

        // Pedido de varias líneas (polera + gorra con el mismo logo), pagado.
        String valeriaPack = order(c.valeria(), "LIMA_METROPOLITANA", null,
                line(p.poleraCuello(), "BORDADO", List.of("PECHO_IZQ"), c.valeria().designId(),
                        item(p.poleraCuello(), "S", "Azul", 1), item(p.poleraCuello(), "M", "Azul", 2)),
                line(p.gorraDad(), "BORDADO", List.of("GORRA_FRENTE"), c.valeria().designId(),
                        item(p.gorraDad(), "Única", "Beige", 3)));
        pay(c.valeria(), valeriaPack, APPROVED_CARD);

        // Cancelado por el administrador: el stock vuelve al inventario.
        String cancelled = order(c.camila(), "RECOJO_TIENDA", null,
                line(p.gorraDad(), "ESTAMPADO", List.of("GORRA_FRENTE"), c.camila().designId(),
                        item(p.gorraDad(), "Única", "Azul", 2)));
        orderAdminService.changeStatus(adminId, orderId(c.camila(), cancelled),
                new StatusChangeRequest(OrderStatus.CANCELADO.name(), "Cancelado a pedido de la clienta"));
    }

    private String order(Customer customer, String shipping, String note, CartLineRequest... lines) {
        Long addressId = shipping.equals("RECOJO_TIENDA") ? null : customer.addressId();
        String phone = addressId == null ? "999 000 111" : null;
        return orderService.create(customer.id(),
                new CreateOrderRequest(List.of(lines), addressId, shipping, phone, note)).orderCode();
    }

    private void pay(Customer customer, String orderCode, String card) {
        paymentService.pay(customer.id(), orderCode,
                new PaymentRequest(card, "CLIENTE DEMO", 12, Year.now().getValue() + 3, "123"));
    }

    /** Avanza desde PAGADO un paso por comentario: EN_PRODUCCION, LISTO_PARA_ENVIO, ENVIADO, ENTREGADO. */
    private void advance(long adminId, Customer customer, String orderCode, String... comments) {
        List<OrderStatus> path = List.of(OrderStatus.EN_PRODUCCION, OrderStatus.LISTO_PARA_ENVIO,
                OrderStatus.ENVIADO, OrderStatus.ENTREGADO);
        long orderId = orderId(customer, orderCode);
        for (int step = 0; step < comments.length; step++) {
            orderAdminService.changeStatus(adminId, orderId,
                    new StatusChangeRequest(path.get(step).name(), comments[step]));
        }
    }

    private long orderId(Customer customer, String orderCode) {
        return orderRepository.findIdByCodeAndUser(orderCode, customer.id()).orElseThrow();
    }

    private static CartLineRequest line(Product product, String technique, List<String> zones, Long designId,
                                        CartLineRequest.Item... items) {
        return new CartLineRequest(product.id(), technique, zones, designId, List.of(items));
    }

    private static CartLineRequest.Item item(Product product, String size, String color, int quantity) {
        return new CartLineRequest.Item(product.variant(size, color), quantity);
    }

    // ---------------------------------------------------------------------------------

    private record Catalog(CatalogOptionsResponse options, List<CategoryView> categories) {

        long category(String name) {
            return categories.stream().filter(category -> category.name().equals(name)).map(CategoryView::id)
                    .findFirst().orElseThrow(() -> new IllegalStateException("Falta la categoría " + name));
        }

        long type(String code) {
            return options.productTypes().stream().filter(type -> type.code().equals(code)).map(ProductTypeView::id)
                    .findFirst().orElseThrow(() -> new IllegalStateException("Falta el tipo " + code));
        }

        long size(String name) {
            return byName(options.sizes(), name);
        }

        long color(String name) {
            return byName(options.colors(), name);
        }

        private static long byName(List<OptionView> options, String name) {
            return options.stream().filter(option -> option.name().equals(name)).map(OptionView::id)
                    .findFirst().orElseThrow(() -> new IllegalStateException("Falta la opción " + name));
        }
    }

    private record Product(long id, List<VariantView> variants) {

        long variant(String size, String color) {
            return variants.stream().filter(v -> v.size().equals(size) && v.color().equals(color))
                    .map(VariantView::id).findFirst()
                    .orElseThrow(() -> new IllegalStateException("Falta la variante " + size + "/" + color));
        }
    }

    private record Products(Product poloClasico, Product poloOversize, Product poloLima, Product poleraCapucha,
                            Product poleraCuello, Product gorraTrucker, Product gorraDad, Product tote) {
    }

    private record Customer(long id, long addressId, long designId) {
    }

    private record Customers(Customer renzo, Customer valeria, Customer lucia, Customer mateo, Customer camila) {
    }
}
