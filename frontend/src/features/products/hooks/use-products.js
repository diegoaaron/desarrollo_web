import { useCallback } from "react";
import { useRequest } from "../../../shared/hooks/use-request";
import { getProductsPage, getProductTypes } from "../api/products-api";

// filters: { type, categoryId, q, page, size }. Con skip no se pide nada (p. ej. mientras se
// resuelve el id de una categoría que llega por nombre en la URL).
export function useProducts({ type, categoryId, q, page = 0, size = 12, skip = false } = {}) {
  const fetcher = useCallback(
    (options) => (skip ? Promise.resolve(null) : getProductsPage({ type, categoryId, q, page, size }, options)),
    [type, categoryId, q, page, size, skip],
  );
  const { data, error, isLoading } = useRequest(fetcher);
  return {
    products: data?.items ?? [],
    totalItems: data?.totalItems ?? 0,
    totalPages: data?.totalPages ?? 0,
    isLoading: isLoading || skip,
    error: error?.message ?? null,
  };
}

export function useProductTypes() {
  const { data } = useRequest(getProductTypes);
  return data ?? [];
}
