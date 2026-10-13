package com.coralshop.notification.service;

import com.coralshop.common.exception.NotFoundException;
import com.coralshop.notification.dto.NotificationsResponse;
import com.coralshop.notification.repository.NotificationRepository;
import com.coralshop.order.event.OrderStatusChanged;
import com.coralshop.order.model.OrderStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/** Avisos al cliente: se redactan a partir de los eventos del pedido y se consultan desde la campana. */
@Service
public class NotificationService {

    private static final int LATEST_LIMIT = 20;
    private static final int MESSAGE_MAX_LENGTH = 500;

    private final NotificationRepository notificationRepository;

    public NotificationService(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    /**
     * Transacción propia: se invoca después del commit del cambio de estado, cuando la
     * transacción original ya terminó.
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void notifyStatusChange(OrderStatusChanged event) {
        String code = event.orderCode();
        String title = event.fromStatus() == null ? "Recibimos tu pedido " + code
                : "Pedido " + code + ": " + event.toStatus().label();
        String message = message(event.toStatus());
        // El comentario del pago trae la referencia de la pasarela; solo se muestran las notas del admin.
        if (event.comment() != null && event.fromStatus() != null && event.toStatus() != OrderStatus.PAGADO) {
            message += " Nota de la tienda: " + event.comment();
        }
        if (message.length() > MESSAGE_MAX_LENGTH) {
            message = message.substring(0, MESSAGE_MAX_LENGTH);
        }
        notificationRepository.insert(event.eventId(), event.customerId(), event.orderId(), title, message,
                "/account/orders/" + code);
    }

    @Transactional(readOnly = true)
    public NotificationsResponse latest(long userId) {
        return new NotificationsResponse(notificationRepository.findLatestByUser(userId, LATEST_LIMIT),
                notificationRepository.countUnread(userId));
    }

    @Transactional
    public void markRead(long userId, long notificationId) {
        if (!notificationRepository.markRead(notificationId, userId)) {
            throw new NotFoundException("Notificación no encontrada");
        }
    }

    @Transactional
    public void markAllRead(long userId) {
        notificationRepository.markAllRead(userId);
    }

    private static String message(OrderStatus status) {
        return switch (status) {
            case PENDIENTE_PAGO -> "Completa el pago para que empecemos a prepararlo.";
            case PAGADO -> "Confirmamos tu pago. Pronto empezaremos a producir tus prendas.";
            case EN_PRODUCCION -> "Estamos estampando tus prendas.";
            case LISTO_PARA_ENVIO -> "Tu pedido está empacado y listo para salir.";
            case ENVIADO -> "Tu pedido va en camino.";
            case ENTREGADO -> "Tu pedido fue entregado. ¡Gracias por comprar en Coral Shop!";
            case CANCELADO -> "Tu pedido fue cancelado.";
        };
    }
}
