# -*- coding: utf-8 -*-
"""Genera todas las figuras del informe y de la presentación en entregables/figuras/."""

import os
import textwrap

from matplotlib.patches import Ellipse, Polygon

from estilo import (
    lienzo, caja, texto, flecha, etiqueta, titulo_figura, guardar,
    DARK, PRIMARY, ACCENT, ROSE, CREAM, CARD, BLUE, GREEN, GOLD,
    TEXT, MUTED, LINE, WHITE, TITLE_FONT, BODY_FONT,
)
import esquema

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "clase_entregables", "figuras")
os.makedirs(BASE, exist_ok=True)


def ruta(n):
    return os.path.join(BASE, n)


# =========================================================== 01 · ISHIKAWA
def fig_ishikawa():
    fig, ax = lienzo(14, 7.8, 140, 78)

    titulo_figura(ax, 5, 72, "Diagrama de causa-efecto",
                  "Por qué Coral Shop pierde ventas y pedidos personalizados")

    y0 = 34.0                       # altura de la espina
    x_ini, x_fin = 8, 113

    # espina central
    flecha(ax, (x_ini, y0), (x_fin, y0), color=PRIMARY, lw=2.6, size=22)

    # cabeza del pescado (efecto)
    caja(ax, 113, 22, 24, 24, fill=PRIMARY, r=0.8)
    texto(ax, 125, 42.6, "EFECTO", size=8.5, color=ROSE, bold=True, ha="center")
    texto(ax, 125, 32.8,
          "Coral Shop no logra\natender la demanda de\nropa juvenil personalizada\ny pierde pedidos, stock\ny trazabilidad",
          size=9.8, color=CREAM, bold=True, font=TITLE_FONT, ha="center", lh=1.5)

    espinas_sup = [
        ("MÉTODO", [
            "Pedido por chat, sin formato",
            "Sin aprobación del arte",
            "Cotización manual del estampado",
            "El stock no se reserva",
        ]),
        ("TECNOLOGÍA (MÁQUINA)", [
            "No hay canal de venta propio",
            "Inventario en hojas de cálculo",
            "Catálogo solo en redes",
            "Catálogo y almacén sin integrar",
        ]),
        ("MEDICIÓN", [
            "No se mide la conversión",
            "Pedidos perdidos sin registro",
            "Sin histórico de tallas",
            "Tiempo de respuesta sin control",
        ]),
    ]
    espinas_inf = [
        ("MANO DE OBRA", [
            "Atención uno a uno por chat",
            "Personal sin formación digital",
            "Una sola persona cotiza",
            "Reprocesos por error de tipeo",
        ]),
        ("MATERIALES E INSUMOS", [
            "Prenda base sin reserva",
            "Insumos sin punto de reorden",
            "Artes en formatos dispares",
            "Mermas por arte mal aprobado",
        ]),
        ("ENTORNO", [
            "Marketplaces más competitivos",
            "El joven espera autoservicio",
            "Demanda muy estacional",
            "Competencia de bajo precio",
        ]),
    ]

    bases_x = [22, 52, 82]

    def dibujar_espina(xb, categoria, causas, arriba):
        signo = 1 if arriba else -1
        yt = y0 + signo * 26
        xt = xb + 12
        ax.plot([xb, xt], [y0, yt], color=ACCENT, lw=2.0, zorder=3,
                solid_capstyle="round")
        # etiqueta de categoria
        ancho = 26
        etiqueta(ax, xt - ancho / 2 + 2, yt + (1.4 if arriba else -4.6), ancho, 3.2,
                 categoria, fill=PRIMARY, size=8.2)
        # causas repartidas a lo largo de la espina
        for i, c in enumerate(causas):
            t = 0.22 + i * 0.245
            px = xb + (xt - xb) * t
            py = y0 + (yt - y0) * t
            ax.plot([px, px + 1.8], [py, py], color=ACCENT, lw=1.0, zorder=3)
            texto(ax, px + 2.5, py, c, size=7.4, color=TEXT)

    for xb, (cat, causas) in zip(bases_x, espinas_sup):
        dibujar_espina(xb, cat, causas, True)
    for xb, (cat, causas) in zip(bases_x, espinas_inf):
        dibujar_espina(xb, cat, causas, False)

    guardar(fig, ruta("01_ishikawa.png"))


