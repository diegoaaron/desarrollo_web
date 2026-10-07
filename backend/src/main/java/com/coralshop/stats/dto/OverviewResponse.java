package com.coralshop.stats.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;

public record OverviewResponse(long totalUsers, long totalProducts, long totalOrders,
                               BigDecimal totalRevenue, List<RecentOrder> recentOrders) {

    public record RecentOrder(long id, String customerName, BigDecimal totalAmount,
                              String status, OffsetDateTime createdAt) {
    }
}
