import { ArrowLeft, ArrowRight, LockKeyhole, Mail, UserRound } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router";
import { registerUser } from "../../features/auth/api/auth-api";

const inputStyles =
  "block w-full rounded-xl border border-stone-200 bg-stone-50 px-4 py-3 pl-11 text-slate-900 outline-none transition focus:border-[#ff623f] focus:bg-white focus:ring-2 focus:ring-[#ff623f]/15";

export function RegisterPage() {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [registeredUser, setRegisteredUser] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    if (saving) return;

    const form = new FormData(event.currentTarget);
    setSaving(true);
    setError("");

    try {
      const user = await registerUser({
        firstName: form.get("firstName").trim(),
        lastName: form.get("lastName").trim(),
        email: form.get("email").trim(),
        password: form.get("password"),
      });
      setRegisteredUser(user);
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? "No pudimos conectar con el servidor. Verifica que el backend esté en ejecución."
          : requestError.message,
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-linear-to-br from-rose-50 via-orange-50 to-rose-50 px-4 py-12">
      <div className="w-full max-w-md rounded-3xl border border-stone-100 bg-white p-7 shadow-xl shadow-orange-950/5 sm:p-9">
        <Link
          to="/"
          className="inline-flex items-center gap-2 rounded text-sm font-semibold text-slate-500 hover:text-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff623f]"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Volver a la tienda
        </Link>

        {registeredUser ? (
          <div className="pt-10" role="status">
            <span className="inline-flex rounded-full bg-orange-50 px-3 py-1 text-xs font-bold uppercase tracking-wider text-[#e94727]">
              Cuenta creada
            </span>
            <h1 className="mt-5 text-3xl font-semibold tracking-tight text-slate-950">
              Te damos la bienvenida a Coral, {registeredUser.firstName}.
            </h1>
            <p className="mt-4 leading-7 text-slate-600">
              Tu cuenta se guardó correctamente. Inicia sesión para acceder a ella.
            </p>
            <Link
              to="/login"
              className="mt-8 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#ff623f] px-5 py-3 font-semibold text-white transition hover:bg-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff623f]"
            >
              Iniciar sesión <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>
        ) : (
          <>
            <div className="mb-8 mt-8">
              <span className="text-xs font-bold uppercase tracking-[0.2em] text-[#e94727]">
                Únete a la comunidad
              </span>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
                Crea tu cuenta
              </h1>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Un pequeño paso hacia las prendas que te encantan.
              </p>
            </div>

            {error ? (
              <p role="alert" className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </p>
            ) : null}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="register-first-name" className="mb-2 block text-sm font-semibold text-slate-700">
                    Nombre
                  </label>
                  <div className="relative">
                    <UserRound className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" aria-hidden="true" />
                    <input id="register-first-name" name="firstName" type="text" autoComplete="given-name" maxLength={80} required className={inputStyles} placeholder="Tu nombre" />
                  </div>
                </div>
                <div>
                  <label htmlFor="register-last-name" className="mb-2 block text-sm font-semibold text-slate-700">
                    Apellido
                  </label>
                  <div className="relative">
                    <UserRound className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" aria-hidden="true" />
                    <input id="register-last-name" name="lastName" type="text" autoComplete="family-name" maxLength={80} required className={inputStyles} placeholder="Tu apellido" />
                  </div>
                </div>
              </div>

              <div>
                <label htmlFor="register-email" className="mb-2 block text-sm font-semibold text-slate-700">
                  Correo electrónico
                </label>
                <div className="relative">
                  <Mail className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" aria-hidden="true" />
                  <input id="register-email" name="email" type="email" autoComplete="email" maxLength={255} required className={inputStyles} placeholder="tu@correo.com" />
                </div>
              </div>

              <div>
                <label htmlFor="register-password" className="mb-2 block text-sm font-semibold text-slate-700">
                  Contraseña
                </label>
                <div className="relative">
                  <LockKeyhole className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" aria-hidden="true" />
                  <input id="register-password" name="password" type="password" autoComplete="new-password" minLength={8} maxLength={72} required className={inputStyles} placeholder="Mínimo 8 caracteres" />
                </div>
              </div>

              <button
                type="submit"
                disabled={saving}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#ff623f] px-5 py-3 font-semibold text-white transition hover:bg-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff623f] disabled:cursor-wait disabled:opacity-60"
              >
                {saving ? "Creando cuenta..." : "Crear cuenta"}
                {!saving ? <ArrowRight className="h-4 w-4" aria-hidden="true" /> : null}
              </button>
            </form>

            <p className="mt-7 text-center text-sm text-slate-600">
              ¿Ya tienes una cuenta?{" "}
              <Link to="/login" className="font-semibold text-[#e94727] hover:underline">
                Inicia sesión
              </Link>
            </p>
          </>
        )}
      </div>
    </main>
  );
}
