package com.coralshop.demo.config;

import com.coralshop.demo.service.DemoDataService;
import java.security.SecureRandom;
import java.util.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

/**
 * Con el perfil {@code demo}, carga los datos de demostración al arrancar (una sola vez; ver
 * {@link DemoDataService}). Si no se define {@code DEMO_ADMIN_PASSWORD}, genera una contraseña
 * aleatoria para el administrador demo y la muestra una vez en el log: así un despliegue
 * público nunca queda con una clave conocida.
 */
@Component
@Profile("demo")
public class DemoDataInitializer implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(DemoDataInitializer.class);

    private final DemoDataService demoDataService;
    private final String adminEmail;
    private final String adminPassword;
    private final String customerPassword;

    public DemoDataInitializer(DemoDataService demoDataService,
                               @Value("${app.demo.admin-email}") String adminEmail,
                               @Value("${app.demo.admin-password:}") String adminPassword,
                               @Value("${app.demo.customer-password}") String customerPassword) {
        this.demoDataService = demoDataService;
        this.adminEmail = adminEmail;
        this.adminPassword = adminPassword;
        this.customerPassword = customerPassword;
    }

    @Override
    public void run(ApplicationArguments args) {
        String password = adminPassword;
        if (password.isBlank()) {
            byte[] random = new byte[12];
            new SecureRandom().nextBytes(random);
            password = Base64.getUrlEncoder().withoutPadding().encodeToString(random);
            log.warn("DEMO_ADMIN_PASSWORD no está definida. Si se crea el administrador demo {}, su contraseña "
                    + "será: {}", adminEmail, password);
        }
        demoDataService.load(adminEmail, password, customerPassword);
    }
}
