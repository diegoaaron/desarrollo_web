import { http } from "../../../shared/api/http-client";
import { toLineRequest } from "../../cart/model/cart-line";

export const addressesApi = {
  list: (options) => http.get("/addresses", options),
  create: (address) => http.post("/addresses", address),
  update: (id, address) => http.put(`/addresses/${id}`, address),
  remove: (id) => http.delete(`/addresses/${id}`),
};

export function getShippingMethods(options) {
  return http.get("/shipping-methods", options);
}

export function createOrder({ lines, addressId, shippingMethodCode, contactPhone, customerNote }) {
  return http.post("/orders", {
    lines: lines.map(toLineRequest),
    addressId: addressId ?? null,
    shippingMethodCode,
    contactPhone: contactPhone || null,
    customerNote: customerNote || null,
  });
}

export function payOrder(orderCode, card) {
  return http.post(`/orders/${encodeURIComponent(orderCode)}/payment`, card);
}
