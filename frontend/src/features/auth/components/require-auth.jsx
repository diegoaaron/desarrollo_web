import { Navigate, Outlet, useLocation } from "react-router";
import { useAuth } from "../hooks/use-auth";

// Guarda de rutas de cliente (checkout, «Mis pedidos»): sin sesión, envía al login y
// guarda la ruta actual para volver exactamente al mismo paso después de ingresar.
export function RequireAuth() {
  const { account, checking, error } = useAuth();
  const location = useLocation();

  if (checking) {
    return <main className="grid min-h-[60vh] place-items-center text-slate-600" role="status">Verificando tu sesión...</main>;
  }
  if (error) {
    return <main className="grid min-h-[60vh] place-items-center px-6 text-center text-red-700" role="alert">{error}</main>;
  }
  if (!account) {
    return <Navigate to="/login" state={{ from: `${location.pathname}${location.search}` }} replace />;
  }
  return <Outlet />;
}
