package com.coralshop.user.controller;

import com.coralshop.user.dto.RoleChangeRequest;
import com.coralshop.user.dto.UserAdminView;
import com.coralshop.user.service.CurrentUserService;
import com.coralshop.user.service.UserAdminService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Cuentas de la tienda (solo ADMIN). */
@RestController
@RequestMapping("/api/users")
public class UserAdminController {

    private final UserAdminService userAdminService;
    private final CurrentUserService currentUserService;

    public UserAdminController(UserAdminService userAdminService, CurrentUserService currentUserService) {
        this.userAdminService = userAdminService;
        this.currentUserService = currentUserService;
    }

    @GetMapping
    public List<UserAdminView> users() {
        return userAdminService.users();
    }

    @PutMapping("/{id}/role")
    public UserAdminView changeRole(@PathVariable Long id, @Valid @RequestBody RoleChangeRequest request,
                                    Authentication authentication) {
        return userAdminService.changeRole(currentUserService.idOf(authentication), id, request.roleId());
    }
}
