package com.coralshop.audit.listener;

import com.coralshop.audit.repository.AuditRepository;
import com.coralshop.order.event.OrderStatusChanged;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;

/**
 * Suscriptor de auditoría. Corre en BEFORE_COMMIT, es decir, dentro de la misma transacción
 * que cambió el pedido: si el cambio se deshace, la auditoría también, y si la auditoría
 * falla, el cambio no se confirma. Así nunca queda un cambio sin rastro.
 */
@Component
public class AuditListener {

    private static final String ENTITY_ORDER = "ORDER";
    private static final int DETAIL_MAX_LENGTH = 500;

    private final AuditRepository auditRepository;

    public AuditListener(AuditRepository auditRepository) {
        this.auditRepository = auditRepository;
    }

    @TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
    public void on(OrderStatusChanged event) {
        auditRepository.insert(event.eventId(), OrderStatusChanged.class.getSimpleName(), ENTITY_ORDER,
                event.orderId(), event.changedBy(), event.fromStatus() == null ? null : event.fromStatus().name(),
                event.toStatus().name(), detail(event), event.occurredAt());
    }

    private static String detail(OrderStatusChanged event) {
        String detail = event.orderCode() + (event.comment() == null ? "" : " · " + event.comment());
        return detail.length() <= DETAIL_MAX_LENGTH ? detail : detail.substring(0, DETAIL_MAX_LENGTH);
    }
}
