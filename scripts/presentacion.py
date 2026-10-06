# -*- coding: utf-8 -*-
"""Genera entregables/Presentacion_Proyecto_Final_Coral_Shop.pptx"""

import os

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

from pptx_util import (
    nueva_presentacion, lamina, caja, texto, cabecera, chip, tarjeta, vinetas,
    figura, pie, numero,
    DARK, PRIMARY, ACCENT, ROSE, CREAM, MUTED_LIGHT, CARD, BLUE, GREEN, GOLD,
    TEXT, MUTED, LINE, WHITE, TITULO, CUERPO, ANCHO, ALTO,
)

SALIDA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "clase_entregables", "Presentacion_Proyecto_Final_Coral_Shop.pptx")

C = PP_ALIGN.CENTER
M = MSO_ANCHOR.MIDDLE


# ------------------------------------------------------------------ 1 portada
def portada(prs):
    s = lamina(prs, DARK)
    caja(s, 10.2, -1.6, 4.8, 4.8, color=PRIMARY, forma=MSO_SHAPE.OVAL)
    caja(s, 11.6, 4.9, 3.4, 3.4, color=ACCENT, forma=MSO_SHAPE.OVAL)

    texto(s, 0.8, 0.75, 9.5, 0.3,
          "UNIVERSIDAD TECNOLÓGICA DEL PERÚ  ·  INGENIERÍA DE SOFTWARE",
          size=11, color=ACCENT, bold=True, spc=200)
    texto(s, 0.8, 1.22, 9.2, 1.1, "Coral Shop", size=46, color=CREAM, bold=True,
          font=TITULO)
    texto(s, 0.8, 2.42, 9.4, 0.9,
          "Plataforma de comercio electrónico para\nla venta de ropa juvenil personalizable",
          size=21, color=ROSE, font=TITULO, interlineado=1.2)
    texto(s, 0.8, 3.62, 9.4, 0.4,
          "Proyecto Final  ·  Diagnóstico, diseño de la solución y plan de implementación",
          size=14, color=MUTED_LIGHT)

    caja(s, 0.8, 4.35, 11.1, 2.0, color=PRIMARY)
    datos = [("CURSO", "Desarrollo Web Integrado", 1.15, 3.2),
             ("DOCENTE", "Ronald Fernando Medina Cabrera", 4.75, 3.6),
             ("AÑO", "2026", 8.7, 2.0)]
    for etiqueta, valor, x, w in datos:
        texto(s, x, 4.62, w, 0.25, etiqueta, size=9.5, color=ROSE, bold=True, spc=100)
        texto(s, x, 4.90, w, 0.32, valor, size=13, color=CREAM)
    texto(s, 1.15, 5.44, 3.0, 0.25, "GRUPO 1", size=9.5, color=ROSE, bold=True, spc=100)
    texto(s, 1.15, 5.72, 10.4, 0.6,
          "Choquehuanca Marrufo, Liam Lennon  ·  Damián Valdivia, Diego Aarón  ·  "
          "Loayza Gerónimo, Juan Franco  ·  Villanueva Montalvo, Apolo Chris  ·  "
          "Campos Sulca, Jian Pier",
          size=12.5, color=CREAM, interlineado=1.25)


# ------------------------------------------------------------------- 2 agenda
def agenda(prs):
    s = lamina(prs)
    cabecera(s, "Agenda", "Lo que vamos a recorrer")
    bloques = [
        ("1", "Diagnóstico del negocio", "Empresa, Canvas, PESTEL, FODA e Ishikawa", PRIMARY),
        ("2", "Problemática y objetivos", "La causa raíz y las metas medibles", ACCENT),
        ("3", "Características de la tienda", "Los 20 módulos y 49 requerimientos", BLUE),
        ("4", "Arquitectura", "Cliente-servidor en tres capas sobre Tomcat", PRIMARY),
        ("5", "Modelo de datos", "28 tablas, relaciones y campos", GREEN),
        ("6", "Implementación", "Paquetes, clases, algoritmos y cronograma", GOLD),
    ]
    for i, (n, t, d, color) in enumerate(bloques):
        fila, col = divmod(i, 3)
        x = 0.7 + col * 4.05
        y = 1.95 + fila * 2.35
        caja(s, x, y, 3.75, 1.95, color=CARD, borde=LINE)
        chip(s, x + 0.28, y + 0.26, 0.42, 0.42, n, color=color, size=13)
        texto(s, x + 0.28, y + 0.86, 3.2, 0.34, t, size=15, color=color, bold=True,
              font=TITULO)
        texto(s, x + 0.28, y + 1.28, 3.2, 0.5, d, size=10.5, color=MUTED,
              interlineado=1.3)
    pie(s, "Exposición del Proyecto Final  ·  Semana 18")


