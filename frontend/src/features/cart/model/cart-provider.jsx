import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from "react";
import { cartUnits } from "./cart-line";
import { CartContext } from "./cart-context";
import { CART_ACTIONS, cartReducer } from "./cart-reducer";
import { loadCart, saveCart } from "./cart-storage";

const NOTIFICATION_DURATION = 3000;

export function CartProvider({ children }) {
  const [cart, dispatch] = useReducer(cartReducer, undefined, loadCart);
  const [notification, setNotification] = useState(null);
  const notificationIdRef = useRef(0);
  const notificationTimerRef = useRef(null);

  const showNotification = useCallback((message, type) => {
    window.clearTimeout(notificationTimerRef.current);
    notificationIdRef.current += 1;

    setNotification({
      id: notificationIdRef.current,
      message,
      type,
    });

    notificationTimerRef.current = window.setTimeout(() => {
      setNotification(null);
      notificationTimerRef.current = null;
    }, NOTIFICATION_DURATION);
  }, []);

  useEffect(() => {
    saveCart(cart);
  }, [cart]);

  useEffect(
    () => () => window.clearTimeout(notificationTimerRef.current),
    [],
  );

  const addLine = useCallback(
    (line) => {
      dispatch({ type: CART_ACTIONS.add, line });
      showNotification("Tu diseño se agregó al carrito.", "success");
    },
    [showNotification],
  );

  const removeLine = useCallback(
    (id) => {
      dispatch({ type: CART_ACTIONS.remove, id });
      showNotification("Producto eliminado del carrito.", "error");
    },
    [showNotification],
  );

  const setItemQuantity = useCallback((id, variantId, quantity) => {
    dispatch({ type: CART_ACTIONS.setQuantity, id, variantId, quantity: Math.max(0, quantity) });
  }, []);

  // silent: al confirmar un pedido el carrito se vacía sin aviso de «eliminado».
  const clearCart = useCallback(({ silent = false } = {}) => {
    dispatch({ type: CART_ACTIONS.clear });
    if (!silent) showNotification("Productos eliminados del carrito.", "error");
  }, [showNotification]);

  const itemCount = useMemo(() => cartUnits(cart), [cart]);

  const value = useMemo(
    () => ({
      cart,
      itemCount,
      notification,
      addLine,
      removeLine,
      setItemQuantity,
      clearCart,
    }),
    [cart, itemCount, notification, addLine, removeLine, setItemQuantity, clearCart],
  );

  return (
    <CartContext.Provider value={value}>{children}</CartContext.Provider>
  );
}
