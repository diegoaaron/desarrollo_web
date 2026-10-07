const PRODUCTS_API_URL = "/api/products";

async function requestProducts(endpoint = "", { signal } = {}) {
  const response = await fetch(`${PRODUCTS_API_URL}${endpoint}`, { signal });

  if (!response.ok) {
    throw new Error(`No se pudieron cargar los productos (${response.status})`);
  }

  return response.json();
}

export function getProducts(options) {
  return requestProducts("", options);
}

export function getProduct(id, options) {
  return requestProducts(`/${encodeURIComponent(id)}`, options);
}
