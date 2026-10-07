import { Loader2 } from "lucide-react";
import { formatPrice } from "../../../shared/utils/format-price";

// Totales de una cotización; con shippingCost (checkout) se suma el envío elegido.
export function CartTotals({ quote, quoting, shippingCost }) {
  if (!quote) {
    return (
      <p className="flex items-center gap-2 text-sm text-slate-500" role="status">
        <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> Calculando precios…
      </p>
    );
  }
  const discount = Number(quote.discountAmount ?? 0);
  const total = Number(quote.total ?? 0) + Number(shippingCost ?? 0);
  return (
    <dl className={`space-y-3 text-sm transition-opacity ${quoting ? "opacity-60" : ""}`}>
      <div className="flex justify-between gap-4 text-slate-500">
        <dt>Subtotal</dt>
        <dd className="font-semibold tabular-nums text-slate-800">{formatPrice(quote.subtotal)}</dd>
      </div>
      {discount > 0 ? (
        <div className="flex justify-between gap-4 text-slate-500">
          <dt>Descuento por mayoreo</dt>
          <dd className="font-semibold tabular-nums text-emerald-700">− {formatPrice(discount)}</dd>
        </div>
      ) : null}
      <div className="flex justify-between gap-4 text-slate-500">
        <dt>Envío</dt>
        <dd className="font-semibold tabular-nums text-slate-800">
          {shippingCost == null ? <span className="text-xs font-medium text-slate-500">Se elige en el checkout</span> : formatPrice(shippingCost)}
        </dd>
      </div>
      <div className="flex items-end justify-between gap-4 border-t border-stone-200 pt-4">
        <dt className="text-base font-extrabold text-slate-950">Total</dt>
        <dd className="text-2xl font-black tracking-tight tabular-nums text-slate-950">{formatPrice(total)}</dd>
      </div>
    </dl>
  );
}
