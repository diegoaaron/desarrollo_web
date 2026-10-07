package com.coralshop.catalog.controller;

import com.coralshop.catalog.dto.CatalogOptionsResponse;
import com.coralshop.catalog.dto.CreateProductRequest;
import com.coralshop.catalog.dto.CreatedResponse;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.service.ProductAdminService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Mantenimiento de productos (solo ADMIN, ver SecurityConfig). */
@RestController
@RequestMapping("/api/admin")
public class AdminProductController {

    private final ProductAdminService productAdminService;

    public AdminProductController(ProductAdminService productAdminService) {
        this.productAdminService = productAdminService;
    }

    @GetMapping("/products")
    public List<ProductView> products() {
        return productAdminService.allProducts();
    }

    @GetMapping("/catalog-options")
    public CatalogOptionsResponse options() {
        return productAdminService.catalogOptions();
    }

    @PostMapping("/products")
    @ResponseStatus(HttpStatus.CREATED)
    public CreatedResponse create(@Valid @RequestBody CreateProductRequest request) {
        return new CreatedResponse(productAdminService.create(request));
    }
}
