package com.coralshop.shipping.controller;

import com.coralshop.shipping.dto.ShippingMethodView;
import com.coralshop.shipping.service.ShippingService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/shipping-methods")
public class ShippingController {

    private final ShippingService shippingService;

    public ShippingController(ShippingService shippingService) {
        this.shippingService = shippingService;
    }

    @GetMapping
    public List<ShippingMethodView> methods() {
        return shippingService.activeMethods();
    }
}
