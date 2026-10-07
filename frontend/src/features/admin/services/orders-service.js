import { api } from "./api";

export const ordersService = {
  // La bandeja está paginada en la API; por ahora se muestra la página máxima (100 pedidos).
  getAll: () => api.get("/orders?size=100").then((page) => page.items),
  updateStatus: (id, status) => api.put(`/orders/${id}/status`, { status }),
};
