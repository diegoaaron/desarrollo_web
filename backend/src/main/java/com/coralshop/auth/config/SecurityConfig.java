package com.coralshop.auth.config;

import com.coralshop.auth.service.AuthService;
import com.coralshop.common.exception.ApiError;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.access.hierarchicalroles.RoleHierarchy;
import org.springframework.security.access.hierarchicalroles.RoleHierarchyImpl;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    /**
     * Un administrador también es cliente: puede comprar y ver sus pedidos con la misma
     * cuenta. Toda regla que exija ROLE_USER acepta también ROLE_ADMIN.
     */
    @Bean
    static RoleHierarchy roleHierarchy() {
        return RoleHierarchyImpl.withDefaultRolePrefix().role("ADMIN").implies("USER").build();
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http, ObjectMapper objectMapper,
                                                    AuthService authService) throws Exception {
        http.authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.GET, "/api/health", "/api/auth/csrf",
                        "/api/products", "/api/products/*", "/api/categories", "/api/brands").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login").permitAll()
                .requestMatchers("/api/auth/me").authenticated()
                // Escritura de categorías, usuarios y pedidos: rutas que completa la fase 2.
                .requestMatchers("/api/admin/**", "/api/stats/**", "/api/users/**", "/api/orders/**",
                        "/api/categories/**").hasRole("ADMIN")
                .anyRequest().authenticated()
        );

        http.formLogin(login -> login
                .loginProcessingUrl("/api/auth/login")
                .usernameParameter("email")
                .successHandler((request, response, authentication) -> {
                    response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                    response.setCharacterEncoding("UTF-8");
                    objectMapper.writeValue(response.getWriter(), authService.currentUser(authentication));
                })
                .failureHandler((request, response, exception) ->
                        writeError(response, objectMapper, HttpStatus.UNAUTHORIZED, "Correo o contraseña incorrectos"))
        );

        http.exceptionHandling(errors -> errors
                .authenticationEntryPoint((request, response, exception) ->
                        writeError(response, objectMapper, HttpStatus.UNAUTHORIZED, "Debes iniciar sesión"))
                .accessDeniedHandler((request, response, exception) ->
                        writeError(response, objectMapper, HttpStatus.FORBIDDEN,
                                "No tienes permiso para esta operación o tu sesión expiró"))
        );

        http.logout(logout -> logout
                .logoutUrl("/api/auth/logout")
                .logoutSuccessHandler((request, response, authentication) ->
                        response.setStatus(HttpStatus.NO_CONTENT.value()))
                .invalidateHttpSession(true)
                .deleteCookies("JSESSIONID")
        );

        // CSRF permanece activo: los POST necesitan el token de GET /api/auth/csrf.
        return http.build();
    }

    private static void writeError(HttpServletResponse response, ObjectMapper objectMapper,
                                   HttpStatus status, String message) throws IOException {
        response.setStatus(status.value());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        objectMapper.writeValue(response.getWriter(), ApiError.of(status.value(), message));
    }
}
