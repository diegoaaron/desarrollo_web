# -*- coding: utf-8 -*-
"""
Prototipos de pantalla del Anexo B.

La paleta y los patrones de maquetado se toman del frontend real del equipo
(coral_shop-main): coral #FF5331 como color de marca, tarjetas gris 50 con
esquinas redondeadas, bordes gris 200 y tipografia sin serifa.

Las figuras se dibujan a ~7,4 pulgadas de ancho, que es casi el ancho con el
que se insertan en el informe, de modo que el texto se imprime a su tamano real.
"""

import os

from matplotlib.patches import Polygon, Circle, FancyBboxPatch

from estilo import lienzo, caja, texto, flecha, guardar

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "clase_entregables", "figuras")
os.makedirs(BASE, exist_ok=True)


def ruta(n):
    return os.path.join(BASE, n)


# ------------------------------------------------- paleta tomada del frontend
CORAL = "#FF5331"       # color de marca (header, precios, boton primario)
CORAL_2 = "#FF623F"     # variante usada en hero y formularios
CORAL_SUAVE = "#FFE8E3" # chip suave
ROSE_50 = "#FFF1F2"     # degradado del hero
ORANGE_50 = "#FFF7ED"
G50 = "#F9FAFB"         # fondo de tarjeta
G100 = "#F3F4F6"
G200 = "#E5E7EB"        # borde
G300 = "#D1D5DB"
G400 = "#9CA3AF"        # texto de marcador de posicion
G500 = "#6B7280"
G600 = "#4B5563"        # texto secundario
G700 = "#374151"
G900 = "#111827"        # texto principal y boton oscuro
AMBER = "#FBBF24"
AMBER_50 = "#FFFBEB"
AMBER_700 = "#B45309"
VERDE = "#16A34A"
VERDE_50 = "#F0FDF4"
AZUL = "#2563EB"
AZUL_50 = "#EFF6FF"
ROJO = "#DC2626"
MORADO = "#7C3AED"
BLANCO = "#FFFFFF"

F = "Arial"
# Arial no tiene glifos de simbolo (estrella, visto, flechas de UI); esta fuente
# del sistema si los tiene y se usa solo para esas etiquetas.
ICO = "Segoe UI Symbol"

# tamano estandar: 7,4 x 4,6 pulgadas con 20 unidades por pulgada
W, H = 148, 92


# --------------------------------------------- iconos dibujados como vectores
def icono_lupa(ax, cx, cy, r=1.15, color=G400, lw=0.9):
    ax.add_patch(Circle((cx, cy + r * 0.25), r, facecolor="none",
                        edgecolor=color, lw=lw, zorder=6))
    ax.plot([cx + r * 0.7, cx + r * 1.5], [cy - r * 0.45, cy - r * 1.2],
            color=color, lw=lw, zorder=6, solid_capstyle="round")


def icono_usuario(ax, cx, cy, r=1.3, color=G700, lw=0.9):
    ax.add_patch(Circle((cx, cy + r * 0.55), r * 0.55, facecolor="none",
                        edgecolor=color, lw=lw, zorder=6))
    ang = [i / 24 * 3.14159 for i in range(25)]
    xs = [cx + r * 0.95 * -1 * __import__("math").cos(a) for a in ang]
    ys = [cy - r * 0.55 + r * 0.85 * __import__("math").sin(a) for a in ang]
    ax.plot(xs, ys, color=color, lw=lw, zorder=6, solid_capstyle="round")


def icono_carrito(ax, cx, cy, s=1.3, color=G700, lw=0.9):
    ax.add_patch(Polygon([[cx - s, cy + s * 0.5], [cx + s, cy + s * 0.5],
                          [cx + s * 0.72, cy - s * 0.55],
                          [cx - s * 0.72, cy - s * 0.55]],
                         closed=True, facecolor="none", edgecolor=color,
                         lw=lw, zorder=6))
    ax.plot([cx - s * 1.35, cx - s * 1.0, cx - s * 0.9],
            [cy + s * 1.2, cy + s * 1.2, cy + s * 0.5],
            color=color, lw=lw, zorder=6, solid_capstyle="round")
    for dx in (-s * 0.45, s * 0.45):
        ax.add_patch(Circle((cx + dx, cy - s * 1.0), s * 0.22,
                            facecolor=color, edgecolor="none", zorder=6))


def pantalla(url, alto=H, ancho=W):
    """Marco de navegador. Reserva una franja superior para el rotulo B.x."""
    fig, ax = lienzo(ancho / 20, alto / 20, ancho, alto, bg=BLANCO)
    tope = alto - 6.5
    caja(ax, 0.5, 0.5, ancho - 1, tope - 0.5, fill=BLANCO, edge=G300, lw=1.0, r=1.2)
    barra = tope - 4.5
    caja(ax, 0.5, barra, ancho - 1, 4.5, fill=G100, edge=G300, lw=1.0, r=1.2)
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        ax.add_patch(Circle((4.0 + i * 2.6, barra + 2.25), 0.75, color=c, zorder=5))
    caja(ax, 13.5, barra + 0.8, ancho - 30, 2.9, fill=BLANCO, edge=G200, lw=0.8, r=1.4)
    texto(ax, 15.2, barra + 2.25, url, size=6.4, color=G500, font=F, va="center")
    return fig, ax, barra - 0.6


# --------------------------------------------------------------- primitivas
def boton(ax, x, y, w, h, etiqueta, tipo="primario", size=7.2, font=None):
    estilos = {
        "primario": (CORAL, BLANCO, None),
        "oscuro": (G900, BLANCO, None),
        "secundario": (BLANCO, G700, G200),
        "suave": (CORAL_SUAVE, CORAL, None),
        "verde": (VERDE, BLANCO, None),
        "peligro": (BLANCO, ROJO, "#FCA5A5"),
    }
    fill, fg, edge = estilos[tipo]
    caja(ax, x, y, w, h, fill=fill, edge=edge or "none",
         lw=0.8 if edge else 0, r=0.7)
    texto(ax, x + w / 2, y + h / 2, etiqueta, size=size, color=fg, bold=True,
          font=font or F, ha="center", va="center")


def campo(ax, x, y, w, h, marcador, etiqueta=None, valor=None, size=6.8,
          desplegable=False):
    if etiqueta:
        texto(ax, x, y + h + 1.5, etiqueta, size=6.2, color=G700, bold=True, font=F)
    caja(ax, x, y, w, h, fill=G50, edge=G200, lw=0.8, r=0.7)
    texto(ax, x + 1.4, y + h / 2, valor or marcador, size=size,
          color=G900 if valor else G400, font=F, va="center")
    if desplegable:
        texto(ax, x + w - 1.6, y + h / 2, "▾", size=6.4, color=G600, font=ICO,
              ha="right", va="center")


def chip(ax, x, y, w, h, etiqueta, fill=BLANCO, fg=G700, edge=G200, size=6.2,
         bold=False, font=None):
    caja(ax, x, y, w, h, fill=fill, edge=edge or "none", lw=0.8 if edge else 0, r=0.6)
    texto(ax, x + w / 2, y + h / 2, etiqueta, size=size, color=fg, bold=bold,
          font=font or F, ha="center", va="center")


def marcador_imagen(ax, x, y, w, h, etiqueta="", fill=G100, r=1.0):
    caja(ax, x, y, w, h, fill=fill, edge=G200, lw=0.7, r=r)
    cx, cy = x + w / 2, y + h / 2
    s = min(w, h) * 0.20
    ax.add_patch(Polygon([[cx - s, cy - s * 0.6], [cx - s * 0.25, cy + s * 0.35],
                          [cx + s * 0.15, cy - s * 0.1], [cx + s, cy - s * 0.6]],
                         closed=True, facecolor=G300, edgecolor="none", zorder=4))
    ax.add_patch(Circle((cx - s * 0.45, cy + s * 0.55), s * 0.20, color=G300, zorder=4))
    if etiqueta:
        texto(ax, cx, y + 1.4, etiqueta, size=5.6, color=G400, font=F, ha="center")


def prenda(ax, x, y, w, h, color=G200, borde=G400):
    """Silueta simple de polo, para las vistas previas del personalizador."""
    p = [(0.14, 0.00), (0.14, 0.60), (0.00, 0.74), (0.09, 0.90), (0.30, 1.00),
         (0.42, 0.92), (0.58, 0.92), (0.70, 1.00), (0.91, 0.90), (1.00, 0.74),
         (0.86, 0.60), (0.86, 0.00)]
    pts = [(x + px * w, y + py * h) for px, py in p]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=borde,
                         lw=0.9, zorder=3))


def estrellas(ax, x, y, n=5, size=5.6, color=AMBER):
    texto(ax, x, y, "★" * n, size=size, color=color, font=ICO, va="center")


def titulo_pantalla(ax, codigo, nombre, alto=H):
    """Etiqueta de la figura, en la franja reservada sobre el navegador."""
    texto(ax, 0.5, alto - 3.4, f"{codigo}  ·  {nombre}", size=7.4, color=CORAL,
          bold=True, font=F, va="center")


