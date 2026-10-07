package com.coralshop.order.repository;

import com.coralshop.design.dto.DesignView;
import com.coralshop.order.dto.AdminOrderSummaryView;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.dto.OrderSummaryView;
import com.coralshop.order.model.NewOrder;
import com.coralshop.order.model.OrderHeader;
import com.coralshop.order.model.OrderStatus;
import com.coralshop.order.model.StockMovement;
import com.coralshop.pricing.model.LineAmounts;
import com.coralshop.pricing.model.PricedLine;
import java.sql.PreparedStatement;
import java.sql.Types;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Pedidos, sus líneas, zonas, ítems e historial de estados. Único lugar con SQL de pedidos. */
@Repository
public class OrderRepository {

    private static final RowMapper<OrderHeader> HEADER_MAPPER = (rs, row) -> new OrderHeader(rs.getLong("id"),
            rs.getString("order_code"), rs.getLong("user_id"), OrderStatus.valueOf(rs.getString("status")),
            rs.getBigDecimal("total_amount"));

    private static final String UNITS = """
            (SELECT COALESCE(SUM(l.quantity_total), 0) FROM order_lines l WHERE l.order_id = o.id) AS units
            """;

    private final JdbcTemplate jdbc;

    public OrderRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    // ------------------------------------------------------------- escritura