# ============================================================= 02 · CANVAS
def fig_canvas():
    fig, ax = lienzo(14, 8.0, 140, 80)
    titulo_figura(ax, 5, 74, "Business Model Canvas",
                  "Modelo de negocio de Coral Shop S.A.C.")

    def bloque(x, y, w, h, tit, items, color=PRIMARY, fill=CARD):
        caja(ax, x, y, w, h, fill=fill, edge=LINE, lw=0.8, r=0.7)
        caja(ax, x, y + h - 3.2, w, 3.2, fill=color, r=0.7)
        texto(ax, x + 1.2, y + h - 1.6, tit.upper(), size=7.8, color=WHITE, bold=True)
        yy = y + h - 5.2
        for it in items:
            lineas = textwrap.wrap(it, int((w - 3.5) * 2.05))
            ax.plot([x + 1.4], [yy], marker="o", ms=1.9, color=color, zorder=5)
            for k, ln in enumerate(lineas):
                texto(ax, x + 2.6, yy - k * 2.0, ln, size=7.2, color=TEXT)
            yy -= len(lineas) * 2.0 + 1.1

    L, R = 5, 135
    ancho_col = (R - L - 4 * 1.2) / 5
    xs = [L + i * (ancho_col + 1.2) for i in range(5)]
    y_base_inf = 5
    alto_inf = 15
    y_sup = y_base_inf + alto_inf + 1.5
    alto_sup = 45
    alto_medio = (alto_sup - 1.2) / 2

    bloque(xs[0], y_sup, ancho_col, alto_sup, "Socios clave", [
        "Talleres de confección de Gamarra (prenda base)",
        "Proveedores de insumos DTF, vinil y tintas",
        "Couriers: Olva, Shalom y motorizados en Lima",
        "Pasarela de pagos (a futuro) y Yape-Plin",
        "Microinfluencers universitarios de Lima",
        "Software libre: Java, Spring, PostgreSQL y React",
    ], color=PRIMARY)

    bloque(xs[1], y_sup + alto_medio + 1.2, ancho_col, alto_medio, "Actividades clave", [
        "Diseño y producción de estampados",
        "Gestión del catálogo y del inventario por variante",
        "Atención y seguimiento del pedido",
        "Marketing de contenidos en redes",
    ], color=BLUE)

    bloque(xs[1], y_sup, ancho_col, alto_medio, "Recursos clave", [
        "Plataforma web propia (este proyecto)",
        "Máquinas de estampado DTF y plancha",
        "Stock de prendas base por talla y color",
        "Equipo de diseño gráfico",
    ], color=BLUE)

    bloque(xs[2], y_sup, ancho_col, alto_sup, "Propuesta de valor", [
        "Diseña tu propio polo o polera en línea y mira cómo queda antes de comprar",
        "Precio del estampado calculado al instante, sin esperar cotización por chat",
        "Stock real por talla y color: lo que se ve disponible, existe",
        "Desde 1 unidad; por mayor con 5 %, 10 % o 15 % de descuento repartido entre tallas",
        "Entrega en 72 horas en Lima con seguimiento del estado del pedido",
    ], color=ACCENT)

    bloque(xs[3], y_sup + alto_medio + 1.2, ancho_col, alto_medio, "Relación con clientes", [
        "Autoservicio 24/7 en la tienda web",
        "Cuenta con historial de pedidos y línea de tiempo",
        "Aviso en la campana en cada cambio de estado",
        "Precio y descuento por volumen a la vista",
    ], color=GREEN)

    bloque(xs[3], y_sup, ancho_col, alto_medio, "Canales", [
        "Tienda virtual propia (canal principal)",
        "Instagram y TikTok como captación",
        "WhatsApp solo para postventa",
        "Tienda física para recojo",
    ], color=GREEN)

    bloque(xs[4], y_sup, ancho_col, alto_sup, "Segmentos de clientes", [
        "Jóvenes de 16 a 28 años de Lima Metropolitana que compran ropa urbana en línea",
        "Estudiantes universitarios y de institutos que encargan polos de promoción o de facultad",
        "Grupos pequeños: equipos deportivos, bandas, colectivos y emprendimientos",
        "Compradores de regalos personalizados",
    ], color=GOLD)

    bloque(xs[0], y_base_inf, ancho_col * 2 + 1.2, alto_inf, "Estructura de costos", [
        "Compra de prenda base e insumos de estampado  ·  Planilla de 12 colaboradores",
        "Alquiler del local y del taller  ·  Servidor, dominio y comisiones de pago",
        "Publicidad digital  ·  Mermas por estampados rechazados",
    ], color=PRIMARY)

    bloque(xs[2], y_base_inf, ancho_col * 3 + 2.4, alto_inf, "Fuentes de ingresos", [
        "Venta de prendas de catálogo  ·  Recargo por personalización (técnica y zonas)",
        "Pedidos por volumen para promociones y grupos  ·  Cobro del envío según modalidad",
        "Pedidos por mayor (paquetes de 3, 6 y 12) que elevan el ticket promedio",
    ], color=ACCENT)

    guardar(fig, ruta("02_canvas.png"))


