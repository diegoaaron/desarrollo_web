# -*- coding: utf-8 -*-
"""Genera clase_entregables/avance_2_ver_1.docx (avance 2: arquitectura de la solución).

La carátula es la del informe del entregable 1 (informe.caratula); el contenido se centra en
los cuatro patrones de arquitectura vistos en clase aplicados al código real de Coral Shop."""

import os

import esquema
from docx_util import (
    nuevo_documento, tabla, figura, figura_apaisada, indice, salto_pagina, parrafo, vineta,
    bloque_codigo, nota, seccion_horizontal,
)
from informe import caratula, h

SALIDA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "clase_entregables", "avance_2_ver_1.docx")


# ============================================================ 1. INTRODUCCIÓN
def introduccion(doc):
    h(doc, 1, "1. Introducción")
    h(doc, 2, "1.1 Objetivo del avance")
    parrafo(doc,
            "Este segundo avance presenta la arquitectura de Coral Shop tal como quedó implementada, a la luz de los "
            "cuatro patrones de arquitectura revisados en clase: arquitectura en capas, cliente-servidor, "
            "modelo-vista-controlador (MVC) y arquitectura dirigida por eventos. Para cada patrón se explica la idea, "
            "dónde aparece en el código real (paquetes, clases y endpoints) y qué problema concreto resuelve en la "
            "tienda.")
    parrafo(doc,
            "El caso que recorre todo el documento es el corazón del negocio: un cliente personaliza 12 polos con su "
            "logo bordado en el pecho, los reparte entre tallas S, M y L, crea el pedido, lo paga y el administrador lo "
            "avanza hasta ENTREGADO. Es la misma historia con la que se verificó el sistema de punta a punta.")

    h(doc, 2, "1.2 Estado del proyecto")
    parrafo(doc,
            "El desarrollo se organiza en fases. Las tres primeras están terminadas e integradas a la rama principal "
            "del repositorio; las siguientes se describen en la sección 4.")
    tabla(doc, ["Fase", "Contenido", "Estado"], [
        ("0 · Ordenar la casa", "Código muerto eliminado, interfaz en español y soles, backend reorganizado en capas, "
         "manejo uniforme de errores", "Terminada"),
        ("1 · Modelo de datos", "Migración V5: tipos de producto, personalización, mayoreo, direcciones, pedidos, "
         "historial de estados y pagos (25 tablas)", "Terminada"),
        ("2 · API del flujo de compra", "Catálogo filtrado, personalizador, diseños, cotización, pedidos, pago "
         "simulado, máquina de estados y administración", "Terminada"),
        ("3 · Frontend del flujo de compra", "Personalizador, carrito, checkout y «Mis pedidos» en React",
         "Siguiente"),
        ("4 · Evento de dominio", "OrderStatusChanged con notificaciones y auditoría", "Diseñada"),
        ("5 · Calidad y demo", "Pruebas, datos de demostración, colección Postman y documentación", "Pendiente"),
        ("6 · Pasarela real", "Pago en sandbox con confirmación por webhook", "Pendiente"),
    ], anchos=[26, 56, 18], size=9)

    h(doc, 2, "1.3 Tecnologías")
    tabla(doc, ["Capa", "Tecnología", "Relación con lo visto en clase"], [
        ("Vista", "React 19 + Vite 8 + Tailwind 4 + React Router 7", "Ocupa el lugar de la JSP: la vista se ejecuta "
         "en el navegador y recibe JSON."),
        ("Controlador", "Spring Boot 3.5 (Spring MVC) sobre Java 21", "Spring MVC se apoya en un único Servlet, el "
         "DispatcherServlet, que reparte cada petición al @RestController que corresponde."),
        ("Contenedor web", "Apache Tomcat embebido", "El mismo contenedor de Servlets de la sesión de contenedores "
         "web, empaquetado dentro de la aplicación."),
        ("Acceso a datos", "JdbcTemplate (Spring JDBC) + JPA para la cuenta", "JdbcTemplate es JDBC con "
         "PreparedStatement y manejo automático de conexiones; nunca se concatena SQL."),
        ("Base de datos", "PostgreSQL 16 + Flyway (migraciones V1 a V5)", "Integridad referencial y restricciones "
         "CHECK en la propia base."),
        ("Seguridad", "Spring Security: sesión (JSESSIONID), BCrypt, CSRF y roles", "El session scope y la cookie "
         "JSESSIONID de la clase de JSP y MVC."),
    ], anchos=[17, 33, 50], size=9)
    salto_pagina(doc)