# ------------------------------------------------ cabecera de la tienda
def header_tienda(ax, y_top, buscador=True, activo=None):
    """Banner promocional + cabecera + navegacion. Devuelve la y inferior."""
    y = y_top - 3.4
    caja(ax, 0.5, y, W - 1, 3.4, fill=CORAL, r=0.4)
    texto(ax, W / 2, y + 1.7, "Envío gratis en pedidos desde S/ 150   ·   "
          "Estampa tu diseño desde una unidad", size=6.2, color=BLANCO,
          font=F, ha="center", va="center")

    y2 = y - 7.2
    caja(ax, 0.5, y2, W - 1, 7.2, fill=BLANCO, r=0.4)
    texto(ax, 4.0, y2 + 3.6, "Coral", size=15, color=CORAL, bold=True, font=F,
          va="center")
    if buscador:
        caja(ax, 20, y2 + 2.0, 62, 3.4, fill=BLANCO, edge=G200, lw=0.8, r=0.8)
        icono_lupa(ax, 22.0, y2 + 3.7)
        texto(ax, 24.8, y2 + 3.7, "Buscar polos, poleras, gorras…", size=6.6,
              color=G400, font=F, va="center")
    texto(ax, W - 16, y2 + 3.6, "♡", size=9, color=G700, font=ICO,
          ha="center", va="center")
    icono_usuario(ax, W - 11, y2 + 3.6)
    icono_carrito(ax, W - 6, y2 + 3.6)
    ax.add_patch(Circle((W - 4.2, y2 + 5.1), 1.15, color=CORAL, zorder=6))
    texto(ax, W - 4.2, y2 + 5.1, "3", size=5.4, color=BLANCO, bold=True, font=F,
          ha="center", va="center", z=7)

    y3 = y2 - 4.0
    caja(ax, 0.5, y3, W - 1, 4.0, fill=BLANCO, r=0.4)
    ax.plot([0.5, W - 0.5], [y3, y3], color=G200, lw=0.8, zorder=4)
    enlaces = ["Polos", "Poleras", "Gorras", "Tote bags", "Personaliza tu prenda"]
    x = 4.0
    for e in enlaces:
        es_activo = (e == activo)
        col = CORAL if es_activo or e.startswith("Personaliza") else G700
        texto(ax, x, y3 + 2.0, e, size=6.6, color=col,
              bold=es_activo or e.startswith("Personaliza"), font=F, va="center")
        if es_activo:
            ax.plot([x, x + len(e) * 0.95], [y3 + 0.5, y3 + 0.5], color=CORAL, lw=1.2)
        x += len(e) * 1.05 + 7.5
    return y3


# ============================================================ B.1 · HOME
def b1_home():
    fig, ax, y = pantalla("coral-shop.pe")
    titulo_pantalla(ax, "B.1", "Portada de la tienda")
    y = header_tienda(ax, y)

    # hero
    caja(ax, 0.5, y - 34, W - 1, 34, fill=ROSE_50, r=0.4)
    caja(ax, 0.5, y - 34, (W - 1) * 0.55, 34, fill=ORANGE_50, r=0.4, alpha=0.55)
    chip(ax, 5, y - 7.5, 27, 3.4, "✦  Colección 2026", fill=CORAL_SUAVE,
         fg=CORAL, edge=None, size=6.4, bold=True, font=ICO)
    texto(ax, 5, y - 13.5, "Diseña tu propia prenda", size=18, color=G900,
          bold=True, font=F, va="center")
    texto(ax, 5, y - 19.5, "y recíbela en 72 horas", size=18, color=CORAL,
          bold=True, font=F, va="center")
    texto(ax, 5, y - 25.5,
          "Elige el polo, la talla y el color, sube tu diseño y mira cómo\n"
          "queda antes de pagar. Sin pedido mínimo.",
          size=7.0, color=G600, font=F, va="center", lh=1.45)
    boton(ax, 5, y - 32.5, 24, 4.6, "Personalizar ahora", "primario", size=7.4)
    boton(ax, 31, y - 32.5, 20, 4.6, "Ver catálogo", "secundario", size=7.4)
    marcador_imagen(ax, 84, y - 31.5, 58, 28, "hero.jpg", fill="#FDE8E2", r=2.0)

    # categorias
    texto(ax, W / 2, y - 39.5, "Compra por categoría", size=11, color=G900,
          bold=True, font=F, ha="center", va="center")
    cats = [("Polos", "128 modelos"), ("Poleras", "76 modelos"),
            ("Gorras", "34 modelos"), ("Tote bags", "22 modelos")]
    for i, (n, c) in enumerate(cats):
        x = 5 + i * 34.5
        marcador_imagen(ax, x, y - 66, 31, 22, "", fill=G100, r=1.6)
        caja(ax, x, y - 66, 31, 8, fill=G700, r=1.6, alpha=0.82)
        texto(ax, x + 2.2, y - 61.5, n, size=8.4, color=BLANCO, bold=True, font=F,
              va="center")
        chip(ax, x + 2.2, y - 65.2, 15, 2.6, c, fill=BLANCO, fg=G700, edge=None,
             size=5.4)

    guardar(fig, ruta("B1_home.png"))


# ======================================================== B.2 · CATALOGO
def b2_catalogo():
    fig, ax, y = pantalla("coral-shop.pe/productos?categoria=polos", alto=126)
    titulo_pantalla(ax, "B.2", "Catálogo con filtros (M01)", alto=126)
    y = header_tienda(ax, y, activo="Polos")

    texto(ax, 5, y - 3.5, "Inicio  ›  Polos", size=6.0, color=G400, font=F, va="center")
    texto(ax, 5, y - 8.5, "Polos", size=13, color=G900, bold=True, font=F, va="center")
    texto(ax, 20, y - 8.0, "128 productos", size=6.6, color=G600, font=F, va="center")
    campo(ax, W - 38, y - 10.5, 33, 3.6, "", valor="Ordenar por:  Más relevantes", desplegable=True)
    texto(ax, W - 8, y - 8.7, "▾", size=7, color=G600, font=ICO, va="center")

    # panel de filtros
    fx, fy, fw = 5, 20, 32
    caja(ax, fx, fy, fw, y - 33, fill=G50, edge=G200, lw=0.8, r=1.0)
    yy = y - 15
    texto(ax, fx + 2, yy, "Filtros", size=8.4, color=G900, bold=True, font=F, va="center")
    texto(ax, fx + fw - 2, yy, "Limpiar", size=6.0, color=CORAL, font=F,
          ha="right", va="center")

    yy -= 5
    texto(ax, fx + 2, yy, "CATEGORÍA", size=5.8, color=G500, bold=True, font=F, va="center")
    for i, (c, n) in enumerate([("Polos", 128), ("Poleras", 76), ("Gorras", 34),
                                ("Tote bags", 22)]):
        yy -= 3.6
        marcado = i == 0
        caja(ax, fx + 2, yy - 1.0, 2.0, 2.0, fill=CORAL if marcado else BLANCO,
             edge=G300, lw=0.7, r=0.3)
        if marcado:
            texto(ax, fx + 3.0, yy, "✓", size=5.0, color=BLANCO, bold=True,
                  font=ICO, ha="center", va="center")
        texto(ax, fx + 5.4, yy, c, size=6.4, color=G700, font=F, va="center")
        texto(ax, fx + fw - 2, yy, str(n), size=6.0, color=G400, font=F,
              ha="right", va="center")

    yy -= 6
    texto(ax, fx + 2, yy, "TALLA", size=5.8, color=G500, bold=True, font=F, va="center")
    yy -= 4.2
    for i, t in enumerate(["XS", "S", "M", "L", "XL", "XXL"]):
        sel = t in ("M", "L")
        chip(ax, fx + 2 + i * 4.9, yy - 1.4, 4.2, 3.0, t,
             fill=CORAL if sel else BLANCO, fg=BLANCO if sel else G700,
             edge=None if sel else G200, size=5.6, bold=sel)

    yy -= 7
    texto(ax, fx + 2, yy, "COLOR", size=5.8, color=G500, bold=True, font=F, va="center")
    yy -= 4.0
    for i, c in enumerate(["#111827", "#FFFFFF", CORAL, "#2563EB", "#16A34A", "#F59E0B"]):
        cx = fx + 3.4 + i * 4.9
        ax.add_patch(Circle((cx, yy), 1.5, facecolor=c, edgecolor=G300, lw=0.7, zorder=5))
        if i == 0:
            ax.add_patch(Circle((cx, yy), 2.2, facecolor="none", edgecolor=CORAL,
                                lw=1.0, zorder=5))

    yy -= 7
    texto(ax, fx + 2, yy, "PRECIO", size=5.8, color=G500, bold=True, font=F, va="center")
    yy -= 4.0
    ax.plot([fx + 2, fx + fw - 2], [yy, yy], color=G300, lw=1.4, zorder=4)
    ax.plot([fx + 6, fx + fw - 8], [yy, yy], color=CORAL, lw=1.4, zorder=5)
    for px in (fx + 6, fx + fw - 8):
        ax.add_patch(Circle((px, yy), 1.1, facecolor=BLANCO, edgecolor=CORAL,
                            lw=1.0, zorder=6))
    texto(ax, fx + 2, yy - 3.2, "S/ 35", size=5.8, color=G600, font=F, va="center")
    texto(ax, fx + fw - 2, yy - 3.2, "S/ 120", size=5.8, color=G600, font=F,
          ha="right", va="center")

    yy -= 8
    caja(ax, fx + 2, yy - 1.6, 5.6, 3.0, fill=CORAL, r=1.5)
    ax.add_patch(Circle((fx + 6.0, yy - 0.1), 1.15, color=BLANCO, zorder=6))
    texto(ax, fx + 9.4, yy - 0.1, "Solo personalizables", size=6.2, color=G700,
          bold=True, font=F, va="center")

    # rejilla de productos
    prods = [("Polo urbano oversize", "45.00", "4.8", True),
             ("Polera con capucha", "89.00", "4.9", True),
             ("Polo básico algodón", "35.00", "4.6", False),
             ("Polo manga larga", "59.00", "4.7", True),
             ("Polera cuello redondo", "79.00", "4.5", True),
             ("Polo tie dye", "52.00", "4.8", False)]
    for i, (n, p, r, pers) in enumerate(prods):
        fila, col = divmod(i, 3)
        px = 41 + col * 34.5
        py = y - 42 - fila * 32
        caja(ax, px, py, 31.5, 29, fill=G50, edge=G200, lw=0.7, r=1.4)
        marcador_imagen(ax, px + 1.2, py + 10.5, 29.1, 17.3, "", fill=BLANCO, r=1.2)
        if pers:
            chip(ax, px + 2.4, py + 24.5, 15, 2.6, "Personalizable",
                 fill=CORAL_SUAVE, fg=CORAL, edge=None, size=5.0, bold=True)
        texto(ax, px + 2, py + 7.6, n, size=7.0, color=G900, bold=True, font=F, va="center")
        estrellas(ax, px + 2, py + 4.6, 5, size=5.0)
        texto(ax, px + 9.5, py + 4.6, f"{r}  ·  62 reseñas", size=5.4, color=G600,
              font=F, va="center")
        texto(ax, px + 2, py + 1.8, f"S/ {p}", size=8.6, color=CORAL, bold=True,
              font=F, va="center")
        boton(ax, px + 17, py + 0.6, 13, 3.4, "Ver detalle", "oscuro", size=5.8)

    # paginacion
    for i, e in enumerate(["‹", "1", "2", "3", "…", "11", "›"]):
        chip(ax, 78 + i * 5.2, 13, 4.4, 3.2, e,
             fill=CORAL if e == "1" else BLANCO, fg=BLANCO if e == "1" else G700,
             edge=None if e == "1" else G200, size=5.8, bold=e == "1", font=ICO)
    guardar(fig, ruta("B2_catalogo.png"))


