import { ChevronLeft, ChevronRight, X } from "lucide-react";
import { useSearchParams } from "react-router";
import { useCategories } from "../../features/categories/hooks/use-categories";
import { ProductCard } from "../../features/products/components/product-card";
import { useProductTypes, useProducts } from "../../features/products/hooks/use-products";
import { ProductsSkeleton } from "../../features/products/skeletons/products-skeleton";
import { ErrorState } from "../../shared/components/error-state";

const PAGE_SIZE = 12;

function normalize(value) {
  return String(value ?? "").toLocaleLowerCase("es");
}

export function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { categories, isLoading: loadingCategories } = useCategories();
  const types = useProductTypes();

  // La URL guarda la categoría por nombre (enlaces del menú); la API la filtra por id.
  const category = searchParams.get("category");
  const type = searchParams.get("type");
  const sort = searchParams.get("sort");
  const query = (searchParams.get("q") ?? "").trim();
  const page = Math.max(0, Number.parseInt(searchParams.get("page") ?? "0", 10) || 0);
  const categoryId = category
    ? categories.find((item) => normalize(item.name) === normalize(category))?.id ?? -1
    : undefined;

  const { products, totalItems, totalPages, isLoading, error } = useProducts({
    type: type ?? undefined,
    categoryId: categoryId === -1 ? undefined : categoryId,
    q: query || undefined,
    page,
    size: PAGE_SIZE,
    skip: Boolean(category) && loadingCategories,
  });

  // La API no ordena por precio: se ordena la página visible.
  const visibleProducts = sort === "price-low"
    ? [...products].sort((a, b) => Number(a.basePrice ?? 0) - Number(b.basePrice ?? 0))
    : products;
  const unknownCategory = categoryId === -1 && !loadingCategories;

  function update(next) {
    const params = new URLSearchParams(searchParams);
    Object.entries(next).forEach(([key, value]) => {
      if (value === null || value === undefined || value === "" || (key === "page" && value === 0)) params.delete(key);
      else params.set(key, value);
    });
    setSearchParams(params);
  }

  const pageTitle = query
    ? `Resultados para «${query}»`
    : category
      ? category
      : type
        ? types.find((item) => item.code === type)?.name ?? "Productos"
        : "Todos los productos";

  if (error) return <ErrorState message={error} />;

  return (
    <section className="mx-auto w-[90%] max-w-7xl py-16">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold md:text-3xl">{pageTitle}</h1>
        <p className="text-slate-600">Elige la prenda base y personalízala con tu diseño.</p>
        {query && (
          <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
            <span className="text-slate-500">Búsqueda activa:</span>
            <span className="inline-flex items-center gap-1 rounded-full bg-[#fff0eb] py-1 pl-3 pr-1 font-semibold text-[#e94727]">
              {query}
              <button
                type="button"
                onClick={() => update({ q: null, page: 0 })}
                className="grid h-6 w-6 place-items-center rounded-full hover:bg-white focus-visible:outline-2 focus-visible:outline-[#ff5331]"
                aria-label={`Quitar la búsqueda «${query}»`}
              >
                <X className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            </span>
          </div>
        )}
      </div>

      <div className="mb-10 flex flex-col gap-4 rounded-2xl border border-stone-200 bg-white p-4 sm:flex-row sm:flex-wrap sm:items-center">
        <div className="flex flex-wrap gap-2" role="group" aria-label="Filtrar por tipo de prenda">
          <FilterChip active={!type} onClick={() => update({ type: null, page: 0 })}>Todas</FilterChip>
          {types.map((item) => (
            <FilterChip key={item.code} active={type === item.code} onClick={() => update({ type: item.code, page: 0 })}>
              {item.name}
            </FilterChip>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-3 sm:ml-auto">
          <label className="flex items-center gap-2 text-sm text-slate-600">
            Categoría
            <select
              value={category ?? ""}
              onChange={(event) => update({ category: event.target.value || null, page: 0 })}
              className="rounded-lg border border-stone-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700"
            >
              <option value="">Todas</option>
              {categories.map((item) => <option key={item.id} value={item.name}>{item.name}</option>)}
            </select>
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-600">
            Orden
            <select
              value={sort ?? ""}
              onChange={(event) => update({ sort: event.target.value || null })}
              className="rounded-lg border border-stone-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700"
            >
              <option value="">Más recientes</option>
              <option value="price-low">Precio: menor a mayor</option>
            </select>
          </label>
        </div>
      </div>

      {isLoading ? (
        <ProductsSkeleton />
      ) : visibleProducts.length > 0 && !unknownCategory ? (
        <>
          <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3">
            {visibleProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          {totalPages > 1 ? (
            <nav className="mt-12 flex items-center justify-center gap-3 text-sm" aria-label="Paginación">
              <button
                type="button"
                onClick={() => update({ page: page - 1 })}
                disabled={page === 0}
                className="inline-flex items-center gap-1 rounded-lg border border-stone-200 px-3 py-2 font-semibold disabled:opacity-40"
              >
                <ChevronLeft className="h-4 w-4" aria-hidden="true" /> Anterior
              </button>
              <span className="text-slate-500">Página {page + 1} de {totalPages} · {totalItems} productos</span>
              <button
                type="button"
                onClick={() => update({ page: page + 1 })}
                disabled={page + 1 >= totalPages}
                className="inline-flex items-center gap-1 rounded-lg border border-stone-200 px-3 py-2 font-semibold disabled:opacity-40"
              >
                Siguiente <ChevronRight className="h-4 w-4" aria-hidden="true" />
              </button>
            </nav>
          ) : null}
        </>
      ) : (
        <div className="rounded-2xl border border-stone-200 bg-stone-50 px-6 py-14 text-center text-slate-500">
          {query
            ? "No encontramos productos que coincidan con tu búsqueda."
            : "No se encontraron productos con estos filtros."}
        </div>
      )}
    </section>
  );
}

function FilterChip({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`rounded-full px-4 py-1.5 text-sm font-semibold transition ${
        active ? "bg-slate-900 text-white" : "bg-stone-100 text-slate-600 hover:bg-stone-200"
      }`}
    >
      {children}
    </button>
  );
}
