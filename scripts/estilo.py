# -*- coding: utf-8 -*-
"""Identidad visual compartida por las figuras, el informe y la presentacion."""

import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Ellipse

# --------------------------------------------------------------------- paleta
DARK = "#3D1927"   # fondo oscuro
PRIMARY = "#6D2E46"   # vinotinto principal
ACCENT = "#A26769"   # rosa palo de acento
ROSE = "#D9AFAF"   # rosa claro
CREAM = "#ECE2D0"   # crema (texto sobre oscuro)
CARD = "#FBF7F2"   # fondo de tarjeta clara
BLUE = "#3C6E8F"   # azul (frontend / catalogo)
GREEN = "#4E7A5A"   # verde (compra)
GOLD = "#8A6D3B"   # dorado (soporte)
TEXT = "#2B2020"   # texto principal
MUTED = "#6E5B5B"   # texto secundario
LINE = "#D8C6C0"   # bordes suaves
WHITE = "#FFFFFF"

# Ojo: en este matplotlib, Calibri y Cambria pierden glifos por debajo de ~7.5 pt
# (solo sobreviven las ligaduras). Las figuras usan Arial para el texto menudo y
# reservan Cambria para titulos, donde el tamano nunca baja de 8 pt.
TITLE_FONT = "Cambria"
BODY_FONT = "Arial"


def lienzo(w, h, xmax, ymax, bg=WHITE):
    """Crea una figura sin ejes con un sistema de coordenadas propio."""
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=bg)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    ax.set_facecolor(bg)
    return fig, ax


def caja(ax, x, y, w, h, fill=CARD, edge="none", lw=1.0, r=0.9, z=2, alpha=1.0, ls="solid"):
    """Rectangulo de esquinas redondeadas anclado en su esquina inferior izquierda."""
    p = FancyBboxPatch(
        (x + r, y + r), w - 2 * r, h - 2 * r,
        boxstyle=f"round,pad={r},rounding_size={r}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
        zorder=z, alpha=alpha, linestyle=ls, mutation_aspect=1,
    )
    ax.add_patch(p)
    return p


def texto(ax, x, y, s, size=10, color=TEXT, bold=False, font=BODY_FONT,
          ha="left", va="center", z=5, wrap=None, lh=1.25, italic=False,
          spacing=None):
    if wrap:
        s = "\n".join(textwrap.wrap(s, wrap))
    t = ax.text(
        x, y, s, fontsize=size, color=color, fontfamily=font,
        fontweight="bold" if bold else "normal",
        fontstyle="italic" if italic else "normal",
        ha=ha, va=va, zorder=z, linespacing=lh,
    )
    return t


def flecha(ax, p1, p2, color=ACCENT, lw=1.6, style="-|>", size=9, z=3,
           conn="arc3,rad=0", ls="solid"):
    a = FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=size, linewidth=lw,
        color=color, zorder=z, connectionstyle=conn, linestyle=ls,
        shrinkA=0, shrinkB=0,
    )
    ax.add_patch(a)
    return a


def etiqueta(ax, x, y, w, h, s, fill=PRIMARY, color=WHITE, size=8.5, bold=True,
             font=BODY_FONT, z=6, r=0.5):
    """Chip: caja pequena con texto centrado."""
    caja(ax, x, y, w, h, fill=fill, r=r, z=z)
    texto(ax, x + w / 2, y + h / 2, s, size=size, color=color, bold=bold,
          font=font, ha="center", z=z + 1)


def titulo_figura(ax, x, y, kicker, titulo, size_k=9.5, size_t=17):
    texto(ax, x, y + 2.4, kicker.upper(), size=size_k, color=ACCENT, bold=True)
    texto(ax, x, y, titulo, size=size_t, color=PRIMARY, bold=True, font=TITLE_FONT)


def guardar(fig, ruta):
    fig.savefig(ruta, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  ok", ruta)
