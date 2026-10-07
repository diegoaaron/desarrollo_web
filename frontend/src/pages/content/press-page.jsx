import { ArrowUpRight, Mail, Newspaper } from "lucide-react";
import { ContentCard, ContentPage } from "./components/content-page";

const RELEASES = [
  {
    date: "12 de octubre de 2026",
    type: "Nota de prensa",
    title: "Coral Shop presenta su nueva colección de primavera",
    description:
      "Nuestra colección más reciente reúne colores vibrantes, siluetas atemporales y materiales de origen ético.",
  },
  {
    date: "5 de septiembre de 2026",
    type: "En los medios",
    title: "Destacados en la edición artesanal de Vogue",
    description:
      "El compromiso de Coral con los artesanos independientes fue destacado en la edición especial de Vogue.",
  },
  {
    date: "18 de julio de 2026",
    type: "Noticias de la empresa",
    title: "Un nuevo hito para nuestra comunidad de creadores",
    description:
      "Más de cien talleres independientes ya comparten su trabajo a través de la tienda Coral.",
  },
];

export function PressPage() {
  return (
    <ContentPage
      eyebrow="Prensa y noticias"
      title="Lo último de Coral"
      description="Novedades de la empresa, lanzamientos de colecciones e historias de toda nuestra comunidad."
      icon={Newspaper}
    >
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <ContentCard className="divide-y divide-stone-200/80 overflow-hidden">
          {RELEASES.map((release) => (
            <article key={release.title} className="p-5 sm:p-7">
              <div className="flex flex-wrap items-center gap-2 text-xs font-bold uppercase tracking-wider">
                <span className="text-[#e94727]">{release.type}</span>
                <span className="text-stone-300" aria-hidden="true">•</span>
                <time className="text-slate-400">{release.date}</time>
              </div>
              <h2 className="mt-3 text-xl font-black tracking-tight text-slate-950 sm:text-2xl">
                {release.title}
              </h2>
              <p className="mt-3 text-sm leading-6 text-slate-500 sm:text-base">
                {release.description}
              </p>
              <p className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[#e94727]">
                Nota completa próximamente
                <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
              </p>
            </article>
          ))}
        </ContentCard>

        <ContentCard className="h-fit bg-slate-950 p-6 text-white lg:sticky lg:top-48">
          <span className="grid h-12 w-12 place-items-center rounded-2xl bg-white/10 text-[#ff7354]">
            <Mail className="h-5 w-5" aria-hidden="true" />
          </span>
          <h2 className="mt-5 text-xl font-black">Consultas de prensa</h2>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            ¿Buscas material de marca, entrevistas o más información sobre Coral?
          </p>
          <a
            href="mailto:prensa@coralshop.pe"
            className="mt-6 inline-flex min-h-11 w-full items-center justify-center rounded-xl bg-[#ff5331] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            prensa@coralshop.pe
          </a>
        </ContentCard>
      </div>
    </ContentPage>
  );
}
