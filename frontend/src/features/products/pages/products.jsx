import { useSearchParams } from "react-router";
import { Footer } from "../../../common/components/footer";
import { Header } from "../../../common/components/header";
import { ProductItem } from "../component/product-item";
import { useGetProducts } from "../hooks/use-get-products";

export function ProductsPage() {
  const { products, loading, error } = useGetProducts();
  const [searchParams] = useSearchParams();
  const category = searchParams.get("category");
  const sort = searchParams.get("sort");

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  const visibleProducts = category
    ? products.filter((product) => product.category === category)
    : [...products];

  if (sort === "best_sellers") {
    visibleProducts.sort((a, b) => b.rating.count - a.rating.count);
  }

  return (
    <>
      <Header />
      <section className="max-w-7xl w-[90%] mx-auto py-16">
        <div className="mb-10">
          <h2 className="text-2xl font-semibold md:text-3xl">
            Features Products
          </h2>
          <p>Handpicked items for you</p>
        </div>
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3">
          {visibleProducts.map((product) => (
            <ProductItem key={product.id} product={product} />
          ))}
        </div>
      </section>
      <Footer />
    </>
  );
}
