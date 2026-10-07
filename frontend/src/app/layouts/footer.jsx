import { Link } from "react-router";
import {
  categoryPath,
  useCategories,
} from "../../features/categories/hooks/use-categories";

const STATIC_SECTIONS = [
  {
    id: 2,
    section: "Nosotros",
    links: [
      { id: "au1", name: "Nuestra historia", url: "/our-story" },
      { id: "au2", name: "Trabaja con nosotros", url: "/careers" },
      { id: "au3", name: "Prensa", url: "/press" },
      { id: "au4", name: "Sostenibilidad", url: "/sustainability" },
      { id: "au5", name: "Blog", url: "/blogs" },
    ],
  },
  {
    id: 3,
    section: "Atención al cliente",
    links: [
      { id: "cs1", name: "Contáctanos", url: "/contact-us" },
      { id: "cs2", name: "Información de envío", url: "/shipping-info" },
      { id: "cs3", name: "Cambios y devoluciones", url: "/returns" },
      { id: "cs4", name: "Preguntas frecuentes", url: "/faq" },
      { id: "cs5", name: "Guía de tallas", url: "/size-guide" },
    ],
  },
];

export function Footer() {
  const currentYear = new Date().getFullYear();
  const { categories } = useCategories();
  const footerSections = [
    {
      id: 1,
      section: "Catálogo",
      links: [
        { id: "c-all", name: "Todos los productos", url: "/products" },
        ...categories.map((category) => ({
          id: `c-${category.id ?? category.name}`,
          name: category.name,
          url: categoryPath(category.name),
        })),
        {
          id: "c-price",
          name: "Precio: menor a mayor",
          url: "/products?sort=price-low",
        },
      ],
    },
    ...STATIC_SECTIONS,
  ];

  return (
    <footer className="bg-linear-to-b from-[#101727] to-[#000000] text-gray-400 pt-16 pb-8 border-t border-gray-800">
      <div className="max-w-7xl w-[90%] mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 xl:gap-16 pb-12">
          <div className="lg:col-span-2 flex flex-col gap-4">
            <h2 className="text-white text-2xl font-bold tracking-wider">
              CORAL
            </h2>
            <p className="text-sm leading-relaxed max-w-sm">
              Ropa juvenil con estampado personalizable, hecha en Lima. Diseña
              tu polo, polera, gorra o tote bag y llévalo a cualquier parte del
              Perú.
            </p>
          </div>

          {footerSections.map((group) => (
            <div key={group.id} className="flex flex-col gap-4">
              <h3 className="text-white font-semibold uppercase tracking-wider text-sm">
                {group.section}
              </h3>
              <ul className="space-y-3">
                {group.links.map((link) => (
                  <li key={link.id}>
                    <Link
                      to={link.url}
                      className="text-sm hover:text-coral-400 transition-all hover:translate-x-1 inline-block duration-200"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-800 pt-8 mt-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <p>&copy; {currentYear} Coral Shop S.A.C. Todos los derechos reservados.</p>
          <div className="flex gap-6">
            <Link to="/privacy-policy" className="hover:text-white transition-colors">
              Política de privacidad
            </Link>
            <Link to="/terms-of-service" className="hover:text-white transition-colors">
              Términos del servicio
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
