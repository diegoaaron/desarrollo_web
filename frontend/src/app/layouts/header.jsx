import { Menu, Search, ShieldCheck, ShoppingCart, User, X } from "lucide-react";
import { useCallback, useRef, useState } from "react";
import { Link, useNavigate } from "react-router";
import { CartDropDown } from "../../features/cart/components/cart-dropdown";
import { useCart } from "../../features/cart/hooks/use-cart";
import { useAuth } from "../../features/auth/hooks/use-auth";
import {
  categoryPath,
  useCategories,
} from "../../features/categories/hooks/use-categories";
import { MobileMenu } from "./mobile-menu";
import { fullName, initial } from "../../features/auth/model/account-name";

export function Header() {
  const { account, checking } = useAuth();
  const { categories } = useCategories();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const cartButtonRef = useRef(null);
  const menuButtonRef = useRef(null);

  const {
    cart,
    removeFromCart,
    increaseQuantity,
    decreaseQuantity,
    cartTotal,
    clearCart,
  } = useCart();


  const closeCart = useCallback(() => {
    setIsCartOpen(false);
    window.requestAnimationFrame(() => cartButtonRef.current?.focus());
  }, []);

  const closeMobileMenu = useCallback(() => {
    setIsMobileMenuOpen(false);
    window.requestAnimationFrame(() => menuButtonRef.current?.focus());
  }, []);

  const toggleMobileMenu = () => {
    if (isMobileMenuOpen) {
      closeMobileMenu();
    } else {
      setIsCartOpen(false);
      setIsMobileMenuOpen(true);
    }
  };

  const toggleCart = () => {
    if (isCartOpen) {
      closeCart();
    } else {
      setIsMobileMenuOpen(false);
      setIsCartOpen(true);
    }
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    const query = searchTerm.trim();
    navigate(query ? `/products?q=${encodeURIComponent(query)}` : "/products");
    setSearchTerm("");
  };

  const cartItemCount = cart.reduce(
    (total, item) => total + item.quantity,
    0,
  );
  const accountPath = account ? "/account" : "/login";
  // Visible para visitantes (lleva al login y luego al panel) y para administradores.
  const showAdminLink = !account || account.role === "ROLE_ADMIN";

  return (
    <header className="sticky top-0 z-50">
      <p className="bg-[#ff5331] py-4 text-center text-white">
        ✨ Prendas personalizadas con tu diseño | Envíos a todo el Perú
      </p>
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto w-[90%] py-4">
          <div className="grid items-center grid-cols-2 gap-4 md:grid-cols-[1fr_2.5fr_1fr]">
            <div className="flex items-center gap-4">
              <button
                ref={menuButtonRef}
                type="button"
                className={`grid h-10 w-10 place-items-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] md:hidden ${
                  isMobileMenuOpen
                    ? "bg-[#fff0eb] text-[#ff5331]"
                    : "text-slate-700 hover:bg-stone-100"
                }`}
                aria-label={
                  isMobileMenuOpen
                    ? "Cerrar menú de navegación"
                    : "Abrir menú de navegación"
                }
                aria-expanded={isMobileMenuOpen}
                aria-controls="mobile-navigation"
                aria-haspopup="dialog"
                onClick={toggleMobileMenu}
              >
                {isMobileMenuOpen ? (
                  <X aria-hidden="true" />
                ) : (
                  <Menu aria-hidden="true" />
                )}
              </button>
              <Link to="/" className="text-[#ff5331] text-3xl font-semibold">
                Coral
              </Link>
            </div>
            <div className="relative col-start-2 col-end-3 flex justify-end gap-3 md:col-start-3 md:col-end-4">
              {!checking && showAdminLink ? (
                <Link
                  to="/admin"
                  className="hidden h-10 items-center gap-1.5 rounded-full border border-stone-200 px-3 text-sm font-semibold text-slate-700 transition-colors hover:border-[#ff5331] hover:text-[#ff5331] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] sm:inline-flex"
                  aria-label="Panel de administración"
                >
                  <ShieldCheck className="h-4 w-4" aria-hidden="true" /> Admin
                </Link>
              ) : null}
              {checking ? (
                <span className="grid h-10 w-10 place-items-center text-slate-400" role="status" aria-label="Cargando cuenta">
                  <User aria-hidden="true" />
                </span>
              ) : (
                <Link
                  to={accountPath}
                  className={`grid h-10 w-10 place-items-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${account ? "bg-[#ff5331] text-white hover:bg-[#e94727]" : "text-slate-700 hover:bg-stone-100"}`}
                  aria-label={account ? `Abrir la cuenta de ${fullName(account)}` : "Iniciar sesión"}
                >
                  {account ? (
                    <span aria-hidden="true" className="text-base font-bold uppercase">
                      {initial(account)}
                    </span>
                  ) : <User aria-hidden="true" />}
                </Link>
              )}
              <button
                ref={cartButtonRef}
                type="button"
                className={`relative grid h-10 w-10 place-items-center rounded-full transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] ${
                  isCartOpen
                    ? "bg-[#fff0eb] text-[#ff5331]"
                    : "text-slate-700 hover:bg-stone-100"
                }`}
                onClick={toggleCart}
                aria-label={`Abrir carrito de compras con ${cartItemCount} ${
                  cartItemCount === 1 ? "producto" : "productos"
                }`}
                aria-expanded={isCartOpen}
                aria-controls="shopping-cart-panel"
                aria-haspopup="dialog"
              >
                <ShoppingCart aria-hidden="true" />
                {cartItemCount > 0 && (
                  <span className="absolute -right-2 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-[#ff5331] px-1 text-xs text-white">
                    {cartItemCount > 99 ? "99+" : cartItemCount}
                  </span>
                )}
              </button>
              {isCartOpen && (
                <CartDropDown
                  cart={cart}
                  removeFromCart={removeFromCart}
                  increaseQuantity={increaseQuantity}
                  decreaseQuantity={decreaseQuantity}
                  cartTotal={cartTotal}
                  clearCart={clearCart}
                  onClose={closeCart}
                />
              )}
            </div>
            <form
              role="search"
              onSubmit={handleSearchSubmit}
              className="col-span-full md:row-start-1 md:col-start-2 md:col-end-3 flex items-center gap-2 border border-gray-200 bg-white px-4 py-2 rounded-xl shadow-sm focus-within:ring-2 focus-within:ring-orange-200"
            >
              <Search className="text-gray-400 w-4 h-4" aria-hidden="true" />
              <input
                className="w-full bg-transparent text-sm text-gray-700 placeholder-gray-400 focus:outline-none"
                type="search"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
                placeholder="Buscar productos..."
                aria-label="Buscar productos"
              />
              <button type="submit" className="sr-only">
                Buscar
              </button>
            </form>
            <ul className="hidden md:col-span-full md:flex md:justify-between md:gap-4 md:border-t md:border-gray-200 md:pt-4">
              <li>
                <Link to="/products">Todos los productos</Link>
              </li>
              {categories.map((category) => (
                <li key={category.id ?? category.name}>
                  <Link to={categoryPath(category.name)}>{category.name}</Link>
                </li>
              ))}
              <li>
                <Link to="/products?sort=price-low">Precio: menor a mayor</Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
      {isMobileMenuOpen && (
        <MobileMenu
          cartItemCount={cartItemCount}
          onClose={closeMobileMenu}
        />
      )}
    </header>
  );
}
