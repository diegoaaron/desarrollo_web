package com.coralshop.stats.service;

import com.coralshop.stats.dto.OverviewResponse;
import com.coralshop.stats.repository.StatsRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class StatsService {

    private static final int RECENT_ORDERS = 5;

    private final StatsRepository statsRepository;

    public StatsService(StatsRepository statsRepository) {
        this.statsRepository = statsRepository;
    }

    @Transactional(readOnly = true)
    public OverviewResponse overview() {
        return new OverviewResponse(statsRepository.countUsers(), statsRepository.countProducts(),
                statsRepository.countOrders(), statsRepository.deliveredRevenue(),
                statsRepository.recentOrders(RECENT_ORDERS));
    }
}
