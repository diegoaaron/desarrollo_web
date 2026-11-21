# -*- coding: utf-8 -*-
"""Genera clase_entregables/Informe_Proyecto_Final_Coral_Shop.docx (informe final)."""

import os

from PIL import Image

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches, Cm

import contenido as C
import esquema
from docx_util import (
    FIGURAS, nuevo_documento, tabla, figura, figura_apaisada, indice, salto_pagina, parrafo, vineta,
    bloque_codigo, nota, seccion_horizontal, seccion_vertical,
    PRIMARY, ACCENT, BLUE, TEXT, MUTED, HEX_BLUE, HEX_ACCENT,
)

SALIDA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "clase_entregables", "Informe_Proyecto_Final_Coral_Shop.docx")

CENTRO = WD_ALIGN_PARAGRAPH.CENTER
IZQ = WD_ALIGN_PARAGRAPH.LEFT


def h(doc, nivel, texto):
    return doc.add_heading(texto, level=nivel)


# ============================================================== PORTADA
def caratula(doc, etiqueta="PROYECTO FINAL"):
    """Carátula común a los entregables: universidad, título, datos del curso y grupo."""
    for _ in range(2):
        doc.add_paragraph()
    parrafo(doc, "UNIVERSIDAD TECNOLÓGICA DEL PERÚ", size=16, bold=True,
            color=PRIMARY, align=CENTRO, space_after=2)
    parrafo(doc, f"Facultad de Ingeniería  ·  {C.CARRERA}", size=12,
            color=MUTED, align=CENTRO, space_after=36)

    parrafo(doc, etiqueta, size=11, bold=True, color=ACCENT, align=CENTRO,
            space_after=6)
    parrafo(doc, C.TITULO, size=20, bold=True, color=PRIMARY, align=CENTRO,
            space_after=6)
    parrafo(doc, f"Caso: {C.EMPRESA}", size=13, color=MUTED, align=CENTRO,
            space_after=30)

    filas = [
        ("Curso", C.CURSO),
        ("Docente", C.DOCENTE),
        ("Grupo", C.GRUPO),
        ("Integrantes", "\n".join(C.INTEGRANTES)),
        ("Año", C.CICLO),
    ]
    tabla(doc, ["Datos generales", ""], filas, anchos=[28, 72], size=11,
          zebra=False)

    parrafo(doc, "Lima - Perú", size=11, color=MUTED, align=CENTRO, space_after=0)
    salto_pagina(doc)


# ============================================================== utilidades
def captura(doc, archivo, pie, alto_max=7.2, ancho_max=6.3):
    """Inserta una captura real de la aplicación sin que exceda el alto de la página."""
    with Image.open(os.path.join(FIGURAS, "capturas", archivo)) as im:
        w, h_px = im.size
    ancho = min(ancho_max, alto_max * w / h_px)
    figura(doc, os.path.join("capturas", archivo), pie, ancho_pulgadas=round(ancho, 2))


# ================================================================ PORTADA
def portada(doc):
    caratula(doc)

    h(doc, 1, "Índice")
    indice(doc)
    salto_pagina(doc)

    n_tablas, _, _ = esquema.totales()
    h(doc, 1, "Resumen ejecutivo")
    parrafo(doc,
            "Coral Shop S.A.C. es una pequeña empresa limeña que produce y vende ropa juvenil (polos, poleras, "
            "gorras y tote bags) con estampado y bordado personalizados. Hoy vende solo por Instagram y "
            "WhatsApp, con el inventario en hojas de cálculo y la cotización del estampado hecha a mano. Esa "
            "forma de operar le cuesta pedidos perdidos, sobreventa de tallas y ausencia total de indicadores.")
    parrafo(doc,
            "Este proyecto diseñó e implementó una plataforma web de comercio electrónico a la medida de ese "
            "problema. El frontend es una aplicación de página única en React 19; el backend es una API REST en "
            "Spring Boot 3.5 con Java 21, organizada por funcionalidad y en tres capas (controller, service y "
            f"repository), sobre una base PostgreSQL 16 de {n_tablas} tablas versionada con Flyway. El núcleo "
            "diferenciador es el personalizador: el cliente elige técnica y zonas válidas para su prenda, sube su "
            "diseño, lo ve sobre la silueta y reparte la cantidad entre tallas y colores, con el descuento por "
            "mayor y el precio calculados por el servidor al instante.")
    parrafo(doc,
            "La solución aplica los cuatro patrones de arquitectura vistos en clase: cliente-servidor, MVC, capas "
            "y arquitectura dirigida por eventos (cada cambio de estado del pedido se audita y se avisa al cliente "
            "en una campana). Se verificó con 73 pruebas automatizadas, una colección Postman de toda la API y la "
            "historia de referencia recorrida en el navegador: 12 polos bordados con un logo en el pecho izquierdo "
            "(4 S, 4 M, 4 L) por S/ 591.60, pagados y seguidos hasta ENTREGADO.")
    nota(doc, "Alcance de esta versión",
         "La aplicación está completa y funciona en local (PostgreSQL en Docker, backend y frontend en el equipo "
         "de demostración). El pago es simulado detrás de una interfaz que permite conectar una pasarela real; "
         "la pasarela y el despliegue público quedan como trabajo futuro (sección 4.2). Todos los datos de la "
         "demo son ficticios.")
    salto_pagina(doc)


