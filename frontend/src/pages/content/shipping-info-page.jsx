import { Clock3, MapPinned, PackageCheck, Plane, Truck } from "lucide-react";
import { ContentCard, ContentPage } from "./components/content-page";

const SHIPPING_OPTIONS = [
  {
    title: "Estándar",
    time: "5–7 días hábiles",
    price: "Tarifa calculada al pagar",
    description: "Nuestra opción de entrega con seguimiento más económica para tus pedidos de siempre.",
    icon: Truck,
  },
  {
    title: "Express",
    time: "2–3 días hábiles",
    price: "Tarifa calculada al pagar",
    description: "Un servicio con seguimiento más rápido para cuando necesitas tu pedido antes.",
    icon: Plane,
  },
  {
    title: "Provincias",
    time: "Según el destino",
    price: "Tarifa calculada al pagar",
    description: "Entregas en todo el Perú, con plazos y tarifas según el departamento, la provincia y el distrito de destino.",
    icon: MapPinned,
  },
];

export function ShippingInfoPage() {
  return (
    <ContentPage
      eyebrow="Guía de envíos"
      title="De nuestro taller a tu puerta"
      description="Opciones de entrega claras, seguimiento confiable y un empaque cuidadoso para cada pedido de Coral."
      icon={PackageCheck}
    >
      <div className="grid gap-5 md:grid-cols-3">
        {SHIPPING_OPTIONS.map((option) => {
          const Icon = option.icon;
          return (
            <ContentCard key={option.title} className="p-6 sm:p-7">
              <span className="grid h-12 w-12 place-items-center rounded-2xl bg-[#fff0eb] text-[#ff5331]">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
              <h2 className="mt-5 text-xl font-black text-slate-950">{option.title}</h2>
              <p className="mt-2 flex items-center gap-2 text-sm font-bold text-slate-700">
                <Clock3 className="h-4 w-4 text-slate-400" aria-hidden="true" />
                {option.time}
              </p>
              <p className="mt-1 text-sm font-bold text-[#e94727]">{option.price}</p>
              <p className="mt-4 text-sm leading-6 text-slate-500">{option.description}</p>
            </ContentCard>
          );
        })}
      </div>

      <ContentCard className="mt-6 overflow-hidden">
        <div className="grid gap-6 p-6 sm:p-8 md:grid-cols-3">
          {[
            ["Seguimiento desde el despacho", "Te enviamos por correo el enlace de seguimiento apenas tu pedido sale de nuestro almacén."],
            ["Empacado con cuidado", "Cada prenda se protege con materiales reciclables o compostables."],
            ["Zonas alejadas", "Los envíos a zonas de difícil acceso pueden requerir días adicionales."],
          ].map(([title, text], index) => (
            <div key={title} className="flex gap-3">
              <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-slate-950 text-xs font-black text-white">
                {index + 1}
              </span>
              <div>
                <h3 className="font-black text-slate-900">{title}</h3>
                <p className="mt-1 text-sm leading-6 text-slate-500">{text}</p>
              </div>
            </div>
          ))}
        </div>
      </ContentCard>
    </ContentPage>
  );
}