# ======================================================= 2. PATRONES DE ARQUITECTURA
def capas(doc):
    h(doc, 2, "2.1 Arquitectura en capas")
    parrafo(doc,
            "La arquitectura en capas divide el sistema en niveles con una responsabilidad cada uno: presentación, "
            "negocio y datos. La regla que la hace funcionar es que cada capa conoce solo a la capa de abajo. En Coral "
            "Shop cada módulo funcional (catálogo, pedidos, pagos, diseños…) tiene sus propios paquetes controller, "
            "service y repository, de modo que la separación se ve en la estructura de carpetas.")
    tabla(doc, ["Capa", "Responsabilidad", "En Coral Shop", "Si algo falla"], [
        ("Presentación", "Recibir la petición HTTP y validar su FORMATO", "@RestController + DTO con @Valid "
         "(CreateOrderRequest, AddressRequest…)", "400 · datos con formato inválido"),
        ("Negocio", "Aplicar las REGLAS en una transacción", "@Service + @Transactional (OrderService, "
         "PricingService, QuantityPolicy, OrderStatusPolicy)", "422 · regla violada\n409 · conflicto (stock)"),
        ("Datos", "Leer y escribir en la base, solo con parámetros", "@Repository con JdbcTemplate "
         "(OrderRepository, ProductRepository)", "409 · restricción de la base"),
    ], anchos=[15, 27, 37, 21], size=9)

    h(doc, 3, "2.1.1 El restaurante en capas")
    parrafo(doc,
            "La dinámica de clase compara las capas con un restaurante. El mozo toma el pedido y revisa que esté "
            "completo, el cocinero aplica la receta y el almacenero trae los ingredientes de la despensa. El mozo nunca "
            "entra a la despensa. En Coral Shop el mozo es el controller, el cocinero el service, el almacenero el "
            "repository y la despensa PostgreSQL.")
    figura(doc, "A2_01_capas_restaurante.png",
           "Figura 1. El restaurante en capas aplicado a Coral Shop.", ancho_pulgadas=6.4)
    nota(doc, "Comprobación en el código",
         "Ningún controller del backend recibe JdbcTemplate ni escribe SQL: todo el SQL vive en las clases "
         "@Repository. Es la versión en código de «el mozo no entra a la despensa». Si mañana cambia la base de "
         "datos, solo se tocan los repositorios.")

    h(doc, 3, "2.1.2 Caso práctico: crear un pedido")
    parrafo(doc,
            "Igual que en el ejemplo de la Mesa de Partes Digital, la petición atraviesa las tres capas en orden y "
            "cada una responde con un código HTTP distinto cuando algo no cuadra. La Figura 2 muestra el recorrido de "
            "POST /api/orders.")
    figura(doc, "A2_02_capas_pedido.png",
           "Figura 2. Recorrido de la creación de un pedido por las tres capas.", ancho_pulgadas=6.0)
    vineta(doc,
           "Presentación. CustomerOrderController recibe el cuerpo y CreateOrderRequest lo valida con @Valid: líneas "
           "no vacías, cantidades entre 1 y 10 000, código de envío obligatorio, teléfono con formato. Si algo falla "
           "responde 400 sin tocar la base.", "Presentación.")
    vineta(doc,
           "Negocio. OrderService abre una transacción. Con PricingService comprueba que el producto esté activo y "
           "sea personalizable, que cada zona admita la técnica elegida, que el diseño sea del propio cliente y "
           "recalcula todos los precios en el servidor; QuantityPolicy elige la escala de mayoreo. Una regla rota "
           "responde 422.", "Negocio.")
    vineta(doc,
           "Datos. OrderRepository y ProductRepository descuentan el stock con una actualización condicional "
           "(UPDATE … WHERE stock >= ?) y guardan el pedido, sus líneas, zonas, ítems y el primer registro del "
           "historial. Si una talla no alcanza, la transacción se deshace completa y se responde 409.", "Datos.")
    parrafo(doc,
            "El modelo (PricedLine, NewOrder, OrderStatus, LineAmounts) no pertenece a ninguna capa: son objetos de "
            "datos inmutables que las tres comparten, igual que la entidad Trámite en el ejemplo de clase.")

    h(doc, 3, "2.1.3 Respuestas de error uniformes")
    parrafo(doc,
            "Un único @RestControllerAdvice traduce las excepciones de todas las capas a un JSON con la misma forma "
            "{ status, message, errors }. Los mensajes de la tabla son respuestas reales obtenidas al verificar la "
            "API.")
    tabla(doc, ["Código", "Capa que lo produce", "Ejemplo real"], [
        ("400", "Presentación", "Cotización sin líneas; archivo que no es imagen; diseño de más de 5 MB"),
        ("404", "Negocio", "Un cliente pide el detalle de un pedido ajeno: «Pedido no encontrado»"),
        ("409", "Negocio / Datos", "«Stock insuficiente para POLO-…-S (S, Blanco): pediste 21»"),
        ("422", "Negocio", "«La zona ESPALDA no admite bordado…»; pasar un pedido de PAGADO a ENTREGADO"),
    ], anchos=[10, 22, 68], size=9)


