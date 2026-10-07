import { useState, useEffect } from "react";
import { ordersService } from "../services/orders-service";

export function useOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchOrders() {
      try {
        const data = await ordersService.getAll();
        if (!cancelled) setOrders(data);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchOrders();

    return () => {
      cancelled = true;
    };
  }, []);

  const updateStatus = async (id, status) => {
    setActionError(null);
    setUpdatingId(id);
    try {
      await ordersService.updateStatus(id, status);
      const data = await ordersService.getAll();
      setOrders(data);
      return true;
    } catch (err) {
      setActionError(`No se pudo actualizar el pedido #${id}: ${err.message}`);
      return false;
    } finally {
      setUpdatingId(null);
    }
  };

  const clearActionError = () => setActionError(null);

  return {
    orders,
    loading,
    error,
    actionError,
    updatingId,
    updateStatus,
    clearActionError,
  };
}
