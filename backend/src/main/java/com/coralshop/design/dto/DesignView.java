package com.coralshop.design.dto;

import java.time.OffsetDateTime;

public record DesignView(Long id, String originalFilename, String contentType, int sizeBytes,
                         OffsetDateTime createdAt, String imageUrl) {

    /** Ruta del endpoint que sirve la imagen (solo para su dueño y los administradores). */
    public static String imageUrlFor(long designId) {
        return "/api/designs/" + designId + "/image";
    }
}