# =================================================== B.3 · FICHA PRODUCTO
def b3_producto():
    fig, ax, y = pantalla("coral-shop.pe/producto/polo-urbano-oversize", alto=118)
    titulo_pantalla(ax, "B.3", "Ficha de producto: talla, color y stock real (M02)",
                    alto=118)
    y = header_tienda(ax, y, activo="Polos")

    texto(ax, 5, y - 3.5, "Inicio  ›  Polos  ›  Polo urbano oversize", size=6.0,
          color=G400, font=F, va="center")

    # galeria
    caja(ax, 5, 20, 58, y - 27, fill=G50, edge=G200, lw=0.8, r=1.4)
    prenda(ax, 17, 26, 34, y - 40, color=BLANCO, borde=G300)
    caja(ax, 27, y - 36, 14, 10, fill=G200, r=0.5, z=5)
    texto(ax, 34, y - 31, "tu diseño", size=5.4, color=G500, font=F,
          ha="center", va="center", z=6)
    for i in range(4):
        marcador_imagen(ax, 5 + i * 15, 8, 13, 10, "", fill=G50, r=0.8)
    ax.add_patch(FancyBboxPatch((5.4, 8.4), 12.2, 9.2,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor="none", edgecolor=CORAL, lw=1.1, zorder=6))

    # panel de compra
    px = 68
    chip(ax, px, y - 6.5, 12, 3.0, "POLOS", fill=G100, fg=G600, edge=None,
         size=5.4, bold=True)
    texto(ax, px, y - 11.5, "Polo urbano oversize", size=13, color=G900, bold=True,
          font=F, va="center")
    chip(ax, px, y - 16.5, 11, 3.2, "★ 4.8", fill=AMBER_50, fg=AMBER_700,
         edge=None, size=6.0, bold=True, font=ICO)
    texto(ax, px + 12.5, y - 14.9, "62 reseñas verificadas", size=6.2, color=G500,
          font=F, va="center")
    texto(ax, px, y - 22, "S/ 45.00", size=17, color=G900, bold=True, font=F, va="center")

    yy = y - 28
    texto(ax, px, yy, "COLOR:  Negro", size=6.0, color=G700, bold=True, font=F, va="center")
    for i, c in enumerate(["#111827", "#FFFFFF", CORAL, "#2563EB"]):
        cx = px + 2.2 + i * 6.0
        ax.add_patch(Circle((cx, yy - 5.2), 2.0, facecolor=c, edgecolor=G300,
                            lw=0.8, zorder=5))
        if i == 0:
            ax.add_patch(Circle((cx, yy - 5.2), 2.9, facecolor="none",
                                edgecolor=CORAL, lw=1.1, zorder=5))

    yy -= 11
    texto(ax, px, yy, "TALLA", size=6.0, color=G700, bold=True, font=F, va="center")
    texto(ax, W - 6, yy, "Guía de tallas", size=6.0, color=CORAL, font=F,
          ha="right", va="center")
    for i, (t, estado) in enumerate([("XS", "ok"), ("S", "ok"), ("M", "sel"),
                                     ("L", "ok"), ("XL", "no"), ("XXL", "ok")]):
        cx = px + i * 7.2
        if estado == "sel":
            chip(ax, cx, yy - 8.4, 6.2, 4.4, t, fill=CORAL, fg=BLANCO, edge=None,
                 size=6.4, bold=True)
        elif estado == "no":
            chip(ax, cx, yy - 8.4, 6.2, 4.4, t, fill=G100, fg=G400, edge=G200,
                 size=6.4)
            ax.plot([cx + 0.7, cx + 5.5], [yy - 7.9, yy - 3.9], color=G400, lw=0.8,
                    zorder=7)
        else:
            chip(ax, cx, yy - 8.4, 6.2, 4.4, t, fill=BLANCO, fg=G700, edge=G200,
                 size=6.4)
    texto(ax, px, yy - 12.0, "⚠  Quedan 3 unidades de la talla M en negro",
          size=6.2, color=AMBER_700, bold=True, font=ICO, va="center")

    yy -= 18
    texto(ax, px, yy + 1.0, "CANTIDAD", size=6.0, color=G700, bold=True, font=F, va="center")
    caja(ax, px, yy - 5.0, 16, 4.4, fill=BLANCO, edge=G200, lw=0.8, r=0.7)
    for i, s in enumerate(["–", "1", "+"]):
        texto(ax, px + 2.7 + i * 5.3, yy - 2.8, s, size=7.4,
              color=G900 if s == "1" else G600, bold=True, font=F,
              ha="center", va="center")

    boton(ax, px, 13.5, 36, 5.4, "Agregar al carrito", "oscuro", size=8.0)
    boton(ax, px + 38, 13.5, 36, 5.4, "✎  Personalizar estampado", "primario",
          size=8.0, font=ICO)
    texto(ax, px, 9.0, "♡  Guardar en favoritos", size=6.2, color=G600,
          font=ICO, va="center")
    texto(ax, px, 4.5, "Entrega en Lima en 72 h  ·  Cambios gratis dentro de 7 días",
          size=6.0, color=G500, font=F, va="center")
    guardar(fig, ruta("B3_producto.png"))


