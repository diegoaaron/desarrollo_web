package com.coralshop.audit.repository;

import java.sql.Timestamp;
import java.time.Instant;
import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

/** Bitácora de auditoría (tabla audit_log). Solo inserta: la bitácora no se edita. */
@Repository
public class AuditRepository {

    private final JdbcTemplate jdbc;

    public AuditRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    /** Ignora un event_id ya registrado, así que registrar dos veces el mismo evento no duplica filas. */
    public void insert(UUID eventId, String eventType, String entityType, long entityId, Long actorId,
                       String oldValue, String newValue, String detail, Instant occurredAt) {
        jdbc.update("""
                INSERT INTO audit_log (event_id, event_type, entity_type, entity_id, actor_id, old_value, new_value,
                                       detail, occurred_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (event_id) DO NOTHING
                """, eventId, eventType, entityType, entityId, actorId, oldValue, newValue, detail,
                Timestamp.from(occurredAt));
    }
}
