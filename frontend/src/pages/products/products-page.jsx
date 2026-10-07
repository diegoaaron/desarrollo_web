import { X } from "lucide-react";
import { useSearchParams } from "react-router";
import { ProductCard } from "../../features/products/components/product-card";
import { useProducts } from "../../features/products/hooks/use-products";
import { ProductsSkeleton } from "../../features/products/skeletons/products-skeleton";
import { ErrorState } from "../../shared/components/error-state";

function normalize(value) {
  return String(value ?? "").toLocaleLowerCase("es");
}

function matchesQuery(product, query) {
  return [product.name, product.description, product.categoryName].some(
    (field) => normalize(field).includes(query),
  );
}

export function ProductsPage() {
  const { products, isLoading, error } = useProducts();
  const [searchParams, setSearchParams] = useSearchParams();

  const category = searchParams.get("category");
  const sort = searchParams.get("sort");
  const query = (searchParams.get("q") ?? "").trim();
  const normalizedQuery = normalize(query);

  let visibleProducts = category
    ? products.filter(
      (product) => normalize(product.categoryName) === normalize(category),
    )
    : products;

  if (normalizedQuery) {
    visibleProducts = visibleProducts.filter((product) =>
      matchesQuery(product, normalizedQuery),
    );
  }

  if (sort === "price-low") {
    visibleProducts = [...visibleProducts].sort(
      (a, b) => Number(a.basePrice ?? 0) - Number(b.basePrice ?? 0),
    );
  }

  const pageTitle = query
    ? `Resultados para «${query}»`
    : sort === "price-low"
      ? "Precio: menor a mayor"
      : category
        ? category
        : "Todos los productos";

  const clearSearch = () => {
    const nextParams = new URLSearchParams(searchParams);
    nextParams.delete("q");
    setSearchParams(nextParams);
  };

  if (isLoading) return <ProductsSkeleton />;
  if (error) return <ErrorState message={error} />;

  return (
    <section className="max-w-7xl w-[90%] mx-auto py-16">
      <div className="mb-10">
        <h1 className="text-2xl font-semibold md:text-3xl">{pageTitle}</h1>
        <p>Seleccionados especialmente para ti</p>
        {query && (
          <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
            <span className="text-slate-500">Búsqueda activa:</span>
            <span className="inline-flex items-center gap-1 rounded-full bg-[#fff0eb] py-1 pl-3 pr-1 font-semibold text-[#e94727]">
              {query}
              <button
                type="button"
                onClick={clearSearch}
                className="grid h-6 w-6 place-items-center rounded-full hover:bg-white focus-visible:outline-2 focus-visible:outline-[#ff5331]"
                aria-label={`Quitar la búsqueda «${query}»`}
              >
                <X className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            </span>
            {category && (
              <span className="text-slate-500">en la categoría {category}</span>
            )}
          </div>
        )}
      </div>
      {visibleProducts.length > 0 ? (
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3">
          {visibleProducts.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
            />
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-stone-200 bg-stone-50 px-6 py-14 text-center text-slate-500">
          {query
            ? "No encontramos productos que coincidan con tu búsqueda."
            : "No se encontraron productos en esta categoría."}
        </div>
      )}
    </section>
  );
}
