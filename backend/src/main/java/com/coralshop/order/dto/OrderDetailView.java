package com.coralshop.order.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;

/** Detalle completo del pedido, con su línea de tiempo. nextStatuses solo se llena para el administrador. */
public record OrderDetailView(Long id, String orderCode, String status, OffsetDateTime createdAt,
                              OffsetDateTime updatedAt, Customer customer, BigDecimal subtotal,
                              BigDecimal discountAmount, BigDecimal shippingCost, BigDecimal totalAmount,
                              Shipping shipping, String customerNote, List<Line> lines, List<History> history,
                              List<Payment> payments, List<String> nextStatuses) {

    public OrderDetailView withParts(List<Line> orderLines, List<History> orderHistory, List<Payment> orderPayments,
                                     List<String> next) {
        return new OrderDetailView(id, orderCode, status, createdAt, updatedAt, customer, subtotal, discountAmount,
                shippingCost, totalAmount, shipping, customerNote, orderLines, orderHistory, orderPayments, next);
    }

    public record Customer(String name, String email) {
    }

    public record Shipping(String methodCode, String methodName, String receiverName, String phone,
                           String department, String province, String district, String street, String reference) {
    }

    public record Line(Long id, Long productId, String productName, String techniqueCode, String techniqueName,
                       Long designId, String designImageUrl, int quantityTotal, int tierMinQuantity,
                       BigDecimal unitBasePrice, BigDecimal unitCustomizationPrice, BigDecimal discountPercent,
                       BigDecimal lineTotal, List<Zone> zones, List<Item> items) {

        public Line withParts(List<Zone> lineZones, List<Item> lineItems) {
            return new Line(id, productId, productName, techniqueCode, techniqueName, designId, designImageUrl,
                    quantityTotal, tierMinQuantity, unitBasePrice, unitCustomizationPrice, discountPercent,
                    lineTotal, lineZones, lineItems);
        }
    }

    public record Zone(String code, String name, BigDecimal surcharge) {
    }

    public record Item(Long variantId, String sku, String size, String color, int quantity) {
    }

    public record History(String fromStatus, String toStatus, String changedBy, String comment,
                          OffsetDateTime changedAt) {
    }

    public record Payment(String provider, String reference, BigDecimal amount, String currency, String status,
                          OffsetDateTime createdAt, OffsetDateTime confirmedAt) {
    }
}
