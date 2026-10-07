package com.coralshop.payment.service;

import com.coralshop.payment.model.PaymentCharge;
import com.coralshop.payment.model.PaymentResult;
import java.time.Clock;
import java.time.YearMonth;
import java.util.UUID;
import org.springframework.stereotype.Component;

/**
 * Pasarela simulada (D6). Reglas, pensadas para la demo:
 * <ul>
 *   <li>número que no pasa el algoritmo de Luhn → rechazado;</li>
 *   <li>tarjeta vencida → rechazado;</li>
 *   <li>número terminado en 0002 (p. ej. 4000 0000 0000 0002) → rechazado por fondos;</li>
 *   <li>cualquier otra (p. ej. 4111 1111 1111 1111) → aprobado.</li>
 * </ul>
 */
@Component
public class SimulatedPaymentGateway implements PaymentGateway {

    public static final String PROVIDER = "SIMULADO";

    private final Clock clock;

    public SimulatedPaymentGateway() {
        this(Clock.systemDefaultZone());
    }

    SimulatedPaymentGateway(Clock clock) {
        this.clock = clock;
    }

    @Override
    public String provider() {
        return PROVIDER;
    }

    @Override
    public PaymentResult charge(PaymentCharge charge) {
        String reference = "SIM-" + UUID.randomUUID();
        PaymentCharge.Card card = charge.card();
        if (!passesLuhn(card.number())) {
            return new PaymentResult(false, reference, "El número de tarjeta no es válido");
        }
        if (YearMonth.of(card.expiryYear(), card.expiryMonth()).isBefore(YearMonth.now(clock))) {
            return new PaymentResult(false, reference, "La tarjeta está vencida");
        }
        if (card.number().endsWith("0002")) {
            return new PaymentResult(false, reference, "Pago rechazado: fondos insuficientes");
        }
        return new PaymentResult(true, reference, "Pago aprobado");
    }

    static boolean passesLuhn(String number) {
        int sum = 0;
        boolean doubleIt = false;
        for (int i = number.length() - 1; i >= 0; i--) {
            int digit = number.charAt(i) - '0';
            if (digit < 0 || digit > 9) {
                return false;
            }
            if (doubleIt) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            sum += digit;
            doubleIt = !doubleIt;
        }
        return number.length() >= 12 && sum % 10 == 0;
    }
}
