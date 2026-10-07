import { Link } from "react-router";
import {
  categoryPath,
  useCategories,
} from "../../../features/categories/hooks/use-categories";

const CATEGORY_IMAGES = {
  mujer: "/category_women.jpg",
  hombre: "/category_men.jpg",
};

function categoryImage(name) {
  return CATEGORY_IMAGES[String(name ?? "").trim().toLowerCase()] ?? null;
}

export function Category() {
  const { categories, isLoading, error } = useCategories();

  if (error || (!isLoading && categories.length === 0)) return null;

  return (
    <section className="bg-white py-16">
      <div className="max-w-7xl w-[90%] mx-auto">
        <div className="mb-10">
          <h2 className="text-4xl text-center font-semibold mb-3">
            Compra por categoría
          </h2>
          <p className="text-gray-600 text-center text-lg">
            Encuentra justo lo que buscas
          </p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3" role="status" aria-label="Cargando categorías">
            {[1, 2, 3].map((placeholder) => (
              <div key={placeholder} className="aspect-4/5 animate-pulse rounded-2xl bg-stone-100" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {categories.map((category) => {
              const image = categoryImage(category.name);

              return (
                <Link
                  to={categoryPath(category.name)}
                  className="relative aspect-4/5 rounded-2xl overflow-hidden cursor-pointer group"
                  key={category.id ?? category.name}
                >
                  {image ? (
                    <>
                      <img
                        className="w-full transition-transform duration-400 hover:scale-105"
                        src={image}
                        alt={category.name}
                      />
                      <div className="absolute inset-0 bg-linear-to-t from-black/80 via-black/30 to-black/10 transition-opacity duration-400 group-hover:from-black/95 group-hover:via/black/50 pointer-events-none"></div>
                    </>
                  ) : (
                    <div className="absolute inset-0 bg-linear-to-br from-[#ff5331] via-[#fa6240] to-[#3d1927] transition-transform duration-400 group-hover:scale-105">
                      <span
                        aria-hidden="true"
                        className="absolute right-6 top-4 text-[9rem] font-black leading-none text-white/15"
                      >
                        {category.name.trim().charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}

                  <div className="absolute z-10 bottom-0 p-8 text-white">
                    <h3 className="text-2xl mb-2">{category.name}</h3>
                    <span className="line-clamp-2 text-sm text-white/90">
                      {category.description || "Explorar colección"}
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
