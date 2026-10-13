import { useCallback, useEffect } from "react";
import { useRequest } from "../../../shared/hooks/use-request";
import {
  getMyNotifications,
  markAllNotificationsRead,
  markNotificationRead,
} from "../api/notifications-api";

// Las notificaciones nacen en el servidor (evento OrderStatusChanged), así que la campana
// consulta cada cierto tiempo y al volver a la pestaña.
const POLL_INTERVAL_MS = 30_000;

export function useNotifications() {
  const { data, setData, error, isLoading, reload } = useRequest(getMyNotifications);

  useEffect(() => {
    const timer = window.setInterval(() => {
      if (document.visibilityState === "visible") reload();
    }, POLL_INTERVAL_MS);
    const handleVisibility = () => {
      if (document.visibilityState === "visible") reload();
    };
    document.addEventListener("visibilitychange", handleVisibility);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", handleVisibility);
    };
  }, [reload]);

  // Se marca en pantalla de inmediato y luego se confirma con el servidor.
  const markRead = useCallback(
    async (id) => {
      setData((current) => {
        if (!current) return current;
        const target = current.items.find((item) => item.id === id);
        if (!target || target.isRead) return current;
        return {
          items: current.items.map((item) => (item.id === id ? { ...item, isRead: true } : item)),
          unreadCount: Math.max(0, current.unreadCount - 1),
        };
      });
      try {
        await markNotificationRead(id);
      } catch {
        reload();
      }
    },
    [setData, reload],
  );

  const markAllRead = useCallback(async () => {
    setData((current) =>
      current
        ? { items: current.items.map((item) => ({ ...item, isRead: true })), unreadCount: 0 }
        : current,
    );
    try {
      await markAllNotificationsRead();
    } catch {
      reload();
    }
  }, [setData, reload]);

  return {
    notifications: data?.items ?? [],
    unreadCount: data?.unreadCount ?? 0,
    error: error?.message ?? null,
    isLoading: isLoading && !data,
    markRead,
    markAllRead,
    reload,
  };
}
