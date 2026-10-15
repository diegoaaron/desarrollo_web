package com.coralshop.demo.service;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import javax.imageio.ImageIO;

/** Dibuja los logos ficticios que los clientes demo «suben» como diseño (PNG con fondo transparente). */
final class DemoLogoFactory {

    private static final int SIZE = 600;

    private DemoLogoFactory() {
    }

    /** Insignia circular con unas iniciales y una leyenda debajo. */
    static byte[] badge(String initials, String caption, Color main, Color accent) {
        BufferedImage image = new BufferedImage(SIZE, SIZE, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();
        try {
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

            g.setColor(main);
            g.fillOval(40, 40, SIZE - 80, SIZE - 80);
            g.setColor(accent);
            g.setStroke(new BasicStroke(18));
            g.drawOval(70, 70, SIZE - 140, SIZE - 140);

            g.setColor(Color.WHITE);
            g.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 190));
            centered(g, initials, SIZE / 2 + 30);
            g.setColor(accent);
            g.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 46));
            centered(g, caption, SIZE / 2 + 130);
        } finally {
            g.dispose();
        }
        return png(image);
    }

    private static void centered(Graphics2D g, String text, int baseline) {
        FontMetrics metrics = g.getFontMetrics();
        g.drawString(text, (SIZE - metrics.stringWidth(text)) / 2, baseline);
    }

    private static byte[] png(BufferedImage image) {
        try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            ImageIO.write(image, "png", out);
            return out.toByteArray();
        } catch (IOException exception) {
            throw new UncheckedIOException(exception);
        }
    }
}
