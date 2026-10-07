import { CheckCircle2, Circle, Download, XCircle } from "lucide-react";
import { formatPrice } from "../../../shared/utils/format-price";
import {
  ORDER_STATUS_FLOW,
  ORDER_STATUS_STYLES,
  formatDateTime,
  statusLabel,
} from "../model/order-status";

export function OrderStatusBadge({ status }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-1 text-[0.7rem] font-black uppercase tracking-wider ring-1 ring-inset ${ORDER_STATUS_STYLES[status] ?? "bg-stone-100 text-stone-600 ring-stone-600/10"}`}>
      {statusLabel(status)}
    </span>
  );
}

// Línea de tiempo: el camino feliz con los pasos cumplidos (y su fecha según el historial).
export function OrderTimeline({ status, history = [] }) {
  const reachedAt = {};
  history.forEach((entry) => {
    reachedAt[entry.toStatus] = entry.changedAt;
  });

  if (status === "CANCELADO") {
    const cancelled = history.find((entry) => entry.toStatus === "CANCELADO");
    return (
      <div className="flex items-start gap-3 rounded-2xl bg-red-50 p-4 text-sm text-red-800">
        <XCircle className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
        <div>
          <p className="font-bold">Pedido cancelado</p>
          <p>{formatDateTime(cancelled?.changedAt)}{cancelled?.comment ? ` · ${cancelled.comment}` : ""}</p>
        </div>
      </div>
    );
  }

  const currentIndex = ORDER_STATUS_FLOW.indexOf(status);
  return (
    <ol className="relative space-y-4">
      {ORDER_STATUS_FLOW.map((step, index) => {
        const done = index <= currentIndex;
        const current = index === currentIndex;
        const entry = [...history].reverse().find((item) => item.toStatus === step);
        return (
          <li key={step} className="relative flex gap-3">
            {index < ORDER_STATUS_FLOW.length - 1 ? (
              <span className={`absolute left-[0.6875rem] top-6 h-[calc(100%-0.5rem)] w-0.5 ${index < currentIndex ? "bg-emerald-500" : "bg-stone-200"}`} aria-hidden="true" />
            ) : null}
            {done ? (
              <CheckCircle2 className={`relative h-6 w-6 shrink-0 ${current ? "text-[#ff5331]" : "text-emerald-500"}`} aria-hidden="true" />
            ) : (
              <Circle className="relative h-6 w-6 shrink-0 text-stone-300" aria-hidden="true" />
            )}
            <div className="pb-1">
              <p className={`text-sm font-bold ${done ? "text-slate-900" : "text-slate-400"}`}>
                {statusLabel(step)}
                {current ? <span className="ml-2 text-xs font-semibold text-[#e94727]">estado actual</span> : null}
              </p>
              {reachedAt[step] ? (
                <p className="text-xs text-slate-500">
                  {formatDateTime(reachedAt[step])}
                  {entry?.comment ? ` · ${entry.comment}` : ""}
                </p>
              ) : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

// Líneas del pedido: diseño, técnica, zonas, reparto por tallas y precios congelados al comprar.
export function OrderLines({ lines, allowDownload = false, orderCode }) {
  return (
    <ul className="divide-y divide-stone-100">
      {lines.map((line) => (
        <li key={line.id} className="grid gap-4 py-5 sm:grid-cols-[6rem_minmax(0,1fr)_auto]">
          <div className="grid h-24 w-24 place-items-center overflow-hidden rounded-xl border border-stone-200 bg-stone-50 p-2">
            {line.designImageUrl ? (
              <img src={line.designImageUrl} alt={`Diseño de ${line.productName}`} className="h-full w-full object-contain" />
            ) : (
              <span className="text-center text-xs text-slate-400">Sin diseño</span>
            )}
          </div>
          <div className="min-w-0 text-sm">
            <p className="font-bold text-slate-900">{line.productName}</p>
            <p className="text-slate-600">
              {line.techniqueName ?? "Sin personalizar"}
              {line.zones?.length ? ` · ${line.zones.map((zone) => zone.name).join(", ")}` : ""}
            </p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {line.items.map((item) => (
                <span key={item.variantId} className="rounded-lg bg-stone-100 px-2 py-0.5 text-xs font-semibold text-slate-700">
                  {item.size} · {item.color} × {item.quantity}
                </span>
              ))}
            </div>
            {allowDownload && line.designImageUrl ? (
              <a
                href={line.designImageUrl}
                download={`${orderCode}-linea-${line.id}`}
                className="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-[#e94727] hover:underline"
              >
                <Download className="h-3.5 w-3.5" aria-hidden="true" /> Descargar diseño
              </a>
            ) : null}
          </div>
          <div className="text-sm sm:text-right">
            <p className="text-lg font-black tabular-nums text-slate-950">{formatPrice(line.lineTotal)}</p>
            <p className="text-xs text-slate-500">
              {line.quantityTotal} u. × {formatPrice(Number(line.unitBasePrice) + Number(line.unitCustomizationPrice))}
            </p>
            {Number(line.discountPercent) > 0 ? (
              <p className="text-xs font-semibold text-emerald-700">−{Number(line.discountPercent)} % por mayoreo</p>
            ) : null}
          </div>
        </li>
      ))}
    </ul>
  );
}

export function OrderAmounts({ order }) {
  return (
    <dl className="space-y-2 text-sm">
      <Row label="Subtotal" value={formatPrice(order.subtotal)} />
      {Number(order.discountAmount) > 0 ? <Row label="Descuento por mayoreo" value={`− ${formatPrice(order.discountAmount)}`} accent /> : null}
      <Row label={`Envío (${order.shipping?.methodName ?? "—"})`} value={formatPrice(order.shippingCost)} />
      <div className="flex justify-between border-t border-stone-200 pt-3">
        <dt className="font-extrabold text-slate-950">Total</dt>
        <dd className="text-xl font-black tabular-nums text-slate-950">{formatPrice(order.totalAmount)}</dd>
      </div>
    </dl>
  );
}

export function OrderShipping({ shipping }) {
  if (!shipping) return null;
  return (
    <div className="text-sm text-slate-600">
      <p className="font-bold text-slate-900">{shipping.methodName}</p>
      <p>{shipping.receiverName}{shipping.phone ? ` · ${shipping.phone}` : ""}</p>
      {shipping.street ? (
        <>
          <p>{shipping.street}</p>
          <p className="text-slate-500">
            {[shipping.district, shipping.province, shipping.department].filter(Boolean).join(", ")}
            {shipping.reference ? ` · ${shipping.reference}` : ""}
          </p>
        </>
      ) : null}
    </div>
  );
}

function Row({ label, value, accent }) {
  return (
    <div className="flex justify-between gap-4 text-slate-600">
      <dt>{label}</dt>
      <dd className={`font-semibold tabular-nums ${accent ? "text-emerald-700" : "text-slate-800"}`}>{value}</dd>
    </div>
  );
}
