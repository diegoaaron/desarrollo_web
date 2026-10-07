package com.coralshop.common.dto;

/**
 * Página pedida por el cliente, ya acotada: page empieza en 0 y size va de 1 a {@link #MAX_SIZE}.
 */
public record PageRequest(int page, int size) {

    public static final int MAX_SIZE = 100;

    public static PageRequest of(Integer page, Integer size, int defaultSize) {
        int safePage = page == null || page < 0 ? 0 : page;
        int safeSize = size == null || size < 1 ? defaultSize : Math.min(size, MAX_SIZE);
        return new PageRequest(safePage, safeSize);
    }

    public int offset() {
        return page * size;
    }
}
