package com.coralshop.order.controller;

import com.coralshop.order.dto.CreateOrderRequest;
import com.coralshop.order.dto.CreatedOrderResponse;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.dto.OrderSummaryView;
import com.coralshop.order.service.OrderService;
import com.coralshop.user.service.CurrentUserService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Pedidos del cliente autenticado (ROLE_USER, que también cumple un administrador). */
@RestController
@RequestMapping("/api/orders")
public class CustomerOrderController {

    private final OrderService orderService;
    private final CurrentUserService currentUserService;

    public CustomerOrderController(OrderService orderService, CurrentUserService currentUserService) {
        this.orderService = orderService;
        this.currentUserService = currentUserService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CreatedOrderResponse create(@Valid @RequestBody CreateOrderRequest request, Authentication authentication) {
        return orderService.create(currentUserService.idOf(authentication), request);
    }

    @GetMapping("/me")
    public List<OrderSummaryView> myOrders(Authentication authentication) {
        return orderService.myOrders(currentUserService.idOf(authentication));
    }

    @GetMapping("/me/{code}")
    public OrderDetailView myOrder(@PathVariable String code, Authentication authentication) {
        return orderService.myOrder(currentUserService.idOf(authentication), code);
    }
}
