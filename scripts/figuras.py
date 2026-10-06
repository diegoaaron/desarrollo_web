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

    titulo_figura(ax, 5, 72, "Figura 1 · Diagrama de causa-efecto",
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
    titulo_figura(ax, 5, 74, "Figura 2 · Business Model Canvas",
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
        "Pasarela de pagos (Culqi / Niubiz) y Yape-Plin",
        "Microinfluencers universitarios de Lima",
        "Proveedor de hosting y dominio",
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
        "Compra unitaria sin pedido mínimo, también para grupos y promociones",
        "Entrega en 72 horas en Lima con seguimiento del estado del pedido",
    ], color=ACCENT)

    bloque(xs[3], y_sup + alto_medio + 1.2, ancho_col, alto_medio, "Relación con clientes", [
        "Autoservicio 24/7 en la tienda web",
        "Cuenta con historial, favoritos y Mis diseños",
        "Aviso automático de cada cambio de estado",
        "Reseñas de compradores verificados",
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
        "Alquiler del local y del taller  ·  Hosting, dominio y pasarela de pagos",
        "Publicidad digital  ·  Mermas por estampados rechazados",
    ], color=PRIMARY)

    bloque(xs[2], y_base_inf, ancho_col * 3 + 2.4, alto_inf, "Fuentes de ingresos", [
        "Venta de prendas de catálogo  ·  Recargo por personalización (técnica, zona y tamaño)",
        "Pedidos por volumen para promociones y grupos  ·  Cobro del envío según modalidad",
        "Campañas con cupones de temporada que elevan el ticket promedio",
    ], color=ACCENT)

    guardar(fig, ruta("02_canvas.png"))


