import { useCallback } from "react";
import { useRequest } from "../../../shared/hooks/use-request";
import { getCustomizationOptions } from "../api/customization-api";

export function useCustomizationOptions(productId) {
  const fetcher = useCallback((options) => getCustomizationOptions(productId, options), [productId]);
  const { data, error, isLoading } = useRequest(fetcher);
  return { options: data, error: error?.message ?? null, isLoading };
}