# ------------------------------------------------------- 3 empresa
def empresa(prs):
    s = lamina(prs)
    cabecera(s, "1 · El negocio", "Coral Shop S.A.C.")

    caja(s, 0.7, 1.62, 7.3, 2.35, color=CARD, borde=LINE)
    texto(s, 1.0, 1.86, 6.7, 0.28, "MISIÓN", size=9.5, color=ACCENT, bold=True, spc=150)
    texto(s, 1.0, 2.16, 6.7, 0.8,
          "Vestir la identidad de los jóvenes peruanos con ropa urbana que pueden "
          "personalizar a su gusto, con precios accesibles y producción local responsable.",
          size=11, color=TEXT, interlineado=1.35)
    texto(s, 1.0, 3.02, 6.7, 0.28, "VISIÓN", size=9.5, color=ACCENT, bold=True, spc=150)
    texto(s, 1.0, 3.32, 6.7, 0.55,
          "Ser en 2030 la primera marca peruana de ropa juvenil personalizable en línea: "
          "diseñar tu prenda en minutos y recibirla en 72 horas.",
          size=11, color=TEXT, interlineado=1.35)

    caja(s, 0.7, 4.15, 7.3, 2.5, color=CARD, borde=LINE)
    texto(s, 1.0, 4.38, 6.7, 0.28, "QUÉ VENDE", size=9.5, color=ACCENT, bold=True, spc=150)
    vinetas(s, 1.0, 4.70, 6.7, [
        ("Catálogo propio: ", "polos, poleras con capucha, gorras y tote bags."),
        ("Estampado personalizado: ", "el cliente elige zona, técnica y tamaño, "
         "y sube su propia imagen o texto."),
        ("El 45 % de las ventas ", "ya proviene de la línea personalizada, que es "
         "también la que más trabajo manual exige."),
        ("Pedidos por volumen: ", "polos de promoción, de facultad, de equipos "
         "deportivos y de colectivos, desde una unidad y sin mínimos."),
        ("Hoy todo pasa por chat: ", "Instagram y WhatsApp para vender, y hojas de "
         "cálculo locales para el inventario."),
    ], size=10.5, interlineado=1.3)

    caja(s, 8.35, 1.62, 4.25, 5.03, color=PRIMARY)
    texto(s, 8.7, 1.9, 3.6, 0.28, "INDUSTRIA Y TAMAÑO", size=10, color=ROSE,
          bold=True, spc=150)
    filas = [
        ("Sector", "Comercio al por menor de\nprendas de vestir (CIIU 4771)"),
        ("Tamaño", "Pequeña empresa"),
        ("Colaboradores", "12"),
        ("Ventas anuales", "S/ 1 800 000"),
        ("Pedidos al mes", "550 a 900 según temporada"),
        ("Ticket promedio", "S/ 78  ·  S/ 112 si es personalizado"),
    ]
    y = 2.42
    for k, v in filas:
        texto(s, 8.7, y, 3.6, 0.22, k.upper(), size=8.5, color=ROSE, bold=True, spc=80)
        alto = 0.46 if "\n" in v else 0.24
        texto(s, 8.7, y + 0.24, 3.6, alto, v, size=11, color=CREAM, interlineado=1.2)
        y += 0.30 + alto + 0.10


# ---------------------------------------------------------------- 4 canvas
def canvas(prs):
    s = lamina(prs)
    cabecera(s, "1 · Modelo de negocio", "Lienzo Canvas")
    figura(s, "02_canvas.png", y=1.55, ancho_max=12.0, alto_max=5.25)
    pie(s, "La propuesta de valor completa depende de que el cliente pueda diseñar y ver "
           "su prenda antes de comprar: por eso hace falta una plataforma propia.")


# ---------------------------------------------------------------- 5 pestel
def pestel(prs):
    s = lamina(prs)
    cabecera(s, "1 · Entorno", "Análisis PESTEL articulado al proyecto")
    items = [
        ("Político", "Fiscalización de INDECOPI sobre información al consumidor",
         "Obliga a publicar políticas y habilitar reclamos", PRIMARY),
        ("Económico", "Tipo de cambio volátil encarece los insumos importados",
         "Los costos de estampado son configurables en base de datos", BLUE),
        ("Social", "El joven valora la autoexpresión y confía en las reseñas",
         "Origina el personalizador (M03) y las reseñas verificadas (M09)", ACCENT),
        ("Tecnológico", "Estampado DTF accesible para tiradas cortas y Java EE maduro",
         "Hace viable producir desde una unidad; sustenta Tomcat y Docker", GREEN),
        ("Ecológico", "Presión por reducir el desperdicio textil",
         "Producir bajo demanda evita el sobrestock", GOLD),
        ("Legal", "Ley 29733 de Protección de Datos Personales",
         "Exige BCrypt, consentimiento y bitácora de auditoría", PRIMARY),
    ]
    for i, (factor, hallazgo, implicancia, color) in enumerate(items):
        fila, col = divmod(i, 2)
        x = 0.7 + col * 6.15
        y = 1.68 + fila * 1.72
        caja(s, x, y, 5.85, 1.5, color=CARD, borde=LINE)
        caja(s, x, y, 0.07, 1.5, color=color, radio=0.02, forma=MSO_SHAPE.RECTANGLE)
        texto(s, x + 0.26, y + 0.2, 5.3, 0.28, factor.upper(), size=10, color=color,
              bold=True, spc=100)
        texto(s, x + 0.26, y + 0.52, 5.3, 0.42, hallazgo, size=10.5, color=TEXT,
              interlineado=1.25)
        texto(s, x + 0.26, y + 1.03, 5.3, 0.36, "→  " + implicancia, size=9.5,
              color=color, interlineado=1.2)


# ------------------------------------------------------------------ 6 foda
def foda(prs):
    s = lamina(prs)
    cabecera(s, "1 · Diagnóstico interno y externo", "Matriz FODA y estrategias cruzadas")
    cuadrantes = [
        ("FORTALEZAS", PRIMARY, 0.7, 1.62, [
            "Taller propio de estampado DTF y vinil",
            "Comunidad de 24 mil seguidores",
            "Produce desde una unidad, sin mínimos",
            "Equipo joven que conoce a su público",
        ]),
        ("OPORTUNIDADES", BLUE, 6.85, 1.62, [
            "Crece el comercio electrónico de moda",
            "Demanda de polos de promoción y facultad",
            "Nadie local ofrece personalización en línea",
            "Yape y Plin masificados entre los jóvenes",
        ]),
        ("DEBILIDADES", ACCENT, 0.7, 3.55, [
            "No existe canal de venta digital propio",
            "Inventario en hojas de cálculo",
            "Cotización del estampado manual",
            "Sin indicadores ni registro de ventas perdidas",
        ]),
        ("AMENAZAS", GOLD, 6.85, 3.55, [
            "Marketplaces con mejor logística",
            "Importación de ropa a bajo costo",
            "Estacionalidad muy marcada",
            "El tipo de cambio encarece los insumos",
        ]),
    ]
    for titulo, color, x, y, items in cuadrantes:
        caja(s, x, y, 5.78, 1.78, color=CARD, borde=LINE)
        chip(s, x, y, 5.78, 0.36, titulo, color=color, size=10)
        vinetas(s, x + 0.24, y + 0.52, 5.3, items, size=10.5, interlineado=1.25,
                bullet_color=color, sep=0.04)

    caja(s, 0.7, 5.55, 11.93, 1.12, color=PRIMARY)
    texto(s, 1.0, 5.75, 11.3, 0.24, "LA LECTURA CRUZADA", size=9.5, color=ROSE,
          bold=True, spc=150)
    texto(s, 1.0, 6.03, 11.3, 0.55,
          "D1 (no hay canal digital propio) condiciona a todas las demás: sin plataforma no se puede "
          "aprovechar la comunidad, ni automatizar la cotización, ni medir nada. El proyecto ataca esa causa raíz.",
          size=11.5, color=CREAM, interlineado=1.3)


