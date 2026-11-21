# -*- coding: utf-8 -*-
"""Contenido textual del informe final, separado del código que arma el .docx.

Refleja la solución tal como quedó implementada (fases 0 a 5 de fases.md): Spring Boot 3.5,
React 19, PostgreSQL 16 y ejecución local. Los códigos de módulo (M01 a M12) son los del
mapa funcional (figuras.MODULOS_FIG)."""

# ---------------------------------------------------------------- portada
EMPRESA = "Coral Shop S.A.C."
TITULO = "Plataforma de comercio electrónico para la venta de ropa juvenil personalizable"
CURSO = "Desarrollo Web Integrado"
DOCENTE = "Joel Ronald Vilca Chambi"
CARRERA = "Ingeniería de Software"
CICLO = "2026"
GRUPO = "Grupo 1"
INTEGRANTES = [
    "Damián Valdivia, Diego Aarón",
    "Loayza Gerónimo, Juan Franco",
    "Villanueva Montalvo, Apolo Chris",
    "Campos Sulca, Jian Pier",
]

# ----------------------------------------------------------------- PESTEL
PESTEL = [
    ("Político",
     "Marco de promoción de la MYPE y del comercio electrónico (Ley 28015 y sus modificatorias). "
     "Fiscalización de INDECOPI sobre la información al consumidor y el Libro de Reclamaciones virtual.",
     "La tienda muestra el precio final desglosado antes de pagar (base, personalización, descuento y envío) y "
     "publica sus políticas de cambio, envío y privacidad en páginas propias."),
    ("Económico",
     "Crecimiento sostenido del comercio electrónico peruano y de las billeteras digitales. Al mismo tiempo, "
     "tipo de cambio volátil que encarece los insumos importados de estampado y bordado.",
     "Justifica invertir en un canal propio. Obliga a que los costos de cada técnica, los recargos por zona y "
     "los descuentos por volumen sean datos de la base (customization_techniques, product_type_zones, "
     "quantity_tiers) y no valores fijos en el código."),
    ("Social",
     "El público de 16 a 28 años valora la autoexpresión, compra desde el celular y encarga prendas en grupo "
     "(promociones, equipos, colectivos).",
     "Da origen al personalizador con vista previa (M03) y a la compra por mayor repartida entre tallas y "
     "colores (M04), además de una interfaz responsiva."),
    ("Tecnológico",
     "Estampado digital DTF y bordado accesibles para tiradas cortas. Ecosistema Java maduro (Spring Boot) y "
     "contenedores Docker que estandarizan la base de datos en cualquier equipo.",
     "Hace viable producir desde una unidad. Sustenta la elección de Spring Boot con Tomcat embebido y de "
     "PostgreSQL en Docker para que todo el equipo ejecute la misma versión en local."),
    ("Ecológico",
     "Presión por reducir el desperdicio textil y preferencia del consumidor joven por marcas responsables.",
     "Producir bajo demanda evita el sobrestock: el stock se reserva por variante al crear el pedido y se "
     "repone automáticamente si se cancela."),
    ("Legal",
     "Ley 29733 de Protección de Datos Personales y su reglamento. Responsabilidad sobre las imágenes que "
     "sube el cliente y sobre los datos de pago.",
     "Contraseñas con BCrypt, sesión protegida con CSRF, diseños visibles solo para su dueño y el "
     "administrador, y ningún dato de tarjeta guardado en la base. La demo usa solo datos ficticios."),
]

# ----------------------------------------------------------- FODA cruzado
FODA_CRUZADO = [
    ("Estrategias FO (ofensivas)",
     "F1+O4  Llevar el taller propio de estampado y bordado a la web con un personalizador con vista previa, "
     "algo que la competencia local aún no ofrece. Sustenta OE-2.\n"
     "F3+O2  Usar la comunidad de 24 mil seguidores para dirigir tráfico a la tienda propia y captar pedidos "
     "de promoción universitaria con precio por mayor. Sustenta OE-1 y OE-3.\n"
     "F5+O1  Ofrecer compra desde una unidad, imposible de igualar por proveedores que exigen mínimos."),
    ("Estrategias DO (adaptativas)",
     "D1+O1  Construir el canal de venta digital propio: es el núcleo del proyecto. Sustenta OE-1.\n"
     "D2+O5  Digitalizar el inventario por talla y color para vender solo lo que existe. Sustenta OE-3.\n"
     "D3+O4  Automatizar la cotización del estampado y del mayoreo con reglas configurables. Sustenta OE-2."),
    ("Estrategias FA (defensivas)",
     "F1+A1  Competir con los marketplaces por diferenciación (producto único) y no por logística.\n"
     "F2+A4  Al controlar el taller, absorber el alza de insumos ajustando los costos por técnica en la base, "
     "sin reprogramar el sistema.\n"
     "F4+A3  Usar el tablero y el historial de pedidos (OE-4) para planificar campañas en los meses valle."),
    ("Estrategias DA (de supervivencia)",
     "D4+A3  Implantar el seguimiento del pedido y la auditoría para dejar de operar a ciegas. Sustenta OE-4.\n"
     "D5+A1  Adoptar tecnologías de licencia libre (Java, Spring Boot, PostgreSQL, React) para contener el "
     "costo de la plataforma.\n"
     "D1+A5  Guardar los diseños de los clientes en la propia plataforma en lugar de en chats dispersos."),
]

