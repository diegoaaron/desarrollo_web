package com.coralshop.payment.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.coralshop.payment.model.PaymentCharge;
import com.coralshop.payment.model.PaymentResult;
import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import org.junit.jupiter.api.Test;

class SimulatedPaymentGatewayTest {

    private final SimulatedPaymentGateway gateway = new SimulatedPaymentGateway(
            Clock.fixed(Instant.parse("2026-10-07T12:00:00Z"), ZoneId.of("America/Lima")));

    private PaymentResult pay(String number, int month, int year) {
        return gateway.charge(new PaymentCharge("CS-TEST", new BigDecimal("100.00"), "PEN",
                new PaymentCharge.Card(number, "Cliente Demo", month, year, "123")));
    }

    @Test
    void approvesValidTestCard() {
        PaymentResult result = pay("4111111111111111", 12, 2030);

        assertTrue(result.approved());
        assertTrue(result.providerReference().startsWith("SIM-"));
    }

    @Test
    void rejectsInsufficientFundsCard() {
        PaymentResult result = pay("4000000000000002", 12, 2030);

        assertFalse(result.approved());
        assertEquals("Pago rechazado: fondos insuficientes", result.message());
    }

    @Test
    void rejectsInvalidNumbersAndExpiredCards() {
        assertFalse(pay("4111111111111112", 12, 2030).approved());
        assertFalse(pay("4111111111111111", 9, 2026).approved());
        assertTrue(pay("4111111111111111", 10, 2026).approved());
    }

    @Test
    void luhnAlgorithm() {
        assertTrue(SimulatedPaymentGateway.passesLuhn("4111111111111111"));
        assertTrue(SimulatedPaymentGateway.passesLuhn("5555555555554444"));
        assertFalse(SimulatedPaymentGateway.passesLuhn("1234567812345678"));
        assertFalse(SimulatedPaymentGateway.passesLuhn("41111111111x1111"));
    }
}
