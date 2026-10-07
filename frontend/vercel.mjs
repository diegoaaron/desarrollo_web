// Configuración de Vercel. Reemplaza a vercel.json: Vercel ejecuta este archivo al
// desplegar, así que la URL del backend sale de una variable de entorno del proyecto en
// Vercel y no queda escrita en el repositorio.
//
// Variable obligatoria en Vercel (Settings → Environment Variables):
//   BACKEND_URL = URL pública del backend, sin "/api" al final (https://api.ejemplo.com)
//
// El navegador llama siempre a /api/... en el mismo dominio del frontend y Vercel reenvía
// la petición al backend. Así la cookie de sesión (JSESSIONID) y el token CSRF funcionan
// como en local, sin configurar CORS ni cookies de terceros.

function backendUrl() {
  const value = process.env.BACKEND_URL?.trim().replace(/\/+$/, "");
  if (!value) {
    throw new Error("Falta la variable BACKEND_URL en el proyecto de Vercel (URL pública del backend).");
  }
  if (!/^https:\/\/[^/]+/.test(value)) {
    throw new Error(`BACKEND_URL debe ser una URL https:// (se recibió «${value}»).`);
  }
  return value.replace(/\/api$/, "");
}

export const config = {
  rewrites: [
    { source: "/api/:path*", destination: `${backendUrl()}/api/:path*` },
    // Aplicación de una sola página: toda otra ruta la resuelve React Router.
    { source: "/(.*)", destination: "/index.html" },
  ],
  headers: [
    {
      // Las respuestas de la API dependen de la sesión: nunca se guardan en la caché de Vercel.
      source: "/api/:path*",
      headers: [{ key: "x-vercel-enable-rewrite-caching", value: "0" }],
    },
  ],
};
