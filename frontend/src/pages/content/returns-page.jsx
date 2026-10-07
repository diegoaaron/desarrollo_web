import { CheckCircle2, PackageOpen, RefreshCcw, RotateCcw } from "lucide-react";
import { Link } from "react-router";
import { ContentCard, ContentPage } from "./components/content-page";

const RETURN_STEPS = [
  ["01", "Inicia tu solicitud", "Escribe a nuestro equipo de atención con tu número de pedido y los productos que deseas devolver."],
  ["02", "Empaca con cuidado", "Coloca los productos sin usar en su empaque original e incluye la boleta o la guía de remisión."],
  ["03", "Envíalo de vuelta", "Usa un servicio de envío con seguimiento y conserva tu comprobante hasta que la devolución concluya."],
  ["04", "Recibe tu reembolso", "Tras la revisión, el reembolso se emite al mismo medio de pago que usaste."],
];

export function ReturnsPage() {
  return (
    <ContentPage
      eyebrow="Atención al cliente"
      title="Devoluciones sin complicaciones"
      description="Tienes 30 días para decidir. Queremos que cada compra en Coral te deje completamente satisfecho."
      icon={RotateCcw}
    >
      <div className="grid gap-6 lg:grid-cols-[1fr_20rem]">
        <ContentCard className="p-5 sm:p-8">
          <h2 className="text-2xl font-black tracking-tight text-slate-950">
            Cómo devolver un producto
          </h2>
          <ol className="mt-7 grid gap-4 sm:grid-cols-2">
            {RETURN_STEPS.map(([number, title, text]) => (
              <li key={number} className="rounded-2xl border border-stone-200 bg-stone-50 p-5">
                <span className="text-xs font-black tracking-widest text-[#e94727]">{number}</span>
                <h3 className="mt-2 font-black text-slate-900">{title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-500">{text}</p>
              </li>
            ))}
          </ol>
        </ContentCard>

        <div className="space-y-5">
          <ContentCard className="p-6">
            <span className="grid h-11 w-11 place-items-center rounded-2xl bg-emerald-50 text-emerald-700">
              <CheckCircle2 className="h-5 w-5" aria-hidden="true" />
            </span>
            <h2 className="mt-4 text-lg font-black text-slate-900">Condiciones para aceptar la devolución</h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Los productos deben estar sin usar y devolverse en su empaque original.
            </p>
          </ContentCard>
          <ContentCard className="p-6">
            <span className="grid h-11 w-11 place-items-center rounded-2xl bg-[#fff0eb] text-[#ff5331]">
              <RefreshCcw className="h-5 w-5" aria-hidden="true" />
            </span>
            <h2 className="mt-4 text-lg font-black text-slate-900">Plazo del reembolso</h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              El reembolso se inicia después de la revisión. El tiempo de procesamiento depende de cada banco.
            </p>
          </ContentCard>
        </div>
      </div>

      <div className="mt-6 flex flex-col items-center justify-between gap-4 rounded-[1.75rem] bg-slate-950 p-6 text-center text-white sm:flex-row sm:text-left">
        <div className="flex items-center gap-4">
          <PackageOpen className="hidden h-7 w-7 shrink-0 text-[#ff7354] sm:block" aria-hidden="true" />
          <div>
            <h2 className="font-black">¿Listo para iniciar una devolución?</h2>
            <p className="mt-1 text-sm text-slate-300">Ten a la mano tu número de pedido.</p>
          </div>
        </div>
        <Link
          to="/contact-us"
          className="inline-flex min-h-11 shrink-0 items-center justify-center rounded-xl bg-[#ff5331] px-5 py-3 text-sm font-bold transition hover:bg-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
        >
          Contactar a atención al cliente
        </Link>
      </div>
    </ContentPage>
  );
}
