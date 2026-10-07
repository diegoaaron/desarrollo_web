import { ArrowRight, Check, ShoppingCart } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router";
import { useAuth } from "../../auth/hooks/use-auth";
import { useCart } from "../../cart/hooks/use-cart";
import { useQuote } from "../../cart/hooks/use-quote";
import { createLine } from "../../cart/model/cart-line";
import { formatPrice } from "../../../shared/utils/format-price";
import { useCustomizationOptions } from "../hooks/use-customization-options";
import { useDesignUpload } from "../hooks/use-design-upload";
import { clearDraft, loadDraft, saveDraft } from "../model/customizer-draft";
import { VIEW_LABELS, viewForZone, viewsFor } from "../model/garment-views";
import { distribute, tierHint } from "../model/quantity-tiers";
import { DesignDropzone } from "./design-dropzone";
import { GarmentPreview } from "./garment-preview";
import { PriceBreakdown } from "./price-breakdown";
import { SizeDistributionTable } from "./size-distribution-table";

const QUICK_QUANTITIES = [1, 3, 6, 12];

export function ProductCustomizer({ product }) {
  const { account } = useAuth();
  const { addLine } = useCart();
  const location = useLocation();
  const { options, error: optionsError, isLoading: optionsLoading } = useCustomizationOptions(product.id);

  const variants = useMemo(() => product.variants.filter((variant) => variant.isActive !== false), [product.variants]);
  const colors = useMemo(() => {
    const list = [];
    variants.forEach((variant) => {
      const existing = list.find((color) => color.id === variant.colorId);
      if (existing) existing.stock += variant.stock;
      else list.push({ id: variant.colorId, name: variant.color, hex: variant.colorHex, stock: variant.stock });
    });
    return list;
  }, [variants]);

  const [draft] = useState(() => loadDraft(product.id));
  const [colorId, setColorId] = useState(() => draft?.colorId ?? colors.find((color) => color.stock > 0)?.id ?? colors[0]?.id ?? null);
  const [techniqueCode, setTechniqueCode] = useState(draft?.techniqueCode ?? null);
  const [zoneCodes, setZoneCodes] = useState(draft?.zoneCodes ?? []);
  const [quantities, setQuantities] = useState(draft?.quantities ?? {});
  const [view, setView] = useState("front");
  const [added, setAdded] = useState(false);

  const upload = useDesignUpload({ canUpload: Boolean(account), initialDesign: account ? draft?.design ?? null : null });

  const customizable = product.isCustomizable && (options?.techniques?.length ?? 0) > 0;
  const technique = options?.techniques?.find((item) => item.code === techniqueCode) ?? null;
  const zones = technique ? technique.zones.filter((zone) => zoneCodes.includes(zone.code)) : [];
  const tiers = options?.tiers ?? [];
  const selectedColor = colors.find((color) => color.id === colorId) ?? null;

  const items = variants
    .filter((variant) => (quantities[variant.id] ?? 0) > 0)
    .map((variant) => ({
      variantId: variant.id,
      size: variant.size,
      color: variant.color,
      colorHex: variant.colorHex,
      stock: variant.stock,
      quantity: quantities[variant.id],
    }));
  const units = items.reduce((total, item) => total + item.quantity, 0);
  const hint = tierHint(units, tiers);

  // Se cotiza en cuanto la línea está completa; el diseño no cambia el precio.
  const readyToQuote = units > 0 && (!customizable || (technique && zones.length > 0));
  const zonesKey = zoneCodes.join();
  const quantitiesKey = JSON.stringify(quantities);
  const quoteInput = useMemo(
    () => (readyToQuote
      ? [{ productId: product.id, techniqueCode: technique?.code ?? null, zones, designId: null, items }]
      : []),
    // zones e items se recalculan en cada render; su contenido lo resumen zonesKey y quantitiesKey.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [readyToQuote, product.id, technique?.code, zonesKey, quantitiesKey],
  );
  const { quote, error: quoteError, isLoading: quoting } = useQuote(quoteInput);
  const quotedLine = readyToQuote ? quote?.lines?.[0] ?? null : null;

  useEffect(() => {
    saveDraft(product.id, { colorId, techniqueCode, zoneCodes, quantities, design: upload.design });
  }, [product.id, colorId, techniqueCode, zoneCodes, quantities, upload.design]);

  function chooseTechnique(code) {
    const next = options.techniques.find((item) => item.code === code);
    setTechniqueCode(code);
    // Al cambiar de técnica se conservan solo las zonas que la nueva admite.
    setZoneCodes((current) => current.filter((zoneCode) => next.zones.some((zone) => zone.code === zoneCode)));
  }

  function toggleZone(zone) {
    setZoneCodes((current) => (current.includes(zone.code)
      ? current.filter((code) => code !== zone.code)
      : [...current, zone.code]));
    setView(viewForZone(zone.code));
  }

  function setQuantity(variantId, quantity) {
    setAdded(false);
    setQuantities((current) => ({ ...current, [variantId]: quantity }));
  }

  function quickFill(total) {
    setAdded(false);
    const ofColor = variants.filter((variant) => variant.colorId === colorId);
    setQuantities(distribute(total, ofColor));
  }

  const needsDesign = customizable;
  const needsSignIn = needsDesign && !account;
  const lineValid = quotedLine && !quotedLine.errors?.length && !quoting;
  const canAdd = lineValid && (!needsDesign || (upload.design && !upload.uploading));

  function handleAdd() {
    if (!canAdd) return;
    addLine(createLine({
      product,
      technique: customizable ? technique : null,
      zones: customizable ? zones : [],
      design: customizable ? upload.design : null,
      items,
      estimatedTotal: quotedLine.lineTotal,
    }));
    setQuantities({});
    setAdded(true);
    clearDraft(product.id);
  }

  if (optionsLoading) {
    return <p className="text-sm text-slate-500" role="status">Cargando opciones de personalización…</p>;
  }
  if (optionsError) {
    return <p className="text-sm font-semibold text-red-600" role="alert">{optionsError}</p>;
  }

  const steps = customizable
    ? { color: 1, technique: 2, zones: 3, design: 4, quantities: 5, price: 6 }
    : { color: 1, quantities: 2, price: 3 };

  return (
    <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
      {/* Vista previa: fija mientras se recorren los pasos */}
      <div className="lg:sticky lg:top-40 lg:self-start">
        <div className="rounded-3xl border border-stone-200 bg-gradient-to-b from-stone-50 to-white p-6">
          <GarmentPreview
            productTypeCode={product.productTypeCode}
            colorHex={selectedColor?.hex}
            view={view}
            zones={zones}
            designUrl={upload.previewUrl}
            techniqueCode={technique?.code}
          />
          {viewsFor(product.productTypeCode).length > 1 ? (
            <div className="mt-4 flex justify-center gap-2" role="group" aria-label="Cambiar vista">
              {viewsFor(product.productTypeCode).map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setView(item)}
                  aria-pressed={view === item}
                  className={`rounded-full px-4 py-1.5 text-xs font-bold ${view === item ? "bg-slate-900 text-white" : "bg-stone-100 text-slate-600 hover:bg-stone-200"}`}
                >
                  {VIEW_LABELS[item]}
                </button>
              ))}
            </div>
          ) : null}
          {zones.length > 0 ? (
            <p className="mt-4 text-center text-xs text-slate-500">
              Medidas máximas: {zones.map((zone) => `${zone.name} ${Number(zone.maxWidthCm)}×${Number(zone.maxHeightCm)} cm`).join(" · ")}
            </p>
          ) : null}
        </div>
        {product.imageUrl ? (
          <div className="mt-4 flex items-center gap-3 text-xs text-slate-500">
            <img
              src={product.imageUrl}
              alt={product.name}
              className="h-14 w-14 rounded-xl border border-stone-200 bg-white object-contain"
              onError={(event) => { event.currentTarget.style.display = "none"; }}
            />
            Foto referencial de la prenda base.
          </div>
        ) : null}
      </div>

      <div className="flex flex-col gap-8">
        <Step number={steps.color} title="Color">
          <div className="flex flex-wrap gap-2">
            {colors.map((color) => (
              <button
                key={color.id}
                type="button"
                onClick={() => setColorId(color.id)}
                disabled={color.stock < 1}
                aria-pressed={color.id === colorId}
                className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm font-semibold transition disabled:opacity-40 ${
                  color.id === colorId ? "border-[#ff5331] bg-[#fff0eb] text-[#c2381c]" : "border-stone-200 bg-white text-slate-700 hover:border-stone-300"
                }`}
              >
                <span className="h-5 w-5 rounded-full border border-stone-300" style={{ backgroundColor: color.hex ?? "#fff" }} />
                {color.name}
                {color.stock < 1 ? " (agotado)" : ""}
              </button>
            ))}
            {colors.length === 0 ? <p className="text-sm text-slate-500">Este producto aún no tiene tallas ni colores disponibles.</p> : null}
          </div>
        </Step>

        {customizable ? (
          <>
            <Step number={steps.technique} title="Técnica">
              <div className="grid gap-3 sm:grid-cols-2">
                {options.techniques.map((item) => (
                  <button
                    key={item.code}
                    type="button"
                    onClick={() => chooseTechnique(item.code)}
                    aria-pressed={item.code === techniqueCode}
                    className={`rounded-2xl border p-4 text-left transition ${
                      item.code === techniqueCode ? "border-[#ff5331] bg-[#fff8f5] ring-2 ring-[#ff5331]/15" : "border-stone-200 bg-white hover:border-stone-300"
                    }`}
                  >
                    <span className="flex items-center justify-between gap-2">
                      <span className="font-bold text-slate-900">{item.name}</span>
                      <span className="text-sm font-semibold text-slate-500">+ {formatPrice(item.baseCost)}</span>
                    </span>
                    <span className="mt-1 block text-xs leading-5 text-slate-500">{item.description}</span>
                  </button>
                ))}
              </div>
            </Step>

            <Step number={steps.zones} title="Zonas del diseño" hint={technique ? null : "Primero elige una técnica."}>
              {technique ? (
                <div className="grid gap-2 sm:grid-cols-2">
                  {technique.zones.map((zone) => {
                    const checked = zoneCodes.includes(zone.code);
                    return (
                      <label
                        key={zone.code}
                        className={`flex cursor-pointer items-center gap-3 rounded-xl border px-3 py-2.5 transition ${
                          checked ? "border-[#ff5331] bg-[#fff8f5]" : "border-stone-200 bg-white hover:border-stone-300"
                        }`}
                      >
                        <input type="checkbox" checked={checked} onChange={() => toggleZone(zone)} className="h-4 w-4 accent-[#ff5331]" />
                        <span className="flex-1">
                          <span className="block text-sm font-semibold text-slate-800">{zone.name}</span>
                          <span className="block text-xs text-slate-400">hasta {Number(zone.maxWidthCm)}×{Number(zone.maxHeightCm)} cm</span>
                        </span>
                        <span className="text-xs font-bold text-slate-500">+ {formatPrice(zone.surcharge)}</span>
                      </label>
                    );
                  })}
                </div>
              ) : null}
            </Step>

            <Step number={steps.design} title="Tu diseño">
              <DesignDropzone upload={upload} isSignedIn={Boolean(account)} />
            </Step>
          </>
        ) : (
          <p className="rounded-xl bg-stone-50 px-4 py-3 text-sm text-slate-600">Este producto se vende sin personalización.</p>
        )}

        <Step number={steps.quantities} title="Cantidades por talla y color">
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-500">Rápido ({selectedColor?.name ?? "color elegido"}):</span>
            {QUICK_QUANTITIES.map((quantity) => (
              <button
                key={quantity}
                type="button"
                onClick={() => quickFill(quantity)}
                className="rounded-lg border border-stone-200 bg-white px-3 py-1.5 text-sm font-bold text-slate-700 hover:border-[#ff5331] hover:text-[#e94727]"
              >
                {quantity === 12 ? "12 (docena)" : quantity}
              </button>
            ))}
            {units > 0 ? (
              <button type="button" onClick={() => setQuantities({})} className="ml-auto text-xs font-semibold text-slate-400 hover:text-red-600">
                Limpiar
              </button>
            ) : null}
          </div>
          <SizeDistributionTable variants={variants} quantities={quantities} onChange={setQuantity} highlightColorId={colorId} />
          <div className="mt-3 rounded-xl bg-stone-50 px-4 py-3 text-sm" aria-live="polite">
            <p className="font-bold text-slate-900">Total: {units} {units === 1 ? "unidad" : "unidades"}</p>
            {hint ? (
              <p className="mt-0.5 text-slate-600">
                {hint.text}
                {hint.nextText ? <>; <span className="font-semibold text-[#e94727]">{hint.nextText}</span></> : null}
              </p>
            ) : (
              <p className="mt-0.5 text-slate-500">Desde 3 unidades del mismo diseño ya pagas precio de paquete.</p>
            )}
          </div>
        </Step>

        <Step number={steps.price} title="Precio">
          <PriceBreakdown line={quotedLine} isLoading={quoting} error={readyToQuote ? quoteError : null} />
        </Step>

        <div className="flex flex-col gap-3 border-t border-stone-200 pt-6">
          {needsSignIn ? (
            <Link
              to="/login"
              state={{ from: `${location.pathname}${location.search}` }}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-8 py-4 font-semibold text-white hover:bg-black"
            >
              Inicia sesión para guardar tu diseño
              <ArrowRight className="h-5 w-5" aria-hidden="true" />
            </Link>
          ) : (
            <button
              type="button"
              onClick={handleAdd}
              disabled={!canAdd}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-8 py-4 font-semibold text-white shadow-lg shadow-[#ff5331]/20 transition hover:bg-[#e94727] disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none"
            >
              <ShoppingCart className="h-5 w-5" aria-hidden="true" />
              {addButtonLabel({ units, customizable, technique, zones, design: upload.design, uploading: upload.uploading })}
            </button>
          )}
          {added ? (
            <p className="flex items-center justify-center gap-2 text-sm font-semibold text-emerald-700" role="status">
              <Check className="h-4 w-4" aria-hidden="true" /> Listo. Puedes armar otro reparto o
              <Link to="/cart" className="underline">ir al carrito</Link>
            </p>
          ) : null}
        </div>
      </div>
    </div>
  );
}

function addButtonLabel({ units, customizable, technique, zones, design, uploading }) {
  if (customizable && !technique) return "Elige una técnica";
  if (customizable && zones.length === 0) return "Elige al menos una zona";
  if (customizable && uploading) return "Subiendo tu diseño…";
  if (customizable && !design) return "Sube tu diseño";
  if (units === 0) return "Elige cantidades";
  return "Agregar al carrito";
}

function Step({ number, title, hint, children }) {
  return (
    <section>
      <h2 className="mb-3 flex items-center gap-3 text-base font-extrabold text-slate-950">
        <span className="grid h-7 w-7 place-items-center rounded-full bg-slate-900 text-xs font-black text-white">{number}</span>
        {title}
      </h2>
      {hint ? <p className="text-sm text-slate-500">{hint}</p> : children}
    </section>
  );
}