# ======================================================== 03 · ARQUITECTURA
def fig_arquitectura():
    fig, ax = lienzo(14, 9.4, 140, 94)
    n_tablas, _, _ = esquema.totales()
    titulo_figura(ax, 5, 88, "Arquitectura de la solución",
                  "Cliente-servidor en capas: React en el navegador, Spring Boot en el servidor")

    # ---------------------------------------------------------- capa cliente
    caja(ax, 5, 68, 96, 14.5, fill=CARD, edge=BLUE, lw=1.2, r=0.8)
    etiqueta(ax, 6.5, 78.6, 20, 3.2, "VISTA · NAVEGADOR", fill=BLUE, size=7.8)
    texto(ax, 28.5, 80.2, "SPA React 19 + Vite 8 + Tailwind 4 + React Router 7  ·  localhost:5173",
          size=9.2, color=TEXT, bold=True)
    chips = ["pages/\npantallas", "features/\npor funcionalidad", "Personalizador\ny vista previa",
             "Carrito en\nlocalStorage", "http-client.js\ncookie + CSRF"]
    for i, c in enumerate(chips):
        x = 7.5 + i * 18.4
        caja(ax, x, 69.3, 17.2, 7.6, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
        texto(ax, x + 8.6, 73.1, c, size=7.8, color=BLUE, bold=True, ha="center", lh=1.35)

    # ------------------------------------------------------------- transporte
    flecha(ax, (53, 67.6), (53, 62.4), color=PRIMARY, lw=2.0, size=16)
    flecha(ax, (48, 62.4), (48, 67.6), color=ACCENT, lw=2.0, size=16)
    texto(ax, 57, 66.3, "HTTP · JSON en /api/…  ·  cookie JSESSIONID  ·  cabecera X-CSRF-TOKEN",
          size=8.0, color=PRIMARY, bold=True)
    texto(ax, 57, 63.5, "El proxy de Vite reenvía /api a localhost:8082: mismo origen, sin CORS",
          size=7.8, color=MUTED)

    # ------------------------------------------------- contenedor de servidor
    caja(ax, 5, 19.5, 96, 43, fill="#FAF4F1", edge=PRIMARY, lw=1.4, r=0.9)
    etiqueta(ax, 6.5, 57.6, 36, 3.4, "SPRING BOOT 3.5 · TOMCAT EMBEBIDO", fill=PRIMARY, size=7.8)
    texto(ax, 44.5, 59.3, "API REST  ·  Java 21  ·  localhost:8082  ·  paquete com.coralshop",
          size=8.8, color=PRIMARY, bold=True)

    caja(ax, 7.5, 51.4, 91, 5.0, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
    texto(ax, 9.5, 53.9, "SPRING SECURITY", size=8, color=ACCENT, bold=True)
    for i, f in enumerate(["CsrfFilter", "Sesión JSESSIONID", "Login por formulario",
                           "Autorización por rol", "DispatcherServlet"]):
        etiqueta(ax, 30 + i * 13.6, 52.4, 12.8, 3.0, f, fill=ROSE, color=PRIMARY, size=6.7)

    capas_srv = [
        ("CONTROLLER", "@RestController + DTO con @Valid  →  400", PRIMARY,
         ["CatalogController", "QuoteController", "DesignController",
          "CustomerOrderController", "PaymentController", "AdminOrderController"]),
        ("SERVICE", "@Service + @Transactional  →  422 / 409", BLUE,
         ["PricingService", "QuantityPolicy", "OrderService",
          "OrderStatusPolicy", "PaymentService", "OrderAdminService"]),
        ("REPOSITORY", "@Repository + JdbcTemplate (JPA solo en la cuenta)", GREEN,
         ["ProductRepository", "CustomizationRepository", "DesignRepository",
          "OrderRepository", "PaymentRepository", "UserRepository"]),
    ]
    y = 43.6
    for tit, sub, color, comps in capas_srv:
        caja(ax, 7.5, y, 91, 7.0, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
        caja(ax, 7.5, y, 1.1, 7.0, fill=color, r=0.4)
        texto(ax, 10.2, y + 4.9, tit, size=8.2, color=color, bold=True)
        texto(ax, 10.2, y + 2.2, sub, size=6.9, color=MUTED, italic=True)
        for i, c in enumerate(comps):
            fila, col = divmod(i, 3)
            etiqueta(ax, 49 + col * 16.4, y + 3.9 - fila * 3.1, 15.6, 2.6, c, fill=color, size=6.1)
        y -= 7.5

    caja(ax, 7.5, 24.6, 91, 3.6, fill="#F2E7E2", edge=LINE, lw=0.8, r=0.5)
    texto(ax, 9.5, 26.4, "EVENTOS", size=7.6, color=GOLD, bold=True)
    texto(ax, 21, 26.4, "OrderStatusChanged  →  ApplicationEventPublisher  →  AuditListener (BEFORE_COMMIT)  ·  "
          "NotificationListener (AFTER_COMMIT)", size=6.9, color=TEXT)
    caja(ax, 7.5, 20.4, 91, 3.6, fill="#F2E7E2", edge=LINE, lw=0.8, r=0.5)
    texto(ax, 9.5, 22.2, "MODELO", size=7.6, color=PRIMARY, bold=True)
    texto(ax, 21, 22.2, "records inmutables (DTO y modelo) que cruzan las capas  ·  entidad User (JPA)  ·  "
          "GlobalExceptionHandler → { status, message, errors }", size=6.9, color=TEXT)

    # ------------------------------------------------------------ persistencia
    caja(ax, 5, 5.5, 46, 12.5, fill=CARD, edge=GREEN, lw=1.2, r=0.8)
    etiqueta(ax, 6.5, 14.2, 17, 3.0, "PERSISTENCIA", fill=GREEN, size=7.6)
    texto(ax, 25, 15.7, "PostgreSQL 16 (Docker)", size=10.5, color=GREEN, bold=True, font=TITLE_FONT)
    texto(ax, 7, 11.2,
          f"{n_tablas} tablas  ·  migraciones Flyway V1 a V6\n"
          "Claves foráneas, CHECK e índices únicos en la propia base\n"
          "Diseños del cliente en bytea (PNG/JPG hasta 5 MB)",
          size=7.2, color=TEXT, lh=1.5)

    caja(ax, 55, 5.5, 46, 12.5, fill=CARD, edge=GOLD, lw=1.2, r=0.8)
    etiqueta(ax, 56.5, 14.2, 21, 3.0, "DOCUMENTACIÓN Y PRUEBAS", fill=GOLD, size=7.0)
    texto(ax, 79, 15.7, "Calidad", size=10.5, color=GOLD, bold=True, font=TITLE_FONT)
    texto(ax, 57, 11.2,
          "Swagger UI en /api/docs (springdoc-openapi)\n"
          "Colección Postman de toda la API (backend/postman)\n"
          "JUnit 5 + Testcontainers: 73 pruebas automatizadas",
          size=7.2, color=TEXT, lh=1.5)

    flecha(ax, (28, 20.4), (28, 18.2), color=GREEN, lw=1.8, size=14)
    flecha(ax, (78, 20.4), (78, 18.2), color=GOLD, lw=1.8, size=14)

    # ------------------------------------------------------- panel transversal
    caja(ax, 104, 4.5, 31, 78, fill=DARK, r=0.9)
    texto(ax, 106.5, 78.5, "ASPECTOS", size=8.5, color=ROSE, bold=True)
    texto(ax, 106.5, 74.8, "transversales", size=15, color=CREAM, bold=True, font=TITLE_FONT)
    items = [
        ("Seguridad", "BCrypt para contraseñas, sesión de servidor (JSESSIONID), token CSRF y roles: ROLE_ADMIN incluye a ROLE_USER."),
        ("Validación", "Formato en el DTO (@Valid) y reglas en el service. El servidor recalcula precio y stock: nunca confía en el navegador."),
        ("Transacciones", "@Transactional en el service. Stock con UPDATE condicional; el pago bloquea el pedido con SELECT … FOR UPDATE."),
        ("Trazabilidad", "order_status_history, audit_log y notifications registran cada cambio de estado del pedido."),
        ("Errores", "JSON uniforme con 400, 401, 403, 404, 409 y 422, mostrado tal cual por el frontend."),
        ("Ejecución local", "PostgreSQL en Docker, backend con Maven y frontend con Vite; el perfil demo carga datos ficticios."),
    ]
    yy = 70
    for t, d in items:
        texto(ax, 106.5, yy, t, size=9, color=ROSE, bold=True)
        texto(ax, 106.5, yy - 4.8, d, size=7.0, color=CREAM, wrap=42, lh=1.5, va="center")
        yy -= 11.3

    guardar(fig, ruta("03_arquitectura.png"))


# ====================================================== 04 · FLUJO PETICION
def fig_flujo():
    fig, ax = lienzo(14, 8.0, 140, 80)
    titulo_figura(ax, 5, 73.5, "Flujo de una petición",
                  "Caso: el cliente confirma el pedido de 12 polos bordados (4 S, 4 M, 4 L)")

    actores = [
        ("React", "checkout", BLUE, 12),
        ("Spring Security", "sesión + CSRF", ACCENT, 32),
        ("CustomerOrder\nController", "controller", PRIMARY, 53),
        ("OrderService", "service", BLUE, 75),
        ("Repositories", "JdbcTemplate", GREEN, 97),
        ("PostgreSQL", "base de datos", GOLD, 118),
    ]
    for nom, sub, color, x in actores:
        caja(ax, x - 8.5, 61, 17, 7.4, fill=color, r=0.7)
        texto(ax, x, 66.0 if "\n" not in nom else 65.6, nom, size=8.2, color=WHITE, bold=True,
              ha="center", lh=1.2)
        texto(ax, x, 62.3, sub, size=6.8, color=CREAM, ha="center")
        ax.plot([x, x], [10.5, 61], color=LINE, lw=1.0, ls=(0, (3, 3)), zorder=1)

    pasos = [
        (12, 32, "POST /api/orders  ·  cookie JSESSIONID  ·  X-CSRF-TOKEN", 57.5, True),
        (32, 53, "Sesión válida, ROLE_USER, token CSRF correcto", 53.8, True),
        (53, 75, "CreateOrderRequest validado con @Valid (si no, 400)", 50.1, True),
        (75, 97, "@Transactional: PricingService recalcula precios; QuantityPolicy → docena (−15 %)", 46.4, True),
        (97, 118, "UPDATE product_variants SET stock = stock − 4 WHERE id = ? AND stock >= 4", 42.7, True),
        (118, 97, "1 fila por talla (0 filas = sin stock → 409 y rollback)", 39.0, False),
        (97, 118, "INSERT orders, order_lines, order_line_zones, order_items, order_status_history", 35.3, True),
        (75, 75, "", 31.6, True),
        (118, 75, "commit", 27.9, False),
        (75, 53, "CreatedOrderResponse { orderCode: CS-…, total, status: PENDIENTE_PAGO }", 24.2, False),
        (53, 12, "201 Created  ·  JSON  →  React vacía el carrito y abre el pago", 20.5, False),
    ]
    for x1, x2, txt, y, ida in pasos:
        if x1 == x2:
            continue
        color = PRIMARY if ida else GREEN
        flecha(ax, (x1, y), (x2, y), color=color, lw=1.5, size=11,
               ls="solid" if ida else (0, (4, 2)))
        texto(ax, (x1 + x2) / 2, y + 1.7, txt, size=6.8, color=color if ida else MUTED,
              bold=ida, ha="center")
    # evento publicado dentro de la transacción
    caja(ax, 66, 30.2, 18, 3.4, fill=CARD, edge=GOLD, lw=1.0, r=0.5)
    texto(ax, 75, 31.9, "publica OrderStatusChanged", size=6.4, color=GOLD, bold=True, ha="center")

    caja(ax, 5, 1.5, 130, 8.0, fill=CARD, edge=LINE, lw=0.8, r=0.7)
    texto(ax, 7, 7.3, "REGLAS QUE PROTEGEN ESTE FLUJO", size=7.6, color=ACCENT, bold=True)
    texto(ax, 7, 4.1,
          "Una regla rota (zona que no admite la técnica, diseño ajeno, reparto que no suma la cantidad) responde 422; una talla sin stock responde 409 y la "
          "transacción se deshace completa: nunca queda un pedido a medio grabar. Al confirmarse, AuditListener registra el cambio y NotificationListener avisa al cliente.",
          size=7.2, color=TEXT, wrap=178, lh=1.5)

    guardar(fig, ruta("04_flujo_peticion.png"))


# ========================================================= 05 · CASOS DE USO
def fig_casos_uso():
    fig, ax = lienzo(14, 9.0, 140, 90)
    titulo_figura(ax, 5, 84, "Diagrama de casos de uso",
                  "Actores del sistema y funcionalidades implementadas")

    caja(ax, 30, 5, 80, 74, fill="#FCFAF8", edge=PRIMARY, lw=1.3, r=0.8)
    texto(ax, 70, 75.5, "SISTEMA CORAL SHOP", size=10, color=PRIMARY, bold=True,
          ha="center", font=TITLE_FONT)

    def actor(x, y, nombre, desc, color):
        ax.plot([x], [y + 3.6], marker="o", ms=7, mfc=color, mec=color, zorder=5)
        ax.plot([x, x], [y + 3.1, y + 0.6], color=color, lw=1.8, zorder=5)
        ax.plot([x - 1.9, x + 1.9], [y + 2.3, y + 2.3], color=color, lw=1.8, zorder=5)
        ax.plot([x, x - 1.6], [y + 0.6, y - 1.8], color=color, lw=1.8, zorder=5)
        ax.plot([x, x + 1.6], [y + 0.6, y - 1.8], color=color, lw=1.8, zorder=5)
        texto(ax, x, y - 4.0, nombre, size=8.4, color=color, bold=True, ha="center")
        texto(ax, x, y - 6.6, desc, size=6.6, color=MUTED, ha="center", wrap=22, lh=1.35)

    def uc(x, y, txt, color):
        e = Ellipse((x, y), 24, 5.0, facecolor=WHITE, edgecolor=color, lw=1.1, zorder=4)
        ax.add_patch(e)
        texto(ax, x, y, txt, size=6.9, color=TEXT, ha="center", wrap=34, lh=1.2, z=5)
        return (x, y)

    izq = [
        ("CU-01 Explorar y filtrar el catálogo", BLUE),
        ("CU-02 Ver la ficha del producto", BLUE),
        ("CU-03 Personalizar: técnica, zonas y diseño", ACCENT),
        ("CU-04 Repartir por tallas y cotizar mayoreo", ACCENT),
        ("CU-05 Gestionar el carrito", GREEN),
        ("CU-06 Registrarse e iniciar sesión", PRIMARY),
        ("CU-07 Confirmar el pedido (checkout)", GREEN),
        ("CU-08 Pagar el pedido (simulado)", GREEN),
        ("CU-09 Seguir pedidos y ver avisos", GOLD),
    ]
    der = [
        ("CU-10 Consultar el tablero", GOLD),
        ("CU-11 Gestionar productos y variantes", BLUE),
        ("CU-12 Gestionar categorías", BLUE),
        ("CU-13 Atender la bandeja de pedidos", GREEN),
        ("CU-14 Cambiar el estado del pedido", GREEN),
        ("CU-15 Descargar el diseño del cliente", ACCENT),
        ("CU-16 Gestionar usuarios y roles", PRIMARY),
        ("CU-17 Auditar cambios de estado", GOLD),
        ("CU-18 Notificar al cliente", GOLD),
    ]
    y0, dy = 70, 7.6
    pos_izq = [uc(50, y0 - i * dy, t, c) for i, (t, c) in enumerate(izq)]
    pos_der = [uc(90, y0 - i * dy, t, c) for i, (t, c) in enumerate(der)]

    actor(14, 52, "Cliente", "Compra, personaliza y sigue su pedido", PRIMARY)
    actor(14, 22, "Invitado", "Navega, personaliza y arma su carrito", MUTED)
    actor(126, 58, "Administrador", "Gestiona la operación (también es cliente)", PRIMARY)
    actor(126, 22, "Sistema", "Reacciona al evento OrderStatusChanged", GOLD)

    def unir(px, py, casos, lado):
        for (cx, cy) in casos:
            xo = cx - 12 if lado == "izq" else cx + 12
            ax.plot([px, xo], [py, cy], color=LINE, lw=0.7, zorder=2)

    unir(16, 52, pos_izq, "izq")
    unir(16, 22, pos_izq[:6], "izq")
    unir(124, 58, pos_der[:7], "der")
    unir(124, 22, pos_der[7:], "der")

    texto(ax, 5, 2.2,
          "El invitado llega hasta el carrito; para subir el diseño y confirmar el pedido debe iniciar sesión y vuelve al paso en que estaba. "
          "Un administrador también compra como cliente (ROLE_ADMIN incluye a ROLE_USER).",
          size=7.2, color=MUTED, italic=True)

    guardar(fig, ruta("05_casos_uso.png"))


# ======================================================= 06 · ESTADOS PEDIDO
def fig_estados():
    fig, ax = lienzo(14, 7.2, 140, 72)
    titulo_figura(ax, 5, 65, "Máquina de estados del pedido",
                  "Transiciones válidas que controla OrderStatusPolicy")

    estados = [
        ("PENDIENTE_PAGO", "Pedido creado,\nstock reservado", ACCENT),
        ("PAGADO", "Pago simulado\naprobado", BLUE),
        ("EN_PRODUCCION", "Estampado o\nbordado en curso", PRIMARY),
        ("LISTO_PARA_ENVIO", "Empacado,\nespera despacho", "#5B6F8A"),
        ("ENVIADO", "En camino o\nlisto para recojo", GREEN),
        ("ENTREGADO", "Recibido por\nel cliente", GOLD),
    ]
    x0, w, paso, yb, hb = 4, 19, 22.2, 42, 13
    for i, (nom, desc, color) in enumerate(estados):
        x = x0 + i * paso
        caja(ax, x, yb, w, hb, fill=color, r=0.8)
        texto(ax, x + w / 2, yb + 9.0, nom, size=7.6 if len(nom) > 12 else 8.6, color=WHITE,
              bold=True, ha="center")
        texto(ax, x + w / 2, yb + 4.0, desc, size=7.0, color=CREAM, ha="center", lh=1.45)

    quien = ["pago aprobado", "admin", "admin", "admin", "admin"]
    for i, m in enumerate(quien):
        xg = x0 + w + i * paso
        flecha(ax, (xg + 0.2, yb + hb / 2), (xg + paso - w - 0.2, yb + hb / 2),
               color=PRIMARY, lw=1.8, size=12)
        texto(ax, xg + (paso - w) / 2, yb + hb + 2.4, m, size=6.6, color=PRIMARY,
              bold=True, ha="center")

    caja(ax, 22, 15, 22, 11, fill="#8C3B3B", r=0.8)
    texto(ax, 33, 22.4, "CANCELADO", size=9.2, color=WHITE, bold=True, ha="center")
    texto(ax, 33, 18.4, "Estado final.\nRepone el stock", size=7.2,
          color=CREAM, ha="center", lh=1.45)
    for xo, xd, rad in ((x0 + w / 2, 28, 0.15), (x0 + paso + w / 2, 38, -0.15)):
        flecha(ax, (xo, yb - 0.4), (xd, 26.4), color="#8C3B3B", lw=1.3, size=11,
               ls=(0, (4, 2)), conn=f"arc3,rad={rad}")
    texto(ax, 48, 21, "cancelar: solo desde PENDIENTE_PAGO o PAGADO (admin)", size=7.4,
          color="#8C3B3B", bold=True)

    caja(ax, 5, 2, 130, 9, fill=CARD, edge=LINE, lw=0.8, r=0.7)
    texto(ax, 7, 8.2, "IMPLEMENTACIÓN", size=7.6, color=ACCENT, bold=True)
    texto(ax, 7, 4.8,
          "Enum OrderStatus + EnumMap<OrderStatus, EnumSet<OrderStatus>> con las transiciones permitidas; cualquier otro salto responde 422. PAGADO solo se alcanza "
          "con un pago aprobado. Cada cambio escribe order_status_history y publica OrderStatusChanged (auditoría y aviso al cliente).",
          size=7.3, color=TEXT, wrap=170, lh=1.5)

    guardar(fig, ruta("06_estados_pedido.png"))


# ========================================================= 07 · MODULOS
MODULOS_FIG = [
    ("TIENDA", BLUE, [
        ("M01", "Catálogo", "Tipo, categoría, búsqueda y paginación en el servidor"),
        ("M02", "Ficha de producto", "Galería, colores y tallas con stock real por variante"),
        ("M03", "Personalizador", "Técnica, zonas con recargo, subida del diseño y vista previa"),
    ]),
    ("COMPRA", GREEN, [
        ("M04", "Mayoreo y cotización", "Reparto por tallas, escalas 1/3/6/12 y precio del servidor"),
        ("M05", "Carrito", "Una línea por diseño, cotizada y validada al abrirla"),
        ("M06", "Checkout y pago", "Dirección, envío, pedido transaccional y pago simulado"),
    ]),
    ("CLIENTE", GOLD, [
        ("M07", "Cuenta", "Registro, sesión, direcciones del Perú"),
        ("M08", "Mis pedidos", "Historial, detalle y línea de tiempo de estados"),
        ("M09", "Notificaciones", "Campana con avisos de cada cambio de estado"),
    ]),
    ("ADMINISTRACIÓN", PRIMARY, [
        ("M10", "Tablero y usuarios", "Indicadores, pedidos recientes y roles"),
        ("M11", "Catálogo admin", "Productos, variantes, stock, tipos y categorías"),
        ("M12", "Pedidos y auditoría", "Bandeja, estados permitidos, diseño y audit_log"),
    ]),
]


def fig_modulos():
    fig, ax = lienzo(14, 6.4, 140, 64)
    titulo_figura(ax, 5, 58, "Mapa funcional",
                  "Los 12 módulos implementados en la tienda y el panel")
    x0, ancho = 5, 31.8
    for gi, (titulo, color, mods) in enumerate(MODULOS_FIG):
        x = x0 + gi * (ancho + 1.5)
        caja(ax, x, 5, ancho, 46, fill="#FCFAF8", edge=LINE, lw=0.8, r=0.7)
        caja(ax, x, 46.4, ancho, 4.6, fill=color, r=0.7)
        texto(ax, x + ancho / 2, 48.7, titulo, size=8.6, color=WHITE, bold=True, ha="center")
        y = 33.5
        for cod, nom, desc in mods:
            caja(ax, x + 1.4, y, ancho - 2.8, 11, fill=WHITE, edge=LINE, lw=0.7, r=0.6)
            etiqueta(ax, x + 2.6, y + 7.2, 6.2, 2.8, cod, fill=color, size=6.8)
            texto(ax, x + 10, y + 8.6, nom, size=8.2, color=color, bold=True)
            texto(ax, x + 2.6, y + 3.4, desc, size=6.8, color=TEXT, wrap=46, lh=1.4)
            y -= 13.2
    guardar(fig, ruta("07_modulos.png"))


# ============================================================ 08-10 · ER
def _caja_entidad(ax, x, y, w, tabla, color, size_f=6.2):
    """Dibuja una entidad con todos sus campos. Devuelve (alto, mapa_de_campos)."""
    campos = tabla["campos"]
    h_head = 3.4
    h_row = 2.05
    h = h_head + len(campos) * h_row + 0.9
    top = y + h

    caja(ax, x, y, w, h, fill=WHITE, edge=color, lw=1.1, r=0.5)
    caja(ax, x, top - h_head, w, h_head, fill=color, r=0.5)
    texto(ax, x + 1.2, top - h_head / 2, tabla["nombre"], size=7.6, color=WHITE,
          bold=True, font=BODY_FONT)

    mapa = {}
    yy = top - h_head - h_row / 2 - 0.3
    for nombre, tipo, llave, _ in campos:
        if llave.startswith("PK"):
            marca, mc, bold = "PK", "#B8860B", True
        elif llave.startswith("FK"):
            marca, mc, bold = "FK", color, False
        elif llave.startswith("UQ"):
            marca, mc, bold = "UQ", MUTED, False
        else:
            marca, mc, bold = "", MUTED, False
        if marca:
            texto(ax, x + 1.2, yy, marca, size=5.2, color=mc, bold=True)
        # nombre y tipo largos se cruzarían: el nombre baja un punto
        size_n = size_f - 1.0 if len(nombre) + len(tipo) > 33 else size_f
        texto(ax, x + 4.6, yy, nombre, size=size_n, color=TEXT, bold=bold)
        texto(ax, x + w - 1.2, yy, tipo, size=5.4, color=MUTED, ha="right")
        mapa[nombre] = yy
        yy -= h_row
    return h, mapa


def _er(nombre_archivo, titulo, kicker, columnas, w_fig, h_fig, xmax, ymax,
        nota=None):
    fig, ax = lienzo(w_fig, h_fig, xmax, ymax)
    titulo_figura(ax, 4, ymax - 7, kicker, titulo, size_k=6.5, size_t=11.5)

    anchos = (xmax - 8 - (len(columnas) - 1) * 3.0) / len(columnas)
    pos = {}          # tabla -> (x, y, w, h, mapa)
    for ci, col in enumerate(columnas):
        x = 4 + ci * (anchos + 3.0)
        y_cursor = ymax - 12
        for nombre in col:
            t = esquema.TABLA_POR_NOMBRE[nombre]
            color = esquema.MODULOS[t["modulo"]][1]
            h, mapa = _caja_entidad(ax, x, 0, anchos, t, color)
            # reposicionar: se dibujo en y=0, hay que redibujar en la posicion real
            for p in list(ax.patches)[-(len(t["campos"]) + 2):]:
                pass
            plt_y = y_cursor - h
            pos[nombre] = (x, plt_y, anchos, h, mapa, color)
            y_cursor = plt_y - 3.2
    # borrar todo y volver a dibujar en las posiciones definitivas
    ax.clear()
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    titulo_figura(ax, 4, ymax - 7, kicker, titulo, size_k=6.5, size_t=11.5)

    pos_final = {}
    for nombre, (x, y, w, h, _m, color) in pos.items():
        t = esquema.TABLA_POR_NOMBRE[nombre]
        hh, mapa = _caja_entidad(ax, x, y, w, t, color)
        pos_final[nombre] = dict(x=x, y=y, w=w, h=hh, campos=mapa, color=color)

    # relaciones
    for origen, campo, destino, campo_d in esquema.relaciones():
        if origen not in pos_final or destino not in pos_final:
            continue
        o, d = pos_final[origen], pos_final[destino]
        if campo not in o["campos"] or campo_d not in d["campos"]:
            continue
        y1 = o["campos"][campo]
        y2 = d["campos"][campo_d]
        if origen == destino:                      # autorreferencia
            x1 = o["x"] + o["w"]
            flecha(ax, (x1, y1), (x1, y2), color=o["color"], lw=0.9, size=8,
                   conn="arc3,rad=-0.9", style="-|>")
            continue
        if d["x"] >= o["x"] + o["w"] - 1:          # destino a la derecha
            p1 = (o["x"] + o["w"], y1)
            p2 = (d["x"], y2)
            rad = 0.14
        elif o["x"] >= d["x"] + d["w"] - 1:        # destino a la izquierda
            p1 = (o["x"], y1)
            p2 = (d["x"] + d["w"], y2)
            rad = -0.14
        else:                                       # misma columna: ruta ortogonal
            xoff = o["x"] - 2.2
            ax.plot([o["x"], xoff], [y1, y1], color=d["color"], lw=0.8, zorder=1)
            ax.plot([xoff, xoff], [y1, y2], color=d["color"], lw=0.8, zorder=1)
            flecha(ax, (xoff, y2), (d["x"], y2), color=d["color"], lw=0.8, size=7, z=1)
            continue
        flecha(ax, p1, p2, color=d["color"], lw=0.8, size=7,
               conn=f"arc3,rad={rad}", style="-|>", z=1)

    # leyenda
    lx = 4
    texto(ax, lx, 3.6, "PK", size=5.6, color="#B8860B", bold=True)
    texto(ax, lx + 3.0, 3.6, "clave primaria", size=6.4, color=MUTED)
    texto(ax, lx + 20, 3.6, "FK", size=5.6, color=PRIMARY, bold=True)
    texto(ax, lx + 23, 3.6, "clave foránea (la flecha apunta a la tabla referenciada)",
          size=6.4, color=MUTED)
    texto(ax, lx + 78, 3.6, "UQ", size=5.6, color=MUTED, bold=True)
    texto(ax, lx + 81, 3.6, "restricción de unicidad", size=6.4, color=MUTED)
    if nota:
        texto(ax, lx, 1.4, nota, size=6.4, color=MUTED, italic=True)

    guardar(fig, ruta(nombre_archivo))


def fig_er_1():
    _er("08_er_usuarios_catalogo.png",
        "Modelo entidad-relación (1 de 2): usuarios, catálogo e inventario",
        "Diseño de base de datos",
        [
            ["roles", "users", "addresses"],
            ["categories", "brands", "product_types"],
            ["products", "product_images"],
            ["sizes", "colors", "product_variants"],
            ["favorites", "banners", "audit_log"],
        ],
        9.0, 4.8, 185, 88,
        nota="El stock no vive en products sino en product_variants: cada combinación de producto, talla y color tiene su propio SKU y su propio stock.")


def fig_er_2():
    _er("09_er_personalizacion_compra.png",
        "Modelo entidad-relación (2 de 2): personalización, mayoreo, pedidos y pagos",
        "Diseño de base de datos",
        [
            ["customization_techniques", "print_zones", "quantity_tiers"],
            ["product_type_zones", "design_uploads"],
            ["order_lines", "order_line_zones"],
            ["orders", "shipping_methods", "notifications"],
            ["order_items", "order_status_history", "payments"],
        ],
        9.0, 6.0, 178, 110.4,
        nota="order_lines y order_items copian nombre, SKU, talla, color y precios al comprar: el pedido queda inmutable aunque el catálogo cambie después.")


def fig_er_global():
    fig, ax = lienzo(14, 7.4, 140, 74)
    n_tablas, n_campos, n_fk = esquema.totales()
    titulo_figura(ax, 5, 68, "Mapa global del modelo de datos",
                  f"{n_tablas} tablas agrupadas en {len(esquema.MODULOS)} módulos funcionales")

    # (modulo, x, ancho, borde_superior, columnas)
    grupos = [
        ("seguridad", 6, 30, 61, 2),
        ("catalogo", 40, 44, 61, 3),
        ("personalizacion", 88, 46, 61, 2),
        ("compra", 6, 78, 36, 3),
        ("soporte", 88, 46, 36, 2),
    ]
    for mod, x, w, top, cols in grupos:
        nombre, color = esquema.MODULOS[mod]
        tablas = [t["nombre"] for t in esquema.TABLAS if t["modulo"] == mod]
        filas = -(-len(tablas) // cols)
        h = 10.1 + (filas - 1) * 5.4
        y = top - h
        caja(ax, x, y, w, h, fill="#FCFAF8", edge=color, lw=1.2, r=0.7)
        caja(ax, x, y + h - 4.0, w, 4.0, fill=color, r=0.7)
        texto(ax, x + w / 2, y + h - 2.0, nombre.upper(), size=8.0, color=WHITE,
              bold=True, ha="center")
        cw = (w - 3 - (cols - 1) * 1.2) / cols
        for i, tn in enumerate(tablas):
            r_, c_ = divmod(i, cols)
            bx = x + 1.5 + c_ * (cw + 1.2)
            by = y + h - 8.6 - r_ * 5.4
            caja(ax, bx, by, cw, 4.4, fill=WHITE, edge=color, lw=0.8, r=0.4)
            campos_tabla = len(esquema.TABLA_POR_NOMBRE[tn]["campos"])
            texto(ax, bx + cw / 2, by + 2.8, tn, size=6.9, color=color, bold=True, ha="center")
            texto(ax, bx + cw / 2, by + 1.2, f"{campos_tabla} campos", size=5.6, color=MUTED,
                  ha="center")

    resumen = [(str(n_tablas), "tablas"), (str(n_campos), "campos"),
               (str(n_fk), "claves foráneas"), (str(len(esquema.MODULOS)), "módulos funcionales")]
    for i, (n, d) in enumerate(resumen):
        x = 6 + i * 33
        texto(ax, x, 6.0, n, size=19, color=PRIMARY, bold=True, font=TITLE_FONT)
        texto(ax, x + (9.5 if len(n) == 3 else 6.5), 5.6, d, size=8.6, color=MUTED)

    texto(ax, 6, 1.6,
          "El detalle de campos, tipos y restricciones de cada tabla se muestra en las diagramas del Anexo A y en el diccionario de datos de la sección 2.4.",
          size=7.0, color=MUTED, italic=True)

    guardar(fig, ruta("10_er_global.png"))


# ================================================================== 11 · FODA
def fig_foda():
    fig, ax = lienzo(13, 7.2, 130, 72)
    titulo_figura(ax, 5, 65.5, "Matriz FODA",
                  "Diagnóstico interno y externo de Coral Shop")

    cuadrantes = [
        ("FORTALEZAS", "Origen interno  ·  ayuda", PRIMARY, 5, 34, [
            "Producto propio: la marca controla el diseño y el estampado de punta a punta",
            "Taller de estampado DTF y vinil en el mismo local, sin depender de terceros",
            "Comunidad activa de 24 mil seguidores en Instagram y TikTok",
            "Equipo joven que conoce el lenguaje y las tendencias de su público",
            "Capacidad de producir desde una unidad, sin pedido mínimo",
        ]),
        ("OPORTUNIDADES", "Origen externo  ·  ayuda", BLUE, 67.5, 34, [
            "Crecimiento sostenido del comercio electrónico de moda en el Perú",
            "Demanda de polos de promoción, facultad y eventos universitarios",
            "Billeteras digitales (Yape y Plin) masificadas entre el público joven",
            "Pocos competidores locales ofrecen personalización en línea con vista previa",
            "Couriers con cobertura nacional y tarifas accesibles",
        ]),
        ("DEBILIDADES", "Origen interno  ·  limita", ACCENT, 5, 5, [
            "No existe canal de venta digital propio: todo pasa por chat",
            "Inventario en hojas de cálculo, sin control por talla ni color",
            "Cotización del estampado manual y dependiente de una sola persona",
            "Sin indicadores de venta ni registro de pedidos perdidos",
            "Presupuesto limitado de tecnología y de personal técnico",
        ]),
        ("AMENAZAS", "Origen externo  ·  limita", GOLD, 67.5, 5, [
            "Marketplaces con logística y experiencia de compra superiores",
            "Importación de ropa a bajo costo que presiona el precio",
            "Estacionalidad fuerte: la demanda se concentra en pocos meses",
            "Alza del precio de insumos importados por tipo de cambio",
            "Facilidad de copia del diseño por parte de la competencia",
        ]),
    ]

    for tit, sub, color, x, y, items in cuadrantes:
        H = 25
        caja(ax, x, y, 57.5, H, fill=CARD, edge=color, lw=1.2, r=0.8)
        caja(ax, x, y + H - 5.0, 57.5, 5.0, fill=color, r=0.8)
        texto(ax, x + 2, y + H - 2.4, tit, size=9.2, color=WHITE, bold=True)
        texto(ax, x + 55.5, y + H - 2.4, sub, size=6.6, color=CREAM, ha="right")
        yy = y + H - 8.5
        for it in items:
            lineas = textwrap.wrap(it, 78)
            ax.plot([x + 2.4], [yy], marker="o", ms=1.8, color=color, zorder=5)
            for k, ln in enumerate(lineas):
                texto(ax, x + 4.0, yy - k * 2.1, ln, size=7.0, color=TEXT)
            yy -= len(lineas) * 2.1 + 1.5

    guardar(fig, ruta("11_foda.png"))


# ======================================================= 12 · FLUJO DE EVENTOS
def _bloque(ax, x, y, w, h, color, titulo, sub, size_t=8.6, size_s=7):
    caja(ax, x, y, w, h, fill=WHITE, edge=color, lw=1.4, r=0.6)
    texto(ax, x + w / 2, y + h * 0.66, titulo, size=size_t, color=color, ha="center", bold=True)
    texto(ax, x + w / 2, y + h * 0.30, sub, size=size_s, color=TEXT, ha="center", lh=1.3)


def fig_eventos():
    fig, ax = lienzo(10, 6.2, 100, 62)
    titulo_figura(ax, 3, 56.5, "Arquitectura dirigida por eventos",
                  "Flujo del evento OrderStatusChanged", size_k=8, size_t=14)

    # Contenido del evento
    caja(ax, 63, 51, 34, 9, fill=CARD, edge=GOLD, lw=1.2, r=0.6)
    texto(ax, 80, 57.6, "OrderStatusChanged", size=8.6, color=GOLD, ha="center", bold=True)
    texto(ax, 80, 53.6, "eventId · orderId · orderCode · customerId\nfrom · to · changedBy · comment · occurredAt",
          size=6.6, color=TEXT, ha="center", lh=1.3)

    # Publicadores (capa de servicio, dentro de su @Transactional)
    texto(ax, 3, 47.5, "PUBLICADORES · capa service, dentro de su transacción", size=7.4, color=PRIMARY, bold=True)
    publicadores = [(3, "OrderService", "crea el pedido\n→ PENDIENTE_PAGO"),
                    (35, "PaymentService", "pago aprobado\n→ PAGADO"),
                    (67, "OrderAdminService", "avanza o cancela\n→ siguiente estado")]
    for x, titulo, sub in publicadores:
        _bloque(ax, x, 36, 30, 9.5, PRIMARY, titulo, sub)
        ax.plot([x + 15, x + 15], [36, 30.4], color=PRIMARY, lw=1.6, zorder=3)
        texto(ax, x + 16, 33.2, "publishEvent", size=6.6, color=PRIMARY, italic=True)

    ax.plot([3, 97], [30, 30], color=ACCENT, lw=3.2, zorder=3)
    texto(ax, 31, 27.6, "BUS DE EVENTOS · ApplicationEventPublisher de Spring", size=7.6, color=ACCENT, bold=True)

    # Suscriptores
    suscriptores = [
        (8, BLUE, "AuditListener", "BEFORE_COMMIT · misma transacción\nsi falla, el cambio se deshace",
         "audit_log", "bitácora: quién, cuándo, de qué a qué"),
        (54, GREEN, "NotificationListener", "AFTER_COMMIT · transacción nueva\nsolo si el cambio se guardó",
         "notifications", "campana del header · GET /api/notifications/me"),
    ]
    for x, color, titulo, sub, tabla, uso in suscriptores:
        ax.plot([x + 19, x + 19], [30, 24.6], color=color, lw=1.6, zorder=3)
        _bloque(ax, x, 15, 38, 9.5, color, titulo, sub)
        flecha(ax, (x + 19, 15), (x + 19, 11.2), color=color, size=8)
        caja(ax, x + 6, 5.2, 26, 6, fill=CARD, edge=color, lw=1.1, r=0.5)
        texto(ax, x + 19, 9.1, tabla, size=7.8, color=color, ha="center", bold=True)
        texto(ax, x + 19, 6.7, uso, size=6.2, color=MUTED, ha="center")

    texto(ax, 3, 2.2, "@TransactionalEventListener: si la transacción se deshace, ningún suscriptor recibe el evento. "
          "event_id es único en ambas tablas, así que un evento repetido no duplica nada.",
          size=6.8, color=MUTED, italic=True)
    guardar(fig, ruta("12_flujo_eventos.png"))


if __name__ == "__main__":
    print("Generando figuras en", BASE)
    fig_ishikawa()
    fig_canvas()
    fig_arquitectura()
    fig_flujo()
    fig_casos_uso()
    fig_estados()
    fig_modulos()
    fig_er_1()
    fig_er_2()
    fig_er_global()
    fig_foda()
    fig_eventos()
    print("Listo.")
