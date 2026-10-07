const PRICE_FORMATTER = new Intl.NumberFormat("es-PE", {
  style: "currency",
  currency: "PEN",
});

export function formatPrice(value) {
  const amount = Number(value ?? 0);
  return PRICE_FORMATTER.format(Number.isFinite(amount) ? amount : 0);
}
