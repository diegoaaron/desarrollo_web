import { ArrowLeft, Check, Loader2, MapPin, Plus, Store, Truck } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useAuth } from "../../features/auth/hooks/use-auth";
import { fullName } from "../../features/auth/model/account-name";
import { CartLineThumb } from "../../features/cart/components/cart-line-thumb";
import { CartTotals } from "../../features/cart/components/cart-totals";
import { useCart } from "../../features/cart/hooks/use-cart";
import { useQuote } from "../../features/cart/hooks/use-quote";
import { lineSummary, lineUnits } from "../../features/cart/model/cart-line";
import { createOrder } from "../../features/checkout/api/checkout-api";
import { AddressForm } from "../../features/checkout/components/address-form";
import { Field } from "../../features/checkout/components/field";
import { fieldClass } from "../../features/checkout/components/field-styles";
import { PaymentForm } from "../../features/checkout/components/payment-form";
import { useAddresses, useShippingMethods } from "../../features/checkout/hooks/use-checkout-data";
import { formatPrice } from "../../shared/utils/format-price";

export function CheckoutPage() {
  const { account } = useAuth();
  const { cart, clearCart } = useCart();
  const navigate = useNavigate();
  const { quote, error: quoteError, isLoading: quoting } = useQuote(cart);
  const { addresses, setAddresses, isLoading: loadingAddresses, error: addressesError } = useAddresses();
  const { methods, isLoading: loadingMethods, error: methodsError } = useShippingMethods();

  const [methodCode, setMethodCode] = useState(null);
  const [addressId, setAddressId] = useState(null);
  const [addingAddress, setAddingAddress] = useState(false);
  const [contactPhone, setContactPhone] = useState("");
  const [note, setNote] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [order, setOrder] = useState(null);

  const method = methods.find((item) => item.code === methodCode) ?? null;
  const defaultAddress = addresses.find((item) => item.isDefault) ?? addresses[0] ?? null;
  const selectedAddressId = addressId ?? defaultAddress?.id ?? null;
  const showAddressForm = addingAddress || (!loadingAddresses && addresses.length === 0 && method?.requiresAddress);

  // Pedido ya creado: el carrito se vació y solo queda pagar.
  if (order) {
    return (
      <CheckoutShell title="Pago" subtitle={`Pedido ${order.orderCode} creado. Completa el pago para enviarlo a producción.`}>
        <div className="mx-auto max-w-xl rounded-[1.75rem] border border-stone-200 bg-white p-6 shadow-sm sm:p-8">
          <div className="mb-6 flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total a pagar</p>
              <p className="text-3xl font-black text-slate-950">{formatPrice(order.total)}</p>
            </div>
            <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-bold text-amber-700">Pendiente de pago</span>
          </div>
          <PaymentForm
            orderCode={order.orderCode}
            amount={order.total}
            onApproved={() => navigate(`/orders/${order.orderCode}/confirmation`, { replace: true })}
          />
          <p className="mt-5 text-center text-xs text-slate-500">
            ¿Prefieres pagar después? Tu pedido queda guardado en{" "}
            <Link to={`/account/orders/${order.orderCode}`} className="font-bold text-[#e94727] hover:underline">Mis pedidos</Link>.
          </p>
        </div>
      </CheckoutShell>
    );
  }

  if (cart.length === 0) {
    return (
      <CheckoutShell title="Checkout">
        <div className="mx-auto max-w-lg rounded-3xl border border-stone-200 bg-white px-6 py-12 text-center">
          <p className="font-bold text-slate-900">Tu carrito está vacío.</p>
          <Link to="/products" className="mt-4 inline-block font-bold text-[#e94727] hover:underline">Ir al catálogo</Link>
        </div>
      </CheckoutShell>
    );
  }

  const ready = Boolean(quote?.valid) && !quoting && method
    && (method.requiresAddress ? Boolean(selectedAddressId) : Boolean(contactPhone.trim() || defaultAddress));

  async function handleSubmit(event) {
    event.preventDefault();
    if (!ready || creating) return;
    setCreating(true);
    setError(null);
    setFieldErrors({});
    try {
      const created = await createOrder({
        lines: cart,
        addressId: method.requiresAddress || !contactPhone.trim() ? selectedAddressId : null,
        shippingMethodCode: method.code,
        contactPhone: method.requiresAddress ? null : contactPhone.trim(),
        customerNote: note.trim(),
      });
      setOrder(created);
      clearCart({ silent: true });
      window.scrollTo({ top: 0 });
    } catch (requestError) {
      setError(requestError.message);
      setFieldErrors(requestError.errors ?? {});
    } finally {
      setCreating(false);
    }
  }

  return (
    <CheckoutShell title="Checkout" subtitle="Elige cómo recibir tu pedido. Después del resumen viene el pago.">
      <form onSubmit={handleSubmit} className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_24rem] lg:gap-8">
        <div className="space-y-6">
          <Card title="1. Método de envío">
            {loadingMethods ? <Loading /> : methodsError ? <ErrorText message={methodsError} /> : (
              <div className="grid gap-3 sm:grid-cols-3">
                {methods.map((item) => {
                  const Icon = item.requiresAddress ? Truck : Store;
                  const checked = item.code === methodCode;
                  return (
                    <label
                      key={item.code}
                      className={`flex cursor-pointer flex-col gap-1 rounded-2xl border p-4 transition ${
                        checked ? "border-[#ff5331] bg-[#fff8f5] ring-2 ring-[#ff5331]/15" : "border-stone-200 bg-white hover:border-stone-300"
                      }`}
                    >
                      <input type="radio" name="shipping" value={item.code} checked={checked} onChange={() => setMethodCode(item.code)} className="sr-only" />
                      <Icon className="h-5 w-5 text-[#e94727]" aria-hidden="true" />
                      <span className="text-sm font-bold text-slate-900">{item.name}</span>
                      <span className="text-xs text-slate-500">
                        {Number(item.cost) > 0 ? formatPrice(item.cost) : "Gratis"} · {item.estimatedDays} {item.estimatedDays === 1 ? "día" : "días"}
                      </span>
                    </label>
                  );
                })}
              </div>
            )}
          </Card>

          {method ? (
            <Card title={method.requiresAddress ? "2. Dirección de entrega" : "2. Datos de contacto"}>
              {loadingAddresses ? <Loading /> : addressesError ? <ErrorText message={addressesError} /> : method.requiresAddress ? (
                <div className="space-y-3">
                  {addresses.map((address) => (
                    <label
                      key={address.id}
                      className={`flex cursor-pointer gap-3 rounded-2xl border p-4 transition ${
                        address.id === selectedAddressId ? "border-[#ff5331] bg-[#fff8f5]" : "border-stone-200 bg-white hover:border-stone-300"
                      }`}
                    >
                      <input
                        type="radio"
                        name="address"
                        checked={address.id === selectedAddressId}
                        onChange={() => setAddressId(address.id)}
                        className="mt-1 h-4 w-4 accent-[#ff5331]"
                      />
                      <span className="text-sm">
                        <span className="block font-bold text-slate-900">
                          {address.receiverName} · {address.phone}
                          {address.isDefault ? <span className="ml-2 rounded-full bg-stone-100 px-2 py-0.5 text-[0.65rem] font-bold uppercase text-slate-500">Principal</span> : null}
                        </span>
                        <span className="block text-slate-600">{address.street}</span>
                        <span className="block text-slate-500">
                          {address.district}, {address.province}, {address.department}
                          {address.reference ? ` · ${address.reference}` : ""}
                        </span>
                      </span>
                    </label>
                  ))}
                  {showAddressForm ? (
                    <AddressForm
                      defaultName={fullName(account)}
                      onSaved={(saved) => {
                        setAddresses((current) => [...(current ?? []).map((item) => (saved.isDefault ? { ...item, isDefault: false } : item)), saved]);
                        setAddressId(saved.id);
                        setAddingAddress(false);
                      }}
                      onCancel={addresses.length > 0 ? () => setAddingAddress(false) : null}
                    />
                  ) : (
                    <button
                      type="button"
                      onClick={() => setAddingAddress(true)}
                      className="inline-flex items-center gap-2 rounded-xl border border-dashed border-stone-300 px-4 py-2.5 text-sm font-bold text-slate-600 hover:border-[#ff5331] hover:text-[#e94727]"
                    >
                      <Plus className="h-4 w-4" aria-hidden="true" /> Nueva dirección
                    </button>
                  )}
                  {fieldErrors.addressId ? <ErrorText message={fieldErrors.addressId} /> : null}
                </div>
              ) : (
                <div className="space-y-3">
                  <p className="flex items-start gap-2 text-sm text-slate-600">
                    <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-[#e94727]" aria-hidden="true" />
                    Recoges en nuestro taller de Lima. Te escribiremos a este número cuando esté listo.
                  </p>
                  <Field
                    label="Teléfono de contacto"
                    error={fieldErrors.contactPhone}
                    hint={defaultAddress && !contactPhone ? `Si lo dejas vacío usaremos ${defaultAddress.phone}` : null}
                  >
                    <input
                      value={contactPhone}
                      onChange={(event) => setContactPhone(event.target.value)}
                      inputMode="tel"
                      autoComplete="tel"
                      placeholder="987 654 321"
                      className={fieldClass}
                    />
                  </Field>
                </div>
              )}
            </Card>
          ) : null}

          <Card title="Nota para el taller (opcional)">
            <textarea
              value={note}
              onChange={(event) => setNote(event.target.value)}
              maxLength={500}
              rows={3}
              placeholder="Ej.: logo centrado, respetar los colores del archivo"
              className={`${fieldClass} resize-y`}
            />
          </Card>
        </div>

        <aside className="space-y-4 lg:sticky lg:top-48">
          <div className="overflow-hidden rounded-[1.75rem] border border-stone-200/80 bg-white shadow-[0_24px_70px_-45px_rgba(15,23,42,0.45)]">
            <div className="border-b border-stone-200/80 px-5 py-5 sm:px-6">
              <h2 className="text-xl font-extrabold tracking-tight text-slate-950">Tu pedido</h2>
            </div>
            <ul className="divide-y divide-stone-100 px-5 sm:px-6">
              {cart.map((line, index) => {
                const quoted = quote?.lines?.find((item) => item.index === index);
                return (
                  <li key={line.id} className="flex gap-3 py-3">
                    <CartLineThumb line={line} className="h-14 w-14" />
                    <div className="min-w-0 flex-1 text-sm">
                      <p className="truncate font-bold text-slate-900">{line.productName}</p>
                      <p className="truncate text-xs text-slate-500">{lineSummary(line)}</p>
                      <p className="text-xs text-slate-500">{lineUnits(line)} u.</p>
                      {quoted?.errors?.length ? <p className="text-xs font-semibold text-red-600">{quoted.errors[0]}</p> : null}
                    </div>
                    <p className="text-sm font-bold tabular-nums text-slate-900">{quoted?.lineTotal != null ? formatPrice(quoted.lineTotal) : "—"}</p>
                  </li>
                );
              })}
            </ul>
            <div className="border-t border-stone-200/80 px-5 py-5 sm:px-6">
              <CartTotals quote={quote} quoting={quoting} shippingCost={method ? method.cost : null} />
              {quoteError ? <ErrorText message={quoteError} /> : null}
              {quote && !quote.valid ? (
                <p className="mt-3 text-sm text-amber-800">
                  Hay líneas con problemas. <Link to="/cart" className="font-bold underline">Revisa tu carrito</Link>.
                </p>
              ) : null}
              {error ? <p role="alert" className="mt-4 rounded-xl bg-red-50 px-3 py-2 text-sm font-semibold text-red-700">{error}</p> : null}
              <button
                type="submit"
                disabled={!ready || creating}
                className="mt-5 flex min-h-13 w-full items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-5 py-3.5 text-sm font-bold text-white shadow-lg shadow-[#ff5331]/20 transition hover:bg-[#e94727] disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none"
              >
                {creating ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Check className="h-4 w-4" aria-hidden="true" />}
                {creating ? "Creando pedido…" : method ? "Confirmar pedido e ir al pago" : "Elige un método de envío"}
              </button>
              <p className="mt-3 text-center text-xs text-slate-400">Al confirmar reservamos el stock de tus prendas.</p>
            </div>
          </div>
        </aside>
      </form>
    </CheckoutShell>
  );
}