# ================================================== B.4 · PERSONALIZADOR
def b4_personalizador():
    fig, ax, y = pantalla("coral-shop.pe/personalizar/polo-urbano-oversize", alto=116)
    titulo_pantalla(ax, "B.4", "Personalizador de estampado (M03)", alto=116)
    y = header_tienda(ax, y, activo=None)

    texto(ax, 5, y - 4.5, "Personaliza tu polo urbano oversize", size=12,
          color=G900, bold=True, font=F, va="center")

    # vista previa
    caja(ax, 5, 6, 56, y - 14, fill=G50, edge=G200, lw=0.8, r=1.4)
    texto(ax, 7, y - 9.5, "VISTA PREVIA", size=5.8, color=G500, bold=True, font=F, va="center")
    for i, (t, sel) in enumerate([("Frente", True), ("Espalda", False)]):
        chip(ax, 40 + i * 10.5, y - 11.2, 9.5, 3.2, t,
             fill=G900 if sel else BLANCO, fg=BLANCO if sel else G700,
             edge=None if sel else G200, size=5.8, bold=sel)
    prenda(ax, 14, 12, 38, y - 28, color=G900, borde=G700)
    caja(ax, 25.5, y - 36, 15, 11, fill=BLANCO, edge=CORAL, lw=1.1, r=0.5, z=6)
    texto(ax, 33, y - 30.5, "CORAL", size=8.5, color=CORAL, bold=True, font=F,
          ha="center", va="center", z=7)
    texto(ax, 33, y - 34, "desde 2021", size=4.8, color=G600, font=F,
          ha="center", va="center", z=7)
    for dx in (25.5, 40.5):
        for dy in (y - 36, y - 25):
            ax.add_patch(Circle((dx, dy), 0.6, facecolor=BLANCO, edgecolor=CORAL,
                                lw=0.9, zorder=8))
    texto(ax, 33, 8.5, "Área imprimible A4  ·  21 × 29,7 cm", size=5.6,
          color=G500, font=F, ha="center", va="center")

    # panel de configuracion
    px, pw = 65, 78
    yy = y - 8
    pasos = [
        ("1", "Zona del estampado",
         [("Pecho frontal", True, "+S/ 0"), ("Espalda completa", False, "+S/ 6"),
          ("Manga", False, "+S/ 4"), ("Pecho izquierdo", False, "+S/ 0")]),
        ("2", "Técnica",
         [("DTF full color", True, "S/ 12"), ("Serigrafía", False, "S/ 9"),
          ("Vinil textil", False, "S/ 10"), ("Bordado", False, "S/ 22")]),
    ]
    for num, titulo, opciones in pasos:
        chip(ax, px, yy - 2.6, 3.4, 3.4, num, fill=CORAL, fg=BLANCO, edge=None,
             size=6.0, bold=True)
        texto(ax, px + 5, yy - 0.9, titulo, size=7.6, color=G900, bold=True,
              font=F, va="center")
        for i, (op, sel, precio) in enumerate(opciones):
            ox = px + (i % 4) * 19.6
            caja(ax, ox, yy - 9.6, 18.4, 5.6, fill=CORAL_SUAVE if sel else BLANCO,
                 edge=CORAL if sel else G200, lw=1.0 if sel else 0.8, r=0.7)
            texto(ax, ox + 1.4, yy - 6.0, op, size=5.9,
                  color=CORAL if sel else G700, bold=sel, font=F, va="center")
            texto(ax, ox + 1.4, yy - 8.4, precio, size=5.4, color=G500, font=F, va="center")
        yy -= 15.5

    chip(ax, px, yy - 2.6, 3.4, 3.4, "3", fill=CORAL, fg=BLANCO, edge=None,
         size=6.0, bold=True)
    texto(ax, px + 5, yy - 0.9, "Tamaño", size=7.6, color=G900, bold=True, font=F, va="center")
    for i, (t, med, sel) in enumerate([("A5", "14,8 × 21 cm", False),
                                       ("A4", "21 × 29,7 cm", True),
                                       ("A3", "29,7 × 42 cm", False)]):
        ox = px + i * 19.6
        caja(ax, ox, yy - 9.6, 18.4, 5.6, fill=CORAL_SUAVE if sel else BLANCO,
             edge=CORAL if sel else G200, lw=1.0 if sel else 0.8, r=0.7)
        texto(ax, ox + 1.4, yy - 6.0, t, size=6.4, color=CORAL if sel else G700,
              bold=True, font=F, va="center")
        texto(ax, ox + 1.4, yy - 8.4, med, size=5.2, color=G500, font=F, va="center")
    yy -= 15.5

    chip(ax, px, yy - 2.6, 3.4, 3.4, "4", fill=CORAL, fg=BLANCO, edge=None,
         size=6.0, bold=True)
    texto(ax, px + 5, yy - 0.9, "Tu diseño", size=7.6, color=G900, bold=True,
          font=F, va="center")
    caja(ax, px, yy - 13.5, 37, 9.6, fill=G50, edge=G300, lw=0.9, r=0.8, ls=(0, (3, 2)))
    texto(ax, px + 18.5, yy - 7.2, "⬆  Arrastra tu imagen o haz clic", size=6.2,
          color=G600, bold=True, font=ICO, ha="center", va="center")
    texto(ax, px + 18.5, yy - 10.4, "PNG o JPG · máx. 5 MB · mín. 300 dpi",
          size=5.4, color=G400, font=F, ha="center", va="center")
    campo(ax, px + 40, yy - 8.0, 38, 4.0, "", etiqueta="O escribe un texto",
          valor="CORAL desde 2021")
    campo(ax, px + 40, yy - 13.5, 22, 4.0, "", valor="Fuente:  Anton")
    caja(ax, px + 64, yy - 13.5, 14, 4.0, fill=BLANCO, edge=G200, lw=0.8, r=0.7)
    ax.add_patch(Circle((px + 66.5, yy - 11.5), 1.3, facecolor=CORAL,
                        edgecolor=G300, lw=0.7, zorder=6))
    texto(ax, px + 69, yy - 11.5, "#FF5331", size=5.4, color=G700, font=F, va="center")

    # resumen de precio
    caja(ax, px, 4, pw, 14, fill=G900, r=1.0)
    filas = [("Polo urbano oversize · Talla M · Negro", "S/ 45.00"),
             ("Estampado DTF · A4 · Pecho frontal", "S/ 18.50")]
    for i, (k, v) in enumerate(filas):
        texto(ax, px + 2.5, 15.2 - i * 3.0, k, size=6.0, color="#D1D5DB", font=F,
              va="center", z=6)
        texto(ax, px + 40, 15.2 - i * 3.0, v, size=6.0, color=BLANCO, font=F,
              ha="right", va="center", z=6)
    ax.plot([px + 2.5, px + 40], [10.2, 10.2], color="#374151", lw=0.8, zorder=6)
    texto(ax, px + 2.5, 7.2, "Total por unidad", size=7.0, color=BLANCO, bold=True,
          font=F, va="center", z=6)
    texto(ax, px + 40, 7.2, "S/ 63.50", size=10, color=CORAL, bold=True, font=F,
          ha="right", va="center", z=6)
    boton(ax, px + 44, 6.5, 15, 5.0, "Guardar diseño", "secundario", size=6.4)
    boton(ax, px + 60.5, 6.5, 17.5, 5.0, "Agregar al carrito", "primario", size=6.8)
    guardar(fig, ruta("B4_personalizador.png"))


# ========================================================= B.5 · CARRITO
def b5_carrito():
    fig, ax, y = pantalla("coral-shop.pe/carrito")
    titulo_pantalla(ax, "B.5", "Carrito de compras (M04 y M07)")
    y = header_tienda(ax, y)

    texto(ax, 5, y - 5, "Tu carrito", size=13, color=G900, bold=True, font=F, va="center")
    texto(ax, 27, y - 4.6, "3 productos", size=6.6, color=G600, font=F, va="center")

    cab = ["PRODUCTO", "PRECIO UNIT.", "CANTIDAD", "SUBTOTAL"]
    xs = [12, 62, 80, 95]
    for c, x in zip(cab, xs):
        texto(ax, x, y - 10, c, size=5.6, color=G500, bold=True, font=F, va="center")
    ax.plot([5, 108], [y - 12, y - 12], color=G200, lw=0.8, zorder=4)

    lineas = [
        ("Polo urbano oversize", "Talla M · Negro", True,
         "DTF · A4 · Pecho frontal", "63.50", "2", "127.00"),
        ("Polera con capucha", "Talla L · Coral", False, "", "89.00", "1", "89.00"),
        ("Gorra clásica", "Talla única · Negro", False, "", "39.00", "1", "39.00"),
    ]
    yy = y - 15
    for nombre, variante, pers, detalle, unit, cant, sub in lineas:
        alto = 15 if pers else 12
        marcador_imagen(ax, 5, yy - alto + 1.5, 11, alto - 3, "", fill=G50, r=0.8)
        texto(ax, 18, yy - 3.2, nombre, size=7.2, color=G900, bold=True, font=F, va="center")
        texto(ax, 18, yy - 6.4, variante, size=6.0, color=G600, font=F, va="center")
        if pers:
            chip(ax, 18, yy - 11.6, 13, 3.0, "Personalizado", fill=CORAL_SUAVE,
                 fg=CORAL, edge=None, size=5.2, bold=True)
            texto(ax, 32.5, yy - 10.1, detalle, size=5.6, color=G600, font=F, va="center")
            texto(ax, 32.5, yy - 13.2, "Ver diseño", size=5.6, color=CORAL, font=F, va="center")
        texto(ax, 62, yy - 5, f"S/ {unit}", size=6.8, color=G700, font=F, va="center")
        caja(ax, 79, yy - 7, 13, 4.0, fill=BLANCO, edge=G200, lw=0.8, r=0.6)
        for i, s in enumerate(["–", cant, "+"]):
            texto(ax, 81.2 + i * 4.3, yy - 5, s, size=6.6,
                  color=G900 if s == cant else G600, bold=True, font=F,
                  ha="center", va="center")
        texto(ax, 95, yy - 5, f"S/ {sub}", size=7.4, color=G900, bold=True, font=F, va="center")
        texto(ax, 109, yy - 5, "✕", size=6.4, color=G400, font=ICO, ha="right", va="center")
        ax.plot([5, 108], [yy - alto, yy - alto], color=G200, lw=0.7, zorder=4)
        yy -= alto

    texto(ax, 5, yy - 4, "←  Seguir comprando", size=6.6, color=CORAL, bold=True,
          font=ICO, va="center")

    # resumen
    rx = 113
    caja(ax, rx, 8, 30, y - 9, fill=G50, edge=G200, lw=0.8, r=1.2)
    texto(ax, rx + 2, y - 5, "Resumen", size=8.6, color=G900, bold=True, font=F, va="center")
    campo(ax, rx + 2, y - 13, 18, 4.0, "Código de cupón")
    boton(ax, rx + 21, y - 13, 7, 4.0, "Aplicar", "oscuro", size=5.6)
    chip(ax, rx + 2, y - 18, 26, 3.4, "✓  COLECCION10  ·  10 %", fill=VERDE_50,
         fg=VERDE, edge=None, size=5.6, bold=True, font=ICO)
    resumen = [("Subtotal", "S/ 255.00"), ("Descuento (10 %)", "− S/ 25.50"),
               ("Envío (Lima, 72 h)", "S/ 12.00")]
    yy2 = y - 24
    for k, v in resumen:
        texto(ax, rx + 2, yy2, k, size=6.2, color=G600, font=F, va="center")
        texto(ax, rx + 28, yy2, v, size=6.2, color=G900, font=F, ha="right", va="center")
        yy2 -= 4.2
    ax.plot([rx + 2, rx + 28], [yy2 + 1.5, yy2 + 1.5], color=G300, lw=0.8, zorder=5)
    texto(ax, rx + 2, yy2 - 2.5, "Total", size=8.0, color=G900, bold=True, font=F, va="center")
    texto(ax, rx + 28, yy2 - 2.5, "S/ 241.50", size=10, color=CORAL, bold=True,
          font=F, ha="right", va="center")
    boton(ax, rx + 2, 14, 26, 5.4, "Ir a pagar", "primario", size=8.0)
    texto(ax, rx + 15, 11, "Pago seguro  ·  Yape, Plin y tarjeta", size=5.4,
          color=G500, font=F, ha="center", va="center")
    guardar(fig, ruta("B5_carrito.png"))