def cliente_servidor(doc):
    h(doc, 2, "2.2 Arquitectura cliente-servidor")
    parrafo(doc,
            "En el modelo cliente-servidor varios clientes piden servicios a un servidor que concentra los datos y las "
            "reglas. Coral Shop tiene tres tipos de cliente (la tienda, el panel de administración y las herramientas "
            "de prueba) y un único servidor Spring Boot, que es el único que habla con PostgreSQL.")
    figura(doc, "A2_03_cliente_servidor.png",
           "Figura 3. Arquitectura cliente-servidor de Coral Shop.", ancho_pulgadas=6.4)
    tabla(doc, ["Aspecto", "Decisión", "Por qué"], [
        ("Protocolo", "HTTP con cuerpos JSON en /api/…", "El navegador y Postman usan el mismo contrato."),
        ("Sesión", "Cookie JSESSIONID emitida por Spring Security", "Se reutiliza el session scope de clase; el "
         "rol (cliente o administrador) viaja en la sesión del servidor."),
        ("CSRF", "Token en la cabecera X-CSRF-TOKEN para todo POST, PUT, PATCH y DELETE",
         "Impide que otra página envíe peticiones con la sesión del usuario."),
        ("Confianza", "El servidor recalcula precios y stock (D10)", "El cliente puede ser manipulado; el "
         "servidor nunca acepta importes enviados por el navegador."),
        ("Mismo origen", "Vite en desarrollo y Vercel en producción reenvían /api al servidor",
         "El navegador solo ve un dominio: la cookie y el CSRF funcionan sin configurar CORS."),
    ], anchos=[15, 42, 43], size=9)


def mvc(doc):
    h(doc, 2, "2.3 Modelo-Vista-Controlador")
    parrafo(doc,
            "MVC separa los datos y sus reglas (modelo), lo que ve el usuario (vista) y quien coordina ambos "
            "(controlador). En clase se presentó con JavaBeans, Servlets y JSP. Coral Shop conserva los tres roles; la "
            "diferencia es que la vista ya no es una JSP renderizada en el servidor sino una aplicación React que se "
            "ejecuta en el navegador.")
    figura(doc, "A2_04_mvc.png", "Figura 4. MVC con React como vista y Spring como controlador.",
           ancho_pulgadas=6.4)
    tabla(doc, ["Rol MVC", "En clase", "En Coral Shop"], [
        ("Modelo", "JavaBeans", "Records inmutables (ProductView, OrderDetailView, PricedLine), la entidad User de "
         "JPA y los servicios que aplican las reglas"),
        ("Vista", "JSP", "Pantallas React en pages/ y features/: catálogo, ficha, carrito, checkout y panel"),
        ("Controlador", "Servlet", "@RestController (CatalogController, CustomerOrderController, "
         "AdminOrderController…) atendidos por el DispatcherServlet"),
    ], anchos=[15, 15, 70], size=9)
    parrafo(doc,
            "El controlador ya no hace forward a una JSP: devuelve JSON y la vista React lo dibuja. Gracias a eso la "
            "misma API sirve a la tienda, al panel y a las pruebas automáticas.")


