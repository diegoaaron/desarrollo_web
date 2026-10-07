package com.coralshop.order.model;

import java.math.BigDecimal;

/** Cabecera de un pedido nuevo, con importes ya calculados y la dirección copiada. */
public record NewOrder(String orderCode, Long userId, BigDecimal subtotal, BigDecimal discountAmount,
                       BigDecimal shippingCost, BigDecimal totalAmount, Long shippingMethodId,
                       Recipient recipient, String customerNote) {

    /** Quién recibe o recoge. La dirección es null en el recojo en tienda. */
    public record Recipient(String receiverName, String phone, String department, String province,
                            String district, String street, String reference) {
    }
}