# ================================================ 1. DIAGNOSTICO
def seccion_1(doc):
    h(doc, 1, "1. Diagnóstico estratégico y análisis del negocio")

    h(doc, 2, "1.1 Nombre de la empresa")
    parrafo(doc,
            "La organización elegida es Coral Shop S.A.C., una empresa ficticia pero construida sobre un caso "
            "realista y frecuente en Lima. Opera desde 2021 con un local y taller propio en el distrito de "
            "Jesús María y una comunidad de aproximadamente 24 mil seguidores entre Instagram y TikTok. Su "
            "marca comercial es Coral Shop y su público es el joven urbano de 16 a 28 años.")
    parrafo(doc,
            "El negocio tiene dos líneas complementarias. La primera es la venta de prendas de catálogo: polos, "
            "poleras con capucha, gorras y tote bags de diseño propio. La segunda, y la que la distingue de "
            "cualquier tienda de ropa convencional, es la personalización: el cliente puede pedir que su prenda "
            "sea estampada con una imagen o un texto propio, eligiendo la zona, la técnica y el tamaño del "
            "estampado. Esa segunda línea representa hoy cerca del 45 % de las ventas y es, al mismo tiempo, la "
            "que más trabajo manual exige.")

    h(doc, 2, "1.2 Misión y visión")
    tabla(doc, ["", "Declaración"], [
        ("Misión",
         "Vestir la identidad de los jóvenes peruanos ofreciéndoles ropa urbana de calidad que pueden "
         "personalizar a su gusto, con precios accesibles, producción local responsable y una experiencia de "
         "compra simple y transparente."),
        ("Visión",
         "Ser en 2030 la primera marca peruana de ropa juvenil personalizable en línea, reconocida porque "
         "cualquier persona puede diseñar su propia prenda en minutos y recibirla en 72 horas en cualquier "
         "ciudad del país."),
        ("Valores",
         "Autenticidad, cercanía con la comunidad, cumplimiento de lo prometido, producción bajo demanda para "
         "evitar el desperdicio textil y respeto por el trabajo de quien diseña."),
    ], anchos=[16, 84], size=10.5, zebra=False)

    h(doc, 2, "1.3 Industria y tamaño de la organización")
    parrafo(doc,
            "Coral Shop pertenece al sector de comercio al por menor de prendas de vestir, con actividad "
            "complementaria de confección y estampado textil. En la Clasificación Industrial Internacional "
            "Uniforme le corresponde la clase 4771 (venta al por menor de prendas de vestir en comercios "
            "especializados). Compite en el segmento de moda urbana juvenil, un mercado fragmentado en el que "
            "conviven marcas de autor pequeñas, importadores de bajo costo y los grandes marketplaces.")
    tabla(doc, ["Indicador", "Valor", "Lectura"], [
        ("Años de operación", "5 (desde 2021)", "Negocio consolidado, ya no es un emprendimiento inicial."),
        ("Colaboradores", "12", "2 en administración, 3 en taller de estampado, 4 en producción y confección, "
         "2 en atención y redes, 1 en despacho."),
        ("Ventas anuales", "Aproximadamente S/ 1 800 000",
         "Supera las 150 UIT, por lo que se clasifica como pequeña empresa según la normativa peruana de la MYPE."),
        ("Pedidos mensuales", "Entre 550 y 900 según temporada",
         "La estacionalidad se concentra en marzo, julio y diciembre."),
        ("Ticket promedio", "S/ 78",
         "Sube a S/ 112 cuando el pedido incluye personalización."),
        ("Canal de venta actual", "Instagram, TikTok y WhatsApp",
         "No existe canal propio: la empresa no controla el medio por el que vende."),
        ("Cobertura", "Lima Metropolitana y envíos puntuales a provincia",
         "El envío a provincia se coordina hoy de forma manual, pedido por pedido."),
    ], anchos=[22, 24, 54], size=9.5)

    h(doc, 2, "1.4 Modelo de negocio: lienzo Canvas")
    parrafo(doc,
            "El lienzo Canvas resume cómo Coral Shop crea, entrega y captura valor. Su lectura deja ver por qué "
            "una plataforma propia no es un lujo sino una necesidad: la propuesta de valor completa depende de "
            "que el cliente pueda diseñar y ver su prenda antes de comprarla, y hoy no existe ningún canal que "
            "lo permita.")
    figura_apaisada(doc, "02_canvas.png", "Figura 1. Business Model Canvas de Coral Shop S.A.C.")
    parrafo(doc,
            "Tres bloques del lienzo se traducen directamente en requerimientos del sistema. La propuesta de "
            "valor exige el personalizador con vista previa y precio al instante (M03), el descuento por volumen "
            "repartible entre tallas (M04) y el stock real por talla y color (M02 y M11). El bloque de canales "
            "convierte la tienda en el canal principal y relega WhatsApp a la postventa, lo que obliga a que la "
            "compra sea completamente autónoma (M05 y M06). El bloque de relación con clientes exige cuenta con "
            "historial y avisos automáticos de cada cambio de estado (M07, M08 y M09).")

    h(doc, 2, "1.5 Análisis PESTEL")
    parrafo(doc,
            "El análisis del entorno se presenta articulado a las decisiones del proyecto: para cada factor se "
            "indica el hallazgo y la consecuencia concreta que tiene sobre la solución, de modo que el "
            "diagnóstico no quede como un ejercicio separado del diseño.")
    tabla(doc, ["Factor", "Hallazgo del entorno", "Implicancia para el proyecto"], C.PESTEL,
          anchos=[14, 43, 43], size=9)

    h(doc, 2, "1.6 Matriz FODA")
    figura_apaisada(doc, "11_foda.png", "Figura 2. Matriz FODA de Coral Shop.")
    parrafo(doc,
            "El diagnóstico se completa con la matriz cruzada, que es la que articula el FODA con los objetivos "
            "del proyecto: cada estrategia indica a qué objetivo específico da origen.")
    tabla(doc, ["Tipo de estrategia", "Estrategias derivadas y objetivo que sustentan"], C.FODA_CRUZADO,
          anchos=[22, 78], size=9)
    parrafo(doc,
            "La lectura cruzada muestra que la debilidad D1 (no existe canal de venta digital propio) es el "
            "cuello de botella del que dependen las demás: sin plataforma no se puede aprovechar la comunidad, "
            "ni automatizar la cotización, ni medir nada. Por eso el proyecto ataca primero esa debilidad.")

    h(doc, 2, "1.7 Diagrama de la problemática (Ishikawa)")
    parrafo(doc,
            "Para identificar las causas raíz del problema se aplicó el diagrama de causa-efecto de Ishikawa "
            "con el esquema de las seis M, adaptado al caso: método, tecnología, medición, mano de obra, "
            "materiales e insumos, y entorno.")
    figura_apaisada(doc, "01_ishikawa.png",
           "Figura 3. Diagrama de Ishikawa de la problemática de Coral Shop.")
    parrafo(doc,
            "El diagrama revela que las causas no están repartidas de forma pareja. Las ramas de tecnología, "
            "método y medición concentran las causas controlables por la empresa y todas apuntan al mismo "
            "vacío: no existe un sistema que sostenga la operación. La rama de entorno reúne causas que la "
            "empresa no controla pero que aumentan la urgencia. Las ramas de mano de obra y materiales son en "
            "buena medida consecuencia de las anteriores: se atiende uno a uno por chat porque no hay "
            "autoservicio, y no se reserva la prenda base porque no hay inventario en línea.")

    h(doc, 2, "1.8 Problemática central del negocio")
    nota(doc, "Problemática central",
         "Coral Shop no cuenta con un canal de venta digital propio ni con un sistema que integre catálogo, "
         "inventario por talla y color y pedidos personalizados. La operación depende de chats de Instagram y "
         "WhatsApp y de hojas de cálculo locales, lo que produce sobreventa de tallas, cotizaciones lentas del "
         "estampado, pérdida de pedidos y ausencia total de trazabilidad e indicadores para decidir.")
    parrafo(doc,
            "El problema se manifiesta en cifras concretas, obtenidas del registro de la propia empresa "
            "durante el último semestre. Se trata de datos simulados pero coherentes con la operación descrita, "
            "conforme a la recomendación de la consigna de no emplear datos sensibles reales.")
    tabla(doc, ["Manifestación del problema", "Situación actual", "Efecto en el negocio"], [
        ("Sobreventa de tallas", "12 % de los pedidos se cancela porque la talla vendida ya no existía",
         "Devoluciones, reprogramaciones y pérdida de confianza del cliente."),
        ("Cotización manual del estampado", "6 horas en promedio entre la consulta y la respuesta",
         "Se estima que 3 de cada 10 consultas de personalización se enfrían antes de responder."),
        ("Pedidos tomados por chat", "Sin formato estándar; datos dispersos en conversaciones",
         "Errores de tipeo en talla, color y dirección; reprocesos en el taller."),
        ("Inventario en hojas de cálculo", "Un archivo local por persona, sin sincronizar",
         "El catálogo publicado en redes no coincide con la existencia real."),
        ("Atención uno a uno", "Ventana de atención de 9 a 19 horas, días hábiles",
         "Se pierde la venta de la noche y del fin de semana, que es cuando compra el público joven."),
        ("Ausencia de indicadores", "No se registra conversión, pedidos perdidos ni rotación por talla",
         "Las decisiones de compra y de campaña se toman por intuición."),
        ("Mermas de estampado", "Sin aprobación formal del arte antes de producir",
         "Prendas perdidas por archivos de baja resolución o mal encuadrados."),
    ], anchos=[26, 38, 36], size=9)

    h(doc, 2, "1.9 Objetivo general del proyecto")
    nota(doc, "Objetivo general", C.OBJETIVO_GENERAL)

    h(doc, 2, "1.10 Objetivos específicos")
    parrafo(doc,
            "Los objetivos específicos se formulan con un indicador y una meta verificable, y se enlazan con "
            "los módulos funcionales (sección 2.1.4) que los hacen posibles. Esa última columna garantiza que el "
            "diagnóstico, los objetivos y el diseño de la solución sean un solo hilo y no tres documentos "
            "distintos.")
    tabla(doc, ["Cod.", "Objetivo específico", "Indicador", "Meta", "Módulos"],
          C.OBJETIVOS_ESPECIFICOS, anchos=[7, 38, 22, 16, 17], size=9)
    salto_pagina(doc)


