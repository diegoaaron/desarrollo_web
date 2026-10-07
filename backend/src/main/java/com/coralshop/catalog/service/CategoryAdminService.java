package com.coralshop.catalog.service;

import com.coralshop.catalog.dto.CategoryRequest;
import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.NotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Mantenimiento de categorías (raíz) por el administrador. */
@Service
public class CategoryAdminService {

    private final CatalogOptionRepository optionRepository;

    public CategoryAdminService(CatalogOptionRepository optionRepository) {
        this.optionRepository = optionRepository;
    }

    @Transactional
    public CategoryView create(CategoryRequest request) {
        String name = request.name().trim();
        String description = normalize(request.description());
        if (optionRepository.rootCategoryNameTaken(name, null)) {
            throw new ConflictException("Ya existe una categoría con ese nombre");
        }
        long id = optionRepository.insertCategory(name, description);
        return new CategoryView(id, name, description == null ? "" : description);
    }

    @Transactional
    public CategoryView update(Long id, CategoryRequest request) {
        if (!optionRepository.categoryExists(id)) {
            throw new NotFoundException("Categoría no encontrada");
        }
        String name = request.name().trim();
        String description = normalize(request.description());
        if (optionRepository.rootCategoryNameTaken(name, id)) {
            throw new ConflictException("Ya existe una categoría con ese nombre");
        }
        optionRepository.updateCategory(id, name, description);
        return new CategoryView(id, name, description == null ? "" : description);
    }

    /** No se elimina una categoría con productos o subcategorías: se perdería la clasificación. */
    @Transactional
    public void delete(Long id) {
        if (!optionRepository.categoryExists(id)) {
            throw new NotFoundException("Categoría no encontrada");
        }
        if (optionRepository.categoryInUse(id)) {
            throw new ConflictException("La categoría tiene productos o subcategorías; reasígnalos antes de eliminarla");
        }
        optionRepository.deleteCategory(id);
    }

    private static String normalize(String description) {
        return description == null || description.isBlank() ? null : description.trim();
    }
}
