package com.coralshop.shipping.service;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.shipping.dto.ShippingMethodView;
import com.coralshop.shipping.repository.ShippingMethodRepository;
import java.util.List;
import java.util.Locale;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class ShippingService {

    private final ShippingMethodRepository shippingMethodRepository;

    public ShippingService(ShippingMethodRepository shippingMethodRepository) {
        this.shippingMethodRepository = shippingMethodRepository;
    }

    public List<ShippingMethodView> activeMethods() {
        return shippingMethodRepository.findActive();
    }

    public ShippingMethodView requireActive(String code) {
        return shippingMethodRepository.findActiveByCode(code.trim().toUpperCase(Locale.ROOT))
                .orElseThrow(() -> new BusinessRuleException("El método de envío " + code + " no está disponible"));
    }
}
