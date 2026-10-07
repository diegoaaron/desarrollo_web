package com.coralshop.shipping.repository;

import com.coralshop.shipping.dto.ShippingMethodView;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

@Repository
public class ShippingMethodRepository {

    private static final String ACTIVE_SQL = """
            SELECT id, code, name, cost, estimated_days, requires_address FROM shipping_methods WHERE is_active
            """;

    private static final RowMapper<ShippingMethodView> MAPPER = (rs, row) -> new ShippingMethodView(rs.getLong("id"),
            rs.getString("code"), rs.getString("name"), rs.getBigDecimal("cost"), rs.getInt("estimated_days"),
            rs.getBoolean("requires_address"));

    private final JdbcTemplate jdbc;

    public ShippingMethodRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<ShippingMethodView> findActive() {
        return jdbc.query(ACTIVE_SQL + " ORDER BY cost, id", MAPPER);
    }

    public Optional<ShippingMethodView> findActiveByCode(String code) {
        return jdbc.query(ACTIVE_SQL + " AND code = ?", MAPPER, code).stream().findFirst();
    }
}
