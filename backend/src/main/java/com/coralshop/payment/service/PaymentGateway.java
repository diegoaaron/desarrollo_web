package com.coralshop.payment.service;

import com.coralshop.payment.model.PaymentCharge;
import com.coralshop.payment.model.PaymentResult;

/**
 * Pasarela de pago. Hoy la implementa {@link SimulatedPaymentGateway}; la fase 6 agrega la
 * pasarela real como otra implementación, sin cambiar a quien la usa.
 */
public interface PaymentGateway {

    /** Código que se guarda en payments.provider (SIMULADO, …). */
    String provider();

    PaymentResult charge(PaymentCharge charge);
}
