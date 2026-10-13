package com.coralshop.notification.dto;

import java.time.OffsetDateTime;

public record NotificationView(Long id, String title, String message, String link, boolean isRead,
                               OffsetDateTime createdAt) {
}
