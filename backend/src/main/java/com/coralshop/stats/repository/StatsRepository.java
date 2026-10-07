package com.coralshop.stats.repository;

import com.coralshop.stats.dto.OverviewResponse.RecentOrder;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

/** Consultas de métricas para el tablero de administración. */
@Repository
public class StatsRepository {

    private final JdbcTemplate jdbc;

    public StatsRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public long countUsers() {
        return count("SELECT count(*) FROM users");
    }

    public long countProducts() {
        return count("SELECT count(*) FROM products");
    }

    public long countOrders() {
        return count("SELECT count(*) FROM orders");
    }

    public BigDecimal deliveredRevenue() {
        return jdbc.queryForObject(
                "SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status = 'DELIVERED'", BigDecimal.class);
    }

    public List<RecentOrder> recentOrders(int limit) {
        return jdbc.query("""
                SELECT o.id, btrim(u.first_name || ' ' || u.last_name) AS customer_name,
                       o.total_amount, o.status, o.created_at
                FROM orders o JOIN users u ON u.id = o.user_id
                ORDER BY o.created_at DESC LIMIT ?
                """, (rs, row) -> new RecentOrder(rs.getLong("id"), rs.getString("customer_name"),
                rs.getBigDecimal("total_amount"), rs.getString("status"),
                rs.getObject("created_at", OffsetDateTime.class)), limit);
    }

    private long count(String sql) {
        Long result = jdbc.queryForObject(sql, Long.class);
        return result == null ? 0 : result;
    }
}
