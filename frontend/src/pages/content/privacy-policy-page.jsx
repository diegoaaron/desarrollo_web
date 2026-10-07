import { ShieldCheck } from "lucide-react";
import { ContentPage } from "./components/content-page";
import { LegalDocument } from "./components/legal-document";

const PRIVACY_SECTIONS = [
  {
    title: "Información que recopilamos",
    content:
      "Recopilamos la información que nos proporcionas directamente, como tu nombre, correo electrónico, dirección de envío, datos de pago y los detalles que compartes al contactar a nuestro equipo o crear una cuenta.",
  },
  {
    title: "Cómo usamos tu información",
    content:
      "Usamos esta información para procesar transacciones, informarte sobre el estado de tus pedidos, responder tus consultas, dar soporte a tu cuenta, mejorar nuestros servicios y enviarte comunicaciones comerciales cuando nos hayas dado tu consentimiento.",
  },
  {
    title: "Información compartida con terceros",
    content:
      "No vendemos ni intercambiamos tu información personal. Podemos compartir la información necesaria con proveedores de confianza que nos ayudan a operar la tienda y que se comprometen a proteger su confidencialidad.",
  },
  {
    title: "Seguridad de los datos",
    content:
      "Aplicamos medidas técnicas y organizativas adecuadas para proteger la información personal. El acceso se limita a las personas autorizadas que la necesitan para prestar nuestros servicios.",
  },
  {
    title: "Cookies",
    content:
      "Las cookies nos ayudan a recordar tus preferencias, entender cómo se usa la tienda y mejorar tu experiencia. Puedes administrarlas o desactivarlas desde la configuración de tu navegador.",
  },
  {
    title: "Tus derechos",
    content:
      "Puedes solicitar el acceso, la rectificación o la eliminación de tu información personal. También puedes darte de baja de los correos comerciales en cualquier momento mediante el enlace incluido en cada mensaje.",
  },
];

export function PrivacyPolicyPage() {
  return (
    <ContentPage
      eyebrow="Legal"
      title="Tu privacidad, explicada con claridad"
      description="Última actualización: septiembre de 2026. Esta política explica qué datos recopilamos, para qué los usamos y qué opciones tienes."
      icon={ShieldCheck}
    >
      <LegalDocument
        sections={PRIVACY_SECTIONS}
        contactEmail="privacidad@coralshop.pe"
      />
    </ContentPage>
  );
}
