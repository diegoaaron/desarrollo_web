package com.coralshop.auth.dto;

public record AuthenticatedUserResponse(String username, String email, String role) {
}