# ======================================================== B.6 · CHECKOUT
def b6_checkout():
    fig, ax, y = pantalla("coral-shop.pe/checkout", alto=120)
    titulo_pantalla(ax, "B.6", "Checkout en tres pasos (M06)", alto=120)
    y = header_tienda(ax, y, buscador=False)

    # stepper
    pasos = [("1", "Entrega", "hecho"), ("2", "Envío", "hecho"), ("3", "Pago", "activo")]
    sx = 13
    for i, (n, t, estado) in enumerate(pasos):
        cx = sx + i * 31
        col = VERDE if estado == "hecho" else CORAL
        ax.add_patch(Circle((cx, y - 6), 2.6, facecolor=col, edgecolor="none", zorder=6))
        texto(ax, cx, y - 6, "✓" if estado == "hecho" else n, size=6.4, color=BLANCO,
              bold=True, font=ICO if estado == "hecho" else F,
              ha="center", va="center", z=7)
        texto(ax, cx + 4.2, y - 6, t, size=7.4, color=G900 if estado != "pend" else G400,
              bold=True, font=F, va="center")
        if i < 2:
            ax.plot([cx + 15, cx + 28], [y - 6, y - 6], color=VERDE, lw=1.4, zorder=4)

    # datos confirmados
    yy = y - 14
    for titulo, valor in [("Entrega", "Av. Brasil 1234, Jesús María, Lima  ·  Recibe: Diego D."),
                          ("Envío", "Delivery Lima  ·  72 horas hábiles  ·  S/ 12.00")]:
        caja(ax, 5, yy - 6.4, 88, 6.4, fill=VERDE_50, edge="#BBF7D0", lw=0.8, r=0.8)
        texto(ax, 7, yy - 3.2, "✓", size=7.0, color=VERDE, bold=True, font=ICO, va="center")
        texto(ax, 11, yy - 3.2, f"{titulo}:", size=6.4, color=G900, bold=True,
              font=F, va="center")
        texto(ax, 11 + len(titulo) * 1.3 + 2.5, yy - 3.2, valor, size=6.4,
              color=G700, font=F, va="center")
        texto(ax, 91, yy - 3.2, "Editar", size=6.0, color=CORAL, font=F,
              ha="right", va="center")
        yy -= 8.2

    # paso activo: pago
    caja(ax, 5, 8, 88, yy - 8.5, fill=BLANCO, edge=CORAL, lw=1.1, r=1.0)
    texto(ax, 7, yy - 5, "Método de pago", size=9.0, color=G900, bold=True,
          font=F, va="center")
    metodos = [("Tarjeta de crédito o débito", "Visa, Mastercard, Amex", True),
               ("Yape", "Escanea el QR desde tu app", False),
               ("Plin", "Transferencia inmediata", False),
               ("Pago contra entrega", "Solo Lima Metropolitana", False)]
    my = yy - 10
    for nombre, det, sel in metodos:
        caja(ax, 7, my - 6.2, 84, 6.2, fill=CORAL_SUAVE if sel else G50,
             edge=CORAL if sel else G200, lw=1.0 if sel else 0.8, r=0.7)
        ax.add_patch(Circle((10.5, my - 3.1), 1.5, facecolor=BLANCO,
                            edgecolor=CORAL if sel else G300, lw=1.0, zorder=6))
        if sel:
            ax.add_patch(Circle((10.5, my - 3.1), 0.8, facecolor=CORAL, zorder=7))
        texto(ax, 14.5, my - 3.1, nombre, size=6.6, color=G900, bold=True, font=F, va="center")
        texto(ax, 50, my - 3.1, det, size=6.0, color=G600, font=F, va="center")
        my -= 7.6

    campo(ax, 7, my - 7.6, 40, 4.4, "", etiqueta="Número de tarjeta",
          valor="4111  ····  ····  1234")
    campo(ax, 49, my - 7.6, 18, 4.4, "", etiqueta="Vencimiento", valor="08/29")
    campo(ax, 69, my - 7.6, 12, 4.4, "", etiqueta="CVV", valor="···")
    texto(ax, 7, my - 11.6, "Simulación de pasarela de pagos para la demostración",
          size=5.8, color=G500, italic=True, font=F, va="center")

    # resumen
    rx = 97
    caja(ax, rx, 8, 46, y - 9, fill=G50, edge=G200, lw=0.8, r=1.2)
    texto(ax, rx + 2.5, y - 5, "Tu pedido", size=8.6, color=G900, bold=True, font=F, va="center")
    items = [("Polo urbano oversize", "M · Negro · Personalizado", "×2", "S/ 127.00"),
             ("Polera con capucha", "L · Coral", "×1", "S/ 89.00"),
             ("Gorra clásica", "Única · Negro", "×1", "S/ 39.00")]
    iy = y - 11
    for n, v, c, p in items:
        marcador_imagen(ax, rx + 2.5, iy - 8.5, 8, 8, "", fill=BLANCO, r=0.6)
        texto(ax, rx + 12, iy - 2.6, n, size=6.4, color=G900, bold=True, font=F, va="center")
        texto(ax, rx + 12, iy - 5.4, v, size=5.6, color=G600, font=F, va="center")
        texto(ax, rx + 12, iy - 8.0, c, size=5.6, color=G500, font=F, va="center")
        texto(ax, rx + 43.5, iy - 4.5, p, size=6.6, color=G900, bold=True, font=F,
              ha="right", va="center")
        iy -= 10
    ax.plot([rx + 2.5, rx + 43.5], [iy + 1, iy + 1], color=G300, lw=0.8, zorder=5)
    for k, v, col in [("Subtotal", "S/ 255.00", G600),
                      ("Descuento COLECCION10", "− S/ 25.50", VERDE),
                      ("Envío", "S/ 12.00", G600)]:
        iy -= 4.2
        texto(ax, rx + 2.5, iy, k, size=6.2, color=col, font=F, va="center")
        texto(ax, rx + 43.5, iy, v, size=6.2, color=col, font=F, ha="right", va="center")
    texto(ax, rx + 2.5, iy - 6, "Total", size=8.6, color=G900, bold=True, font=F, va="center")
    texto(ax, rx + 43.5, iy - 6, "S/ 241.50", size=11, color=CORAL, bold=True,
          font=F, ha="right", va="center")
    boton(ax, rx + 2.5, 13, 41, 5.6, "Confirmar pedido", "primario", size=8.4)
    texto(ax, rx + 23, 10, "Al confirmar aceptas los términos y la política de cambios",
          size=5.2, color=G500, font=F, ha="center", va="center")
    guardar(fig, ruta("B6_checkout.png"))


# ==================================================== B.7 · CONFIRMACION
def b7_confirmacion():
    fig, ax, y = pantalla("coral-shop.pe/pedido/CS-2026-000123", alto=80)
    titulo_pantalla(ax, "B.7", "Confirmación y seguimiento del pedido (M06 y M08)", alto=80)
    y = header_tienda(ax, y, buscador=False)

    ax.add_patch(Circle((W / 2, y - 10), 5.0, facecolor=VERDE_50,
                        edgecolor=VERDE, lw=1.2, zorder=5))
    texto(ax, W / 2, y - 10, "✓", size=15, color=VERDE, bold=True, font=ICO,
          ha="center", va="center", z=6)
    texto(ax, W / 2, y - 19, "¡Pedido confirmado!", size=15, color=G900, bold=True,
          font=F, ha="center", va="center")
    texto(ax, W / 2, y - 24.5,
          "Te avisaremos en tu bandeja cada vez que tu pedido avance de estado.",
          size=7.0, color=G600, font=F, ha="center", va="center")
    chip(ax, W / 2 - 22, y - 31.5, 44, 5.0, "Código de seguimiento:  CS-2026-000123",
         fill=CORAL_SUAVE, fg=CORAL, edge=None, size=7.4, bold=True)

    # linea de tiempo
    estados = [("Pendiente", "12 abr · 19:04", "hecho"),
               ("Pagado", "12 abr · 19:05", "hecho"),
               ("En producción", "Arte aprobado", "actual"),
               ("Enviado", "Estimado 14 abr", "pend"),
               ("Entregado", "Estimado 15 abr", "pend")]
    tx, ty = 14, y - 44
    paso = (W - 2 * tx) / (len(estados) - 1)
    for i, (n, d, e) in enumerate(estados):
        cx = tx + i * paso
        col = {"hecho": VERDE, "actual": CORAL, "pend": G300}[e]
        if i < len(estados) - 1:
            sig = estados[i + 1][2]
            ax.plot([cx + 3, cx + paso - 3], [ty, ty],
                    color=VERDE if e == "hecho" and sig != "pend" else
                    (VERDE if e == "hecho" else G200), lw=1.6, zorder=4)
        ax.add_patch(Circle((cx, ty), 2.6, facecolor=col, edgecolor="none", zorder=6))
        if e == "hecho":
            texto(ax, cx, ty, "✓", size=6.0, color=BLANCO, bold=True, font=ICO,
                  ha="center", va="center", z=7)
        elif e == "actual":
            ax.add_patch(Circle((cx, ty), 4.0, facecolor="none", edgecolor=CORAL,
                                lw=1.0, zorder=6))
        texto(ax, cx, ty - 6.5, n, size=6.6, color=G900 if e != "pend" else G400,
              bold=e == "actual", font=F, ha="center", va="center")
        texto(ax, cx, ty - 10, d, size=5.4, color=G500 if e != "pend" else G400,
              font=F, ha="center", va="center")

    # resumen
    caja(ax, 14, 6, 58, 22, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 16.5, 24.5, "Detalle del pedido", size=7.6, color=G900, bold=True,
          font=F, va="center")
    for i, (k, v) in enumerate([("3 productos", "S/ 255.00"),
                                ("Descuento COLECCION10", "− S/ 25.50"),
                                ("Envío delivery Lima", "S/ 12.00"),
                                ("Total pagado", "S/ 241.50")]):
        ultimo = i == 3
        texto(ax, 16.5, 20.5 - i * 4.0, k, size=6.2,
              color=G900 if ultimo else G600, bold=ultimo, font=F, va="center")
        texto(ax, 69.5, 20.5 - i * 4.0, v, size=6.2 if not ultimo else 7.4,
              color=CORAL if ultimo else G900, bold=ultimo, font=F,
              ha="right", va="center")

    caja(ax, 76, 6, 58, 22, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 78.5, 24.5, "Entrega", size=7.6, color=G900, bold=True, font=F, va="center")
    texto(ax, 78.5, 20.0,
          "Diego Damián  ·  987 654 321\nAv. Brasil 1234, Jesús María, Lima\n"
          "Delivery Lima  ·  entrega estimada el 15 de abril",
          size=6.2, color=G600, font=F, va="top", lh=1.5)
    boton(ax, 78.5, 8.5, 25, 4.6, "Ver mis pedidos", "oscuro", size=6.6)
    boton(ax, 105.5, 8.5, 26, 4.6, "Seguir comprando", "secundario", size=6.6)
    guardar(fig, ruta("B7_confirmacion.png"))


