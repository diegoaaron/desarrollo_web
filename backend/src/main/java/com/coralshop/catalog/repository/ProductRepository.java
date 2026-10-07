package com.coralshop.catalog.repository;

import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.dto.VariantView;
import com.coralshop.catalog.model.NewProduct;
import com.coralshop.catalog.model.ProductFilter;
import com.coralshop.catalog.model.ProductUpdate;
import com.coralshop.catalog.model.PurchasableProduct;
import com.coralshop.catalog.model.PurchasableVariant;
import java.sql.PreparedStatement;
import java.sql.Types;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Productos, sus imágenes y variantes. Único lugar con SQL de productos. */
@Repository
public class ProductRepository {

    private static final String PRODUCTS_FROM = """
            FROM products p
            JOIN categories c ON c.id = p.category_id
            LEFT JOIN brands b ON b.id = p.brand_id
            LEFT JOIN product_types pt ON pt.id = p.product_type_id
            WHERE 1 = 1
            """;

    private static final String PRODUCTS_SQL = """
            SELECT p.id, p.name, p.description, p.base_price, p.category_id,
                   c.name AS category_name, b.name AS brand_name,
                   p.product_type_id, pt.code AS product_type_code, p.is_customizable,
                   (SELECT image_url FROM product_images i WHERE i.product_id = p.id
                    ORDER BY i.is_primary DESC, i.sort_order, i.id LIMIT 1) AS image_url,
                   COALESCE((SELECT SUM(v.stock) FROM product_variants v
                             WHERE v.product_id = p.id AND v.is_active), 0) AS total_stock,
                   p.is_active
            """ + PRODUCTS_FROM;

    private static final String ACTIVE = " AND p.is_active AND c.is_active";

    private static final RowMapper<ProductView> PRODUCT_MAPPER = (rs, row) ->
            new ProductView(rs.getLong("id"), rs.getString("name"), rs.getString("description"),
                    rs.getBigDecimal("base_price"), rs.getLong("category_id"),
                    rs.getString("category_name"), rs.getString("brand_name"),
                    rs.getObject("product_type_id", Long.class), rs.getString("product_type_code"),
                    rs.getBoolean("is_customizable"), rs.getString("image_url"), rs.getInt("total_stock"),
                    rs.getBoolean("is_active"), List.of());

    private static final String VARIANTS_SQL = """
            SELECT v.id, v.sku, v.size_id, s.name AS size, v.color_id, co.name AS color, co.hex_code,
                   v.stock, v.is_active
            FROM product_variants v
            JOIN sizes s ON s.id = v.size_id
            JOIN colors co ON co.id = v.color_id
            WHERE v.product_id = ?
            """;

    private static final RowMapper<VariantView> VARIANT_MAPPER = (rs, row) ->
            new VariantView(rs.getLong("id"), rs.getString("sku"), rs.getLong("size_id"), rs.getString("size"),
                    rs.getLong("color_id"), rs.getString("color"), rs.getString("hex_code"), rs.getInt("stock"),
                    rs.getBoolean("is_active"));

    private final JdbcTemplate jdbc;

    public ProductRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    /** Página del catálogo público con los filtros aplicados. */
    public List<ProductView> findActive(ProductFilter filter, int limit, int offset) {
        List<Object> args = new ArrayList<>();
        String where = filterClause(filter, args);
        args.add(limit);
        args.add(offset);
        return jdbc.query(PRODUCTS_SQL + ACTIVE + where + " ORDER BY p.id DESC LIMIT ? OFFSET ?",
                PRODUCT_MAPPER, args.toArray());
    }

    public long countActive(ProductFilter filter) {
        List<Object> args = new ArrayList<>();
        String where = filterClause(filter, args);
        Long total = jdbc.queryForObject("SELECT count(*) " + PRODUCTS_FROM + ACTIVE + where, Long.class,
                args.toArray());
        return total == null ? 0 : total;
    }

    /** Cada filtro presente agrega su condición con un parámetro «?»; nunca se concatena el valor. */
    private static String filterClause(ProductFilter filter, List<Object> args) {
        StringBuilder where = new StringBuilder();
        if (filter.typeCode() != null) {
            where.append(" AND pt.code = ?");
            args.add(filter.typeCode());
        }
        if (filter.categoryId() != null) {
            where.append(" AND p.category_id = ?");
            args.add(filter.categoryId());
        }
        if (filter.text() != null) {
            where.append(" AND (p.name ILIKE ? OR p.description ILIKE ?)");
            String pattern = "%" + escapeLike(filter.text()) + "%";
            args.add(pattern);
            args.add(pattern);
        }
        return where.toString();
    }

    private static String escapeLike(String text) {
        return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_");
    }

    public List<ProductView> findAll() {
        return jdbc.query(PRODUCTS_SQL + " ORDER BY p.id DESC", PRODUCT_MAPPER);
    }

    public Optional<ProductView> findById(Long id) {
        return jdbc.query(PRODUCTS_SQL + " AND p.id = ?", PRODUCT_MAPPER, id).stream().findFirst();
    }

    public Optional<ProductView> findActiveById(Long id) {
        return jdbc.query(PRODUCTS_SQL + ACTIVE + " AND p.id = ?", PRODUCT_MAPPER, id).stream().findFirst();
    }

    public List<VariantView> findActiveVariants(Long productId) {
        return jdbc.query(VARIANTS_SQL + " AND v.is_active ORDER BY s.sort_order, co.name, v.id",
                VARIANT_MAPPER, productId);
    }

    public List<VariantView> findAllVariants(Long productId) {
        return jdbc.query(VARIANTS_SQL + " ORDER BY s.sort_order, co.name, v.id", VARIANT_MAPPER, productId);
    }