# -------------------------------------------------------------- objetivos
OBJETIVO_GENERAL = (
    "Diseñar e implementar una plataforma web de comercio electrónico para Coral Shop S.A.C. que permita al "
    "cliente personalizar prendas juveniles en línea y comprarlas por unidad o por mayor, y a la empresa "
    "gestionar de forma integrada su catálogo, su inventario por talla y color y el ciclo completo del pedido, "
    "sustituyendo la operación actual basada en redes sociales y hojas de cálculo."
)

OBJETIVOS_ESPECIFICOS = [
    ("OE-1",
     "Implementar una tienda virtual que exponga el catálogo con stock real y permita completar la compra "
     "(carrito, checkout y pago) sin intervención manual del vendedor.",
     "Pedidos registrados por la web sobre el total de pedidos",
     "80 % al tercer mes",
     "M01, M02, M05, M06, M07"),
    ("OE-2",
     "Construir un personalizador de estampado y bordado que valide las zonas por tipo de prenda, guarde el "
     "diseño del cliente, muestre la vista previa y calcule el precio al instante.",
     "Tiempo entre la solicitud y la cotización del estampado",
     "De 6 horas a menos de 1 minuto",
     "M03, M04"),
    ("OE-3",
     "Gestionar el inventario a nivel de variante (producto, talla y color) y la venta por mayor con escalas de "
     "descuento, sin permitir sobreventa.",
     "Pedidos cancelados por falta de stock",
     "De 12 % a menos de 2 %",
     "M02, M04, M11"),
    ("OE-4",
     "Dar trazabilidad al pedido de punta a punta: estados controlados, historial, avisos al cliente, "
     "auditoría y tablero para la gerencia.",
     "Cambios de estado registrados y notificados",
     "100 %",
     "M08, M09, M10, M12"),
    ("OE-5",
     "Proteger las cuentas, los diseños y los datos de pago del cliente.",
     "Accesos indebidos a recursos ajenos en las pruebas de seguridad",
     "0",
     "M07, transversal"),
    ("OE-6",
     "Aplicar en la construcción la arquitectura en capas, cliente-servidor, MVC y dirigida por eventos vista "
     "en clase, con pruebas automatizadas.",
     "Pruebas automatizadas en verde",
     "100 % (73 de 73)",
     "Transversal"),
]

# ----------------------------------------------------------------- actores
ACTORES = [
    ("Invitado", "Persona sin sesión iniciada.",
     "Explora el catálogo, ve la ficha, configura el personalizador con vista previa local y arma su carrito. "
     "Para guardar el diseño y comprar debe iniciar sesión; el sistema lo devuelve al paso en que estaba."),
    ("Cliente", "Cuenta con rol ROLE_USER.",
     "Todo lo del invitado, más subir su diseño, gestionar direcciones, confirmar y pagar pedidos, revisar «Mis "
     "pedidos» con su línea de tiempo y recibir avisos en la campana."),
    ("Administrador", "Cuenta con rol ROLE_ADMIN (incluye ROLE_USER).",
     "Panel de administración: tablero, productos y variantes, categorías, bandeja de pedidos con cambio de "
     "estado, descarga de diseños y gestión de usuarios y roles. También puede comprar como cliente."),
    ("Sistema", "Procesos automáticos del backend.",
     "Recalcula precios, reserva y repone stock, genera el código del pedido y, ante cada cambio de estado, "
     "registra la auditoría y crea el aviso para el cliente."),
]

# --------------------------------------------------------------- modulos
MODULOS = [
    ("M01", "Catálogo", "Tienda",
     "Listado de productos activos con filtro por tipo y categoría, búsqueda y paginación en el servidor.",
     "RF-01 a RF-03"),
    ("M02", "Ficha de producto", "Tienda",
     "Galería, colores y tallas con el stock real de cada variante.", "RF-04, RF-05"),
    ("M03", "Personalizador", "Tienda",
     "Técnica (estampado o bordado), zonas válidas por tipo de prenda con su recargo, subida del diseño y "
     "vista previa sobre la silueta.", "RF-06 a RF-10"),
    ("M04", "Mayoreo y cotización", "Compra",
     "Reparto de un diseño entre tallas y colores, escalas de descuento y precio calculado por el servidor.",
     "RF-11 a RF-13"),
    ("M05", "Carrito", "Compra",
     "Una línea por diseño, guardada en el navegador y cotizada de nuevo al abrir el carrito o el checkout.",
     "RF-14, RF-15"),
    ("M06", "Checkout y pago", "Compra",
     "Método de envío, dirección, creación transaccional del pedido y pago simulado.", "RF-16 a RF-20"),
    ("M07", "Cuenta", "Cliente",
     "Registro, inicio y cierre de sesión, libreta de direcciones del Perú.", "RF-21 a RF-23"),
    ("M08", "Mis pedidos", "Cliente",
     "Historial del cliente, detalle con reparto por tallas y línea de tiempo de estados.", "RF-24, RF-25"),
    ("M09", "Notificaciones", "Cliente",
     "Campana con los avisos de cada cambio de estado; marcar uno o todos como leídos.", "RF-26, RF-27"),
    ("M10", "Tablero y usuarios", "Administración",
     "Indicadores de la tienda, pedidos recientes y gestión de roles.", "RF-28, RF-29"),
    ("M11", "Catálogo admin", "Administración",
     "Alta y edición de productos con sus variantes y stock, activación y categorías.", "RF-30 a RF-32"),
    ("M12", "Pedidos y auditoría", "Administración",
     "Bandeja filtrable, detalle con diseño descargable, cambio de estado permitido y auditoría automática.",
     "RF-33 a RF-36"),
]

