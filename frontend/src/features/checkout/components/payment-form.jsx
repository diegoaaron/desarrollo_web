import { CreditCard, Loader2, Lock } from "lucide-react";
import { useState } from "react";
import { formatPrice } from "../../../shared/utils/format-price";
import { payOrder } from "../api/checkout-api";
import { Field } from "./field";
import { fieldClass } from "./field-styles";

// Tarjetas de prueba de la pasarela simulada (fases.md §2.4). La tarjeta nunca se guarda.
const TEST_CARDS = [
  { number: "4111 1111 1111 1111", label: "Aprobada" },
  { number: "4000 0000 0000 0002", label: "Rechazada por fondos" },
];

function formatCardNumber(value) {
  return value.replace(/\D/g, "").slice(0, 19).replace(/(\d{4})(?=\d)/g, "$1 ");
}

export function PaymentForm({ orderCode, amount, onApproved }) {
  const now = new Date();
  const [card, setCard] = useState({
    cardNumber: "",
    cardHolder: "",
    expiryMonth: String(now.getMonth() + 1),
    expiryYear: String(now.getFullYear() + 2),
    cvv: "",
  });
  const [paying, setPaying] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});

  const update = (field) => (event) => {
    const value = field === "cardNumber" ? formatCardNumber(event.target.value)
      : field === "cvv" ? event.target.value.replace(/\D/g, "").slice(0, 4)
        : event.target.value;
    setCard((current) => ({ ...current, [field]: value }));
  };

  async function handleSubmit(event) {
    event.preventDefault();
    if (paying) return;
    setPaying(true);
    setError(null);
    setFieldErrors({});
    setResult(null);
    try {
      const response = await payOrder(orderCode, {
        ...card,
        cardHolder: card.cardHolder.trim(),
        expiryMonth: Number(card.expiryMonth),
        expiryYear: Number(card.expiryYear),
      });
      setResult(response);
      if (response.paymentStatus === "APROBADO") onApproved(response);
    } catch (requestError) {
      setError(requestError.message);
      setFieldErrors(requestError.errors ?? {});
    } finally {
      setPaying(false);
    }
  }

  const years = Array.from({ length: 12 }, (_, index) => now.getFullYear() - 1 + index);

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      <div className="rounded-2xl border border-dashed border-sky-200 bg-sky-50 px-4 py-3 text-xs text-sky-900">
        <p className="font-bold">Pago simulado: usa una tarjeta de prueba</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {TEST_CARDS.map((test) => (
            <button
              key={test.number}
              type="button"
              onClick={() => setCard((current) => ({ ...current, cardNumber: test.number, cardHolder: current.cardHolder || "CLIENTE DEMO", cvv: current.cvv || "123" }))}
              className="rounded-lg bg-white px-2.5 py-1 font-mono font-semibold text-sky-800 ring-1 ring-sky-200 hover:ring-sky-400"
            >
              {test.number} · {test.label}
            </button>
          ))}
        </div>
      </div>

      <Field label="Número de tarjeta" error={fieldErrors.cardNumber}>
        <div className="relative">
          <CreditCard className="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" aria-hidden="true" />
          <input
            value={card.cardNumber}
            onChange={update("cardNumber")}
            inputMode="numeric"
            autoComplete="cc-number"
            placeholder="0000 0000 0000 0000"
            className={`${fieldClass} pl-10 font-mono`}
            required
          />
        </div>
      </Field>
      <Field label="Titular" error={fieldErrors.cardHolder}>
        <input value={card.cardHolder} onChange={update("cardHolder")} autoComplete="cc-name" className={fieldClass} required />
      </Field>
      <div className="grid grid-cols-3 gap-3">
        <Field label="Mes" error={fieldErrors.expiryMonth}>
          <select value={card.expiryMonth} onChange={update("expiryMonth")} className={fieldClass}>
            {Array.from({ length: 12 }, (_, index) => index + 1).map((month) => (
              <option key={month} value={month}>{String(month).padStart(2, "0")}</option>
            ))}
          </select>
        </Field>
        <Field label="Año" error={fieldErrors.expiryYear}>
          <select value={card.expiryYear} onChange={update("expiryYear")} className={fieldClass}>
            {years.map((year) => <option key={year} value={year}>{year}</option>)}
          </select>
        </Field>
        <Field label="CVV" error={fieldErrors.cvv}>
          <input value={card.cvv} onChange={update("cvv")} inputMode="numeric" autoComplete="cc-csc" className={fieldClass} required />
        </Field>
      </div>

      {error ? <p role="alert" className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p> : null}
      {result && result.paymentStatus !== "APROBADO" ? (
        <p role="alert" className="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-800">
          <span className="font-bold">Pago rechazado.</span> {result.message} Tu pedido sigue pendiente de pago: puedes intentar con otra tarjeta.
        </p>
      ) : null}

      <button
        type="submit"
        disabled={paying}
        className="flex min-h-13 w-full items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-5 py-3.5 text-sm font-bold text-white shadow-lg shadow-[#ff5331]/20 transition hover:bg-[#e94727] disabled:cursor-wait disabled:opacity-60"
      >
        {paying ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Lock className="h-4 w-4" aria-hidden="true" />}
        {paying ? "Procesando pago…" : `Pagar ${formatPrice(amount)}`}
      </button>
    </form>
  );
}
