package com.coralshop.customization.controller;

import com.coralshop.customization.dto.CustomizationOptionsResponse;
import com.coralshop.customization.service.CustomizationService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Opciones del personalizador (público). */
@RestController
@RequestMapping("/api/products")
public class CustomizationController {

    private final CustomizationService customizationService;

    public CustomizationController(CustomizationService customizationService) {
        this.customizationService = customizationService;
    }

    @GetMapping("/{id}/customization-options")
    public CustomizationOptionsResponse options(@PathVariable Long id) {
        return customizationService.optionsFor(id);
    }
}
