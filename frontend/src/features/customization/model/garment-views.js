// Las zonas traseras se dibujan sobre la vista de espalda; el resto, sobre la frontal.
const BACK_ZONES = new Set(["ESPALDA", "TOTE_CARA_B"]);

export function viewForZone(zoneCode) {
  return BACK_ZONES.has(zoneCode) ? "back" : "front";
}

export const VIEW_LABELS = { front: "Delante", back: "Espalda" };

export function viewsFor(productTypeCode) {
  return productTypeCode === "GORRA" ? ["front"] : ["front", "back"];
}
