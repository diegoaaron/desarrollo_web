import { ChevronLeft, ChevronRight, SlidersHorizontal } from "lucide-react";
import { Link, useSearchParams } from "react-router";
import {
  AdminBadge,
  AdminPageHeader,
  AdminPanel,
  EmptyState,
  ErrorState,
} from "../components/admin-ui";
import { ORDER_STATUS_LABELS, formatAdminDate } from "../components/admin-styles";
import { formatPrice } from "../../../shared/utils/format-price";
import { useOrders } from "../hooks/use-orders";

const STATUSES = ["ALL", ...Object.keys(ORDER_STATUS_LABELS)];
const SKELETONS = Array.from({ length: 5 }, (_, index) => index);

export function Orders() {
  // Filtro y página en la URL: al volver del detalle se conserva la vista.
  const [searchParams, setSearchParams] = useSearchParams();
  const filter = searchParams.get("status") ?? "ALL";
  const page = Math.max(0, Number.parseInt(searchParams.get("page") ?? "0", 10) || 0);
  const { orders, totalItems, totalPages, loading, error } = useOrders({
    status: filter === "ALL" ? undefined : filter,
    page,
  });

  function update(next) {
    const params = new URLSearchParams(searchParams);
    Object.entries(next).forEach(([key, value]) => {
      if (value === null || value === undefined || value === "ALL" || value === 0) params.delete(key);
      else params.set(key, value);
    });
    setSearchParams(params);
  }

  if (error) return <ErrorState error={error} />;

  return (
    <div>
      <AdminPageHeader
        eyebrow="Despacho"
        title="Pedidos"
        description="Sigue cada pedido desde el pago hasta la entrega. Abre uno para ver los diseños y avanzar su estado."
      />

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
                onClick={() => update({ status, page: 0 })}
                className={`min-h-10 shrink-0 rounded-xl px-4 py-2 text-xs font-black uppercase tracking-wider transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${
                  filter === status
                    ? "bg-slate-950 text-white shadow-lg shadow-slate-950/10"
                    : "border border-stone-200 bg-white text-slate-500 hover:bg-stone-50 hover:text-slate-900"
                }`}
                aria-pressed={filter === status}
              >
                {status === "ALL" ? "Todos" : ORDER_STATUS_LABELS[status]}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <OrderSkeletons />
        ) : orders.length > 0 ? (
          <>
            <div className="divide-y divide-stone-100 lg:hidden">
              {orders.map((order) => (
                <Link key={order.id} to={`/admin/orders/${order.id}`} className="block p-5 hover:bg-[#fffaf7] sm:p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="font-mono font-black text-slate-950">{order.orderCode}</p>
                      <p className="mt-1 text-sm font-semibold text-slate-500">{order.customerName}</p>
                    </div>
                    <AdminBadge value={order.status} />
                  </div>
                  <div className="mt-4 grid grid-cols-3 gap-4 rounded-2xl bg-stone-50 p-4 text-sm">
                    <Stat label="Total" value={formatPrice(order.totalAmount)} />
                    <Stat label="Unidades" value={order.units} />
                    <Stat label="Fecha" value={formatAdminDate(order.createdAt)} />
                  </div>
                </Link>
              ))}
            </div>

            <div className="hidden overflow-x-auto lg:block">
              <table className="w-full min-w-[58rem] text-left">
                <thead className="bg-stone-50/80">
                  <tr className="text-[0.66rem] font-black uppercase tracking-[0.14em] text-slate-400">
                    <th className="px-6 py-4">Pedido</th>
                    <th className="px-6 py-4">Cliente</th>
                    <th className="px-6 py-4">Unidades</th>
                    <th className="px-6 py-4">Total</th>
                    <th className="px-6 py-4">Estado</th>
                    <th className="px-6 py-4">Fecha</th>
                    <th className="px-6 py-4 text-right"><span className="sr-only">Abrir</span></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {orders.map((order) => (
                    <tr key={order.id} className="transition-colors hover:bg-[#fffaf7]">
                      <td className="px-6 py-4 font-mono text-sm font-black text-slate-900">{order.orderCode}</td>
                      <td className="px-6 py-4 text-sm">
                        <p className="font-semibold text-slate-700">{order.customerName}</p>
                        <p className="text-xs text-slate-400">{order.customerEmail}</p>
                      </td>
                      <td className="px-6 py-4 text-sm font-semibold text-slate-600">{order.units}</td>
                      <td className="px-6 py-4 text-sm font-black text-slate-900">{formatPrice(order.totalAmount)}</td>
                      <td className="px-6 py-4"><AdminBadge value={order.status} /></td>
                      <td className="px-6 py-4 text-sm text-slate-500">{formatAdminDate(order.createdAt)}</td>
                      <td className="px-6 py-4 text-right">
                        <Link to={`/admin/orders/${order.id}`} className="text-sm font-bold text-[#e94727] hover:underline">
                          Ver detalle
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <nav className="flex items-center justify-between gap-4 border-t border-stone-100 px-5 py-4 text-sm sm:px-7" aria-label="Paginación">
              <p className="text-slate-500">{totalItems} {totalItems === 1 ? "pedido" : "pedidos"} · página {page + 1} de {Math.max(totalPages, 1)}</p>
              <div className="flex gap-2">
                <PageButton disabled={page === 0} onClick={() => update({ page: page - 1 })} label="Página anterior">
                  <ChevronLeft className="h-4 w-4" aria-hidden="true" />
                </PageButton>
                <PageButton disabled={page + 1 >= totalPages} onClick={() => update({ page: page + 1 })} label="Página siguiente">
                  <ChevronRight className="h-4 w-4" aria-hidden="true" />
                </PageButton>
              </div>
            </nav>
          </>
        ) : (
          <EmptyState title="No hay pedidos que coincidan" description="Prueba con otro filtro de estado o vuelve cuando lleguen nuevos pedidos." />
        )}
      </AdminPanel>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <p className="text-[0.65rem] font-black uppercase tracking-wider text-slate-400">{label}</p>
      <p className="mt-1 font-bold text-slate-900">{value}</p>
    </div>
  );
}

function PageButton({ disabled, onClick, label, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      className="grid h-9 w-9 place-items-center rounded-xl border border-stone-200 bg-white text-slate-600 hover:bg-stone-50 disabled:opacity-40"
    >
      {children}
    </button>
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
