import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router";
import { ProductCustomizer } from "../../features/customization/components/product-customizer";
import { useProduct } from "../../features/products/hooks/use-product";
import { ProductDetailSkeleton } from "../../features/products/skeletons/products-detail-skeleton";
import { ErrorState } from "../../shared/components/error-state";
import { formatPrice } from "../../shared/utils/format-price";

export function ProductDetailPage() {
  const { id } = useParams();
  const { product, isLoading, error } = useProduct(id);

  if (isLoading) return <ProductDetailSkeleton />;
  if (error || !product) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <ErrorState message={error || "Producto no encontrado"} />
        <Link to="/products" className="text-sm font-semibold text-gray-600 underline hover:text-black">
          Volver a productos
        </Link>
      </div>
    );
  }

  return (
    <main className="mx-auto w-[92%] max-w-7xl py-10">
      <Link to="/products" className="mb-6 inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-[#e94727]">
        <ArrowLeft className="h-4 w-4" aria-hidden="true" /> Volver al catálogo
      </Link>

      <header className="mb-10 flex flex-col gap-4 border-b border-stone-200 pb-8 md:flex-row md:items-end md:justify-between">
        <div className="max-w-2xl">
          <span className="mb-2 inline-block text-xs font-bold uppercase tracking-wider text-[#e94727]">
            {product.categoryName}{product.brandName ? ` · ${product.brandName}` : ""}
            {product.isCustomizable ? " · Personalizable" : ""}
          </span>
          <h1 className="text-3xl font-bold leading-tight tracking-tight text-gray-900 sm:text-4xl">{product.name}</h1>
          <p className="mt-3 leading-relaxed text-gray-600">{product.description || "Aún no tiene descripción."}</p>
        </div>
        <div className="md:text-right">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Prenda base desde</p>
          <p className="text-4xl font-extrabold text-gray-900">{formatPrice(product.basePrice)}</p>
          <p className="mt-1 text-xs text-slate-500">Descuentos desde 3 unidades del mismo diseño</p>
        </div>
      </header>

      <ProductCustomizer key={product.id} product={product} />
    </main>
  );
}
