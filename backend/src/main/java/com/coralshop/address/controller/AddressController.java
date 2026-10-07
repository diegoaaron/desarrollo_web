package com.coralshop.address.controller;

import com.coralshop.address.dto.AddressRequest;
import com.coralshop.address.dto.AddressView;
import com.coralshop.address.service.AddressService;
import com.coralshop.user.service.CurrentUserService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Direcciones del cliente autenticado. */
@RestController
@RequestMapping("/api/addresses")
public class AddressController {

    private final AddressService addressService;
    private final CurrentUserService currentUserService;

    public AddressController(AddressService addressService, CurrentUserService currentUserService) {
        this.addressService = addressService;
        this.currentUserService = currentUserService;
    }

    @GetMapping
    public List<AddressView> list(Authentication authentication) {
        return addressService.list(currentUserService.idOf(authentication));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public AddressView create(@Valid @RequestBody AddressRequest request, Authentication authentication) {
        return addressService.create(currentUserService.idOf(authentication), request);
    }

    @PutMapping("/{id}")
    public AddressView update(@PathVariable Long id, @Valid @RequestBody AddressRequest request,
                              Authentication authentication) {
        return addressService.update(currentUserService.idOf(authentication), id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id, Authentication authentication) {
        addressService.delete(currentUserService.idOf(authentication), id);
    }
}
