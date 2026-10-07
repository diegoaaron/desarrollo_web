import { Link } from "react-router";
import HeroImage from "/hero.jpg";

export function Hero() {
  return (
    <section className="bg-linear-to-br from-rose-50 via-orange-50 to-rose-50 overflow-hidden py-16">
      <div className="max-w-7xl w-[90%] mx-auto flex flex-col items-center gap-8 md:flex-row">
        <div className="flex-1">
          <span className="inline-block bg-[#FFE8E3] px-4 py-2 rounded-full mb-6">
            ✨ Colección 2026
          </span>
          <h1 className="font-semibold text-5xl max-w-150 lg:text-6xl tracking-tight mb-6">
            Diseña tu estilo,
            <span className="text-[#FF623F]"> estampa tu idea</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-lg mb-6">
            Polos, poleras, gorras y tote bags que tú mismo personalizas con tu
            imagen o texto. Cada prenda cuenta tu historia.
          </p>
          <div className="flex gap-5">
            <Link to="/products" className="px-8 py-3 bg-[#FF623F] text-white font-semibold rounded-lg hover:shadow-xl hover:scale-105 transition-all duration-300 shadow-lg shador-bg-[#FF623F]">
              Comprar ahora
            </Link>
            <Link to="/products" className="px-8 py-3 bg-white font-semibold text-gray-700 rounded-lg hover:bg-gray-50 hover:shadow-lg transition-all duration-300 border border-gray-200">
              Ver colecciones
            </Link>
          </div>
        </div>
        <div className="flex-1 rounded-4xl overflow-hidden">
          <img src={HeroImage} alt="Prendas personalizadas de Coral Shop" />
        </div>
      </div>
    </section>
  );
}
