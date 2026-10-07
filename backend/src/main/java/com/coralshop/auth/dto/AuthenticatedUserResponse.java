package com.coralshop.auth.dto;

public record AuthenticatedUserResponse(String firstName, String lastName, String email, String role) {
}
