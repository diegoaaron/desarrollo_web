import { useEffect, useMemo, useState } from "react";
import { quoteLines } from "../api/quote-api";
import { toLineRequest } from "../model/cart-line";

const QUOTE_DELAY_MS = 300;

// Cotiza las líneas en el servidor cada vez que cambian (con una pequeña espera para no
// disparar una petición por tecla). Mientras llega la nueva, se muestra la última cotización.
export function useQuote(lines) {
  const [result, setResult] = useState({ key: null, quote: null, error: null });

  // La clave cambia solo cuando cambia lo que se envía, no con cada render.
  const requestKey = useMemo(() => JSON.stringify(lines.map(toLineRequest)), [lines]);
  const empty = lines.length === 0;

  useEffect(() => {
    if (empty) return undefined;

    const controller = new AbortController();
    const timer = window.setTimeout(() => {
      quoteLines(JSON.parse(requestKey), { signal: controller.signal })
        .then((quote) => setResult({ key: requestKey, quote, error: null }))
        .catch((error) => {
          if (error.name !== "AbortError") setResult((current) => ({ ...current, key: requestKey, error: error.message }));
        });
    }, QUOTE_DELAY_MS);

    return () => {
      window.clearTimeout(timer);
      controller.abort();
    };
  }, [requestKey, empty]);

  if (empty) return { quote: null, error: null, isLoading: false };
  return {
    quote: result.quote,
    error: result.key === requestKey ? result.error : null,
    isLoading: result.key !== requestKey,
  };
}