def eventos(doc):
    h(doc, 2, "2.4 Arquitectura dirigida por eventos")
    parrafo(doc,
            "En la arquitectura dirigida por eventos un componente publica un hecho («el pedido cambió de estado») en "
            "un bus, y otros componentes suscritos reaccionan sin que quien publica los conozca. Así se agregan "
            "efectos nuevos sin modificar el código que ya funciona.")
    nota(doc, "Estado actual",
         "Este patrón todavía no está implementado: hoy no existen eventos, suscriptores ni bus. Se diseñó para la "
         "fase 4 sobre el mecanismo de eventos que Spring ya incluye, sin agregar un broker externo.")
    figura(doc, "A2_05_eventos.png",
           "Figura 5. Propuesta del evento OrderStatusChanged para la fase 4.", ancho_pulgadas=6.4)
    tabla(doc, ["Elemento", "Diseño"], [
        ("Evento", "OrderStatusChanged { orderId, orderCode, from, to, changedBy, changedAt }"),
        ("Publicadores", "PaymentService (pago aprobado → PAGADO) y OrderAdminService (avance o cancelación)"),
        ("Bus", "ApplicationEventPublisher de Spring, dentro del mismo proceso"),
        ("Suscriptores", "NotificationListener (aviso en «Mis pedidos»), AuditListener (bitácora) y, más adelante, "
         "EmailListener (correo al cliente)"),
        ("Garantía", "@TransactionalEventListener(AFTER_COMMIT): solo se reacciona si el cambio se guardó"),
    ], anchos=[18, 82], size=9)
    parrafo(doc,
            "Se descarta por ahora un broker como Kafka o RabbitMQ: con un solo servidor y pocos suscriptores, el bus "
            "en memoria de Spring da el mismo desacoplamiento sin infraestructura adicional. Si la tienda creciera a "
            "varios servicios, el evento ya definido se podría publicar en un broker sin cambiar a los publicadores.")


def combinacion(doc):
    h(doc, 2, "2.5 Cómo conviven los cuatro patrones")
    parrafo(doc,
            "Los patrones no compiten: cada uno describe el sistema desde un nivel distinto y se aplican a la vez.")
    tabla(doc, ["Patrón", "Nivel que describe", "Dónde se ve", "Beneficio para Coral Shop"], [
        ("Cliente-servidor", "Despliegue: qué corre dónde", "React en el navegador, Spring Boot en el servidor, "
         "PostgreSQL detrás", "Reglas y datos protegidos en un solo lugar"),
        ("MVC", "Interacción con el usuario", "React (vista), @RestController (controlador), records y "
         "servicios (modelo)", "La misma API sirve a la tienda, al panel y a las pruebas"),
        ("Capas", "Organización del servidor", "Paquetes controller / service / repository de cada módulo",
         "Cambios acotados; errores 400, 422 y 409 bien separados"),
        ("Eventos", "Reacciones a hechos del negocio", "OrderStatusChanged (fase 4)",
         "Notificar y auditar sin tocar el flujo de pedidos"),
    ], anchos=[16, 22, 33, 29], size=9)
    salto_pagina(doc)


def patrones(doc):
    h(doc, 1, "2. Patrones de arquitectura aplicados")
    parrafo(doc,
            "Esta sección recorre, uno por uno, los patrones revisados en clase. Los diagramas usan nombres reales de "
            "clases, endpoints y tablas del repositorio.")
    capas(doc)
    cliente_servidor(doc)
    mvc(doc)
    eventos(doc)
    combinacion(doc)


# ============================================================ 3. IMPLEMENTACIÓN
ESTRUCTURA = """backend/src/main/java/com/coralshop/
├─ auth/            config · controller · dto · service      (registro, sesión, seguridad)
├─ catalog/         controller · dto · model · repository · service
├─ customization/   controller · dto · model · repository · service
├─ design/          controller · dto · model · repository · service
├─ pricing/         controller · dto · model · service        (QuantityPolicy, PricingService)
├─ order/           controller · dto · model · repository · service
├─ payment/         controller · dto · model · repository · service
├─ address/         controller · dto · repository · service
├─ shipping/        controller · dto · repository · service
├─ user/            controller · dto · model · repository · service
├─ stats/           controller · dto · repository · service
├─ health/          controller · repository · service
└─ common/          dto (paginación) · exception (GlobalExceptionHandler)
backend/src/main/resources/db/migration/   V1 … V5 (Flyway)"""


