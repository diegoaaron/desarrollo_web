package com.coralshop.order.service;

import static com.coralshop.order.model.OrderStatus.CANCELADO;
import static com.coralshop.order.model.OrderStatus.EN_PRODUCCION;
import static com.coralshop.order.model.OrderStatus.ENTREGADO;
import static com.coralshop.order.model.OrderStatus.ENVIADO;
import static com.coralshop.order.model.OrderStatus.LISTO_PARA_ENVIO;
import static com.coralshop.order.model.OrderStatus.PAGADO;
import static com.coralshop.order.model.OrderStatus.PENDIENTE_PAGO;

import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.order.model.OrderStatus;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.stereotype.Component;

/**
 * Máquina de estados del pedido (fases.md §1.5):
 * <pre>
 * PENDIENTE_PAGO ─pago aprobado─► PAGADO ─► EN_PRODUCCION ─► LISTO_PARA_ENVIO ─► ENVIADO ─► ENTREGADO
 *       └───────────► CANCELADO ◄───────┘
 * </pre>
 * PAGADO solo se alcanza con un pago aprobado, nunca a mano desde el panel.
 */
@Component
public class OrderStatusPolicy {

    private static final Map<OrderStatus, Set<OrderStatus>> TRANSITIONS = new EnumMap<>(OrderStatus.class);

    static {
        TRANSITIONS.put(PENDIENTE_PAGO, EnumSet.of(PAGADO, CANCELADO));
        TRANSITIONS.put(PAGADO, EnumSet.of(EN_PRODUCCION, CANCELADO));
        TRANSITIONS.put(EN_PRODUCCION, EnumSet.of(LISTO_PARA_ENVIO));
        TRANSITIONS.put(LISTO_PARA_ENVIO, EnumSet.of(ENVIADO));
        TRANSITIONS.put(ENVIADO, EnumSet.of(ENTREGADO));
        TRANSITIONS.put(ENTREGADO, EnumSet.noneOf(OrderStatus.class));
        TRANSITIONS.put(CANCELADO, EnumSet.noneOf(OrderStatus.class));
    }

    public boolean canTransition(OrderStatus from, OrderStatus to) {
        return TRANSITIONS.get(from).contains(to);
    }

    /** Valida un cambio pedido por el sistema (por ejemplo, el pago aprobado). */
    public void requireTransition(OrderStatus from, OrderStatus to) {
        if (from == to) {
            throw new BusinessRuleException("El pedido ya está en estado " + to.label());
        }
        if (!canTransition(from, to)) {
            throw new BusinessRuleException("No se puede pasar un pedido de " + from.label() + " a " + to.label());
        }
    }

    /** Valida un cambio hecho por un administrador desde el panel. */
    public void requireAdminTransition(OrderStatus from, OrderStatus to) {
        if (to == PAGADO) {
            throw new BusinessRuleException("Un pedido pasa a Pagado solo cuando se aprueba su pago");
        }
        requireTransition(from, to);
    }

    /** Estados a los que el administrador puede llevar el pedido desde el actual. */
    public List<OrderStatus> adminNextStatuses(OrderStatus from) {
        return TRANSITIONS.get(from).stream().filter(status -> status != PAGADO).toList();
    }

    /** Cancelar devuelve las unidades al inventario. */
    public boolean restocks(OrderStatus to) {
        return to == CANCELADO;
    }
}
