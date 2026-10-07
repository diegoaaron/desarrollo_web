package com.coralshop.payment.model;

import java.math.BigDecimal;

/** Cobro que se pide a la pasarela. Los datos de tarjeta nunca se guardan en la base. */
public record PaymentCharge(String orderCode, BigDecimal amount, String currency, Card card) {

    public record Card(String number, String holder, int expiryMonth, int expiryYear, String cvv) {

        @Override
        public String toString() {
            String last4 = number.length() >= 4 ? number.substring(number.length() - 4) : "****";
            return "Card[**** " + last4 + "]";
        }
    }
}
