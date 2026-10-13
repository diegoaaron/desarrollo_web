package com.coralshop.notification.repository;

import com.coralshop.notification.dto.NotificationView;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

/** Notificaciones del cliente. Toda lectura y marcado va filtrado por el dueño. */
@Repository
public class NotificationRepository {

    private static final RowMapper<NotificationView> MAPPER = (rs, row) -> new NotificationView(rs.getLong("id"),
            rs.getString("title"), rs.getString("message"), rs.getString("link"), rs.getBoolean("is_read"),
            rs.getObject("created_at", OffsetDateTime.class));

    private final JdbcTemplate jdbc;

    public NotificationRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    /** Un event_id ya registrado se ignora: el mismo evento nunca genera dos avisos. */
    public void insert(UUID eventId, long userId, Long orderId, String title, String message, String link) {
        jdbc.update("""
                INSERT INTO notifications (event_id, user_id, order_id, title, message, link)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (event_id) DO NOTHING
                """, eventId, userId, orderId, title, message, link);
    }

    public List<NotificationView> findLatestByUser(long userId, int limit) {
        return jdbc.query("""
                SELECT id, title, message, link, is_read, created_at
                FROM notifications WHERE user_id = ?
                ORDER BY created_at DESC, id DESC LIMIT ?
                """, MAPPER, userId, limit);
    }

    public long countUnread(long userId) {
        Long count = jdbc.queryForObject("SELECT count(*) FROM notifications WHERE user_id = ? AND NOT is_read",
                Long.class, userId);
        return count == null ? 0 : count;
    }

    /** Devuelve false si la notificación no existe o es de otro usuario. */
    public boolean markRead(long id, long userId) {
        return jdbc.update("""
                UPDATE notifications SET is_read = TRUE, read_at = COALESCE(read_at, NOW())
                WHERE id = ? AND user_id = ?
                """, id, userId) == 1;
    }

    public void markAllRead(long userId) {
        jdbc.update("UPDATE notifications SET is_read = TRUE, read_at = NOW() WHERE user_id = ? AND NOT is_read",
                userId);
    }
}