# ========================================================= B.8 · CUENTA
def b8_cuenta():
    fig, ax, y = pantalla("coral-shop.pe/mi-cuenta/pedidos")
    titulo_pantalla(ax, "B.8", "Mi cuenta: pedidos y Mis diseños (M08 y M10)")
    y = header_tienda(ax, y, buscador=False)

    # menu lateral
    caja(ax, 5, 8, 30, y - 9, fill=G50, edge=G200, lw=0.8, r=1.0)
    ax.add_patch(Circle((11, y - 7), 3.4, facecolor=CORAL_SUAVE, edgecolor="none", zorder=5))
    texto(ax, 11, y - 7, "DD", size=6.6, color=CORAL, bold=True, font=F,
          ha="center", va="center", z=6)
    texto(ax, 16, y - 5.5, "Diego Damián", size=7.2, color=G900, bold=True, font=F, va="center")
    texto(ax, 16, y - 8.8, "diego@correo.com", size=5.6, color=G600, font=F, va="center")
    opciones = [("Mi perfil", False), ("Mis pedidos", True), ("Mis diseños", False),
                ("Favoritos", False), ("Direcciones", False), ("Notificaciones", False)]
    oy = y - 15
    for n, sel in opciones:
        if sel:
            caja(ax, 6.5, oy - 2.4, 27, 4.8, fill=CORAL_SUAVE, r=0.7)
        texto(ax, 9, oy, n, size=6.6, color=CORAL if sel else G700, bold=sel,
              font=F, va="center")
        if n == "Notificaciones":
            ax.add_patch(Circle((31, oy), 1.4, facecolor=CORAL, zorder=6))
            texto(ax, 31, oy, "2", size=5.0, color=BLANCO, bold=True, font=F,
                  ha="center", va="center", z=7)
        oy -= 5.6

    texto(ax, 39, y - 5, "Mis pedidos", size=11, color=G900, bold=True, font=F, va="center")
    for i, (t, sel) in enumerate([("Todos", True), ("En curso", False),
                                  ("Entregados", False), ("Cancelados", False)]):
        chip(ax, 39 + i * 17, y - 12, 15.5, 3.8, t, fill=G900 if sel else BLANCO,
             fg=BLANCO if sel else G700, edge=None if sel else G200, size=6.0, bold=sel)

    cab = [("PEDIDO", 41), ("FECHA", 66), ("PRODUCTOS", 84), ("TOTAL", 106), ("ESTADO", 120)]
    for c, x in cab:
        texto(ax, x, y - 17.5, c, size=5.6, color=G500, bold=True, font=F, va="center")
    ax.plot([39, 143], [y - 19.5, y - 19.5], color=G200, lw=0.8, zorder=4)

    pedidos = [("CS-2026-000123", "12 abr 2026", "3 productos", "S/ 241.50",
                "En producción", CORAL, CORAL_SUAVE),
               ("CS-2026-000098", "02 abr 2026", "1 producto", "S/ 89.00",
                "Entregado", VERDE, VERDE_50),
               ("CS-2026-000071", "24 mar 2026", "5 productos", "S/ 412.00",
                "Entregado", VERDE, VERDE_50),
               ("CS-2026-000054", "11 mar 2026", "2 productos", "S/ 134.00",
                "Cancelado", ROJO, "#FEF2F2")]
    py = y - 24
    for cod, fecha, prods, total, est, col, bg in pedidos:
        texto(ax, 41, py, cod, size=6.4, color=G900, bold=True, font=F, va="center")
        texto(ax, 66, py, fecha, size=6.2, color=G600, font=F, va="center")
        texto(ax, 84, py, prods, size=6.2, color=G600, font=F, va="center")
        texto(ax, 106, py, total, size=6.4, color=G900, bold=True, font=F, va="center")
        chip(ax, 119, py - 1.9, 17, 3.8, est, fill=bg, fg=col, edge=None, size=5.6, bold=True)
        texto(ax, 141, py, "Ver ›", size=6.0, color=CORAL, font=ICO, ha="right", va="center")
        ax.plot([39, 143], [py - 4.2, py - 4.2], color=G200, lw=0.6, zorder=4)
        py -= 8.4

    texto(ax, 39, py - 3, "Mis diseños guardados", size=9.0, color=G900, bold=True,
          font=F, va="center")
    texto(ax, 141, py - 3, "Ver todos ›", size=6.0, color=CORAL, font=ICO,
          ha="right", va="center")
    disenos = ["Logo banda", "Promo 2026", "Texto CORAL", "Ilustración"]
    for i, d in enumerate(disenos):
        dx = 39 + i * 26.5
        caja(ax, dx, 8, 24, py - 12, fill=G50, edge=G200, lw=0.7, r=0.9)
        marcador_imagen(ax, dx + 1.5, 12, 21, py - 17, "", fill=BLANCO, r=0.7)
        texto(ax, dx + 2, 10, d, size=6.0, color=G700, bold=True, font=F, va="center")
    guardar(fig, ruta("B8_cuenta.png"))


# ===================================================== B.9 · TABLERO ADMIN
def _sidebar_admin(ax, activo, y_top):
    """y_top es la coordenada superior del area de contenido de la pantalla."""
    caja(ax, 0.5, 0.5, 27, y_top + 0.1, fill="#1F2937", r=1.0)
    texto(ax, 3.5, y_top - 4.0, "Coral", size=11, color=CORAL, bold=True, font=F,
          va="center")
    texto(ax, 14, y_top - 3.7, "admin", size=6.0, color="#9CA3AF", font=F, va="center")
    ops = ["Tablero", "Catálogo", "Inventario", "Pedidos", "Maestros",
           "Cupones", "Envíos", "Usuarios", "Reportes", "Auditoría"]
    oy = y_top - 10.5
    for o in ops:
        sel = o == activo
        if sel:
            caja(ax, 2.0, oy - 2.3, 24, 4.6, fill=CORAL, r=0.7)
        texto(ax, 4.5, oy, o, size=6.6, color=BLANCO if sel else "#D1D5DB",
              bold=sel, font=F, va="center")
        oy -= 5.4
    texto(ax, 4.5, 5.5, "Diego D.  ·  ADMIN", size=5.6, color="#9CA3AF", font=F, va="center")


