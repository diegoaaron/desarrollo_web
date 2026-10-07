package com.coralshop.auth.service;

import com.coralshop.auth.dto.RegisterRequest;
import com.coralshop.auth.dto.RegisterResponse;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.InvalidRequestException;
import com.coralshop.user.model.Role;
import com.coralshop.user.model.User;
import com.coralshop.user.repository.RoleRepository;
import com.coralshop.user.repository.UserRepository;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RegistrationService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public RegistrationService(UserRepository userRepository, RoleRepository roleRepository,
                               PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public RegisterResponse register(RegisterRequest request) {
        String username = request.username().trim();
        String email = request.email().trim().toLowerCase(Locale.ROOT);

        if (username.length() < 3) {
            throw new InvalidRequestException("El usuario debe tener al menos 3 caracteres");
        }
        // BCrypt solo utiliza los primeros 72 bytes; rechazar el resto evita truncar contraseñas.
        if (request.password().getBytes(StandardCharsets.UTF_8).length > 72) {
            throw new InvalidRequestException("La contraseña es demasiado larga");
        }
        if (userRepository.existsByEmailIgnoreCase(email) || userRepository.existsByUsername(username)) {
            throw new ConflictException("El correo o usuario ya está registrado");
        }

        Role userRole = roleRepository.findByName("ROLE_USER")
                .orElseThrow(() -> new IllegalStateException("Falta el rol ROLE_USER en la base de datos"));

        User user = new User(userRole, username, email, passwordEncoder.encode(request.password()));
        try {
            User saved = userRepository.saveAndFlush(user);
            return new RegisterResponse(saved.getId(), saved.getUsername(), saved.getEmail());
        } catch (DataIntegrityViolationException exception) {
            // La restricción UNIQUE también protege si dos solicitudes llegan al mismo tiempo.
            throw new ConflictException("El correo o usuario ya está registrado", exception);
        }
    }
}
