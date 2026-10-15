package com.coralshop.order;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.coralshop.support.IntegrationTest;
import com.coralshop.support.TestData;
import com.coralshop.support.TestData.Product;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

/**
 * POST /api/orders contra la base real: el pedido, sus líneas y el descuento de stock se
 * graban juntos o no se graba nada (fases.md §2.1, criterio de la fase 5.1).
 */
class OrderCreationIntegrationTest extends IntegrationTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private TestData data;

    @Autowired
    private JdbcTemplate jdbc;

    @Test
    void createsTheOrderAndReservesTheStock() throws Exception {
        String customer = data.customer();
        Product polo = data.polo("S=10", "M=10");

        mvc.perform(post("/api/orders").with(user(customer).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(order(line(polo.id(), item(polo.variant("S"), 4), item(polo.variant("M"), 2)))))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.orderCode").value(org.hamcrest.Matchers.startsWith("CS-")))
                .andExpect(jsonPath("$.status").value("PENDIENTE_PAGO"))
                // 6 polos a S/ 35 = 210; escala de 6 (10 %) = 21 de descuento; recojo sin costo.
                .andExpect(jsonPath("$.total").value(189.00));

        assertThat(data.stockOf(polo, "S")).isEqualTo(6);
        assertThat(data.stockOf(polo, "M")).isEqualTo(8);
        assertThat(ordersOf(customer)).isEqualTo(1);
    }

    /**
     * La primera línea sí tiene stock y se descuenta antes de llegar a la segunda, que no lo
     * tiene: el 409 debe deshacer también el descuento de la primera.
     */
    @Test
    void insufficientStockAnswers409AndRollsBackEverything() throws Exception {
        String customer = data.customer();
        Product polo = data.polo("S=10", "M=2");

        mvc.perform(post("/api/orders").with(user(customer).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(order(
                                line(polo.id(), item(polo.variant("S"), 3)),
                                line(polo.id(), item(polo.variant("M"), 5)))))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.status").value(409))
                .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("Stock insuficiente")));

        assertThat(data.stockOf(polo, "S")).isEqualTo(10);
        assertThat(data.stockOf(polo, "M")).isEqualTo(2);
        assertThat(ordersOf(customer)).isZero();
        long userId = data.idOf(customer);
        assertThat(jdbc.queryForObject("SELECT COUNT(*) FROM notifications WHERE user_id = ?", Long.class, userId))
                .isZero();
        mvc.perform(get("/api/orders/me").with(user(customer).roles("USER")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    void theSameVariantInTwoLinesCountsTowardsOneStock() throws Exception {
        String customer = data.customer();
        Product polo = data.polo("S=5");

        mvc.perform(post("/api/orders").with(user(customer).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(order(
                                line(polo.id(), item(polo.variant("S"), 3)),
                                line(polo.id(), item(polo.variant("S"), 3)))))
                .andExpect(status().isConflict());

        assertThat(data.stockOf(polo, "S")).isEqualTo(5);
    }

    @Test
    void anInvalidBodyAnswers400WithTheFieldErrors() throws Exception {
        String customer = data.customer();

        mvc.perform(post("/api/orders").with(user(customer).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"lines\": [], \"shippingMethodCode\": \"\"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors.lines").exists())
                .andExpect(jsonPath("$.errors.shippingMethodCode").exists());
    }

    private long ordersOf(String email) {
        return jdbc.queryForObject("SELECT COUNT(*) FROM orders WHERE user_id = ?", Long.class, data.idOf(email));
    }

    private static String order(String... lines) {
        return """
                {"lines": [%s], "shippingMethodCode": "RECOJO_TIENDA", "contactPhone": "999 888 777"}
                """.formatted(String.join(",", lines));
    }

    private static String line(long productId, String... items) {
        return """
                {"productId": %d, "items": [%s]}""".formatted(productId, String.join(",", items));
    }

    private static String item(long variantId, int quantity) {
        return """
                {"variantId": %d, "quantity": %d}""".formatted(variantId, quantity);
    }
}
