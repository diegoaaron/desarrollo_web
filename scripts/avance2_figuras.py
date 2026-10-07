# -*- coding: utf-8 -*-
"""Diagramas del avance 2: los cuatro patrones de arquitectura vistos en clase aplicados a
Coral Shop. Salida: clase_entregables/figuras/A2_*.png"""

import os

from matplotlib.patches import Ellipse, Rectangle

from estilo import (
    lienzo, caja, texto, flecha, etiqueta, titulo_figura, guardar,
    DARK, PRIMARY, ACCENT, ROSE, CARD, BLUE, GREEN, GOLD, TEXT, MUTED, LINE, WHITE, TITLE_FONT,
)

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "clase_entregables", "figuras")
os.makedirs(BASE, exist_ok=True)

RED = "#B23A3A"
ORANGE = "#C0703F"


def ruta(nombre):
    return os.path.join(BASE, nombre)


def persona(ax, x, y, color, rotulo, size=8):
    """Monigote de actor (cabeza en (x, y))."""
    ax.add_patch(Ellipse((x, y), 2.2, 2.2, facecolor=WHITE, edgecolor=color, lw=1.4, zorder=4))
    ax.plot([x, x], [y - 1.1, y - 4.6], color=color, lw=1.4, zorder=4)
    ax.plot([x - 1.8, x + 1.8], [y - 2.4, y - 2.4], color=color, lw=1.4, zorder=4)
    ax.plot([x, x - 1.5], [y - 4.6, y - 7.0], color=color, lw=1.4, zorder=4)
    ax.plot([x, x + 1.5], [y - 4.6, y - 7.0], color=color, lw=1.4, zorder=4)
    texto(ax, x, y - 8.6, rotulo, size=size, color=color, ha="center", italic=True)


def cilindro(ax, x, y, w, h, color, rotulo, size=8, fill=WHITE):
    """Base de datos: cilindro con el rótulo centrado."""
    tapa = h * 0.18
    ax.add_patch(Rectangle((x, y + tapa / 2), w, h - tapa, facecolor=fill, edgecolor="none", zorder=3))
    ax.plot([x, x], [y + tapa / 2, y + h - tapa / 2], color=color, lw=1.4, zorder=4)
    ax.plot([x + w, x + w], [y + tapa / 2, y + h - tapa / 2], color=color, lw=1.4, zorder=4)
    ax.add_patch(Ellipse((x + w / 2, y + tapa / 2), w, tapa, facecolor=fill, edgecolor=color, lw=1.4, zorder=3))
    ax.add_patch(Ellipse((x + w / 2, y + h - tapa / 2), w, tapa, facecolor=fill, edgecolor=color, lw=1.4,
                         zorder=4))
    texto(ax, x + w / 2, y + h / 2 - tapa / 4, rotulo, size=size, color=color, ha="center", bold=True, lh=1.3)


def bloque(ax, x, y, w, h, color, titulo, sub=None, size_t=9.5, size_s=8, fill=WHITE):
    caja(ax, x, y, w, h, fill=fill, edge=color, lw=1.4, r=0.6)
    if sub:
        texto(ax, x + w / 2, y + h * 0.64, titulo, size=size_t, color=color, ha="center", bold=True)
        texto(ax, x + w / 2, y + h * 0.30, sub, size=size_s, color=TEXT, ha="center", lh=1.3)
    else:
        texto(ax, x + w / 2, y + h / 2, titulo, size=size_t, color=color, ha="center", bold=True)


def numero(ax, x, y, n):
    ax.add_patch(Ellipse((x, y), 3.0, 3.0, facecolor=RED, edgecolor="none", zorder=6))
    texto(ax, x, y, str(n), size=8.5, color=WHITE, ha="center", bold=True, z=7)


