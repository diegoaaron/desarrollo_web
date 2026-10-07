package com.coralshop.stats.controller;

import com.coralshop.stats.dto.OverviewResponse;
import com.coralshop.stats.service.StatsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Métricas del tablero de administración (solo ADMIN). */
@RestController
@RequestMapping("/api/stats")
public class StatsController {

    private final StatsService statsService;

    public StatsController(StatsService statsService) {
        this.statsService = statsService;
    }

    @GetMapping("/overview")
    public OverviewResponse overview() {
        return statsService.overview();
    }
}
