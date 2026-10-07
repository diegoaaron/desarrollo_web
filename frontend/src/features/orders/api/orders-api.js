import { http } from "../../../shared/api/http-client";

export function getMyOrders(options) {
  return http.get("/orders/me", options);
}

export function getMyOrder(code, options) {
  return http.get(`/orders/me/${encodeURIComponent(code)}`, options);
}