def b9_tablero():
    fig, ax, y = pantalla("coral-shop.pe/admin", alto=104)
    titulo_pantalla(ax, "B.9", "Tablero administrativo (M11)", alto=104)
    _sidebar_admin(ax, "Tablero", y)

    texto(ax, 31, y - 4, "Tablero", size=12, color=G900, bold=True, font=F, va="center")
    texto(ax, 31, y - 9, "Resumen de la operación al 12 de abril de 2026", size=6.4,
          color=G600, font=F, va="center")
    campo(ax, 112, y - 6.5, 30, 4.2, "", valor="Últimos 7 días", desplegable=True)

    kpis = [("Ventas del día", "S/ 3 480", "+12 % vs. ayer", VERDE),
            ("Pedidos del mes", "218", "+8 % vs. marzo", VERDE),
            ("Ticket promedio", "S/ 112", "+S/ 6 con estampado", CORAL),
            ("Stock crítico", "7 variantes", "requieren reposición", ROJO)]
    for i, (t, v, d, col) in enumerate(kpis):
        kx = 31 + i * 28.5
        caja(ax, kx, y - 26, 26.5, 13, fill=G50, edge=G200, lw=0.8, r=1.0)
        texto(ax, kx + 2, y - 16.5, t, size=5.8, color=G500, bold=True, font=F, va="center")
        texto(ax, kx + 2, y - 21, v, size=12, color=G900, bold=True, font=F, va="center")
        texto(ax, kx + 2, y - 24.5, d, size=5.4, color=col, font=F, va="center")

    # grafico de barras
    caja(ax, 31, 30, 68, y - 60, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 33, y - 31, "Ventas de los últimos 7 días", size=7.6, color=G900,
          bold=True, font=F, va="center")
    valores = [2.4, 3.1, 2.8, 3.9, 4.4, 5.2, 3.5]
    dias = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]
    base, maxh = 36, 20
    for i, (v, d) in enumerate(zip(valores, dias)):
        bx = 36 + i * 8.6
        h = v / 5.6 * maxh
        caja(ax, bx, base, 5.6, h, fill=CORAL if v == max(valores) else "#FDBA9E", r=0.4)
        texto(ax, bx + 2.8, base - 2.6, d, size=5.4, color=G600, font=F,
              ha="center", va="center")
        texto(ax, bx + 2.8, base + h + 1.8, f"{v:.1f}k", size=5.0, color=G500,
              font=F, ha="center", va="center")

    # stock critico
    caja(ax, 102, 30, 40, y - 60, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 104, y - 31, "Stock crítico", size=7.6, color=G900, bold=True, font=F, va="center")
    criticos = [("POL-URB-M-NEG", "2 / 10"), ("POL-URB-L-NEG", "1 / 10"),
                ("PLR-CAP-S-COR", "3 / 12"), ("GOR-CLA-U-NEG", "0 / 15")]
    cy = y - 36
    for sku, st in criticos:
        texto(ax, 104, cy, sku, size=5.8, color=G700, font=F, va="center")
        chip(ax, 130, cy - 1.6, 10, 3.2, st, fill="#FEF2F2", fg=ROJO, edge=None,
             size=5.4, bold=True)
        cy -= 5.0

    # pedidos recientes
    texto(ax, 31, 25, "Pedidos por atender", size=7.6, color=G900, bold=True, font=F, va="center")
    for c, x in [("PEDIDO", 31), ("CLIENTE", 56), ("TOTAL", 82), ("ESTADO", 100),
                 ("ARTE", 126)]:
        texto(ax, x, 21, c, size=5.4, color=G500, bold=True, font=F, va="center")
    ax.plot([31, 142], [19.5, 19.5], color=G200, lw=0.7, zorder=4)
    filas = [("CS-2026-000123", "Diego D.", "S/ 241.50", "Pagado", AZUL, AZUL_50, "Pendiente", CORAL),
             ("CS-2026-000122", "Ana R.", "S/ 78.00", "En producción", CORAL, CORAL_SUAVE, "Aprobado", VERDE),
             ("CS-2026-000121", "Luis M.", "S/ 156.00", "Enviado", VERDE, VERDE_50, "—", G400)]
    fy = 15.5
    for cod, cli, tot, est, ec, eb, arte, ac in filas:
        texto(ax, 31, fy, cod, size=6.0, color=G900, bold=True, font=F, va="center")
        texto(ax, 56, fy, cli, size=6.0, color=G600, font=F, va="center")
        texto(ax, 82, fy, tot, size=6.0, color=G900, font=F, va="center")
        chip(ax, 99, fy - 1.7, 20, 3.4, est, fill=eb, fg=ec, edge=None, size=5.4, bold=True)
        texto(ax, 126, fy, arte, size=5.8, color=ac, bold=arte != "—", font=F, va="center")
        fy -= 5.2
    guardar(fig, ruta("B9_tablero.png"))


# ================================================ B.10 · PRODUCTO ADMIN
def b10_producto_admin():
    fig, ax, y = pantalla("coral-shop.pe/admin/productos/12/editar", alto=112)
    titulo_pantalla(ax, "B.10", "Mantenimiento de producto y variantes (M12)", alto=112)
    _sidebar_admin(ax, "Catálogo", y)

    texto(ax, 31, y - 4, "Editar producto", size=11, color=G900, bold=True, font=F, va="center")
    texto(ax, 31, y - 9, "Catálogo  ›  Polos  ›  Polo urbano oversize", size=6.0,
          color=G400, font=F, va="center")
    boton(ax, 113, y - 6.5, 13, 4.4, "Cancelar", "secundario", size=6.2)
    boton(ax, 128, y - 6.5, 14, 4.4, "Guardar", "primario", size=6.2)

    # datos del producto
    caja(ax, 31, 44, 68, y - 57, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 33, y - 15, "Datos generales", size=7.6, color=G900, bold=True, font=F, va="center")
    campo(ax, 33, y - 24, 40, 4.4, "", etiqueta="Nombre", valor="Polo urbano oversize")
    campo(ax, 75, y - 24, 22, 4.4, "", etiqueta="Slug", valor="polo-urbano-oversize")
    campo(ax, 33, y - 33, 26, 4.4, "", etiqueta="Categoría", valor="Polos", desplegable=True)
    campo(ax, 61, y - 33, 18, 4.4, "", etiqueta="Precio base", valor="S/ 45.00")
    campo(ax, 81, y - 33, 16, 4.4, "", etiqueta="Género", valor="Unisex", desplegable=True)
    texto(ax, 33, y - 37, "Personalizable", size=6.2, color=G700, bold=True, font=F, va="center")
    caja(ax, 55, y - 38.6, 5.6, 3.0, fill=CORAL, r=1.5)
    ax.add_patch(Circle((58.8, y - 37.1), 1.15, color=BLANCO, zorder=6))
    texto(ax, 63, y - 37.1, "Habilita el personalizador en la ficha pública",
          size=5.6, color=G500, font=F, va="center")
    campo(ax, 33, y - 50, 64, 8.0, "", etiqueta="Descripción",
          valor="Algodón peinado 20/1, corte oversize, cuello reforzado.")

    # imagenes
    caja(ax, 102, 44, 40, y - 57, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, 104, y - 15, "Imágenes", size=7.6, color=G900, bold=True, font=F, va="center")
    for i in range(4):
        fila, col = divmod(i, 2)
        ix = 104 + col * 18.5
        iy = y - 32 - fila * 15
        marcador_imagen(ax, ix, iy, 16.5, 13, "", fill=BLANCO, r=0.7)
        if i == 0:
            chip(ax, ix + 0.8, iy + 9.8, 9, 2.4, "Principal", fill=CORAL,
                 fg=BLANCO, edge=None, size=4.6, bold=True)
    caja(ax, 104, y - 47, 35, 6.5, fill=BLANCO, edge=G300, lw=0.9, r=0.7, ls=(0, (3, 2)))
    texto(ax, 121.5, y - 43.7, "⬆  Subir imagen", size=6.0, color=G600, bold=True,
          font=ICO, ha="center", va="center")

    # variantes
    texto(ax, 31, 39, "Variantes", size=8.6, color=G900, bold=True, font=F, va="center")
    texto(ax, 46, 39, "18 combinaciones de talla y color", size=6.0, color=G600,
          font=F, va="center")
    boton(ax, 108, 37, 34, 4.4, "⚙  Generar variantes automáticamente", "oscuro",
          size=6.0, font=ICO)

    cols = [("SKU", 33), ("TALLA", 60), ("COLOR", 72), ("STOCK", 88),
            ("MÍN.", 100), ("PRECIO", 111), ("ACTIVA", 126)]
    for c, x in cols:
        texto(ax, x, 32, c, size=5.4, color=G500, bold=True, font=F, va="center")
    ax.plot([31, 142], [30.5, 30.5], color=G200, lw=0.8, zorder=4)
    variantes = [("POL-URB-S-NEG", "S", "Negro", "14", "10", "—", True),
                 ("POL-URB-M-NEG", "M", "Negro", "2", "10", "—", True),
                 ("POL-URB-L-NEG", "L", "Negro", "1", "10", "—", True),
                 ("POL-URB-M-BLA", "M", "Blanco", "23", "10", "S/ 47.00", True),
                 ("POL-URB-M-COR", "M", "Coral", "0", "10", "—", False)]
    vy = 26.5
    for sku, t, c, st, mn, pr, act in variantes:
        bajo = int(st) < int(mn)
        texto(ax, 33, vy, sku, size=5.8, color=G900, font=F, va="center")
        texto(ax, 60, vy, t, size=5.8, color=G700, font=F, va="center")
        texto(ax, 72, vy, c, size=5.8, color=G700, font=F, va="center")
        chip(ax, 87, vy - 1.6, 8, 3.2, st, fill="#FEF2F2" if bajo else VERDE_50,
             fg=ROJO if bajo else VERDE, edge=None, size=5.4, bold=True)
        texto(ax, 100, vy, mn, size=5.8, color=G600, font=F, va="center")
        texto(ax, 111, vy, pr, size=5.8, color=G600, font=F, va="center")
        caja(ax, 126, vy - 1.4, 4.8, 2.6, fill=CORAL if act else G300, r=1.3)
        ax.add_patch(Circle((129.0 if act else 127.2, vy - 0.1), 1.0,
                            color=BLANCO, zorder=6))
        texto(ax, 137, vy, "Editar", size=5.6, color=CORAL, font=F, va="center")
        ax.plot([31, 142], [vy - 3.4, vy - 3.4], color=G200, lw=0.6, zorder=4)
        vy -= 4.4
    guardar(fig, ruta("B10_producto_admin.png"))


