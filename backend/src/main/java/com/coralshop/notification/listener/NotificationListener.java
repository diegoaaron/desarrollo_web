package com.coralshop.notification.listener;

import com.coralshop.notification.service.NotificationService;
import com.coralshop.order.event.OrderStatusChanged;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;

/**
 * Suscriptor de notificaciones. Corre en AFTER_COMMIT: solo avisa al cliente de cambios que
 * realmente quedaron guardados, y si la transacción se deshace el evento nunca llega aquí.
 * Un fallo al notificar se registra en el log sin afectar al cambio, que ya está confirmado.
 */
@Component
public class NotificationListener {

    private static final Logger log = LoggerFactory.getLogger(NotificationListener.class);

    private final NotificationService notificationService;

    public NotificationListener(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(OrderStatusChanged event) {
        try {
            notificationService.notifyStatusChange(event);
        } catch (RuntimeException exception) {
            log.error("No se pudo notificar el evento {} del pedido {}", event.eventId(), event.orderCode(), exception);
        }
    }
}
