# -*- coding: utf-8 -*-
"""Genera clase_entregables/Presentacion_Proyecto_Final_Coral_Shop.pptx (exposición final).

Cada lámina lleva notas del orador con el expositor y qué decir (presentacion_notas.NOTAS).
portada() también la usa avance2_presentacion.py."""

import os

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

import contenido as CONT
import esquema
from presentacion_notas import NOTAS
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
def portada(prs, lema="Proyecto Final  ·  Diagnóstico, diseño de la solución y plan de implementación"):
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
          lema, size=14, color=MUTED_LIGHT)

    caja(s, 0.8, 4.35, 11.1, 2.0, color=PRIMARY)
    datos = [("CURSO", "Desarrollo Web Integrado", 1.15, 3.2),
             ("DOCENTE", CONT.DOCENTE, 4.75, 3.6),
             ("AÑO", CONT.CICLO, 8.7, 2.0)]
    for etiqueta, valor, x, w in datos:
        texto(s, x, 4.62, w, 0.25, etiqueta, size=9.5, color=ROSE, bold=True, spc=100)
        texto(s, x, 4.90, w, 0.32, valor, size=13, color=CREAM)
    texto(s, 1.15, 5.44, 3.0, 0.25, "GRUPO 1", size=9.5, color=ROSE, bold=True, spc=100)
    texto(s, 1.15, 5.72, 10.4, 0.6, "  ·  ".join(CONT.INTEGRANTES),
          size=12.5, color=CREAM, interlineado=1.25)


def portada_final(prs):
    portada(prs, lema="Proyecto Final  ·  Diagnóstico, solución implementada y demostración")


