import { Loader2 } from "lucide-react";
import { formatPrice } from "../../../shared/utils/format-price";

// Desglose devuelto por POST /api/quotes: base + técnica y zonas − descuento por escala.
export function PriceBreakdown({ line, isLoading, error }) {
  if (error) return <p role="alert" className="text-sm font-semibold text-red-600">{error}</p>;
  if (!line) {
    return <p className="text-sm text-slate-500">Elige técnica, zonas y cantidades para ver el precio.</p>;
  }
  if (line.errors?.length) {
    return (
      <ul role="alert" className="space-y-1 text-sm font-semibold text-red-600">
        {line.errors.map((message) => <li key={message}>{message}</li>)}
      </ul>
    );
  }

  const discount = Number(line.discountAmount ?? 0);
  return (
    <div className={`transition-opacity ${isLoading ? "opacity-60" : ""}`} aria-live="polite">
      <dl className="space-y-2 text-sm">
        <Row label="Prenda base (c/u)" value={formatPrice(line.unitBasePrice)} />
        <Row label="Personalización (c/u)" value={formatPrice(line.unitCustomizationPrice)} />
        {line.zones?.map((zone) => (
          <Row key={zone.code} label={`· ${zone.name}`} value={`+ ${formatPrice(zone.surcharge)}`} muted />
        ))}
        <Row label={`Precio unitario × ${line.quantityTotal}`} value={formatPrice(line.grossAmount)} />
        {discount > 0 ? (
          <Row
            label={`Descuento ${line.tier?.label?.toLocaleLowerCase("es")} (−${Number(line.tier?.discountPercent)} %)`}
            value={`− ${formatPrice(discount)}`}
            accent
          />
        ) : null}
        <div className="flex items-end justify-between border-t border-stone-200 pt-3">
          <dt className="text-base font-extrabold text-slate-950">Total del diseño</dt>
          <dd className="flex items-center gap-2 text-2xl font-black tabular-nums text-slate-950">
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin text-slate-400" aria-hidden="true" /> : null}
            {formatPrice(line.lineTotal)}
          </dd>
        </div>
      </dl>
    </div>
  );
}

function Row({ label, value, muted, accent }) {
  const valueColor = accent ? "text-emerald-700" : muted ? "text-slate-500" : "text-slate-800";
  return (
    <div className={`flex justify-between gap-4 ${muted ? "text-xs text-slate-400" : "text-slate-600"}`}>
      <dt>{label}</dt>
      <dd className={`tabular-nums ${muted ? "" : "font-semibold"} ${valueColor}`}>{value}</dd>
    </div>
  );
}
