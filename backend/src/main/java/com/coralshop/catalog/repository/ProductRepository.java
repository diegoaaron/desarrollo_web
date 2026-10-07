package com.coralshop.catalog.repository;

import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.dto.VariantView;
import com.coralshop.catalog.model.NewProduct;
import java.sql.PreparedStatement;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Productos, sus imágenes y variantes. Único lugar con SQL de productos. */
@Repository
public class ProductRepository {

    private static final String PRODUCTS_SQL = """
            SELECT p.id, p.name, p.description, p.base_price, p.category_id,
                   c.name AS category_name, b.name AS brand_name,
                   (SELECT image_url FROM product_images i WHERE i.product_id = p.id
                    ORDER BY i.is_primary DESC, i.sort_order, i.id LIMIT 1) AS image_url,
                   COALESCE((SELECT SUM(v.stock) FROM product_variants v
                             WHERE v.product_id = p.id AND v.is_active), 0) AS total_stock,
                   p.is_active
            FROM products p
            JOIN categories c ON c.id = p.category_id
            LEFT JOIN brands b ON b.id = p.brand_id
            WHERE 1 = 1
            """;

    private static final RowMapper<ProductView> PRODUCT_MAPPER = (rs, row) ->
            new ProductView(rs.getLong("id"), rs.getString("name"), rs.getString("description"),
                    rs.getBigDecimal("base_price"), rs.getLong("category_id"),
                    rs.getString("category_name"), rs.getString("brand_name"),
                    rs.getString("image_url"), rs.getInt("total_stock"), rs.getBoolean("is_active"), List.of());

    private static final RowMapper<VariantView> VARIANT_MAPPER = (rs, row) ->
            new VariantView(rs.getLong("id"), rs.getString("sku"), rs.getString("size"),
                    rs.getString("color"), rs.getInt("stock"));

    private final JdbcTemplate jdbc;

    public ProductRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<ProductView> findActive() {
        return jdbc.query(PRODUCTS_SQL + " AND p.is_active AND c.is_active ORDER BY p.id DESC", PRODUCT_MAPPER);
    }

    public List<ProductView> findAll() {
        return jdbc.query(PRODUCTS_SQL + " ORDER BY p.id DESC", PRODUCT_MAPPER);
    }

    public Optional<ProductView> findActiveById(Long id) {
        return jdbc.query(PRODUCTS_SQL + " AND p.is_active AND c.is_active AND p.id = ?", PRODUCT_MAPPER, id)
                .stream().findFirst();
    }

    public List<VariantView> findActiveVariants(Long productId) {
        return jdbc.query("""
                SELECT v.id, v.sku, s.name AS size, co.name AS color, v.stock
                FROM product_variants v
                JOIN sizes s ON s.id = v.size_id
                JOIN colors co ON co.id = v.color_id
                WHERE v.product_id = ? AND v.is_active
                ORDER BY s.sort_order, co.name, v.id
                """, VARIANT_MAPPER, productId);
    }

    /** Inserta el producto, su imagen principal y sus variantes; devuelve el id generado. */
    public long insert(NewProduct product) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO products (name, description, base_price, category_id, is_active)
                    VALUES (?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setString(1, product.name());
            statement.setString(2, product.description());
            statement.setBigDecimal(3, product.basePrice());
            statement.setLong(4, product.categoryId());
            statement.setBoolean(5, product.active());
            return statement;
        }, keys);
        long productId = keys.getKey().longValue();

        jdbc.update("INSERT INTO product_images (product_id, image_url, alt_text, is_primary) VALUES (?, ?, ?, true)",
                productId, product.imageUrl(), product.name());
        for (NewProduct.Variant variant : product.variants()) {
            jdbc.update("""
                    INSERT INTO product_variants (product_id, size_id, color_id, sku, stock)
                    VALUES (?, ?, ?, ?, ?)
                    """, productId, variant.sizeId(), variant.colorId(), variant.sku(), variant.stock());
        }
        return productId;
    }
}
