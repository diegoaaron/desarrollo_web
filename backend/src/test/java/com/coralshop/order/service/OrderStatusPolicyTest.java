package com.coralshop.order.service;

import static com.coralshop.order.model.OrderStatus.CANCELADO;
import static com.coralshop.order.model.OrderStatus.EN_PRODUCCION;
import static com.coralshop.order.model.OrderStatus.ENTREGADO;
import static com.coralshop.order.model.OrderStatus.ENVIADO;
import static com.coralshop.order.model.OrderStatus.LISTO_PARA_ENVIO;
import static com.coralshop.order.model.OrderStatus.PAGADO;
import static com.coralshop.order.model.OrderStatus.PENDIENTE_PAGO;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.order.model.OrderStatus;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class OrderStatusPolicyTest {

    private final OrderStatusPolicy policy = new OrderStatusPolicy();

    @ParameterizedTest
    @CsvSource({
            "PENDIENTE_PAGO,PAGADO", "PENDIENTE_PAGO,CANCELADO", "PAGADO,EN_PRODUCCION", "PAGADO,CANCELADO",
            "EN_PRODUCCION,LISTO_PARA_ENVIO", "LISTO_PARA_ENVIO,ENVIADO", "ENVIADO,ENTREGADO"})
    void allowsTheDiagramTransitions(OrderStatus from, OrderStatus to) {
        assertDoesNotThrow(() -> policy.requireTransition(from, to));
    }

    @ParameterizedTest
    @CsvSource({
            "PENDIENTE_PAGO,ENVIADO", "PAGADO,ENTREGADO", "EN_PRODUCCION,CANCELADO", "ENVIADO,PAGADO",
            "ENTREGADO,CANCELADO", "CANCELADO,PAGADO", "PAGADO,PAGADO"})
    void rejectsEverythingElse(OrderStatus from, OrderStatus to) {
        assertThrows(BusinessRuleException.class, () -> policy.requireTransition(from, to));
    }

    @Test
    void adminCannotMarkAnOrderAsPaid() {
        assertThrows(BusinessRuleException.class, () -> policy.requireAdminTransition(PENDIENTE_PAGO, PAGADO));
        assertEquals(List.of(CANCELADO), policy.adminNextStatuses(PENDIENTE_PAGO));
        assertEquals(List.of(EN_PRODUCCION, CANCELADO), policy.adminNextStatuses(PAGADO));
        assertEquals(List.of(), policy.adminNextStatuses(ENTREGADO));
    }

    @Test
    void onlyCancellingRestocks() {
        assertTrue(policy.restocks(CANCELADO));
        for (OrderStatus status : List.of(PENDIENTE_PAGO, PAGADO, EN_PRODUCCION, LISTO_PARA_ENVIO, ENVIADO,
                ENTREGADO)) {
            assertFalse(policy.restocks(status));
        }
    }
}
