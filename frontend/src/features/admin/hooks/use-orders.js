import { useCallback, useState } from "react";
import { useRequest } from "../../../shared/hooks/use-request";
import { ordersService } from "../services/orders-service";

const PAGE_SIZE = 20;

// Bandeja paginada y filtrada en el servidor.
export function useOrders({ status, page }) {
  const fetcher = useCallback(() => ordersService.getPage({ status, page, size: PAGE_SIZE }), [status, page]);
  const { data, error, isLoading } = useRequest(fetcher);
  return {
    orders: data?.items ?? [],
    totalItems: data?.totalItems ?? 0,
    totalPages: data?.totalPages ?? 0,
    loading: isLoading,
    error: error?.message ?? null,
  };
}

export function useAdminOrder(id) {
  const fetcher = useCallback(() => ordersService.getById(id), [id]);
  const { data, setData, error, isLoading } = useRequest(fetcher);
  const [updating, setUpdating] = useState(false);
  const [actionError, setActionError] = useState(null);

  const changeStatus = async (status, comment) => {
    setUpdating(true);
    setActionError(null);
    try {
      // La API devuelve el detalle ya actualizado (historial y siguientes estados incluidos).
      setData(await ordersService.updateStatus(id, status, comment));
      return true;
    } catch (requestError) {
      setActionError(requestError.message);
      return false;
    } finally {
      setUpdating(false);
    }
  };

  return {
    order: data,
    loading: isLoading,
    error: error?.message ?? null,
    updating,
    actionError,
    changeStatus,
    clearActionError: () => setActionError(null),
  };
}
