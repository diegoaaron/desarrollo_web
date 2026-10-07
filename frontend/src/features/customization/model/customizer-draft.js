// Borrador del personalizador en sessionStorage: si el cliente va a iniciar sesión a mitad
// del camino, al volver encuentra sus elecciones (color, técnica, zonas, cantidades y diseño).
const key = (productId) => `coralshop.customizer.${productId}`;

export function loadDraft(productId) {
  try {
    const raw = window.sessionStorage.getItem(key(productId));
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveDraft(productId, draft) {
  try {
    window.sessionStorage.setItem(key(productId), JSON.stringify(draft));
  } catch {
    // Sin almacenamiento disponible el borrador solo vive en memoria.
  }
}

export function clearDraft(productId) {
  try {
    window.sessionStorage.removeItem(key(productId));
  } catch {
    // Nada que limpiar.
  }
}
