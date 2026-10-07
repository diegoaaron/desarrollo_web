package com.coralshop.order.controller;

import com.coralshop.common.dto.PageRequest;
import com.coralshop.common.dto.PageResponse;
import com.coralshop.order.dto.AdminOrderSummaryView;
import com.coralshop.order.dto.OrderDetailView;
import com.coralshop.order.dto.StatusChangeRequest;
import com.coralshop.order.service.OrderAdminService;
import com.coralshop.user.service.CurrentUserService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** Bandeja de pedidos (solo ADMIN). Las rutas /me son del cliente, ver {@link CustomerOrderController}. */
@RestController
@RequestMapping("/api/orders")
public class AdminOrderController {

    private static final int DEFAULT_PAGE_SIZE = 20;

    private final OrderAdminService orderAdminService;
    private final CurrentUserService currentUserService;

    public AdminOrderController(OrderAdminService orderAdminService, CurrentUserService currentUserService) {
        this.orderAdminService = orderAdminService;
        this.currentUserService = currentUserService;
    }

    @GetMapping
    public PageResponse<AdminOrderSummaryView> orders(@RequestParam(required = false) String status,
                                                      @RequestParam(required = false) Integer page,
                                                      @RequestParam(required = false) Integer size) {
        return orderAdminService.orders(status, PageRequest.of(page, size, DEFAULT_PAGE_SIZE));
    }

    @GetMapping("/{id:\\d+}")
    public OrderDetailView order(@PathVariable Long id) {
        return orderAdminService.order(id);
    }

    @PutMapping("/{id:\\d+}/status")
    public OrderDetailView changeStatus(@PathVariable Long id, @Valid @RequestBody StatusChangeRequest request,
                                        Authentication authentication) {
        return orderAdminService.changeStatus(currentUserService.idOf(authentication), id, request);
    }
}
