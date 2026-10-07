package com.coralshop.pricing.controller;

import com.coralshop.pricing.dto.CartLineRequest;
import com.coralshop.pricing.dto.QuoteRequest;
import com.coralshop.pricing.dto.QuoteResponse;
import com.coralshop.pricing.service.PricingService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Cotización del carrito (pública: el invitado también ve precios). */
@RestController
@RequestMapping("/api/quotes")
public class QuoteController {

    private final PricingService pricingService;

    public QuoteController(PricingService pricingService) {
        this.pricingService = pricingService;
    }

    @PostMapping
    public QuoteResponse quote(@Valid @RequestBody QuoteRequest request) {
        return pricingService.quote(request.lines().stream().map(CartLineRequest::toSpec).toList());
    }
}