# ======================================================== 1 · restaurante en capas
def fig_restaurante():
    fig, ax = lienzo(10, 5.4, 100, 54)
    titulo_figura(ax, 3, 49, "Figura A1 · Arquitectura en capas",
                  "El restaurante en capas aplicado a Coral Shop", size_k=8, size_t=14)

    # restaurante
    texto(ax, 3, 41.5, "RESTAURANTE", size=8.5, color=ORANGE, bold=True)
    persona(ax, 7, 36.5, ORANGE, "Comensal")
    filas = [(16, "Mozo", "toma el pedido y revisa\nque esté completo"),
             (38, "Cocinero", "aplica la receta\n(las reglas)"),
             (60, "Almacenero", "trae y guarda\nlos ingredientes")]
    for x, nombre, nota_ in filas:
        bloque(ax, x, 30, 17, 7, ORANGE, nombre, size_t=10)
        texto(ax, x + 8.5, 40.2, nota_, size=7, color=MUTED, ha="center", italic=True, lh=1.2)
    cilindro(ax, 83, 29.5, 13, 8, GREEN, "Despensa")
    flecha(ax, (10.5, 33.5), (16, 33.5), color=ORANGE)
    for a, b in ((33, 38), (55, 60), (77, 83)):
        flecha(ax, (a, 33.5), (b, 33.5), color=ORANGE)

    # software
    texto(ax, 3, 21.5, "SOFTWARE · CORAL SHOP", size=8.5, color=BLUE, bold=True)
    persona(ax, 7, 16, BLUE, "Cliente HTTP")
    capas = [(16, "Controller", "CustomerOrderController", "Presentación"),
             (38, "Service", "OrderService", "Negocio"),
             (60, "Repository", "OrderRepository", "Datos")]
    for x, nombre, clase, capa in capas:
        bloque(ax, x, 9.5, 17, 8, BLUE, nombre, clase, size_t=10, size_s=7)
        texto(ax, x + 8.5, 7.2, capa, size=7.5, color=MUTED, ha="center", italic=True)
    cilindro(ax, 83, 9, 13, 9, BLUE, "PostgreSQL")
    flecha(ax, (10.5, 13.5), (16, 13.5), color=BLUE)
    for a, b in ((33, 38), (55, 60), (77, 83)):
        flecha(ax, (a, 13.5), (b, 13.5), color=BLUE)
    texto(ax, 89.5, 21.5, "pedido = petición\nplato = respuesta", size=7, color=MUTED, ha="center",
          italic=True, lh=1.2)

    # correspondencias
    for x in (24.5, 46.5, 68.5):
        flecha(ax, (x, 29.6), (x, 17.9), color=LINE, lw=1.1, ls="dashed", size=7)

    # atajo prohibido
    flecha(ax, (27, 29.8), (84, 30.5), color=RED, lw=1.2, ls="dashed", conn="arc3,rad=0.32", size=8)
    texto(ax, 56, 22.6, "×", size=22, color=RED, ha="center", bold=True)
    aviso = texto(ax, 56, 19.6, "¡El mozo NO entra a la despensa!  ·  Ningún controller usa JdbcTemplate",
                  size=7.5, color=RED, ha="center", italic=True, z=8)
    aviso.set_bbox(dict(facecolor=WHITE, edgecolor="none", pad=1.5))

    texto(ax, 3, 2.2, "Cada capa solo conversa con la de al lado: si cambia la base de datos, el mozo y el "
          "cocinero no se enteran.", size=7.5, color=MUTED, italic=True)
    guardar(fig, ruta("A2_01_capas_restaurante.png"))


# ============================================== 2 · pedido en capas (mesa de partes)
def fig_pedido_capas():
    fig, ax = lienzo(10, 7.4, 100, 74)
    titulo_figura(ax, 3, 69, "Figura A2 · Arquitectura en capas",
                  "Crear un pedido en Coral Shop: el recorrido por las tres capas", size_k=8, size_t=14)

    persona(ax, 9, 59, PRIMARY, "Cliente")
    texto(ax, 15, 59, "POST /api/orders", size=8, color=PRIMARY, bold=True)
    texto(ax, 15, 52.5, "{ lines, addressId,\n  shippingMethodCode }", size=7, color=MUTED, lh=1.3)
    flecha(ax, (15, 56.5), (29, 56.5), color=PRIMARY)

    capas = [
        (49.5, "PRESENTACIÓN", "CustomerOrderController  +  CreateOrderRequest (DTO)", BLUE,
         "valida el FORMATO con @Valid:\ncampos obligatorios, cantidades\n1 a 10 000, teléfono  →  400"),
        (31.5, "NEGOCIO", "OrderService  ·  PricingService  ·  QuantityPolicy", PRIMARY,
         "aplica las REGLAS en una transacción:\nzona válida para la técnica, diseño propio,\n"
         "escala de mayoreo, precios  →  422\nstock insuficiente  →  409"),
        (13.5, "DATOS", "OrderRepository  ·  ProductRepository", GREEN,
         "único lugar con SQL, siempre con «?»:\nUPDATE … SET stock = stock − ?\nWHERE id = ? AND stock >= ?"),
    ]
    for i, (y, titulo, clases, color, nota_) in enumerate(capas, start=1):
        bloque(ax, 30, y, 40, 11, color, titulo, clases, size_t=10, size_s=7.6)
        numero(ax, 29.2, y + 11, i)
        texto(ax, 73, y + 5.5, nota_, size=7, color=color, italic=True, lh=1.3)
    for y in (49.5, 31.5):
        flecha(ax, (50, y), (50, y - 7), color=BLUE)
        texto(ax, 52, y - 3.5, "llama", size=7, color=MUTED, italic=True)
    flecha(ax, (50, 13.5), (50, 10.2), color=GREEN)
    cilindro(ax, 35, 1.5, 30, 8.8, GREEN, "orders · order_lines · order_items\nproduct_variants", size=7)
    numero(ax, 33.5, 10, 4)

    caja(ax, 3, 24, 22, 18, fill=CARD, edge=MUTED, lw=1.0, r=0.6, ls="dashed")
    texto(ax, 14, 37.5, "Modelo", size=9, color=TEXT, ha="center", bold=True)
    texto(ax, 14, 31.5, "PricedLine · NewOrder\nOrderStatus · LineAmounts", size=7.2, color=MUTED,
          ha="center", lh=1.35)
    texto(ax, 14, 26.3, "lo usan las 3 capas", size=7, color=MUTED, ha="center", italic=True)

    texto(ax, 85, 4.5, "Regla de oro:\ncada capa conoce\nSOLO a la de abajo", size=8, color=PRIMARY,
          ha="center", italic=True, bold=True, lh=1.3)
    guardar(fig, ruta("A2_02_capas_pedido.png"))