# ================================================ 2. DISEÑO DE LA SOLUCIÓN
def seccion_2(doc):
    h(doc, 1, "2. Diseño de la solución")

    h(doc, 2, "2.1 Propuesta de solución")

    h(doc, 3, "2.1.1 Descripción general")
    parrafo(doc,
            "La solución es una tienda en línea de prendas personalizables compuesta por dos aplicaciones que se "
            "comunican por una API REST: la tienda y el panel de administración, construidos en React, y el "
            "servidor, construido en Spring Boot, que concentra las reglas del negocio, la seguridad y el acceso "
            "a PostgreSQL.")
    parrafo(doc,
            "Tres decisiones de diseño la distinguen de una tienda genérica. La primera es que el stock vive en "
            "la variante (producto, talla y color), la única forma de dejar de vender tallas que no hay. La "
            "segunda es el personalizador: las zonas y técnicas permitidas dependen del tipo de prenda y el "
            "precio se calcula al instante, sin esperar a que nadie responda un chat. La tercera es la compra por "
            "mayor: un mismo diseño se reparte entre tallas y colores y alcanza el descuento de su escala, que es "
            "como compran las promociones y los equipos.")

    h(doc, 3, "2.1.2 Alcance de la solución")
    tabla(doc, ["Incluido e implementado", "Fuera del alcance (trabajo futuro)"], [
        ("Catálogo con filtros por tipo y categoría, búsqueda y paginación en el servidor; ficha con stock real "
         "por variante.",
         "Pasarela de pagos real (Mercado Pago, Culqi o Izipay). Hoy el pago es simulado detrás de la interfaz "
         "PaymentGateway."),
        ("Personalizador: técnica, zonas válidas con recargo, subida del diseño, vista previa y conservación del "
         "borrador al iniciar sesión.",
         "Despliegue público. La aplicación se ejecuta y se demuestra en local."),
        ("Mayoreo: reparto por tallas y colores y escalas de 3, 6 y 12 unidades con 5 %, 10 % y 15 % de "
         "descuento.",
         "Facturación electrónica ante SUNAT y comprobantes formales."),
        ("Carrito por diseño, checkout con envío y dirección, pedido transaccional y pago simulado.",
         "Correo electrónico al cliente; hoy los avisos llegan a la campana de la tienda."),
        ("Cuenta, direcciones, «Mis pedidos» con línea de tiempo y campana de notificaciones.",
         "Cupones, favoritos, reseñas y banners administrables (backlog)."),
        ("Panel: tablero, productos y variantes, categorías, bandeja de pedidos con máquina de estados, "
         "descarga del diseño, usuarios y roles, auditoría automática.",
         "Recuperación de contraseña por correo y aplicación móvil nativa (la web es responsiva)."),
    ], anchos=[55, 45], size=9)
    parrafo(doc,
            "Las exclusiones son integraciones con terceros que no cambian la arquitectura: la interfaz "
            "PaymentGateway y el evento OrderStatusChanged ya dejan preparados los puntos donde se conectarían la "
            "pasarela y el correo.")

    h(doc, 3, "2.1.3 Actores del sistema")
    tabla(doc, ["Actor", "Descripción", "Qué puede hacer"], C.ACTORES,
          anchos=[15, 25, 60], size=9)

    h(doc, 3, "2.1.4 Características de la tienda virtual: mapa de módulos")
    parrafo(doc,
            "Las funcionalidades se agrupan en 12 módulos repartidos en cuatro dominios: la tienda, la compra, el "
            "área del cliente y la administración. Todos están implementados y verificados.")
    figura_apaisada(doc, "07_modulos.png", "Figura 4. Mapa funcional de la tienda virtual.")
    tabla(doc, ["Cód.", "Módulo", "Dominio", "Qué resuelve", "Requerimientos"], C.MODULOS,
          anchos=[7, 18, 14, 45, 16], size=9)

    h(doc, 3, "2.1.5 Requerimientos funcionales")
    parrafo(doc,
            "Cada módulo se descompone en requerimientos verificables. Los de prioridad alta son los que la "
            "tienda necesita para vender; todos están implementados.")
    tabla(doc, ["Cód.", "Mód.", "Descripción", "Prior.", "Actor"], C.RF,
          anchos=[8, 7, 61, 8, 16], size=8.5)

    h(doc, 3, "2.1.6 Historias de usuario y criterios de aceptación")
    parrafo(doc,
            "Las historias describen las funcionalidades críticas desde quien las usa, con criterios en formato "
            "dado-cuando-entonces para que no haya ambigüedad sobre cuándo están terminadas. Las cinco primeras "
            "cubren el personalizador y el mayoreo, el corazón del negocio; los valores de los ejemplos son los "
            "que devuelve la aplicación real.")
    tabla(doc, ["Cód.", "Mód.", "Historia de usuario", "Criterios de aceptación"], C.HISTORIAS,
          anchos=[7, 6, 40, 47], size=8.5)

    h(doc, 3, "2.1.7 Casos de uso")
    figura_apaisada(doc, "05_casos_uso.png",
                    "Figura 5. Diagrama de casos de uso: actores y funcionalidades implementadas.")
    parrafo(doc,
            "Se detalla el caso de uso más crítico, porque involucra más reglas de negocio y la única transacción "
            "que escribe en cinco tablas a la vez.")
    tabla(doc, ["Campo", "CU-07: Confirmar el pedido (checkout)"], [
        ("Actor principal", "Cliente"),
        ("Actor secundario", "Sistema (recálculo de precios, reserva de stock, evento de dominio)"),
        ("Precondiciones", "El cliente inició sesión y su carrito tiene al menos una línea válida con su diseño "
         "subido."),
        ("Postcondiciones", "Existe un pedido CS-… en PENDIENTE_PAGO con sus líneas, zonas, reparto por tallas y "
         "primer registro del historial; el stock de cada variante quedó reservado; hay un registro en audit_log "
         "y un aviso para el cliente; el carrito queda vacío."),
        ("Flujo principal",
         "1. El cliente abre el checkout desde el carrito; el sistema recotiza las líneas.\n"
         "2. El cliente elige el método de envío; el sistema suma su costo al total.\n"
         "3. Si el envío es a domicilio, el cliente elige una dirección guardada o registra una nueva.\n"
         "4. El cliente agrega una nota opcional para el taller y confirma.\n"
         "5. El sistema valida el formato (CreateOrderRequest) y abre la transacción.\n"
         "6. El sistema comprueba que cada producto esté activo y sea personalizable, que cada zona admita la "
         "técnica para ese tipo de prenda, que el diseño sea del cliente y que el reparto sume la cantidad.\n"
         "7. El sistema recalcula los precios y aplica la escala de mayoreo de cada línea.\n"
         "8. El sistema descuenta el stock de cada variante con una actualización condicional.\n"
         "9. El sistema graba el pedido y publica OrderStatusChanged; se confirma la transacción.\n"
         "10. El sistema responde 201 con el código del pedido y la tienda abre el formulario de pago."),
        ("Flujo alterno A: formato inválido",
         "En el paso 5, si faltan datos o el teléfono no tiene formato válido, responde 400 con el error de cada "
         "campo y no toca la base."),
        ("Flujo alterno B: regla violada",
         "En el paso 6, si una zona no admite la técnica, el diseño es ajeno o el reparto no suma, responde 422 "
         "con el motivo."),
        ("Flujo alterno C: stock insuficiente",
         "En el paso 8, si una talla no alcanza, la transacción se deshace completa (incluido el stock ya "
         "descontado de otras líneas) y responde 409 indicando la variante."),
        ("Reglas aplicadas", "RN-01 a RN-09, RN-12 a RN-14"),
        ("Requerimientos", "RF-15 a RF-18"),
    ], anchos=[18, 82], size=9, zebra=False)

    h(doc, 3, "2.1.8 Requerimientos no funcionales")
    tabla(doc, ["Cód.", "Atributo", "Requerimiento"], C.RNF, anchos=[9, 16, 75], size=9)

    h(doc, 3, "2.1.9 Reglas de negocio")
    parrafo(doc,
            "Las reglas se hacen cumplir en la capa de servicio (y, cuando es posible, también en la base de "
            "datos), nunca solo en el frontend, porque el navegador no es de confianza.")
    tabla(doc, ["Cód.", "Regla"], C.REGLAS, anchos=[9, 91], size=9)

    # -------------------------------------------------------- 2.2
    h(doc, 2, "2.2 Tecnologías utilizadas")
    parrafo(doc,
            "La consigna pide justificar las decisiones técnicas con la teoría vista en clase. La última columna "
            "indica la sesión que sustenta cada elección.")
    tabla(doc, ["Capa o función", "Tecnología", "Justificación", "Sustento en clase"], C.TECNOLOGIAS,
          anchos=[15, 21, 46, 18], size=8.5)

    h(doc, 3, "2.2.1 Por qué Spring Boot y no Servlets escritos a mano")
    parrafo(doc,
            "El primer entregable planteó Servlets, JDBC y un Tomcat externo. Al implementar se eligió Spring "
            "Boot, sin abandonar esos conceptos: Spring MVC es una capa sobre la API de Servlets. Toda petición "
            "entra por un Servlet, el DispatcherServlet, que cumple el rol de controlador frontal y reparte el "
            "trabajo a los @RestController; Tomcat sigue siendo el contenedor web, solo que embebido en la "
            "aplicación; y JdbcTemplate ejecuta JDBC con PreparedStatement, ahorrando la apertura y el cierre "
            "manual de conexiones.")
    parrafo(doc,
            "La ganancia es que el equipo dedica el tiempo a las reglas del negocio (precios, mayoreo, stock, "
            "estados) y no a infraestructura repetitiva: la seguridad (sesión, CSRF, roles), la validación con "
            "@Valid, las transacciones con @Transactional y los eventos ya vienen resueltos y probados.")
    tabla(doc, ["Concepto de clase", "Cómo aparece en Coral Shop"], [
        ("Servlet como Controlador (S01)", "DispatcherServlet + @RestController por recurso"),
        ("Contenedor web (S02)", "Tomcat embebido en Spring Boot, puerto 8082"),
        ("JDBC y PreparedStatement (S03)", "JdbcTemplate con parámetros ?; SQL solo en los @Repository"),
        ("Transacción con commit y rollback (S03)", "@Transactional en el service: todo o nada"),
        ("Session scope y JSESSIONID (Clase 4)", "Sesión de Spring Security con la cookie JSESSIONID"),
        ("JavaBean como Modelo (S01)", "Records inmutables y la entidad User de JPA"),
        ("JSP como Vista (Clase 4)", "React en el navegador; el controlador responde JSON"),
    ], anchos=[38, 62], size=9)

    # -------------------------------------------------------- 2.3
    h(doc, 2, "2.3 Arquitectura de la solución")
    parrafo(doc,
            "La arquitectura combina los cuatro patrones vistos en clase, cada uno a un nivel distinto: "
            "cliente-servidor describe qué corre dónde; MVC, cómo interactúa el usuario; las capas, cómo se "
            "organiza el servidor; y los eventos, cómo reacciona el sistema a los hechos del negocio. La Figura 6 "
            "los reúne.")
    figura_apaisada(doc, "03_arquitectura.png",
                    "Figura 6. Arquitectura de la solución: cliente-servidor en capas con Spring Boot y React.")

    h(doc, 3, "2.3.1 Cliente-servidor")
    parrafo(doc,
            "Hay un único servidor que concentra los datos y las reglas, y varios clientes que le piden "
            "servicios: la tienda, el panel de administración y las herramientas de prueba (Swagger y Postman). "
            "Solo el servidor habla con PostgreSQL, así que ningún cliente puede fijar un precio ni prometer stock "
            "que no existe.")
    figura(doc, "A2_03_cliente_servidor.png", "Figura 7. Arquitectura cliente-servidor de Coral Shop.",
           ancho_pulgadas=6.3)
    tabla(doc, ["Aspecto", "Decisión", "Por qué"], [
        ("Protocolo", "HTTP con cuerpos JSON en /api/…", "El navegador, Swagger y Postman usan el mismo contrato."),
        ("Sesión", "Cookie JSESSIONID emitida por Spring Security", "El rol viaja en la sesión del servidor, no "
         "en el navegador."),
        ("CSRF", "Token en la cabecera X-CSRF-TOKEN en todo POST, PUT, PATCH y DELETE",
         "Impide que otra página envíe peticiones con la sesión del usuario."),
        ("Confianza", "El servidor recalcula precios y stock", "El navegador puede manipularse."),
        ("Avisos", "La campana consulta /api/notifications/me cada 30 s y al volver a la pestaña",
         "En cliente-servidor el cliente pregunta; el servidor no inicia la conversación."),
        ("Mismo origen", "El proxy de Vite reenvía /api al servidor", "La cookie y el CSRF funcionan sin "
         "configurar CORS."),
    ], anchos=[14, 44, 42], size=9)

    h(doc, 3, "2.3.2 Modelo-Vista-Controlador")
    parrafo(doc,
            "MVC se conserva con una adaptación: la Vista ya no es una JSP renderizada en el servidor sino React en "
            "el navegador, y el Controlador responde JSON en lugar de hacer forward. Por eso la misma API atiende "
            "a la tienda, al panel y a las pruebas automáticas.")
    figura(doc, "A2_04_mvc.png", "Figura 8. MVC con React como vista y Spring como controlador.",
           ancho_pulgadas=6.3)
    tabla(doc, ["Rol MVC", "En clase", "En Coral Shop"], [
        ("Modelo", "JavaBeans", "Records inmutables (ProductView, PricedLine, OrderDetailView), la entidad User y "
         "los servicios que aplican las reglas (PricingService, QuantityPolicy)"),
        ("Vista", "JSP", "Pantallas React en pages/ y features/: catálogo, personalizador, carrito, checkout, "
         "«Mis pedidos», campana y panel"),
        ("Controlador", "Servlet", "@RestController atendidos por el DispatcherServlet"),
    ], anchos=[14, 14, 72], size=9)
    parrafo(doc,
            "Ejemplo real: al marcar «pecho izquierdo» en el personalizador, la vista envía POST /api/quotes; "
            "QuoteController delega en PricingService, que calcula base + técnica + zona − descuento, y React "
            "redibuja el precio y la vista previa con el JSON recibido.")

    h(doc, 3, "2.3.3 Arquitectura en capas")
    parrafo(doc,
            "Dentro del servidor cada módulo tiene sus paquetes controller, service y repository, y cada capa "
            "solo conoce a la de abajo. Cada capa responde además con su propio código de error, de modo que el "
            "frontend sabe si el problema es de formato, de regla o de concurrencia.")
    tabla(doc, ["Capa", "Responsabilidad", "En Coral Shop", "Si algo falla"], [
        ("Presentación", "Recibir HTTP y validar el formato", "@RestController + DTO con @Valid", "400"),
        ("Negocio", "Aplicar las reglas en una transacción", "@Service + @Transactional (OrderService, "
         "PricingService, QuantityPolicy, OrderStatusPolicy)", "422 regla · 409 conflicto · 404 ajeno"),
        ("Datos", "Leer y escribir con parámetros", "@Repository con JdbcTemplate", "409 por restricción"),
    ], anchos=[14, 28, 38, 20], size=9)
    parrafo(doc,
            "La Figura 9 sigue la petición más compleja del sistema por todas las capas: la confirmación del "
            "pedido de 12 polos bordados.")
    figura_apaisada(doc, "04_flujo_peticion.png",
                    "Figura 9. Flujo de una petición: confirmación del pedido de la historia de referencia.")
    parrafo(doc,
            "Un único @RestControllerAdvice (GlobalExceptionHandler) traduce las excepciones de todas las capas a "
            "un JSON con la misma forma { status, message, errors }. Ejemplos reales: «La zona ESPALDA no admite "
            "bordado» (422), «Stock insuficiente para POLO-…-S (S, Blanco)» (409) o el detalle de un pedido ajeno "
            "(404, para no revelar que existe).")

    h(doc, 3, "2.3.4 Máquina de estados del pedido")
    figura_apaisada(doc, "06_estados_pedido.png",
                    "Figura 10. Máquina de estados del pedido y transiciones válidas.")

    h(doc, 3, "2.3.5 Arquitectura dirigida por eventos")
    parrafo(doc,
            "Cuando un pedido cambia de estado, quien lo cambia publica el evento OrderStatusChanged y dos "
            "suscriptores reaccionan sin que el publicador los conozca: AuditListener lo registra en audit_log "
            "dentro de la misma transacción (si la auditoría falla, el cambio se deshace) y NotificationListener "
            "crea el aviso para el cliente solo después de confirmada la transacción. Publican tres servicios: "
            "OrderService (pedido creado), PaymentService (pago aprobado) y OrderAdminService (cambio del "
            "administrador).")
    figura(doc, "12_flujo_eventos.png", "Figura 11. El evento OrderStatusChanged: publicadores, bus y suscriptores.",
           ancho_pulgadas=6.3)
    parrafo(doc,
            "Se usó el bus de eventos de Spring, dentro del mismo proceso, en lugar de un broker como Kafka o "
            "RabbitMQ: con un solo servidor y dos suscriptores da el mismo desacoplamiento sin infraestructura "
            "adicional. Un futuro envío de correo sería un tercer suscriptor, sin tocar ningún servicio existente. "
            "La clave única event_id hace la entrega idempotente.")

    h(doc, 3, "2.3.6 Patrones de diseño aplicados")
    tabla(doc, ["Patrón", "Dónde se aplica", "Qué problema resuelve"], [
        ("Front Controller", "DispatcherServlet", "Un solo punto de entrada para todas las peticiones."),
        ("Chain of Responsibility", "Cadena de filtros de Spring Security",
         "Sesión, CSRF y autorización se resuelven antes de llegar al controlador."),
        ("Repository", "Paquetes repository", "Aísla el SQL; los servicios no conocen la base."),
        ("DTO", "Paquetes dto (records)", "Desacopla la API de las tablas y no expone campos sensibles."),
        ("Strategy", "PaymentGateway → SimulatedPaymentGateway",
         "Cambiar a una pasarela real es agregar otra implementación, sin tocar PaymentService."),
        ("State (tabla de transiciones)", "OrderStatusPolicy", "Impide saltos de estado no permitidos (RN-10)."),
        ("Observer / Publish-Subscribe", "OrderStatusChanged con AuditListener y NotificationListener",
         "Nuevas reacciones sin modificar a quien publica."),
        ("Assembler", "OrderDetailAssembler", "Arma la vista del pedido desde varias consultas en un solo lugar."),
        ("Dependency Injection", "Constructores de controllers, services y repositories",
         "Componentes desacoplados y fáciles de probar."),
    ], anchos=[22, 33, 45], size=9)

    # -------------------------------------------------------- 2.4
    n_tablas, n_campos, n_fk = esquema.totales()
    h(doc, 2, "2.4 Diseño de la base de datos")
    parrafo(doc,
            f"El modelo relacional consta de {n_tablas} tablas, {n_campos} campos y {n_fk} claves foráneas, "
            f"agrupadas en {len(esquema.MODULOS)} módulos. Se crea con seis migraciones Flyway (V1 a V6) que se "
            "aplican solas al arrancar el backend, y los diagramas de este informe se generan desde la misma "
            "especificación que esas migraciones, así que no pueden desincronizarse.")
    figura_apaisada(doc, "10_er_global.png",
                    "Figura 12. Mapa global del modelo de datos agrupado por módulos.")
    parrafo(doc,
            "Los diagramas entidad-relación completos, con todos los campos y relaciones, están en el Anexo A. El "
            "diccionario de datos de la sección 2.4.3 detalla cada tabla.")

    h(doc, 3, "2.4.1 Decisiones de diseño del modelo")
    for texto, corte in [
        ("El stock vive en la variante. products guarda el modelo de prenda y product_variants cada combinación de "
         "talla y color con su SKU y su stock, con UNIQUE (product_id, size_id, color_id) y CHECK (stock >= 0).",
         "El stock vive en la variante."),
        ("Las reglas de personalización son datos. product_type_zones define, para cada tipo de producto, qué zona "
         "admite qué técnica, su medida máxima, su recargo y el recuadro de la vista previa. Cambiar un precio o "
         "abrir una zona nueva no exige programar.", "Las reglas de personalización son datos."),
        ("Una línea es un diseño. order_lines guarda el producto, la técnica, el diseño, la escala aplicada y los "
         "precios congelados; order_line_zones las zonas con su recargo, y order_items el reparto por talla y "
         "color. Así un paquete de 12 polos es una sola línea con tres ítems.", "Una línea es un diseño."),
        ("El pedido es inmutable. Nombre, SKU, talla, color, precios y la dirección completa se copian al comprar: "
         "editar el catálogo o la dirección después no altera los pedidos emitidos.", "El pedido es inmutable."),
        ("Los diseños se guardan en la base (bytea), con tipo, tamaño y hash SHA-256 validados por CHECK, para no "
         "depender del disco del servidor.", "Los diseños se guardan en la base"),
        ("Trazabilidad desde el modelo. order_status_history, payments (también los rechazados), audit_log y "
         "notifications registran todo lo que le pasa a un pedido.", "Trazabilidad desde el modelo."),
        ("La tabla de pedidos se llama orders porque order es palabra reservada de SQL.",
         "La tabla de pedidos se llama orders"),
    ]:
        vineta(doc, texto, corte)

    h(doc, 3, "2.4.2 Integridad, restricciones e índices")
    tabla(doc, ["Mecanismo", "Aplicación en el modelo"], [
        ("Claves primarias", "Clave sustituta en cada tabla (BIGSERIAL o SERIAL)."),
        ("Claves foráneas", f"{n_fk} relaciones; ON DELETE CASCADE solo en dependencias débiles (direcciones del "
         "usuario, imágenes del producto)."),
        ("Unicidad", "lower(email), sku, order_code, provider_reference, event_id; UNIQUE (product_type_id, "
         "zone_id, technique_id) y UNIQUE (order_line_id, variant_id)."),
        ("Índices únicos parciales", "Una sola dirección principal por usuario, una sola imagen principal por "
         "producto y un solo pago APROBADO por pedido."),
        ("Restricciones CHECK", "stock >= 0; total_amount = subtotal − discount_amount + shipping_cost; estado "
         "dentro de los siete válidos; técnica y diseño van juntos; diseño PNG/JPG de hasta 5 MB; descuento entre "
         "0 y 100 %; la dirección del pedido va completa o vacía."),
        ("Transacciones", "Crear el pedido, pagarlo y cambiar su estado son @Transactional; el stock se descuenta "
         "con UPDATE condicional y el pago bloquea el pedido con SELECT … FOR UPDATE."),
        ("Baja lógica", "Productos, variantes y usuarios se desactivan con is_active para no romper el histórico."),
    ], anchos=[22, 78], size=9)

    h(doc, 3, "2.4.3 Diccionario de datos")
    parrafo(doc, "Cada tabla del modelo con sus campos, tipos, llaves y significado.")
    for modulo_id, (nombre_mod, _color) in esquema.MODULOS.items():
        tablas_mod = [t for t in esquema.TABLAS if t["modulo"] == modulo_id]
        h(doc, 4, f"Módulo: {nombre_mod}")
        for t in tablas_mod:
            parrafo(doc, t["nombre"], size=11, bold=True, color=BLUE, align=IZQ, space_after=1)
            parrafo(doc, t["desc"], size=9.5, italic=True, color=MUTED, space_after=3)
            filas = [(c[0], c[1], c[2] if c[2] else "-", c[3]) for c in t["campos"]]
            tabla(doc, ["Campo", "Tipo", "Llave", "Descripción"], filas,
                  anchos=[19, 17, 18, 46], size=8.5)
            if t.get("restricciones"):
                parrafo(doc, "Restricciones adicionales: " + "; ".join(t["restricciones"]),
                        size=9, italic=True, color=ACCENT, space_after=10)
    salto_pagina(doc)