# ------------------------------------------------ requerimientos funcionales
RF = [
    ("RF-01", "M01", "Listar los productos activos con imagen, nombre, tipo y precio base, paginados en el servidor (12 por página).", "Alta", "Invitado / Cliente"),
    ("RF-02", "M01", "Filtrar el catálogo por tipo de producto (polo, polera, gorra, tote) y por categoría, y buscar por texto libre en el nombre.", "Alta", "Invitado / Cliente"),
    ("RF-03", "M01", "Navegar por categorías desde el menú principal de la tienda.", "Media", "Invitado / Cliente"),
    ("RF-04", "M02", "Mostrar la ficha del producto con su descripción, galería y precio base.", "Alta", "Invitado / Cliente"),
    ("RF-05", "M02", "Mostrar los colores y tallas del producto con el stock disponible de cada variante.", "Alta", "Invitado / Cliente"),
    ("RF-06", "M03", "Ofrecer solo las técnicas (estampado, bordado) que admite el tipo de producto, con su costo.", "Alta", "Invitado / Cliente"),
    ("RF-07", "M03", "Ofrecer solo las zonas válidas para la técnica elegida, con su medida máxima y su recargo.", "Alta", "Invitado / Cliente"),
    ("RF-08", "M03", "Subir el diseño del cliente (PNG o JPG de hasta 5 MB), validando el tipo real del archivo por su cabecera.", "Alta", "Cliente"),
    ("RF-09", "M03", "Mostrar la vista previa del diseño sobre la silueta de la prenda en cada zona elegida, de frente y de espalda.", "Alta", "Invitado / Cliente"),
    ("RF-10", "M03", "Conservar el borrador del personalizador si el invitado debe iniciar sesión a mitad del proceso.", "Media", "Invitado"),
    ("RF-11", "M04", "Repartir la cantidad de un mismo diseño entre tallas y colores en una tabla, con botones rápidos de 1, 3, 6 y 12.", "Alta", "Invitado / Cliente"),
    ("RF-12", "M04", "Aplicar la escala de descuento más alta alcanzada por la cantidad total del diseño e indicar cuánto falta para la siguiente.", "Alta", "Invitado / Cliente"),
    ("RF-13", "M04", "Cotizar en el servidor cada línea (base + técnica + zonas − descuento) y devolver errores por línea.", "Alta", "Sistema"),
    ("RF-14", "M05", "Agregar, modificar y quitar líneas del carrito; un mismo diseño agregado dos veces suma sus cantidades.", "Alta", "Invitado / Cliente"),
    ("RF-15", "M05", "Recotizar el carrito al abrirlo y bloquear el pago si alguna línea dejó de ser válida.", "Alta", "Sistema"),
    ("RF-16", "M06", "Elegir el método de envío (recojo en tienda, Lima Metropolitana o provincias) con su costo y plazo.", "Alta", "Cliente"),
    ("RF-17", "M06", "Elegir una dirección guardada o registrar una nueva durante el checkout.", "Alta", "Cliente"),
    ("RF-18", "M06", "Crear el pedido en una sola transacción: validar reglas, recalcular precios, reservar stock y registrar el historial.", "Alta", "Sistema"),
    ("RF-19", "M06", "Pagar el pedido con el pago simulado; un rechazo queda registrado y permite reintentar.", "Alta", "Cliente"),
    ("RF-20", "M06", "Mostrar la confirmación con el código del pedido, el resumen y el siguiente paso.", "Media", "Cliente"),
    ("RF-21", "M07", "Registrar una cuenta con nombre, apellido, correo y contraseña de al menos 8 caracteres.", "Alta", "Invitado"),
    ("RF-22", "M07", "Iniciar y cerrar sesión; tras el login volver a la pantalla que la pidió.", "Alta", "Invitado / Cliente"),
    ("RF-23", "M07", "Crear, editar, eliminar y marcar como principal las direcciones (departamento, provincia y distrito).", "Media", "Cliente"),
    ("RF-24", "M08", "Listar los pedidos del cliente con su estado, unidades y total.", "Alta", "Cliente"),
    ("RF-25", "M08", "Mostrar el detalle del pedido con el diseño, el reparto por tallas y la línea de tiempo de estados.", "Alta", "Cliente"),
    ("RF-26", "M09", "Crear un aviso para el cliente en cada cambio de estado de su pedido.", "Alta", "Sistema"),
    ("RF-27", "M09", "Mostrar los avisos no leídos en la campana y marcarlos como leídos, uno a uno o todos.", "Media", "Cliente"),
    ("RF-28", "M10", "Mostrar el tablero con usuarios, productos, pedidos, ingresos de pedidos entregados y pedidos recientes.", "Media", "Administrador"),
    ("RF-29", "M10", "Listar los usuarios y cambiar su rol; un administrador no puede cambiar su propio rol.", "Media", "Administrador"),
    ("RF-30", "M11", "Crear y editar productos con tipo, categoría, precio base, imágenes y la condición de personalizable.", "Alta", "Administrador"),
    ("RF-31", "M11", "Gestionar las variantes (talla, color, SKU y stock) y activar o desactivar productos.", "Alta", "Administrador"),
    ("RF-32", "M11", "Crear, editar y eliminar categorías; no se elimina una categoría en uso.", "Media", "Administrador"),
    ("RF-33", "M12", "Listar los pedidos filtrando por estado, con paginación.", "Alta", "Administrador"),
    ("RF-34", "M12", "Ver el detalle del pedido con el cliente, la entrega, los pagos y descargar el diseño.", "Alta", "Administrador"),
    ("RF-35", "M12", "Cambiar el estado solo a los estados permitidos, con comentario opcional; cancelar repone el stock.", "Alta", "Administrador"),
    ("RF-36", "M12", "Registrar en audit_log cada cambio de estado con su autor, dentro de la misma transacción.", "Alta", "Sistema"),
]

