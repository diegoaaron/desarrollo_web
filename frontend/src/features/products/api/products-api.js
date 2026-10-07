import { http, queryString } from "../../../shared/api/http-client";

// Catálogo paginado y filtrado en el servidor: { items, page, size, totalItems, totalPages }.
export function getProductsPage({ type, categoryId, q, page = 0, size = 12 } = {}, options) {
  return http.get(`/products${queryString({ type, category: categoryId, q, page, size })}`, options);
}

export function getProduct(id, options) {
  return http.get(`/products/${encodeURIComponent(id)}`, options);
}

export function getProductTypes(options) {
  return http.get("/product-types", options);
}
