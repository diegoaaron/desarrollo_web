package com.coralshop.demo;

import static org.assertj.core.api.Assertions.assertThat;

import com.coralshop.demo.service.DemoDataService;
import com.coralshop.support.IntegrationTest;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;

/** Con el perfil demo, la aplicación arranca con un pedido en cada estado y datos coherentes. */
@ActiveProfiles("demo")
@TestPropertySource(properties = "app.demo.admin-password=Admin-demo-2026")
class DemoDataIntegrationTest extends IntegrationTest {

    private static final String DEMO_ORDERS = """
            FROM orders o JOIN users u ON u.id = o.user_id WHERE u.email LIKE '%@demo.coralshop.pe'""";

    @Autowired
    private JdbcTemplate jdbc;

    @Autowired
    private DemoDataService demoDataService;

    @Test
    void loadsAnOrderInEveryStatus() {
        List<String> statuses = jdbc.queryForList("SELECT DISTINCT o.status " + DEMO_ORDERS, String.class);

        assertThat(statuses).containsExactlyInAnyOrder("PENDIENTE_PAGO", "PAGADO", "EN_PRODUCCION",
                "LISTO_PARA_ENVIO", "ENVIADO", "ENTREGADO", "CANCELADO");
        assertThat(jdbc.queryForObject("SELECT COUNT(*) " + DEMO_ORDERS, Long.class)).isEqualTo(8);
        assertThat(jdbc.queryForObject("SELECT COUNT(DISTINCT product_id) FROM product_variants "
                + "WHERE sku LIKE 'DEMO-%'", Long.class)).isEqualTo(8);
    }

    /** Historia de referencia: 12 polos bordados, entregados, con su historial completo. */
    @Test
    void theReferenceOrderWentAllTheWayToDelivered() {
        Map<String, Object> order = jdbc.queryForMap("SELECT o.id, o.status, o.total_amount " + DEMO_ORDERS
                + " AND u.email = 'renzo.paredes@demo.coralshop.pe'");

        assertThat(order.get("status")).isEqualTo("ENTREGADO");
        assertThat(jdbc.queryForObject("SELECT SUM(quantity) FROM order_items i JOIN order_lines l "
                + "ON l.id = i.order_line_id WHERE l.order_id = ?", Long.class, order.get("id"))).isEqualTo(12);
        assertThat(jdbc.queryForList("SELECT to_status FROM order_status_history WHERE order_id = ? ORDER BY id",
                String.class, order.get("id")))
                .containsExactly("PENDIENTE_PAGO", "PAGADO", "EN_PRODUCCION", "LISTO_PARA_ENVIO", "ENVIADO",
                        "ENTREGADO");
        assertThat(jdbc.queryForObject("SELECT COUNT(*) FROM notifications n JOIN users u ON u.id = n.user_id "
                + "WHERE u.email = 'renzo.paredes@demo.coralshop.pe'", Long.class)).isEqualTo(6);
    }

    @Test
    void stockReflectsTheOrdersAndTheCancellationReturnedIt() {
        // 30 iniciales − 4 de la historia de referencia.
        assertThat(stock("DEMO-POLO-CLA-NEG-S")).isEqualTo(26);
        // La gorra azul del pedido cancelado volvió al inventario.
        assertThat(stock("DEMO-GORRA-DAD-AZU-U")).isEqualTo(40);
        assertThat(stock("DEMO-GORRA-DAD-BEI-U")).isEqualTo(37);
    }

    @Test
    void theRejectedPaymentIsRecordedAndTheOrderStaysPending() {
        Map<String, Object> payment = jdbc.queryForMap("SELECT p.status, o.status AS order_status FROM payments p "
                + "JOIN orders o ON o.id = p.order_id JOIN users u ON u.id = o.user_id "
                + "WHERE u.email = 'camila.torres@demo.coralshop.pe'");

        assertThat(payment).containsEntry("status", "RECHAZADO").containsEntry("order_status", "PENDIENTE_PAGO");
    }

    @Test
    void loadingAgainChangesNothing() {
        long orders = jdbc.queryForObject("SELECT COUNT(*) " + DEMO_ORDERS, Long.class);

        demoDataService.load("admin@demo.coralshop.pe", "Admin-demo-2026", "Cliente2026");

        assertThat(jdbc.queryForObject("SELECT COUNT(*) " + DEMO_ORDERS, Long.class)).isEqualTo(orders);
    }

    private int stock(String sku) {
        return jdbc.queryForObject("SELECT stock FROM product_variants WHERE sku = ?", Integer.class, sku);
    }
}
