package com.coralshop.catalog.controller;

import com.coralshop.catalog.dto.CategoryRequest;
import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.service.CategoryAdminService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Escritura de categorías (solo ADMIN). La lectura es pública en {@link CatalogController}. */
@RestController
@RequestMapping("/api/categories")
public class AdminCategoryController {

    private final CategoryAdminService categoryAdminService;

    public AdminCategoryController(CategoryAdminService categoryAdminService) {
        this.categoryAdminService = categoryAdminService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CategoryView create(@Valid @RequestBody CategoryRequest request) {
        return categoryAdminService.create(request);
    }

    @PutMapping("/{id}")
    public CategoryView update(@PathVariable Long id, @Valid @RequestBody CategoryRequest request) {
        return categoryAdminService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        categoryAdminService.delete(id);
    }
}