# ================================================ 3. IMPLEMENTACIÓN
def seccion_3(doc):
    h(doc, 1, "3. Implementación")

    h(doc, 2, "3.1 Estructura de paquetes")
    parrafo(doc,
            "El backend se organiza por funcionalidad y, dentro de cada una, por capa: 17 paquetes de primer "
            "nivel y 131 clases, sin ningún paquete que mezcle capas. El frontend sigue la misma idea: cada "
            "funcionalidad tiene su carpeta en features/ con su api, sus hooks y sus componentes, y todas usan un "
            "único cliente HTTP.")
    bloque_codigo(doc, C.ARBOL_PAQUETES, size=7.5)
    parrafo(doc,
            "La dependencia es unidireccional: controller → service → repository. Un repository no conoce al "
            "servicio que lo usa y un servicio no sabe si lo llama un controller o una prueba; por eso las reglas "
            "puras (QuantityPolicy, OrderStatusPolicy, el cálculo de importes) se prueban sin levantar Spring ni "
            "la base de datos.")

    h(doc, 2, "3.2 Clases utilizadas en la aplicación")
    tabla(doc, ["Capa / paquete", "Clases principales", "Responsabilidad"], C.CLASES,
          anchos=[14, 50, 36], size=8.5)

    h(doc, 3, "3.2.1 Aplicación de la programación orientada a objetos")
    for texto, corte in [
        ("Encapsulamiento: los records exponen sus datos solo por métodos de acceso y son inmutables; la entidad "
         "User tiene atributos privados. Ninguna clase tiene atributos públicos mutables.", "Encapsulamiento:"),
        ("Abstracción: PaymentGateway es una interfaz; PaymentService depende de ella y no de la implementación "
         "simulada.", "Abstracción:"),
        ("Polimorfismo: en ejecución se inyecta SimulatedPaymentGateway; una pasarela real sería otra "
         "implementación intercambiable por configuración.", "Polimorfismo:"),
        ("Herencia: las excepciones de negocio extienden RuntimeException y el manejador global las traduce por "
         "su tipo a 404, 409 o 422.", "Herencia:"),
        ("Composición: OrderService no hereda de nadie; compone PricingService, QuantityPolicy, los repositories "
         "y el publicador de eventos dentro de una sola transacción.", "Composición:"),
    ]:
        vineta(doc, texto, corte)

    h(doc, 2, "3.3 Funcionalidades implementadas")
    parrafo(doc,
            "Las capturas siguientes son de la aplicación real ejecutándose en local con los datos ficticios del "
            "perfil demo, recorriendo la historia de referencia. El Anexo B reúne todas las pantallas.")

    h(doc, 3, "3.3.1 Personalizador y mayoreo")
    parrafo(doc,
            "El cliente elige color, técnica y zonas (solo las válidas para el polo y la técnica), sube su logo y lo "
            "ve sobre la silueta. En la tabla reparte 4 S, 4 M y 4 L; el sistema reconoce la escala de docena y "
            "muestra el desglose calculado por el servidor: S/ 35.00 de prenda base + S/ 15.00 de bordado + "
            "S/ 8.00 de pecho izquierdo = S/ 58.00 por unidad; × 12 = S/ 696.00; −15 % = S/ 591.60.")
    captura(doc, "C04_personalizador.png",
            "Figura 13. Personalizador: bordado en el pecho izquierdo, reparto por tallas y precio de docena.")

    h(doc, 3, "3.3.2 Compra: checkout y pago simulado")
    parrafo(doc,
            "En el checkout el cliente elige el envío y la dirección; al confirmar, el servidor crea el pedido en "
            "una transacción y la tienda abre el pago. La tarjeta 4000 0000 0000 0002 se rechaza (queda registrado "
            "y el pedido sigue pendiente) y la 4111 1111 1111 1111 se aprueba y pasa el pedido a PAGADO.")
    captura(doc, "C06_checkout.png", "Figura 14. Checkout: método de envío, dirección y resumen.")
    captura(doc, "C08_pago_rechazado.png", "Figura 15. Pago simulado rechazado con opción de reintentar.")

    h(doc, 3, "3.3.3 Seguimiento y notificaciones")
    parrafo(doc,
            "«Mis pedidos» muestra el historial y el detalle con la línea de tiempo de estados; la campana avisa "
            "cada cambio de estado.")
    captura(doc, "C11_detalle_pedido.png", "Figura 16. Detalle de un pedido entregado con su línea de tiempo.")
    captura(doc, "C12_campana.png", "Figura 17. Campana de notificaciones con los avisos del cliente.")

    h(doc, 3, "3.3.4 Panel de administración")
    parrafo(doc,
            "El administrador ve el tablero, gestiona el catálogo y atiende la bandeja de pedidos. En el detalle "
            "descarga el diseño, revisa los pagos (incluido el rechazado) y solo puede elegir los estados "
            "permitidos; el historial muestra quién hizo cada cambio.")
    captura(doc, "C13_tablero.png", "Figura 18. Tablero del administrador.")
    captura(doc, "C18_detalle_admin.png",
            "Figura 19. Detalle del pedido en el panel: diseño, pagos, cambio de estado e historial.")

    h(doc, 3, "3.3.5 Interfaz de programación (API REST)")
    parrafo(doc,
            "La API se documenta sola con Swagger UI en /api/docs y se prueba con la colección Postman de "
            "backend/postman/, que recorre la historia de referencia completa (cliente y administrador) y los "
            "errores esperados.")
    tabla(doc, ["Método", "Ruta", "Acceso", "Descripción", "Controller"], C.ENDPOINTS,
          anchos=[11, 29, 12, 27, 21], size=8)

    h(doc, 2, "3.4 Algoritmos y estructuras de datos implementados")
    parrafo(doc,
            "Cada estructura se eligió por la operación que se ejecuta sobre ella con más frecuencia o por la "
            "garantía que debe dar.")
    tabla(doc, ["Propósito", "Estructura o algoritmo", "Justificación", "Dónde"], C.ALGORITMOS,
          anchos=[18, 25, 40, 17], size=8.5)

    h(doc, 2, "3.5 Pruebas y verificación")
    tabla(doc, ["Verificación", "Alcance", "Resultado"], [
        ("Pruebas unitarias (JUnit 5)", "QuantityPolicy, importes de línea, PricingService (historia de "
         "referencia y cada regla de rechazo), OrderStatusPolicy, detección de imagen, pasarela simulada y entrega "
         "del evento", "En verde"),
        ("Integración (Testcontainers + PostgreSQL 16)", "Creación del pedido: 201 y descuento de stock; 409 que "
         "deshace también el stock de otra línea; 400 con errores por campo", "En verde"),
        ("Seguridad", "Pedido, diseño y pago ajenos → 404; diseño ajeno en un pedido → 422; rutas de admin → 403; "
         "sin sesión → 401; sin CSRF → 403", "En verde"),
        ("Datos demo", "El perfil demo carga 8 productos, 5 clientes y 8 pedidos pasando por las mismas reglas de "
         "la API", "En verde"),
        ("Total", "Suite completa con ./mvnw test", "73 de 73"),
        ("Postman (Newman)", "39 peticiones de la historia de referencia y sus errores", "38 aserciones en verde"),
        ("Navegador", "Historia de referencia de punta a punta en la tienda y el panel", "Completa"),
    ], anchos=[26, 56, 18], size=9)
    salto_pagina(doc)


