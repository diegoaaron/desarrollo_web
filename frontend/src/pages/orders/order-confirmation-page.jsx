import { ArrowRight, CheckCircle2, Clock } from "lucide-react";
import { Link, useParams } from "react-router";
import { OrderAmounts, OrderLines, OrderShipping, OrderStatusBadge } from "../../features/orders/components/order-parts";
import { useMyOrder } from "../../features/orders/hooks/use-my-orders";
import { ErrorState } from "../../shared/components/error-state";
import { LoadingState } from "../../shared/components/loading-state";

export function OrderConfirmationPage() {
  const { code } = useParams();
  const { order, error, isLoading } = useMyOrder(code);

  if (isLoading) return <LoadingState message="Cargando tu pedido..." />;
  if (error || !order) return <ErrorState message={error ?? "No encontramos el pedido."} />;

  const paid = order.status !== "PENDIENTE_PAGO";

  return (
    <main className="min-h-[70vh] bg-[#faf8f4] px-4 py-12 sm:py-16">
      <div className="mx-auto max-w-3xl">
        <section className="rounded-[2rem] border border-stone-200 bg-white px-6 py-10 text-center shadow-sm sm:px-10">
          <span className={`mx-auto grid h-16 w-16 place-items-center rounded-full ${paid ? "bg-emerald-50 text-emerald-600" : "bg-amber-50 text-amber-600"}`}>
            {paid ? <CheckCircle2 className="h-8 w-8" aria-hidden="true" /> : <Clock className="h-8 w-8" aria-hidden="true" />}
          </span>
          <h1 className="mt-5 text-3xl font-black tracking-tight text-slate-950">
            {paid ? "¡Gracias por tu compra!" : "Tu pedido espera el pago"}
          </h1>
          <p className="mt-2 text-slate-600">
            Código de pedido <span className="font-mono font-bold text-slate-900">{order.orderCode}</span>
          </p>
          <div className="mt-3"><OrderStatusBadge status={order.status} /></div>
          <p className="mx-auto mt-5 max-w-md text-sm leading-6 text-slate-500">
            {paid
              ? "Recibimos tu pago. Nuestro taller revisará tu diseño y lo pasará a producción; puedes seguir cada paso desde «Mis pedidos»."
              : "Completa el pago desde el detalle del pedido para que entre a producción."}
          </p>
          <div className="mt-7 flex flex-wrap justify-center gap-3">
            <Link
              to={`/account/orders/${order.orderCode}`}
              className="inline-flex items-center gap-2 rounded-xl bg-[#ff5331] px-5 py-3 text-sm font-bold text-white hover:bg-[#e94727]"
            >
              {paid ? "Seguir mi pedido" : "Ir a pagar"} <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <Link to="/products" className="rounded-xl border border-stone-200 px-5 py-3 text-sm font-bold text-slate-700 hover:bg-stone-50">
              Seguir comprando
            </Link>
          </div>
        </section>

        <section className="mt-6 rounded-[1.5rem] border border-stone-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-extrabold text-slate-950">Resumen</h2>
          <OrderLines lines={order.lines} />
          <div className="mt-4 grid gap-6 border-t border-stone-100 pt-5 sm:grid-cols-2">
            <OrderShipping shipping={order.shipping} />
            <OrderAmounts order={order} />
          </div>
        </section>
      </div>
    </main>
  );
}
