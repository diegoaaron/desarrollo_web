package com.coralshop.catalog.repository;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductTypeView;
import java.sql.PreparedStatement;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Categorías, marcas, tipos de producto, tallas y colores. */
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

    public List<ProductTypeView> findActiveProductTypes() {
        return jdbc.query("SELECT id, code, name FROM product_types WHERE is_active ORDER BY name",
                (rs, row) -> new ProductTypeView(rs.getLong("id"), rs.getString("code"), rs.getString("name")));
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

    public boolean isActiveProductType(Long id) {
        return count("SELECT count(*) FROM product_types WHERE id = ? AND is_active", id) > 0;
    }

    public boolean sizeExists(Long id) {
        return count("SELECT count(*) FROM sizes WHERE id = ?", id) > 0;
    }

    public boolean colorExists(Long id) {
        return count("SELECT count(*) FROM colors WHERE id = ?", id) > 0;
    }

    // ------------------------------------------------------------- categorías

    public boolean categoryExists(Long id) {
        return count("SELECT count(*) FROM categories WHERE id = ?", id) > 0;
    }

    /** Hay otra categoría raíz con el mismo nombre (sin distinguir mayúsculas). */
    public boolean rootCategoryNameTaken(String name, Long exceptId) {
        return count("""
                SELECT count(*) FROM categories
                WHERE parent_id IS NULL AND lower(name) = lower(?) AND id <> ?
                """, name, exceptId == null ? -1L : exceptId) > 0;
    }

    public long insertCategory(String name, String description) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement(
                    "INSERT INTO categories (name, description) VALUES (?, ?)", new String[] {"id"});
            statement.setString(1, name);
            statement.setString(2, description);
            return statement;
        }, keys);
        return keys.getKey().longValue();
    }

    public void updateCategory(Long id, String name, String description) {
        jdbc.update("UPDATE categories SET name = ?, description = ? WHERE id = ?", name, description, id);
    }

    /** Una categoría está en uso si tiene productos o subcategorías. */
    public boolean categoryInUse(Long id) {
        return count("""
                SELECT (SELECT count(*) FROM products WHERE category_id = ?)
                     + (SELECT count(*) FROM categories WHERE parent_id = ?)
                """, id, id) > 0;
    }

    public void deleteCategory(Long id) {
        jdbc.update("DELETE FROM categories WHERE id = ?", id);
    }

    private int count(String sql, Object... args) {
        Integer result = jdbc.queryForObject(sql, Integer.class, args);
        return result == null ? 0 : result;
    }
}