function CheckoutShell({ title, subtitle, children }) {
  return (
    <main className="min-h-[70vh] bg-[#faf8f4] py-8 sm:py-12">
      <div className="mx-auto w-[92%] max-w-7xl">
        <Link to="/cart" className="mb-6 inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-[#ff5331]">
          <ArrowLeft className="h-4 w-4" aria-hidden="true" /> Volver al carrito
        </Link>
        <header className="mb-8">
          <h1 className="text-3xl font-black tracking-[-0.035em] text-slate-950 sm:text-4xl">{title}</h1>
          {subtitle ? <p className="mt-2 text-slate-500">{subtitle}</p> : null}
        </header>
        {children}
      </div>
    </main>
  );
}

function Card({ title, children }) {
  return (
    <section className="rounded-[1.5rem] border border-stone-200/80 bg-white p-5 shadow-sm sm:p-6">
      <h2 className="mb-4 text-lg font-extrabold text-slate-950">{title}</h2>
      {children}
    </section>
  );
}

function Loading() {
  return (
    <p className="flex items-center gap-2 text-sm text-slate-500" role="status">
      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> Cargando…
    </p>
  );
}

function ErrorText({ message }) {
  return <p role="alert" className="mt-2 text-sm font-semibold text-red-600">{message}</p>;
}
