import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  Minus,
  Plus,
  ShieldCheck,
  ShoppingBag,
  Trash2,
} from "lucide-react";
import { Link, useNavigate } from "react-router";
import { CartLineThumb } from "../../features/cart/components/cart-line-thumb";
import { CartTotals } from "../../features/cart/components/cart-totals";
import { useCart } from "../../features/cart/hooks/use-cart";
import { useQuote } from "../../features/cart/hooks/use-quote";
import { lineSummary, lineUnits } from "../../features/cart/model/cart-line";
import { formatPrice } from "../../shared/utils/format-price";

export function CartPage() {
  const { cart, itemCount, removeLine, setItemQuantity, clearCart } = useCart();
  const { quote, error: quoteError, isLoading: quoting } = useQuote(cart);
  const navigate = useNavigate();

  const quotedLine = (index) => quote?.lines?.find((line) => line.index === index) ?? null;
  const canCheckout = Boolean(quote?.valid) && !quoting && cart.length > 0;

  return (
    <main className="relative min-h-[70vh] overflow-hidden bg-[#faf8f4] py-8 sm:py-12 lg:py-16">
      <div
        className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-[#ff5331]/8 blur-3xl"
        aria-hidden="true"
      />

      <div className="relative mx-auto w-[92%] max-w-7xl">
        <Link
          to="/products"
          className="mb-7 inline-flex min-h-10 items-center gap-2 rounded-lg px-1 text-sm font-semibold text-slate-500 transition-colors hover:text-[#ff5331]"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Seguir comprando
        </Link>

        <header className="mb-8 flex flex-col gap-5 sm:mb-10 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <span className="mb-3 inline-flex items-center gap-2 rounded-full border border-[#ff5331]/15 bg-[#fff0eb] px-3.5 py-1.5 text-xs font-bold uppercase tracking-[0.16em] text-[#e94727]">
              <ShoppingBag className="h-3.5 w-3.5" aria-hidden="true" />
              Carrito de compras
            </span>
            <h1 className="max-w-2xl text-3xl font-black tracking-[-0.035em] text-slate-950 sm:text-4xl lg:text-5xl">
              Tus diseños
            </h1>
            <p className="mt-3 max-w-xl text-sm leading-6 text-slate-500 sm:text-base">
              Ajusta el reparto por tallas. Los precios se recalculan en el servidor con cada cambio.
            </p>
          </div>

          {cart.length > 0 && (
            <div className="inline-flex w-fit items-center gap-2 rounded-2xl border border-stone-200 bg-white px-4 py-3 shadow-sm">
              <span className="grid h-8 w-8 place-items-center rounded-xl bg-stone-100 text-sm font-black text-slate-900">
                {itemCount}
              </span>
              <span className="text-sm font-medium text-slate-600">
                {itemCount === 1 ? "unidad" : "unidades"} en {cart.length} {cart.length === 1 ? "diseño" : "diseños"}
              </span>
            </div>
          )}
        </header>

        {cart.length === 0 ? (
          <EmptyCart />
        ) : (
          <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_22rem] lg:gap-8 xl:grid-cols-[minmax(0,1fr)_24rem]">
            <section
              className="overflow-hidden rounded-[1.75rem] border border-stone-200/80 bg-white shadow-[0_24px_70px_-45px_rgba(15,23,42,0.4)]"
              aria-labelledby="cart-items-title"
            >
              <div className="flex items-center justify-between gap-4 border-b border-stone-200/80 px-4 py-4 sm:px-6 sm:py-5">
                <h2 id="cart-items-title" className="text-lg font-extrabold tracking-tight text-slate-900 sm:text-xl">
                  Tu selección
                </h2>
                <button
                  type="button"
                  onClick={() => clearCart()}
                  className="inline-flex min-h-10 shrink-0 items-center gap-2 rounded-xl px-3 text-xs font-bold text-slate-500 transition-colors hover:bg-red-50 hover:text-red-600 sm:text-sm"
                >
                  <Trash2 className="h-4 w-4" aria-hidden="true" />
                  <span className="hidden sm:inline">Vaciar carrito</span>
                </button>
              </div>

              <div className="divide-y divide-stone-200/80 px-4 sm:px-6">
                {cart.map((line, index) => (
                  <CartLineRow
                    key={line.id}
                    line={line}
                    quoted={quotedLine(index)}
                    quoting={quoting}
                    onRemove={() => removeLine(line.id)}
                    onQuantity={(variantId, quantity) => setItemQuantity(line.id, variantId, quantity)}
                  />
                ))}
              </div>
            </section>

            <aside className="lg:sticky lg:top-48" aria-labelledby="order-summary-title">
              <div className="overflow-hidden rounded-[1.75rem] border border-stone-200/80 bg-white shadow-[0_24px_70px_-45px_rgba(15,23,42,0.45)]">
                <div className="border-b border-stone-200/80 px-5 py-5 sm:px-6">
                  <h2 id="order-summary-title" className="text-xl font-extrabold tracking-tight text-slate-950">
                    Resumen
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">Cotizado por el servidor</p>
                </div>

                <div className="px-5 py-5 sm:px-6">
                  <CartTotals quote={quote} quoting={quoting} />

                  {quoteError ? <p role="alert" className="mt-4 text-sm font-semibold text-red-600">{quoteError}</p> : null}
                  {quote && !quote.valid ? (
                    <p role="alert" className="mt-4 flex gap-2 rounded-xl bg-amber-50 px-3 py-2 text-sm text-amber-800">
                      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                      Hay líneas que no se pueden comprar tal como están. Corrígelas o quítalas para continuar.
                    </p>
                  ) : null}

                  <button
                    type="button"
                    onClick={() => navigate("/checkout")}
                    disabled={!canCheckout}
                    className="mt-6 flex min-h-13 w-full items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-5 py-3.5 text-sm font-bold text-white shadow-lg shadow-[#ff5331]/20 transition hover:bg-[#e94727] disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none"
                  >
                    Continuar con el pago
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </button>

                  <div className="mt-4 flex items-center justify-center gap-2 text-xs font-medium text-slate-400">
                    <ShieldCheck className="h-4 w-4 text-emerald-600" aria-hidden="true" />
                    El precio final se confirma al crear el pedido
                  </div>
                </div>
              </div>
            </aside>
          </div>
        )}
      </div>
    </main>
  );
}

function CartLineRow({ line, quoted, quoting, onRemove, onQuantity }) {
  const errors = quoted?.errors ?? [];
  return (
    <article className="py-5 sm:py-6">
      <div className="grid grid-cols-[5.5rem_minmax(0,1fr)] gap-4 sm:grid-cols-[7rem_minmax(0,1fr)_auto] sm:gap-5">
        <CartLineThumb line={line} className="h-24 w-[5.5rem] sm:h-28 sm:w-28" />

        <div className="min-w-0">
          <Link to={`/product/${line.productId}`} className="text-sm font-bold text-slate-900 hover:text-[#ff5331] sm:text-base">
            {line.productName}
          </Link>
          <p className="mt-1 text-xs text-slate-500 sm:text-sm">{lineSummary(line)}</p>
          {line.designName ? <p className="mt-0.5 truncate text-xs text-slate-400">Diseño: {line.designName}</p> : null}
          {quoted && !errors.length ? (
            <p className="mt-2 text-xs font-semibold text-slate-600">
              {formatPrice(quoted.unitPrice)} c/u · {quoted.tier?.label}
              {Number(quoted.tier?.discountPercent) > 0 ? ` (−${Number(quoted.tier.discountPercent)} %)` : ""}
            </p>
          ) : null}
        </div>

        <div className="col-span-2 flex items-start justify-between gap-3 sm:col-span-1 sm:flex-col sm:items-end">
          <div className="text-left sm:text-right">
            <p className={`text-lg font-black tabular-nums text-slate-950 ${quoting ? "opacity-60" : ""}`}>
              {quoted?.lineTotal != null ? formatPrice(quoted.lineTotal) : "—"}
            </p>
            <p className="text-xs text-slate-400">{lineUnits(line)} unidades</p>
          </div>
          <button
            type="button"
            onClick={onRemove}
            className="inline-flex min-h-9 items-center gap-1.5 rounded-lg px-2 text-xs font-semibold text-slate-400 transition-colors hover:bg-red-50 hover:text-red-600 sm:text-sm"
            aria-label={`Quitar ${line.productName} del carrito`}
          >
            <Trash2 className="h-4 w-4" aria-hidden="true" />
            Quitar
          </button>
        </div>
      </div>

      <ul className="mt-4 flex flex-wrap gap-2">
        {line.items.map((item) => (
          <li key={item.variantId} className="inline-flex items-center gap-2 rounded-xl border border-stone-200 bg-stone-50 py-1 pl-3 pr-1">
            <span className="h-3.5 w-3.5 rounded-full border border-stone-300" style={{ backgroundColor: item.colorHex ?? "#fff" }} />
            <span className="text-xs font-bold text-slate-700">{item.size} · {item.color}</span>
            <span className="inline-flex items-center rounded-lg bg-white">
              <button
                type="button"
                onClick={() => onQuantity(item.variantId, item.quantity - 1)}
                className="grid h-7 w-7 place-items-center rounded-lg text-slate-600 hover:bg-stone-100"
                aria-label={`Quitar una unidad talla ${item.size} ${item.color}`}
              >
                <Minus className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
              <span className="min-w-7 text-center text-sm font-extrabold tabular-nums">{item.quantity}</span>
              <button
                type="button"
                onClick={() => onQuantity(item.variantId, item.quantity + 1)}
                disabled={item.stock != null && item.quantity >= item.stock}
                className="grid h-7 w-7 place-items-center rounded-lg text-slate-600 hover:bg-stone-100 disabled:opacity-35"
                aria-label={`Agregar una unidad talla ${item.size} ${item.color}`}
              >
                <Plus className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            </span>
          </li>
        ))}
      </ul>

      {errors.length ? (
        <ul role="alert" className="mt-3 space-y-1 rounded-xl bg-red-50 px-3 py-2 text-sm font-semibold text-red-700">
          {errors.map((message) => <li key={message}>{message}</li>)}
        </ul>
      ) : null}
    </article>
  );
}

function EmptyCart() {
  return (
    <section className="mx-auto max-w-2xl overflow-hidden rounded-[2rem] border border-stone-200/80 bg-white px-6 py-12 text-center shadow-[0_30px_80px_-50px_rgba(15,23,42,0.45)] sm:px-12 sm:py-16">
      <div className="relative mx-auto mb-7 w-fit">
        <div className="absolute inset-0 scale-150 rounded-full bg-[#ff5331]/10 blur-2xl" />
        <div className="relative grid h-24 w-24 place-items-center rounded-full border border-[#ff5331]/15 bg-[#fff8f4] text-[#ff5331]">
          <ShoppingBag className="h-10 w-10" aria-hidden="true" />
        </div>
      </div>
      <h2 className="text-2xl font-black tracking-tight text-slate-950 sm:text-3xl">
        Tu carrito está listo para algo especial
      </h2>
      <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-slate-500 sm:text-base">
        Elige una prenda, súbele tu diseño y arma tu pedido por unidad o por mayor.
      </p>
      <Link
        to="/products"
        className="mt-8 inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-6 py-3 text-sm font-bold text-white shadow-lg shadow-[#ff5331]/20 transition hover:bg-[#e94727]"
      >
        Descubrir productos
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </Link>
    </section>
  );
}
