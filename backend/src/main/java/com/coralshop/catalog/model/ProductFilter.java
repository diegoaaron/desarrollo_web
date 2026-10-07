package com.coralshop.catalog.model;

/** Filtros del catálogo público; un valor nulo significa «sin filtrar por ese campo». */
public record ProductFilter(String typeCode, Long categoryId, String text) {
}
