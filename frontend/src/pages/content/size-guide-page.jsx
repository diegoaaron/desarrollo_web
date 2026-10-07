import { Info, Ruler } from "lucide-react";
import { ContentCard, ContentPage } from "./components/content-page";

const SIZES = [
  ["Pequeña (S)", "4–6", "86–89", "66–69", "91–94"],
  ["Mediana (M)", "8–10", "91–94", "71–74", "97–99"],
  ["Grande (L)", "12–14", "98–102", "77–81", "103–107"],
  ["Extra grande (XL)", "16–18", "105–109", "85–89", "110–114"],
];

export function SizeGuidePage() {
  return (
    <ContentPage
      eyebrow="Calce y medidas"
      title="Encuentra la talla ideal para ti"
      description="Usa estas medidas como guía general. Cada producto puede incluir indicaciones de calce más específicas."
      icon={Ruler}
    >
      <ContentCard className="mx-auto max-w-5xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[42rem] text-left">
            <caption className="sr-only">Medidas de las tallas de Coral en centímetros</caption>
            <thead className="bg-slate-950 text-white">
              <tr>
                {['Talla', 'Equivalencia EE. UU.', 'Busto (cm)', 'Cintura (cm)', 'Cadera (cm)'].map((heading) => (
                  <th key={heading} scope="col" className="px-5 py-4 text-xs font-black uppercase tracking-wider sm:px-6">
                    {heading}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-200">
              {SIZES.map((size) => (
                <tr key={size[0]} className="transition-colors hover:bg-[#fff8f4]">
                  {size.map((value, index) => (
                    <td
                      key={`${size[0]}-${index}`}
                      className={`px-5 py-5 text-sm sm:px-6 ${index === 0 ? 'font-black text-slate-900' : 'font-medium text-slate-500'}`}
                    >
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ContentCard>

      <div className="mx-auto mt-6 flex max-w-5xl items-start gap-4 rounded-2xl border border-[#ff5331]/15 bg-[#fff0eb] p-5">
        <Info className="mt-0.5 h-5 w-5 shrink-0 text-[#ff5331]" aria-hidden="true" />
        <div>
          <h2 className="font-black text-slate-900">Cómo medirte</h2>
          <p className="mt-1 text-sm leading-6 text-slate-600">
            Mantén la cinta métrica nivelada y cómodamente pegada al cuerpo. Si
            estás entre dos tallas, elige la más grande para un calce más holgado.
          </p>
        </div>
      </div>
    </ContentPage>
  );
}
