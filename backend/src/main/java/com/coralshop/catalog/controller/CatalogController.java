package com.coralshop.catalog.controller;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.service.CatalogService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Catálogo público de la tienda. */
@RestController
@RequestMapping("/api")
public class CatalogController {

    private final CatalogService catalogService;

    public CatalogController(CatalogService catalogService) {
        this.catalogService = catalogService;
    }

    @GetMapping("/products")
    public List<ProductView> products() {
        return catalogService.activeProducts();
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
}
