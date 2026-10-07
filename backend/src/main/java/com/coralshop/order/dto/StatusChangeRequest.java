package com.coralshop.order.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record StatusChangeRequest(@NotBlank @Size(max = 20) String status, @Size(max = 500) String comment) {
}
