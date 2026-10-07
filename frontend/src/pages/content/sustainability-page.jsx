import { Earth, Leaf, PackageCheck, Recycle, Scale } from "lucide-react";
import { ContentCard, ContentPage } from "./components/content-page";

const COMMITMENTS = [
  {
    title: "Abastecimiento ético",
    description:
      "Trabajamos con talleres que garantizan salarios justos, condiciones seguras y cadenas de suministro transparentes.",
    icon: Scale,
  },
  {
    title: "Mejores materiales",
    description:
      "Priorizamos fibras de cultivo orgánico, tintes de bajo impacto y materiales resistentes pensados para durar.",
    icon: Leaf,
  },
  {
    title: "Empaques conscientes",
    description:
      "Nuestros empaques son reciclables o compostables, y usamos menos material en cada envío.",
    icon: PackageCheck,
  },
];

export function SustainabilityPage() {
  return (
    <ContentPage
      eyebrow="Nuestro compromiso"
      title="Lo bonito también debe respetar el planeta"
      description="Construimos una tienda más responsable a través de mejores alianzas, mejores materiales y decisiones del día a día."
      icon={Earth}
    >
      <div className="grid gap-5 md:grid-cols-3">
        {COMMITMENTS.map((commitment) => {
          const Icon = commitment.icon;
          return (
            <ContentCard key={commitment.title} className="p-6 sm:p-7">
              <span className="grid h-12 w-12 place-items-center rounded-2xl bg-emerald-50 text-emerald-700">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
              <h2 className="mt-5 text-xl font-black tracking-tight text-slate-950">
                {commitment.title}
              </h2>
              <p className="mt-3 text-sm leading-6 text-slate-500">
                {commitment.description}
              </p>
            </ContentCard>
          );
        })}
      </div>

      <ContentCard className="mt-6 overflow-hidden bg-emerald-950 text-white">
        <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-[1fr_auto] lg:items-center lg:p-10">
          <div className="max-w-2xl">
            <p className="text-xs font-black uppercase tracking-[0.18em] text-emerald-300">
              Progreso, no perfección
            </p>
            <h2 className="mt-3 text-2xl font-black tracking-tight sm:text-3xl">
              Cada pedido es una oportunidad para hacerlo un poco mejor
            </h2>
            <p className="mt-3 text-sm leading-6 text-emerald-100/75 sm:text-base">
              Medimos constantemente nuestra huella y trabajamos con nuestra
              comunidad de creadores para reducir residuos sin sacrificar la calidad.
            </p>
          </div>
          <div className="flex items-center gap-4 rounded-2xl bg-white/10 p-5 backdrop-blur">
            <Recycle className="h-9 w-9 text-emerald-300" aria-hidden="true" />
            <div>
              <p className="text-3xl font-black">100%</p>
              <p className="text-sm text-emerald-100/70">empaques reciclables</p>
            </div>
          </div>
        </div>
      </ContentCard>
    </ContentPage>
  );
}
