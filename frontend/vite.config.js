import { defineConfig, loadEnv } from 'vite'
import { cwd } from 'node:process'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, cwd(), 'API_PROXY_TARGET')
  // Por defecto, el backend local (./mvnw spring-boot:run). Otro destino: API_PROXY_TARGET en .env.local.
  const target = env.API_PROXY_TARGET || 'http://localhost:8082'
  const proxy = {
    '/api': {
      target,
      changeOrigin: true,
    },
  }

  return {
    plugins: [react(), tailwindcss()],
    server: { proxy },
    preview: { proxy },
  }
})
