// Regla de cantidad D2 (opción A): cualquier cantidad ≥ 1 y se aplica la escala más alta
// alcanzada. Es solo para orientar al cliente; el precio final lo calcula el servidor.

export function tierFor(quantity, tiers) {
  const sorted = [...tiers].sort((a, b) => a.minQuantity - b.minQuantity);
  return sorted.filter((tier) => tier.minQuantity <= quantity).at(-1) ?? null;
}

export function nextTier(quantity, tiers) {
  return [...tiers].sort((a, b) => a.minQuantity - b.minQuantity).find((tier) => tier.minQuantity > quantity) ?? null;
}

// «Llevas 9 → precio de paquete de 6; agrega 3 más y obtienes precio de docena».
export function tierHint(quantity, tiers) {
  if (quantity < 1 || tiers.length === 0) return null;
  const current = tierFor(quantity, tiers);
  const next = nextTier(quantity, tiers);
  const reached = current ? `precio de ${current.label.toLocaleLowerCase("es")}` : "precio por unidad";
  const missing = next ? next.minQuantity - quantity : 0;
  return {
    current,
    next,
    text: `Llevas ${quantity} → ${reached}`,
    nextText: next
      ? `agrega ${missing} más y obtienes precio de ${next.label.toLocaleLowerCase("es")} (−${Number(next.discountPercent)} %)`
      : null,
  };
}

// Reparte `total` unidades entre las variantes dadas (en orden de talla), sin pasar del stock.
export function distribute(total, variants) {
  const available = variants.filter((variant) => variant.stock > 0);
  const quantities = Object.fromEntries(available.map((variant) => [variant.id, 0]));
  let remaining = total;
  while (remaining > 0) {
    const open = available.filter((variant) => quantities[variant.id] < variant.stock);
    if (open.length === 0) break;
    for (const variant of open) {
      if (remaining === 0) break;
      quantities[variant.id] += 1;
      remaining -= 1;
    }
  }
  return quantities;
}
