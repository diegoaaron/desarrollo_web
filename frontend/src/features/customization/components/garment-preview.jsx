import { useId } from "react";
import { VIEW_LABELS, viewForZone } from "../model/garment-views";

// Siluetas en un lienzo de 100 × 100: así las coordenadas preview_* de la base de datos
// (porcentajes de la imagen) se usan tal cual como x, y, ancho y alto del SVG.
const SILHOUETTES = {
  POLO: {
    front: {
      body: "M36 10 Q50 19 64 10 L78 14 L94 30 L84 40 L76 34 L76 92 L24 92 L24 34 L16 40 L6 30 L22 14 Z",
      details: ["M36 10 Q50 19 64 10", "M24 88 L76 88", "M84 40 L94 30", "M6 30 L16 40"],
    },
    back: {
      body: "M36 10 Q50 14 64 10 L78 14 L94 30 L84 40 L76 34 L76 92 L24 92 L24 34 L16 40 L6 30 L22 14 Z",
      details: ["M36 10 Q50 14 64 10", "M24 88 L76 88"],
    },
  },
  POLERA: {
    front: {
      body: "M38 12 Q50 22 62 12 L76 16 Q86 20 90 32 L95 78 L84 80 L77 40 L76 90 L24 90 L23 40 L16 80 L5 78 L10 32 Q14 20 24 16 Z",
      details: ["M38 12 Q50 22 62 12", "M34 70 L66 70 L70 84 L30 84 Z", "M24 86 L76 86", "M5 74 L16 76", "M95 74 L84 76", "M46 18 L45 30", "M54 18 L55 30"],
      extra: "M36 13 Q38 2 50 2 Q62 2 64 13 Q50 20 36 13 Z",
    },
    back: {
      body: "M38 12 Q50 16 62 12 L76 16 Q86 20 90 32 L95 78 L84 80 L77 40 L76 90 L24 90 L23 40 L16 80 L5 78 L10 32 Q14 20 24 16 Z",
      details: ["M24 86 L76 86", "M5 74 L16 76", "M95 74 L84 76"],
      extra: "M34 14 Q34 0 50 0 Q66 0 66 14 Q66 22 50 22 Q34 22 34 14 Z",
    },
  },
  GORRA: {
    front: {
      body: "M14 62 Q14 14 50 14 Q88 14 88 62 Z",
      details: ["M50 14 L50 62", "M30 20 Q34 40 32 62", "M70 20 Q66 40 68 62"],
      extra: "M10 62 Q50 50 90 62 Q94 76 50 78 Q6 76 10 62 Z",
      button: true,
    },
  },
  TOTE: {
    front: {
      body: "M16 28 L84 28 L86 92 L14 92 Z",
      details: ["M16 32 L84 32"],
      handles: true,
    },
    back: {
      body: "M16 28 L84 28 L86 92 L14 92 Z",
      details: ["M16 32 L84 32"],
      handles: true,
    },
  },
};

function isLight(hex) {
  const value = String(hex ?? "").replace("#", "");
  if (value.length !== 6) return true;
  const [r, g, b] = [0, 2, 4].map((index) => parseInt(value.slice(index, index + 2), 16));
  return r * 0.299 + g * 0.587 + b * 0.114 > 160;
}

export function GarmentPreview({ productTypeCode, colorHex, view, zones, designUrl, techniqueCode }) {
  const gradientId = useId();
  const shape = SILHOUETTES[productTypeCode]?.[view] ?? SILHOUETTES.POLO.front;
  const fill = colorHex || "#f5f5f4";
  const stroke = isLight(fill) ? "#94a3b8" : "rgba(255,255,255,0.35)";
  const visibleZones = zones.filter((zone) => viewForZone(zone.code) === view);
  const embroidered = techniqueCode === "BORDADO";

  return (
    <figure className="relative">
      <svg viewBox="0 0 100 100" className="h-auto w-full" role="img" aria-label={`Vista previa: ${VIEW_LABELS[view]}`}>
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ffffff" stopOpacity="0.18" />
            <stop offset="1" stopColor="#000000" stopOpacity="0.12" />
          </linearGradient>
        </defs>

        {shape.handles ? (
          <g fill="none" stroke={fill} strokeWidth="3.2" strokeLinecap="round">
            <path d="M30 29 Q30 4 42 4 Q48 4 48 29" />
            <path d="M52 29 Q52 4 58 4 Q70 4 70 29" />
          </g>
        ) : null}
        {shape.extra && productTypeCode === "POLERA" ? (
          <path d={shape.extra} fill={fill} stroke={stroke} strokeWidth="0.5" />
        ) : null}
        <path d={shape.body} fill={fill} stroke={stroke} strokeWidth="0.6" strokeLinejoin="round" />
        <path d={shape.body} fill={`url(#${gradientId})`} />
        {shape.details.map((detail) => (
          <path key={detail} d={detail} fill="none" stroke={stroke} strokeWidth="0.4" strokeDasharray="1 0.8" />
        ))}
        {shape.extra && productTypeCode === "GORRA" ? (
          <path d={shape.extra} fill={fill} stroke={stroke} strokeWidth="0.6" />
        ) : null}
        {shape.button ? <circle cx="50" cy="14" r="1.6" fill={fill} stroke={stroke} strokeWidth="0.4" /> : null}

        {visibleZones.map((zone) => {
          const { x, y, width, height } = zone.preview;
          return (
            <g key={zone.code}>
              {designUrl ? (
                <image
                  href={designUrl}
                  x={x}
                  y={y}
                  width={width}
                  height={height}
                  preserveAspectRatio="xMidYMid meet"
                  style={embroidered ? { filter: "saturate(1.25) contrast(1.1)" } : undefined}
                />
              ) : null}
              <rect
                x={x}
                y={y}
                width={width}
                height={height}
                fill={designUrl ? "none" : "rgba(255,83,49,0.08)"}
                stroke="#ff5331"
                strokeWidth="0.35"
                strokeDasharray="1.2 0.8"
                rx="0.6"
              />
            </g>
          );
        })}
      </svg>
      <figcaption className="mt-2 text-center text-xs font-bold uppercase tracking-[0.16em] text-slate-400">
        {VIEW_LABELS[view]}
      </figcaption>
    </figure>
  );
}