    public boolean exists(Long id) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM products WHERE id = ?", Integer.class, id);
        return count != null && count > 0;
    }

    /** Inserta el producto, su imagen principal y sus variantes; devuelve el id generado. */
    public long insert(NewProduct product) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO products (name, description, base_price, category_id, product_type_id,
                                          is_customizable, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setString(1, product.name());
            statement.setString(2, product.description());
            statement.setBigDecimal(3, product.basePrice());
            statement.setLong(4, product.categoryId());
            statement.setObject(5, product.productTypeId(), Types.BIGINT);
            statement.setBoolean(6, product.customizable());
            statement.setBoolean(7, product.active());
            return statement;
        }, keys);
        long productId = keys.getKey().longValue();

        jdbc.update("INSERT INTO product_images (product_id, image_url, alt_text, is_primary) VALUES (?, ?, ?, true)",
                productId, product.imageUrl(), product.name());
        for (NewProduct.Variant variant : product.variants()) {
            insertVariant(productId, variant.sizeId(), variant.colorId(), variant.sku(), variant.stock(), true);
        }
        return productId;
    }

    /** Actualiza los datos del producto, su imagen principal y sus variantes. */
    public void update(Long productId, ProductUpdate product) {
        jdbc.update("""
                UPDATE products
                SET name = ?, description = ?, base_price = ?, category_id = ?, product_type_id = ?,
                    is_customizable = ?, is_active = ?, updated_at = NOW()
                WHERE id = ?
                """, product.name(), product.description(), product.basePrice(), product.categoryId(),
                product.productTypeId(), product.customizable(), product.active(), productId);

        int updated = jdbc.update("UPDATE product_images SET image_url = ?, alt_text = ? WHERE product_id = ? AND is_primary",
                product.imageUrl(), product.name(), productId);
        if (updated == 0) {
            jdbc.update("INSERT INTO product_images (product_id, image_url, alt_text, is_primary) VALUES (?, ?, ?, true)",
                    productId, product.imageUrl(), product.name());
        }

        for (ProductUpdate.Variant variant : product.variants()) {
            if (variant.id() == null) {
                insertVariant(productId, variant.sizeId(), variant.colorId(), variant.sku(), variant.stock(),
                        variant.active());
            } else {
                jdbc.update("""
                        UPDATE product_variants
                        SET size_id = ?, color_id = ?, sku = ?, stock = ?, is_active = ?, updated_at = NOW()
                        WHERE id = ? AND product_id = ?
                        """, variant.sizeId(), variant.colorId(), variant.sku(), variant.stock(), variant.active(),
                        variant.id(), productId);
            }
        }
    }

    private void insertVariant(long productId, Long sizeId, Long colorId, String sku, int stock, boolean active) {
        jdbc.update("""
                INSERT INTO product_variants (product_id, size_id, color_id, sku, stock, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, productId, sizeId, colorId, sku, stock, active);
    }

    public List<Long> findVariantIds(Long productId) {
        return jdbc.queryForList("SELECT id FROM product_variants WHERE product_id = ?", Long.class, productId);
    }

    public int setActive(Long productId, boolean active) {
        return jdbc.update("UPDATE products SET is_active = ?, updated_at = NOW() WHERE id = ?", active, productId);
    }

    // ------------------------------------------------------------------ venta

    /** Un producto se puede comprar si él y su categoría están activos. */
    public Optional<PurchasableProduct> findPurchasable(Long id) {
        return jdbc.query("""
                SELECT p.id, p.name, p.base_price, (p.is_active AND c.is_active) AS active,
                       p.is_customizable, p.product_type_id, pt.code AS product_type_code
                FROM products p
                JOIN categories c ON c.id = p.category_id
                LEFT JOIN product_types pt ON pt.id = p.product_type_id
                WHERE p.id = ?
                """, (rs, row) -> new PurchasableProduct(rs.getLong("id"), rs.getString("name"),
                rs.getBigDecimal("base_price"), rs.getBoolean("active"), rs.getBoolean("is_customizable"),
                rs.getObject("product_type_id", Long.class), rs.getString("product_type_code")), id)
                .stream().findFirst();
    }

    public List<PurchasableVariant> findVariantsByIds(Collection<Long> ids) {
        if (ids.isEmpty()) {
            return List.of();
        }
        String placeholders = String.join(", ", Collections.nCopies(ids.size(), "?"));
        return jdbc.query("""
                SELECT v.id, v.product_id, v.sku, s.name AS size_name, co.name AS color_name, v.stock, v.is_active
                FROM product_variants v
                JOIN sizes s ON s.id = v.size_id
                JOIN colors co ON co.id = v.color_id
                WHERE v.id IN (%s)
                """.formatted(placeholders), (rs, row) -> new PurchasableVariant(rs.getLong("id"),
                rs.getLong("product_id"), rs.getString("sku"), rs.getString("size_name"),
                rs.getString("color_name"), rs.getInt("stock"), rs.getBoolean("is_active")), ids.toArray());
    }

    /**
     * Descuenta stock solo si alcanza (actualización condicional). Devuelve false si otra
     * compra se llevó las unidades antes, sin dejar nunca el stock en negativo.
     */
    public boolean decrementStock(Long variantId, int quantity) {
        return jdbc.update("""
                UPDATE product_variants SET stock = stock - ?, updated_at = NOW()
                WHERE id = ? AND is_active AND stock >= ?
                """, quantity, variantId, quantity) == 1;
    }

    public void incrementStock(Long variantId, int quantity) {
        jdbc.update("UPDATE product_variants SET stock = stock + ?, updated_at = NOW() WHERE id = ?",
                quantity, variantId);
    }
}
