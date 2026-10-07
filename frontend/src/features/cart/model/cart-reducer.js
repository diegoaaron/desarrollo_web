import { designKey, mergeItems } from "./cart-line";

export const CART_ACTIONS = {
  add: "cart/add",
  remove: "cart/remove",
  setQuantity: "cart/set-quantity",
  clear: "cart/clear",
};

export function cartReducer(cart, action) {
  switch (action.type) {
    case CART_ACTIONS.add: {
      const key = designKey(action.line);
      const existing = cart.find((line) => designKey(line) === key);
      if (!existing) return [...cart, action.line];

      return cart.map((line) =>
        line === existing
          ? { ...line, items: mergeItems(line.items, action.line.items), estimatedTotal: null }
          : line,
      );
    }

    case CART_ACTIONS.remove:
      return cart.filter((line) => line.id !== action.id);

    // Cambia la cantidad de una talla/color; en 0 se quita y, si la línea queda vacía, también.
    case CART_ACTIONS.setQuantity:
      return cart
        .map((line) => {
          if (line.id !== action.id) return line;
          const items = line.items
            .map((item) => (item.variantId === action.variantId ? { ...item, quantity: action.quantity } : item))
            .filter((item) => item.quantity > 0);
          return { ...line, items, estimatedTotal: null };
        })
        .filter((line) => line.items.length > 0);

    case CART_ACTIONS.clear:
      return [];

    default:
      return cart;
  }
}