# --------------------------------------------------------------- 7 ishikawa
def ishikawa(prs):
    s = lamina(prs)
    cabecera(s, "2 · La causa raíz", "Diagrama de Ishikawa")
    figura(s, "01_ishikawa.png", y=1.55, ancho_max=12.0, alto_max=5.3)
    pie(s, "Tecnología, método y medición concentran las causas controlables, y las tres "
           "apuntan al mismo vacío: no existe un sistema que sostenga la operación.")


# ------------------------------------------------------------ 8 problematica
def problematica(prs):
    s = lamina(prs)
    cabecera(s, "2 · Problemática central", "Qué le está costando al negocio")

    caja(s, 0.7, 1.6, 11.93, 1.28, color=PRIMARY)
    texto(s, 1.0, 1.82, 11.3, 0.9,
          "Coral Shop no cuenta con un canal de venta digital propio ni con un sistema que integre "
          "catálogo, inventario por talla y color y pedidos personalizados. Todo pasa por chats de "
          "Instagram y WhatsApp y por hojas de cálculo locales.",
          size=13, color=CREAM, interlineado=1.32, font=TITULO)

    cifras = [
        ("12 %", "de los pedidos se cancela\npor sobreventa de tallas", ACCENT),
        ("6 h", "en promedio para cotizar\nun estampado por chat", BLUE),
        ("3 de 10", "consultas de personalización\nse enfrían antes de responder", GREEN),
        ("0", "indicadores de venta,\nconversión o rotación", GOLD),
    ]
    for i, (dato, desc, color) in enumerate(cifras):
        x = 0.7 + i * 3.06
        caja(s, x, 3.1, 2.83, 1.7, color=CARD, borde=LINE)
        texto(s, x, 3.28, 2.83, 0.7, dato, size=32, color=color, bold=True,
              font=TITULO, align=C)
        texto(s, x + 0.2, 4.06, 2.43, 0.6, desc, size=10, color=MUTED, align=C,
              interlineado=1.25)

    caja(s, 0.7, 5.05, 11.93, 1.62, color=CARD, borde=LINE)
    texto(s, 1.0, 5.24, 11.3, 0.24, "CÓMO SE MANIFIESTA", size=9.5, color=ACCENT,
          bold=True, spc=150)
    vinetas(s, 1.0, 5.54, 11.3, [
        ("Pedidos por chat sin formato: ", "errores de tipeo en talla, color y dirección, y reprocesos en el taller."),
        ("El catálogo publicado no coincide con la existencia real: ", "cada persona lleva su propia hoja de cálculo."),
        ("Atención de 9 a 19 horas: ", "se pierde la venta de la noche y del fin de semana, que es cuando compra el público joven."),
    ], size=10.5, interlineado=1.25, sep=0.03)


# ------------------------------------------------------------- 9 objetivos
def objetivos(prs):
    s = lamina(prs)
    cabecera(s, "2 · Hacia dónde vamos", "Objetivo general y objetivos específicos")

    caja(s, 0.7, 1.6, 11.93, 1.05, color=PRIMARY)
    texto(s, 1.0, 1.72, 2.2, 0.24, "OBJETIVO GENERAL", size=9.5, color=ROSE,
          bold=True, spc=150)
    texto(s, 1.0, 1.98, 11.3, 0.6,
          "Diseñar e implementar una plataforma web que permita al cliente comprar y personalizar "
          "prendas en línea, y a la empresa gestionar catálogo, inventario por variante y el ciclo "
          "completo del pedido.",
          size=12, color=CREAM, interlineado=1.28)

    oes = [
        ("OE-1", "Tienda virtual operativa", "80 % de pedidos por la web al 3.er mes", PRIMARY),
        ("OE-2", "Personalizador automático", "De 6 horas a menos de 1 minuto", ACCENT),
        ("OE-3", "Inventario por variante", "Cancelaciones por stock: de 12 % a < 2 %", BLUE),
        ("OE-4", "Tablero e informes", "8 indicadores actualizados al día", GREEN),
        ("OE-5", "Seguridad y trazabilidad", "100 % de acciones en bitácora", GOLD),
        ("OE-6", "Arquitectura del curso con TDD", "70 % de cobertura en la capa de servicio", PRIMARY),
    ]
    for i, (cod, nombre, meta, color) in enumerate(oes):
        fila, col = divmod(i, 3)
        x = 0.7 + col * 4.05
        y = 2.95 + fila * 1.95
        caja(s, x, y, 3.75, 1.62, color=CARD, borde=LINE)
        chip(s, x + 0.24, y + 0.24, 0.75, 0.26, cod, color=color, size=9)
        texto(s, x + 0.24, y + 0.62, 3.28, 0.4, nombre, size=13, color=color,
              bold=True, font=TITULO, interlineado=1.1)
        texto(s, x + 0.24, y + 1.08, 3.28, 0.42, "Meta:  " + meta, size=9.5,
              color=MUTED, interlineado=1.22)


