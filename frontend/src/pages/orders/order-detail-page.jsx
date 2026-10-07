import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router";
import { PaymentForm } from "../../features/checkout/components/payment-form";
import {
  OrderAmounts,
  OrderLines,
  OrderShipping,
  OrderStatusBadge,
  OrderTimeline,
} from "../../features/orders/components/order-parts";
import { useMyOrder } from "../../features/orders/hooks/use-my-orders";
import { formatDateTime } from "../../features/orders/model/order-status";
import { ErrorState } from "../../shared/components/error-state";
import { LoadingState } from "../../shared/components/loading-state";

export function OrderDetailPage() {
  const { code } = useParams();
  const { order, error, notFound, isLoading, reload } = useMyOrder(code);

  if (isLoading && !order) return <LoadingState message="Cargando tu pedido..." />;
  if (error || !order) return <ErrorState message={notFound ? "No encontramos ese pedido en tu cuenta." : error} />;

  return (
    <main className="min-h-[70vh] bg-[#faf8f4] px-4 py-12 sm:py-16">
      <div className="mx-auto max-w-5xl">
        <Link to="/account/orders" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-[#e94727]">
          <ArrowLeft className="h-4 w-4" aria-hidden="true" /> Mis pedidos
        </Link>

        <header className="mt-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#e94727]">Pedido</p>
            <h1 className="mt-1 font-mono text-3xl font-bold text-slate-950">{order.orderCode}</h1>
            <p className="mt-1 text-sm text-slate-500">Creado el {formatDateTime(order.createdAt)}</p>
          </div>
          <OrderStatusBadge status={order.status} />
        </header>

        <div className="mt-8 grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
          <div className="space-y-6">
            {order.status === "PENDIENTE_PAGO" ? (
              <section className="rounded-[1.5rem] border border-amber-200 bg-white p-6 shadow-sm">
                <h2 className="mb-1 text-lg font-extrabold text-slate-950">Completa el pago</h2>
                <p className="mb-5 text-sm text-slate-500">Tu stock está reservado. Cuando el pago se apruebe, el pedido pasa a producción.</p>
                <PaymentForm orderCode={order.orderCode} amount={order.totalAmount} onApproved={reload} />
              </section>
            ) : null}

            <section className="rounded-[1.5rem] border border-stone-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-extrabold text-slate-950">Prendas y diseños</h2>
              <OrderLines lines={order.lines} />
              {order.customerNote ? (
                <p className="mt-2 rounded-xl bg-stone-50 px-4 py-3 text-sm text-slate-600">
                  <span className="font-bold">Tu nota:</span> {order.customerNote}
                </p>
              ) : null}
            </section>
          </div>

          <aside className="space-y-6">
            <section className="rounded-[1.5rem] border border-stone-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-extrabold text-slate-950">Seguimiento</h2>
              <OrderTimeline status={order.status} history={order.history} />
            </section>
            <section className="rounded-[1.5rem] border border-stone-200 bg-white p-6 shadow-sm">
              <h2 className="mb-3 text-lg font-extrabold text-slate-950">Entrega</h2>
              <OrderShipping shipping={order.shipping} />
            </section>
            <section className="rounded-[1.5rem] border border-stone-200 bg-white p-6 shadow-sm">
              <h2 className="mb-3 text-lg font-extrabold text-slate-950">Importes</h2>
              <OrderAmounts order={order} />
            </section>
          </aside>
        </div>
      </div>
    </main>
  );
}
