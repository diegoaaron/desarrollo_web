import { Loader2 } from "lucide-react";
import { useState } from "react";
import { addressesApi } from "../api/checkout-api";
import { Field } from "./field";
import { fieldClass } from "./field-styles";

const EMPTY = {
  receiverName: "",
  phone: "",
  department: "Lima",
  province: "Lima",
  district: "",
  street: "",
  reference: "",
  isDefault: false,
};

// Alta de una dirección (D9: departamento, provincia y distrito). El servidor valida otra vez.
export function AddressForm({ defaultName = "", onSaved, onCancel }) {
  const [address, setAddress] = useState({ ...EMPTY, receiverName: defaultName });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});

  const update = (field) => (event) => {
    const value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
    setAddress((current) => ({ ...current, [field]: value }));
  };

  // Formulario anidado en el del checkout: se envía con su propio botón, no con submit.
  async function handleSave() {
    if (saving) return;
    setSaving(true);
    setError(null);
    setFieldErrors({});
    try {
      const saved = await addressesApi.create({
        ...address,
        reference: address.reference.trim() || null,
      });
      onSaved(saved);
    } catch (requestError) {
      setError(requestError.message);
      setFieldErrors(requestError.errors ?? {});
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-4 rounded-2xl border border-stone-200 bg-stone-50/60 p-4 sm:p-5">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Quién recibe" error={fieldErrors.receiverName}>
          <input value={address.receiverName} onChange={update("receiverName")} autoComplete="name" className={fieldClass} />
        </Field>
        <Field label="Teléfono" error={fieldErrors.phone}>
          <input value={address.phone} onChange={update("phone")} inputMode="tel" autoComplete="tel" placeholder="987 654 321" className={fieldClass} />
        </Field>
        <Field label="Departamento" error={fieldErrors.department}>
          <input value={address.department} onChange={update("department")} className={fieldClass} />
        </Field>
        <Field label="Provincia" error={fieldErrors.province}>
          <input value={address.province} onChange={update("province")} className={fieldClass} />
        </Field>
        <Field label="Distrito" error={fieldErrors.district}>
          <input value={address.district} onChange={update("district")} placeholder="Miraflores" className={fieldClass} />
        </Field>
        <Field label="Dirección" error={fieldErrors.street}>
          <input value={address.street} onChange={update("street")} autoComplete="street-address" placeholder="Av. Larco 123, dpto. 401" className={fieldClass} />
        </Field>
      </div>
      <Field label="Referencia (opcional)" error={fieldErrors.reference}>
        <input value={address.reference} onChange={update("reference")} placeholder="Frente al parque" className={fieldClass} />
      </Field>
      <label className="flex items-center gap-2 text-sm text-slate-600">
        <input type="checkbox" checked={address.isDefault} onChange={update("isDefault")} className="h-4 w-4 accent-[#ff5331]" />
        Usar como dirección principal
      </label>

      {error ? <p role="alert" className="text-sm font-semibold text-red-600">{error}</p> : null}

      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          onClick={handleSave}
          disabled={saving}
          className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-bold text-white hover:bg-black disabled:opacity-60"
        >
          {saving ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : null}
          Guardar dirección
        </button>
        {onCancel ? (
          <button type="button" onClick={onCancel} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-500 hover:text-slate-900">
            Cancelar
          </button>
        ) : null}
      </div>
    </div>
  );
}
