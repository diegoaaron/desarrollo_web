package com.coralshop.auth.service;

import com.coralshop.auth.dto.AuthenticatedUserResponse;
import com.coralshop.user.model.User;
import com.coralshop.user.repository.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;

    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public AuthenticatedUserResponse currentUser(Authentication authentication) {
        String email = authentication.getName();
        User user = userRepository.findByEmailIgnoreCase(email)
                .orElseThrow(() -> new IllegalStateException("No existe el usuario autenticado"));
        String role = authentication.getAuthorities().iterator().next().getAuthority();
        return new AuthenticatedUserResponse(user.getFirstName(), user.getLastName(), email, role);
    }
}