# ----------------------------------------------------- requerimientos no funcionales
RNF = [
    ("RNF-01", "Seguridad",
     "Las contraseñas se guardan como hash BCrypt; nunca se almacena ni se devuelve la contraseña en claro."),
    ("RNF-02", "Seguridad",
     "La sesión es de servidor (cookie JSESSIONID de Spring Security) y toda escritura exige el token CSRF en la "
     "cabecera X-CSRF-TOKEN."),
    ("RNF-03", "Seguridad",
     "Autorización por rol en una sola configuración (SecurityConfig): sin sesión responde 401, sin permiso 403, "
     "y un recurso ajeno (pedido, diseño, aviso) responde 404."),
    ("RNF-04", "Seguridad",
     "Todo acceso a datos usa JdbcTemplate o JPA con parámetros; queda prohibido concatenar valores en el SQL."),
    ("RNF-05", "Integridad",
     "El servidor recalcula siempre precios y stock: nunca acepta importes enviados por el navegador."),
    ("RNF-06", "Integridad",
     "Crear un pedido, pagarlo y cambiar su estado son operaciones transaccionales: se confirman completas o se "
     "deshacen."),
    ("RNF-07", "Integridad",
     "La base protege sus propias reglas con claves foráneas, CHECK e índices únicos (por ejemplo, un solo pago "
     "aprobado por pedido)."),
    ("RNF-08", "Usabilidad",
     "Interfaz en español, precios en soles (S/) y mensajes de error claros junto al campo o la línea que falló."),
    ("RNF-09", "Usabilidad",
     "Interfaz responsiva para el público joven que compra desde el celular."),
    ("RNF-10", "Rendimiento",
     "Catálogo y bandeja de pedidos paginados en el servidor (máximo 100 elementos por página) e índices sobre las "
     "columnas de búsqueda."),
    ("RNF-11", "Mantenibilidad",
     "Paquetes por funcionalidad y, dentro de cada una, por capa (controller, service, repository, dto, model); "
     "ningún controller accede a la base de datos."),
    ("RNF-12", "Mantenibilidad",
     "Todo cambio de esquema es una migración Flyway nueva (V1 a V6); nunca se edita una migración aplicada."),
    ("RNF-13", "Trazabilidad",
     "Cada cambio de estado del pedido queda en order_status_history y en audit_log con su autor y fecha."),
    ("RNF-14", "Portabilidad",
     "El proyecto se levanta en local con PostgreSQL en Docker, el backend con Maven y el frontend con Vite, "
     "siguiendo la guía del README."),
    ("RNF-15", "Calidad",
     "73 pruebas automatizadas (JUnit 5 y Testcontainers con PostgreSQL real) y colección Postman de toda la API."),
]

# ------------------------------------------------------- reglas de negocio
REGLAS = [
    ("RN-01", "El stock pertenece a la variante (producto + talla + color), no al producto."),
    ("RN-02", "Precio unitario = precio base del producto + costo base de la técnica + suma de los recargos de las "
              "zonas elegidas."),
    ("RN-03", "La cantidad de un diseño es libre (≥ 1) y se aplica la escala más alta alcanzada: 1–2 sin "
              "descuento, 3–5 con 5 %, 6–11 con 10 % y 12 o más con 15 %."),
    ("RN-04", "Un paquete comparte diseño, técnica y zonas, pero puede repartirse entre tallas y colores; la suma "
              "del reparto debe igualar la cantidad de la línea."),
    ("RN-05", "Cada tipo de producto define qué zona admite qué técnica; el bordado solo se ofrece en zonas "
              "pequeñas (pecho izquierdo, mangas, gorra y cara A del tote)."),
    ("RN-06", "Un producto personalizable se compra siempre con técnica, al menos una zona y un diseño del propio "
              "cliente."),
    ("RN-07", "El diseño es PNG o JPG de hasta 5 MB; el tipo se verifica por la cabecera del archivo, no por la "
              "extensión."),
    ("RN-08", "El stock se descuenta al crear el pedido con una actualización condicional; si una talla no "
              "alcanza, la transacción completa se deshace (409)."),
    ("RN-09", "Los datos del pedido (nombre, SKU, talla, color, precios y dirección) se copian al comprar: el "
              "pedido no cambia si el catálogo o la dirección cambian después."),
    ("RN-10", "Estados válidos: PENDIENTE_PAGO → PAGADO → EN_PRODUCCION → LISTO_PARA_ENVIO → ENVIADO → "
              "ENTREGADO; CANCELADO solo desde PENDIENTE_PAGO o PAGADO, y repone el stock."),
    ("RN-11", "PAGADO solo se alcanza con un pago aprobado; un pedido no se paga dos veces y los datos de la "
              "tarjeta nunca se guardan."),
    ("RN-12", "El envío a domicilio exige una dirección completa; el recojo en tienda solo nombre y teléfono."),
    ("RN-13", "El código del pedido es CS- seguido de 8 caracteres aleatorios sin caracteres ambiguos (0, O, 1, I)."),
    ("RN-14", "Cada cambio de estado se audita en la misma transacción y genera un aviso para el cliente."),
]