# --------------------------------------------------------------- 10 solucion
def solucion(prs):
    s = lamina(prs)
    cabecera(s, "3 · La propuesta", "Qué vamos a construir")

    tarjeta(s, 0.7, 1.62, 5.95, 2.15,
            "coral_shop",
            "Aplicación de página única en React 19 + Vite. Catálogo, ficha de producto, "
            "personalizador de estampado, carrito, checkout y panel administrativo.",
            color=BLUE, etiqueta="FRONTEND", size_t=17, size_c=11)
    tarjeta(s, 6.68, 1.62, 5.95, 2.15,
            "coral_shop_backend",
            "Aplicación Java sobre Apache Tomcat. API REST en tres capas: Servlets como "
            "controlador, servicios con las reglas y DAO sobre JDBC. PostgreSQL de 28 tablas.",
            color=PRIMARY, etiqueta="BACKEND", size_t=17, size_c=11)

    caja(s, 0.7, 3.95, 11.93, 2.72, color=PRIMARY)
    texto(s, 1.0, 4.18, 11.3, 0.28, "LAS DOS DECISIONES QUE LA HACEN DISTINTA",
          size=10, color=ROSE, bold=True, spc=150)

    caja(s, 1.0, 4.58, 5.5, 1.9, color=DARK)
    texto(s, 1.28, 4.8, 4.95, 0.34, "El stock vive en la variante", size=15,
          color=CREAM, bold=True, font=TITULO)
    texto(s, 1.28, 5.22, 4.95, 1.1,
          "Un polo negro talla M y uno negro talla L son existencias independientes, cada una "
          "con su SKU y su stock. Es lo que corta de raíz el 12 % de cancelaciones por sobreventa.",
          size=10.5, color=MUTED_LIGHT, interlineado=1.32)

    caja(s, 6.83, 4.58, 5.5, 1.9, color=DARK)
    texto(s, 7.11, 4.8, 4.95, 0.34, "El personalizador en línea", size=15,
          color=CREAM, bold=True, font=TITULO)
    texto(s, 7.11, 5.22, 4.95, 1.1,
          "El cliente compone su arte, lo ve sobre la prenda y conoce el precio final sin esperar "
          "a nadie. Ese diseño viaja al taller convertido en una orden de producción trazable.",
          size=10.5, color=MUTED_LIGHT, interlineado=1.32)


# ----------------------------------------------------------------- 11 alcance
def alcance(prs):
    s = lamina(prs)
    cabecera(s, "3 · Alcance", "Qué entra y qué no en esta solución")

    caja(s, 0.7, 1.62, 6.1, 5.05, color=CARD, borde=LINE)
    chip(s, 0.7, 1.62, 6.1, 0.4, "INCLUIDO", color=GREEN, size=11)
    vinetas(s, 0.98, 2.22, 5.6, [
        "Tienda pública con catálogo, búsqueda, filtros y stock real por variante",
        "Personalizador con vista previa, carga de arte y recargo automático",
        "Carrito de invitado y de usuario, favoritos y cupones",
        "Checkout con direcciones, modalidades de entrega y confirmación",
        "Cuenta: registro, JWT, perfil, historial y Mis diseños",
        "Backoffice: tablero, CRUD de catálogo, inventario con kardex y pedidos",
        "Aprobación del arte y máquina de estados del pedido",
        "Usuarios y roles, cupones, envíos, reportes y auditoría",
    ], size=10.5, interlineado=1.28, bullet_color=GREEN, sep=0.05)

    caja(s, 7.0, 1.62, 5.63, 5.05, color=CARD, borde=LINE)
    chip(s, 7.0, 1.62, 5.63, 0.4, "FUERA DE ESTA VERSIÓN", color=ACCENT, size=11)
    vinetas(s, 7.28, 2.22, 5.1, [
        "Pasarela de pagos real (el pago se simula y se registra)",
        "Facturación electrónica ante SUNAT",
        "Envío automático de correos (los avisos van a la bandeja del sistema)",
        "Rastreo satelital del paquete (sí se registra el número de guía)",
        "Inicio de sesión con redes sociales",
        "Módulo contable y de planillas",
        "Editor gráfico avanzado con capas y filtros",
        "Aplicación móvil nativa (la web es responsiva)",
    ], size=10.5, interlineado=1.28, bullet_color=ACCENT, sep=0.05)


# ---------------------------------------------------------------- 12 modulos
def modulos(prs):
    s = lamina(prs)
    cabecera(s, "3 · Características de la tienda", "Los 20 módulos de la plataforma")
    figura(s, "07_modulos.png", y=1.55, ancho_max=12.0, alto_max=5.3)
    pie(s, "Cada módulo se descompone en requerimientos funcionales verificables: 49 en total, "
           "más 15 requerimientos no funcionales y 14 reglas de negocio.")


# --------------------------------------------------- 13 funcionalidades cliente
def funcionalidades_cliente(prs):
    s = lamina(prs)
    cabecera(s, "3 · Funcionalidades", "Lo que puede hacer el cliente")
    bloques = [
        ("M01-M02", "Explorar y elegir", BLUE, [
            "Catálogo con búsqueda, filtros por categoría, talla, color y precio",
            "Orden por relevancia, precio, novedad o valoración",
            "Ficha con galería, guía de tallas y stock real de cada variante",
            "Las combinaciones agotadas se muestran deshabilitadas",
            "Hasta cuatro productos relacionados de la misma categoría",
        ]),
        ("M03", "Personalizar", ACCENT, [
            "Elegir zona (pecho, espalda, manga), técnica (DTF, serigrafía, vinil, bordado) y tamaño (A5, A4, A3)",
            "Subir una imagen o escribir un texto con tipografía y color",
            "Vista previa del estampado sobre la prenda elegida",
            "Recargo calculado al instante y guardado en Mis diseños",
            "Solo PNG o JPG de hasta 5 MB: el resto se rechaza indicando el motivo",
        ]),
        ("M04-M07", "Comprar", GREEN, [
            "Carrito de invitado que se fusiona con la cuenta al iniciar sesión",
            "Favoritos, cupones de descuento y cálculo del envío",
            "Checkout con libreta de direcciones y pago simulado",
            "Código de pedido CS-2026-000123 al confirmar",
            "Si una talla se agotó mientras compraba, el pedido no se crea y el carrito queda intacto",
        ]),
        ("M08-M10", "Seguir y opinar", GOLD, [
            "Estado del pedido con su línea de tiempo completa",
            "Notificación en la bandeja ante cada cambio de estado",
            "Reseña solo si compró el producto y ya lo recibió",
            "Perfil, direcciones, historial y diseños guardados",
            "Recuperación de contraseña con token de un solo uso",
        ]),
    ]
    for i, (cod, titulo, color, items) in enumerate(bloques):
        fila, col = divmod(i, 2)
        x = 0.7 + col * 6.15
        y = 1.62 + fila * 2.6
        caja(s, x, y, 5.85, 2.4, color=CARD, borde=LINE)
        caja(s, x, y, 0.07, 2.4, color=color, radio=0.02, forma=MSO_SHAPE.RECTANGLE)
        chip(s, x + 0.26, y + 0.22, 1.05, 0.26, cod, color=color, size=8.5)
        texto(s, x + 1.45, y + 0.19, 4.2, 0.32, titulo, size=15, color=color,
              bold=True, font=TITULO)
        vinetas(s, x + 0.26, y + 0.62, 5.35, items, size=10, interlineado=1.25,
                bullet_color=color, sep=0.035)