# ------------------------------------------------------------------- 2 agenda
def agenda(prs):
    s = lamina(prs)
    cabecera(s, "Agenda", "Lo que vamos a recorrer")
    bloques = [
        ("1", "Diagnóstico del negocio", "Empresa, Canvas, PESTEL, FODA e Ishikawa", PRIMARY),
        ("2", "Problemática y objetivos", "La causa raíz y las metas medibles", ACCENT),
        ("3", "La solución", "12 módulos, personalizador y mayoreo", BLUE),
        ("4", "Arquitectura", "Cliente-servidor, MVC, capas y eventos", PRIMARY),
        ("5", "Modelo de datos", f"{esquema.totales()[0]} tablas versionadas con Flyway", GREEN),
        ("6", "Implementación y demo", "Paquetes, algoritmos, pruebas y demo en vivo", GOLD),
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
        ("Estampado y bordado personalizados: ", "el cliente elige la técnica y las "
         "zonas, y sube su propio diseño."),
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
         "Precio final desglosado y políticas publicadas en la tienda", PRIMARY),
        ("Económico", "Tipo de cambio volátil encarece los insumos importados",
         "Los costos de estampado son configurables en base de datos", BLUE),
        ("Social", "El joven valora la autoexpresión y encarga prendas en grupo",
         "Origina el personalizador (M03) y el mayoreo repartible (M04)", ACCENT),
        ("Tecnológico", "Estampado DTF y bordado para tiradas cortas; Spring Boot maduro",
         "Producir desde una unidad; Spring Boot y PostgreSQL en Docker", GREEN),
        ("Ecológico", "Presión por reducir el desperdicio textil",
         "Producir bajo demanda evita el sobrestock", GOLD),
        ("Legal", "Ley 29733 de Protección de Datos Personales",
         "BCrypt, CSRF, diseños privados y nunca guardar la tarjeta", PRIMARY),
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
          "Diseñar e implementar una plataforma web que permita al cliente personalizar prendas y "
          "comprarlas por unidad o por mayor, y a la empresa gestionar catálogo, inventario por variante "
          "y el ciclo completo del pedido.",
          size=12, color=CREAM, interlineado=1.28)

    oes = [
        ("OE-1", "Tienda virtual operativa", "80 % de pedidos por la web al 3.er mes", PRIMARY),
        ("OE-2", "Personalizador automático", "Cotizar: de 6 horas a menos de 1 minuto", ACCENT),
        ("OE-3", "Inventario y mayoreo", "Cancelaciones por stock: de 12 % a < 2 %", BLUE),
        ("OE-4", "Trazabilidad del pedido", "100 % de cambios auditados y avisados", GREEN),
        ("OE-5", "Seguridad", "0 accesos a recursos ajenos en las pruebas", GOLD),
        ("OE-6", "Arquitectura del curso", "73 de 73 pruebas automatizadas en verde", PRIMARY),
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
    cabecera(s, "3 · La solución", "Qué construimos")
    tarjetas = [
        ("Stock por variante", "Cada combinación de producto, talla y color tiene su SKU y su stock. Se "
         "descuenta en la misma transacción del pedido: no hay sobreventa.", BLUE),
        ("Personalizador", "Técnica y zonas válidas según la prenda, subida del diseño, vista previa sobre "
         "la silueta y precio calculado por el servidor al instante.", ACCENT),
        ("Mayoreo repartible", "Un mismo diseño se reparte entre tallas y colores y alcanza su escala: "
         "3 → 5 %, 6 → 10 %, 12 → 15 % de descuento.", GREEN),
    ]
    for i, (t, c, color) in enumerate(tarjetas):
        tarjeta(s, 0.7 + i * 4.05, 1.62, 3.78, 2.05, t, c, color=color, size_c=10.5)

    caja(s, 0.7, 3.92, 7.6, 2.75, color=CARD, borde=LINE)
    texto(s, 1.0, 4.1, 7.0, 0.26, "IMPLEMENTADO Y FUNCIONANDO EN LOCAL", size=9.5, color=GREEN, bold=True, spc=120)
    vinetas(s, 1.0, 4.42, 7.0, [
        "Tienda: catálogo, ficha, personalizador, carrito, checkout y pago simulado",
        "Cliente: cuenta, direcciones, «Mis pedidos» con línea de tiempo y campana de avisos",
        "Panel: tablero, productos y variantes, categorías, bandeja de pedidos, usuarios",
        "Calidad: 73 pruebas, Swagger, Postman y datos demo ficticios",
    ], size=10.5, interlineado=1.25, bullet_color=GREEN)
    caja(s, 8.55, 3.92, 4.08, 2.75, color=PRIMARY)
    texto(s, 8.85, 4.1, 3.5, 0.26, "TRABAJO FUTURO", size=9.5, color=ROSE, bold=True, spc=120)
    vinetas(s, 8.85, 4.42, 3.5, [
        "Pasarela de pago real (sandbox)",
        "Despliegue público",
        "Correo al cliente",
        "Cupones, favoritos y reseñas",
    ], size=10.5, color=CREAM, interlineado=1.25, bullet_color=ROSE)


# ----------------------------------------------------------------- 11 modulos
def modulos(prs):
    s = lamina(prs)
    cabecera(s, "3 · Características de la tienda", "12 módulos, 36 requerimientos funcionales")
    figura(s, "07_modulos.png", y=1.6, ancho_max=12.0, alto_max=4.9)
    pie(s, "Todos implementados y verificados. Detalle de requerimientos, historias de usuario y reglas en la "
           "sección 2.1 del informe.")


# ---------------------------------------------------------- 12 personalizador
def personalizador(prs):
    s = lamina(prs)
    cabecera(s, "3 · El corazón del negocio", "Personalizador y mayoreo")
    figura(s, "capturas/C04_personalizador.png", x=0.7, y=1.5, ancho_max=5.0, alto_max=5.35)
    caja(s, 6.1, 1.6, 6.53, 2.15, color=CARD, borde=LINE)
    texto(s, 6.4, 1.78, 6.0, 0.26, "HISTORIA DE REFERENCIA", size=9.5, color=ACCENT, bold=True, spc=120)
    texto(s, 6.4, 2.1, 6.0, 1.5,
          "«Como delegado de mi promoción quiero 12 polos con el mismo logo bordado en el pecho, repartidos "
          "en 4 S, 4 M y 4 L, y pagar precio de docena.»", size=13, color=TEXT, font=TITULO, interlineado=1.3)
    filas = [("Prenda base", "S/ 35.00"), ("+ Bordado", "S/ 15.00"), ("+ Pecho izquierdo", "S/ 8.00"),
             ("= Precio unitario", "S/ 58.00"), ("× 12 unidades", "S/ 696.00"), ("− 15 % docena", "− S/ 104.40")]
    for i, (k, v) in enumerate(filas):
        y = 3.98 + i * 0.36
        texto(s, 6.4, y, 3.6, 0.3, k, size=11.5, color=TEXT)
        texto(s, 9.6, y, 2.7, 0.3, v, size=11.5, color=TEXT, bold=True, align=PP_ALIGN.RIGHT)
    caja(s, 6.1, 6.2, 6.53, 0.55, color=PRIMARY)
    texto(s, 6.4, 6.2, 6.0, 0.55, "Total del diseño:  S/ 591.60  · calculado por el servidor", size=14,
          color=CREAM, bold=True, anchor=M)


# ----------------------------------------------------------------- 13 casos de uso
def casos_uso(prs):
    s = lamina(prs)
    cabecera(s, "3 · Quién hace qué", "Casos de uso")
    figura(s, "05_casos_uso.png", y=1.5, ancho_max=11.4, alto_max=5.35)


# --------------------------------------------------------------- 14 tecnologias
def tecnologias(prs):
    s = lamina(prs)
    cabecera(s, "4 · Tecnologías", "Stack y sustento en lo visto en clase")
    stack = [
        ("VISTA", "React 19 · Vite 8 · Tailwind 4 · React Router 7", BLUE),
        ("SERVIDOR", "Spring Boot 3.5 · Java 21 · Tomcat embebido", PRIMARY),
        ("DATOS", "PostgreSQL 16 en Docker · Flyway V1–V6 · JdbcTemplate", GREEN),
        ("SEGURIDAD", "Spring Security · sesión JSESSIONID · CSRF · BCrypt", ACCENT),
        ("CALIDAD", "JUnit 5 · Testcontainers · Swagger · Postman", GOLD),
    ]
    for i, (k, v, color) in enumerate(stack):
        y = 1.62 + i * 0.98
        caja(s, 0.7, y, 5.7, 0.82, color=CARD, borde=LINE)
        chip(s, 0.9, y + 0.24, 1.35, 0.34, k, color=color, size=9)
        texto(s, 2.45, y, 3.85, 0.82, v, size=11, color=TEXT, anchor=M, interlineado=1.15)

    caja(s, 6.7, 1.62, 5.93, 5.05, color=PRIMARY)
    texto(s, 7.0, 1.84, 5.4, 0.26, "¿POR QUÉ SPRING BOOT?", size=10, color=ROSE, bold=True, spc=150)
    texto(s, 7.0, 2.16, 5.4, 0.7, "No reemplaza lo visto en clase: lo empaqueta.", size=15, color=CREAM,
          bold=True, font=TITULO)
    pares = [("Servlet = Controlador (S01)", "DispatcherServlet + @RestController"),
             ("Contenedor web (S02)", "Tomcat embebido"),
             ("JDBC + PreparedStatement (S03)", "JdbcTemplate con parámetros ?"),
             ("commit / rollback (S03)", "@Transactional"),
             ("Session scope (Clase 4)", "Cookie JSESSIONID"),
             ("JSP = Vista (Clase 4)", "React en el navegador")]
    for i, (a, b) in enumerate(pares):
        y = 2.95 + i * 0.6
        texto(s, 7.0, y, 2.85, 0.5, a, size=10.5, color=ROSE, interlineado=1.1)
        texto(s, 9.9, y, 2.55, 0.5, "→  " + b, size=10.5, color=CREAM, bold=True, interlineado=1.1)


# -------------------------------------------------------------- 15 arquitectura
def arquitectura(prs):
    s = lamina(prs)
    cabecera(s, "4 · Arquitectura", "Cliente-servidor en capas")
    figura(s, "03_arquitectura.png", y=1.5, ancho_max=11.6, alto_max=5.35)


# -------------------------------------------------- 16 cliente-servidor y MVC
def cs_mvc(prs):
    s = lamina(prs)
    cabecera(s, "4 · Patrones vistos en clase", "Cliente-servidor y MVC")
    figura(s, "A2_03_cliente_servidor.png", x=0.6, y=1.55, ancho_max=6.0, alto_max=3.9)
    figura(s, "A2_04_mvc.png", x=6.75, y=1.55, ancho_max=6.0, alto_max=3.9)
    tarjeta(s, 0.7, 5.6, 5.85, 1.12, "Un servidor, varios clientes",
            "Tienda, panel, Swagger y Postman hablan con la misma API; solo el servidor toca PostgreSQL.",
            color=BLUE, size_t=12, size_c=10)
    tarjeta(s, 6.78, 5.6, 5.85, 1.12, "La Vista pasó al navegador",
            "React reemplaza a la JSP; el controlador responde JSON en lugar de hacer forward.",
            color=GREEN, size_t=12, size_c=10)


# ------------------------------------------------------------ 17 capas y flujo
def capas_flujo(prs):
    s = lamina(prs)
    cabecera(s, "4 · Arquitectura en capas", "Recorrido del pedido de 12 polos")
    figura(s, "04_flujo_peticion.png", y=1.5, ancho_max=10.4, alto_max=4.55)
    chips = [("400", "formato · controller", PRIMARY), ("422", "regla · service", BLUE),
             ("409", "stock · transacción", GREEN), ("404", "recurso ajeno", ACCENT)]
    for i, (n, d, color) in enumerate(chips):
        x = 0.9 + i * 3.0
        chip(s, x, 6.25, 0.8, 0.42, n, color=color, size=13)
        texto(s, x + 0.95, 6.25, 2.0, 0.42, d, size=10.5, color=TEXT, anchor=M)


# ------------------------------------------------------------------ 18 estados
def estados(prs):
    s = lamina(prs)
    cabecera(s, "4 · Ciclo de vida", "Máquina de estados del pedido")
    figura(s, "06_estados_pedido.png", y=1.55, ancho_max=12.0, alto_max=5.2)


# ------------------------------------------------------------------ 19 eventos
def eventos(prs):
    s = lamina(prs)
    cabecera(s, "4 · Arquitectura dirigida por eventos", "OrderStatusChanged")
    figura(s, "12_flujo_eventos.png", x=0.6, y=1.5, ancho_max=7.6, alto_max=5.3)
    vinetas(s, 8.5, 1.75, 4.2, [
        ("Tres publicadores: ", "crear el pedido, aprobar el pago y el cambio del administrador."),
        ("AuditListener: ", "antes del commit, en la misma transacción. Sin auditoría no hay cambio."),
        ("NotificationListener: ", "después del commit. Crea el aviso de la campana."),
        ("Idempotente: ", "event_id único; un evento repetido no duplica nada."),
        ("Extensible: ", "un correo al cliente sería otro suscriptor, sin tocar los servicios."),
    ], size=11, interlineado=1.3, sep=0.1)


# ------------------------------------------------------------------- 20 datos
def datos(prs):
    s = lamina(prs)
    n_t, n_c, n_fk = esquema.totales()
    cabecera(s, "5 · Modelo de datos", f"{n_t} tablas, {n_c} campos, {n_fk} claves foráneas")
    figura(s, "10_er_global.png", x=0.6, y=1.5, ancho_max=7.9, alto_max=4.3)
    vinetas(s, 8.75, 1.7, 3.9, [
        ("Stock en la variante: ", "UNIQUE (producto, talla, color) y CHECK stock ≥ 0."),
        ("Reglas como datos: ", "product_type_zones define zona × técnica × recargo."),
        ("Una línea = un diseño: ", "order_lines → order_line_zones → order_items (reparto)."),
        ("Pedido inmutable: ", "precios, SKU y dirección copiados al comprar."),
        ("Integridad en la base: ", "un solo pago aprobado por pedido; total = subtotal − descuento + envío."),
    ], size=10.5, interlineado=1.28, sep=0.08)
    pie(s, "Flyway V1–V6 crea el esquema al arrancar. Los diagramas ER completos están en el Anexo A del informe.")


# --------------------------------------------------------- 21 implementacion
def implementacion(prs):
    s = lamina(prs)
    cabecera(s, "6 · Implementación", "Paquetes por funcionalidad y por capa")
    caja(s, 0.7, 1.62, 5.6, 5.05, color=DARK)
    texto(s, 0.95, 1.8, 5.2, 4.8,
          "com.coralshop/\n"
          "├─ catalog/      controller · service · repository · dto\n"
          "├─ customization/\n"
          "├─ design/\n"
          "├─ pricing/      PricingService · QuantityPolicy\n"
          "├─ order/        … · event/OrderStatusChanged\n"
          "├─ payment/      PaymentGateway (interfaz)\n"
          "├─ notification/ listener · …\n"
          "├─ audit/        listener · repository\n"
          "├─ address/ shipping/ user/ stats/\n"
          "├─ auth/         SecurityConfig\n"
          "└─ common/       GlobalExceptionHandler\n\n"
          "17 paquetes · 131 clases · 0 controllers con SQL",
          size=10, color=CREAM, font="Consolas", interlineado=1.25)
    texto(s, 6.6, 1.62, 6.0, 0.3, "ALGORITMOS Y ESTRUCTURAS", size=10, color=ACCENT, bold=True, spc=150)
    algos = [
        ("EnumMap + EnumSet", "transiciones de estado en O(1)", PRIMARY),
        ("UPDATE … WHERE stock >= ?", "reserva atómica, sin sobreventa", GREEN),
        ("SELECT … FOR UPDATE", "un pedido no se paga dos veces", BLUE),
        ("Luhn", "valida la tarjeta de prueba", ACCENT),
        ("Bytes mágicos + SHA-256", "tipo real y huella del diseño", GOLD),
        ("SecureRandom", "código CS-XXXXXXXX impredecible", PRIMARY),
    ]
    for i, (a, b, color) in enumerate(algos):
        y = 2.05 + i * 0.77
        caja(s, 6.6, y, 6.03, 0.66, color=CARD, borde=LINE)
        caja(s, 6.6, y, 0.07, 0.66, color=color, radio=0.02, forma=MSO_SHAPE.RECTANGLE)
        texto(s, 6.85, y, 2.9, 0.66, a, size=11, color=color, bold=True, anchor=M)
        texto(s, 9.8, y, 2.75, 0.66, b, size=10.5, color=TEXT, anchor=M, interlineado=1.1)


# ------------------------------------------------------------------ 22 pruebas
def pruebas(prs):
    s = lamina(prs)
    cabecera(s, "6 · Calidad", "Cómo sabemos que funciona")
    cifras = [("73", "pruebas automatizadas\nen verde", PRIMARY), ("39", "peticiones Postman\nde la historia", BLUE),
              ("0", "accesos a recursos\najenos", GREEN), ("1", "historia completa\nen el navegador", GOLD)]
    for i, (n, d, color) in enumerate(cifras):
        x = 0.7 + i * 3.06
        caja(s, x, 1.62, 2.83, 1.8, color=CARD, borde=LINE)
        texto(s, x, 1.75, 2.83, 0.8, n, size=40, color=color, bold=True, font=TITULO, align=C)
        texto(s, x + 0.2, 2.65, 2.43, 0.65, d, size=10.5, color=MUTED, align=C, interlineado=1.2)
    tarjeta(s, 0.7, 3.7, 3.85, 2.97, "Unitarias", "PricingService con la historia de referencia (S/ 591.60) y "
            "cada regla de rechazo; QuantityPolicy; OrderStatusPolicy; detección de imagen; pasarela simulada; "
            "entrega del evento.", color=PRIMARY, size_c=10)
    tarjeta(s, 4.74, 3.7, 3.85, 2.97, "Integración", "Testcontainers con PostgreSQL 16 real y las migraciones "
            "V1–V6: pedido 201 con descuento de stock; 409 que deshace todo; 400 con errores por campo.",
            color=BLUE, size_c=10)
    tarjeta(s, 8.78, 3.7, 3.85, 2.97, "Seguridad", "Pedido, diseño o pago ajeno → 404; diseño ajeno en un "
            "pedido → 422; admin → 403; sin sesión → 401; sin token CSRF → 403.", color=GREEN, size_c=10)


# --------------------------------------------------------------------- 23 demo
def demo(prs):
    s = lamina(prs, DARK)
    texto(s, 0.7, 0.42, 11.9, 0.3, "DEMOSTRACIÓN EN VIVO", size=11, color=ACCENT, bold=True, spc=200)
    texto(s, 0.7, 0.74, 11.9, 0.7, "La historia de los 12 polos, de punta a punta", size=30, color=CREAM,
          bold=True, font=TITULO)
    pasos = [
        ("1", "Catálogo y ficha", "Polo clásico: stock por talla y color"),
        ("2", "Personalizar", "Bordado en pecho izquierdo + logo; la espalda no admite bordado"),
        ("3", "Mayoreo", "4 S, 4 M, 4 L → docena: S/ 591.60"),
        ("4", "Comprar", "Envío a Lima S/ 601.60; pago rechazado y luego aprobado"),
        ("5", "Panel", "Pedido PAGADO → EN_PRODUCCION; descargar el diseño"),
        ("6", "Cliente", "Campana con el aviso y línea de tiempo en «Mis pedidos»"),
        ("7", "API", "Swagger: 409 por stock y 422 por zona inválida"),
    ]
    for i, (n, t, d) in enumerate(pasos):
        y = 1.7 + i * 0.7
        chip(s, 0.8, y + 0.08, 0.44, 0.44, n, color=ACCENT, size=12)
        texto(s, 1.45, y, 2.4, 0.6, t, size=14, color=ROSE, bold=True, anchor=M)
        texto(s, 3.85, y, 4.6, 0.6, d, size=11.5, color=CREAM, anchor=M, interlineado=1.15)
    figura(s, "capturas/C18_detalle_admin.png", x=8.75, y=1.65, ancho_max=3.9, alto_max=4.6)
    texto(s, 0.8, 6.75, 11.5, 0.35, "Todo corre en local · datos ficticios del perfil demo · tarjetas de prueba "
          "4111 1111 1111 1111 y 4000 0000 0000 0002", size=10, color=MUTED_LIGHT, italic=True)


# ------------------------------------------------------------- 24 conclusiones
def conclusiones(prs):
    s = lamina(prs)
    cabecera(s, "7 · Conclusiones", "Lo que demuestra el proyecto")
    items = [
        ("Ataca la causa raíz. ", "El problema era la falta de canal propio (D1); la plataforma lo resuelve."),
        ("Sin sobreventa por diseño. ", "Stock por variante y reserva atómica en la transacción."),
        ("La propuesta de valor es software. ", "Personalizar, ver y cotizar una docena con tallas mezcladas, en segundos."),
        ("El servidor manda. ", "Recalcula precios y stock; la base protege sus reglas con CHECK e índices únicos."),
        ("Cuatro patrones, comprobables. ", "Cliente-servidor, MVC, capas y eventos están en el código, no solo en el papel."),
        ("Calidad con evidencia. ", "73 pruebas, Postman y la historia de referencia en el navegador."),
    ]
    for i, (a, b) in enumerate(items):
        fila, col = divmod(i, 2)
        x = 0.7 + col * 6.05
        y = 1.65 + fila * 1.68
        caja(s, x, y, 5.85, 1.45, color=CARD, borde=LINE)
        chip(s, x + 0.25, y + 0.25, 0.42, 0.42, str(i + 1), color=PRIMARY, size=12)
        texto(s, x + 0.85, y + 0.22, 4.8, 1.1, a + b, size=11.5, color=TEXT, interlineado=1.3)


# ----------------------------------------------------------- 25 trabajo futuro
def futuro(prs):
    s = lamina(prs)
    cabecera(s, "7 · Recomendaciones", "Trabajo futuro")
    items = [
        ("Pasarela real", "Otra implementación de PaymentGateway (Mercado Pago, Culqi o Izipay) con webhook "
         "firmado e idempotente.", PRIMARY),
        ("Expiración", "@Scheduled cancela los pedidos pendientes de pago y repone el stock.", ACCENT),
        ("Despliegue", "Frontend en Vercel (vercel.mjs listo) y backend en un servicio con el JAR.", BLUE),
        ("Correo", "EmailListener como tercer suscriptor del evento, sin tocar los servicios.", GREEN),
        ("Backlog", "Cupones, favoritos, reseñas y banners (dos tablas ya existen).", GOLD),
        ("Indicadores", "Ventas por periodo y tiempo por etapa desde el historial y la auditoría.", PRIMARY),
    ]
    for i, (t, c, color) in enumerate(items):
        fila, col = divmod(i, 3)
        tarjeta(s, 0.7 + col * 4.05, 1.65 + fila * 2.55, 3.78, 2.3, t, c, color=color, size_c=10.5)


# ------------------------------------------------------------------ 26 cierre
def cierre(prs):
    s = lamina(prs, DARK)
    caja(s, 10.2, -1.6, 4.8, 4.8, color=PRIMARY, forma=MSO_SHAPE.OVAL)
    caja(s, 11.6, 4.9, 3.4, 3.4, color=ACCENT, forma=MSO_SHAPE.OVAL)
    texto(s, 0.8, 1.2, 9.5, 0.3, "CORAL SHOP  ·  GRUPO 1", size=11, color=ACCENT, bold=True, spc=200)
    texto(s, 0.8, 1.7, 9.5, 1.2, "Diseña tu estilo,\nestampa tu idea.", size=44, color=CREAM, bold=True,
          font=TITULO, interlineado=1.1)
    texto(s, 0.8, 3.6, 9.5, 0.5, "Gracias.  ¿Preguntas?", size=24, color=ROSE, bold=True, font=TITULO)
    texto(s, 0.8, 4.6, 10.0, 1.0, "  ·  ".join(CONT.INTEGRANTES), size=13, color=CREAM, interlineado=1.3)
    texto(s, 0.8, 5.6, 10.0, 0.4, "Repositorio: github.com/diegoaaron/desarrollo_web", size=12,
          color=MUTED_LIGHT)


def notas(slide, expositor, contenido):
    marco = slide.notes_slide.notes_text_frame
    marco.text = f"EXPOSITOR: {expositor}\n\n{contenido.strip()}"


LAMINAS = [portada_final, agenda, empresa, canvas, pestel, foda, ishikawa, problematica, objetivos,
           solucion, modulos, personalizador, casos_uso, tecnologias, arquitectura, cs_mvc, capas_flujo,
           estados, eventos, datos, implementacion, pruebas, demo, conclusiones, futuro, cierre]


def main():
    prs = nueva_presentacion()
    assert len(LAMINAS) == len(NOTAS), "cada lámina necesita sus notas del orador"
    for f, (expositor, contenido) in zip(LAMINAS, NOTAS):
        f(prs)
        notas(prs.slides[len(prs.slides._sldIdLst) - 1], expositor, contenido)
    total = len(prs.slides._sldIdLst)
    for i, slide in enumerate(prs.slides, start=1):
        if i not in (1, total) and LAMINAS[i - 1] is not demo:
            numero(slide, i, total)
    prs.save(SALIDA)
    print(f"Presentación generada ({total} láminas):", SALIDA)


if __name__ == "__main__":
    main()