# ----------------------------------------------------- historias de usuario
HISTORIAS = [
    ("HU-01", "M03",
     "Como cliente quiero elegir la técnica y las zonas de mi polo y ver solo las que esa prenda admite, para "
     "no pedir algo que el taller no puede hacer.",
     "Dado un polo, cuando elijo Bordado, entonces solo se ofrecen pecho izquierdo y mangas, cada una con su "
     "medida máxima y su recargo.\n"
     "Dado que cambio a Estampado, entonces aparecen también pecho centro y espalda, y las zonas que ya no "
     "aplican se desmarcan."),
    ("HU-02", "M03",
     "Como cliente quiero subir mi logo y verlo sobre la prenda antes de pagar, para estar seguro de lo que "
     "voy a recibir.",
     "Dado que subo un PNG de 2 MB, cuando termina la subida, entonces veo «Diseño guardado» y el logo dentro "
     "del recuadro de cada zona elegida, de frente o de espalda.\n"
     "Dado que subo un archivo de más de 5 MB o un PDF renombrado a .png, entonces el sistema lo rechaza con el "
     "motivo y conserva el resto de mi configuración."),
    ("HU-03", "M03",
     "Como invitado quiero armar mi diseño sin haber iniciado sesión, para decidir sin fricción.",
     "Dado que configuro color, técnica, zonas y cantidades sin sesión, cuando inicio sesión, entonces vuelvo a "
     "la ficha con mis elecciones conservadas y solo debo elegir la imagen otra vez."),
    ("HU-04", "M04",
     "Como delegado de mi promoción quiero pedir 12 polos con el mismo logo repartidos en tallas S, M y L, para "
     "pagar precio de docena aunque las tallas sean distintas.",
     "Dado un diseño con 4 S, 4 M y 4 L, cuando reviso el precio, entonces el total aplica la escala de 12 "
     "(−15 %): 12 × S/ 58.00 − S/ 104.40 = S/ 591.60.\n"
     "Dado que llevo 9 unidades, entonces se aplica la escala de 6 (−10 %) y el sistema indica que faltan 3 "
     "para la docena."),
    ("HU-05", "M04",
     "Como cliente quiero que el precio que veo sea el que realmente pago, para confiar en la tienda.",
     "Dado que alguien modifica el importe en el navegador, cuando se crea el pedido, entonces el servidor lo "
     "recalcula con los precios de la base e ignora el valor enviado."),
    ("HU-06", "M02",
     "Como cliente quiero ver cuántas unidades quedan de cada talla y color, para no comprar algo que luego me "
     "cancelen.",
     "Dado que una variante tiene 26 unidades, cuando reparto cantidades, entonces veo «quedan 26» y no puedo "
     "confirmar más de lo disponible.\n"
     "Dado que otro cliente compra la última unidad antes que yo, cuando confirmo, entonces recibo 409 con la "
     "talla afectada y no se crea ningún pedido."),
    ("HU-07", "M06",
     "Como cliente quiero confirmar mi pedido eligiendo el envío y la dirección, y pagarlo con tarjeta, para "
     "terminar la compra sin escribir por chat.",
     "Dado un carrito válido, cuando elijo Lima Metropolitana y mi dirección principal y confirmo, entonces se "
     "crea el pedido CS-… en PENDIENTE_PAGO, el carrito se vacía y se abre el pago.\n"
     "Dado que la tarjeta es rechazada, entonces el pedido sigue pendiente, el rechazo queda registrado y puedo "
     "reintentar desde el checkout o desde «Mis pedidos»."),
    ("HU-08", "M08",
     "Como cliente quiero ver en qué etapa está mi pedido, para saber cuándo llegará.",
     "Dado un pedido ENTREGADO, cuando abro su detalle, entonces veo la línea de tiempo completa con la fecha "
     "de cada estado y el reparto por tallas."),
    ("HU-09", "M09",
     "Como cliente quiero recibir un aviso cuando mi pedido cambie de estado, para no tener que preguntar.",
     "Dado que el administrador pasa mi pedido a EN_PRODUCCION, cuando vuelvo a la tienda, entonces la campana "
     "muestra un aviso no leído que al abrirlo me lleva al pedido."),
    ("HU-10", "M12",
     "Como administrador quiero avanzar los pedidos solo por las etapas válidas y descargar el diseño del "
     "cliente, para producir sin errores.",
     "Dado un pedido PAGADO, cuando abro el selector, entonces solo puedo elegir En producción o Cancelado.\n"
     "Dado que cancelo un pedido pagado, entonces el stock de cada talla se repone y el cambio queda auditado "
     "con mi nombre."),
]

