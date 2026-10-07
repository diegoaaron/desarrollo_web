import { Shirt } from "lucide-react";
import { useState } from "react";

// Miniatura de una línea: el diseño del cliente sobre el color elegido o, sin diseño, la foto del producto.
export function CartLineThumb({ line, className = "h-24 w-24" }) {
  const [failed, setFailed] = useState(false);
  const src = line.designImageUrl ?? line.image;
  const colors = [...new Set(line.items.map((item) => item.colorHex).filter(Boolean))];

  return (
    <div
      className={`relative grid shrink-0 place-items-center overflow-hidden rounded-xl border border-stone-200 p-2 ${className}`}
      style={{ backgroundColor: line.designImageUrl ? colors[0] ?? "#fafaf9" : "#fafaf9" }}
    >
      {src && !failed ? (
        <img src={src} alt="" className="h-full w-full object-contain" onError={() => setFailed(true)} />
      ) : (
        <Shirt className="h-1/2 w-1/2 text-stone-300" aria-hidden="true" />
      )}
      {colors.length > 1 ? (
        <span className="absolute bottom-1 right-1 flex -space-x-1">
          {colors.slice(0, 3).map((hex) => (
            <span key={hex} className="h-3 w-3 rounded-full border border-white" style={{ backgroundColor: hex }} />
          ))}
        </span>
      ) : null}
    </div>
  );
}