# ===================================================== 3 · cliente-servidor
def fig_cliente_servidor():
    fig, ax = lienzo(10, 5.6, 100, 56)
    titulo_figura(ax, 3, 51, "Figura A3 · Arquitectura cliente-servidor",
                  "Varios clientes, un servidor de aplicación y una base de datos", size_k=8, size_t=14)

    clientes = [(36, "Navegador · cliente", "tienda en React 19"),
                (24, "Navegador · administrador", "panel en React 19"),
                (12, "Postman / pruebas", "colección de la API")]
    for y, titulo, sub in clientes:
        bloque(ax, 3, y, 22, 8, BLUE, titulo, sub, size_t=8.5, size_s=7.2)
        flecha(ax, (25, y + 4), (40, 28), color=BLUE, lw=1.3)
    texto(ax, 32.5, 46.4, "HTTP + JSON", size=8, color=BLUE, ha="center", bold=True)
    texto(ax, 32.5, 43.6, "cookie JSESSIONID\n+ cabecera X-CSRF-TOKEN", size=6.8, color=MUTED, ha="center",
          lh=1.25)

    caja(ax, 40, 9, 34, 34, fill=CARD, edge=PRIMARY, lw=1.5, r=0.8)
    texto(ax, 57, 39.6, "SERVIDOR", size=9.5, color=PRIMARY, ha="center", bold=True)
    texto(ax, 57, 36.8, "Spring Boot 3.5 · Java 21 · Tomcat embebido :8082", size=7, color=MUTED,
          ha="center")
    for i, (nombre, color) in enumerate((("Spring Security · sesión y roles", ACCENT),
                                         ("@RestController (presentación)", BLUE),
                                         ("@Service (negocio)", PRIMARY),
                                         ("@Repository · JdbcTemplate (datos)", GREEN))):
        etiqueta(ax, 43, 29 - i * 4.8, 28, 3.6, nombre, fill=color, size=7.4)

    flecha(ax, (74, 26), (81, 26), color=GREEN, style="<|-|>")
    texto(ax, 77.5, 28.3, "JDBC", size=7, color=GREEN, ha="center", bold=True)
    cilindro(ax, 81, 19, 16, 14, GREEN, "PostgreSQL 16\n25 tablas\nFlyway V1–V5", size=7.4)

    caja(ax, 3, 1.5, 94, 6, fill=WHITE, edge=LINE, lw=1.0, r=0.5)
    texto(ax, 5, 4.5, "Desarrollo: Vite (:5173) reenvía /api → localhost:8082.   Producción (prevista): "
          "Vercel sirve el frontend y reenvía /api → BACKEND_URL.", size=7.3, color=TEXT)
    guardar(fig, ruta("A2_03_cliente_servidor.png"))