# ------------------------------------------------------------- tecnologías
TECNOLOGIAS = [
    ("Vista", "React 19 + Vite 8 + Tailwind 4 + React Router 7",
     "SPA que actualiza el precio y la vista previa del personalizador sin recargar la página. Un único "
     "cliente HTTP (http-client.js) maneja la cookie de sesión, el token CSRF y los errores de la API.",
     "Clase 4 (MVC): ocupa el lugar de la JSP"),
    ("Lenguaje", "Java 21 (LTS)",
     "Versión con soporte extendido. Los records permiten DTO y objetos de modelo inmutables sin código "
     "repetitivo.",
     "S01 - Arquitectura Java"),
    ("Controlador y contenedor", "Spring Boot 3.5 (Spring MVC) con Tomcat embebido",
     "Spring MVC se apoya en un único Servlet, el DispatcherServlet, que reparte cada petición al "
     "@RestController correspondiente. Tomcat, el contenedor web visto en clase, viaja dentro de la aplicación.",
     "S01 (Servlet = Controlador) y S02 (Web Container)"),
    ("Acceso a datos", "Spring JDBC (JdbcTemplate) + JPA solo para la cuenta",
     "JdbcTemplate es JDBC con PreparedStatement, pool de conexiones y cierre automático de recursos. Se usa en "
     "todo el negocio para controlar el SQL (actualización condicional de stock, SELECT … FOR UPDATE).",
     "S03 - JDBC"),
    ("Base de datos", "PostgreSQL 16 en Docker + Flyway",
     "Integridad referencial, CHECK, índices únicos parciales y bytea para los diseños. Flyway versiona el "
     "esquema con las migraciones V1 a V6.",
     "S03 - JDBC"),
    ("Seguridad", "Spring Security: sesión, BCrypt, CSRF y roles",
     "La sesión de servidor reutiliza el session scope y la cookie JSESSIONID de clase; CSRF protege toda "
     "escritura; ROLE_ADMIN incluye a ROLE_USER.",
     "Clase 4 - Session"),
    ("Eventos", "ApplicationEventPublisher y @TransactionalEventListener",
     "Bus de eventos dentro del mismo proceso: auditoría y avisos sin acoplar a quien publica.",
     "Patrones de arquitectura (eventos)"),
    ("Documentación de la API", "springdoc-openapi (Swagger UI) + Postman",
     "Swagger UI en /api/docs describe y prueba cada endpoint; la colección Postman recorre la historia de "
     "referencia completa.",
     "Metodología del curso"),
    ("Pruebas", "JUnit 5 + Spring Boot Test + Testcontainers",
     "Pruebas unitarias de las reglas puras y de integración contra un PostgreSQL real levantado en Docker.",
     "TDD (rojo, verde, refactor)"),
    ("Herramientas", "Maven Wrapper, npm, Git y GitHub, IntelliJ IDEA",
     "Configuraciones de ejecución compartidas (.run/) para levantar backend y frontend con un clic.",
     "Decisión del equipo"),
]

# ------------------------------------------------------------- endpoints
ENDPOINTS = [
    ("GET", "/api/products", "público", "Catálogo con filtros type, category, q y paginación", "CatalogController"),
    ("GET", "/api/products/{id}", "público", "Ficha con variantes y stock", "CatalogController"),
    ("GET", "/api/categories · /api/product-types", "público", "Categorías y tipos de producto", "CatalogController"),
    ("GET", "/api/products/{id}/customization-options", "público", "Técnicas, zonas con recargo y vista previa, escalas", "CustomizationController"),
    ("POST", "/api/quotes", "público", "Cotiza las líneas del carrito con errores por línea", "QuoteController"),
    ("POST", "/api/auth/register", "público", "Registro de cuenta", "AuthController"),
    ("POST", "/api/auth/login · /logout", "público", "Inicio y cierre de sesión (Spring Security)", "SecurityConfig"),
    ("GET", "/api/auth/csrf · /api/auth/me", "público / sesión", "Token CSRF y usuario autenticado", "AuthController"),
    ("POST", "/api/designs", "cliente", "Sube el diseño (multipart, PNG/JPG ≤ 5 MB)", "DesignController"),
    ("GET", "/api/designs/{id}/image", "dueño o admin", "Imagen del diseño", "DesignController"),
    ("CRUD", "/api/addresses[/{id}]", "cliente", "Libreta de direcciones", "AddressController"),
    ("GET", "/api/shipping-methods", "público", "Métodos de envío", "ShippingController"),
    ("POST", "/api/orders", "cliente", "Crea el pedido en una transacción", "CustomerOrderController"),
    ("POST", "/api/orders/{code}/payment", "cliente dueño", "Pago simulado", "PaymentController"),
    ("GET", "/api/orders/me[/{code}]", "cliente", "Mis pedidos y su detalle", "CustomerOrderController"),
    ("GET · PUT", "/api/notifications/me · /{id}/read · /me/read", "cliente", "Avisos y marcarlos como leídos", "NotificationController"),
    ("GET", "/api/orders · /api/orders/{id}", "admin", "Bandeja y detalle de pedidos", "AdminOrderController"),
    ("PUT", "/api/orders/{id}/status", "admin", "Cambio de estado con la máquina de estados", "AdminOrderController"),
    ("GET · POST · PUT · PATCH", "/api/admin/products[/{id}]", "admin", "Productos, variantes y activación", "AdminProductController"),
    ("POST · PUT · DELETE", "/api/categories[/{id}]", "admin", "Categorías", "AdminCategoryController"),
    ("GET · PUT", "/api/users · /api/users/{id}/role", "admin", "Usuarios y roles", "UserAdminController"),
    ("GET", "/api/stats/overview", "admin", "Indicadores del tablero", "StatsController"),
]

# ------------------------------------------------------------- paquetes
ARBOL_PAQUETES = """backend/src/main/java/com/coralshop/
├─ catalog/         controller · dto · model · repository · service   (catálogo y admin de productos)
├─ customization/   controller · dto · model · repository · service   (técnicas, zonas, escalas)
├─ design/          controller · dto · model · repository · service   (diseños del cliente)
├─ pricing/         controller · dto · model · service                (PricingService, QuantityPolicy)
├─ order/           controller · dto · event · model · repository · service
├─ payment/         controller · dto · model · repository · service   (PaymentGateway)
├─ notification/    controller · dto · listener · repository · service
├─ audit/           listener · repository
├─ address/  shipping/  user/  stats/  health/   (cada uno con sus capas)
├─ auth/            config · controller · dto · service              (SecurityConfig, registro)
├─ demo/            config · service                                 (datos ficticios, perfil demo)
├─ docs/            config                                           (OpenAPI / Swagger)
└─ common/          dto (paginación) · exception (GlobalExceptionHandler)
backend/src/main/resources/db/migration/     V1 … V6 (Flyway)
backend/src/test/java/com/coralshop/         pruebas unitarias e integración (Testcontainers)

frontend/src/
├─ app/             router, layouts y guardas de sesión
├─ pages/           home · products · product-detail · cart · checkout · orders · account · login …
├─ features/        products · customization · cart · checkout · orders · notifications · auth · admin
│                   (cada una con api/ · components/ · hooks/ · model/)
└─ shared/          api/http-client.js · components · hooks · utils"""

