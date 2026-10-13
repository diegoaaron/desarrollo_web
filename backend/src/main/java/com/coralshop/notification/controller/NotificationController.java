package com.coralshop.notification.controller;

import com.coralshop.notification.dto.NotificationsResponse;
import com.coralshop.notification.service.NotificationService;
import com.coralshop.user.service.CurrentUserService;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Notificaciones del cliente autenticado (campana del header). */
@RestController
@RequestMapping("/api/notifications")
public class NotificationController {

    private final NotificationService notificationService;
    private final CurrentUserService currentUserService;

    public NotificationController(NotificationService notificationService, CurrentUserService currentUserService) {
        this.notificationService = notificationService;
        this.currentUserService = currentUserService;
    }

    @GetMapping("/me")
    public NotificationsResponse mine(Authentication authentication) {
        return notificationService.latest(currentUserService.idOf(authentication));
    }

    @PutMapping("/{id}/read")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markRead(@PathVariable Long id, Authentication authentication) {
        notificationService.markRead(currentUserService.idOf(authentication), id);
    }

    @PutMapping("/me/read")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markAllRead(Authentication authentication) {
        notificationService.markAllRead(currentUserService.idOf(authentication));
    }
}
