package com.coralshop.order.event;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.reset;
import static org.mockito.Mockito.verify;

import com.coralshop.audit.listener.AuditListener;
import com.coralshop.audit.repository.AuditRepository;
import com.coralshop.notification.listener.NotificationListener;
import com.coralshop.notification.repository.NotificationRepository;
import com.coralshop.notification.service.NotificationService;
import com.coralshop.order.model.OrderStatus;
import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.transaction.support.AbstractPlatformTransactionManager;
import org.springframework.transaction.support.DefaultTransactionStatus;
import org.springframework.transaction.support.TransactionTemplate;

/**
 * Criterio de la fase 4: la auditoría viaja dentro de la transacción del cambio y la
 * notificación solo sale si esa transacción se confirma. Usa los suscriptores reales sobre un
 * gestor de transacciones sin base de datos.
 */
@SpringJUnitConfig(OrderStatusChangedDeliveryTest.Config.class)
class OrderStatusChangedDeliveryTest {

    @Configuration
    @EnableTransactionManagement
    @Import({AuditListener.class, NotificationListener.class, NotificationService.class})
    static class Config {

        @Bean
        PlatformTransactionManager transactionManager() {
            return new InMemoryTransactionManager();
        }

        @Bean
        AuditRepository auditRepository() {
            return mock(AuditRepository.class);
        }

        @Bean
        NotificationRepository notificationRepository() {
            return mock(NotificationRepository.class);
        }
    }

    /** Gestor que solo administra el ciclo de vida (y las sincronizaciones) de la transacción. */
    static class InMemoryTransactionManager extends AbstractPlatformTransactionManager {
        @Override
        protected Object doGetTransaction() {
            return new Object();
        }

        @Override
        protected void doBegin(Object transaction, TransactionDefinition definition) {
        }

        @Override
        protected void doCommit(DefaultTransactionStatus status) {
        }

        @Override
        protected void doRollback(DefaultTransactionStatus status) {
        }
    }

    @Autowired
    private ApplicationEventPublisher publisher;
    @Autowired
    private PlatformTransactionManager transactionManager;
    @Autowired
    private AuditRepository auditRepository;
    @Autowired
    private NotificationRepository notificationRepository;

    private TransactionTemplate transaction;

    @BeforeEach
    void setUp() {
        reset(auditRepository, notificationRepository);
        transaction = new TransactionTemplate(transactionManager);
    }

    @Test
    void confirmedChangeIsAuditedAndNotified() {
        OrderStatusChanged event = event();

        transaction.executeWithoutResult(status -> publisher.publishEvent(event));

        verify(auditRepository).insert(eq(event.eventId()), eq("OrderStatusChanged"), eq("ORDER"), eq(5L), eq(1L),
                eq("PAGADO"), eq("EN_PRODUCCION"), anyString(), eq(event.occurredAt()));
        verify(notificationRepository).insert(eq(event.eventId()), eq(9L), eq(5L),
                eq("Pedido CS-TEST0001: En producción"), anyString(), eq("/account/orders/CS-TEST0001"));
    }

    @Test
    void rolledBackChangePublishesNothing() {
        assertThatThrownBy(() -> transaction.executeWithoutResult(status -> {
            publisher.publishEvent(event());
            throw new IllegalStateException("falla después de publicar");
        })).isInstanceOf(IllegalStateException.class);

        verifyNothingRecorded();
    }

    @Test
    void failedAuditCancelsTheChangeAndTheNotification() {
        doThrow(new IllegalStateException("audit_log no disponible")).when(auditRepository).insert(any(), any(),
                any(), anyLong(), any(), any(), any(), any(), any());

        assertThatThrownBy(() -> transaction.executeWithoutResult(status -> publisher.publishEvent(event())))
                .isInstanceOf(IllegalStateException.class);

        verify(notificationRepository, never()).insert(any(), anyLong(), any(), any(), any(), any());
    }

    @Test
    void eventOutsideATransactionIsIgnored() {
        publisher.publishEvent(event());

        verifyNothingRecorded();
    }

    private void verifyNothingRecorded() {
        verify(auditRepository, never()).insert(any(), any(), any(), anyLong(), any(), any(), any(), any(), any());
        verify(notificationRepository, never()).insert(any(), anyLong(), any(), any(), any(), any());
    }

    private static OrderStatusChanged event() {
        return new OrderStatusChanged(UUID.randomUUID(), 5L, "CS-TEST0001", 9L, OrderStatus.PAGADO,
                OrderStatus.EN_PRODUCCION, 1L, null, Instant.now());
    }
}
