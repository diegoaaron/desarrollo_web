package com.coralshop.payment.model;

/** Respuesta de la pasarela: aprobado o rechazado, con la referencia de la operación. */
public record PaymentResult(boolean approved, String providerReference, String message) {
}