def implementacion(doc):
    h(doc, 1, "3. Implementación del avance")
    h(doc, 2, "3.1 Estructura de paquetes")
    parrafo(doc,
            "El backend se organiza por funcionalidad y, dentro de cada una, por capa. Son 13 módulos y 118 clases; "
            "ningún paquete mezcla capas.")
    bloque_codigo(doc, ESTRUCTURA, size=8)

    h(doc, 2, "3.2 Endpoints implementados")
    tabla(doc, ["Método y ruta", "Acceso", "Para qué sirve"], [
        ("GET /api/products?type=&category=&q=&page=", "público", "Catálogo filtrado y paginado en el servidor"),
        ("GET /api/products/{id}/customization-options", "público", "Técnicas, zonas válidas con recargo y vista "
         "previa, escalas de mayoreo"),
        ("POST /api/quotes", "público", "Cotiza el carrito con precios recalculados y errores por línea"),
        ("POST /api/designs · GET /api/designs/{id}/image", "cliente", "Sube el diseño (PNG/JPG ≤ 5 MB) y lo "
         "muestra a su dueño o al administrador"),
        ("GET/POST/PUT/DELETE /api/addresses", "cliente", "Libreta de direcciones del Perú"),
        ("POST /api/orders", "cliente", "Crea el pedido en una sola transacción"),
        ("POST /api/orders/{code}/payment", "cliente", "Pago simulado detrás de la interfaz PaymentGateway"),
        ("GET /api/orders/me[/{code}]", "cliente", "Mis pedidos y su línea de tiempo"),
        ("GET /api/orders · PUT /api/orders/{id}/status", "admin", "Bandeja de pedidos y máquina de estados"),
        ("GET/PUT/PATCH /api/admin/products/{id}", "admin", "Edición y activación de productos"),
        ("POST/PUT/DELETE /api/categories", "admin", "Categorías; no se elimina una en uso"),
        ("GET /api/users · PUT /api/users/{id}/role", "admin", "Cuentas y roles"),
    ], anchos=[42, 12, 46], size=8.5)

    h(doc, 2, "3.3 Reglas de negocio implementadas")
    for texto, corte in [
        ("Precio en el servidor. Unitario = precio base + costo de la técnica + recargos de zona; el total de la "
         "línea aplica el descuento de la escala. El navegador nunca envía importes.", "Precio en el servidor."),
        ("Mayoreo por escalas. 1–2 unidades sin descuento, 3–5 con 5 %, 6–11 con 10 % y 12 o más con 15 %. Un "
         "paquete puede repartirse entre tallas y colores.", "Mayoreo por escalas."),
        ("Zonas por tipo de producto. Cada tipo define qué zona admite qué técnica; el bordado tiene menos zonas y "
         "tamaños más chicos que el estampado.", "Zonas por tipo de producto."),
        ("Stock sin sobreventa. Se descuenta con una actualización condicional; si dos clientes compran la última "
         "unidad a la vez, solo uno lo consigue.", "Stock sin sobreventa."),
        ("Máquina de estados. PENDIENTE_PAGO → PAGADO → EN_PRODUCCION → LISTO_PARA_ENVIO → ENVIADO → ENTREGADO, o "
         "CANCELADO desde los dos primeros; cancelar repone el stock y PAGADO solo se alcanza con un pago "
         "aprobado.", "Máquina de estados."),
        ("Pago seguro. El pedido queda bloqueado durante el cobro, no se puede pagar dos veces y los datos de la "
         "tarjeta no se guardan.", "Pago seguro."),
    ]:
        vineta(doc, texto, corte)

    h(doc, 2, "3.4 Modelo de datos")
    n_tablas, n_campos, n_fk = esquema.totales()
    parrafo(doc,
            f"La migración V5 completó el modelo: {n_tablas} tablas, {n_campos} campos y {n_fk} claves foráneas, "
            "agrupadas en cinco módulos. Los diagramas entidad-relación completos están en el Anexo A.")
    figura_apaisada(doc, "10_er_global.png", "Figura 6. Mapa global del modelo de datos.")

    h(doc, 2, "3.5 Pruebas y verificación")
    tabla(doc, ["Verificación", "Alcance", "Resultado"], [
        ("Pruebas unitarias (JUnit 5)", "QuantityPolicy, importes de línea, OrderStatusPolicy, detección del tipo "
         "de imagen y pasarela simulada", "40 de 40 en verde"),
        ("Recorrido de punta a punta", "Cotizar → subir diseño → pedido → pago rechazado y aprobado → admin hasta "
         "ENTREGADO, contra PostgreSQL", "64 de 64 controles"),
        ("Reglas rotas", "Cada regla violada responde 400, 404, 409 o 422 con un mensaje claro",
         "Incluido en los 64"),
        ("Frontend", "ESLint y build de producción", "Sin errores"),
    ], anchos=[24, 56, 20], size=9)
    salto_pagina(doc)


