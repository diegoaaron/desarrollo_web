import { http } from "../../../shared/api/http-client";

export function getCustomizationOptions(productId, options) {
  return http.get(`/products/${encodeURIComponent(productId)}/customization-options`, options);
}

// Sube la imagen del cliente (PNG o JPG, máx. 5 MB). El servidor vuelve a validar el tipo real.
export function uploadDesign(file) {
  const form = new FormData();
  form.append("file", file);
  return http.post("/designs", form);
}
