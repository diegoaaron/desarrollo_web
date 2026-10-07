package com.coralshop.design.service;

import java.util.Optional;

/**
 * Reconoce el tipo real de una imagen por su firma binaria (los primeros bytes), no por la
 * extensión ni por el Content-Type que declara el navegador, que el cliente puede falsear.
 */
public final class ImageTypeDetector {

    public static final String PNG = "image/png";
    public static final String JPEG = "image/jpeg";

    private static final byte[] PNG_SIGNATURE = {(byte) 0x89, 'P', 'N', 'G', '\r', '\n', 0x1A, '\n'};
    private static final byte[] JPEG_SIGNATURE = {(byte) 0xFF, (byte) 0xD8, (byte) 0xFF};

    private ImageTypeDetector() {
    }

    public static Optional<String> detect(byte[] content) {
        if (startsWith(content, PNG_SIGNATURE)) {
            return Optional.of(PNG);
        }
        if (startsWith(content, JPEG_SIGNATURE)) {
            return Optional.of(JPEG);
        }
        return Optional.empty();
    }

    private static boolean startsWith(byte[] content, byte[] signature) {
        if (content == null || content.length < signature.length) {
            return false;
        }
        for (int i = 0; i < signature.length; i++) {
            if (content[i] != signature[i]) {
                return false;
            }
        }
        return true;
    }
}
