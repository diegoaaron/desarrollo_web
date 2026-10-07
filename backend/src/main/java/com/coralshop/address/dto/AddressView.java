package com.coralshop.address.dto;

public record AddressView(Long id, String receiverName, String phone, String department, String province,
                          String district, String street, String reference, boolean isDefault) {
}
