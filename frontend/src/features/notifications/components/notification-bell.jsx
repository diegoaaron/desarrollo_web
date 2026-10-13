import { Bell } from "lucide-react";
import { useEffect, useId, useRef, useState } from "react";
import { useNavigate } from "react-router";
import { useNotifications } from "../hooks/use-notifications";

const dateFormat = new Intl.DateTimeFormat("es-PE", { dateStyle: "short", timeStyle: "short" });

export function NotificationBell() {
  const { notifications, unreadCount, error, isLoading, markRead, markAllRead, reload } =
    useNotifications();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);
  const buttonRef = useRef(null);
  const panelId = useId();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isOpen) return undefined;
    const handlePointer = (event) => {
      if (!containerRef.current?.contains(event.target)) setIsOpen(false);
    };
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        setIsOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("mousedown", handlePointer);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handlePointer);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  const toggle = () => {
    if (!isOpen) reload();
    setIsOpen((value) => !value);
  };

  const openNotification = (notification) => {
    markRead(notification.id);
    setIsOpen(false);
    if (notification.link) navigate(notification.link);
  };

  const badge = unreadCount > 99 ? "99+" : unreadCount;

  return (
    // Sin `relative`: el panel se ancla al grupo de iconos del header, que llega al borde derecho.
    <div ref={containerRef}>
      <button
        ref={buttonRef}
        type="button"
        className={`relative grid h-10 w-10 place-items-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${
          isOpen ? "bg-[#fff0eb] text-[#ff5331]" : "text-slate-700 hover:bg-stone-100"
        }`}
        onClick={toggle}
        aria-label={
          unreadCount > 0
            ? `Notificaciones: ${unreadCount} sin leer`
            : "Notificaciones"
        }
        aria-expanded={isOpen}
        aria-controls={panelId}
      >
        <Bell aria-hidden="true" />
        {unreadCount > 0 && (
          <span className="absolute -right-2 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-[#ff5331] px-1 text-xs text-white">
            {badge}
          </span>
        )}
      </button>
      {isOpen && (
        <div
          id={panelId}
          className="absolute right-0 top-12 z-50 w-[min(22rem,calc(100vw-2rem))] overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-xl"
        >
          <div className="flex items-center justify-between border-b border-stone-100 px-4 py-3">
            <h2 className="text-sm font-semibold text-slate-900">Notificaciones</h2>
            {unreadCount > 0 && (
              <button
                type="button"
                className="text-xs font-semibold text-[#ff5331] hover:underline"
                onClick={markAllRead}
              >
                Marcar todo como leído
              </button>
            )}
          </div>
          {isLoading ? (
            <p className="px-4 py-6 text-center text-sm text-slate-500" role="status">
              Cargando…
            </p>
          ) : error && notifications.length === 0 ? (
            <p className="px-4 py-6 text-center text-sm text-red-600" role="alert">
              {error}
            </p>
          ) : notifications.length === 0 ? (
            <p className="px-4 py-6 text-center text-sm text-slate-500">
              Aquí verás los avances de tus pedidos.
            </p>
          ) : (
            <ul className="max-h-96 divide-y divide-stone-100 overflow-y-auto">
              {notifications.map((notification) => (
                <li key={notification.id}>
                  <button
                    type="button"
                    className={`flex w-full gap-3 px-4 py-3 text-left transition-colors hover:bg-stone-50 ${
                      notification.isRead ? "" : "bg-[#fff7f4]"
                    }`}
                    onClick={() => openNotification(notification)}
                  >
                    <span
                      aria-hidden="true"
                      className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${
                        notification.isRead ? "bg-transparent" : "bg-[#ff5331]"
                      }`}
                    />
                    <span className="min-w-0">
                      <span className="block text-sm font-semibold text-slate-900">
                        {notification.title}
                        {!notification.isRead && <span className="sr-only"> (sin leer)</span>}
                      </span>
                      <span className="mt-0.5 block text-sm text-slate-600">
                        {notification.message}
                      </span>
                      <span className="mt-1 block text-xs text-slate-400">
                        {dateFormat.format(new Date(notification.createdAt))}
                      </span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
