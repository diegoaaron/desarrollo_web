package com.coralshop.address.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record AddressRequest(
        @NotBlank @Size(max = 160) String receiverName,
        @NotBlank @Pattern(regexp = "\\+?[0-9 ]{6,20}", message = "Ingresa un teléfono válido (solo números)")
        String phone,
        @NotBlank @Size(max = 60) String department,
        @NotBlank @Size(max = 60) String province,
        @NotBlank @Size(max = 60) String district,
        @NotBlank @Size(max = 200) String street,
        @Size(max = 200) String reference,
        boolean isDefault
) {
}
