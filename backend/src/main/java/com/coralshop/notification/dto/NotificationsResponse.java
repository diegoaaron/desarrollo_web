package com.coralshop.notification.dto;

import java.util.List;

/** Últimas notificaciones del cliente y cuántas hay sin leer en total (contador de la campana). */
public record NotificationsResponse(List<NotificationView> items, long unreadCount) {
}