# ================================================ 4. CONCLUSIONES
def seccion_4(doc):
    h(doc, 1, "4. Conclusiones y recomendaciones")

    h(doc, 2, "4.1 Conclusiones")
    for c in [
        "El diagnóstico mostró que el problema de Coral Shop no es de demanda sino de infraestructura: el Ishikawa "
        "concentró las causas controlables en tecnología, método y medición, y el FODA cruzado señaló la falta de "
        "canal propio (D1) como la debilidad de la que dependen las demás. La plataforma ataca esa causa raíz.",
        "Guardar el stock por variante y descontarlo con una actualización condicional dentro de la transacción "
        "elimina la sobreventa por diseño, no por disciplina: si dos clientes compran la última unidad, solo uno "
        "lo consigue y el otro recibe un mensaje claro.",
        "El personalizador con zonas por tipo de prenda y el mayoreo repartible entre tallas son la propuesta de "
        "valor convertida en software. Ningún marketplace permite componer el diseño, verlo sobre la prenda y "
        "conocer al instante el precio de una docena con tallas mezcladas; la cotización pasa de horas a segundos.",
        "Que el servidor recalcule siempre precios y stock, y que la base proteja sus reglas con CHECK e índices "
        "únicos, hace que la tienda sea segura aunque el navegador se manipule.",
        "Los cuatro patrones de arquitectura de clase conviven en el código y se pueden comprobar: cliente-servidor "
        "en el despliegue, MVC en la interacción, capas en los paquetes (ningún controller toca la base) y eventos "
        "en la auditoría y los avisos, que se agregaron sin modificar el flujo de pedidos.",
        "Spring Boot no reemplazó los conceptos de clase sino que los empaquetó: el DispatcherServlet es un "
        "Servlet, Tomcat sigue siendo el contenedor web y JdbcTemplate es JDBC con PreparedStatement. Eso permitió "
        "dedicar el esfuerzo a las reglas del negocio.",
        "La calidad se demostró con evidencia: 73 pruebas automatizadas (las de integración, contra un PostgreSQL real), la "
        "colección Postman y la historia de referencia recorrida en el navegador.",
    ]:
        vineta(doc, c)

    h(doc, 2, "4.2 Recomendaciones y trabajo futuro")
    for texto, corte in [
        ("Pasarela de pago real. Agregar una implementación de PaymentGateway para Mercado Pago, Culqi o Izipay en "
         "modo sandbox, elegida por configuración, con un webhook que verifique la firma del proveedor, sea "
         "idempotente (provider_reference único) y solo entonces pase el pedido a PAGADO. Las claves deben vivir "
         "en variables de entorno y nunca guardarse datos de tarjeta.", "Pasarela de pago real."),
        ("Expiración de pedidos pendientes. Una tarea programada (@Scheduled) que cancele los pedidos en "
         "PENDIENTE_PAGO después de N minutos y reponga su stock, para no bloquear tallas indefinidamente.",
         "Expiración de pedidos pendientes."),
        ("Despliegue. Publicar el frontend en Vercel (frontend/vercel.mjs ya lee la variable BACKEND_URL) y el "
         "backend en un servicio que ejecute el JAR con las variables de la base de datos, sin el perfil dev.",
         "Despliegue."),
        ("Correo al cliente. Sumar un EmailListener como tercer suscriptor de OrderStatusChanged; no requiere tocar "
         "OrderService, PaymentService ni OrderAdminService.", "Correo al cliente."),
        ("Backlog comercial. Cupones, favoritos, reseñas de compradores verificados y banners administrables "
         "(las tablas favorites y banners ya existen).", "Backlog comercial."),
        ("Indicadores. Ampliar el tablero con ventas por periodo, rotación por talla y tiempo promedio por etapa, a "
         "partir de order_status_history y audit_log.", "Indicadores."),
        ("Proceso. Mantener la regla de una migración Flyway nueva por cada cambio de esquema y ejecutar las pruebas "
         "en cada pull request para no romper lo ya entregado.", "Proceso."),
    ]:
        vineta(doc, texto, corte)
    salto_pagina(doc)


