package com.coralshop.user.repository;

import com.coralshop.user.dto.UserAdminView;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

/** Listado y cambio de rol de cuentas para el panel de administración. */
@Repository
public class UserAdminRepository {

    private static final String USERS_SQL = """
            SELECT u.id, u.first_name, u.last_name, u.email, u.role_id, r.name AS role_name, u.is_active,
                   u.created_at
            FROM users u JOIN roles r ON r.id = u.role_id
            """;

    private static final RowMapper<UserAdminView> MAPPER = (rs, row) -> new UserAdminView(rs.getLong("id"),
            rs.getString("first_name"), rs.getString("last_name"), rs.getString("email"), rs.getLong("role_id"),
            rs.getString("role_name"), rs.getBoolean("is_active"), rs.getObject("created_at", OffsetDateTime.class));

    private final JdbcTemplate jdbc;

    public UserAdminRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<UserAdminView> findAll() {
        return jdbc.query(USERS_SQL + " ORDER BY u.created_at DESC, u.id DESC", MAPPER);
    }

    public Optional<UserAdminView> findById(Long id) {
        return jdbc.query(USERS_SQL + " WHERE u.id = ?", MAPPER, id).stream().findFirst();
    }

    public boolean roleExists(Long roleId) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM roles WHERE id = ?", Integer.class, roleId);
        return count != null && count > 0;
    }

    public void updateRole(Long userId, Long roleId) {
        jdbc.update("UPDATE users SET role_id = ?, updated_at = NOW() WHERE id = ?", roleId, userId);
    }
}
