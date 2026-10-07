import { ChevronDown, CircleHelp, MessageCircle } from "lucide-react";
import { Link } from "react-router";
import { ContentCard, ContentPage } from "./components/content-page";

const QUESTIONS = [
  ["¿Cómo puedo hacer seguimiento a mi pedido?", "Cuando tu pedido sea despachado, recibirás un correo con el número de seguimiento y el enlace a la página del courier."],
  ["¿Hacen envíos a provincias?", "Sí. Enviamos a todo el Perú; la tarifa y el tiempo estimado de entrega se calculan durante el pago según tu departamento, provincia y distrito."],
  ["¿Puedo modificar o cancelar mi pedido?", "Escríbenos lo antes posible. Una vez que el pedido ha sido despachado, ya no es posible modificarlo ni cancelarlo."],
  ["¿Qué medios de pago aceptan?", "Aceptamos tarjetas Visa, Mastercard y American Express, además de Yape y Plin."],
  ["¿Cuánto demora una devolución?", "Las devoluciones suelen revisarse en un plazo de tres días hábiles. Tu banco puede necesitar algunos días adicionales para reflejar el reembolso."],
  ["¿Los productos de Coral se fabrican de forma ética?", "Priorizamos proveedores que ofrecen salarios justos, condiciones de trabajo seguras y prácticas de abastecimiento transparentes."],
];

export function FAQPage() {
  return (
    <ContentPage
      eyebrow="Atención al cliente"
      title="Respuestas, sin tener que buscar"
      description="Las preguntas más comunes sobre pedidos, envíos, devoluciones y compras en Coral."
      icon={CircleHelp}
    >
      <ContentCard className="mx-auto max-w-4xl overflow-hidden divide-y divide-stone-200/80">
        {QUESTIONS.map(([question, answer]) => (
          <details key={question} className="group px-5 py-1 sm:px-7">
            <summary className="flex min-h-18 cursor-pointer list-none items-center gap-4 py-5 font-bold text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] [&::-webkit-details-marker]:hidden">
              <span className="flex-1 text-sm sm:text-base">{question}</span>
              <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-stone-100 text-slate-500 transition group-open:rotate-180 group-open:bg-[#fff0eb] group-open:text-[#ff5331] motion-reduce:transition-none">
                <ChevronDown className="h-4 w-4" aria-hidden="true" />
              </span>
            </summary>
            <p className="max-w-3xl pb-5 pr-10 text-sm leading-6 text-slate-500 sm:text-base sm:leading-7">
              {answer}
            </p>
          </details>
        ))}
      </ContentCard>

      <div className="mx-auto mt-6 flex max-w-4xl flex-col items-center justify-between gap-4 rounded-2xl bg-slate-950 p-5 text-center text-white sm:flex-row sm:text-left">
        <div className="flex items-center gap-3">
          <MessageCircle className="h-5 w-5 shrink-0 text-[#ff7354]" aria-hidden="true" />
          <p className="text-sm font-semibold">¿Aún necesitas ayuda? Nuestro equipo de atención está listo.</p>
        </div>
        <Link
          to="/contact-us"
          className="inline-flex min-h-10 shrink-0 items-center justify-center rounded-xl bg-white px-4 py-2 text-sm font-bold text-slate-950 transition hover:bg-[#ff5331] hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
        >
          Contáctanos
        </Link>
      </div>
    </ContentPage>
  );
}
