package com.coralshop.customization.repository;

import com.coralshop.customization.model.QuantityTier;
import com.coralshop.customization.model.Technique;
import com.coralshop.customization.model.ZoneRule;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

/** Técnicas, zonas por tipo de producto y escalas de mayoreo. */
@Repository
public class CustomizationRepository {

    private static final RowMapper<Technique> TECHNIQUE_MAPPER = (rs, row) -> new Technique(rs.getLong("id"),
            rs.getString("code"), rs.getString("name"), rs.getString("description"), rs.getBigDecimal("base_cost"));

    private final JdbcTemplate jdbc;

    public CustomizationRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Technique> findActiveTechniques() {
        return jdbc.query("""
                SELECT id, code, name, description, base_cost FROM customization_techniques
                WHERE is_active ORDER BY base_cost, id
                """, TECHNIQUE_MAPPER);
    }

    public Optional<Technique> findActiveTechnique(String code) {
        return jdbc.query("""
                SELECT id, code, name, description, base_cost FROM customization_techniques
                WHERE code = ? AND is_active
                """, TECHNIQUE_MAPPER, code).stream().findFirst();
    }

    /** Zonas que admite el tipo de producto, para todas las técnicas activas. */
    public List<ZoneRule> findZoneRules(Long productTypeId) {
        return jdbc.query("""
                SELECT t.id AS technique_id, t.code AS technique_code, z.id AS zone_id, z.code AS zone_code,
                       z.name AS zone_name, r.max_width_cm, r.max_height_cm, r.surcharge,
                       r.preview_x, r.preview_y, r.preview_w, r.preview_h
                FROM product_type_zones r
                JOIN print_zones z ON z.id = r.zone_id
                JOIN customization_techniques t ON t.id = r.technique_id
                WHERE r.product_type_id = ? AND t.is_active
                ORDER BY t.id, z.id
                """, (rs, row) -> new ZoneRule(rs.getLong("technique_id"), rs.getString("technique_code"),
                rs.getLong("zone_id"), rs.getString("zone_code"), rs.getString("zone_name"),
                rs.getBigDecimal("max_width_cm"), rs.getBigDecimal("max_height_cm"), rs.getBigDecimal("surcharge"),
                rs.getBigDecimal("preview_x"), rs.getBigDecimal("preview_y"), rs.getBigDecimal("preview_w"),
                rs.getBigDecimal("preview_h")), productTypeId);
    }

    public List<QuantityTier> findTiers() {
        return jdbc.query("SELECT min_quantity, label, discount_percent FROM quantity_tiers ORDER BY min_quantity",
                (rs, row) -> new QuantityTier(rs.getInt("min_quantity"), rs.getString("label"),
                        rs.getBigDecimal("discount_percent")));
    }
}
