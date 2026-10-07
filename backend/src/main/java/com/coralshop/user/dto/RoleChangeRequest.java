package com.coralshop.user.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record RoleChangeRequest(@NotNull @Positive Long roleId) {
}
