import {
  ChevronDown,
  CircleHelp,
  Home,
  LayoutGrid,
  LogIn,
  ShieldCheck,
  ShoppingBag,
  X,
} from "lucide-react";
import { useEffect, useRef } from "react";
import { Link, useLocation } from "react-router";
import { useAuth } from "../../features/auth/hooks/use-auth";
import {
  categoryPath,
  useCategories,
} from "../../features/categories/hooks/use-categories";

const HELP_LINKS = [
  { label: "Nuestra historia", to: "/our-story" },
  { label: "Preguntas frecuentes", to: "/faq" },
  { label: "Información de envío", to: "/shipping-info" },
  { label: "Cambios y devoluciones", to: "/returns" },
  { label: "Guía de tallas", to: "/size-guide" },
  { label: "Contáctanos", to: "/contact-us" },
];

const FOCUSABLE_ELEMENTS =
  'a[href], button:not([disabled]), summary, [tabindex]:not([tabindex="-1"])';

export function MobileMenu({ cartItemCount, onClose }) {
  const { account } = useAuth();
  const { categories } = useCategories();
  const categoryLinks = [
    ...categories.map((category) => ({
      label: category.name,
      to: categoryPath(category.name),
    })),
    { label: "Precio: menor a mayor", to: "/products?sort=price-low" },
  ];
  const accountPath = account ? "/account" : "/login";
  const showAdminLink = !account || account.role === "ROLE_ADMIN";
  const location = useLocation();
  const panelRef = useRef(null);
  const closeButtonRef = useRef(null);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    const desktopMedia = window.matchMedia("(min-width: 768px)");
    document.body.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    const handleDesktopChange = (event) => {
      if (event.matches) onClose();
    };

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        onClose();
        return;
      }

      if (event.key !== "Tab") return;

      const focusableElements = panelRef.current?.querySelectorAll(
        FOCUSABLE_ELEMENTS,
      );

      if (!focusableElements?.length) return;

      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    };

    desktopMedia.addEventListener("change", handleDesktopChange);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      desktopMedia.removeEventListener("change", handleDesktopChange);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [onClose]);

  const isCurrentPath = (path) => location.pathname === path;

  return (
    <div className="md:hidden">
      <button
        type="button"
        className="mobile-menu-backdrop fixed inset-0 z-[70] cursor-default bg-slate-950/50 backdrop-blur-[2px]"
        aria-label="Cerrar menú de navegación"
        onClick={onClose}
      />

      <aside
        ref={panelRef}
        id="mobile-navigation"
        className="mobile-menu-panel fixed inset-y-0 left-0 z-[80] flex h-dvh w-[min(88vw,22rem)] flex-col overflow-hidden border-r border-stone-200 bg-[#fffdf9] shadow-[24px_0_70px_-24px_rgba(15,23,42,0.45)]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="mobile-navigation-title"
      >
        <header className="flex items-center justify-between border-b border-stone-200/80 px-5 py-5">
          <Link
            to="/"
            onClick={onClose}
            id="mobile-navigation-title"
            className="text-2xl font-black tracking-tight text-[#ff5331] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331]"
          >
            Coral
          </Link>
          <button
            ref={closeButtonRef}
            type="button"
            className="grid h-11 w-11 place-items-center rounded-full text-slate-500 transition-colors hover:bg-stone-100 hover:text-slate-950 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331]"
            aria-label="Cerrar menú de navegación"
            onClick={onClose}
          >
            <X className="h-5 w-5" aria-hidden="true" />
          </button>
        </header>

        <nav
          className="flex-1 overflow-y-auto overscroll-contain px-4 py-5"
          aria-label="Navegación móvil"
        >
          <p className="mb-2 px-3 text-[0.68rem] font-black uppercase tracking-[0.18em] text-slate-400">
            Explorar
          </p>

          <div className="space-y-1">
            <MobileNavLink
              to="/"
              icon={Home}
              isActive={isCurrentPath("/")}
              onClick={onClose}
            >
              Inicio
            </MobileNavLink>
            <MobileNavLink
              to="/products"
              icon={LayoutGrid}
              isActive={isCurrentPath("/products") && !location.search}
              onClick={onClose}
            >
              Todos los productos
            </MobileNavLink>

            <details className="group rounded-2xl open:bg-stone-50">
              <summary className="flex min-h-12 cursor-pointer list-none items-center gap-3 rounded-2xl px-3 text-sm font-bold text-slate-700 transition-colors hover:bg-stone-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] [&::-webkit-details-marker]:hidden">
                <span className="grid h-9 w-9 place-items-center rounded-xl bg-white text-slate-500 shadow-sm">
                  <ShoppingBag className="h-4 w-4" aria-hidden="true" />
                </span>
                <span className="flex-1">Comprar por categoría</span>
                <ChevronDown
                  className="h-4 w-4 text-slate-400 transition-transform group-open:rotate-180 motion-reduce:transition-none"
                  aria-hidden="true"
                />
              </summary>
              <ul className="space-y-1 pb-2 pl-[3.75rem] pr-2 pt-1">
                {categoryLinks.map((link) => (
                  <li key={link.to}>
                    <Link
                      to={link.to}
                      onClick={onClose}
                      className="block rounded-lg px-2 py-2.5 text-sm font-medium text-slate-500 transition-colors hover:bg-white hover:text-[#ff5331] focus-visible:outline-2 focus-visible:outline-[#ff5331]"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </details>

            <MobileNavLink
              to="/cart"
              icon={ShoppingBag}
              isActive={isCurrentPath("/cart")}
              onClick={onClose}
              badge={cartItemCount}
            >
              Carrito de compras
            </MobileNavLink>
            <MobileNavLink
              to={accountPath}
              icon={LogIn}
              isActive={isCurrentPath(accountPath)}
              onClick={onClose}
            >
              {account ? account.username : "Iniciar sesión"}
            </MobileNavLink>
            {showAdminLink ? (
              <MobileNavLink
                to="/admin"
                icon={ShieldCheck}
                isActive={isCurrentPath("/admin")}
                onClick={onClose}
              >
                Admin
              </MobileNavLink>
            ) : null}
          </div>

          <div className="my-5 h-px bg-stone-200" />

          <p className="mb-2 px-3 text-[0.68rem] font-black uppercase tracking-[0.18em] text-slate-400">
            Soporte
          </p>
          <details className="group rounded-2xl open:bg-stone-50">
            <summary className="flex min-h-12 cursor-pointer list-none items-center gap-3 rounded-2xl px-3 text-sm font-bold text-slate-700 transition-colors hover:bg-stone-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] [&::-webkit-details-marker]:hidden">
              <span className="grid h-9 w-9 place-items-center rounded-xl bg-white text-slate-500 shadow-sm">
                <CircleHelp className="h-4 w-4" aria-hidden="true" />
              </span>
              <span className="flex-1">Ayuda e información</span>
              <ChevronDown
                className="h-4 w-4 text-slate-400 transition-transform group-open:rotate-180 motion-reduce:transition-none"
                aria-hidden="true"
              />
            </summary>
            <ul className="space-y-1 pb-2 pl-[3.75rem] pr-2 pt-1">
              {HELP_LINKS.map((link) => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    onClick={onClose}
                    className="block rounded-lg px-2 py-2.5 text-sm font-medium text-slate-500 transition-colors hover:bg-white hover:text-[#ff5331] focus-visible:outline-2 focus-visible:outline-[#ff5331]"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </details>
        </nav>

        <footer className="border-t border-stone-200/80 bg-white/80 px-5 pb-[max(1.25rem,env(safe-area-inset-bottom))] pt-4 backdrop-blur">
          <div className="flex items-center justify-between gap-4 text-xs font-semibold text-slate-400">
            <Link
              to="/privacy-policy"
              onClick={onClose}
              className="rounded-md py-2 transition-colors hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-[#ff5331]"
            >
              Privacidad
            </Link>
            <span aria-hidden="true">•</span>
            <Link
              to="/terms-of-service"
              onClick={onClose}
              className="rounded-md py-2 transition-colors hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-[#ff5331]"
            >
              Términos
            </Link>
            <span className="ml-auto text-[#ff5331]">Coral © 2026</span>
          </div>
        </footer>
      </aside>
    </div>
  );
}

function MobileNavLink({
  to,
  icon: Icon,
  isActive,
  onClick,
  badge,
  children,
}) {
  return (
    <Link
      to={to}
      onClick={onClick}
      aria-current={isActive ? "page" : undefined}
      className={`flex min-h-12 items-center gap-3 rounded-2xl px-3 text-sm font-bold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${
        isActive
          ? "bg-[#fff0eb] text-[#e94727]"
          : "text-slate-700 hover:bg-stone-100"
      }`}
    >
      <span
        className={`grid h-9 w-9 place-items-center rounded-xl shadow-sm ${
          isActive ? "bg-white text-[#ff5331]" : "bg-white text-slate-500"
        }`}
      >
        <Icon className="h-4 w-4" aria-hidden="true" />
      </span>
      <span className="flex-1">{children}</span>
      {badge > 0 && (
        <span className="grid min-h-6 min-w-6 place-items-center rounded-full bg-[#ff5331] px-1.5 text-[0.68rem] font-black text-white">
          {badge > 99 ? "99+" : badge}
        </span>
      )}
    </Link>
  );
}