# ----------------------------------------------------- 14 funcionalidades admin
def funcionalidades_admin(prs):
    s = lamina(prs)
    cabecera(s, "3 · Funcionalidades", "Lo que puede hacer la tienda")
    bloques = [
        ("M11", "Tablero", PRIMARY, [
            "Ventas del día y del mes",
            "Pedidos por estado",
            "Top de productos vendidos",
            "Alertas de stock crítico",
        ]),
        ("M12-M13", "Catálogo y maestros", BLUE, [
            "CRUD de categorías jerárquicas",
            "Productos con varias imágenes",
            "Variantes con SKU generado",
            "Tallas, colores, técnicas y zonas",
        ]),
        ("M14", "Inventario", GREEN, [
            "Ajustes de stock con motivo",
            "Kardex de todo movimiento",
            "Alertas de stock mínimo",
            "Reserva y liberación por pedido",
        ]),
        ("M15", "Pedidos", ACCENT, [
            "Bandeja filtrable por estado",
            "Cambio de estado validado",
            "Aprobación del arte del cliente",
            "Historial con responsable",
        ]),
        ("M16-M18", "Gobierno", GOLD, [
            "Usuarios, roles y permisos",
            "Campañas de cupones",
            "Modalidades y costos de envío",
            "Baja lógica, nunca borrado",
        ]),
        ("M19-M20", "Reportes y auditoría", PRIMARY, [
            "Ventas por periodo y categoría",
            "Productos más vendidos",
            "Exportación a CSV",
            "Bitácora de toda acción admin",
        ]),
    ]
    for i, (cod, titulo, color, items) in enumerate(bloques):
        fila, col = divmod(i, 3)
        x = 0.7 + col * 4.05
        y = 1.62 + fila * 2.6
        caja(s, x, y, 3.75, 2.4, color=CARD, borde=LINE)
        caja(s, x, y, 0.07, 2.4, color=color, radio=0.02, forma=MSO_SHAPE.RECTANGLE)
        chip(s, x + 0.24, y + 0.22, 1.05, 0.26, cod, color=color, size=8.5)
        texto(s, x + 0.24, y + 0.6, 3.3, 0.32, titulo, size=14, color=color,
              bold=True, font=TITULO)
        vinetas(s, x + 0.24, y + 1.02, 3.3, items, size=9.8, interlineado=1.25,
                bullet_color=color, sep=0.03)


# --------------------------------------------------------------- 15 casos uso
def casos_uso(prs):
    s = lamina(prs)
    cabecera(s, "3 · Actores y casos de uso", "Quién hace qué en el sistema")
    figura(s, "05_casos_uso.png", y=1.55, ancho_max=11.4, alto_max=5.3)
    pie(s, "El invitado solo alcanza los cuatro primeros casos de uso: al intentar el checkout "
           "debe registrarse y su carrito de sesión se fusiona con el de su cuenta.")


# ------------------------------------------------------------- 16 tecnologias
def tecnologias(prs):
    s = lamina(prs)
    cabecera(s, "4 · Stack", "Tecnologías y su sustento en las clases del curso")

    caja(s, 0.7, 1.62, 3.85, 5.05, color=CARD, borde=LINE)
    chip(s, 0.7, 1.62, 3.85, 0.4, "FRONTEND", color=BLUE, size=10.5)
    vinetas(s, 0.98, 2.2, 3.35, [
        "React 19 + Vite", "Tailwind CSS", "React Router", "Context API",
        "Fetch sobre /api/v1", "Desplegado en Netlify",
    ], size=11.5, interlineado=1.3, bullet_color=BLUE, sep=0.09)
    texto(s, 0.98, 4.75, 3.35, 1.7,
          "Decisión del equipo: una SPA evita recargar la página en cada filtro del "
          "catálogo y es lo que hace posible un personalizador de estampado fluido.",
          size=10, color=MUTED, interlineado=1.3)

    caja(s, 4.72, 1.62, 4.6, 5.05, color=PRIMARY)
    chip(s, 4.72, 1.62, 4.6, 0.4, "BACKEND  ·  JAVA EE DEL CURSO", color=DARK, size=10.5)
    filas = [
        ("Java 17 + JVM", "S01 · Arquitectura Java"),
        ("Jakarta Servlets (controlador)", "S01 · Servlet = Controlador"),
        ("JavaBeans (modelo)", "S01 · Bean = Modelo"),
        ("Apache Tomcat 10 (web container)", "S03 · Web Server vs Container"),
        ("JDBC: PreparedStatement y ResultSet", "S03 · JDBC"),
        ("HttpSession y JSESSIONID", "Clase 4 · Session scope"),
        ("Docker y Docker Compose", "S02 · Contenedores web"),
    ]
    y = 2.18
    for tecnologia, fuente in filas:
        texto(s, 5.0, y, 4.05, 0.28, tecnologia, size=11, color=CREAM, bold=True,
              interlineado=1.15)
        texto(s, 5.0, y + 0.28, 4.05, 0.22, fuente, size=8.8, color=ROSE)
        y += 0.63

    caja(s, 9.49, 1.62, 3.14, 5.05, color=CARD, borde=LINE)
    chip(s, 9.49, 1.62, 3.14, 0.4, "DATOS Y CALIDAD", color=GREEN, size=10.5)
    vinetas(s, 9.77, 2.2, 2.64, [
        "PostgreSQL 16", "HikariCP (pool)", "Gson (JSON)", "JWT + BCrypt",
        "Maven (WAR)", "JUnit 5 + Mockito", "Postman y Swagger", "Git y GitHub",
    ], size=11, interlineado=1.3, bullet_color=GREEN, sep=0.09)


