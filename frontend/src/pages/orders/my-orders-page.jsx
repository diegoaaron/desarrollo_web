import { ArrowLeft, ChevronRight, Package } from "lucide-react";
import { Link } from "react-router";
import { OrderStatusBadge } from "../../features/orders/components/order-parts";
import { useMyOrders } from "../../features/orders/hooks/use-my-orders";
import { formatDate } from "../../features/orders/model/order-status";
import { ErrorState } from "../../shared/components/error-state";
import { LoadingState } from "../../shared/components/loading-state";
import { formatPrice } from "../../shared/utils/format-price";

export function MyOrdersPage() {
  const { orders, error, isLoading } = useMyOrders();

  return (
    <main className="min-h-[70vh] bg-[#faf8f4] px-4 py-12 sm:py-16">
      <div className="mx-auto max-w-4xl">
        <Link to="/account" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-[#e94727]">
          <ArrowLeft className="h-4 w-4" aria-hidden="true" /> Mi cuenta
        </Link>
        <h1 className="mt-6 text-3xl font-semibold text-slate-950 sm:text-4xl">Mis pedidos</h1>
        <p className="mt-2 text-slate-600">Sigue cada pedido desde el pago hasta la entrega.</p>

        <div className="mt-8">
          {isLoading ? <LoadingState message="Cargando tus pedidos..." /> : error ? <ErrorState message={error} /> : orders.length === 0 ? (
            <div className="rounded-2xl border border-stone-200 bg-white px-6 py-14 text-center">
              <Package className="mx-auto h-10 w-10 text-stone-300" aria-hidden="true" />
              <p className="mt-4 font-bold text-slate-900">Aún no tienes pedidos</p>
              <Link to="/products" className="mt-3 inline-block text-sm font-bold text-[#e94727] hover:underline">Personaliza tu primera prenda</Link>
            </div>
          ) : (
            <ul className="overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-sm">
              {orders.map((order) => (
                <li key={order.orderCode} className="border-b border-stone-100 last:border-0">
                  <Link
                    to={`/account/orders/${order.orderCode}`}
                    className="flex flex-wrap items-center gap-x-6 gap-y-2 px-5 py-4 transition hover:bg-[#fffaf7]"
                  >
                    <div className="min-w-36">
                      <p className="font-mono font-bold text-slate-900">{order.orderCode}</p>
                      <p className="text-xs text-slate-500">{formatDate(order.createdAt)}</p>
                    </div>
                    <OrderStatusBadge status={order.status} />
                    <p className="text-sm text-slate-500">{order.units} {order.units === 1 ? "unidad" : "unidades"}</p>
                    <p className="ml-auto font-black tabular-nums text-slate-950">{formatPrice(order.totalAmount)}</p>
                    <ChevronRight className="h-4 w-4 text-slate-400" aria-hidden="true" />
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </main>
  );
}
