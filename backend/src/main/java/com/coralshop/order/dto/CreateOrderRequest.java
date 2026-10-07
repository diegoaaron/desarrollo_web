package com.coralshop.order.dto;

import com.coralshop.pricing.dto.CartLineRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import java.util.List;

/**
 * Pedido desde el carrito. Con envío a domicilio, addressId es obligatorio. En el recojo
 * en tienda basta con contactPhone (o una dirección, de la que se toman nombre y teléfono).
 */
public record CreateOrderRequest(
        @NotEmpty @Size(max = 50) @Valid List<CartLineRequest> lines,
        @Positive Long addressId,
        @NotBlank @Size(max = 30) String shippingMethodCode,
        @Pattern(regexp = "\\+?[0-9 ]{6,20}", message = "Ingresa un teléfono válido (solo números)")
        String contactPhone,
        @Size(max = 500) String customerNote
) {
}
