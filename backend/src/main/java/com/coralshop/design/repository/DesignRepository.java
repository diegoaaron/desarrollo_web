package com.coralshop.design.repository;

import com.coralshop.design.dto.DesignView;
import com.coralshop.design.model.DesignImage;
import java.sql.PreparedStatement;
import java.time.OffsetDateTime;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Repository;

/** Diseños subidos por los clientes (imagen en bytea). */
@Repository
public class DesignRepository {

    private static final String VIEW_COLUMNS = "id, original_filename, content_type, size_bytes, created_at";

    private static final RowMapper<DesignView> VIEW_MAPPER = (rs, row) -> {
        long id = rs.getLong("id");
        return new DesignView(id, rs.getString("original_filename"), rs.getString("content_type"),
                rs.getInt("size_bytes"), rs.getObject("created_at", OffsetDateTime.class), DesignView.imageUrlFor(id));
    };

    private final JdbcTemplate jdbc;

    public DesignRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Optional<DesignView> findByUserAndHash(Long userId, String sha256) {
        return jdbc.query("SELECT " + VIEW_COLUMNS + " FROM design_uploads WHERE user_id = ? AND sha256 = ?"
                        + " ORDER BY id LIMIT 1", VIEW_MAPPER, userId, sha256).stream().findFirst();
    }

    public DesignView insert(Long userId, String filename, String contentType, byte[] data, String sha256) {
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO design_uploads (user_id, original_filename, content_type, size_bytes, sha256, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, new String[] {"id"});
            statement.setLong(1, userId);
            statement.setString(2, filename);
            statement.setString(3, contentType);
            statement.setInt(4, data.length);
            statement.setString(5, sha256);
            statement.setBytes(6, data);
            return statement;
        }, keys);
        long id = keys.getKey().longValue();
        return jdbc.queryForObject("SELECT " + VIEW_COLUMNS + " FROM design_uploads WHERE id = ?", VIEW_MAPPER, id);
    }

    public Optional<Long> findOwnerId(Long designId) {
        return jdbc.queryForList("SELECT user_id FROM design_uploads WHERE id = ?", Long.class, designId)
                .stream().findFirst();
    }

    public boolean isOwnedBy(Long designId, Long userId) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM design_uploads WHERE id = ? AND user_id = ?",
                Integer.class, designId, userId);
        return count != null && count > 0;
    }

    public Optional<DesignImage> findImage(Long designId) {
        return jdbc.query("SELECT content_type, data FROM design_uploads WHERE id = ?",
                (rs, row) -> new DesignImage(rs.getString("content_type"), rs.getBytes("data")), designId)
                .stream().findFirst();
    }
}
