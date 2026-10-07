import { CheckCircle2, Clock3, Mail, MapPin, MessageCircle, Send } from "lucide-react";
import { useState } from "react";
import { isValidEmail } from "../../shared/utils/validation";
import { ContentCard, ContentPage } from "./components/content-page";

const CONTACT_DETAILS = [
  { label: "Escríbenos", value: "hola@coralshop.pe", icon: Mail },
  { label: "Visítanos", value: "Miraflores, Lima – Perú", icon: MapPin },
  { label: "Horario de atención", value: "Lun–Vie, 9:00–18:00 (hora de Lima)", icon: Clock3 },
];

const EMPTY_FORM = { firstName: "", lastName: "", email: "", message: "" };

function validate(form) {
  const errors = {};
  if (!form.firstName.trim()) errors.firstName = "Ingresa tu nombre.";
  if (!form.lastName.trim()) errors.lastName = "Ingresa tu apellido.";
  if (!isValidEmail(form.email)) errors.email = "Ingresa un correo electrónico válido.";
  if (form.message.trim().length < 10) {
    errors.message = "Cuéntanos un poco más (mínimo 10 caracteres).";
  }
  return errors;
}

export function ContactUsPage() {
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const [submittedName, setSubmittedName] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    setErrors((current) => ({ ...current, [name]: undefined }));
    setSubmittedName("");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const nextErrors = validate(form);
    setErrors(nextErrors);

    if (Object.keys(nextErrors).length > 0) return;

    setSubmittedName(form.firstName.trim());
    setForm(EMPTY_FORM);
  };

  return (
    <ContentPage
      eyebrow="Atención al cliente"
      title="Nos encantaría saber de ti"
      description="¿Tienes dudas sobre un pedido, un producto o la personalización de tu prenda? Nuestro equipo está para ayudarte."
      icon={MessageCircle}
    >
      <div className="grid gap-6 lg:grid-cols-[0.75fr_1.25fr]">
        <div className="space-y-4">
          {CONTACT_DETAILS.map((detail) => {
            const Icon = detail.icon;
            return (
              <ContentCard key={detail.label} className="flex items-center gap-4 p-5">
                <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[#fff0eb] text-[#ff5331]">
                  <Icon className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <p className="text-xs font-black uppercase tracking-wider text-slate-400">
                    {detail.label}
                  </p>
                  <p className="mt-1 text-sm font-bold text-slate-800 sm:text-base">
                    {detail.value}
                  </p>
                </div>
              </ContentCard>
            );
          })}

          <div className="rounded-[1.75rem] bg-slate-950 p-6 text-white">
            <p className="text-xs font-black uppercase tracking-[0.18em] text-[#ff7354]">
              Tiempo de respuesta habitual
            </p>
            <p className="mt-3 text-3xl font-black">Menos de 24 horas</p>
            <p className="mt-2 text-sm leading-6 text-slate-300">
              Respondemos cada mensaje de forma personal durante el horario de atención.
            </p>
          </div>
        </div>

        <ContentCard className="p-5 sm:p-8">
          <h2 className="text-2xl font-black tracking-tight text-slate-950">
            Envíanos un mensaje
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Cuéntanos cómo podemos ayudarte e incluye tu número de pedido si corresponde.
          </p>

          {submittedName && (
            <div
              role="status"
              className="mt-6 flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800"
            >
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
              <p>
                Gracias, {submittedName}. Tu mensaje quedó registrado; te
                responderemos al correo que indicaste.
              </p>
            </div>
          )}

          <form className="mt-7 space-y-5" onSubmit={handleSubmit} noValidate>
            <div className="grid gap-5 sm:grid-cols-2">
              <FormField id="first-name" label="Nombre" error={errors.firstName}>
                <input id="first-name" name="firstName" type="text" autoComplete="given-name" value={form.firstName} onChange={handleChange} aria-invalid={Boolean(errors.firstName)} aria-describedby={errors.firstName ? "first-name-error" : undefined} className={inputStyles} />
              </FormField>
              <FormField id="last-name" label="Apellido" error={errors.lastName}>
                <input id="last-name" name="lastName" type="text" autoComplete="family-name" value={form.lastName} onChange={handleChange} aria-invalid={Boolean(errors.lastName)} aria-describedby={errors.lastName ? "last-name-error" : undefined} className={inputStyles} />
              </FormField>
            </div>
            <FormField id="contact-email" label="Correo electrónico" error={errors.email}>
              <input id="contact-email" name="email" type="email" autoComplete="email" value={form.email} onChange={handleChange} aria-invalid={Boolean(errors.email)} aria-describedby={errors.email ? "contact-email-error" : undefined} className={inputStyles} />
            </FormField>
            <FormField id="contact-message" label="¿En qué podemos ayudarte?" error={errors.message}>
              <textarea id="contact-message" name="message" rows="5" value={form.message} onChange={handleChange} aria-invalid={Boolean(errors.message)} aria-describedby={errors.message ? "contact-message-error" : undefined} className={`${inputStyles} resize-none`} />
            </FormField>
            <button
              type="submit"
              className="flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[#ff5331] px-5 py-3 text-sm font-bold text-white shadow-lg shadow-[#ff5331]/20 transition hover:-translate-y-0.5 hover:bg-[#e94727] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#ff5331] motion-reduce:transform-none"
            >
              Enviar mensaje
              <Send className="h-4 w-4" aria-hidden="true" />
            </button>
          </form>
        </ContentCard>
      </div>
    </ContentPage>
  );
}

const inputStyles =
  "mt-2 min-h-12 w-full rounded-xl border border-stone-200 bg-stone-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-[#ff5331] focus:bg-white focus:ring-4 focus:ring-[#ff5331]/10 aria-[invalid=true]:border-red-400";

function FormField({ id, label, error, children }) {
  return (
    <div>
      <label htmlFor={id} className="text-sm font-bold text-slate-700">
        {label}
      </label>
      {children}
      {error && (
        <p id={`${id}-error`} className="mt-1.5 text-xs font-semibold text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