# ------------------------------------------------------------- clases
CLASES = [
    ("controller", "CatalogController, CustomizationController, QuoteController, DesignController, "
     "CustomerOrderController, PaymentController, AdminOrderController, AdminProductController, "
     "AdminCategoryController, AddressController, NotificationController, UserAdminController, StatsController",
     "Reciben HTTP, validan el formato con DTO + @Valid y delegan en el service. Ninguno accede a la base."),
    ("dto", "CreateOrderRequest, CartLineRequest, QuoteResponse, ProductView, OrderDetailView, "
     "AddressRequest, PaymentRequest, NotificationsResponse, PageResponse …",
     "Records inmutables con la forma exacta de la API; nunca exponen la contraseña ni la tarjeta."),
    ("service", "PricingService, QuantityPolicy, OrderService, OrderStatusPolicy, OrderAdminService, "
     "PaymentService, SimulatedPaymentGateway, DesignService, ImageTypeDetector, CatalogService, "
     "ProductAdminService, NotificationService …",
     "Reglas de negocio y transacciones (@Transactional). Lanzan BusinessRuleException (422), "
     "ConflictException (409) o NotFoundException (404)."),
    ("repository", "ProductRepository, CustomizationRepository, DesignRepository, OrderRepository, "
     "PaymentRepository, NotificationRepository, AuditRepository, AddressRepository, UserRepository (JPA)",
     "Único lugar con SQL, siempre con parámetros."),
    ("model", "PricedLine, LineAmounts, LineSpec, NewOrder, OrderStatus, QuantityTier, ZoneRule, Technique, "
     "DesignImage, PaymentCharge, PaymentResult, User, Role",
     "Objetos de datos del dominio compartidos por las capas."),
    ("event / listener", "OrderStatusChanged, AuditListener, NotificationListener",
     "Evento de dominio y sus dos suscriptores."),
    ("common / config", "GlobalExceptionHandler, ApiError, SecurityConfig, PasswordConfig, OpenApiConfig, "
     "DemoDataInitializer",
     "Aspectos transversales: errores uniformes, seguridad, documentación y datos demo."),
]

# --------------------------------------------- algoritmos y estructuras
ALGORITMOS = [
    ("Validar transiciones de estado", "EnumMap<OrderStatus, EnumSet<OrderStatus>>",
     "Búsqueda en O(1) del conjunto de estados siguientes; agregar un estado no exige tocar condicionales "
     "anidados.", "OrderStatusPolicy, RN-10"),
    ("Elegir la escala de mayoreo", "Recorrido con filtro y máximo (Stream.filter + max)",
     "Elige la escala con mayor cantidad mínima que no supere la cantidad; con 4 escalas es O(n) trivial y "
     "las escalas viven en la base.", "QuantityPolicy, RN-03"),
    ("Agrupar zonas por técnica", "Map<String, List<ZoneRule>> (Collectors.groupingBy)",
     "Arma de una sola consulta las opciones del personalizador por técnica.", "CustomizationService, RF-07"),
    ("Reservar stock sin sobreventa", "UPDATE … SET stock = stock − ? WHERE id = ? AND stock >= ?",
     "Operación atómica en la base: si devuelve 0 filas no hay stock y se deshace la transacción. Evita leer y "
     "luego escribir.", "OrderRepository, RN-08"),
    ("Evitar dobles pagos", "SELECT … FOR UPDATE sobre el pedido",
     "Bloquea la fila mientras se cobra; un segundo pago concurrente espera y ya ve el pedido PAGADO.",
     "PaymentService, RN-11"),
    ("Validar la tarjeta de prueba", "Algoritmo de Luhn (suma de dígitos con duplicado alterno)",
     "Rechaza números mal formados en O(n) sin llamar a ningún proveedor.", "SimulatedPaymentGateway"),
    ("Detectar el tipo real del diseño", "Comparación de bytes mágicos (firma PNG 89 50 4E 47, JPG FF D8 FF)",
     "La extensión del archivo puede mentir; la cabecera no.", "ImageTypeDetector, RN-07"),
    ("Identificar diseños", "Hash SHA-256 (MessageDigest)",
     "Huella de 64 caracteres guardada con cada diseño para su trazabilidad.", "DesignService"),
    ("Generar el código del pedido", "SecureRandom sobre un alfabeto de 32 caracteres",
     "8 caracteres dan 32⁸ ≈ 1,1 × 10¹² combinaciones, impredecibles, y sin caracteres que se confundan al "
     "dictarlos.", "OrderService, RN-13"),
    ("Errores por campo en orden", "LinkedHashMap<String, String>",
     "Conserva el orden de los campos del formulario en la respuesta de error.", "GlobalExceptionHandler"),
    ("Entregar el evento una sola vez", "Clave única event_id + INSERT … ON CONFLICT DO NOTHING",
     "Idempotencia: un evento repetido no duplica auditoría ni avisos.", "AuditListener, NotificationListener"),
]

