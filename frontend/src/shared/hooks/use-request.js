import { useCallback, useEffect, useState } from "react";

// Carga datos con `fetcher({ signal })`, que debe ser estable (función de módulo o useCallback):
// cuando cambia, se vuelve a pedir. reload() repite la petición actual.
// El estado de carga se deriva (la respuesta guardada no corresponde a la petición vigente),
// así el efecto solo escribe estado cuando llega la respuesta.
export function useRequest(fetcher) {
  const [version, setVersion] = useState(0);
  const [result, setResult] = useState({ fetcher: null, version: -1, data: null, error: null });

  useEffect(() => {
    const controller = new AbortController();
    fetcher({ signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) setResult({ fetcher, version, data, error: null });
      })
      .catch((error) => {
        if (error.name !== "AbortError" && !controller.signal.aborted) {
          setResult((current) => ({ fetcher, version, data: current.data, error }));
        }
      });
    return () => controller.abort();
  }, [fetcher, version]);

  const isLoading = result.fetcher !== fetcher || result.version !== version;
  const reload = useCallback(() => setVersion((value) => value + 1), []);
  const setData = useCallback((update) => {
    setResult((current) => ({
      ...current,
      data: typeof update === "function" ? update(current.data) : update,
    }));
  }, []);

  return {
    data: result.data,
    setData,
    error: isLoading ? null : result.error,
    isLoading,
    reload,
  };
}
