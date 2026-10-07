package com.coralshop.design.model;

/** Contenido de un diseño listo para enviarse al navegador. */
public record DesignImage(String contentType, byte[] data) {
}