# ------------------------------------------------------------- 17 arquitectura
def arquitectura(prs):
    s = lamina(prs)
    cabecera(s, "4 · Arquitectura de la solución",
             "Cliente-servidor en tres capas sobre un contenedor web Java")
    figura(s, "03_arquitectura.png", y=1.52, ancho_max=12.1, alto_max=5.35)
    pie(s, "El Servlet recibe y coordina, el Servicio concentra las reglas y la transacción, "
           "y el DAO es el único punto que conoce SQL.")


# ------------------------------------------------------------------- 18 mvc
def mvc(prs):
    s = lamina(prs)
    cabecera(s, "4 · Justificación", "Cómo aplicamos el MVC visto en clase")

    texto(s, 0.7, 1.6, 11.93, 0.5,
          "La sesión 1 cierra estableciendo la correspondencia: JavaBean es el Modelo, "
          "el Servlet es el Controlador y el JSP es la Vista. La conservamos con una sola adaptación.",
          size=12.5, color=TEXT, interlineado=1.3)

    cols = [
        ("MODELO", "JavaBean por tabla", "Idéntico a la teoría", GREEN,
         "paquete model + DTO para la API.\nAtributos privados con getters y setters, "
         "sin lógica de negocio."),
        ("CONTROLADOR", "Servlet por recurso", "Idéntico a la teoría", PRIMARY,
         "paquete web.controller + filtros.\nLee la petición, delega en el servicio y "
         "serializa la respuesta."),
        ("VISTA", "JSP con EL y JSTL", "Adaptado: React en el navegador", ACCENT,
         "El servlet responde JSON en lugar de hacer forward a un JSP, porque el cliente "
         "es una aplicación de página única."),
    ]
    for i, (capa, clase, estado, color, detalle) in enumerate(cols):
        x = 0.7 + i * 4.05
        caja(s, x, 2.35, 3.75, 2.6, color=CARD, borde=LINE)
        chip(s, x, 2.35, 3.75, 0.4, capa, color=color, size=10.5)
        texto(s, x + 0.26, 2.95, 3.23, 0.34, clase, size=14, color=color, bold=True,
              font=TITULO)
        texto(s, x + 0.26, 3.38, 3.23, 0.34, estado, size=10.5, color=MUTED,
              italic=True, interlineado=1.2)
        texto(s, x + 0.26, 3.9, 3.23, 0.9, detalle, size=10.5, color=TEXT,
              interlineado=1.3)

    caja(s, 0.7, 5.15, 11.93, 1.5, color=PRIMARY)
    texto(s, 1.0, 5.35, 11.3, 0.24, "POR QUÉ LA ADAPTACIÓN NO ROMPE EL PATRÓN",
          size=9.5, color=ROSE, bold=True, spc=150)
    texto(s, 1.0, 5.65, 11.3, 0.85,
          "El Servlet sigue siendo el Controlador y sigue sin contener reglas de negocio ni SQL: lo único "
          "que cambia es el formato de la respuesta, de HTML a JSON. Añadimos además una capa de servicio "
          "entre el controlador y el acceso a datos, para no concentrar la lógica en el servlet.",
          size=11.5, color=CREAM, interlineado=1.3)


# ------------------------------------------------------------------ 19 flujo
def flujo(prs):
    s = lamina(prs)
    cabecera(s, "4 · Cómo colaboran las capas", "Confirmación de un pedido personalizado")
    figura(s, "04_flujo_peticion.png", y=1.55, ancho_max=12.0, alto_max=5.3)
    pie(s, "Si una variante no tiene stock, el servicio hace rollback y responde 409: nunca "
           "queda un pedido a medio grabar.")


# ---------------------------------------------------------------- 20 datos
def datos_global(prs):
    s = lamina(prs)
    cabecera(s, "5 · Modelo de datos", "28 tablas agrupadas en cinco módulos")
    figura(s, "10_er_global.png", y=1.55, ancho_max=12.0, alto_max=5.3)


def datos_er1(prs):
    s = lamina(prs)
    cabecera(s, "5 · Modelo entidad-relación (1 de 2)", "Usuarios, catálogo e inventario")
    figura(s, "08_er_usuarios_catalogo.png", y=1.5, ancho_max=12.4, alto_max=5.55)


def datos_er2(prs):
    s = lamina(prs)
    cabecera(s, "5 · Modelo entidad-relación (2 de 2)",
             "Personalización, carrito, pedidos y soporte")
    figura(s, "09_er_personalizacion_compra.png", y=1.5, ancho_max=12.4, alto_max=5.55)


def datos_decisiones(prs):
    s = lamina(prs)
    cabecera(s, "5 · Modelo de datos", "Las decisiones que sostienen el modelo")
    decisiones = [
        ("El stock vive en la variante",
         "product guarda el modelo de prenda; product_variant guarda cada combinación real de "
         "talla y color con su SKU, su stock y su precio propio. UNIQUE (product_id, size_id, color_id).",
         BLUE),
        ("El pedido es inmutable",
         "order_item copia nombre, SKU, talla, color y precio al momento de comprar. Si mañana "
         "sube el precio, los pedidos ya emitidos no cambian. Desnormalización consciente.",
         GREEN),
        ("La personalización es una entidad propia",
         "customization guarda la configuración concreta del estampado y puede reutilizar un "
         "design de Mis diseños. La misma estructura sirve al carrito y al pedido.",
         ACCENT),
        ("Todo movimiento deja rastro",
         "Ninguna operación cambia el stock sin escribir en inventory_movement el stock anterior, "
         "el nuevo, el motivo y el responsable. Lo mismo hacen order_status_history y audit_log.",
         GOLD),
    ]
    for i, (titulo, cuerpo, color) in enumerate(decisiones):
        fila, col = divmod(i, 2)
        x = 0.7 + col * 6.15
        y = 1.7 + fila * 2.5
        tarjeta(s, x, y, 5.85, 2.25, titulo, cuerpo, color=color, size_t=15,
                size_c=10.5)
    pie(s, "222 campos  ·  39 claves foráneas  ·  tercera forma normal, con la excepción "
           "deliberada de order_item")


