package com.coralshop.auth.config;

import com.coralshop.auth.service.DevAdminService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

/**
 * Al arrancar con el perfil {@code dev}, garantiza que exista el administrador de
 * desarrollo definido en {@code application-dev.properties}. En producción (sin el perfil
 * {@code dev}) este componente no se carga.
 */
@Component
@Profile("dev")
public class DevAdminInitializer implements ApplicationRunner {

    private final DevAdminService devAdminService;
    private final String username;
    private final String email;
    private final String password;

    public DevAdminInitializer(DevAdminService devAdminService,
                               @Value("${app.dev-admin.username}") String username,
                               @Value("${app.dev-admin.email}") String email,
                               @Value("${app.dev-admin.password}") String password) {
        this.devAdminService = devAdminService;
        this.username = username;
        this.email = email;
        this.password = password;
    }

    @Override
    public void run(ApplicationArguments args) {
        devAdminService.ensureAdmin(username, email, password);
    }
}
