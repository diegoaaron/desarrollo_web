// Reparto de un mismo diseño entre tallas (columnas) y colores (filas), con stock por celda.
export function SizeDistributionTable({ variants, quantities, onChange, highlightColorId }) {
  const sizes = [];
  const colors = [];
  variants.forEach((variant) => {
    if (!sizes.some((size) => size.id === variant.sizeId)) sizes.push({ id: variant.sizeId, name: variant.size });
    if (!colors.some((color) => color.id === variant.colorId)) {
      colors.push({ id: variant.colorId, name: variant.color, hex: variant.colorHex });
    }
  });

  const find = (colorId, sizeId) => variants.find((variant) => variant.colorId === colorId && variant.sizeId === sizeId);

  return (
    <div className="overflow-x-auto rounded-2xl border border-stone-200">
      <table className="w-full min-w-max text-sm">
        <thead className="bg-stone-50 text-xs font-bold uppercase tracking-wider text-slate-500">
          <tr>
            <th scope="col" className="px-3 py-2.5 text-left">Color</th>
            {sizes.map((size) => (
              <th key={size.id} scope="col" className="px-2 py-2.5 text-center">{size.name}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-stone-100">
          {colors.map((color) => (
            <tr key={color.id} className={color.id === highlightColorId ? "bg-[#fff8f5]" : undefined}>
              <th scope="row" className="px-3 py-2 text-left font-semibold text-slate-700">
                <span className="inline-flex items-center gap-2">
                  <span className="h-4 w-4 rounded-full border border-stone-300" style={{ backgroundColor: color.hex ?? "#fff" }} />
                  {color.name}
                </span>
              </th>
              {sizes.map((size) => {
                const variant = find(color.id, size.id);
                if (!variant) return <td key={size.id} className="px-2 py-2 text-center text-slate-300">—</td>;
                const soldOut = variant.stock < 1;
                return (
                  <td key={size.id} className="px-2 py-2 text-center">
                    <input
                      type="number"
                      min="0"
                      max={variant.stock}
                      inputMode="numeric"
                      value={quantities[variant.id] ?? 0}
                      disabled={soldOut}
                      onChange={(event) => {
                        const value = Number.parseInt(event.target.value, 10);
                        onChange(variant.id, Number.isNaN(value) ? 0 : Math.min(Math.max(value, 0), variant.stock));
                      }}
                      onFocus={(event) => event.target.select()}
                      aria-label={`Cantidad talla ${size.name}, color ${color.name} (quedan ${variant.stock})`}
                      className="h-10 w-16 rounded-lg border border-stone-200 bg-white text-center font-bold tabular-nums text-slate-900 outline-none focus:border-[#ff5331] focus:ring-2 focus:ring-[#ff5331]/20 disabled:bg-stone-100 disabled:text-slate-300"
                    />
                    <span className="mt-1 block text-[0.65rem] text-slate-400">{soldOut ? "Agotado" : `quedan ${variant.stock}`}</span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