# ---------------------------------------------------------------- 21 estados
def estados(prs):
    s = lamina(prs)
    cabecera(s, "5 · Reglas del negocio en el código", "Máquina de estados del pedido")
    figura(s, "06_estados_pedido.png", y=1.7, ancho_max=12.0, alto_max=4.7)
    pie(s, "Enum OrderStatus + EnumMap de transiciones permitidas: cualquier salto no declarado "
           "lanza TransicionInvalidaException (HTTP 409).")


# ------------------------------------------------------------ 22 paquetes
def paquetes(prs):
    s = lamina(prs)
    cabecera(s, "6 · Implementación", "Estructura de paquetes y clases")

    caja(s, 0.7, 1.62, 5.7, 5.05, color=DARK)
    texto(s, 1.0, 1.86, 5.1, 0.24, "pe.edu.utp.coralshop", size=10, color=ROSE,
          bold=True, spc=100)
    arbol = (
        "config/      DataSourceProvider, AppContextListener\n"
        "web/\n"
        "  controller/  Servlets, uno por recurso\n"
        "  filter/      CORS, JWT, roles, logging\n"
        "  listener/    arranque y cierre del pool\n"
        "service/     reglas de negocio y transacción\n"
        "  impl/        implementaciones\n"
        "dao/         interfaces de acceso a datos\n"
        "  jdbc/        PreparedStatement y ResultSet\n"
        "model/       un JavaBean por tabla\n"
        "  dto/         entrada y salida de la API\n"
        "  enums/       OrderStatus, MovementType...\n"
        "exception/   excepciones de negocio\n"
        "util/        Json, Password, Jwt, SkuGenerator"
    )
    texto(s, 1.0, 2.2, 5.1, 4.2, arbol, size=10, color=CREAM, font="Consolas",
          interlineado=1.42)

    caja(s, 6.6, 1.62, 6.03, 2.4, color=CARD, borde=LINE)
    texto(s, 6.88, 1.86, 5.47, 0.3, "La regla de dependencia", size=15,
          color=PRIMARY, bold=True, font=TITULO)
    texto(s, 6.88, 2.28, 5.47, 0.4,
          "web.controller → service → dao → model.  Nunca al revés.",
          size=12, color=BLUE, bold=True)
    texto(s, 6.88, 2.75, 5.47, 1.1,
          "Un DAO no conoce al servicio que lo invoca y un servicio no sabe si lo llama un "
          "servlet o una prueba. Gracias a eso la capa de servicio se prueba con Mockito sin "
          "levantar Tomcat ni la base de datos.",
          size=10.5, color=TEXT, interlineado=1.3)

    caja(s, 6.6, 4.22, 6.03, 2.45, color=CARD, borde=LINE)
    texto(s, 6.88, 4.44, 5.47, 0.3, "POO aplicada", size=15, color=PRIMARY,
          bold=True, font=TITULO)
    vinetas(s, 6.88, 4.86, 5.47, [
        ("Encapsulamiento: ", "atributos privados con getters y setters (estándar JavaBean)."),
        ("Abstracción: ", "cada DAO y servicio se declara primero como interfaz."),
        ("Herencia: ", "AbstractJdbcDao concentra conexión, cierre y manejo de SQLException."),
        ("Polimorfismo: ", "PricingService resuelve el recargo según la técnica."),
        ("Composición: ", "OrderService compone cuatro DAO en una sola transacción."),
    ], size=10, interlineado=1.22, sep=0.03)


# ------------------------------------------------------------ 23 algoritmos
def algoritmos(prs):
    s = lamina(prs)
    cabecera(s, "6 · Implementación", "Algoritmos y estructuras de datos")
    filas = [
        ("Carrito en sesión", "HashMap", "O(1)",
         "Clave = variante + hash de la personalización", BLUE),
        ("Ordenar el catálogo", "Comparator + TimSort", "O(n log n)",
         "Comparadores encadenados por precio, valoración y fecha", BLUE),
        ("Árbol de categorías", "Árbol n-ario, recorrido DFS", "O(n)",
         "category se autorreferencia con parent_id", GREEN),
        ("Estados del pedido", "EnumMap + EnumSet", "O(1)",
         "Sustituye una cadena de condicionales anidados", ACCENT),
        ("Cola de estampados", "Queue (FIFO)", "O(1)",
         "El taller atiende en el orden en que se aprobó el arte", ACCENT),
        ("Precios y descuentos", "BigDecimal, HALF_UP", "—",
         "Evita el error de redondeo del punto flotante en dinero", GOLD),
        ("Búsqueda por SKU o slug", "Índice B-tree", "O(log n)",
         "Frente al recorrido secuencial de la tabla", GREEN),
        ("Reserva de stock", "SELECT ... FOR UPDATE", "O(log n)",
         "Impide que dos compras vendan la misma última unidad", PRIMARY),
    ]
    y0 = 1.62
    chip(s, 0.7, y0, 11.93, 0.36, "", color=PRIMARY)
    encabezados = [("PROPÓSITO", 0.95, 2.9), ("ESTRUCTURA", 3.95, 2.8),
                   ("COMPLEJIDAD", 6.85, 1.5), ("POR QUÉ", 8.45, 4.0)]
    for t, x, w in encabezados:
        texto(s, x, y0, w, 0.36, t, size=9.5, color=WHITE, bold=True, spc=80,
              anchor=M)
    for i, (prop, est, cmpx, motivo, color) in enumerate(filas):
        y = y0 + 0.46 + i * 0.62
        if i % 2 == 0:
            caja(s, 0.7, y - 0.06, 11.93, 0.56, color=CARD, radio=0.02)
        texto(s, 0.95, y, 2.9, 0.45, prop, size=11, color=color, bold=True, anchor=M)
        texto(s, 3.95, y, 2.8, 0.45, est, size=10.5, color=TEXT, anchor=M)
        texto(s, 6.85, y, 1.5, 0.45, cmpx, size=10.5, color=MUTED, bold=True, anchor=M)
        texto(s, 8.45, y, 4.0, 0.45, motivo, size=10, color=MUTED, anchor=M,
              interlineado=1.15)


