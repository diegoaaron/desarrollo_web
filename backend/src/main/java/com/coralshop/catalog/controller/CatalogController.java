package com.coralshop.catalog.controller;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductTypeView;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.service.CatalogService;
import com.coralshop.common.dto.PageRequest;
import com.coralshop.common.dto.PageResponse;
import jakarta.validation.constraints.Size;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** Catálogo público de la tienda. */
@RestController
@RequestMapping("/api")
public class CatalogController {

    private static final int DEFAULT_PAGE_SIZE = 12;

    private final CatalogService catalogService;

    public CatalogController(CatalogService catalogService) {
        this.catalogService = catalogService;
    }

    /** Catálogo filtrado por tipo (código), categoría y texto, paginado desde la página 0. */
    @GetMapping("/products")
    public PageResponse<ProductView> products(@RequestParam(required = false) @Size(max = 30) String type,
                                              @RequestParam(required = false) Long category,
                                              @RequestParam(required = false) @Size(max = 100) String q,
                                              @RequestParam(required = false) Integer page,
                                              @RequestParam(required = false) Integer size) {
        return catalogService.activeProducts(type, category, q, PageRequest.of(page, size, DEFAULT_PAGE_SIZE));
    }

    @GetMapping("/products/{id}")
    public ProductView product(@PathVariable Long id) {
        return catalogService.productDetail(id);
    }

    @GetMapping("/categories")
    public List<CategoryView> categories() {
        return catalogService.activeCategories();
    }

    @GetMapping("/brands")
    public List<OptionView> brands() {
        return catalogService.activeBrands();
    }

    @GetMapping("/product-types")
    public List<ProductTypeView> productTypes() {
        return catalogService.activeProductTypes();
    }
}
