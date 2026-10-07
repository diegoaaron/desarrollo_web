const PRODUCTS_API_URL = "/api/products";

async function requestProducts(endpoint = "", { signal } = {}) {
  const response = await fetch(`${PRODUCTS_API_URL}${endpoint}`, { signal });

  if (!response.ok) {
    throw new Error(`No se pudieron cargar los productos (${response.status})`);
  }

  return response.json();
}

// La API pagina el catálogo; mientras el filtrado siga en el navegador (fase 3), se pide la página máxima.
export async function getProducts(options) {
  const page = await requestProducts("?size=100", options);
  return page.items;
}

export function getProduct(id, options) {
  return requestProducts(`/${encodeURIComponent(id)}`, options);
}
