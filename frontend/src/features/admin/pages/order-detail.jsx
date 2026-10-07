import { ArrowLeft, Loader2, Mail, User } from "lucide-react";
import { useState } from "react";
import { Link, useParams } from "react-router";
import {
  OrderAmounts,
  OrderLines,
  OrderShipping,
  OrderTimeline,
} from "../../orders/components/order-parts";
import { formatDateTime, statusLabel } from "../../orders/model/order-status";
import { formatPrice } from "../../../shared/utils/format-price";
import { ActionAlert, AdminBadge, AdminPageHeader, AdminPanel, ErrorState } from "../components/admin-ui";
import { fieldStyles, primaryButtonStyles, selectStyles } from "../components/admin-styles";
import { useAdminOrder } from "../hooks/use-orders";

export function OrderDetail() {
  const { id } = useParams();
  const { order, loading, error, updating, actionError, changeStatus, clearActionError } = useAdminOrder(id);
  const [nextStatus, setNextStatus] = useState("");
  const [comment, setComment] = useState("");

  if (error) return <ErrorState error={error} />;
  if (loading || !order) {
    return <p className="py-20 text-center text-slate-500" role="status">Cargando pedido...</p>;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!nextStatus) return;
    if (await changeStatus(nextStatus, comment.trim())) {
      setNextStatus("");
      setComment("");
    }
  }

  // PAGADO solo se alcanza con un pago aprobado: el servidor no lo ofrece en nextStatuses.
  const nextStatuses = order.nextStatuses ?? [];

  return (
    <div>
      <Link to="/admin/orders" className="mb-5 inline-flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-[#e94727]">
        <ArrowLeft className="h-4 w-4" aria-hidden="true" /> Bandeja de pedidos
      </Link>
      <AdminPageHeader
        eyebrow={`Pedido · ${formatDateTime(order.createdAt)}`}
        title={order.orderCode}
        actions={<AdminBadge value={order.status} />}
      />

      <ActionAlert message={actionError} onDismiss={clearActionError} />

      <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,1fr)_24rem]">
        <div className="space-y-6">
          <AdminPanel className="p-5 sm:p-7">
            <h2 className="text-lg font-black text-slate-950">Líneas y diseños</h2>
            <OrderLines lines={order.lines} allowDownload orderCode={order.orderCode} />
            {order.customerNote ? (
              <p className="mt-2 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900">
                <span className="font-bold">Nota del cliente:</span> {order.customerNote}
              </p>
            ) : null}
          </AdminPanel>

          <AdminPanel className="p-5 sm:p-7">
            <h2 className="mb-4 text-lg font-black text-slate-950">Pagos</h2>
            {order.payments?.length ? (
              <ul className="divide-y divide-stone-100 text-sm">
                {order.payments.map((payment) => (
                  <li key={payment.reference} className="flex flex-wrap items-center justify-between gap-3 py-3">
                    <span className="font-mono text-xs text-slate-500">{payment.reference}</span>
                    <span className="text-slate-500">{formatDateTime(payment.createdAt)}</span>
                    <span className="font-bold tabular-nums">{formatPrice(payment.amount)}</span>
                    <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${payment.status === "APROBADO" ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>
                      {payment.status === "APROBADO" ? "Aprobado" : "Rechazado"}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-500">Aún no hay intentos de pago.</p>
            )}
          </AdminPanel>
        </div>

        <div className="space-y-6">
          <AdminPanel className="p-5 sm:p-6">
            <h2 className="mb-4 text-lg font-black text-slate-950">Cambiar estado</h2>
            {nextStatuses.length > 0 ? (
              <form onSubmit={handleSubmit} className="space-y-3">
                <label className="block text-xs font-black uppercase tracking-wider text-slate-400" htmlFor="next-status">
                  Siguiente estado
                </label>
                <select
                  id="next-status"
                  value={nextStatus}
                  onChange={(event) => setNextStatus(event.target.value)}
                  className={`${selectStyles} w-full`}
                >
                  <option value="">Elige un estado</option>
                  {nextStatuses.map((status) => (
                    <option key={status} value={status}>{statusLabel(status)}</option>
                  ))}
                </select>
                <textarea
                  value={comment}
                  onChange={(event) => setComment(event.target.value)}
                  maxLength={500}
                  rows={2}
                  placeholder="Comentario para el historial (opcional)"
                  className={fieldStyles}
                />
                {nextStatus === "CANCELADO" ? (
                  <p className="text-xs font-semibold text-red-600">Cancelar repone el stock de todas las prendas del pedido.</p>
                ) : null}
                <button type="submit" disabled={!nextStatus || updating} className={`${primaryButtonStyles} w-full`}>
                  {updating ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : null}
                  Actualizar estado
                </button>
              </form>
            ) : (
              <p className="text-sm text-slate-500">
                {order.status === "PENDIENTE_PAGO"
                  ? "El pedido pasa a «Pagado» cuando el cliente completa el pago."
                  : "Este pedido ya no admite cambios de estado."}
              </p>
            )}
          </AdminPanel>

          <AdminPanel className="p-5 sm:p-6">
            <h2 className="mb-4 text-lg font-black text-slate-950">Historial</h2>
            <OrderTimeline status={order.status} history={order.history} />
            <ul className="mt-5 space-y-2 border-t border-stone-100 pt-4 text-xs text-slate-500">
              {order.history.map((entry) => (
                <li key={`${entry.toStatus}-${entry.changedAt}`}>
                  <span className="font-semibold text-slate-700">{formatDateTime(entry.changedAt)}</span> ·{" "}
                  {entry.fromStatus ? `${statusLabel(entry.fromStatus)} → ` : ""}{statusLabel(entry.toStatus)}
                  {entry.changedBy ? ` · ${entry.changedBy}` : ""}
                  {entry.comment ? ` · «${entry.comment}»` : ""}
                </li>
              ))}
            </ul>
          </AdminPanel>

          <AdminPanel className="space-y-4 p-5 sm:p-6">
            <h2 className="text-lg font-black text-slate-950">Cliente y entrega</h2>
            <p className="flex items-center gap-2 text-sm font-semibold text-slate-700">
              <User className="h-4 w-4 text-slate-400" aria-hidden="true" /> {order.customer?.name}
            </p>
            <p className="flex items-center gap-2 text-sm text-slate-600">
              <Mail className="h-4 w-4 text-slate-400" aria-hidden="true" /> {order.customer?.email}
            </p>
            <OrderShipping shipping={order.shipping} />
            <div className="border-t border-stone-100 pt-4">
              <OrderAmounts order={order} />
            </div>
          </AdminPanel>
        </div>
      </div>
    </div>
  );
}
