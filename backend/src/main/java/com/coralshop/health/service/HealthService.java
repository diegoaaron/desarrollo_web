package com.coralshop.health.service;

import com.coralshop.health.repository.HealthRepository;
import org.springframework.stereotype.Service;

@Service
public class HealthService {

    private final HealthRepository healthRepository;

    public HealthService(HealthRepository healthRepository) {
        this.healthRepository = healthRepository;
    }

    public boolean isUp() {
        return healthRepository.isDatabaseUp();
    }
}