# ================================================ 5. ANEXOS
CAPTURAS_ANEXO = [
    ("C01_inicio.png", "Portada de la tienda."),
    ("C02_catalogo.png", "Catálogo con filtro por tipo de producto (M01)."),
    ("C03_ficha.png", "Ficha del producto antes de personalizar (M02)."),
    ("C05_carrito.png", "Carrito con una línea por diseño repartida entre tallas (M05)."),
    ("C07_pago.png", "Formulario de pago simulado (M06)."),
    ("C09_confirmacion.png", "Confirmación del pedido pagado (M06)."),
    ("C10_mis_pedidos.png", "Mis pedidos (M08)."),
    ("C14_productos_admin.png", "Panel: biblioteca de productos (M11)."),
    ("C15_producto_form.png", "Panel: alta de producto con variantes, tallas, colores y stock (M11)."),
    ("C16_categorias.png", "Panel: categorías (M11)."),
    ("C17_bandeja_pedidos.png", "Panel: bandeja de pedidos filtrable por estado (M12)."),
    ("C19_usuarios.png", "Panel: usuarios y roles (M10)."),
    ("C20_swagger.png", "Documentación de la API en Swagger UI (/api/docs)."),
]


def seccion_5(doc):
    h(doc, 1, "5. Anexos")

    h(doc, 2, "Anexo A. Modelo entidad-relación ampliado")
    parrafo(doc,
            "Modelo completo con todos los campos y sus relaciones, generado desde la misma especificación que "
            "las migraciones. La flecha parte del campo con la clave foránea y apunta al campo referenciado.")
    seccion_horizontal(doc)
    figura(doc, "08_er_usuarios_catalogo.png",
           "Figura A1. Modelo entidad-relación (1 de 2): usuarios, auditoría, catálogo e inventario.",
           ancho_pulgadas=9.0)
    salto_pagina(doc)
    figura(doc, "09_er_personalizacion_compra.png",
           "Figura A2. Modelo entidad-relación (2 de 2): personalización, mayoreo, pedidos, pagos y avisos.",
           ancho_pulgadas=9.0)
    seccion_vertical(doc)

    h(doc, 2, "Anexo B. Pantallas de la aplicación")
    parrafo(doc,
            "Capturas reales de la aplicación ejecutándose en local con datos ficticios (perfil demo). Se generan "
            "con scripts/capturas.py, que recorre la historia de referencia con un navegador automatizado. Las "
            "pantallas del personalizador, el checkout, el seguimiento y el detalle del administrador están en la "
            "sección 3.3.")
    for i, (archivo, pie) in enumerate(CAPTURAS_ANEXO, start=1):
        captura(doc, archivo, f"Figura B{i}. {pie}", alto_max=6.6)

    h(doc, 2, "Anexo C. Cronograma del proyecto")
    tabla(doc, ["Etapa", "Periodo", "Objetivo", "Entregables", "Estado"], C.CRONOGRAMA,
          anchos=[12, 13, 22, 40, 13], size=9)

    h(doc, 2, "Anexo D. Matriz de trazabilidad")
    parrafo(doc,
            "Enlaza cada objetivo específico con los módulos que lo realizan, los requerimientos que lo especifican "
            "y las tablas que lo soportan.")
    tabla(doc, ["Obj.", "Módulos", "Requerimientos", "Tablas principales"], [
        ("OE-1", "M01, M02, M05, M06, M07", "RF-01 a RF-05, RF-14 a RF-23",
         "products, product_variants, categories, product_types, orders, order_lines, order_items, payments, "
         "shipping_methods, users, addresses"),
        ("OE-2", "M03, M04", "RF-06 a RF-13",
         "customization_techniques, print_zones, product_type_zones, design_uploads, quantity_tiers"),
        ("OE-3", "M02, M04, M11", "RF-05, RF-11, RF-12, RF-30, RF-31",
         "product_variants, sizes, colors, quantity_tiers, order_items"),
        ("OE-4", "M08, M09, M10, M12", "RF-24 a RF-28, RF-33 a RF-36",
         "orders, order_status_history, notifications, audit_log"),
        ("OE-5", "M07, transversal", "RF-08, RF-19, RF-21, RF-22, RNF-01 a RNF-04",
         "users, roles, design_uploads, payments"),
        ("OE-6", "Transversal", "RNF-11, RNF-12, RNF-15", "Todas (migraciones V1 a V6)"),
    ], anchos=[7, 20, 27, 46], size=9)

    h(doc, 2, "Anexo E. Guía de la demostración")
    parrafo(doc,
            "La demo se ejecuta en local. La guía paso a paso para instalar y levantar el proyecto está en el "
            "README del repositorio; el resumen es:")
    bloque_codigo(doc,
                  "docker start coralshop-db                      # PostgreSQL 16 en Docker\n"
                  "IntelliJ → «Backend (demo)» + «Frontend»       # o desde la terminal:\n"
                  "  backend:  SPRING_PROFILES_ACTIVE=dev,demo DEMO_ADMIN_PASSWORD=… ./mvnw spring-boot:run\n"
                  "  frontend: npm run dev                         # http://localhost:5173\n"
                  "Swagger:    http://localhost:5173/api/docs", size=8)
    tabla(doc, ["Paso", "Qué se muestra"], [
        ("1", "Catálogo y ficha del Polo clásico de algodón (stock por talla y color)."),
        ("2", "Personalizador: bordado en el pecho izquierdo, subida del logo y vista previa; intentar la espalda "
         "con bordado (no se ofrece)."),
        ("3", "Reparto 4 S, 4 M, 4 L → escala de docena, S/ 591.60."),
        ("4", "Carrito y checkout con envío a Lima (S/ 601.60); pago rechazado y luego aprobado."),
        ("5", "Panel: el pedido aparece PAGADO; se avanza a EN_PRODUCCION y se descarga el diseño."),
        ("6", "Tienda: la campana muestra el aviso y «Mis pedidos» la línea de tiempo."),
        ("7", "Swagger o Postman: un 409 por stock y un 422 por zona inválida."),
    ], anchos=[8, 92], size=9)
    parrafo(doc,
            "Cuentas ficticias: cliente renzo.paredes@demo.coralshop.pe (clave Cliente2026) y administrador "
            "admin@demo.coralshop.pe (clave definida en DEMO_ADMIN_PASSWORD). Tarjetas de prueba: "
            "4111 1111 1111 1111 (aprobada) y 4000 0000 0000 0002 (rechazada).", size=10)

    h(doc, 2, "Anexo F. Glosario de términos")
    tabla(doc, ["Término", "Definición"], C.GLOSARIO, anchos=[20, 80], size=9)

    h(doc, 1, "Referencias")
    for r in C.REFERENCIAS:
        p = parrafo(doc, r, size=10, space_after=6)
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-1.0)


def main():
    doc = nuevo_documento()
    portada(doc)
    seccion_1(doc)
    seccion_2(doc)
    seccion_3(doc)
    seccion_4(doc)
    seccion_5(doc)
    doc.save(SALIDA)
    print("Informe generado:", SALIDA)


if __name__ == "__main__":
    main()
