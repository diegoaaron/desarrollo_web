import { Package, Plus, Search } from "lucide-react";
import { Link } from "react-router";
import {
  AdminBadge,
  AdminPageHeader,
  AdminPanel,
  EmptyState,
  ErrorState,
} from "../components/admin-ui";
import { primaryButtonStyles } from "../components/admin-styles";
import { secondaryButtonStyles } from "../components/admin-styles";
import { useProducts } from "../hooks/use-products";
import { formatPrice } from "../../../shared/utils/format-price";

const SKELETONS = Array.from({ length: 5 }, (_, index) => index);

export function Products() {
  const { products, loading, error } = useProducts();

  if (error) return <ErrorState error={error} />;

  return (
    <div>
      <AdminPageHeader
        eyebrow="Catálogo"
        title="Productos"
        description="Agrega prendas a tu catálogo. La edición y la eliminación estarán disponibles en una próxima actualización."
        actions={<div className="flex flex-wrap gap-3">
          <Link to="/admin/products/import" className={secondaryButtonStyles}>
            <Search className="h-4 w-4" aria-hidden="true" /> Importar desde CJ
          </Link>
          <Link to="/admin/products/new" className={primaryButtonStyles}>
            <Plus className="h-4 w-4" aria-hidden="true" /> Agregar producto
          </Link>
        </div>}
      />

      <AdminPanel>
        <div className="flex items-center justify-between border-b border-stone-200/80 px-5 py-4 sm:px-7">
          <div className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-xl bg-[#fff0eb] text-[#e94727]">
              <Package className="h-4 w-4" aria-hidden="true" />
            </span>
            <div>
              <h2 className="font-black text-slate-900">Biblioteca de productos</h2>
              <p className="text-xs text-slate-400">{products.length} productos en total</p>
            </div>
          </div>
        </div>

        {loading ? (
          <ProductSkeletons />
        ) : products.length > 0 ? (
          <>
            <div className="divide-y divide-stone-100 md:hidden">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>

            <div className="hidden overflow-x-auto md:block">
              <table className="w-full min-w-[52rem] text-left">
                <thead className="bg-stone-50/80">
                  <tr className="text-[0.66rem] font-black uppercase tracking-[0.14em] text-slate-400">
                    <th className="px-6 py-4">ID</th>
                    <th className="px-6 py-4">Producto</th>
                    <th className="px-6 py-4">Precio</th>
                    <th className="px-6 py-4">Categoría</th>
                    <th className="px-6 py-4">Estado</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {products.map((product) => (
                    <tr key={product.id} className="transition-colors hover:bg-[#fffaf7]">
                      <td className="px-6 py-4 text-xs font-bold text-slate-400">#{product.id}</td>
                      <td className="max-w-[18rem] px-6 py-4 text-sm font-black text-slate-900">
                        <span className="block truncate">{product.name}</span>
                      </td>
                      <td className="px-6 py-4 text-sm font-black text-slate-900">{formatPrice(product.basePrice)}</td>
                      <td className="px-6 py-4 text-sm font-semibold text-slate-500">{product.categoryName || "Sin categoría"}</td>
                      <td className="px-6 py-4">
                        <AdminBadge value={product.isActive ? "ACTIVE" : "INACTIVE"} label={product.isActive ? "Activo" : "Inactivo"} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ) : (
          <EmptyState title="Aún no hay productos" description="Agrega tu primer producto para empezar a armar el catálogo." />
        )}
      </AdminPanel>

    </div>
  );
}

function ProductCard({ product }) {
  return (
    <article className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs font-bold text-slate-400">#{product.id}</p>
          <h2 className="mt-1 truncate font-black text-slate-950">{product.name}</h2>
          <p className="mt-1 text-sm font-semibold text-slate-500">{product.categoryName || "Sin categoría"}</p>
        </div>
        <AdminBadge value={product.isActive ? "ACTIVE" : "INACTIVE"} label={product.isActive ? "Activo" : "Inactivo"} />
      </div>
      <div className="mt-5 flex items-center justify-between gap-4 border-t border-stone-100 pt-4">
        <p className="text-lg font-black text-slate-950">{formatPrice(product.basePrice)}</p>
      </div>
    </article>
  );
}

function ProductSkeletons() {
  return (
    <div className="divide-y divide-stone-100 px-5 sm:px-7">
      {SKELETONS.map((item) => (
        <div key={item} className="flex animate-pulse items-center gap-4 py-5">
          <div className="h-10 w-10 rounded-xl bg-stone-100" />
          <div className="flex-1 space-y-2">
            <div className="h-3 w-40 max-w-full rounded bg-stone-100" />
            <div className="h-3 w-24 rounded bg-stone-100" />
          </div>
          <div className="h-8 w-16 rounded-xl bg-stone-100" />
        </div>
      ))}
    </div>
  );
}
