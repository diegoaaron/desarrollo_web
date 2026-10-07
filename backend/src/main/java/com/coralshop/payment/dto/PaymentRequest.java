package com.coralshop.payment.dto;

import com.coralshop.payment.model.PaymentCharge;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/** Datos de la tarjeta de prueba. Se usan para el cobro y se descartan: no se guardan. */
public record PaymentRequest(
        @NotBlank @Pattern(regexp = "[0-9 ]{12,23}", message = "Ingresa un número de tarjeta válido")
        String cardNumber,
        @NotBlank @Size(max = 120) String cardHolder,
        @NotNull @Min(1) @Max(12) Integer expiryMonth,
        @NotNull @Min(2000) @Max(2100) Integer expiryYear,
        @NotBlank @Pattern(regexp = "[0-9]{3,4}", message = "El CVV tiene 3 o 4 dígitos") String cvv
) {

    public PaymentCharge.Card toCard() {
        return new PaymentCharge.Card(cardNumber.replace(" ", ""), cardHolder.trim(), expiryMonth, expiryYear, cvv);
    }

    /** Evita que los datos de la tarjeta lleguen a los registros si alguien imprime la solicitud. */
    @Override
    public String toString() {
        return "PaymentRequest[" + toCard() + "]";
    }
}
