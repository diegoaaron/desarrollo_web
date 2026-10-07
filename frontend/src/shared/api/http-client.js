// Cliente HTTP único de la tienda y del panel. La sesión viaja en la cookie (mismo origen
// gracias al proxy de Vite o de Vercel) y toda petición que modifica datos lleva el token CSRF.
const API_BASE_URL = "/api";

export class ApiError extends Error {
  constructor(message, status, errors = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.errors = errors ?? {};
  }
}

async function csrfHeaders() {
  const response = await fetch(`${API_BASE_URL}/auth/csrf`);
  if (!response.ok) throw new ApiError("No se pudo verificar tu sesión. Inténtalo de nuevo.", response.status);
  const { token } = await response.json();
  return { "X-CSRF-TOKEN": token };
}

function fallbackMessage(status) {
  if (status === 401) return "Tu sesión expiró. Vuelve a iniciar sesión.";
  if (status === 403) return "No tienes permiso para realizar esta acción.";
  if (status === 404) return "No encontramos lo que buscabas.";
  if (status === 413) return "El archivo es demasiado grande.";
  return `La solicitud falló (${status})`;
}

async function request(endpoint, { method = "GET", body, signal, headers = {} } = {}) {
  const isForm = body instanceof FormData;
  const config = {
    method,
    signal,
    headers: {
      ...(body !== undefined && !isForm ? { "Content-Type": "application/json" } : {}),
      ...(method !== "GET" ? await csrfHeaders() : {}),
      ...headers,
    },
    body: body === undefined ? undefined : isForm ? body : JSON.stringify(body),
  };

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  } catch (networkError) {
    if (networkError.name === "AbortError") throw networkError;
    throw new ApiError("No pudimos conectar con el servidor. Inténtalo de nuevo.", 0);
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new ApiError(error.message || error.detail || fallbackMessage(response.status), response.status, error.errors);
  }

  if (response.status === 204) return null;
  return response.json();
}

export function queryString(params) {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") search.set(key, value);
  });
  const text = search.toString();
  return text ? `?${text}` : "";
}

export const http = {
  get: (endpoint, options) => request(endpoint, options),
  post: (endpoint, body, options) => request(endpoint, { ...options, method: "POST", body }),
  put: (endpoint, body, options) => request(endpoint, { ...options, method: "PUT", body }),
  patch: (endpoint, body, options) => request(endpoint, { ...options, method: "PATCH", body }),
  delete: (endpoint, options) => request(endpoint, { ...options, method: "DELETE" }),
};
