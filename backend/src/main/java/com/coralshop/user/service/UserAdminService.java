package com.coralshop.user.service;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.NotFoundException;
import com.coralshop.user.dto.UserAdminView;
import com.coralshop.user.repository.UserAdminRepository;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserAdminService {

    private final UserAdminRepository userAdminRepository;

    public UserAdminService(UserAdminRepository userAdminRepository) {
        this.userAdminRepository = userAdminRepository;
    }

    @Transactional(readOnly = true)
    public List<UserAdminView> users() {
        return userAdminRepository.findAll();
    }

    /**
     * Un administrador no puede cambiar su propio rol: evita que la tienda se quede sin
     * nadie que la administre por un clic accidental.
     */
    @Transactional
    public UserAdminView changeRole(long adminId, long userId, long roleId) {
        UserAdminView user = userAdminRepository.findById(userId)
                .orElseThrow(() -> new NotFoundException("Usuario no encontrado"));
        if (user.id() == adminId) {
            throw new BusinessRuleException("No puedes cambiar tu propio rol");
        }
        if (!userAdminRepository.roleExists(roleId)) {
            throw new BusinessRuleException("El rol " + roleId + " no existe");
        }
        userAdminRepository.updateRole(userId, roleId);
        return userAdminRepository.findById(userId).orElseThrow();
    }
}
