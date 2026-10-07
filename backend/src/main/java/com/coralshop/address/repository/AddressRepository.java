package com.coralshop.address.repository;

import com.coralshop.address.dto.AddressView;
import java.sql.PreparedStatement;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Libreta de direcciones. Toda consulta va filtrada por el dueño. */
@Repository
public class AddressRepository {

    private static final String COLUMNS =
            "id, receiver_name, phone, department, province, district, street, reference, is_default";

    private static final RowMapper<AddressView> MAPPER = (rs, row) -> new AddressView(rs.getLong("id"),
            rs.getString("receiver_name"), rs.getString("phone"), rs.getString("department"),
            rs.getString("province"), rs.getString("district"), rs.getString("street"), rs.getString("reference"),
            rs.getBoolean("is_default"));

    private final JdbcTemplate jdbc;

    public AddressRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<AddressView> findByUser(Long userId) {
        return jdbc.query("SELECT " + COLUMNS + " FROM addresses WHERE user_id = ? ORDER BY is_default DESC, id DESC",
                MAPPER, userId);
    }

    public Optional<AddressView> findByIdAndUser(Long id, Long userId) {
        return jdbc.query("SELECT " + COLUMNS + " FROM addresses WHERE id = ? AND user_id = ?", MAPPER, id, userId)
                .stream().findFirst();
    }

    public int countByUser(Long userId) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM addresses WHERE user_id = ?", Integer.class, userId);
        return count == null ? 0 : count;
    }

    public long insert(Long userId, AddressView address) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO addresses (user_id, receiver_name, phone, department, province, district, street,
                                           reference, is_default)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setLong(1, userId);
            statement.setString(2, address.receiverName());
            statement.setString(3, address.phone());
            statement.setString(4, address.department());
            statement.setString(5, address.province());
            statement.setString(6, address.district());
            statement.setString(7, address.street());
            statement.setString(8, address.reference());
            statement.setBoolean(9, address.isDefault());
            return statement;
        }, keys);
        return keys.getKey().longValue();
    }

    public void update(Long id, Long userId, AddressView address) {
        jdbc.update("""
                UPDATE addresses
                SET receiver_name = ?, phone = ?, department = ?, province = ?, district = ?, street = ?,
                    reference = ?, is_default = ?, updated_at = NOW()
                WHERE id = ? AND user_id = ?
                """, address.receiverName(), address.phone(), address.department(), address.province(),
                address.district(), address.street(), address.reference(), address.isDefault(), id, userId);
    }

    /** Quita la marca de predeterminada a todas las direcciones del usuario (antes de asignarla a otra). */
    public void clearDefault(Long userId) {
        jdbc.update("UPDATE addresses SET is_default = FALSE WHERE user_id = ? AND is_default", userId);
    }

    /** Marca como predeterminada la dirección más reciente del usuario, si tiene alguna. */
    public void makeNewestDefault(Long userId) {
        jdbc.update("""
                UPDATE addresses SET is_default = TRUE
                WHERE id = (SELECT id FROM addresses WHERE user_id = ? ORDER BY id DESC LIMIT 1)
                """, userId);
    }

    public int delete(Long id, Long userId) {
        return jdbc.update("DELETE FROM addresses WHERE id = ? AND user_id = ?", id, userId);
    }
}
