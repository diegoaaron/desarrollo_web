// Nombre visible de una cuenta (sesión, usuario del admin o cliente de un pedido).
export function fullName(person) {
  return [person?.firstName, person?.lastName]
    .map((part) => part?.trim())
    .filter(Boolean)
    .join(" ");
}

export function initial(person) {
  return (person?.firstName?.trim().charAt(0) || person?.email?.charAt(0) || "?").toUpperCase();
}
