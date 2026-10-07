export const MAX_DESIGN_BYTES = 5 * 1024 * 1024;
export const DESIGN_TYPES = ["image/png", "image/jpeg"];

// Primera validación en el navegador (D7); el servidor revisa además la cabecera real del archivo.
export function validateDesignFile(file) {
  if (!file) return "Elige una imagen.";
  if (!DESIGN_TYPES.includes(file.type)) return "Solo se aceptan imágenes PNG o JPG.";
  if (file.size > MAX_DESIGN_BYTES) return "La imagen pesa más de 5 MB.";
  if (file.size === 0) return "El archivo está vacío.";
  return null;
}

export function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}
