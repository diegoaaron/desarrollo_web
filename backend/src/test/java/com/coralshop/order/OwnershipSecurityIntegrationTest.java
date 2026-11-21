package com.coralshop.order;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.coralshop.design.service.DesignService;
import com.coralshop.order.dto.CreateOrderRequest;
import com.coralshop.order.service.OrderService;
import com.coralshop.pricing.dto.CartLineRequest;
import com.coralshop.support.IntegrationTest;
import com.coralshop.support.TestData;
import com.coralshop.support.TestData.Product;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Un cliente no puede ver ni usar lo que pertenece a otro: el pedido y el diseño ajenos
 * responden 404 (como si no existieran, para no revelar que existen) y las rutas de
 * administración, 403. Criterio de la fase 5.1.
 */
class OwnershipSecurityIntegrationTest extends IntegrationTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private TestData data;

    @Autowired
    private DesignService designService;

    @Autowired
    private OrderService orderService;

    private String owner;
    private String stranger;
    private long designId;
    private String orderCode;
    private Product polo;

    /** El dueño sube su logo y hace un pedido bordado con él. */
    @BeforeEach
    void ownerWithDesignAndOrder() throws IOException {
        owner = data.customer();
        stranger = data.customer();
        polo = data.polo("S=10");
        long ownerId = data.idOf(owner);
        designId = designService.upload(ownerId, "logo.png", png()).id();
        orderCode = orderService.create(ownerId, new CreateOrderRequest(
                List.of(new CartLineRequest(polo.id(), "BORDADO", List.of("PECHO_IZQ"), designId,
                        List.of(new CartLineRequest.Item(polo.variant("S"), 1)))),
                null, "RECOJO_TIENDA", "999 888 777", null)).orderCode();
    }

    @Test
    void theOwnerSeesTheirOrderAndDesign() throws Exception {
        mvc.perform(get("/api/orders/me/" + orderCode).with(user(owner).roles("USER")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.orderCode").value(orderCode));
        mvc.perform(get("/api/designs/" + designId + "/image").with(user(owner).roles("USER")))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.IMAGE_PNG));
    }

    @Test
    void anotherCustomerCannotSeeTheOrder() throws Exception {
        mvc.perform(get("/api/orders/me/" + orderCode).with(user(stranger).roles("USER")))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("Pedido no encontrado"));
    }

    @Test
    void anotherCustomerCannotSeeTheDesign() throws Exception {
        mvc.perform(get("/api/designs/" + designId + "/image").with(user(stranger).roles("USER")))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("Diseño no encontrado"));
    }

    @Test
    void anotherCustomerCannotOrderWithTheDesign() throws Exception {
        mvc.perform(post("/api/orders").with(user(stranger).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"lines": [{"productId": %d, "techniqueCode": "BORDADO", "zoneCodes": ["PECHO_IZQ"],
                                            "designId": %d, "items": [{"variantId": %d, "quantity": 1}]}],
                                 "shippingMethodCode": "RECOJO_TIENDA", "contactPhone": "999 111 222"}
                                """.formatted(polo.id(), designId, polo.variant("S"))))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("no existe en tu cuenta")));
    }

    @Test
    void anotherCustomerCannotPayTheOrder() throws Exception {
        mvc.perform(post("/api/orders/" + orderCode + "/payment").with(user(stranger).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"cardNumber": "4111 1111 1111 1111", "cardHolder": "Otro Cliente",
                                 "expiryMonth": 12, "expiryYear": 2099, "cvv": "123"}
                                """))
                .andExpect(status().isNotFound());
    }

    @Test
    void aCustomerCannotUseTheAdminRoutes() throws Exception {
        mvc.perform(get("/api/orders").with(user(stranger).roles("USER")))
                .andExpect(status().isForbidden());
        mvc.perform(put("/api/orders/1/status").with(user(stranger).roles("USER")).with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\": \"ENTREGADO\"}"))
                .andExpect(status().isForbidden());
    }

    @Test
    void anAdministratorSeesTheDesignToProduceIt() throws Exception {
        mvc.perform(get("/api/designs/" + designId + "/image").with(user(data.admin()).roles("ADMIN")))
                .andExpect(status().isOk());
    }

    @Test
    void withoutASessionTheCustomerRoutesAnswer401() throws Exception {
        mvc.perform(get("/api/orders/me"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.message").value("Debes iniciar sesión"));
        mvc.perform(get("/api/designs/" + designId + "/image"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void aWriteWithoutTheCsrfTokenIsRejected() throws Exception {
        mvc.perform(post("/api/orders").with(user(owner).roles("USER"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isForbidden());
    }

    private static byte[] png() throws IOException {
        BufferedImage image = new BufferedImage(8, 8, BufferedImage.TYPE_INT_RGB);
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ImageIO.write(image, "png", out);
        return out.toByteArray();
    }
}
