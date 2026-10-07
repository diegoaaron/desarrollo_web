package com.coralshop.common.exception;

import java.util.Map;

/** Cuerpo JSON uniforme de todas las respuestas de error de la API. */
public record ApiError(int status, String message, Map<String, String> errors) {

    public static ApiError of(int status, String message) {
        return new ApiError(status, message, Map.of());
    }
}
