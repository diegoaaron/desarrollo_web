import { useCallback } from "react";
import { useRequest } from "../../../shared/hooks/use-request";
import { getMyOrder, getMyOrders } from "../api/orders-api";

export function useMyOrders() {
  const { data, error, isLoading } = useRequest(getMyOrders);
  return { orders: data ?? [], error: error?.message ?? null, isLoading };
}

export function useMyOrder(code) {
  const fetcher = useCallback((options) => getMyOrder(code, options), [code]);
  const { data, error, isLoading, reload } = useRequest(fetcher);
  return { order: data, error: error?.message ?? null, notFound: error?.status === 404, isLoading, reload };
}
