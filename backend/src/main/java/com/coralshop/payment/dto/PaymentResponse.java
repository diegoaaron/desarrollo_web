package com.coralshop.payment.dto;

import java.math.BigDecimal;

/** Resultado del pago: si fue rechazado, el pedido sigue en PENDIENTE_PAGO y se puede reintentar. */
public record PaymentResponse(String orderCode, String paymentStatus, String orderStatus, String reference,
                              BigDecimal amount, String message) {
}
