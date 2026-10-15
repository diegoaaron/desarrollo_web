package com.coralshop.support;

import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Import;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Testcontainers;

/**
 * Base de las pruebas de integración: la aplicación completa (seguridad, controladores,
 * servicios, Flyway V1–V6) contra un PostgreSQL 16 real levantado por Testcontainers.
 * El contenedor se comparte entre todas las clases; cada prueba crea sus propios datos con
 * correos y SKU únicos, así que no dependen del orden. Sin Docker, las pruebas se omiten.
 */
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers(disabledWithoutDocker = true)
@Import(TestData.class)
public abstract class IntegrationTest {

    @ServiceConnection
    static final PostgreSQLContainer<?> POSTGRES = new PostgreSQLContainer<>("postgres:16-alpine");

    static {
        if (DockerClientFactory.instance().isDockerAvailable()) {
            POSTGRES.start();
        }
    }
}
