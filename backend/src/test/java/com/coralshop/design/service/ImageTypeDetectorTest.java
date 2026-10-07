package com.coralshop.design.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.charset.StandardCharsets;
import java.util.Optional;
import org.junit.jupiter.api.Test;

class ImageTypeDetectorTest {

    @Test
    void recognizesPngAndJpegBySignature() {
        byte[] png = {(byte) 0x89, 'P', 'N', 'G', '\r', '\n', 0x1A, '\n', 0, 0};
        byte[] jpeg = {(byte) 0xFF, (byte) 0xD8, (byte) 0xFF, (byte) 0xE0, 0};

        assertEquals(Optional.of(ImageTypeDetector.PNG), ImageTypeDetector.detect(png));
        assertEquals(Optional.of(ImageTypeDetector.JPEG), ImageTypeDetector.detect(jpeg));
    }

    /** Un archivo renombrado a .png no pasa: lo que cuenta es su contenido. */
    @Test
    void rejectsOtherContentEvenIfNamedLikeAnImage() {
        assertTrue(ImageTypeDetector.detect("<svg onload=alert(1)>".getBytes(StandardCharsets.UTF_8)).isEmpty());
        assertTrue(ImageTypeDetector.detect("GIF89a".getBytes(StandardCharsets.US_ASCII)).isEmpty());
        assertTrue(ImageTypeDetector.detect(new byte[] {(byte) 0x89, 'P'}).isEmpty());
        assertTrue(ImageTypeDetector.detect(new byte[0]).isEmpty());
        assertTrue(ImageTypeDetector.detect(null).isEmpty());
    }
}
