package com.coralshop.auth.service;

import com.coralshop.user.model.Role;
import com.coralshop.user.model.User;
import com.coralshop.user.repository.RoleRepository;
import com.coralshop.user.repository.UserRepository;
import java.util.Locale;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Crea el administrador de desarrollo si todavía no existe. Nunca modifica una cuenta existente. */
@Service
public class DevAdminService {

    private static final Logger log = LoggerFactory.getLogger(DevAdminService.class);

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public DevAdminService(UserRepository userRepository, RoleRepository roleRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public void ensureAdmin(String firstName, String lastName, String email, String password) {
        String normalizedEmail = email.trim().toLowerCase(Locale.ROOT);
        if (userRepository.existsByEmailIgnoreCase(normalizedEmail)) {
            log.info("Administrador de desarrollo {} ya existe; no se modifica", normalizedEmail);
            return;
        }
        Role adminRole = roleRepository.findByName("ROLE_ADMIN")
                .orElseThrow(() -> new IllegalStateException("Falta el rol ROLE_ADMIN en la base de datos"));
        userRepository.save(new User(adminRole, firstName, lastName, normalizedEmail,
                passwordEncoder.encode(password)));
        log.info("Administrador de desarrollo {} creado", normalizedEmail);
    }
}
