# -*- coding: utf-8 -*-
"""Ilustraciones de los productos de demostración → frontend/public/demo/*.png.

Prendas planas dibujadas con Pillow (sin fotos de terceros): las usa el sembrador de datos
demo del backend (perfil «demo») como imagen principal de cada producto. Se sirven desde el
propio frontend, así que funcionan igual en local y en Vercel.

    python demo_imagenes.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SALIDA = Path(__file__).resolve().parent.parent / "frontend" / "public" / "demo"
LADO = 800          # tamaño final (px)
ESCALA = 3          # se dibuja más grande y se reduce: bordes suavizados
FONDO = (0, 0, 0, 0)

NEGRO = "#26232a"
BLANCO = "#f4f1ec"
AZUL = "#2f5d8c"
ROJO = "#b8322f"
BEIGE = "#d6c6a6"
CORAL = "#ff5331"


def _rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _tono(hex_color, factor):
    """Aclara (factor > 1) u oscurece (factor < 1) un color."""
    r, g, b = _rgb(hex_color)
    if factor >= 1:
        return tuple(int(c + (255 - c) * (factor - 1)) for c in (r, g, b))
    return tuple(int(c * factor) for c in (r, g, b))


def _lienzo():
    img = Image.new("RGBA", (LADO * ESCALA, LADO * ESCALA), FONDO)
    return img, ImageDraw.Draw(img)


def _p(*pts):
    """Puntos en coordenadas 0–1000 → píxeles del lienzo grande."""
    k = LADO * ESCALA / 1000
    return [(x * k, y * k) for x, y in pts]


def _w(valor):
    return int(valor * LADO * ESCALA / 1000)


def _guardar(img, nombre):
    sombra = Image.new("RGBA", img.size, FONDO)
    alfa = img.split()[3].point(lambda a: 70 if a else 0)
    sombra.putalpha(alfa)
    sombra = sombra.filter(ImageFilter.GaussianBlur(_w(10)))
    base = Image.new("RGBA", img.size, FONDO)
    base.alpha_composite(sombra, (_w(8), _w(14)))
    base.alpha_composite(img)
    base = base.resize((LADO, LADO), Image.LANCZOS)
    SALIDA.mkdir(parents=True, exist_ok=True)
    base.save(SALIDA / nombre, optimize=True)
    print("  ", nombre)


def polo(color, nombre, oversize=False, logo=None):
    img, d = _lienzo()
    borde = _tono(color, 0.75)
    ancho = 30 if oversize else 0
    cuerpo = _p((300 - ancho, 250), (400, 205), (600, 205), (700 + ancho, 250),
                (880 + ancho, 400), (800 + ancho, 480), (720 + ancho, 420),
                (720 + ancho, 880), (280 - ancho, 880), (280 - ancho, 420),
                (200 - ancho, 480), (120 - ancho, 400))
    d.polygon(cuerpo, fill=_rgb(color), outline=borde, width=_w(5))
    # Cuello redondo y costuras de las mangas.
    d.chord(_p((405, 150), (595, 290))[0] + _p((405, 150), (595, 290))[1], 0, 180,
            fill=_tono(color, 0.82), outline=borde, width=_w(5))
    d.line(_p((280 - ancho, 420), (300 - ancho, 250)), fill=borde, width=_w(4))
    d.line(_p((720 + ancho, 420), (700 + ancho, 250)), fill=borde, width=_w(4))
    d.line(_p((280 - ancho, 850), (720 + ancho, 850)), fill=borde, width=_w(3))
    if logo:
        _logo(d, logo, 500, 450, 95)
    _guardar(img, nombre)


def polera(color, nombre, capucha=True):
    img, d = _lienzo()
    borde = _tono(color, 0.72)
    oscuro = _tono(color, 0.85)
    if capucha:
        d.ellipse(_p((350, 90), (650, 330)), fill=oscuro, outline=borde, width=_w(5))
        d.ellipse(_p((405, 150), (595, 320)), fill=_tono(color, 0.6))
    cuerpo = _p((290, 250), (400, 215), (600, 215), (710, 250),
                (850, 470), (900, 820), (810, 840), (740, 520),
                (740, 860), (260, 860), (260, 520),
                (190, 840), (100, 820), (150, 470))
    d.polygon(cuerpo, fill=_rgb(color), outline=borde, width=_w(5))
    if not capucha:
        d.chord(_p((410, 160), (590, 300))[0] + _p((410, 160), (590, 300))[1], 0, 180,
                fill=oscuro, outline=borde, width=_w(5))
    # Puños, pretina y bolsillo canguro.
    d.rectangle(_p((260, 820), (740, 880)), fill=oscuro, outline=borde, width=_w(4))
    d.polygon(_p((100, 820), (190, 840), (185, 885), (92, 865)), fill=oscuro, outline=borde, width=_w(4))
    d.polygon(_p((900, 820), (810, 840), (815, 885), (908, 865)), fill=oscuro, outline=borde, width=_w(4))
    d.polygon(_p((360, 640), (640, 640), (690, 800), (310, 800)), fill=oscuro, outline=borde, width=_w(4))
    if capucha:
        for x in (465, 535):
            d.line(_p((x, 300), (x, 450)), fill=BLANCO, width=_w(7))
    _guardar(img, nombre)


def gorra(color, nombre, trucker=False):
    img, d = _lienzo()
    borde = _tono(color, 0.72)
    copa = _p((220, 230), (780, 830))
    d.chord(copa[0] + copa[1], 180, 360, fill=_rgb(color), outline=borde, width=_w(5))
    if trucker:
        # Malla trasera clara a ambos lados del panel frontal.
        d.chord(copa[0] + copa[1], 180, 235, fill=BLANCO, outline=borde, width=_w(4))
        d.chord(copa[0] + copa[1], 305, 360, fill=BLANCO, outline=borde, width=_w(4))
    # Visera: media elipse que nace del borde de la copa.
    visera = _p((170, 425), (830, 640))
    d.chord(visera[0] + visera[1], 0, 180, fill=_tono(color, 0.8), outline=borde, width=_w(5))
    for angulo_x in (380, 620):
        d.line(_p((500, 235), (angulo_x, 525)), fill=borde, width=_w(3))
    d.ellipse(_p((480, 215), (520, 250)), fill=borde)
    _guardar(img, nombre)


def tote(color, nombre, logo=None):
    img, d = _lienzo()
    borde = _tono(color, 0.7)
    for x0 in (330, 560):
        d.arc(_p((x0 - 20, 90), (x0 + 130, 420))[0] + _p((x0 - 20, 90), (x0 + 130, 420))[1], 180, 360,
              fill=_tono(color, 0.65), width=_w(26))
    d.rounded_rectangle(_p((220, 300), (780, 900))[0] + _p((220, 300), (780, 900))[1], radius=_w(18),
                        fill=_rgb(color), outline=borde, width=_w(5))
    d.line(_p((220, 360), (780, 360)), fill=borde, width=_w(3))
    if logo:
        _logo(d, logo, 500, 620, 120)
    _guardar(img, nombre)


def _logo(d, color, cx, cy, r):
    """Isotipo ficticio de Coral Shop: un círculo con una ola."""
    d.ellipse(_p((cx - r, cy - r), (cx + r, cy + r)), outline=color, width=_w(10))
    d.arc(_p((cx - r * 0.7, cy - r * 0.35), (cx, cy + r * 0.35))[0]
          + _p((cx - r * 0.7, cy - r * 0.35), (cx, cy + r * 0.35))[1], 180, 360, fill=color, width=_w(10))
    d.arc(_p((cx, cy - r * 0.35), (cx + r * 0.7, cy + r * 0.35))[0]
          + _p((cx, cy - r * 0.35), (cx + r * 0.7, cy + r * 0.35))[1], 0, 180, fill=color, width=_w(10))


if __name__ == "__main__":
    print("Ilustraciones de productos demo →", SALIDA)
    polo(NEGRO, "polo-clasico.png")
    polo(BEIGE, "polo-oversize.png", oversize=True)
    polo(BLANCO, "polo-edicion-lima.png", logo=CORAL)
    polera(ROJO, "polera-capucha.png", capucha=True)
    polera(AZUL, "polera-cuello-redondo.png", capucha=False)
    gorra(NEGRO, "gorra-trucker.png", trucker=True)
    gorra(BEIGE, "gorra-dad-hat.png")
    tote(BEIGE, "tote-lona.png")
