import { HeartHandshake, Sparkles, Store, UsersRound } from "lucide-react";
import {
  ContentCard,
  ContentPage,
  SectionHeading,
} from "./components/content-page";

const MILESTONES = [
  ["2018", "Una pequeña idea", "Coral nació como una tienda de barrio en Lima, enfocada en prendas con significado y hechas a mano."],
  ["2021", "Una comunidad más grande", "Diseñadores y talleres independientes se sumaron a nuestra creciente red creativa."],
  ["Hoy", "Hecho para importar", "Seguimos conectando a clientes exigentes con prendas que cuentan una historia humana."],
];

export function OurStoryPage() {
  return (
    <ContentPage
      eyebrow="Nuestros orígenes"
      title="Cada prenda empieza con una persona"
      description="Coral nació para celebrar a los creadores independientes, los materiales duraderos y las prendas con una historia que vale la pena compartir."
      icon={Store}
    >
      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <ContentCard className="p-6 sm:p-8 lg:p-10">
          <SectionHeading
            eyebrow="Por qué empezamos"
            title="Una forma de comprar más pausada y personal"
          />
          <div className="space-y-5 text-sm leading-7 text-slate-600 sm:text-base">
            <p>
              Fundada con pasión por las prendas únicas y hechas a mano, Coral
              empezó como una pequeña tienda. Buscamos creadores talentosos y
              materiales bonitos y sostenibles para ofrecerte prendas que
              cuentan una historia.
            </p>
            <p>
              Hoy nuestra misión sigue siendo simple: apoyar a los creadores
              independientes y ofrecer polos, poleras, gorras y tote bags que
              puedes personalizar y que no encontrarás en ningún otro lugar.
            </p>
          </div>
          <div className="mt-8 grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl bg-[#fff0eb] p-5">
              <HeartHandshake className="h-6 w-6 text-[#ff5331]" aria-hidden="true" />
              <p className="mt-3 font-black text-slate-900">Primero los creadores</p>
              <p className="mt-1 text-sm text-slate-500">Alianzas justas pensadas para durar.</p>
            </div>
            <div className="rounded-2xl bg-stone-100 p-5">
              <UsersRound className="h-6 w-6 text-slate-700" aria-hidden="true" />
              <p className="mt-3 font-black text-slate-900">Impulsado por la comunidad</p>
              <p className="mt-1 text-sm text-slate-500">Seleccionado pensando en las personas.</p>
            </div>
          </div>
        </ContentCard>

        <ContentCard className="p-6 sm:p-8">
          <SectionHeading eyebrow="Nuestro camino" title="Creciendo con intención" />
          <ol className="relative space-y-7 border-l border-[#ff5331]/20 pl-7">
            {MILESTONES.map(([year, title, text]) => (
              <li key={year} className="relative">
                <span className="absolute -left-[2.12rem] top-1 h-3 w-3 rounded-full border-2 border-white bg-[#ff5331] shadow" />
                <p className="text-xs font-black uppercase tracking-widest text-[#e94727]">
                  {year}
                </p>
                <h3 className="mt-1 text-lg font-black text-slate-900">{title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-500">{text}</p>
              </li>
            ))}
          </ol>
          <div className="mt-8 flex items-center gap-3 rounded-2xl border border-stone-200 bg-stone-50 p-4">
            <Sparkles className="h-5 w-5 shrink-0 text-[#ff5331]" aria-hidden="true" />
            <p className="text-sm font-semibold text-slate-600">
              El mejor capítulo siempre es el que escribimos a continuación.
            </p>
          </div>
        </ContentCard>
      </div>
    </ContentPage>
  );
}
