import { http } from "../../../shared/api/http-client";

// Cotiza en el servidor (D10): el navegador nunca decide precios ni stock.
// Recibe las líneas ya en formato de la API (ver toLineRequest).
export function quoteLines(lineRequests, options) {
  return http.post("/quotes", { lines: lineRequests }, options);
}
