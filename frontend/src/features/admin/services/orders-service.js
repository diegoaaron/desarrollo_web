import { queryString } from "../../../shared/api/http-client";
import { api } from "./api";

export const ordersService = {
  getPage: ({ status, page = 0, size = 20 } = {}) => api.get(`/orders${queryString({ status, page, size })}`),
  getById: (id) => api.get(`/orders/${id}`),
  updateStatus: (id, status, comment) => api.put(`/orders/${id}/status`, { status, comment: comment || null }),
};
