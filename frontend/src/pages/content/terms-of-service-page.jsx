import { FileCheck2 } from "lucide-react";
import { ContentPage } from "./components/content-page";
import { LegalDocument } from "./components/legal-document";

const TERMS_SECTIONS = [
  {
    title: "Aceptación de los términos",
    content:
      "Al acceder y usar el sitio web y los servicios de Coral Shop, aceptas estos Términos del servicio. Si no estás de acuerdo, te pedimos no utilizar nuestros servicios.",
  },
  {
    title: "Registro de cuenta",
    content:
      "Algunas funciones requieren una cuenta. Eres responsable de mantener la confidencialidad de tus credenciales y de la actividad que se realice desde tu cuenta.",
  },
  {
    title: "Productos y precios",
    content:
      "Procuramos que las descripciones, la disponibilidad y los precios de los productos sean exactos. Nos reservamos el derecho de corregir errores y actualizar la información cuando sea necesario.",
  },
  {
    title: "Pedidos y pagos",
    content:
      "Al realizar un pedido, confirmas que la información proporcionada es correcta. Podemos rechazar o cancelar pedidos por falta de disponibilidad, problemas con el pago o información incorrecta del producto.",
  },
  {
    title: "Envíos y devoluciones",
    content:
      "Las condiciones de entrega y devolución se describen en nuestras páginas de Información de envío y de Cambios y devoluciones. Al completar una compra, aceptas dichas condiciones.",
  },
  {
    title: "Propiedad intelectual",
    content:
      "Los textos, gráficos, la marca y las imágenes de este sitio web pertenecen a Coral Shop o a sus respectivos titulares y no pueden reproducirse sin autorización.",
  },
  {
    title: "Limitación de responsabilidad",
    content:
      "En la medida en que lo permita la ley, Coral Shop no se responsabiliza por daños indirectos, incidentales o consecuentes derivados del uso de nuestros servicios o productos.",
  },
  {
    title: "Cambios en estos términos",
    content:
      "Podemos actualizar estos términos cuando cambien nuestros servicios o nuestras obligaciones legales. El uso continuado tras una actualización implica la aceptación de los términos revisados.",
  },
];

export function TermsOfServicePage() {
  return (
    <ContentPage
      eyebrow="Legal"
      title="Términos pensados para entenderse"
      description="Última actualización: septiembre de 2026. Estos términos describen el acuerdo entre tú y Coral al usar nuestra tienda."
      icon={FileCheck2}
    >
      <LegalDocument
        sections={TERMS_SECTIONS}
        contactEmail="terminos@coralshop.pe"
      />
    </ContentPage>
  );
}
