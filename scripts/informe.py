# -*- coding: utf-8 -*-
"""Genera entregables/Informe_Proyecto_Final_Coral_Shop.docx"""

import os

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches, Cm

import contenido as C
import esquema
from docx_util import (
    nuevo_documento, tabla, figura, figura_apaisada, indice, salto_pagina, parrafo, vineta,
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
def portada(doc):
    for _ in range(2):
        doc.add_paragraph()
    parrafo(doc, "UNIVERSIDAD TECNOLÓGICA DEL PERÚ", size=16, bold=True,
            color=PRIMARY, align=CENTRO, space_after=2)
    parrafo(doc, f"Facultad de Ingeniería  ·  {C.CARRERA}", size=12,
            color=MUTED, align=CENTRO, space_after=36)

    parrafo(doc, "PROYECTO FINAL", size=11, bold=True, color=ACCENT, align=CENTRO,
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

    h(doc, 1, "Índice")
    indice(doc)
    salto_pagina(doc)

    h(doc, 1, "Resumen ejecutivo")
    parrafo(doc,
            "Coral Shop S.A.C. es una pequeña empresa limeña que produce y vende ropa juvenil (polos, poleras, "
            "gorras y tote bags) y que ofrece estampado personalizado. Hoy vende exclusivamente por Instagram y "
            "WhatsApp, con el inventario anotado en hojas de cálculo y la cotización del estampado hecha a mano. "
            "Esa forma de operar le cuesta pedidos perdidos, sobreventa de tallas y ausencia total de indicadores.")
    parrafo(doc,
            "Este proyecto diseña e implementa una plataforma web de comercio electrónico a la medida de ese "
            "problema. El frontend es una aplicación de página única construida en React; el backend es una "
            "aplicación Java desplegada sobre un contenedor web Apache Tomcat, organizada en tres capas "
            "(controlador con Servlets, servicio y acceso a datos con JDBC) sobre una base de datos PostgreSQL "
            "de 28 tablas. El núcleo diferenciador es un personalizador de estampado que calcula el recargo en "
            "línea y muestra una vista previa antes de comprar.")
    parrafo(doc,
            "El documento recorre el diagnóstico estratégico del negocio (Canvas, PESTEL, FODA e Ishikawa), la "
            "definición completa de las funcionalidades (20 módulos, 49 requerimientos funcionales, 15 "
            "requerimientos no funcionales y 14 reglas de negocio), la arquitectura de la solución, el modelo de "
            "datos con su diccionario de campos y el plan de implementación.")
    nota(doc, "Alcance de esta versión",
         "Esta entrega corresponde a la fase de análisis y diseño. La sección 3 documenta la estructura de "
         "paquetes, las clases y los algoritmos previstos, que se construirán en los sprints 1 a 4 según el "
         "cronograma del Anexo C. Las decisiones técnicas del backend se sustentan en las sesiones del curso "
         "(Arquitectura Java, Contenedores Web, JDBC y MVC), tal como pide la consigna.")
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
            "El lienzo Canvas resume cómo Coral Shop crea, entrega y captura valor. Su lectura deja ver por que "
            "una plataforma propia no es un lujo sino una necesidad: la propuesta de valor completa depende de "
            "que el cliente pueda diseñar y ver su prenda antes de comprarla, y hoy no existe ningún canal que "
            "lo permita.")
    figura_apaisada(doc, "02_canvas.png", "Figura 2. Business Model Canvas de Coral Shop S.A.C.")
    parrafo(doc,
            "Tres bloques del lienzo se traducen directamente en requerimientos del sistema. La propuesta de "
            "valor exige el personalizador con vista previa y el precio calculado al instante (módulo M03) y el "
            "stock real por talla y color (módulos M02 y M14). El bloque de canales convierte la tienda virtual "
            "en el canal principal y relega WhatsApp a la postventa, lo que obliga a que el proceso de compra "
            "sea completamente autónomo (módulos M04, M06 y M07). El bloque de relación con clientes exige "
            "cuenta con historial, avisos automáticos y reseñas de compradores verificados (módulos M08, M09 y "
            "M10).")

    h(doc, 2, "1.5 Análisis PESTEL")
    parrafo(doc,
            "El análisis del entorno se presenta articulado a las decisiones del proyecto: para cada factor se "
            "indica el hallazgo y la consecuencia concreta que tiene sobre la solución, de modo que el "
            "diagnóstico no quede como un ejercicio separado del diseño.")
    tabla(doc, ["Factor", "Hallazgo del entorno", "Implicancia para el proyecto"], C.PESTEL,
          anchos=[14, 43, 43], size=9)

    h(doc, 2, "1.6 Matriz FODA")
    figura_apaisada(doc, "11_foda.png", "Figura 11. Matriz FODA de Coral Shop.")
    parrafo(doc,
            "El diagnóstico se completa con la matriz cruzada, que es la que articula el FODA con los objetivos "
            "del proyecto: cada estrategia indica a que objetivo específico da origen.")
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
           "Figura 1. Diagrama de Ishikawa de la problemática de Coral Shop.")
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
         "estampado, perdida de pedidos y ausencia total de trazabilidad e indicadores para decidir.")
    parrafo(doc,
            "El problema se manifiesta en cifras concretas, obtenidas del registro de la propia empresa "
            "durante el último semestre. Se trata de datos simulados pero coherentes con la operación descrita, "
            "conforme a la recomendación de la consigna de no emplear datos sensibles reales.")
    tabla(doc, ["Manifestación del problema", "Situación actual", "Efecto en el negocio"], [
        ("Sobreventa de tallas", "12 % de los pedidos se cancela porque la talla vendida ya no existía",
         "Devoluciones, reprogramaciones y perdida de confianza del cliente."),
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
            "los módulos funcionales que los hacen posibles. Esa última columna es la que garantiza que el "
            "diagnóstico, los objetivos y el diseño de la solución sean un solo hilo y no tres documentos "
            "distintos.")
    tabla(doc, ["Cod.", "Objetivo específico", "Indicador", "Meta", "Módulos"],
          C.OBJETIVOS_ESPECIFICOS, anchos=[7, 38, 22, 16, 17], size=9)
    salto_pagina(doc)


# ================================================ 2. DISENO DE LA SOLUCION
def seccion_2(doc):
    h(doc, 1, "2. Diseño de la solución")

    h(doc, 2, "2.1 Propuesta de solución")

    h(doc, 3, "2.1.1 Descripción general")
    parrafo(doc,
            "La solución es una plataforma web de comercio electrónico compuesta por dos aplicaciones "
            "conectadas por una API REST. La primera, coral_shop, es la interfaz que usan el cliente y el "
            "personal: una aplicación de página única construida en React. La segunda, coral_shop_backend, es "
            "el motor del negocio: una aplicación Java desplegada sobre un contenedor web que concentra las "
            "reglas, resguarda la seguridad y persiste todo en una base de datos relacional.")
    parrafo(doc,
            "Lo que hace distinta a esta plataforma frente a una tienda en línea genérica son dos decisiones de "
            "diseño. La primera es que el stock no pertenece al producto sino a la variante: cada combinación "
            "de producto, talla y color es un artículo con su propio SKU y su propia existencia, que es la "
            "única forma de dejar de vender tallas que no hay. La segunda es el personalizador de estampado: "
            "el cliente arma su diseño, lo ve sobre la prenda y conoce el precio final sin esperar a que nadie "
            "le responda, y ese diseño viaja hasta el taller convertido en una orden de producción trazable.")

    h(doc, 3, "2.1.2 Alcance de la solución")
    tabla(doc, ["Incluido en el alcance", "Excluido de esta versión"], [
        ("Tienda pública completa: catálogo, búsqueda, filtros, ficha de producto y stock real por variante.",
         "Integración con una pasarela de pagos real. El pago se simula y se registra en la tabla payment con "
         "su código de transacción."),
        ("Personalizador de estampado con vista previa, carga de arte y cálculo automático del recargo.",
         "Facturación electrónica ante SUNAT y emisión de comprobantes formales."),
        ("Carrito de invitado y de usuario, con fusión al iniciar sesión, favoritos y cupones.",
         "Envío automático de correos. Las notificaciones se registran en la bandeja del usuario dentro del "
         "sistema."),
        ("Checkout con direcciones, modalidades de entrega y confirmación del pedido.",
         "Rastreo satelital del paquete. Se registra el número de guía del courier, sin integración con su API."),
        ("Cuenta de usuario: registro, autenticación JWT, perfil, direcciones, historial y Mis diseños.",
         "Inicio de sesión con redes sociales."),
        ("Backoffice: tablero, CRUD de catálogo y maestros, inventario con kardex y bandeja de pedidos.",
         "Módulo contable y de planillas."),
        ("Aprobación del arte por el diseñador y máquina de estados del pedido.",
         "Editor gráfico avanzado (capas, filtros). El personalizador admite una imagen o un texto por zona."),
        ("Gobierno: usuarios y roles, cupones, envíos, reportes exportables y bitácora de auditoría.",
         "Aplicación móvil nativa. La web es responsiva y cubre el uso desde el celular."),
    ], anchos=[50, 50], size=9)
    parrafo(doc,
            "El alcance descrito es deliberadamente amplio: cubre el ciclo completo de venta y la "
            "administración del negocio, con 20 módulos funcionales y 28 tablas relacionadas. Las exclusiones "
            "corresponden a integraciones con terceros que no aportan al aprendizaje del curso y que se "
            "sustituyen por simulaciones coherentes.")

    h(doc, 3, "2.1.3 Actores del sistema")
    tabla(doc, ["Actor", "Descripción", "Qué puede hacer"], C.ACTORES,
          anchos=[15, 27, 58], size=9)

    h(doc, 3, "2.1.4 Características de la tienda virtual: mapa de módulos")
    parrafo(doc,
            "Las funcionalidades de la plataforma se agrupan en 20 módulos repartidos en cuatro dominios: la "
            "tienda pública, el proceso de compra, el backoffice de operación y el gobierno del sistema. El "
            "mapa siguiente los presenta de un vistazo.")
    figura_apaisada(doc, "07_modulos.png", "Figura 7. Mapa funcional de la tienda virtual.")
    tabla(doc, ["Cod.", "Módulo", "Dominio", "Qué resuelve", "Requerimientos"], C.MODULOS,
          anchos=[6, 20, 13, 45, 16], size=9)

    h(doc, 3, "2.1.5 Requerimientos funcionales")
    parrafo(doc,
            "Cada módulo se descompone en requerimientos funcionales enunciados de forma verificable. La "
            "prioridad se asigna con el criterio de que sin los de prioridad alta la tienda no puede operar.")
    tabla(doc, ["Cod.", "Mod.", "Descripción", "Prior.", "Actor"], C.RF,
          anchos=[7, 6, 63, 8, 16], size=8.5)

    h(doc, 3, "2.1.6 Historias de usuario y criterios de aceptación")
    parrafo(doc,
            "Las historias siguientes describen las funcionalidades críticas desde la perspectiva de quien las "
            "usa, con criterios de aceptación escritos en formato dado-cuando-entonces para que no queden "
            "ambigüedades sobre cuando una funcionalidad está terminada.")
    tabla(doc, ["Cod.", "Mod.", "Historia de usuario", "Criterios de aceptación"], C.HISTORIAS,
          anchos=[7, 6, 41, 46], size=8.5)

    h(doc, 3, "2.1.7 Casos de uso")
    figura_apaisada(doc, "05_casos_uso.png",
           "Figura 5. Diagrama de casos de uso: actores y funcionalidades del sistema.")
    parrafo(doc,
            "A modo de ejemplo se detalla el caso de uso más crítico del sistema, porque es el que involucra "
            "más tablas, más reglas de negocio y la única transacción realmente compleja del proyecto.")
    tabla(doc, ["Campo", "CU-06: Realizar el checkout y confirmar el pedido"], [
        ("Actor principal", "Cliente"),
        ("Actores secundarios", "Sistema (cálculo de precios, generación del código, notificación)"),
        ("Precondiciones", "El cliente está autenticado y su carrito tiene al menos una línea."),
        ("Postcondiciones",
         "Existe un pedido en estado PENDIENTE con sus líneas, su pago y sus movimientos de inventario; el "
         "carrito queda marcado como CONVERTIDO."),
        ("Flujo principal",
         "1. El cliente abre el checkout desde el carrito.\n"
         "2. El sistema muestra el resumen y sus direcciones guardadas.\n"
         "3. El cliente elige o registra la dirección de entrega.\n"
         "4. El cliente elige la modalidad de entrega; el sistema recalcula el total con el costo de envío.\n"
         "5. El cliente ingresa un cupón (opcional); el sistema lo valida y aplica el descuento.\n"
         "6. El cliente selecciona el medio de pago y confirma.\n"
         "7. El sistema abre la transacción, bloquea las variantes involucradas y verifica el stock.\n"
         "8. El sistema graba el pedido, sus líneas, la personalización, el pago y los movimientos de stock.\n"
         "9. El sistema confirma la transacción, genera el código CS-AAAA-NNNNNN y notifica al cliente.\n"
         "10. El sistema muestra la página de confirmación con el código de seguimiento."),
        ("Flujo alterno A: stock insuficiente",
         "En el paso 7, si alguna variante no alcanza, el sistema deshace la transacción, no crea el pedido, "
         "responde 409 Conflict indicando la talla afectada y devuelve al cliente al carrito sin perder sus "
         "líneas."),
        ("Flujo alterno B: cupón inválido",
         "En el paso 5, si el cupón esta vencido, agotado o el subtotal no alcanza el mínimo, el sistema lo "
         "rechaza indicando el motivo y mantiene el total sin descuento."),
        ("Flujo alterno C: pago rechazado",
         "En el paso 8, si la pasarela simulada rechaza el pago, el pedido se crea igualmente en estado "
         "PENDIENTE con el pago en estado RECHAZADO, para que el cliente pueda reintentar."),
        ("Reglas aplicadas", "RN-02, RN-03, RN-04, RN-05, RN-06, RN-07, RN-13"),
        ("Requerimientos", "RF-19, RF-20, RF-21, RF-22, RF-23"),
    ], anchos=[18, 82], size=9, zebra=False)

    h(doc, 3, "2.1.8 Requerimientos no funcionales")
    tabla(doc, ["Cod.", "Atributo", "Requerimiento"], C.RNF, anchos=[8, 16, 76], size=9)

    h(doc, 3, "2.1.9 Reglas de negocio")
    parrafo(doc,
            "Las reglas de negocio son las condiciones que el sistema debe hacer cumplir siempre, con "
            "independencia de la pantalla desde la que se le pida. Todas ellas se implementan en la capa de "
            "servicio, nunca en el frontend ni en el servlet, porque el cliente nunca es de confianza.")
    tabla(doc, ["Cod.", "Regla"], C.REGLAS, anchos=[8, 92], size=9)

    # -------------------------------------------------------- 2.2
    h(doc, 2, "2.2 Tecnologías utilizadas")
    parrafo(doc,
            "La consigna pide justificar las decisiones técnicas con base en la teoría vista en clase. Por eso "
            "el backend no se construye con un framework de alto nivel sino con la pila Java EE estudiada en "
            "el curso: Servlets como controlador, JavaBeans como modelo y JDBC como acceso a datos, desplegados "
            "sobre un contenedor web. La última columna de la tabla indica la sesión del curso que sustenta "
            "cada elección.")
    tabla(doc, ["Capa o función", "Tecnología", "Justificación", "Sustento en clase"], C.TECNOLOGIAS,
          anchos=[15, 20, 47, 18], size=8.5)

    h(doc, 3, "2.2.1 Correspondencia con el patrón MVC visto en clase")
    parrafo(doc,
            "La sesión 1 del curso cierra estableciendo la correspondencia entre las tecnologías Java EE y las "
            "capas del patrón MVC: JSP es la Vista, el Servlet es el Controlador y el JavaBean es el Modelo. "
            "El proyecto conserva esa correspondencia con una única adaptación, que conviene explicar porque "
            "es la decisión de diseño más discutible del trabajo.")
    tabla(doc, ["Capa MVC", "Cómo se resuelve en clase", "Cómo se resuelve en este proyecto", "Motivo"], [
        ("Modelo", "JavaBean que representa la estructura de una tabla",
         "Idéntico: un JavaBean por tabla en el paquete model, más DTO para la API",
         "Sin cambios respecto de la teoría."),
        ("Controlador", "Servlet que recibe la petición y coordina",
         "Idéntico: un Servlet por recurso en web.controller, apoyado en Filtros para lo transversal",
         "Sin cambios respecto de la teoría."),
        ("Vista", "JSP con EL y JSTL que genera HTML en el servidor",
         "React en el navegador. El Servlet ya no hace forward a un JSP: escribe JSON en la respuesta",
         "El frontend del equipo es una SPA. Renderizar HTML en el servidor obligaría a recargar la página en "
         "cada filtro del catálogo y haría inviable el personalizador de estampado."),
    ], anchos=[12, 28, 32, 28], size=9)
    parrafo(doc,
            "La adaptación no rompe el patrón: el Servlet sigue siendo el Controlador y sigue sin contener "
            "reglas de negocio ni SQL. Lo único que cambia es el formato de la respuesta, de HTML a JSON. Se "
            "agrega además una capa de servicio entre el controlador y el acceso a datos, para no concentrar "
            "la lógica en el servlet, algo que la rúbrica penaliza explícitamente.")

    h(doc, 3, "2.2.2 Por qué un contenedor web y no un servidor de aplicaciones")
    parrafo(doc,
            "La sesión 3 distingue tres piezas que suelen confundirse. El Web Server (Apache HTTPD, Nginx) "
            "atiende peticiones HTTP y entrega contenido estático, pero no entiende Java. El Web Container "
            "(Tomcat, Jetty) implementa la API de Servlets y JSP y gestiona su ciclo de vida. El Application "
            "Server (WildFly, WebLogic) incluye un contenedor web pero añade el soporte completo de Java EE: "
            "EJB, JMS, JPA y transacciones distribuidas.")
    parrafo(doc,
            "Coral Shop necesita exactamente lo que ofrece la capa intermedia: ejecutar Servlets y Filtros. No "
            "usa componentes distribuidos ni colas de mensajería, y la transacción del pedido se controla "
            "directamente sobre la conexión JDBC. Adoptar un servidor de aplicaciones completo añadiría peso y "
            "complejidad de configuración sin ningún beneficio. Por eso la elección es Apache Tomcat 10.1, que "
            "además es la versión que implementa el espacio de nombres jakarta.servlet.")

    # -------------------------------------------------------- 2.3
    h(doc, 2, "2.3 Arquitectura de la solución")
    parrafo(doc,
            "La arquitectura es cliente-servidor con separación en tres capas del lado del servidor. El "
            "diagrama siguiente muestra los componentes, el medio por el que se comunican y los aspectos que "
            "atraviesan todas las capas.")
    figura_apaisada(doc, "03_arquitectura.png",
           "Figura 3. Arquitectura de la solución: cliente-servidor en tres capas sobre un contenedor web Java.")

    h(doc, 3, "2.3.1 Descripción de las capas")
    vineta(doc,
           "Capa de presentación (navegador): aplicación React que gestiona la navegación, el estado del "
           "carrito y el personalizador. No conoce la base de datos ni las reglas de negocio; solo consume la "
           "API. Se despliega como contenido estático.", "Capa de presentación (navegador):")
    vineta(doc,
           "Filtros: primera línea del servidor. Resuelven la codificación, el CORS, la validación del JWT y "
           "la autorización por rol antes de que la petición llegue al servlet. Concentrar aquí lo transversal "
           "evita repetir el control de acceso en cada controlador.", "Filtros:")
    vineta(doc,
           "Capa de controlador (Servlets): traduce entre el mundo HTTP y el mundo del negocio. Lee "
           "parámetros y cuerpo, valida el formato, invoca al servicio y serializa la respuesta con el código "
           "HTTP correcto. Es deliberadamente delgada.", "Capa de controlador (Servlets):")
    vineta(doc,
           "Capa de servicio: es donde vive el negocio. Aplica las reglas RN-01 a RN-14, orquesta varios DAO "
           "y, cuando una operación toca varias tablas, abre la transacción, desactiva el autocommit y decide "
           "entre commit y rollback.", "Capa de servicio:")
    vineta(doc,
           "Capa de acceso a datos (DAO sobre JDBC): único punto del sistema que conoce SQL. Cada DAO usa "
           "PreparedStatement, recorre el ResultSet y devuelve JavaBeans. Cuando participa en una transacción "
           "recibe la Connection desde el servicio, en lugar de pedir una propia.",
           "Capa de acceso a datos (DAO sobre JDBC):")
    vineta(doc,
           "Persistencia: PostgreSQL 16 con 28 tablas, claves foráneas, restricciones CHECK e índices. El "
           "acceso pasa siempre por un pool de conexiones expuesto como javax.sql.DataSource.", "Persistencia:")

    h(doc, 3, "2.3.2 Flujo de una petición")
    parrafo(doc,
            "Para hacer tangible como colaboran las capas, el diagrama siguiente sigue la petición más "
            "compleja del sistema: la confirmación de un pedido que incluye una prenda personalizada.")
    figura_apaisada(doc, "04_flujo_peticion.png",
           "Figura 4. Flujo de una petición: confirmación de un pedido con personalización.")

    h(doc, 3, "2.3.3 Manejo de la sesión y de la autenticación")
    parrafo(doc,
            "La clase 4 explica el sessión scope: en la primera petición el servidor crea la HttpSessión, "
            "genera el identificador JSESSIONID y lo devuelve como cookie; el navegador la reenvía en cada "
            "petición posterior y el servidor recupera la sesión. El proyecto usa ese mecanismo tal cual para "
            "el carrito del invitado, que es el único estado que tiene sentido guardar en el servidor antes de "
            "que la persona se identifique.")
    parrafo(doc,
            "Para el usuario autenticado, en cambio, la API es sin estado: el cliente envía un JWT firmado en "
            "la cabecera Authorization y el filtro lo valida en cada petición. La combinación es deliberada: "
            "la sesión resuelve la comodidad del invitado y el token resuelve la seguridad y la escalabilidad "
            "del cliente registrado. Al iniciar sesión, CartService fusiona el carrito de la sesión con el "
            "carrito persistido del usuario, según la regla RN-14.")

    h(doc, 3, "2.3.4 Máquina de estados del pedido")
    figura_apaisada(doc, "06_estados_pedido.png",
           "Figura 6. Máquina de estados del pedido y transiciones válidas.")

    h(doc, 3, "2.3.5 Patrones de diseño aplicados")
    tabla(doc, ["Patrón", "Dónde se aplica", "Qué problema resuelve"], [
        ("MVC", "Organización general del backend",
         "Separa datos, coordinación y presentación, que es lo que la rúbrica exige frente a un código "
         "centralizado en un solo bloque."),
        ("DAO", "Paquete dao y dao.jdbc",
         "Aisla el SQL en un único lugar. Cambiar de motor de base de datos no obliga a tocar los servicios."),
        ("DTO", "Paquete model.dto",
         "Desacopla la forma de la API de la forma de las tablas y evita exponer campos sensibles."),
        ("Front Controller / Filter Chain", "Paquete web.filter",
         "Centraliza autenticación, autorización, CORS y registro antes de cualquier controlador."),
        ("Singleton", "DataSourceProvider",
         "Garantiza un único pool de conexiones para toda la aplicación."),
        ("Factory Method", "DaoFactory",
         "Entrega la implementación JDBC de cada DAO sin que el servicio dependa de la clase concreta."),
        ("Strategy", "PricingService y las técnicas de estampado",
         "Permite añadir una nueva técnica de estampado con su fórmula de costo sin modificar el cálculo "
         "existente."),
        ("State", "OrderStatus y sus transiciones",
         "Impide que un pedido salte a un estado no permitido (regla RN-08)."),
    ], anchos=[18, 27, 55], size=9)

    # -------------------------------------------------------- 2.4
    h(doc, 2, "2.4 Diseño de la base de datos")
    parrafo(doc,
            "El modelo relacional consta de 28 tablas, 222 campos y 39 claves foráneas, agrupadas en cinco "
            "módulos funcionales. Todas las tablas están en tercera forma normal, con la única excepción "
            "deliberada de order_item, que se explica más adelante.")
    figura_apaisada(doc, "10_er_global.png",
           "Figura 10. Mapa global del modelo de datos agrupado por módulos funcionales.")
    parrafo(doc,
            "Los diagramas entidad-relación completos, con todos los campos, sus tipos y sus relaciones, se "
            "presentan en las figuras 8 y 9 del Anexo A, en orientación horizontal para que puedan leerse con "
            "comodidad. El diccionario de datos que sigue detalla cada tabla campo por campo.")

    h(doc, 3, "2.4.1 Decisiones de diseño del modelo")
    vineta(doc,
           "El stock vive en la variante, no en el producto. product guarda el modelo de prenda y "
           "product_variant guarda cada combinación real de talla y color, con su SKU, su stock y su precio "
           "propio opcional. Es la decisión que resuelve la causa raíz de la sobreventa.",
           "El stock vive en la variante, no en el producto.")
    vineta(doc,
           "El pedido es inmutable. order_item copia el nombre del producto, el SKU, la talla, el color, el "
           "precio unitario y el recargo del estampado en el momento de la compra. Si mañana sube el precio o "
           "se renombra el producto, los pedidos ya emitidos no cambian. Es una desnormalización consciente: "
           "se prefiere la exactitud histórica sobre la ausencia de redundancia.",
           "El pedido es inmutable.")
    vineta(doc,
           "La personalización es una entidad propia. customization guarda la configuración concreta de un "
           "estampado y puede referirse a un design reutilizable de Mis diseños o ser de un solo uso. Así la "
           "misma estructura sirve al carrito y al pedido.", "La personalización es una entidad propia.")
    vineta(doc,
           "Todo movimiento de stock deja rastro. Ninguna operación modifica product_variant.stock sin "
           "escribir la fila correspondiente en inventory_movement, con el stock anterior, el nuevo, el motivo "
           "y el responsable.", "Todo movimiento de stock deja rastro.")
    vineta(doc,
           "Las categorías forman un árbol. category se autorreferencia mediante parent_id, lo que permite "
           "subcategorías sin cambiar el esquema.", "Las categorías forman un árbol.")
    vineta(doc,
           "La tabla de pedidos se llama orders y no order porque order es una palabra reservada del "
           "estándar SQL y obligaría a entrecomillar el identificador en cada consulta.",
           "La tabla de pedidos se llama orders y no order")

    h(doc, 3, "2.4.2 Integridad, restricciones e índices")
    tabla(doc, ["Mecanismo", "Aplicación en el modelo"], [
        ("Claves primarias", "Toda tabla tiene una clave primaria sustituta de tipo SERIAL o BIGSERIAL."),
        ("Claves foráneas", "39 relaciones declaradas. Se usa ON DELETE RESTRICT en catálogo y pedidos para "
         "impedir borrar información referenciada, y ON DELETE CASCADE en las dependencias débiles "
         "(product_image, cart_item, order_status_history)."),
        ("Unicidad simple", "email, sku, slug, order_code, coupon.code y role.name."),
        ("Unicidad compuesta", "UNIQUE (product_id, size_id, color_id) en product_variant impide duplicar una "
         "variante. UNIQUE (user_id, product_id) en wishlist_item y UNIQUE (user_id, order_item_id) en review "
         "impiden favoritos y reseñas repetidas."),
        ("Restricciones CHECK", "stock >= 0 y reserved_stock >= 0 en product_variant; quantity > 0 en cart_item "
         "y order_item; rating entre 1 y 5 en review; discount_value > 0 en coupon; total_amount >= 0 en orders."),
        ("Valores por defecto", "created_at con CURRENT_TIMESTAMP, is_active en TRUE, used_count y "
         "reserved_stock en 0."),
        ("Índices B-tree", "Sobre product(category_id), product(slug), product_variant(sku), "
         "product_variant(product_id), orders(user_id), orders(order_code), orders(status), "
         "order_item(order_id), inventory_movement(variant_id, created_at) y audit_log(created_at)."),
        ("Baja lógica", "Las entidades del catálogo y los usuarios no se borran físicamente: se desactivan con "
         "is_active, para no romper el histórico de pedidos."),
        ("Transacciones", "La creación del pedido y el ajuste de inventario se ejecutan con autocommit "
         "desactivado, con commit único al final y rollback ante cualquier excepción."),
    ], anchos=[22, 78], size=9)

    h(doc, 3, "2.4.3 Diccionario de datos")
    parrafo(doc,
            "Se detalla a continuación cada tabla del modelo con sus campos, tipos, llaves y significado. Es "
            "la especificación a partir de la cual se escribirá el archivo schema.sql.")

    for modulo_id, (nombre_mod, _color) in esquema.MODULOS.items():
        tablas_mod = [t for t in esquema.TABLAS if t["modulo"] == modulo_id]
        h(doc, 4, f"Módulo: {nombre_mod}")
        for t in tablas_mod:
            parrafo(doc, t["nombre"], size=11, bold=True, color=BLUE, align=IZQ,
                    space_after=1)
            parrafo(doc, t["desc"], size=9.5, italic=True, color=MUTED, space_after=3)
            filas = [(c[0], c[1], c[2] if c[2] else "-", c[3]) for c in t["campos"]]
            tabla(doc, ["Campo", "Tipo", "Llave", "Descripción"], filas,
                  anchos=[19, 17, 18, 46], size=8.5)
            if t.get("restricciones"):
                parrafo(doc, "Restricciones adicionales: " + "; ".join(t["restricciones"]),
                        size=9, italic=True, color=ACCENT, space_after=10)
    salto_pagina(doc)


# ================================================ 3. IMPLEMENTACION
def seccion_3(doc):
    h(doc, 1, "3. Implementación")
    nota(doc, "Estado de esta sección",
         "Esta sección documenta el diseño de la implementación: la estructura de paquetes, el catálogo de "
         "clases por capa, el detalle de las funcionalidades y los algoritmos y estructuras de datos que se "
         "emplearán. La construcción del código se ejecuta en los sprints 1 a 4 del cronograma del Anexo C, y "
         "sus resultados se incorporarán a esta misma sección en la entrega final.")

    h(doc, 2, "3.1 Estructura de paquetes")
    parrafo(doc,
            "La organización en paquetes refleja de forma literal las capas de la arquitectura. Ningún "
            "directorio mezcla componentes de dos capas distintas, que es exactamente lo que la rúbrica "
            "sanciona en los niveles bajos de logro.")
    bloque_codigo(doc, C.ARBOL_PAQUETES)
    parrafo(doc,
            "La regla de dependencia es unidireccional: web.controller depende de service, service depende de "
            "dao, y dao depende de model. Nunca al revés. Un DAO no conoce al servicio que lo invoca y un "
            "servicio no sabe si lo llama un servlet o una prueba unitaria; gracias a eso la capa de servicio "
            "puede probarse con Mockito sin levantar Tomcat ni la base de datos.")

    h(doc, 2, "3.2 Clases utilizadas en la aplicación")
    tabla(doc, ["Paquete", "Clases", "Responsabilidad"], C.CLASES, anchos=[15, 45, 40], size=8.5)

    h(doc, 3, "3.2.1 Aplicación de la programación orientada a objetos")
    vineta(doc,
           "Encapsulamiento: todos los atributos de las clases del modelo son privados y se exponen "
           "únicamente mediante getters y setters, tal como define el estándar JavaBean visto en la sesión 1.",
           "Encapsulamiento:")
    vineta(doc,
           "Abstracción: cada DAO y cada servicio se declaran primero como interfaz. Los servicios dependen "
           "de la interfaz del DAO, no de su implementación JDBC.", "Abstracción:")
    vineta(doc,
           "Herencia: AbstractJdbcDao concentra la obtención de la conexión, el cierre de recursos y la "
           "traducción de SQLException; cada DAO concreto la extiende y solo escribe sus consultas. Todos los "
           "controladores extienden HttpServlet.", "Herencia:")
    vineta(doc,
           "Polimorfismo: PricingService resuelve el recargo invocando la estrategia de cálculo que "
           "corresponde a la técnica de estampado, sin conocer cual es.", "Polimorfismo:")
    vineta(doc,
           "Composición: OrderService no hereda de los DAO, los compone. Recibe OrderDao, VariantDao, "
           "InventoryDao y PaymentDao y coordina su trabajo dentro de una sola transacción.", "Composición:")

    h(doc, 2, "3.3 Funcionalidades implementadas")
    parrafo(doc,
            "El detalle de las funcionalidades corresponde a los 20 módulos y los 49 requerimientos "
            "funcionales especificados en la sección 2.1. La tabla siguiente indica en que sprint se construye "
            "cada bloque y con que endpoints de la API se expone, de modo que el avance sea verificable.")
    tabla(doc, ["Sprint", "Módulos", "Funcionalidades", "Estado"], [
        ("Sprint 1", "M16, M10",
         "Registro, inicio y cierre de sesión con JWT, recuperación de contraseña, perfil, direcciones, "
         "usuarios y roles.", "Planificado"),
        ("Sprint 2", "M01, M02, M12, M13, M14",
         "Catálogo público con filtros y búsqueda, ficha de producto con variantes, CRUD de catálogo y "
         "maestros, inventario con kardex y alertas.", "Planificado"),
        ("Sprint 3", "M03, M04, M05, M06, M07, M08",
         "Personalizador con vista previa y cálculo de recargo, carrito de invitado y de usuario, favoritos, "
         "checkout transaccional, cupones y seguimiento.", "Planificado"),
        ("Sprint 4", "M09, M11, M15, M17, M18, M19, M20",
         "Reseñas moderadas, tablero de indicadores, bandeja de pedidos con máquina de estados y aprobación "
         "del arte, cupones, envíos, reportes y auditoría.", "Planificado"),
    ], anchos=[10, 20, 55, 15], size=9)

    h(doc, 3, "3.3.1 Interfaz de programación (API REST)")
    parrafo(doc,
            "Las funcionalidades se exponen al frontend a través de los siguientes recursos. La columna de "
            "acceso indica el rol mínimo que exige el filtro de autorización.")
    tabla(doc, ["Método", "Ruta", "Acceso", "Descripción", "Servlet"], C.ENDPOINTS,
          anchos=[8, 27, 13, 37, 15], size=8.5)

    h(doc, 2, "3.4 Algoritmos y estructuras de datos implementados")
    parrafo(doc,
            "La elección de cada estructura responde a la operación que se ejecuta con más frecuencia sobre "
            "ella, y no a la costumbre. La última columna enlaza cada decisión con la funcionalidad que la "
            "necesita.")
    tabla(doc, ["Propósito", "Estructura o algoritmo", "Justificación", "Usado en"], C.ALGORITMOS,
          anchos=[19, 22, 44, 15], size=8.5)

    h(doc, 3, "3.4.1 Complejidad de las operaciones críticas")
    tabla(doc, ["Operación", "Estructura", "Complejidad", "Alternativa descartada"], [
        ("Agregar o buscar una línea en el carrito", "HashMap", "O(1) promedio",
         "Recorrer una lista: O(n) en cada pulsación del botón."),
        ("Ordenar el resultado del catálogo", "TimSort sobre ArrayList", "O(n log n)",
         "Ordenar en base de datos en cada petición cuando el conjunto ya está en memoria."),
        ("Validar una transición de estado", "EnumMap con EnumSet", "O(1)",
         "Cadena de condicionales anidados, difícil de mantener y de probar."),
        ("Buscar un producto por slug o SKU", "Índice B-tree", "O(log n)",
         "Recorrido secuencial de la tabla: O(n)."),
        ("Armar el menú de categorías", "Recorrido en profundidad del árbol", "O(n)",
         "Una consulta por nivel, que multiplica los viajes a la base de datos."),
        ("Reservar stock en compras simultáneas", "SELECT ... FOR UPDATE", "O(log n) más espera del bloqueo",
         "Leer y luego escribir sin bloqueo, que permite vender dos veces la última unidad."),
    ], anchos=[27, 21, 20, 32], size=9)
    salto_pagina(doc)


# ================================================ 4. CONCLUSIONES
def seccion_4(doc):
    h(doc, 1, "4. Conclusiones y recomendaciones")

    h(doc, 2, "4.1 Conclusiones")
    conclusiones = [
        "El diagnóstico estratégico demostró que el problema de Coral Shop no es de ventas sino de "
        "infraestructura: el análisis de Ishikawa concentró las causas controlables en las ramas de "
        "tecnología, método y medición, y las tres apuntan a la ausencia de un sistema propio. El Canvas y el "
        "FODA cruzado confirmaron que la debilidad D1 condiciona a todas las demás, por lo que el proyecto "
        "ataca esa causa raíz y no sus síntomas.",
        "Definir el stock a nivel de variante y no de producto es la decisión de modelado que resuelve el "
        "síntoma más costoso del negocio. El 12 % de cancelaciones por sobreventa se origina en que el "
        "catálogo publicado no distingue tallas ni colores; separar product de product_variant convierte ese "
        "problema en una restricción de integridad que la base de datos hace cumplir sola.",
        "El personalizador de estampado es lo que justifica construir una plataforma propia en lugar de "
        "abrir una tienda en un marketplace. Ningún canal de terceros permite que el cliente componga su arte, "
        "lo vea sobre la prenda y conozca el precio final al instante; esa funcionalidad, sostenida por las "
        "tablas de técnicas, zonas y tamaños, es la propuesta de valor convertida en software.",
        "La pila Java EE estudiada en el curso resulta suficiente para un alcance de esta complejidad. "
        "Servlets como controlador, JavaBeans como modelo y JDBC como acceso a datos, sobre un contenedor web "
        "Tomcat, cubren las 20 funcionalidades sin necesidad de un servidor de aplicaciones completo. La única "
        "adaptación respecto de la teoría, sustituir la Vista JSP por React, se justifica en la naturaleza de "
        "aplicación de página única del frontend y no altera los roles de Modelo ni de Controlador.",
        "Separar el sistema en tres capas con una regla de dependencia unidireccional tiene un beneficio "
        "verificable y no solo estético: la capa de servicio, donde viven las 14 reglas de negocio, puede "
        "probarse con JUnit y Mockito sin levantar el contenedor ni la base de datos, lo que hace viable el "
        "ciclo TDD comprometido por el equipo.",
        "La trazabilidad se diseño como parte del modelo y no como un añadido posterior. Las tablas "
        "inventory_movement, order_status_history y audit_log garantizan que toda variación de stock, todo "
        "cambio de estado y toda acción administrativa queden registrados con su responsable, lo que a la vez "
        "resuelve el problema de la ausencia de indicadores.",
        "Formular cada objetivo específico con un indicador y una meta, y enlazarlo con los módulos que lo "
        "hacen posible, permite evaluar el éxito del proyecto con datos y no con impresiones. La matriz de "
        "trazabilidad del Anexo D cierra ese hilo hasta el nivel de las tablas de la base de datos.",
    ]
    for c in conclusiones:
        vineta(doc, c)

    h(doc, 2, "4.2 Recomendaciones")
    recomendaciones = [
        "Construir primero el módulo de usuarios, roles y autenticación. Es la base sobre la que se apoyan "
        "el control de acceso de todos los demás módulos y la bitácora de auditoría; dejarlo para el final "
        "obligaría a reescribir los controladores ya hechos.",
        "Escribir el archivo schema.sql a partir del diccionario de datos de la sección 2.4 antes de "
        "programar cualquier DAO, y versionarlo en el repositorio junto con un seed.sql de datos simulados. "
        "Trabajar sobre una base creada a mano por cada integrante es la vía más rápida hacia diferencias "
        "imposibles de reproducir.",
        "Producir los prototipos de pantalla de los módulos M03 y M06 antes de programarlos. El "
        "personalizador y el checkout son los dos flujos con más pasos y más decisiones del usuario, y "
        "resolverlos en papel cuesta mucho menos que corregirlos en código.",
        "Cubrir con pruebas unitarias, como mínimo, PricingService, OrderService y la validación de "
        "transiciones de OrderStatus. Son las clases donde un error se traduce directamente en dinero mal "
        "cobrado o en stock mal descontado.",
        "No dejar la seguridad para el final. El hash BCrypt, el uso obligatorio de PreparedStatement y la "
        "validación en el servidor deben incorporarse desde la primera clase que se escriba, porque añadirlos "
        "después implica revisar todo el código ya producido.",
        "Mantener configurables en base de datos los costos de las técnicas, las zonas y los tamaños de "
        "estampado. El análisis PESTEL mostró que el tipo de cambio afecta el precio de los insumos "
        "importados; si esos valores quedarán escritos en el código, cada ajuste de precio exigiría un nuevo "
        "despliegue.",
        "Levantar el entorno con Docker Compose desde el sprint 1 y no al final. Es la forma de asegurar que "
        "los cinco integrantes trabajen sobre la misma versión de Tomcat y de PostgreSQL, y de que la "
        "demostración de la semana 18 no dependa de la máquina de una persona.",
        "Preparar los datos simulados con volumen realista, del orden de 60 productos y 400 variantes. Un "
        "catálogo de cinco productos no permite demostrar la paginación, los filtros ni el rendimiento, que "
        "son criterios evaluados en la rúbrica.",
    ]
    for r in recomendaciones:
        vineta(doc, r)
    salto_pagina(doc)


# ================================================ 5. ANEXOS
def seccion_5(doc):
    h(doc, 1, "5. Anexos")

    h(doc, 2, "Anexo A. Modelo entidad-relación ampliado")
    parrafo(doc,
            "Los dos diagramas siguientes presentan el modelo completo con todos los campos y sus relaciones. "
            "Se muestran en orientación horizontal para facilitar su lectura. En ambos, la flecha parte del "
            "campo que contiene la clave foránea y apunta al campo referenciado.")
    seccion_horizontal(doc)
    figura(doc, "08_er_usuarios_catalogo.png",
           "Figura 8. Modelo entidad-relación (1 de 2): usuarios, catálogo e inventario.",
           ancho_pulgadas=9.0)
    figura(doc, "09_er_personalizacion_compra.png",
           "Figura 9. Modelo entidad-relación (2 de 2): personalización, carrito, pedidos y soporte.",
           ancho_pulgadas=9.0)
    seccion_vertical(doc)

    h(doc, 2, "Anexo B. Prototipos de pantalla")
    parrafo(doc,
            "El diseño de pantallas se desarrolla sobre la base visual del frontend ya construido por el "
            "equipo, disponible en https://coral-st.netlify.app. La Figura B0 muestra el mapa de navegación "
            "completo; las figuras B1 a B11 detallan cada pantalla, agrupadas en tienda pública, cliente "
            "autenticado y backoffice, en el mismo orden en que aparece el flujo de compra.")
    figura(doc, "B0_mapa_navegacion.png",
           "Figura B0. Mapa de navegación: cómo se enlazan las pantallas de la tienda y del backoffice.")
    figura(doc, "B1_home.png", "Figura B1. Portada de la tienda.")
    figura(doc, "B2_catalogo.png", "Figura B2. Catálogo con filtros (M01).")
    figura(doc, "B3_producto.png",
           "Figura B3. Ficha de producto: talla, color y stock real (M02).")
    figura(doc, "B4_personalizador.png", "Figura B4. Personalizador de estampado (M03).")
    figura(doc, "B5_carrito.png", "Figura B5. Carrito de compras (M04 y M07).")
    figura(doc, "B6_checkout.png", "Figura B6. Checkout en tres pasos (M06).")
    figura(doc, "B7_confirmacion.png",
           "Figura B7. Confirmación y seguimiento del pedido (M06 y M08).")
    figura(doc, "B8_cuenta.png", "Figura B8. Mi cuenta: pedidos y Mis diseños (M08 y M10).")
    figura(doc, "B9_tablero.png", "Figura B9. Tablero administrativo (M11).")
    figura(doc, "B10_producto_admin.png",
           "Figura B10. Mantenimiento de producto y variantes (M12).")
    figura(doc, "B11_pedidos_admin.png",
           "Figura B11. Bandeja de pedidos y aprobación del arte (M15).")

    h(doc, 2, "Anexo C. Cronograma del proyecto")
    tabla(doc, ["Sprint", "Periodo", "Objetivo", "Entregables", "Estado"], C.CRONOGRAMA,
          anchos=[9, 14, 20, 44, 13], size=9)

    h(doc, 2, "Anexo D. Matriz de trazabilidad")
    parrafo(doc,
            "La matriz enlaza cada objetivo específico con los módulos que lo realizan, los requerimientos "
            "que lo especifican y las tablas que lo soportan. Es la evidencia de que el diagnóstico, los "
            "objetivos, el diseño funcional y el modelo de datos forman una sola línea argumental.")
    tabla(doc, ["Obj.", "Módulos", "Requerimientos", "Tablas principales"], [
        ("OE-1", "M01, M02, M04, M05, M06, M07, M10",
         "RF-01 a RF-09, RF-15 a RF-23, RF-28 a RF-31",
         "product, product_variant, category, cart, cart_item, orders, order_item, payment, coupon, "
         "shipping_method, app_user, address, wishlist_item"),
        ("OE-2", "M03, M13, M15",
         "RF-10 a RF-14, RF-36, RF-42",
         "print_technique, print_zone, print_size, design, customization"),
        ("OE-3", "M02, M12, M14",
         "RF-07, RF-08, RF-33 a RF-35, RF-37 a RF-39",
         "product_variant, size, color, inventory_movement, product_image"),
        ("OE-4", "M11, M19",
         "RF-32, RF-46, RF-47",
         "orders, order_item, product_variant, review"),
        ("OE-5", "M16, M20",
         "RF-43, RF-48, RF-49",
         "role, app_user, audit_log, password_reset_token"),
        ("OE-6", "Transversal",
         "RNF-09 a RNF-11, RNF-15",
         "Todas (a través de la capa de servicio y los DAO)"),
    ], anchos=[7, 20, 26, 47], size=9)

    h(doc, 2, "Anexo E. Glosario de términos")
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
