package com.coralshop.catalog.repository;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

/** Categorías, marcas, tallas y colores. */
@Repository
public class CatalogOptionRepository {

    private static final RowMapper<OptionView> OPTION_MAPPER =
            (rs, row) -> new OptionView(rs.getLong("id"), rs.getString("name"));

    private final JdbcTemplate jdbc;

    public CatalogOptionRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<CategoryView> findActiveCategories() {
        return jdbc.query("SELECT id, name, description FROM categories WHERE is_active ORDER BY name",
                (rs, row) -> new CategoryView(rs.getLong("id"), rs.getString("name"),
                        rs.getString("description") == null ? "" : rs.getString("description")));
    }

    public List<OptionView> findActiveBrands() {
        return jdbc.query("SELECT id, name FROM brands WHERE is_active ORDER BY name", OPTION_MAPPER);
    }

    public List<OptionView> findSizes() {
        return jdbc.query("SELECT id, name FROM sizes ORDER BY sort_order, id", OPTION_MAPPER);
    }

    public List<OptionView> findColors() {
        return jdbc.query("SELECT id, name FROM colors ORDER BY name", OPTION_MAPPER);
    }

    public boolean isActiveCategory(Long id) {
        return count("SELECT count(*) FROM categories WHERE id = ? AND is_active", id) > 0;
    }

    public boolean sizeExists(Long id) {
        return count("SELECT count(*) FROM sizes WHERE id = ?", id) > 0;
    }

    public boolean colorExists(Long id) {
        return count("SELECT count(*) FROM colors WHERE id = ?", id) > 0;
    }

    private int count(String sql, Object... args) {
        Integer result = jdbc.queryForObject(sql, Integer.class, args);
        return result == null ? 0 : result;
    }
}
