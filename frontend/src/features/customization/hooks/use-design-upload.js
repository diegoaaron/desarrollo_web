import { useCallback, useEffect, useRef, useState } from "react";
import { uploadDesign } from "../api/customization-api";
import { validateDesignFile } from "../model/design-file";

// Estado del diseño del cliente: vista previa local inmediata y, con sesión iniciada,
// subida al servidor (que devuelve el id que viaja en el carrito y en el pedido). Sin sesión
// la imagen queda solo como vista previa: al volver del login hay que elegirla otra vez.
export function useDesignUpload({ canUpload, initialDesign = null }) {
  const [localUrl, setLocalUrl] = useState(null);
  const [fileName, setFileName] = useState(initialDesign?.originalFilename ?? null);
  const [design, setDesign] = useState(initialDesign);
  const [pendingFile, setPendingFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const localUrlRef = useRef(null);

  const replaceLocalUrl = useCallback((url) => {
    if (localUrlRef.current) URL.revokeObjectURL(localUrlRef.current);
    localUrlRef.current = url;
    setLocalUrl(url);
  }, []);

  useEffect(() => () => {
    if (localUrlRef.current) URL.revokeObjectURL(localUrlRef.current);
  }, []);

  const upload = useCallback(async (file) => {
    setUploading(true);
    setError(null);
    try {
      const saved = await uploadDesign(file);
      setDesign(saved);
      setPendingFile(null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setUploading(false);
    }
  }, []);

  const selectFile = useCallback(
    (file) => {
      const problem = validateDesignFile(file);
      if (problem) {
        setError(problem);
        return;
      }
      setError(null);
      setDesign(null);
      setFileName(file.name);
      replaceLocalUrl(URL.createObjectURL(file));
      if (canUpload) upload(file);
      else setPendingFile(file);
    },
    [canUpload, replaceLocalUrl, upload],
  );

  const clear = useCallback(() => {
    replaceLocalUrl(null);
    setDesign(null);
    setPendingFile(null);
    setFileName(null);
    setError(null);
  }, [replaceLocalUrl]);

  return {
    design,
    previewUrl: localUrl ?? design?.imageUrl ?? null,
    fileName,
    uploading,
    error,
    hasLocalOnly: Boolean(pendingFile),
    selectFile,
    clear,
  };
}
