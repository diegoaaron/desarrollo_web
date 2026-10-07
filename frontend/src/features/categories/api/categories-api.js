const CATEGORIES_API_URL = "/api/categories";

let cachedRequest = null;

async function requestCategories() {
  const response = await fetch(CATEGORIES_API_URL);

  if (!response.ok) {
    throw new Error(`No se pudieron cargar las categorías (${response.status})`);
  }

  const data = await response.json();
  return Array.isArray(data) ? data.filter((category) => category?.name) : [];
}

// Header, menú móvil y home piden las categorías a la vez: se comparte una sola petición.
export function getCategories() {
  if (!cachedRequest) {
    cachedRequest = requestCategories().catch((error) => {
      cachedRequest = null;
      throw error;
    });
  }

  return cachedRequest;
}
