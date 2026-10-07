package com.coralshop.user.dto;

import java.time.OffsetDateTime;

public record UserAdminView(Long id, String firstName, String lastName, String email, Long roleId, String roleName,
                            boolean isActive, OffsetDateTime createdAt) {
}