# ------------------------------------------------------------- cronograma
CRONOGRAMA = [
    ("Diagnóstico", "Set. 2026", "Análisis del negocio y diseño inicial",
     "Diagnóstico estratégico, funcionalidades, arquitectura y modelo de datos (entregable 1).", "Completado"),
    ("Fase 0", "Oct. 2026", "Ordenar la casa",
     "Limpieza del frontend, interfaz en español y soles, backend en capas y errores uniformes.", "Completado"),
    ("Fase 1", "Oct. 2026", "Modelo de datos del negocio",
     "Migración V5: tipos de producto, personalización, mayoreo, direcciones, pedidos y pagos.", "Completado"),
    ("Fase 2", "Oct. 2026", "API del flujo de compra",
     "Catálogo, personalizador, diseños, cotización, pedidos, pago simulado y administración.", "Completado"),
    ("Fase 3", "Oct. 2026", "Frontend del flujo de compra",
     "Personalizador con vista previa, carrito, checkout, confirmación, «Mis pedidos» y bandeja admin.",
     "Completado"),
    ("Fase 4", "Oct. 2026", "Evento de dominio",
     "OrderStatusChanged con auditoría, notificaciones y campana (migración V6). Avance 2.", "Completado"),
    ("Fase 5", "Oct.–Nov. 2026", "Calidad, demo y documentación",
     "73 pruebas, perfil demo, Swagger y Postman, capturas reales, informe y presentación finales.",
     "Completado"),
    ("Exposición", "Semana 18", "Demostración",
     "Exposición de 20 minutos con demo en vivo en local y ronda de preguntas.", "Pendiente"),
]

GLOSARIO = [
    ("Bytes mágicos", "Primeros bytes de un archivo que identifican su formato real (por ejemplo, la firma PNG)."),
    ("CSRF", "Cross-Site Request Forgery. Ataque en que otra página envía peticiones con la sesión del usuario; "
     "se previene con un token que solo conoce la tienda."),
    ("Contenedor web", "Componente que implementa la API de Servlets y gestiona su ciclo de vida. Aquí, Tomcat "
     "embebido en Spring Boot."),
    ("DispatcherServlet", "Servlet único de Spring MVC que recibe todas las peticiones y las reparte a los "
     "@RestController."),
    ("DTF", "Direct to Film. Técnica de estampado digital para tiradas cortas a todo color."),
    ("DTO", "Data Transfer Object. Objeto que transporta datos entre capas con la forma que necesita la API."),
    ("Escala de mayoreo", "Tramo de cantidad (1, 3, 6 o 12) que fija el porcentaje de descuento de un diseño."),
    ("Evento de dominio", "Hecho relevante del negocio («el pedido cambió de estado») que otros componentes "
     "escuchan sin que quien lo publica los conozca."),
    ("Flyway", "Herramienta que versiona el esquema de la base con migraciones numeradas."),
    ("JdbcTemplate", "Clase de Spring que ejecuta SQL sobre JDBC con parámetros y libera los recursos sola."),
    ("JSESSIONID", "Cookie con la que el servidor identifica la sesión de un navegador."),
    ("MVC", "Modelo, Vista y Controlador. Patrón que separa datos y reglas, presentación y coordinación."),
    ("Record", "Tipo de Java que declara una clase inmutable de solo datos en una línea."),
    ("SKU", "Stock Keeping Unit. Código único de una variante del almacén."),
    ("SPA", "Single Page Application. Aplicación web que actualiza la vista sin recargar la página."),
    ("Testcontainers", "Biblioteca que levanta servicios reales (aquí PostgreSQL) en Docker durante las pruebas."),
    ("Variante", "Combinación de producto, talla y color. Es la unidad que tiene stock y SKU."),
]

REFERENCIAS = [
    "Fowler, M. (2003). Patterns of Enterprise Application Architecture. Addison-Wesley.",
    "Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1995). Design Patterns: Elements of Reusable "
    "Object-Oriented Software. Addison-Wesley.",
    "Medina Cabrera, R. (2026). Sesión 01: Arquitectura Java [Material del curso Desarrollo Web Integrado]. "
    "Universidad Tecnológica del Perú.",
    "Medina Cabrera, R. (2026). Sesión 02: Tecnología Web, Web Container [Material del curso Desarrollo Web "
    "Integrado]. Universidad Tecnológica del Perú.",
    "Medina Cabrera, R. (2026). Semana 03: Java Database Connectivity [Material del curso Desarrollo Web "
    "Integrado]. Universidad Tecnológica del Perú.",
    "Medina Cabrera, R. (2026). Clase 04: Java Server Pages y MVC [Material del curso Desarrollo Web "
    "Integrado]. Universidad Tecnológica del Perú.",
    "Oracle. (2024). Java Platform, Standard Edition 21 Documentation. https://docs.oracle.com/en/java/javase/21/",
    "Osterwalder, A. y Pigneur, Y. (2011). Generación de modelos de negocio. Deusto.",
    "PostgreSQL Global Development Group. (2024). PostgreSQL 16 Documentation. https://www.postgresql.org/docs/16/",
    "React Team. (2024). React Documentation. https://react.dev/",
    "Richards, M. y Ford, N. (2020). Fundamentals of Software Architecture. O'Reilly Media.",
    "VMware. (2025). Spring Boot Reference Documentation 3.5. https://docs.spring.io/spring-boot/",
    "VMware. (2025). Spring Security Reference. https://docs.spring.io/spring-security/reference/",
]
