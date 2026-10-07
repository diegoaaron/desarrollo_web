// Los códigos (PENDIENTE_PAGO, PAGADO…) viajan tal cual a la API; aquí solo se traducen.
export const ORDER_STATUS_LABELS = {
  PENDIENTE_PAGO: "Pendiente de pago",
  PAGADO: "Pagado",
  EN_PRODUCCION: "En producción",
  LISTO_PARA_ENVIO: "Listo para envío",
  ENVIADO: "Enviado",
  ENTREGADO: "Entregado",
  CANCELADO: "Cancelado",
};

// Camino feliz del pedido, en el orden en que lo recorre (diagrama 1.5 de fases.md).
export const ORDER_STATUS_FLOW = [
  "PENDIENTE_PAGO",
  "PAGADO",
  "EN_PRODUCCION",
  "LISTO_PARA_ENVIO",
  "ENVIADO",
  "ENTREGADO",
];

export const ORDER_STATUS_STYLES = {
  PENDIENTE_PAGO: "bg-amber-50 text-amber-700 ring-amber-600/15",
  PAGADO: "bg-sky-50 text-sky-700 ring-sky-600/15",
  EN_PRODUCCION: "bg-violet-50 text-violet-700 ring-violet-600/15",
  LISTO_PARA_ENVIO: "bg-indigo-50 text-indigo-700 ring-indigo-600/15",
  ENVIADO: "bg-blue-50 text-blue-700 ring-blue-600/15",
  ENTREGADO: "bg-emerald-50 text-emerald-700 ring-emerald-600/15",
  CANCELADO: "bg-red-50 text-red-700 ring-red-600/15",
};

export function statusLabel(status) {
  return ORDER_STATUS_LABELS[status] ?? status ?? "—";
}

export function formatDateTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString("es-PE", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleDateString("es-PE", { day: "numeric", month: "short", year: "numeric" });
}