    public long insertOrder(NewOrder order) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        NewOrder.Recipient recipient = order.recipient();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO orders (order_code, user_id, status, subtotal, discount_amount, shipping_cost,
                                        total_amount, shipping_method_id, receiver_name, phone, department,
                                        province, district, street, reference, customer_note)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setString(1, order.orderCode());
            statement.setLong(2, order.userId());
            statement.setString(3, OrderStatus.PENDIENTE_PAGO.name());
            statement.setBigDecimal(4, order.subtotal());
            statement.setBigDecimal(5, order.discountAmount());
            statement.setBigDecimal(6, order.shippingCost());
            statement.setBigDecimal(7, order.totalAmount());
            statement.setLong(8, order.shippingMethodId());
            statement.setString(9, recipient.receiverName());
            statement.setString(10, recipient.phone());
            statement.setString(11, recipient.department());
            statement.setString(12, recipient.province());
            statement.setString(13, recipient.district());
            statement.setString(14, recipient.street());
            statement.setString(15, recipient.reference());
            statement.setString(16, order.customerNote());
            return statement;
        }, keys);
        return keys.getKey().longValue();
    }

    /** Inserta la línea con sus zonas y su reparto por variante, con los precios congelados. */
    public void insertLine(long orderId, PricedLine line) {
        LineAmounts amounts = line.amounts();
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO order_lines (order_id, product_id, product_name, technique_id, design_upload_id,
                                             quantity_total, tier_min_quantity, unit_base_price,
                                             unit_customization_price, discount_percent, line_total)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setLong(1, orderId);
            statement.setLong(2, line.product().id());
            statement.setString(3, line.product().name());
            statement.setObject(4, line.technique() == null ? null : line.technique().id(), Types.BIGINT);
            statement.setObject(5, line.designId(), Types.BIGINT);
            statement.setInt(6, amounts.quantityTotal());
            statement.setInt(7, line.tier().minQuantity());
            statement.setBigDecimal(8, amounts.unitBasePrice());
            statement.setBigDecimal(9, amounts.unitCustomizationPrice());
            statement.setBigDecimal(10, amounts.discountPercent());
            statement.setBigDecimal(11, amounts.lineTotal());
            return statement;
        }, keys);
        long lineId = keys.getKey().longValue();

        for (PricedLine.PricedZone zone : line.zones()) {
            jdbc.update("INSERT INTO order_line_zones (order_line_id, zone_id, surcharge) VALUES (?, ?, ?)",
                    lineId, zone.zoneId(), zone.surcharge());
        }
        for (PricedLine.PricedItem item : line.items()) {
            jdbc.update("""
                    INSERT INTO order_items (order_line_id, variant_id, sku, size_name, color_name, quantity)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, lineId, item.variant().id(), item.variant().sku(), item.variant().sizeName(),
                    item.variant().colorName(), item.quantity());
        }
    }

    public void insertHistory(long orderId, OrderStatus from, OrderStatus to, Long changedBy, String comment) {
        jdbc.update("""
                INSERT INTO order_status_history (order_id, from_status, to_status, changed_by, comment)
                VALUES (?, ?, ?, ?, ?)
                """, orderId, from == null ? null : from.name(), to.name(), changedBy, comment);
    }

    /**
     * Cambia el estado solo si sigue siendo el esperado. Devuelve false si otro proceso lo
     * cambió antes (el llamador responde 409).
     */
    public boolean updateStatus(long orderId, OrderStatus expected, OrderStatus next) {
        return jdbc.update("UPDATE orders SET status = ?, updated_at = NOW() WHERE id = ? AND status = ?",
                next.name(), orderId, expected.name()) == 1;
    }

    // ---------------------------------------------------------------- lectura

    /** Bloquea la fila del pedido hasta el fin de la transacción (evita dos cambios o dos pagos simultáneos). */
    public Optional<OrderHeader> lockById(long orderId) {
        return jdbc.query("SELECT id, order_code, user_id, status, total_amount FROM orders WHERE id = ? FOR UPDATE",
                HEADER_MAPPER, orderId).stream().findFirst();
    }

    public Optional<OrderHeader> lockByCode(String orderCode) {
        return jdbc.query("""
                SELECT id, order_code, user_id, status, total_amount FROM orders WHERE order_code = ? FOR UPDATE
                """, HEADER_MAPPER, orderCode).stream().findFirst();
    }

    public Optional<Long> findIdByCodeAndUser(String orderCode, long userId) {
        return jdbc.queryForList("SELECT id FROM orders WHERE order_code = ? AND user_id = ?", Long.class,
                orderCode, userId).stream().findFirst();
    }

    public List<StockMovement> findStockMovements(long orderId) {
        return jdbc.query("""
                SELECT i.variant_id, SUM(i.quantity) AS quantity
                FROM order_items i JOIN order_lines l ON l.id = i.order_line_id
                WHERE l.order_id = ?
                GROUP BY i.variant_id ORDER BY i.variant_id
                """, (rs, row) -> new StockMovement(rs.getLong("variant_id"), rs.getInt("quantity")), orderId);
    }

    public List<OrderSummaryView> findSummariesByUser(long userId) {
        return jdbc.query("SELECT o.order_code, o.status, o.total_amount, o.created_at, " + UNITS
                        + " FROM orders o WHERE o.user_id = ? ORDER BY o.created_at DESC, o.id DESC",
                (rs, row) -> new OrderSummaryView(rs.getString("order_code"), rs.getString("status"),
                        rs.getBigDecimal("total_amount"), rs.getInt("units"),
                        rs.getObject("created_at", OffsetDateTime.class)), userId);
    }

    public List<AdminOrderSummaryView> findAdminPage(OrderStatus status, int limit, int offset) {
        String sql = """
                SELECT o.id, o.order_code, btrim(u.first_name || ' ' || u.last_name) AS customer_name,
                       u.email, o.total_amount, o.status, o.created_at,
                """ + UNITS + """
                FROM orders o JOIN users u ON u.id = o.user_id
                """;
        RowMapper<AdminOrderSummaryView> mapper = (rs, row) -> new AdminOrderSummaryView(rs.getLong("id"),
                rs.getString("order_code"), rs.getString("customer_name"), rs.getString("email"),
                rs.getBigDecimal("total_amount"), rs.getString("status"), rs.getInt("units"),
                rs.getObject("created_at", OffsetDateTime.class));
        String order = " ORDER BY o.created_at DESC, o.id DESC LIMIT ? OFFSET ?";
        if (status == null) {
            return jdbc.query(sql + order, mapper, limit, offset);
        }
        return jdbc.query(sql + " WHERE o.status = ?" + order, mapper, status.name(), limit, offset);
    }

    public long countAdmin(OrderStatus status) {
        Long count = status == null
                ? jdbc.queryForObject("SELECT count(*) FROM orders", Long.class)
                : jdbc.queryForObject("SELECT count(*) FROM orders WHERE status = ?", Long.class, status.name());
        return count == null ? 0 : count;
    }

    /** Cabecera del detalle (sin líneas, historial ni pagos: se cargan aparte). */
    public Optional<OrderDetailView> findDetail(long orderId) {
        return jdbc.query("""
                SELECT o.id, o.order_code, o.status, o.created_at, o.updated_at,
                       btrim(u.first_name || ' ' || u.last_name) AS customer_name, u.email,
                       o.subtotal, o.discount_amount, o.shipping_cost, o.total_amount,
                       sm.code AS method_code, sm.name AS method_name, o.receiver_name, o.phone, o.department,
                       o.province, o.district, o.street, o.reference, o.customer_note
                FROM orders o
                JOIN users u ON u.id = o.user_id
                JOIN shipping_methods sm ON sm.id = o.shipping_method_id
                WHERE o.id = ?
                """, (rs, row) -> new OrderDetailView(rs.getLong("id"), rs.getString("order_code"),
                rs.getString("status"), rs.getObject("created_at", OffsetDateTime.class),
                rs.getObject("updated_at", OffsetDateTime.class),
                new OrderDetailView.Customer(rs.getString("customer_name"), rs.getString("email")),
                rs.getBigDecimal("subtotal"), rs.getBigDecimal("discount_amount"), rs.getBigDecimal("shipping_cost"),
                rs.getBigDecimal("total_amount"),
                new OrderDetailView.Shipping(rs.getString("method_code"), rs.getString("method_name"),
                        rs.getString("receiver_name"), rs.getString("phone"), rs.getString("department"),
                        rs.getString("province"), rs.getString("district"), rs.getString("street"),
                        rs.getString("reference")),
                rs.getString("customer_note"), List.of(), List.of(), List.of(), List.of()), orderId)
                .stream().findFirst();
    }

    public List<OrderDetailView.Line> findLines(long orderId) {
        return jdbc.query("""
                SELECT l.id, l.product_id, l.product_name, t.code AS technique_code, t.name AS technique_name,
                       l.design_upload_id, l.quantity_total, l.tier_min_quantity, l.unit_base_price,
                       l.unit_customization_price, l.discount_percent, l.line_total
                FROM order_lines l
                LEFT JOIN customization_techniques t ON t.id = l.technique_id
                WHERE l.order_id = ?
                ORDER BY l.id
                """, (rs, row) -> {
            Long designId = rs.getObject("design_upload_id", Long.class);
            return new OrderDetailView.Line(rs.getLong("id"), rs.getLong("product_id"), rs.getString("product_name"),
                    rs.getString("technique_code"), rs.getString("technique_name"), designId,
                    designId == null ? null : DesignView.imageUrlFor(designId), rs.getInt("quantity_total"),
                    rs.getInt("tier_min_quantity"), rs.getBigDecimal("unit_base_price"),
                    rs.getBigDecimal("unit_customization_price"), rs.getBigDecimal("discount_percent"),
                    rs.getBigDecimal("line_total"), List.of(), List.of());
        }, orderId);
    }

    public List<LineZone> findZones(long orderId) {
        return jdbc.query("""
                SELECT lz.order_line_id, z.code, z.name, lz.surcharge
                FROM order_line_zones lz
                JOIN print_zones z ON z.id = lz.zone_id
                JOIN order_lines l ON l.id = lz.order_line_id
                WHERE l.order_id = ?
                ORDER BY z.id
                """, (rs, row) -> new LineZone(rs.getLong("order_line_id"), new OrderDetailView.Zone(
                rs.getString("code"), rs.getString("name"), rs.getBigDecimal("surcharge"))), orderId);
    }

    public List<LineItem> findItems(long orderId) {
        return jdbc.query("""
                SELECT i.order_line_id, i.variant_id, i.sku, i.size_name, i.color_name, i.quantity
                FROM order_items i
                JOIN order_lines l ON l.id = i.order_line_id
                WHERE l.order_id = ?
                ORDER BY i.id
                """, (rs, row) -> new LineItem(rs.getLong("order_line_id"), new OrderDetailView.Item(
                rs.getLong("variant_id"), rs.getString("sku"), rs.getString("size_name"), rs.getString("color_name"),
                rs.getInt("quantity"))), orderId);
    }

    public List<OrderDetailView.History> findHistory(long orderId) {
        return jdbc.query("""
                SELECT h.from_status, h.to_status, btrim(u.first_name || ' ' || u.last_name) AS changed_by,
                       h.comment, h.changed_at
                FROM order_status_history h
                LEFT JOIN users u ON u.id = h.changed_by
                WHERE h.order_id = ?
                ORDER BY h.changed_at, h.id
                """, (rs, row) -> new OrderDetailView.History(rs.getString("from_status"), rs.getString("to_status"),
                rs.getString("changed_by"), rs.getString("comment"),
                rs.getObject("changed_at", OffsetDateTime.class)), orderId);
    }

    public List<OrderDetailView.Payment> findPayments(long orderId) {
        return jdbc.query("""
                SELECT provider, provider_reference, amount, currency, status, created_at, confirmed_at
                FROM payments WHERE order_id = ? ORDER BY created_at, id
                """, (rs, row) -> new OrderDetailView.Payment(rs.getString("provider"),
                rs.getString("provider_reference"), rs.getBigDecimal("amount"), rs.getString("currency"),
                rs.getString("status"), rs.getObject("created_at", OffsetDateTime.class),
                rs.getObject("confirmed_at", OffsetDateTime.class)), orderId);
    }

    /** Zona de una línea del pedido (para agrupar por línea en el Service). */
    public record LineZone(long lineId, OrderDetailView.Zone zone) {
    }

    /** Ítem de una línea del pedido (para agrupar por línea en el Service). */
    public record LineItem(long lineId, OrderDetailView.Item item) {
    }
}
