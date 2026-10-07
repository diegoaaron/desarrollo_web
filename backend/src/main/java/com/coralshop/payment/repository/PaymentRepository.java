package com.coralshop.payment.repository;

import java.math.BigDecimal;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class PaymentRepository {

    private final JdbcTemplate jdbc;

    public PaymentRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    /** Registra el intento; si fue aprobado, con su fecha de confirmación. */
    public void insert(long orderId, String provider, String reference, BigDecimal amount, String currency,
                       boolean approved) {
        jdbc.update("""
                INSERT INTO payments (order_id, provider, provider_reference, amount, currency, status, confirmed_at)
                VALUES (?, ?, ?, ?, ?, ?, CASE WHEN ? THEN NOW() END)
                """, orderId, provider, reference, amount, currency, approved ? "APROBADO" : "RECHAZADO", approved);
    }
}