# ================================================================== 4 · MVC
def fig_mvc():
    fig, ax = lienzo(10, 5.8, 100, 58)
    titulo_figura(ax, 3, 53, "Figura A4 · Modelo-Vista-Controlador",
                  "MVC con React como vista y Spring como controlador", size_k=8, size_t=14)

    bloque(ax, 32, 34, 30, 11, GREEN, "MODELO", "records y entidades + reglas\nProductView · OrderDetailView\n"
           "User (@Entity) · servicios", size_t=10, size_s=7.2)
    bloque(ax, 3, 6, 30, 12, BLUE, "VISTA", "React 19 (SPA)\npages/ · features/\ncarrito, checkout, panel",
           size_t=10, size_s=7.2)
    bloque(ax, 61, 6, 30, 12, PRIMARY, "CONTROLADOR", "@RestController\nCatalogController\n"
           "CustomerOrderController", size_t=10, size_s=7.2)

    flecha(ax, (33, 14), (61, 14), color=BLUE)
    texto(ax, 47, 16, "petición HTTP (fetch)", size=7.2, color=BLUE, ha="center")
    flecha(ax, (61, 9.5), (33, 9.5), color=PRIMARY)
    texto(ax, 47, 7.5, "respuesta JSON", size=7.2, color=PRIMARY, ha="center")
    flecha(ax, (74, 18), (58, 34), color=PRIMARY)
    texto(ax, 73, 27, "invoca el Service", size=7.2, color=PRIMARY)
    flecha(ax, (52, 34), (68, 18.3), color=GREEN, conn="arc3,rad=0.25")
    texto(ax, 55.5, 24.2, "datos (DTO)", size=7.2, color=GREEN)

    caja(ax, 3, 28, 25, 16.5, fill=CARD, edge=LINE, lw=1.0, r=0.6)
    texto(ax, 15.5, 41.5, "Lo visto en clase", size=8, color=PRIMARY, ha="center", bold=True)
    texto(ax, 15.5, 34.5, "JavaBeans → Modelo\nServlets → Controlador\nJSP → Vista", size=7.4,
          color=TEXT, ha="center", lh=1.4)
    texto(ax, 15.5, 29.6, "aquí la Vista vive en el navegador", size=6.8, color=MUTED, ha="center",
          italic=True)
    texto(ax, 94, 41, "El controlador no hace\nforward a una JSP:\nresponde JSON y la vista\nReact lo dibuja.",
          size=7.2, color=MUTED, ha="right", italic=True, lh=1.3)
    guardar(fig, ruta("A2_04_mvc.png"))


# ============================================================ 5 · eventos
def fig_eventos():
    fig, ax = lienzo(10, 5.6, 100, 56)
    titulo_figura(ax, 3, 51, "Figura A5 · Arquitectura dirigida por eventos",
                  "Propuesta para la fase 4: el evento OrderStatusChanged", size_k=8, size_t=14)
    etiqueta(ax, 72, 49.5, 25, 3.6, "PROPUESTA · AÚN NO IMPLEMENTADO", fill=GOLD, size=7)

    publicadores = [(5, "PaymentService", "publica al aprobarse el pago"),
                    (30, "OrderAdminService", "publica al avanzar o cancelar")]
    for x, titulo, sub in publicadores:
        bloque(ax, x, 34, 22, 8, PRIMARY, titulo, sub, size_t=8.6, size_s=7)
        ax.plot([x + 11, x + 11], [34, 24.5], color=PRIMARY, lw=1.6, zorder=3)
        texto(ax, x + 12, 29, "publica", size=6.8, color=PRIMARY, italic=True)

    ax.plot([3, 97], [24, 24], color=RED, lw=3.2, zorder=3)
    texto(ax, 4, 21.4, "BUS DE EVENTOS · ApplicationEventPublisher de Spring", size=7.8, color=RED, bold=True)

    caja(ax, 56, 31, 41, 12, fill=CARD, edge=GOLD, lw=1.2, r=0.6)
    texto(ax, 76.5, 39.8, "OrderStatusChanged", size=9, color=GOLD, ha="center", bold=True)
    texto(ax, 76.5, 34.6, "orderId · orderCode · from · to\nchangedBy · changedAt", size=7.2, color=TEXT,
          ha="center", lh=1.3)
    flecha(ax, (55.5, 37), (49, 37), color=GOLD, ls="dashed", style="-", size=6)

    suscriptores = [(5, "NotificationListener", "aviso en «Mis pedidos»"),
                    (37, "AuditListener", "bitácora de cambios"),
                    (69, "EmailListener", "correo al cliente (futuro)")]
    for x, titulo, sub in suscriptores:
        ax.plot([x + 13, x + 13], [24, 16], color=GREEN, lw=1.6, zorder=3)
        bloque(ax, x, 8, 26, 8, GREEN, titulo, sub, size_t=8.6, size_s=7)
    texto(ax, 4, 3.5, "@TransactionalEventListener(AFTER_COMMIT): los suscriptores reaccionan solo si el cambio "
          "de estado se guardó. Quien publica no conoce a quien escucha.", size=7.2, color=MUTED, italic=True)
    guardar(fig, ruta("A2_05_eventos.png"))


def main():
    print("Generando figuras del avance 2 en", BASE)
    fig_restaurante()
    fig_pedido_capas()
    fig_cliente_servidor()
    fig_mvc()
    fig_eventos()


if __name__ == "__main__":
    main()
