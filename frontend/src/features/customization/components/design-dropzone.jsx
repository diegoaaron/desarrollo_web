import { CheckCircle2, ImagePlus, Loader2, LogIn, X } from "lucide-react";
import { useRef, useState } from "react";
import { Link, useLocation } from "react-router";
import { DESIGN_TYPES } from "../model/design-file";

export function DesignDropzone({ upload, isSignedIn }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);
  const location = useLocation();
  const { previewUrl, fileName, design, uploading, error, hasLocalOnly, selectFile, clear } = upload;

  function handleFiles(files) {
    const file = files?.[0];
    if (file) selectFile(file);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div>
      <div
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          handleFiles(event.dataTransfer.files);
        }}
        className={`flex flex-col items-center gap-3 rounded-2xl border-2 border-dashed px-5 py-6 text-center transition ${
          dragging ? "border-[#ff5331] bg-[#fff0eb]" : "border-stone-300 bg-stone-50"
        }`}
      >
        {previewUrl ? (
          <div className="flex w-full items-center gap-4 text-left">
            <img src={previewUrl} alt="" className="h-16 w-16 shrink-0 rounded-xl border border-stone-200 bg-white object-contain p-1" />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-bold text-slate-900">{fileName ?? "Tu diseño"}</p>
              {uploading ? (
                <p className="mt-1 inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500">
                  <Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" /> Subiendo…
                </p>
              ) : design ? (
                <p className="mt-1 inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700">
                  <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" /> Diseño guardado
                </p>
              ) : hasLocalOnly ? (
                <p className="mt-1 text-xs font-semibold text-amber-700">Solo vista previa: inicia sesión para guardarlo</p>
              ) : null}
            </div>
            <button
              type="button"
              onClick={clear}
              className="grid h-9 w-9 shrink-0 place-items-center rounded-full text-slate-400 hover:bg-red-50 hover:text-red-600"
              aria-label="Quitar el diseño"
            >
              <X className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        ) : (
          <>
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-white text-[#ff5331] shadow-sm">
              <ImagePlus className="h-6 w-6" aria-hidden="true" />
            </span>
            <p className="text-sm font-semibold text-slate-700">Arrastra tu imagen aquí</p>
            <p className="text-xs text-slate-500">PNG o JPG, hasta 5 MB. Mejor con fondo transparente.</p>
          </>
        )}
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="rounded-xl border border-stone-200 bg-white px-4 py-2 text-sm font-bold text-slate-700 hover:border-[#ff5331] hover:text-[#e94727] disabled:opacity-50"
        >
          {previewUrl ? "Cambiar imagen" : "Elegir archivo"}
        </button>
        <input
          ref={inputRef}
          type="file"
          accept={DESIGN_TYPES.join(",")}
          className="sr-only"
          aria-label="Subir diseño"
          onChange={(event) => handleFiles(event.target.files)}
        />
      </div>

      {error ? <p role="alert" className="mt-2 text-sm font-semibold text-red-600">{error}</p> : null}

      {!isSignedIn ? (
        <p className="mt-3 flex flex-wrap items-center gap-1.5 text-xs text-slate-500">
          <LogIn className="h-3.5 w-3.5" aria-hidden="true" />
          Para guardar tu diseño y comprarlo,
          <Link
            to="/login"
            state={{ from: `${location.pathname}${location.search}` }}
            className="font-bold text-[#e94727] hover:underline"
          >
            inicia sesión
          </Link>
          . Tus elecciones se conservan; solo tendrás que volver a elegir la imagen.
        </p>
      ) : null}
    </div>
  );
}
