package com.coralshop.common.dto;

import java.util.List;

/** Página de resultados: los elementos de la página pedida y los totales para paginar. */
public record PageResponse<T>(List<T> items, int page, int size, long totalItems, int totalPages) {

    public static <T> PageResponse<T> of(List<T> items, int page, int size, long totalItems) {
        int totalPages = (int) ((totalItems + size - 1) / size);
        return new PageResponse<>(items, page, size, totalItems, totalPages);
    }
}
