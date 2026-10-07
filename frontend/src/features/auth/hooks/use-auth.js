import { useContext } from "react";
import { AuthContext } from "../model/auth-context";

export function useAuth() {
  const auth = useContext(AuthContext);
  if (!auth) throw new Error("useAuth debe usarse dentro de un AuthProvider");
  return auth;
}