# ------------------------------------------------------------ 24 metodologia
def metodologia(prs):
    s = lamina(prs)
    cabecera(s, "6 · Cómo trabajamos", "Metodología TDD y plan de trabajo")

    for i, (n, titulo, desc, color) in enumerate([
        ("1", "Red", "Se escribe la prueba con JUnit para una funcionalidad que aún no existe, "
         "y por tanto falla.", ACCENT),
        ("2", "Green", "Se escribe el código mínimo en Java para que esa prueba concreta pase.", GREEN),
        ("3", "Refactor", "Se limpia y optimiza el código con la confianza de que las pruebas "
         "siguen respaldándolo.", BLUE),
    ]):
        x = 0.7 + i * 4.05
        caja(s, x, 1.62, 3.75, 1.85, color=CARD, borde=LINE)
        chip(s, x + 0.26, 1.86, 0.42, 0.42, n, color=color, size=13)
        texto(s, x + 0.9, 1.9, 2.6, 0.34, titulo, size=17, color=color, bold=True,
              font=TITULO)
        texto(s, x + 0.26, 2.46, 3.23, 0.85, desc, size=10.5, color=TEXT,
              interlineado=1.3)

    caja(s, 0.7, 3.72, 11.93, 2.95, color=CARD, borde=LINE)
    chip(s, 0.7, 3.72, 11.93, 0.4, "CRONOGRAMA", color=PRIMARY, size=10.5)
    sprints = [
        ("Sprint 0", "Sem. 9-10", "Diagnóstico y diseño", "Este informe", "Completado", GREEN),
        ("Sprint 1", "Sem. 11-12", "Cimientos", "Maven, Docker, schema.sql, usuarios y JWT", "Planificado", MUTED),
        ("Sprint 2", "Sem. 13-14", "Catálogo e inventario", "M01, M02, M12, M13, M14", "Planificado", MUTED),
        ("Sprint 3", "Sem. 15-16", "Personalización y compra", "M03 a M08", "Planificado", MUTED),
        ("Sprint 4", "Sem. 17", "Backoffice y cierre", "M09, M11, M15, M17 a M20", "Planificado", MUTED),
        ("Sprint 5", "Sem. 18", "Exposición", "Ensayo y demostración", "Planificado", MUTED),
    ]
    y = 4.32
    for nombre, periodo, objetivo, entregable, estado, color in sprints:
        texto(s, 1.0, y, 1.2, 0.3, nombre, size=11, color=PRIMARY, bold=True, anchor=M)
        texto(s, 2.25, y, 1.3, 0.3, periodo, size=10.5, color=MUTED, anchor=M)
        texto(s, 3.6, y, 2.9, 0.3, objetivo, size=10.5, color=TEXT, anchor=M)
        texto(s, 6.6, y, 4.6, 0.3, entregable, size=10.5, color=MUTED, anchor=M)
        chip(s, 11.3, y + 0.02, 1.15, 0.26, estado, color=color, size=8)
        y += 0.38


# --------------------------------------------------------------- 25 cierre
def cierre(prs):
    s = lamina(prs, DARK)
    caja(s, -1.4, 4.6, 4.6, 4.6, color=PRIMARY, forma=MSO_SHAPE.OVAL)
    caja(s, 11.0, -1.4, 3.8, 3.8, color=ACCENT, forma=MSO_SHAPE.OVAL)

    texto(s, 1.2, 1.0, 9.5, 0.3, "PARA CERRAR", size=11, color=ROSE, bold=True, spc=200)
    texto(s, 1.2, 1.42, 10.5, 0.9, "Lo que dejamos definido", size=40, color=CREAM,
          bold=True, font=TITULO)

    puntos = [
        ("Un problema con causa raíz identificada",
         "Ishikawa, Canvas, PESTEL y FODA cruzado apuntan al mismo vacío: no hay canal propio."),
        ("Una tienda con las funcionalidades cerradas",
         "20 módulos, 49 requerimientos funcionales, 15 no funcionales y 14 reglas de negocio."),
        ("Una arquitectura justificada en la teoría del curso",
         "Servlets, JavaBeans, JDBC y Tomcat, en tres capas y con la Vista externalizada a React."),
        ("Un modelo de datos completo",
         "28 tablas, 222 campos y 39 claves foráneas, con su diccionario campo por campo."),
    ]
    for i, (t, d) in enumerate(puntos):
        fila, col = divmod(i, 2)
        x = 1.2 + col * 5.75
        y = 2.75 + fila * 1.55
        caja(s, x, y, 5.4, 1.3, color=PRIMARY)
        texto(s, x + 0.3, y + 0.2, 4.8, 0.34, t, size=13, color=CREAM, bold=True,
              font=TITULO, interlineado=1.15)
        texto(s, x + 0.3, y + 0.66, 4.8, 0.5, d, size=10, color=MUTED_LIGHT,
              interlineado=1.25)

    texto(s, 1.2, 6.35, 10.5, 0.4,
          "Gracias.  ¿Preguntas?",
          size=20, color=ROSE, bold=True, font=TITULO)
    texto(s, 8.9, 6.98, 3.7, 0.3, "coral-st.netlify.app", size=10, color=MUTED_LIGHT,
          align=PP_ALIGN.RIGHT)


def main():
    prs = nueva_presentacion()
    laminas = [
        portada, agenda, empresa, canvas, pestel, foda, ishikawa, problematica,
        objetivos, solucion, alcance, modulos, funcionalidades_cliente,
        funcionalidades_admin, casos_uso, tecnologias, arquitectura, mvc, flujo,
        datos_global, datos_er1, datos_er2, datos_decisiones, estados, paquetes,
        algoritmos, metodologia, cierre,
    ]
    for f in laminas:
        f(prs)
    # numeracion (se omite en portada y cierre)
    total = len(prs.slides._sldIdLst)
    for i, slide in enumerate(prs.slides, start=1):
        if i in (1, total):
            continue
        numero(slide, i, total)
    prs.save(SALIDA)
    print(f"Presentacion generada ({total} laminas):", SALIDA)


if __name__ == "__main__":
    main()
