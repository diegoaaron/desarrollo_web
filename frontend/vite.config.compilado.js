import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

// Build "todo en uno" para entregar al profesor: genera un solo index.html
// con el JS y el CSS embebidos, sin type="module", para poder abrirlo con
// doble clic (file://) sin depender de un servidor de Vite.
export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss(), viteSingleFile()],
  build: {
    outDir: 'compilado',
    emptyOutDir: true,
    cssCodeSplit: false,
  },
})