# ==================================================== B.11 · PEDIDOS ADMIN
def b11_pedidos_admin():
    fig, ax, y = pantalla("coral-shop.pe/admin/pedidos/CS-2026-000123", alto=104)
    titulo_pantalla(ax, "B.11", "Bandeja de pedidos y aprobación del arte (M15)",
                    alto=104)
    _sidebar_admin(ax, "Pedidos", y)

    texto(ax, 31, y - 4, "Pedidos", size=11, color=G900, bold=True, font=F, va="center")
    tabs = [("Todos", "218", False), ("Pendientes", "12", False), ("Pagados", "31", True),
            ("En producción", "18", False), ("Enviados", "9", False)]
    tx = 31
    for n, c, sel in tabs:
        w = len(n) * 1.25 + 9
        chip(ax, tx, y - 12.5, w, 4.2, f"{n}  {c}", fill=G900 if sel else BLANCO,
             fg=BLANCO if sel else G700, edge=None if sel else G200,
             size=5.8, bold=sel)
        tx += w + 2.5
    campo(ax, 112, y - 12.5, 30, 4.2, "Buscar pedido o cliente…")

    # tabla
    for c, x in [("PEDIDO", 33), ("CLIENTE", 56), ("FECHA", 74), ("TOTAL", 90)]:
        texto(ax, x, y - 18, c, size=5.4, color=G500, bold=True, font=F, va="center")
    ax.plot([31, 100], [y - 20, y - 20], color=G200, lw=0.8, zorder=4)
    filas = [("CS-2026-000123", "Diego Damián", "12 abr", "S/ 241.50", True),
             ("CS-2026-000122", "Ana Rojas", "12 abr", "S/ 78.00", False),
             ("CS-2026-000120", "Luis Mendoza", "11 abr", "S/ 156.00", False),
             ("CS-2026-000119", "Sofía Paz", "11 abr", "S/ 92.00", False),
             ("CS-2026-000118", "Marco Ruiz", "10 abr", "S/ 310.00", False)]
    fy = y - 24
    for cod, cli, fec, tot, sel in filas:
        if sel:
            caja(ax, 31, fy - 2.6, 69, 5.4, fill=CORAL_SUAVE, r=0.6)
        texto(ax, 33, fy, cod, size=6.0, color=CORAL if sel else G900, bold=True,
              font=F, va="center")
        texto(ax, 56, fy, cli, size=6.0, color=G600, font=F, va="center")
        texto(ax, 74, fy, fec, size=6.0, color=G600, font=F, va="center")
        texto(ax, 90, fy, tot, size=6.0, color=G900, font=F, va="center")
        fy -= 6.2

    # panel de detalle
    dx = 103
    caja(ax, dx, 8, 39, y - 9, fill=G50, edge=G200, lw=0.8, r=1.0)
    texto(ax, dx + 2.5, y - 5, "CS-2026-000123", size=8.6, color=G900, bold=True,
          font=F, va="center")
    chip(ax, dx + 2.5, y - 11.5, 13, 3.6, "Pagado", fill=AZUL_50, fg=AZUL,
         edge=None, size=5.6, bold=True)
    texto(ax, dx + 17.5, y - 9.7, "12 abr 2026 · 19:05", size=5.6, color=G600,
          font=F, va="center")

    texto(ax, dx + 2.5, y - 16, "ARTE DEL CLIENTE", size=5.6, color=G500, bold=True,
          font=F, va="center")
    caja(ax, dx + 2.5, y - 38, 34, 20, fill=BLANCO, edge=G200, lw=0.8, r=0.8)
    caja(ax, dx + 10, y - 34, 19, 12, fill=G900, r=0.5)
    texto(ax, dx + 19.5, y - 28, "CORAL", size=9, color=CORAL, bold=True, font=F,
          ha="center", va="center")
    texto(ax, dx + 2.5, y - 42, "DTF · A4 · Pecho frontal · 2 unidades", size=5.8,
          color=G700, font=F, va="center")
    texto(ax, dx + 2.5, y - 45.5, "arte_cliente.png · 2480 × 3508 px · 300 dpi",
          size=5.4, color=G500, font=F, va="center")
    chip(ax, dx + 2.5, y - 50.5, 20, 3.6, "✓  Resolución suficiente", fill=VERDE_50,
         fg=VERDE, edge=None, size=5.4, bold=True, font=ICO)

    campo(ax, dx + 2.5, y - 60, 34, 6.0, "Observación para el cliente (opcional)")
    boton(ax, dx + 2.5, 22, 16.5, 5.0, "✓  Aprobar arte", "verde", size=6.4, font=ICO)
    boton(ax, dx + 20, 22, 16.5, 5.0, "✕  Rechazar", "peligro", size=6.4, font=ICO)

    texto(ax, dx + 2.5, 17, "Cambiar estado del pedido", size=5.8, color=G500,
          bold=True, font=F, va="center")
    boton(ax, dx + 2.5, 10.5, 34, 5.0, "Pasar a EN_PRODUCCIÓN  →", "oscuro",
          size=6.4, font=ICO)
    guardar(fig, ruta("B11_pedidos_admin.png"))


# ================================================= B.0 · MAPA DE NAVEGACION
def b0_mapa():
    fig, ax = lienzo(7.4, 5.0, 148, 100, bg="#FFFFFF")
    texto(ax, 4, 95, "ANEXO B · MAPA DE NAVEGACIÓN", size=7.0, color=CORAL,
          bold=True, font=F, va="center")
    texto(ax, 4, 89.5, "Cómo se enlazan las pantallas", size=13, color=G900,
          bold=True, font=F, va="center")

    zonas = [("TIENDA PÚBLICA  ·  invitado y cliente", CORAL, 4, 44, 140, 38),
             ("CLIENTE AUTENTICADO", VERDE, 4, 24, 88, 18),
             ("BACKOFFICE  ·  vendedor, diseñador y administrador", G900, 4, 3, 140, 19)]
    for t, c, x, yz, w, h in zonas:
        caja(ax, x, yz, w, h, fill="#FCFCFD", edge=c, lw=1.0, r=1.0)
        chip(ax, x, yz + h - 3.6, 52 if len(t) > 30 else 32, 3.6, t, fill=c,
             fg=BLANCO, edge=None, size=5.8, bold=True)

    def nodo(x, yn, w, h, cod, nombre, color=CORAL):
        caja(ax, x, yn, w, h, fill=BLANCO, edge=color, lw=0.9, r=0.7)
        texto(ax, x + w / 2, yn + h - 2.6, cod, size=5.2, color=color, bold=True,
              font=F, ha="center", va="center")
        texto(ax, x + w / 2, yn + h / 2 - 1.6, nombre, size=6.0, color=G900,
              font=F, ha="center", va="center", wrap=16, lh=1.25)
        return (x + w / 2, yn, x + w, yn + h / 2, x, yn + h / 2)

    n_home = nodo(8, 68, 23, 9, "B.1", "Portada")
    n_cat = nodo(37, 68, 23, 9, "B.2", "Catálogo con filtros")
    n_prod = nodo(66, 68, 23, 9, "B.3", "Ficha de producto")
    n_pers = nodo(95, 68, 23, 9, "B.4", "Personalizador")
    n_car = nodo(124, 68, 16, 9, "B.5", "Carrito")
    n_login = nodo(37, 50, 23, 9, "—", "Registro / login", G600)
    n_check = nodo(66, 50, 23, 9, "B.6", "Checkout")
    n_conf = nodo(95, 50, 23, 9, "B.7", "Confirmación")
    n_cuenta = nodo(37, 27, 23, 9, "B.8", "Mi cuenta", VERDE)
    n_dis = nodo(66, 27, 23, 9, "B.8", "Mis diseños", VERDE)

    n_tab = nodo(10, 6, 26, 9, "B.9", "Tablero", G900)
    n_pa = nodo(42, 6, 30, 9, "B.10", "Catálogo y variantes", G900)
    n_ped = nodo(78, 6, 30, 9, "B.11", "Pedidos y arte", G900)
    n_inv = nodo(114, 6, 26, 9, "M14", "Inventario", G900)

    def unir(a, b, color=G400, rad=0.0, ls="solid"):
        flecha(ax, (a[2], a[3]), (b[4], b[3]), color=color, lw=0.9, size=8,
               conn=f"arc3,rad={rad}", ls=ls)

    unir(n_home, n_cat, CORAL)
    unir(n_cat, n_prod, CORAL)
    unir(n_prod, n_pers, CORAL)
    unir(n_pers, n_car, CORAL)
    flecha(ax, (n_prod[0], n_prod[1]), (n_car[0] - 6, 77), color=CORAL, lw=0.9,
           size=8, conn="arc3,rad=-0.25")
    flecha(ax, (n_car[0], n_car[1]), (n_login[0], n_login[1] + 9), color=CORAL,
           lw=0.9, size=8, conn="arc3,rad=0.18")
    texto(ax, 108, 63, "si es invitado, se le pide registrarse", size=5.2,
          color=G500, italic=True, font=F, va="center")
    unir(n_login, n_check, VERDE)
    unir(n_check, n_conf, VERDE)
    flecha(ax, (n_conf[0], n_conf[1]), (n_cuenta[0] + 6, n_cuenta[1] + 9),
           color=VERDE, lw=0.9, size=8, conn="arc3,rad=0.25")
    unir(n_cuenta, n_dis, VERDE)
    flecha(ax, (n_dis[2], n_dis[3]), (n_pers[0], n_pers[1]), color=VERDE, lw=0.9,
           size=8, conn="arc3,rad=-0.3", ls=(0, (4, 2)))
    texto(ax, 92, 34, "reutiliza un diseño guardado", size=5.2, color=VERDE,
          italic=True, font=F, va="center")

    unir(n_tab, n_pa, G600)
    unir(n_pa, n_ped, G600)
    unir(n_ped, n_inv, G600)
    flecha(ax, (n_ped[0], n_ped[1] + 9), (n_conf[0] - 8, n_conf[1]), color=G600,
           lw=0.9, size=8, conn="arc3,rad=-0.2", ls=(0, (4, 2)))
    texto(ax, 62, 20.5, "el cambio de estado del pedido notifica al cliente",
          size=5.2, color=G600, italic=True, font=F, va="center")
    guardar(fig, ruta("B0_mapa_navegacion.png"))


TODAS = [b0_mapa, b1_home, b2_catalogo, b3_producto, b4_personalizador,
         b5_carrito, b6_checkout, b7_confirmacion, b8_cuenta, b9_tablero,
         b10_producto_admin, b11_pedidos_admin]


if __name__ == "__main__":
    print("Generando prototipos en", BASE)
    for f in TODAS:
        f()
    print("Listo.")
