async function getCsrfToken() {
  const response = await fetch("/api/auth/csrf");
  if (!response.ok) {
    throw new Error("No pudimos conectar con el servidor. Inténtalo de nuevo más tarde.");
  }
  const { token } = await response.json();
  return token;
}

export async function registerUser(details) {
  const token = await getCsrfToken();
  const response = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-TOKEN": token },
    body: JSON.stringify(details),
  });

  if (!response.ok) {
    if (response.status === 409) {
      throw new Error("Ese correo ya está registrado.");
    }
    if (response.status === 400) {
      throw new Error("Revisa tus datos e inténtalo de nuevo.");
    }
    throw new Error("No pudimos crear tu cuenta. Inténtalo de nuevo más tarde.");
  }

  return response.json();
}

export async function loginUser({ email, password }) {
  const token = await getCsrfToken();
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRF-TOKEN": token,
    },
    body: new URLSearchParams({ email, password }),
  });

  if (response.status === 401) {
    throw new Error("Correo o contraseña incorrectos.");
  }
  if (!response.ok) {
    throw new Error("No pudimos iniciar tu sesión. Inténtalo de nuevo más tarde.");
  }

  return response.json();
}

export async function getCurrentUser({ signal } = {}) {
  const response = await fetch("/api/auth/me", { signal });
  if (response.status === 401) return null;
  if (!response.ok) {
    throw new Error("No pudimos verificar tu sesión. Inténtalo de nuevo más tarde.");
  }

  return response.json();
}

export async function logoutUser() {
  const token = await getCsrfToken();
  const response = await fetch("/api/auth/logout", {
    method: "POST",
    headers: { "X-CSRF-TOKEN": token },
  });
  if (!response.ok) {
    throw new Error("No pudimos cerrar tu sesión. Inténtalo de nuevo.");
  }
}
