package com.coralshop.payment.controller;

import com.coralshop.payment.dto.PaymentRequest;
import com.coralshop.payment.dto.PaymentResponse;
import com.coralshop.payment.service.PaymentService;
import com.coralshop.user.service.CurrentUserService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Pago del pedido por su dueño. */
@RestController
@RequestMapping("/api/orders")
public class PaymentController {

    private final PaymentService paymentService;
    private final CurrentUserService currentUserService;

    public PaymentController(PaymentService paymentService, CurrentUserService currentUserService) {
        this.paymentService = paymentService;
        this.currentUserService = currentUserService;
    }

    @PostMapping("/{code}/payment")
    public PaymentResponse pay(@PathVariable String code, @Valid @RequestBody PaymentRequest request,
                               Authentication authentication) {
        return paymentService.pay(currentUserService.idOf(authentication), code, request);
    }
}
