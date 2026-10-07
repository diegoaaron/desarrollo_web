export const CART_STORAGE_KEY = "coralshop.cart.v1";

function isValidItem(item) {
  return (
    item !== null &&
    typeof item === "object" &&
    (typeof item.id === "number" || typeof item.id === "string") &&
    item.id !== "" &&
    Number.isInteger(item.quantity) &&
    item.quantity > 0
  );
}

export function loadCart() {
  try {
    const raw = window.localStorage.getItem(CART_STORAGE_KEY);
    if (!raw) return [];

    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.every(isValidItem) ? parsed : [];
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
