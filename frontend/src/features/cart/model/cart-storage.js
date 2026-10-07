// v2: líneas personalizadas con reparto por tallas. El carrito v1 (una variante por ítem)
// no se migra: se descarta al leer.
export const CART_STORAGE_KEY = "coralshop.cart.v2";

function isValidItem(item) {
  return item !== null && typeof item === "object" && Number.isInteger(item.variantId)
    && Number.isInteger(item.quantity) && item.quantity > 0;
}

function isValidLine(line) {
  return (
    line !== null &&
    typeof line === "object" &&
    typeof line.id === "string" &&
    Number.isInteger(line.productId) &&
    Array.isArray(line.zones) &&
    Array.isArray(line.items) &&
    line.items.length > 0 &&
    line.items.every(isValidItem)
  );
}

export function loadCart() {
  try {
    window.localStorage.removeItem("coralshop.cart.v1");
    const raw = window.localStorage.getItem(CART_STORAGE_KEY);
    if (!raw) return [];

    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter(isValidLine) : [];
  } catch {
    return [];
  }
}

export function saveCart(cart) {
  try {
    window.localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
  } catch {
    // Almacenamiento lleno o bloqueado (modo privado): el carrito sigue en memoria.
  }
}
