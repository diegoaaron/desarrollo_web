package com.coralshop.address.service;

import com.coralshop.address.dto.AddressRequest;
import com.coralshop.address.dto.AddressView;
import com.coralshop.address.repository.AddressRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.NotFoundException;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Direcciones del cliente. Siempre hay como máximo una predeterminada; la primera que se
 * registra lo es automáticamente.
 */
@Service
public class AddressService {

    /** Límite razonable para que la libreta no crezca sin control. */
    private static final int MAX_ADDRESSES = 20;

    private final AddressRepository addressRepository;

    public AddressService(AddressRepository addressRepository) {
        this.addressRepository = addressRepository;
    }

    @Transactional(readOnly = true)
    public List<AddressView> list(long userId) {
        return addressRepository.findByUser(userId);
    }

    @Transactional(readOnly = true)
    public AddressView get(long userId, long addressId) {
        return addressRepository.findByIdAndUser(addressId, userId)
                .orElseThrow(() -> new NotFoundException("Dirección no encontrada"));
    }

    @Transactional
    public AddressView create(long userId, AddressRequest request) {
        int existing = addressRepository.countByUser(userId);
        if (existing >= MAX_ADDRESSES) {
            throw new BusinessRuleException("Puedes guardar hasta " + MAX_ADDRESSES + " direcciones");
        }
        boolean makeDefault = request.isDefault() || existing == 0;
        if (makeDefault) {
            addressRepository.clearDefault(userId);
        }
        long id = addressRepository.insert(userId, normalize(null, request, makeDefault));
        return get(userId, id);
    }

    @Transactional
    public AddressView update(long userId, long addressId, AddressRequest request) {
        AddressView current = get(userId, addressId);
        // Una dirección predeterminada sigue siéndolo hasta que se elija otra.
        boolean makeDefault = request.isDefault() || current.isDefault();
        if (makeDefault) {
            addressRepository.clearDefault(userId);
        }
        addressRepository.update(addressId, userId, normalize(addressId, request, makeDefault));
        return get(userId, addressId);
    }

    @Transactional
    public void delete(long userId, long addressId) {
        AddressView current = get(userId, addressId);
        addressRepository.delete(addressId, userId);
        if (current.isDefault()) {
            addressRepository.makeNewestDefault(userId);
        }
    }

    private static AddressView normalize(Long id, AddressRequest request, boolean isDefault) {
        String reference = request.reference() == null || request.reference().isBlank()
                ? null : request.reference().trim();
        return new AddressView(id, request.receiverName().trim(), request.phone().trim(),
                request.department().trim(), request.province().trim(), request.district().trim(),
                request.street().trim(), reference, isDefault);
    }
}
