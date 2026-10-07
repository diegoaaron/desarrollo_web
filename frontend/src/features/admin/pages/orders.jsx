import { SlidersHorizontal } from "lucide-react";
import { useState } from "react";
import {
  ActionAlert,
  AdminBadge,
  AdminPageHeader,
  AdminPanel,
  EmptyState,
  ErrorState,
} from "../components/admin-ui";
import {
  ORDER_STATUS_LABELS,
  formatAdminDate,
  selectStyles,
} from "../components/admin-styles";
import { formatPrice } from "../../../shared/utils/format-price";
import { useOrders } from "../hooks/use-orders";

const STATUSES = ["ALL", "PENDING", "SHIPPED", "DELIVERED", "CANCELLED"];
const SKELETONS = Array.from({ length: 5 }, (_, index) => index);

export function Orders() {
  const {
    orders,
    loading,
    error,
    actionError,
    updatingId,
    updateStatus,
    clearActionError,
  } = useOrders();
  const [filter, setFilter] = useState("ALL");
  const filteredOrders = filter === "ALL" ? orders : orders.filter((order) => order.status === filter);

  if (error) return <ErrorState error={error} />;

  return (
    <div>
      <AdminPageHeader
        eyebrow="Despacho"
        title="Pedidos"
        description="Sigue cada pedido desde el pago hasta la entrega y mantén informados a los clientes."
      />

      <ActionAlert message={actionError} onDismiss={clearActionError} />

      <AdminPanel>
        <div className="border-b border-stone-200/80 px-5 py-5 sm:px-7">
          <div className="mb-4 flex items-center gap-2">
            <SlidersHorizontal className="h-4 w-4 text-[#e94727]" aria-hidden="true" />
            <p className="text-xs font-black uppercase tracking-[0.16em] text-slate-500">Filtrar pedidos</p>
          </div>
          <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1" aria-label="Filtro por estado del pedido">
            {STATUSES.map((status) => (
              <button
                key={status}
                type="button"
                onClick={() => setFilter(status)}
                className={`min-h-10 shrink-0 rounded-xl px-4 py-2 text-xs font-black uppercase tracking-wider transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${
                  filter === status
                    ? "bg-slate-950 text-white shadow-lg shadow-slate-950/10"
                    : "border border-stone-200 bg-white text-slate-500 hover:bg-stone-50 hover:text-slate-900"
                }`}
                aria-pressed={filter === status}
              >
                {status === "ALL" ? `Todos (${orders.length})` : ORDER_STATUS_LABELS[status]}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <OrderSkeletons />
        ) : filteredOrders.length > 0 ? (
          <>
            <div className="divide-y divide-stone-100 lg:hidden">
              {filteredOrders.map((order) => (
                <article key={order.id} className="p-5 sm:p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="font-black text-slate-950">Pedido #{order.id}</p>
                      <p className="mt-1 text-sm font-semibold text-slate-500">{order.username}</p>
                    </div>
                    <AdminBadge value={order.status} />
                  </div>
                  <div className="mt-5 grid grid-cols-2 gap-4 rounded-2xl bg-stone-50 p-4">
                    <div>
                      <p className="text-[0.65rem] font-black uppercase tracking-wider text-slate-400">Total</p>
                      <p className="mt-1 font-black text-slate-900">{formatPrice(order.totalAmount)}</p>
                    </div>
                    <div>
                      <p className="text-[0.65rem] font-black uppercase tracking-wider text-slate-400">Fecha</p>
                      <p className="mt-1 text-sm font-bold text-slate-600">{formatAdminDate(order.createdAt)}</p>
                    </div>
                  </div>
                  <label className="mt-4 block text-xs font-black uppercase tracking-wider text-slate-400" htmlFor={`order-${order.id}-status`}>
                    Actualizar estado
                  </label>
                  <select
                    id={`order-${order.id}-status`}
                    value={order.status}
                    onChange={(event) => updateStatus(order.id, event.target.value)}
                    disabled={updatingId === order.id}
                    className={`${selectStyles} mt-2 w-full disabled:opacity-50`}
                  >
                    <StatusOptions />
                  </select>
                </article>
              ))}
            </div>

            <div className="hidden overflow-x-auto lg:block">
              <table className="w-full min-w-[58rem] text-left">
                <thead className="bg-stone-50/80">
                  <tr className="text-[0.66rem] font-black uppercase tracking-[0.14em] text-slate-400">
                    <th className="px-6 py-4">Pedido</th>
                    <th className="px-6 py-4">Cliente</th>
                    <th className="px-6 py-4">Total</th>
                    <th className="px-6 py-4">Estado</th>
                    <th className="px-6 py-4">Fecha</th>
                    <th className="px-6 py-4 text-right">Actualizar</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {filteredOrders.map((order) => (
                    <tr key={order.id} className="transition-colors hover:bg-[#fffaf7]">
                      <td className="px-6 py-4 text-sm font-black text-slate-900">#{order.id}</td>
                      <td className="px-6 py-4 text-sm font-semibold text-slate-600">{order.username}</td>
                      <td className="px-6 py-4 text-sm font-black text-slate-900">{formatPrice(order.totalAmount)}</td>
                      <td className="px-6 py-4"><AdminBadge value={order.status} /></td>
                      <td className="px-6 py-4 text-sm text-slate-500">{formatAdminDate(order.createdAt)}</td>
                      <td className="px-6 py-4 text-right">
                        <label className="sr-only" htmlFor={`desktop-order-${order.id}-status`}>Actualizar el estado del pedido {order.id}</label>
                        <select
                          id={`desktop-order-${order.id}-status`}
                          value={order.status}
                          onChange={(event) => updateStatus(order.id, event.target.value)}
                          disabled={updatingId === order.id}
                          className={`${selectStyles} disabled:opacity-50`}
                        >
                          <StatusOptions />
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ) : (
          <EmptyState title="No hay pedidos que coincidan" description="Prueba con otro filtro de estado o vuelve cuando lleguen nuevos pedidos." />
        )}
      </AdminPanel>
    </div>
  );
}

function StatusOptions() {
  return (
    <>
      {Object.entries(ORDER_STATUS_LABELS).map(([value, label]) => (
        <option key={value} value={value}>{label}</option>
      ))}
    </>
  );
}

function OrderSkeletons() {
  return (
    <div className="divide-y divide-stone-100 px-5 sm:px-7">
      {SKELETONS.map((item) => (
        <div key={item} className="flex animate-pulse items-center gap-4 py-5">
          <div className="space-y-2">
            <div className="h-3 w-24 rounded bg-stone-100" />
            <div className="h-3 w-16 rounded bg-stone-100" />
          </div>
          <div className="ml-auto h-7 w-20 rounded-full bg-stone-100" />
        </div>
      ))}
    </div>
  );
}
