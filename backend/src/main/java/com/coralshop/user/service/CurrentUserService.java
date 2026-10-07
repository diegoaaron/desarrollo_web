package com.coralshop.user.service;

import com.coralshop.user.model.User;
import com.coralshop.user.repository.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Traduce la sesión autenticada (identificada por el correo) al usuario de la base. */
@Service
public class CurrentUserService {

    private static final String ROLE_ADMIN = "ROLE_ADMIN";

    private final UserRepository userRepository;

    public CurrentUserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public long idOf(Authentication authentication) {
        return userOf(authentication).getId();
    }

    @Transactional(readOnly = true)
    public User userOf(Authentication authentication) {
        return userRepository.findByEmailIgnoreCase(authentication.getName())
                .orElseThrow(() -> new IllegalStateException("No existe el usuario autenticado"));
    }

    public boolean isAdmin(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .anyMatch(authority -> ROLE_ADMIN.equals(authority.getAuthority()));
    }
}