# ======================================================== 4 y 5. CIERRE
def proximos_pasos(doc):
    h(doc, 1, "4. Próximos pasos")
    for texto, corte in [
        ("Fase 3 · Frontend del flujo de compra. Personalizador con vista previa sobre la foto del producto, carrito "
         "por diseño, checkout con direcciones y envío, pago y «Mis pedidos».", "Fase 3 · Frontend del flujo de compra."),
        ("Fase 4 · Evento de dominio. Implementar OrderStatusChanged con sus suscriptores de notificación y "
         "auditoría (sección 2.4).", "Fase 4 · Evento de dominio."),
        ("Fase 5 · Calidad y demo. Datos de demostración ficticios, colección Postman, informe y presentación "
         "finales.", "Fase 5 · Calidad y demo."),
        ("Despliegue. Frontend en Vercel configurando la variable BACKEND_URL; el backend, en el servicio que se "
         "elija.", "Despliegue."),
    ]:
        vineta(doc, texto, corte)

    h(doc, 1, "5. Conclusiones")
    for texto in [
        "La arquitectura en capas no quedó solo en el papel: está en la estructura de paquetes y se puede comprobar "
        "en el código, porque ningún controller toca la base de datos y cada capa responde con su propio código de "
        "error.",
        "El modelo cliente-servidor, con el servidor como única autoridad sobre precios y stock, es lo que permite "
        "vender con seguridad aunque el navegador pueda ser manipulado.",
        "MVC se mantiene con una adaptación: la vista pasó del servidor (JSP) al navegador (React), y el controlador "
        "responde JSON. Eso permite que una misma API atienda a la tienda, al panel y a las pruebas.",
        "La arquitectura dirigida por eventos está diseñada pero no implementada; se incorporará en la fase 4, "
        "cuando hay un efecto concreto que desacoplar: avisar al cliente y auditar cada cambio de estado.",
    ]:
        vineta(doc, texto)
    salto_pagina(doc)


def anexos(doc):
    h(doc, 1, "Anexo A. Diagramas entidad-relación")
    parrafo(doc, "Modelo completo con todos los campos, generado desde el mismo esquema que crean las migraciones.")
    # Las dos figuras comparten una sola sección horizontal y el documento termina en ella,
    # para no dejar páginas verticales en blanco entre ambas ni al final.
    seccion_horizontal(doc)
    figura(doc, "08_er_usuarios_catalogo.png", "Figura A.1. Usuarios, catálogo e inventario.", ancho_pulgadas=9.0)
    salto_pagina(doc)
    figura(doc, "09_er_personalizacion_compra.png", "Figura A.2. Personalización, mayoreo, pedidos y pagos.",
           ancho_pulgadas=9.0)


def main():
    doc = nuevo_documento()
    caratula(doc, etiqueta="AVANCE 2  ·  ARQUITECTURA DE LA SOLUCIÓN")
    h(doc, 1, "Índice")
    indice(doc)
    salto_pagina(doc)
    introduccion(doc)
    patrones(doc)
    implementacion(doc)
    proximos_pasos(doc)
    anexos(doc)
    doc.save(SALIDA)
    print("Avance 2 generado:", SALIDA)


if __name__ == "__main__":
    main()
