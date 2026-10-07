package com.coralshop.order.model;

import java.util.Arrays;
import java.util.Locale;
import java.util.Optional;

/** Estados del pedido (fases.md §1.5). Los nombres coinciden con el CHECK de orders.status. */
public enum OrderStatus {
    PENDIENTE_PAGO("Pendiente de pago"),
    PAGADO("Pagado"),
    EN_PRODUCCION("En producción"),
    LISTO_PARA_ENVIO("Listo para envío"),
    ENVIADO("Enviado"),
    ENTREGADO("Entregado"),
    CANCELADO("Cancelado");

    private final String label;

    OrderStatus(String label) {
        this.label = label;
    }

    public String label() {
        return label;
    }

    public static Optional<OrderStatus> parse(String value) {
        if (value == null) {
            return Optional.empty();
        }
        String normalized = value.trim().toUpperCase(Locale.ROOT);
        return Arrays.stream(values()).filter(status -> status.name().equals(normalized)).findFirst();
    }
}