# ======================================================== 03 · ARQUITECTURA
def fig_arquitectura():
    fig, ax = lienzo(14, 9.4, 140, 94)
    titulo_figura(ax, 5, 88, "Figura 3 · Arquitectura de la solución",
                  "Cliente - Servidor en tres capas sobre un contenedor web Java")

    # ---------------------------------------------------------- capa cliente
    caja(ax, 5, 68, 96, 14.5, fill=CARD, edge=BLUE, lw=1.2, r=0.8)
    etiqueta(ax, 6.5, 78.6, 20, 3.2, "CAPA DE PRESENTACIÓN", fill=BLUE, size=7.8)
    texto(ax, 28.5, 80.2, "Navegador del cliente  ·  SPA React 19 + Vite  ·  desplegada en Netlify",
          size=9.5, color=TEXT, bold=True)
    chips = ["Componentes\ny páginas", "React Router\n(navegación)", "Context API\n(carrito y sesión)",
             "Personalizador\nde estampado", "Servicios fetch\n/api/v1"]
    for i, c in enumerate(chips):
        x = 7.5 + i * 18.4
        caja(ax, x, 69.3, 17.2, 7.6, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
        texto(ax, x + 8.6, 73.1, c, size=7.8, color=BLUE, bold=True, ha="center", lh=1.35)

    # ------------------------------------------------------------- transporte
    flecha(ax, (53, 67.6), (53, 62.4), color=PRIMARY, lw=2.0, size=16)
    flecha(ax, (48, 62.4), (48, 67.6), color=ACCENT, lw=2.0, size=16)
    texto(ax, 57, 66.3, "HTTP/HTTPS  ·  petición JSON  ·  cabecera Authorization: Bearer <JWT>",
          size=8.2, color=PRIMARY, bold=True)
    texto(ax, 57, 63.5, "Respuesta JSON  ·  códigos 200 / 201 / 400 / 401 / 403 / 404 / 409",
          size=8.2, color=MUTED)

    # ------------------------------------------------- contenedor de servidor
    caja(ax, 5, 19.5, 96, 43, fill="#FAF4F1", edge=PRIMARY, lw=1.4, r=0.9)
    etiqueta(ax, 6.5, 57.6, 34, 3.4, "APACHE TOMCAT 10  ·  WEB CONTAINER", fill=PRIMARY, size=7.8)
    texto(ax, 42.5, 59.3, "Aplicación coral_shop_backend.war  ·  Java 17 + Jakarta Servlet API",
          size=9, color=PRIMARY, bold=True)

    # filtros
    caja(ax, 7.5, 50.6, 91, 5.6, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
    texto(ax, 9.5, 53.4, "FILTROS (jakarta.servlet.Filter)", size=8, color=ACCENT, bold=True)
    for i, f in enumerate(["CorsFilter", "JwtAuthenticationFilter", "RoleAuthorizationFilter",
                           "RequestLoggingFilter", "EncodingFilter"]):
        etiqueta(ax, 40 + i * 11.8, 51.9, 11, 3.0, f, fill=ROSE, color=PRIMARY, size=6.9)

    capas = [
        ("CAPA CONTROLADOR", "Servlets  ·  paquete web.controller", PRIMARY,
         ["AuthServlet", "ProductServlet", "VariantServlet", "CartServlet",
          "CustomizationServlet", "OrderServlet", "AdminReportServlet"],
         "Recibe la petición, valida el formato de entrada, delega en el servicio y serializa la respuesta a JSON."),
        ("CAPA DE SERVICIO", "Reglas de negocio  ·  paquete service", BLUE,
         ["AuthService", "ProductService", "InventoryService", "CartService",
          "PricingService", "OrderService", "ReportService"],
         "Concentra las reglas: valida stock, calcula el precio del estampado, aplica cupones y controla la transacción."),
        ("CAPA DE ACCESO A DATOS", "DAO sobre JDBC  ·  paquete dao", GREEN,
         ["UserDao", "ProductDao", "VariantDao", "CartDao",
          "CustomizationDao", "OrderDao", "AuditDao"],
         "Único punto que conoce SQL. Usa PreparedStatement y devuelve JavaBeans del paquete model."),
    ]
    y = 42.3
    for tit, sub, color, comps, desc in capas:
        caja(ax, 7.5, y, 91, 7.4, fill=WHITE, edge=LINE, lw=0.8, r=0.6)
        caja(ax, 7.5, y, 1.1, 7.4, fill=color, r=0.4)
        texto(ax, 10.2, y + 5.5, tit, size=8, color=color, bold=True)
        texto(ax, 10.2, y + 3.4, sub, size=7.2, color=MUTED, italic=True)
        texto(ax, 10.2, y + 1.3, desc, size=6.9, color=TEXT)
        for i, c in enumerate(comps[:4]):
            etiqueta(ax, 57 + i * 10.6, y + 4.4, 10, 2.6, c, fill=color, size=6.3)
        for i, c in enumerate(comps[4:]):
            etiqueta(ax, 57 + i * 10.6, y + 1.2, 10, 2.6, c, fill=color, size=6.3)
        y -= 8.2

    # modelo transversal
    caja(ax, 7.5, 20.4, 91, 4.8, fill="#F2E7E2", edge=LINE, lw=0.8, r=0.6)
    texto(ax, 9.5, 22.8, "MODELO  ·  JavaBeans y DTO  ·  paquete model", size=8,
          color=PRIMARY, bold=True)
    texto(ax, 45, 22.8,
          "Atributos privados con getters y setters. Atraviesan las tres capas: el DAO los construye y el servlet los serializa.",
          size=6.7, color=TEXT)

    # ------------------------------------------------------------ persistencia
    caja(ax, 5, 5.5, 46, 12.5, fill=CARD, edge=GREEN, lw=1.2, r=0.8)
    etiqueta(ax, 6.5, 14.2, 17, 3.0, "PERSISTENCIA", fill=GREEN, size=7.6)
    texto(ax, 25, 15.7, "PostgreSQL 16", size=10.5, color=GREEN, bold=True, font=TITLE_FONT)
    texto(ax, 7, 11.2,
          "28 tablas relacionales  ·  claves foráneas con ON DELETE definido\n"
          "Índices B-tree en sku, slug, email y order_code  ·  CHECK de integridad\n"
          "Acceso por JDBC (java.sql) con pool de conexiones HikariCP (javax.sql.DataSource)",
          size=7.2, color=TEXT, lh=1.5)

    caja(ax, 55, 5.5, 46, 12.5, fill=CARD, edge=GOLD, lw=1.2, r=0.8)
    etiqueta(ax, 56.5, 14.2, 21, 3.0, "ALMACENAMIENTO DE ARCHIVOS", fill=GOLD, size=7.0)
    texto(ax, 79, 15.7, "Volumen /uploads", size=10.5, color=GOLD, bold=True, font=TITLE_FONT)
    texto(ax, 57, 11.2,
          "Imágenes del catálogo y artes subidos por el cliente\n"
          "Mockups generados para la vista previa del estampado\n"
          "Validación de tipo MIME y tamaño máximo antes de guardar",
          size=7.2, color=TEXT, lh=1.5)

    flecha(ax, (28, 20.2), (28, 18.2), color=GREEN, lw=1.8, size=14)
    flecha(ax, (78, 20.2), (78, 18.2), color=GOLD, lw=1.8, size=14)

    # ------------------------------------------------------- panel transversal
    caja(ax, 104, 4.5, 31, 78, fill=DARK, r=0.9)
    texto(ax, 106.5, 78.5, "ASPECTOS", size=8.5, color=ROSE, bold=True)
    texto(ax, 106.5, 74.8, "transversales", size=15, color=CREAM, bold=True, font=TITLE_FONT)

    items = [
        ("Seguridad", "BCrypt para contraseñas, JWT firmado con HS256, control de acceso por rol en filtro y PreparedStatement contra inyección SQL."),
        ("Validación", "Toda entrada se valida en el servidor aunque el formulario React ya la valide; el cliente nunca es de confianza."),
        ("Sesión", "HttpSessión y JSESSIONID sostienen el carrito del invitado; al iniciar sesión se fusiona con el carrito del usuario."),
        ("Transacciones", "El servicio abre la conexión, desactiva autocommit y hace commit o rollback: el pedido se guarda completo o no se guarda."),
        ("Trazabilidad", "audit_log, inventory_movement y order_status_history registran quién hizo qué y cuándo."),
        ("Despliegue", "Docker Compose levanta tomcat y postgres como servicios; el WAR se construye con Maven."),
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
    titulo_figura(ax, 5, 73.5, "Figura 4 · Flujo de una petición",
                  "Caso: el cliente confirma un pedido con una polera personalizada")

    actores = [
        ("React SPA", "Navegador", BLUE, 13),
        ("Filtros", "CORS + JWT", ACCENT, 33),
        ("OrderServlet", "Controlador", PRIMARY, 55),
        ("OrderService", "Negocio", BLUE, 79),
        ("DAO / JDBC", "Acceso a datos", GREEN, 103),
        ("PostgreSQL", "Base de datos", GOLD, 126),
    ]
    for nom, sub, color, x in actores:
        caja(ax, x - 10, 62, 20, 6.4, fill=color, r=0.7)
        texto(ax, x, 66.4, nom, size=8.8, color=WHITE, bold=True, ha="center")
        texto(ax, x, 63.7, sub, size=6.8, color=CREAM, ha="center")
        ax.plot([x, x], [7, 62], color=LINE, lw=1.0, ls=(0, (3, 3)), zorder=1)

    pasos = [
        (13, 33, "POST /api/v1/orders  ·  Bearer <JWT>", 57.5, True),
        (33, 55, "Token válido, rol CLIENTE  ·  request.setAttribute(\"userId\")", 53.5, True),
        (55, 79, "Deserializa el JSON a OrderRequestDto y valida el formato", 49.5, True),
        (79, 103, "beginTransaction()  ·  setAutoCommit(false)", 45.5, True),
        (103, 126, "SELECT ... FOR UPDATE sobre product_variant", 41.5, True),
        (126, 103, "ResultSet con el stock real de cada variante", 37.5, False),
        (103, 79, "Lista<ProductVariant>", 33.5, False),
        (79, 103, "INSERT orders, order_item, customization, payment, inventory_movement", 29.5, True),
        (103, 126, "PreparedStatement por lote  ·  executeBatch()", 25.5, True),
        (126, 79, "Confirmación  ·  commit()", 21.5, False),
        (79, 55, "OrderDto con el código CS-2026-000123", 17.5, False),
        (55, 13, "201 Created  ·  JSON del pedido  ·  Location: /api/v1/orders/123", 13.5, False),
    ]
    for x1, x2, txt, y, ida in pasos:
        color = PRIMARY if ida else GREEN
        flecha(ax, (x1, y), (x2, y), color=color, lw=1.5, size=11,
               ls="solid" if ida else (0, (4, 2)))
        cx = (x1 + x2) / 2
        texto(ax, cx, y + 1.9, txt, size=7.0, color=color if ida else MUTED,
              bold=ida, ha="center")

    # nota de negocio
    caja(ax, 5, 1.5, 130, 8.4, fill=CARD, edge=LINE, lw=0.8, r=0.7)
    texto(ax, 7, 7.6, "REGLA DE NEGOCIO QUE PROTEGE ESTE FLUJO", size=7.6, color=ACCENT, bold=True)
    texto(ax, 7, 4.3,
          "Si cualquier variante no tiene stock suficiente, el servicio lanza StockInsuficienteException, ejecuta rollback() y el servlet responde 409 Conflict con el detalle de la talla "
          "afectada. Nunca queda un pedido a medio grabar: o se escriben las cinco tablas o no se escribe ninguna.",
          size=7.4, color=TEXT, wrap=175, lh=1.5)

    guardar(fig, ruta("04_flujo_peticion.png"))


# ========================================================= 05 · CASOS DE USO
def fig_casos_uso():
    fig, ax = lienzo(14, 9.0, 140, 90)
    titulo_figura(ax, 5, 84, "Figura 5 · Diagrama de casos de uso",
                  "Actores del sistema y funcionalidades que puede ejecutar cada uno")

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
        ("Explorar catálogo, buscar y filtrar", BLUE),
        ("Ver detalle y elegir talla y color", BLUE),
        ("Personalizar el estampado", ACCENT),
        ("Gestionar carrito y favoritos", GREEN),
        ("Realizar el checkout y pagar", GREEN),
        ("Aplicar cupón de descuento", GREEN),
        ("Seguir el estado de su pedido", GREEN),
        ("Registrarse e iniciar sesión", PRIMARY),
        ("Calificar el producto comprado", GOLD),
    ]
    der = [
        ("Gestionar catálogo y variantes", BLUE),
        ("Controlar el inventario y el kardex", BLUE),
        ("Configurar opciones de estampado", ACCENT),
        ("Aprobar o rechazar el arte del cliente", ACCENT),
        ("Atender pedidos y cambiar su estado", GREEN),
        ("Administrar cupones y envíos", GREEN),
        ("Gestionar usuarios y roles", PRIMARY),
        ("Consultar reportes e indicadores", GOLD),
        ("Revisar la bitácora de auditoría", GOLD),
    ]

    y0, dy = 70, 7.6
    pos_izq, pos_der = [], []
    for i, (t, c) in enumerate(izq):
        pos_izq.append(uc(50, y0 - i * dy, t, c))
    for i, (t, c) in enumerate(der):
        pos_der.append(uc(90, y0 - i * dy, t, c))

    actor(14, 52, "Cliente", "Joven que compra y personaliza su prenda", PRIMARY)
    actor(14, 22, "Invitado", "Navega y arma su carrito sin cuenta", MUTED)
    actor(126, 62, "Administrador", "Gestiona toda la operación", PRIMARY)
    actor(126, 38, "Vendedor", "Atiende y despacha pedidos", GREEN)
    actor(126, 14, "Diseñador", "Revisa y aprueba los artes", ACCENT)

    def unir(px, py, casos, lado):
        for (cx, cy) in casos:
            xo = cx - 12 if lado == "izq" else cx + 12
            ax.plot([px, xo], [py, cy], color=LINE, lw=0.7, zorder=2)

    unir(16, 52, pos_izq, "izq")
    unir(16, 22, pos_izq[:4], "izq")
    unir(124, 62, pos_der, "der")
    unir(124, 38, [pos_der[1], pos_der[4], pos_der[5]], "der")
    unir(124, 14, [pos_der[2], pos_der[3]], "der")

    texto(ax, 5, 2.2,
          "El Invitado solo alcanza los cuatro primeros casos de uso; al intentar el checkout el sistema lo obliga a registrarse y fusiona su carrito de sesión con el de su cuenta.",
          size=7.4, color=MUTED, italic=True)

    guardar(fig, ruta("05_casos_uso.png"))


# ======================================================= 06 · ESTADOS PEDIDO
def fig_estados():
    fig, ax = lienzo(14, 7.2, 140, 72)
    titulo_figura(ax, 5, 65, "Figura 6 · Máquina de estados del pedido",
                  "Transiciones válidas que controla OrderService")

    estados = [
        ("PENDIENTE", "Pedido creado,\npago no acreditado", ACCENT),
        ("PAGADO", "Pago aprobado,\nstock descontado", BLUE),
        ("EN_PRODUCCION", "Arte aprobado,\nestampado en curso", PRIMARY),
        ("ENVIADO", "Entregado al courier\ncon número de guía", GREEN),
        ("ENTREGADO", "Recibido por el cliente.\nHabilita la reseña", GOLD),
    ]
    x0, w, paso, yb, hb = 7, 22, 26, 44, 13
    for i, (nom, desc, color) in enumerate(estados):
        x = x0 + i * paso
        caja(ax, x, yb, w, hb, fill=color, r=0.8)
        texto(ax, x + w / 2, yb + 9.0, nom, size=9.2, color=WHITE, bold=True, ha="center")
        texto(ax, x + w / 2, yb + 4.0, desc, size=7.2, color=CREAM, ha="center", lh=1.45)

    metodos = ["registrarPago()", "aprobarArte()", "despachar()", "confirmarEntrega()"]
    for i, m in enumerate(metodos):
        xg = x0 + w + i * paso
        flecha(ax, (xg + 0.3, yb + hb / 2), (xg + paso - w - 0.3, yb + hb / 2),
               color=PRIMARY, lw=1.8, size=13)
        texto(ax, xg + (paso - w) / 2, yb + hb + 2.4, m, size=7.0, color=PRIMARY,
              bold=True, ha="center")

    # estado terminal
    caja(ax, 33, 17, 22, 11, fill="#8C3B3B", r=0.8)
    texto(ax, 44, 24.4, "CANCELADO", size=9.2, color=WHITE, bold=True, ha="center")
    texto(ax, 44, 20.4, "Estado terminal.\nLibera el stock reservado", size=7.2,
          color=CREAM, ha="center", lh=1.45)

    for xo, rad in ((18, 0.22), (44, 0.0), (70, -0.22)):
        flecha(ax, (xo, yb - 0.4), (44 if xo == 44 else (40 if xo < 44 else 48), 28.4),
               color="#8C3B3B", lw=1.3, size=11, ls=(0, (4, 2)),
               conn=f"arc3,rad={rad}")
    texto(ax, 60, 22.5,
          "cancelar()  ·  admitido solo antes de ENVIADO  ·  ejecuta liberarStock()",
          size=7.4, color="#8C3B3B", bold=True)

    caja(ax, 5, 2, 130, 9, fill=CARD, edge=LINE, lw=0.8, r=0.7)
    texto(ax, 7, 8.2, "IMPLEMENTACIÓN", size=7.6, color=ACCENT, bold=True)
    texto(ax, 7, 4.8,
          "Enum OrderStatus + Map<OrderStatus, Set<OrderStatus>> con las transiciones permitidas. Cualquier salto no declarado lanza TransicionInvalidaException (HTTP 409). "
          "Cada cambio efectivo inserta una fila en order_status_history y genera una notificación al cliente.",
          size=7.3, color=TEXT, wrap=170, lh=1.5)

    guardar(fig, ruta("06_estados_pedido.png"))


# ========================================================= 07 · MODULOS
def fig_modulos():
    fig, ax = lienzo(14, 8.6, 140, 86)
    titulo_figura(ax, 5, 80, "Figura 7 · Mapa funcional",
                  "Los 20 módulos que componen la tienda virtual")

    grupos = [
        ("TIENDA PÚBLICA", BLUE, [
            ("M01", "Catálogo y navegación", "Home, categorías, búsqueda, filtros, orden y paginación"),
            ("M02", "Detalle de producto", "Galería, selección de talla y color, stock real, guía de tallas"),
            ("M03", "Personalizador", "Zona, técnica, tamaño, imagen o texto, vista previa y recargo"),
            ("M04", "Carrito", "Alta, edición, recálculo y fusión del carrito de invitado"),
            ("M05", "Favoritos", "Lista de deseos por usuario"),
        ]),
        ("COMPRA", GREEN, [
            ("M06", "Checkout", "Dirección, modalidad de entrega, pago simulado y confirmación"),
            ("M07", "Cupones", "Validación de vigencia, monto mínimo y tope de canjes"),
            ("M08", "Seguimiento", "Estado del pedido, historial y notificaciones"),
            ("M09", "Reseñas", "Calificación de compradores verificados con moderación"),
            ("M10", "Cuenta", "Registro, login, perfil, direcciones y Mis diseños"),
        ]),
        ("BACKOFFICE", PRIMARY, [
            ("M11", "Tablero", "Indicadores de ventas, pedidos por estado y stock crítico"),
            ("M12", "Catálogo admin", "CRUD de categorías, productos, imágenes y variantes"),
            ("M13", "Maestros", "Tallas, colores, técnicas, zonas y tamaños de estampado"),
            ("M14", "Inventario", "Ajustes con motivo, alertas de mínimo y kardex"),
            ("M15", "Pedidos", "Bandeja, cambio de estado y aprobación del arte"),
        ]),
        ("GOBIERNO", GOLD, [
            ("M16", "Usuarios y roles", "Alta, baja y asignación de permisos"),
            ("M17", "Cupones admin", "Creación y control de campañas"),
            ("M18", "Envíos", "Modalidades, costos y cobertura"),
            ("M19", "Reportes", "Ventas por periodo, top de productos y exportación"),
            ("M20", "Auditoría", "Bitácora de acciones y trazabilidad"),
        ]),
    ]

    x0 = 5
    ancho = 32.4
    for gi, (titulo, color, mods) in enumerate(grupos):
        x = x0 + gi * (ancho + 1.5)
        caja(ax, x, 5, ancho, 68, fill="#FCFAF8", edge=LINE, lw=0.8, r=0.7)
        caja(ax, x, 68.4, ancho, 4.6, fill=color, r=0.7)
        texto(ax, x + ancho / 2, 70.7, titulo, size=8.6, color=WHITE, bold=True, ha="center")
        y = 56.0
        for cod, nom, desc in mods:
            caja(ax, x + 1.4, y, ancho - 2.8, 11, fill=WHITE, edge=LINE, lw=0.7, r=0.6)
            etiqueta(ax, x + 2.6, y + 7.2, 6.2, 2.8, cod, fill=color, size=6.8)
            texto(ax, x + 10, y + 8.6, nom, size=8.2, color=color, bold=True)
            texto(ax, x + 2.6, y + 3.4, desc, size=6.7, color=TEXT, wrap=48, lh=1.4)
            y -= 12.2

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
        if llave == "PK":
            marca, mc, bold = "PK", "#B8860B", True
        elif llave.startswith("FK"):
            marca, mc, bold = "FK", color, False
        elif llave.startswith("UQ"):
            marca, mc, bold = "UQ", MUTED, False
        else:
            marca, mc, bold = "", MUTED, False
        if marca:
            texto(ax, x + 1.2, yy, marca, size=5.2, color=mc, bold=True)
        texto(ax, x + 4.6, yy, nombre, size=size_f, color=TEXT, bold=bold)
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
        "Figura 8 · Diseño de base de datos",
        [
            ["role", "app_user", "password_reset_token"],
            ["address", "category", "size"],
            ["color", "product", "product_image"],
            ["product_variant", "inventory_movement"],
        ],
        9.0, 4.8, 165, 88,
        nota="El stock no vive en product sino en product_variant: cada combinación de producto, talla y color tiene su propio SKU y su propio stock.")


def fig_er_2():
    _er("09_er_personalizacion_compra.png",
        "Modelo entidad-relación (2 de 2): personalización, carrito, pedidos y soporte",
        "Figura 9 · Diseño de base de datos",
        [
            ["print_technique", "print_zone", "print_size", "design"],
            ["customization", "cart", "cart_item"],
            ["orders", "coupon", "shipping_method"],
            ["order_item", "payment", "order_status_history"],
            ["review", "wishlist_item", "notification", "audit_log"],
        ],
        9.0, 5.08, 195, 110,
        nota="order_item copia nombre, SKU, talla, color y precio al momento de comprar: el pedido queda inmutable aunque el catálogo cambie después.")


def fig_er_global():
    fig, ax = lienzo(14, 7.4, 140, 74)
    titulo_figura(ax, 5, 68, "Figura 10 · Mapa global del modelo de datos",
                  "28 tablas agrupadas en cinco módulos funcionales")

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
            n_campos = len(esquema.TABLA_POR_NOMBRE[tn]["campos"])
            texto(ax, bx + cw / 2, by + 2.8, tn, size=6.9, color=color, bold=True, ha="center")
            texto(ax, bx + cw / 2, by + 1.2, f"{n_campos} campos", size=5.6, color=MUTED,
                  ha="center")

    resumen = [("28", "tablas"), ("222", "campos"),
               ("39", "claves foráneas"), ("5", "módulos funcionales")]
    for i, (n, d) in enumerate(resumen):
        x = 6 + i * 33
        texto(ax, x, 6.0, n, size=19, color=PRIMARY, bold=True, font=TITLE_FONT)
        texto(ax, x + (9.5 if len(n) == 3 else 6.5), 5.6, d, size=8.6, color=MUTED)

    texto(ax, 6, 1.6,
          "El detalle de campos, tipos y restricciones de cada tabla se muestra en las figuras 8 y 9 y en el diccionario de datos de la sección 2.4.",
          size=7.0, color=MUTED, italic=True)

    guardar(fig, ruta("10_er_global.png"))


# ================================================================== 11 · FODA
def fig_foda():
    fig, ax = lienzo(13, 7.2, 130, 72)
    titulo_figura(ax, 5, 65.5, "Figura 11 · Matriz FODA",
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
    print("Listo.")
