package com.coralshop.docs.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import java.util.List;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Documento OpenAPI que sirve Swagger UI en /api/docs (springdoc lo completa con los controladores). */
@Configuration
public class OpenApiConfig {

    private static final String SESSION = "sesion";
    private static final String CSRF = "csrf";

    @Bean
    public OpenAPI coralShopOpenApi() {
        return new OpenAPI()
                .info(new Info()
                        .title("Coral Shop API")
                        .version("fase 5")
                        .description("""
                                API de la tienda de prendas personalizables Coral Shop.

                                **Cómo autenticarse desde esta página**
                                1. `GET /api/auth/csrf` y copia el `token` de la respuesta.
                                2. Pulsa **Authorize** y pega el token en `X-CSRF-TOKEN`.
                                3. `POST /api/auth/login` (formulario: `email`, `password`). La cookie de
                                   sesión `JSESSIONID` queda en el navegador.
                                4. El login renueva el token: repite el paso 1 y 2 antes de escribir.

                                Errores con cuerpo uniforme `{ status, message, errors }`: 400 formato,
                                401 sin sesión, 403 sin permiso o sin CSRF, 404 no existe (o es de otro
                                cliente), 409 conflicto (stock), 422 regla de negocio.""")
                        .license(new License().name("Apache 2.0").url("https://www.apache.org/licenses/LICENSE-2.0")))
                .servers(List.of(new Server().url("/").description("Mismo origen que esta página")))
                .components(new Components()
                        .addSecuritySchemes(SESSION, new SecurityScheme()
                                .type(SecurityScheme.Type.APIKEY).in(SecurityScheme.In.COOKIE).name("JSESSIONID")
                                .description("Sesión creada por POST /api/auth/login"))
                        .addSecuritySchemes(CSRF, new SecurityScheme()
                                .type(SecurityScheme.Type.APIKEY).in(SecurityScheme.In.HEADER).name("X-CSRF-TOKEN")
                                .description("Token de GET /api/auth/csrf; obligatorio en POST, PUT, PATCH y DELETE")))
                .addSecurityItem(new SecurityRequirement().addList(SESSION).addList(CSRF));
    }
}
