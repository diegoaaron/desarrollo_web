// Una línea del carrito = un diseño (producto + técnica + zonas + imagen) repartido entre
// tallas y colores (D3). El navegador solo guarda la elección; los precios los pone el servidor.

let sequence = 0;

function newLineId() {
  sequence += 1;
  return `l${Date.now().toString(36)}${sequence}`;
}

// Mismo diseño = mismo producto, técnica, zonas e imagen: se suman sus cantidades.
export function designKey(line) {
  return [line.productId, line.techniqueCode ?? "", [...(line.zones ?? [])].map((z) => z.code).sort().join("+"), line.designId ?? ""].join("|");
}

export function createLine({ product, technique, zones, design, items, estimatedTotal }) {
  return {
    id: newLineId(),
    productId: product.id,
    productName: product.name,
    productTypeCode: product.productTypeCode ?? null,
    image: product.imageUrl ?? null,
    techniqueCode: technique?.code ?? null,
    techniqueName: technique?.name ?? null,
    zones: (zones ?? []).map((zone) => ({ code: zone.code, name: zone.name })),
    designId: design?.id ?? null,
    designImageUrl: design?.imageUrl ?? null,
    designName: design?.originalFilename ?? null,
    items: items
      .filter((item) => item.quantity > 0)
      .map((item) => ({
        variantId: item.variantId,
        size: item.size,
        color: item.color,
        colorHex: item.colorHex ?? null,
        stock: item.stock ?? null,
        quantity: item.quantity,
      })),
    estimatedTotal: estimatedTotal ?? null,
  };
}

export function lineUnits(line) {
  return line.items.reduce((total, item) => total + item.quantity, 0);
}

export function cartUnits(lines) {
  return lines.reduce((total, line) => total + lineUnits(line), 0);
}

export function mergeItems(current, added) {
  const merged = current.map((item) => ({ ...item }));
  added.forEach((item) => {
    const existing = merged.find((candidate) => candidate.variantId === item.variantId);
    if (existing) existing.quantity += item.quantity;
    else merged.push({ ...item });
  });
  return merged;
}

export function lineSummary(line) {
  if (!line.techniqueCode) return "Sin personalizar";
  const zones = line.zones.map((zone) => zone.name).join(", ");
  return `${line.techniqueName ?? line.techniqueCode} · ${zones}`;
}

export function toLineRequest(line) {
  return {
    productId: line.productId,
    techniqueCode: line.techniqueCode,
    zoneCodes: line.zones.map((zone) => zone.code),
    designId: line.designId,
    items: line.items.map((item) => ({ variantId: item.variantId, quantity: item.quantity })),
  };
}
