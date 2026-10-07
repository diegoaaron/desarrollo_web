package com.coralshop.design.service;

import com.coralshop.common.exception.InvalidRequestException;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.design.dto.DesignView;
import com.coralshop.design.model.DesignImage;
import com.coralshop.design.repository.DesignRepository;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Subida y consulta de los diseños (imágenes) del cliente. */
@Service
public class DesignService {

    /** 5 MB (D7); coincide con el CHECK de design_uploads y con spring.servlet.multipart.max-file-size. */
    public static final int MAX_BYTES = 5 * 1024 * 1024;

    private static final int MAX_FILENAME = 255;

    private final DesignRepository designRepository;

    public DesignService(DesignRepository designRepository) {
        this.designRepository = designRepository;
    }

    /**
     * Guarda el diseño del usuario. Si ya subió exactamente la misma imagen, devuelve la
     * existente en lugar de duplicarla.
     */
    @Transactional
    public DesignView upload(long userId, String originalFilename, byte[] content) {
        if (content == null || content.length == 0) {
            throw new InvalidRequestException("El archivo está vacío");
        }
        if (content.length > MAX_BYTES) {
            throw new InvalidRequestException("El diseño no puede superar los 5 MB");
        }
        String contentType = ImageTypeDetector.detect(content)
                .orElseThrow(() -> new InvalidRequestException("Solo se aceptan imágenes PNG o JPG"));
        String sha256 = sha256(content);
        return designRepository.findByUserAndHash(userId, sha256)
                .orElseGet(() -> designRepository.insert(userId, cleanFilename(originalFilename), contentType,
                        content, sha256));
    }

    /** El dueño del diseño y los administradores pueden verlo; para el resto no existe. */
    @Transactional(readOnly = true)
    public DesignImage image(long designId, long userId, boolean admin) {
        Long ownerId = designRepository.findOwnerId(designId)
                .orElseThrow(() -> new NotFoundException("Diseño no encontrado"));
        if (!admin && ownerId != userId) {
            throw new NotFoundException("Diseño no encontrado");
        }
        return designRepository.findImage(designId)
                .orElseThrow(() -> new NotFoundException("Diseño no encontrado"));
    }

    /** Solo el nombre (sin rutas) y con un largo que entre en la columna. */
    private static String cleanFilename(String filename) {
        if (filename == null || filename.isBlank()) {
            return "diseño";
        }
        String name = filename.replace('\\', '/');
        name = name.substring(name.lastIndexOf('/') + 1).strip();
        if (name.isEmpty()) {
            return "diseño";
        }
        return name.length() > MAX_FILENAME ? name.substring(name.length() - MAX_FILENAME) : name;
    }

    private static String sha256(byte[] content) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(content));
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 no disponible", exception);
        }
    }
}
