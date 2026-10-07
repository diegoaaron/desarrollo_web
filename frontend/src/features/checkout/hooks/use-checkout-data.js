import { useRequest } from "../../../shared/hooks/use-request";
import { addressesApi, getShippingMethods } from "../api/checkout-api";

export function useAddresses() {
  const { data, setData, error, isLoading } = useRequest(addressesApi.list);
  return { addresses: data ?? [], setAddresses: setData, error: error?.message ?? null, isLoading };
}

export function useShippingMethods() {
  const { data, error, isLoading } = useRequest(getShippingMethods);
  return { methods: data ?? [], error: error?.message ?? null, isLoading };
}
