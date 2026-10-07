# -*- coding: utf-8 -*-
"""Contenido textual del informe, separado del código que arma el .docx."""

# ---------------------------------------------------------------- portada
EMPRESA = "Coral Shop S.A.C."
TITULO = "Plataforma de comercio electrónico para la venta de ropa juvenil personalizable"
CURSO = "Desarrollo Web Integrado"
DOCENTE = "Joel Ronald Vilca Chambi"
CARRERA = "Ingeniería de Software"
CICLO = "2026"
GRUPO = "Grupo 1"
INTEGRANTES = [
    "Choquehuanca Marrufo, Liam Lennon",
    "Damián Valdivia, Diego Aarón",
    "Loayza Gerónimo, Juan Franco",
    "Villanueva Montalvo, Apolo Chris",
    "Campos Sulca, Jian Pier",
]

# ----------------------------------------------------------------- PESTEL
PESTEL = [
    ("Político",
     "Marco de promoción de la MYPE y del comercio electrónico (Ley 28015 y sus modificatorias). "
     "Fiscalización de INDECOPI sobre el Libro de Reclamaciones virtual y la información al consumidor.",
     "La plataforma debe emitir comprobante de la operación, publicar políticas de cambio y devolución, "
     "y habilitar un canal de reclamos. Se incorpora como requerimiento no funcional de cumplimiento."),
    ("Económico",
     "Crecimiento sostenido del comercio electrónico peruano y de la penetración de billeteras digitales. "
     "Al mismo tiempo, tipo de cambio volátil que encarece los insumos importados de estampado.",
     "Justifica invertir en canal propio y aceptar Yape y Plin. Obliga a que el precio del estampado sea "
     "un dato configurable en base de datos (print_technique.base_cost) y no un valor fijo en el código."),
    ("Social",
     "El público de 16 a 28 años valora la autoexpresión y la personalización, compra desde el celular y "
     "confía en las reseñas de otros compradores antes de decidir.",
     "Da origen a los módulos de personalizador (M03), reseñas de comprador verificado (M09) y a la "
     "exigencia de diseño responsivo mobile first."),
    ("Tecnológico",
     "Estampado digital DTF accesible para tiradas cortas. Ecosistema Java EE maduro para aplicaciones web "
     "y contenedores que estandarizan el despliegue.",
     "Hace viable producir desde una unidad, lo que sustenta la propuesta de valor. Sustenta la elección de "
     "Tomcat como contenedor web y de Docker para el despliegue."),
    ("Ecológico",
     "Presión creciente por reducir el desperdicio textil y preferencia del consumidor joven por marcas "
     "responsables.",
     "Producir bajo demanda evita el sobrestock. El flujo de aprobación del arte (M15) reduce las mermas por "
     "estampados mal ejecutados, un indicador que el sistema debe poder medir."),
    ("Legal",
     "Ley 29733 de Protección de Datos Personales y su reglamento. Responsabilidad sobre el uso de imágenes "
     "con derechos de autor que suba el cliente.",
     "Obliga a cifrar credenciales con BCrypt, a pedir consentimiento explícito y a incluir en el "
     "personalizador una declaración de titularidad del arte, además de la bitácora de auditoría (M20)."),
]

# ----------------------------------------------------------- FODA cruzado
FODA_CRUZADO = [
    ("Estrategias FO (ofensivas)",
     "F1+O4  Llevar el taller propio de estampado a la web con un personalizador en línea con vista previa, "
     "algo que la competencia local aun no ofrece. Sustenta OE-2.\n"
     "F3+O2  Usar la comunidad de 24 mil seguidores para dirigir tráfico a la tienda propia y captar los "
     "pedidos de promoción universitaria. Sustenta OE-1.\n"
     "F5+O1  Ofrecer compra unitaria en línea, imposible de igualar por los proveedores que exigen mínimos."),
    ("Estrategias DO (adaptativas)",
     "D1+O1  Construir el canal de venta digital propio: es el núcleo del proyecto. Sustenta OE-1.\n"
     "D2+O5  Digitalizar el inventario por talla y color para poder prometer entrega en 72 horas con stock "
     "real. Sustenta OE-3.\n"
     "D3+O4  Automatizar la cotización del estampado con reglas configurables. Sustenta OE-2."),
    ("Estrategias FA (defensivas)",
     "F1+A1  Competir con los marketplaces por diferenciación (producto único) y no por logística.\n"
     "F2+A4  Al controlar el taller, absorber mejor el alza de insumos ajustando los costos por técnica "
     "desde el panel, sin reprogramar el sistema.\n"
     "F4+A3  Usar los reportes de estacionalidad (OE-4) para planificar campañas en los meses valle."),
    ("Estrategias DA (de supervivencia)",
     "D4+A3  Implantar el tablero de indicadores para dejar de decidir a ciegas frente a la estacionalidad. "
     "Sustenta OE-4.\n"
     "D5+A1  Adoptar tecnologías de licencia libre (Java, Tomcat, PostgreSQL, React) y despliegue en "
     "contenedores para contener el costo de la plataforma.\n"
     "D1+A5  Registrar los diseños de los clientes en la propia plataforma en lugar de en chats dispersos."),
]

# -------------------------------------------------------------- objetivos
OBJETIVO_GENERAL = (
    "Diseñar e implementar una plataforma web de comercio electrónico para Coral Shop S.A.C. que permita al "
    "cliente comprar y personalizar prendas juveniles en línea, y a la empresa gestionar de forma integrada su "
    "catálogo, su inventario por talla y color, y el ciclo completo del pedido, sustituyendo la operación actual "
    "basada en redes sociales y hojas de cálculo."
)

OBJETIVOS_ESPECIFICOS = [
    ("OE-1",
     "Implementar una tienda virtual publica que exponga el catálogo con stock real y permita completar la "
     "compra sin intervención manual del vendedor.",
     "Pedidos registrados por la web sobre el total de pedidos",
     "80 % al tercer mes",
     "M01, M02, M04, M05, M06, M07, M10"),
    ("OE-2",
     "Construir un personalizador de estampado que calcule el recargo automáticamente y genere una vista previa "
     "antes de la compra.",
     "Tiempo medio entre la solicitud y la cotización del estampado",
     "De 6 horas a menos de 1 minuto",
     "M03, M13, M15"),
    ("OE-3",
     "Digitalizar el inventario a nivel de variante (producto, talla y color) con trazabilidad de cada "
     "movimiento de stock.",
     "Pedidos cancelados por falta de stock",
     "Reducir de 12 % a menos de 2 %",
     "M02, M12, M14"),
    ("OE-4",
     "Proveer un tablero e informes que permitan a la gerencia decidir con datos sobre ventas, productos y "
     "estados de pedido.",
     "Indicadores disponibles en línea",
     "8 indicadores actualizados al día",
     "M11, M19"),
    ("OE-5",
     "Garantizar la seguridad de las cuentas y la trazabilidad de las operaciones administrativas.",
     "Operaciones administrativas registradas en bitácora",
     "100 %",
     "M16, M20"),
    ("OE-6",
     "Aplicar en la construcción del backend la arquitectura por capas y las tecnologías Java EE estudiadas en "
     "el curso, con pruebas automatizadas.",
     "Cobertura de pruebas de la capa de servicio",
     "Mínimo 70 %",
     "Transversal"),
]

# ----------------------------------------------------------------- actores
ACTORES = [
    ("Invitado", "Persona no autenticada.",
     "Explora el catálogo, ve el detalle, personaliza y arma un carrito de sesión. Para pagar debe registrarse."),
    ("Cliente", "Usuario registrado con rol CLIENTE.",
     "Todo lo del invitado, más checkout, favoritos, Mis diseños, historial, seguimiento y reseñas."),
    ("Vendedor", "Personal de tienda con rol VENDEDOR.",
     "Atiende la bandeja de pedidos, cambia estados, gestiona cupones y envíos, y consulta el inventario."),
    ("Diseñador", "Personal de taller con rol DISENADOR.",
     "Revisa el arte que sube el cliente, lo aprueba o lo rechaza con observaciones, y administra las "
     "opciones de estampado."),
    ("Administrador", "Rol ADMIN.",
     "Acceso total: catálogo, maestros, inventario, pedidos, usuarios, cupones, reportes y auditoría."),
    ("Sistema", "Procesos automáticos del backend.",
     "Genera SKU y códigos de pedido, emite notificaciones, libera reservas de stock vencidas y expira "
     "carritos de invitado."),
]

# --------------------------------------------------------------- modulos
MODULOS = [
    ("M01", "Catálogo y navegación", "Tienda pública",
     "Home, listado por categoría, búsqueda, filtros combinados, ordenamiento y paginación.", "RF-01 a RF-05"),
    ("M02", "Detalle de producto", "Tienda pública",
     "Ficha con galería, selección de talla y color, stock real de la variante y guía de tallas.", "RF-06 a RF-09"),
    ("M03", "Personalizador de estampado", "Tienda pública",
     "Zona, técnica y tamaño de estampado, carga de imagen o texto, vista previa y recargo automático.",
     "RF-10 a RF-14"),
    ("M04", "Carrito de compras", "Tienda pública",
     "Alta, edición y borrado de líneas, recálculo del total y fusión del carrito de invitado al iniciar sesión.",
     "RF-15 a RF-17"),
    ("M05", "Favoritos", "Tienda pública",
     "Lista de deseos por usuario.", "RF-18"),
    ("M06", "Checkout", "Compra",
     "Dirección de entrega, modalidad de envío, pago simulado y confirmación con código de pedido.",
     "RF-19 a RF-22"),
    ("M07", "Cupones de descuento", "Compra",
     "Validación de vigencia, monto mínimo y tope de canjes, y aplicación sobre el total.", "RF-23"),
    ("M08", "Seguimiento del pedido", "Compra",
     "Estado actual, historial de cambios y bandeja de notificaciones.", "RF-24, RF-25"),
    ("M09", "Reseñas y valoraciones", "Compra",
     "Calificación de 1 a 5 de compradores verificados, con moderación previa.", "RF-26, RF-27"),
    ("M10", "Cuenta de usuario", "Compra",
     "Registro, inicio de sesión, recuperación de contraseña, perfil, direcciones, historial y Mis diseños.",
     "RF-28 a RF-31"),
    ("M11", "Tablero de indicadores", "Backoffice",
     "Ventas del día y del mes, pedidos por estado, top de productos y alertas de stock crítico.", "RF-32"),
    ("M12", "Gestión de catálogo", "Backoffice",
     "CRUD de categorías jerárquicas, productos, imágenes y variantes con SKU.", "RF-33 a RF-35"),
    ("M13", "Maestros de estampado y prenda", "Backoffice",
     "CRUD de tallas, colores, técnicas, zonas y tamaños de estampado con sus costos.", "RF-36"),
    ("M14", "Control de inventario", "Backoffice",
     "Ajustes de stock con motivo, alertas de stock mínimo y consulta del kardex.", "RF-37 a RF-39"),
    ("M15", "Gestión de pedidos", "Backoffice",
     "Bandeja filtrable, cambio de estado según transiciones válidas y aprobación del arte.", "RF-40 a RF-42"),
    ("M16", "Usuarios y roles", "Gobierno",
     "CRUD de usuarios, asignación de rol y baja lógica.", "RF-43"),
    ("M17", "Administración de cupones", "Gobierno",
     "CRUD de campañas con vigencia, tipo de descuento y tope de canjes.", "RF-44"),
    ("M18", "Modalidades de envío", "Gobierno",
     "CRUD de métodos de entrega con costo, plazo y cobertura.", "RF-45"),
    ("M19", "Reportes", "Gobierno",
     "Ventas por periodo y categoría, top de productos, pedidos por estado y exportación a CSV.",
     "RF-46, RF-47"),
    ("M20", "Auditoría", "Gobierno",
     "Bitácora de acciones administrativas y consulta filtrada.", "RF-48, RF-49"),
]

# ------------------------------------------------ requerimientos funcionales
RF = [
    ("RF-01", "M01", "Listar los productos activos con imagen principal, nombre, precio desde y valoración promedio, paginados de 12 en 12.", "Alta", "Invitado / Cliente"),
    ("RF-02", "M01", "Filtrar el catálogo por categoría, talla, color, rango de precio y condición de personalizable, combinando varios filtros a la vez.", "Alta", "Invitado / Cliente"),
    ("RF-03", "M01", "Ordenar los resultados por relevancia, precio ascendente, precio descendente, novedad o mejor valorados.", "Media", "Invitado / Cliente"),
    ("RF-04", "M01", "Buscar por texto libre sobre el nombre y la descripción del producto, sin distinguir mayúsculas ni tildes.", "Alta", "Invitado / Cliente"),
    ("RF-05", "M01", "Navegar el árbol de categorías y subcategorías desde el menú principal.", "Media", "Invitado / Cliente"),
    ("RF-06", "M02", "Mostrar la ficha del producto con galería de imágenes, descripción, composición, cuidados y guía de tallas.", "Alta", "Invitado / Cliente"),
    ("RF-07", "M02", "Permitir seleccionar talla y color y resolver la variante correspondiente con su stock y su precio.", "Alta", "Invitado / Cliente"),
    ("RF-08", "M02", "Deshabilitar las combinaciones de talla y color sin stock e informar las unidades disponibles cuando queden menos de cinco.", "Alta", "Invitado / Cliente"),
    ("RF-09", "M02", "Sugerir hasta cuatro productos relacionados de la misma categoría.", "Baja", "Invitado / Cliente"),
    ("RF-10", "M03", "Permitir elegir zona de estampado, técnica y tamaño, mostrando el recargo de cada opción antes de confirmarla.", "Alta", "Invitado / Cliente"),
    ("RF-11", "M03", "Permitir subir una imagen PNG o JPG de hasta 5 MB, o escribir un texto eligiendo tipografía y color.", "Alta", "Invitado / Cliente"),
    ("RF-12", "M03", "Generar una vista previa que muestre el estampado sobre la prenda, la talla y el color seleccionados.", "Alta", "Invitado / Cliente"),
    ("RF-13", "M03", "Calcular el recargo en línea como costo base de la técnica por factor del tamaño más recargo de la zona, y congelarlo al agregar al carrito.", "Alta", "Sistema"),
    ("RF-14", "M03", "Guardar el diseño en Mis diseños para reutilizarlo en compras posteriores.", "Media", "Cliente"),
    ("RF-15", "M04", "Agregar al carrito una variante, con o sin personalización, indicando la cantidad.", "Alta", "Invitado / Cliente"),
    ("RF-16", "M04", "Modificar cantidades y eliminar líneas del carrito, recalculando subtotal, recargos y total.", "Alta", "Invitado / Cliente"),
    ("RF-17", "M04", "Conservar el carrito del invitado en la sesión HTTP y fusionarlo con el carrito del usuario al iniciar sesión.", "Alta", "Sistema"),
    ("RF-18", "M05", "Marcar y desmarcar productos como favoritos y consultar la lista de deseos.", "Media", "Cliente"),
    ("RF-19", "M06", "Seleccionar una dirección guardada o registrar una nueva durante el checkout.", "Alta", "Cliente"),
    ("RF-20", "M06", "Elegir la modalidad de entrega mostrando su costo y su plazo estimado.", "Alta", "Cliente"),
    ("RF-21", "M06", "Registrar el pago mediante la pasarela simulada y confirmar el pedido generando su código único.", "Alta", "Cliente"),
    ("RF-22", "M06", "Mostrar y notificar al cliente el resumen del pedido con su código de seguimiento.", "Alta", "Sistema"),
    ("RF-23", "M07", "Validar el cupón por vigencia, monto mínimo de compra y tope de canjes, y aplicar el descuento al total.", "Media", "Cliente"),
    ("RF-24", "M08", "Consultar el estado actual y el historial completo de cambios de un pedido.", "Alta", "Cliente"),
    ("RF-25", "M08", "Generar una notificación en la bandeja del cliente ante cada cambio de estado del pedido.", "Media", "Sistema"),
    ("RF-26", "M09", "Calificar de 1 a 5 y comentar un producto, solo si el cliente lo compró y el pedido fue entregado.", "Media", "Cliente"),
    ("RF-27", "M09", "Publicar la reseña únicamente después de la moderación del administrador.", "Media", "Administrador"),
    ("RF-28", "M10", "Registrar una cuenta con correo y contraseña, validando formato y unicidad del correo.", "Alta", "Invitado"),
    ("RF-29", "M10", "Iniciar y cerrar sesión, y recuperar la contraseña mediante un token de un solo uso con vencimiento.", "Alta", "Cliente"),
    ("RF-30", "M10", "Editar los datos del perfil y administrar la libreta de direcciones, marcando una como predeterminada.", "Media", "Cliente"),
    ("RF-31", "M10", "Consultar el historial de pedidos y los diseños guardados.", "Media", "Cliente"),
    ("RF-32", "M11", "Mostrar ventas del día y del mes, pedidos por estado, top de productos vendidos y variantes con stock crítico.", "Alta", "Administrador"),
    ("RF-33", "M12", "Crear, editar, activar y desactivar categorías, permitiendo subcategorías.", "Alta", "Administrador"),
    ("RF-34", "M12", "Crear, editar y dar de baja productos, con carga de varias imágenes y marcado de la principal.", "Alta", "Administrador"),
    ("RF-35", "M12", "Crear y editar variantes con SKU generado automáticamente, stock, stock mínimo y precio propio opcional.", "Alta", "Administrador"),
    ("RF-36", "M13", "Administrar tallas, colores, técnicas de estampado, zonas y tamaños con sus costos y factores.", "Alta", "Administrador / Diseñador"),
    ("RF-37", "M14", "Registrar ajustes de stock indicando tipo de movimiento y motivo, dejando constancia en el kardex.", "Alta", "Administrador"),
    ("RF-38", "M14", "Alertar en el tablero las variantes cuyo stock esté por debajo del stock mínimo.", "Media", "Sistema"),
    ("RF-39", "M14", "Consultar el kardex filtrado por variante, tipo de movimiento y rango de fechas.", "Media", "Administrador"),
    ("RF-40", "M15", "Listar y filtrar pedidos por estado, rango de fechas y cliente.", "Alta", "Vendedor / Administrador"),
    ("RF-41", "M15", "Cambiar el estado de un pedido respetando únicamente las transiciones válidas, registrando responsable y comentario.", "Alta", "Vendedor / Administrador"),
    ("RF-42", "M15", "Aprobar o rechazar el arte del estampado con observaciones, notificando al cliente.", "Alta", "Diseñador"),
    ("RF-43", "M16", "Crear, editar y dar de baja usuarios, y asignarles un rol.", "Alta", "Administrador"),
    ("RF-44", "M17", "Crear y editar cupones definiendo código, tipo y valor de descuento, vigencia, monto mínimo y tope de canjes.", "Media", "Administrador"),
    ("RF-45", "M18", "Administrar las modalidades de entrega con su costo, plazo y cobertura.", "Media", "Administrador"),
    ("RF-46", "M19", "Emitir el reporte de ventas por periodo y por categoría, exportable a CSV.", "Media", "Administrador"),
    ("RF-47", "M19", "Emitir el reporte de productos más vendidos y de pedidos agrupados por estado.", "Media", "Administrador"),
    ("RF-48", "M20", "Registrar en la bitácora toda alta, modificación, baja y acceso administrativo, con usuario, fecha e IP.", "Alta", "Sistema"),
    ("RF-49", "M20", "Consultar la bitácora filtrada por usuario, entidad afectada y rango de fechas.", "Baja", "Administrador"),
]

# -------------------------------------------- requerimientos no funcionales
RNF = [
    ("RNF-01", "Seguridad",
     "Las contraseñas se almacenan como hash BCrypt con factor de trabajo 12. Nunca se guarda ni se transmite la contraseña en claro."),
    ("RNF-02", "Seguridad",
     "El acceso a la API se autoriza con un JWT firmado (HS256) con vigencia de 2 horas, validado por un filtro antes de llegar al servlet."),
    ("RNF-03", "Seguridad",
     "Todo acceso a la base de datos usa PreparedStatement con parámetros; queda prohibido concatenar valores en la sentencia SQL."),
    ("RNF-04", "Seguridad",
     "Toda entrada se valida en el servidor aunque el formulario del cliente ya la haya validado, y toda salida se escapa para evitar XSS."),
    ("RNF-05", "Rendimiento",
     "El listado del catálogo responde en menos de 2 segundos con 1000 productos, apoyado en paginación e índices B-tree."),
    ("RNF-06", "Rendimiento",
     "La aplicación usa un pool de 10 a 20 conexiones (HikariCP); ninguna operación abre una conexión por consulta."),
    ("RNF-07", "Usabilidad",
     "La interfaz es responsiva desde 360 px de ancho, con enfoque mobile first, ya que el público objetivo compra desde el celular."),
    ("RNF-08", "Accesibilidad",
     "Contraste mínimo AA, textos alternativos en las imágenes y navegación completa por teclado."),
    ("RNF-09", "Mantenibilidad",
     "El código se organiza en paquetes por capa (web.controller, service, dao, model, útil); ninguna clase mezcla responsabilidades de dos capas."),
    ("RNF-10", "Mantenibilidad",
     "Los atributos de las clases del modelo son privados y se exponen mediante getters y setters."),
    ("RNF-11", "Integridad",
     "El registro de un pedido es transaccional: se confirman todas sus tablas o ninguna (commit / rollback)."),
    ("RNF-12", "Portabilidad",
     "La solución se levanta con un único docker compose up que arranca Tomcat y PostgreSQL con la misma configuración en cualquier máquina."),
    ("RNF-13", "Trazabilidad",
     "Toda operación administrativa y todo movimiento de stock quedan registrados con usuario, fecha y valor anterior."),
    ("RNF-14", "Cumplimiento",
     "El sitio debe publicar las políticas de cambio, devolución y tratamiento de datos personales, y habilita el Libro de Reclamaciones virtual."),
    ("RNF-15", "Calidad",
     "La capa de servicio se construye con TDD (ciclo rojo, verde, refactor) y alcanza al menos 70 % de cobertura con JUnit 5 y Mockito."),
]

# ------------------------------------------------------- reglas de negocio
REGLAS = [
    ("RN-01", "El stock pertenece a la variante, no al producto. Un polo negro talla M y uno negro talla L son existencias independientes."),
    ("RN-02", "No se puede confirmar un pedido si alguna línea supera el stock disponible de su variante. La verificación se hace dentro de la transacción, no antes."),
    ("RN-03", "El precio unitario y el recargo de personalización se copian a order_item al confirmar el pedido. Cambiar el catálogo después no altera pedidos ya emitidos."),
    ("RN-04", "Precio de una línea = (precio de la variante o precio base del producto) + recargo de estampado, multiplicado por la cantidad."),
    ("RN-05", "Recargo de estampado = costo base de la técnica x factor del tamaño + recargo de la zona. Si la prenda no es personalizable, el recargo es cero."),
    ("RN-06", "Un cupón solo aplica si está activo, dentro de vigencia, el subtotal alcanza el monto mínimo y no se agotó el tope de canjes."),
    ("RN-07", "El descuento nunca puede dejar el total por debajo de cero ni aplicarse sobre el costo de envío."),
    ("RN-08", "Las transiciones de estado válidas son PENDIENTE a PAGADO a EN_PRODUCCION a ENVIADO a ENTREGADO. Cancelar solo se admite antes de ENVIADO."),
    ("RN-09", "Cancelar un pedido libera el stock reservado y registra el movimiento de tipo LIBERACION en el kardex."),
    ("RN-10", "Un pedido con al menos una línea personalizada no pasa a EN_PRODUCCION hasta que el diseñador apruebe el arte."),
    ("RN-11", "Solo puede reseñar un producto quien lo compró en un pedido ENTREGADO, y una sola vez por línea de pedido."),
    ("RN-12", "El SKU se genera como PRODUCTO-TALLA-COLOR (por ejemplo POL-URB-M-NEG) y es único en todo el catálogo."),
    ("RN-13", "El código de pedido tiene el formato CS-AAAA-NNNNNN, correlativo por año, y es el único identificador visible al cliente."),
    ("RN-14", "El carrito de un invitado vive 7 días; al iniciar sesión sus líneas se fusionan con el carrito del usuario sumando cantidades de la misma variante y personalización."),
]

# ----------------------------------------------------- historias de usuario
HISTORIAS = [
    ("HU-01", "M03",
     "Como cliente joven quiero diseñar mi propio estampado sobre el polo y ver cómo queda antes de pagar, "
     "para tener la seguridad de que voy a recibir lo que imagino.",
     "Dado un producto marcado como personalizable, cuando elijo zona, técnica y tamaño y subo una imagen, "
     "entonces el sistema muestra la vista previa sobre la prenda y el recargo actualizado en menos de 3 segundos.\n"
     "Dado que subo un archivo mayor a 5 MB o de un formato distinto a PNG o JPG, entonces el sistema lo rechaza "
     "e indica el motivo sin perder el resto de mi configuración."),
    ("HU-02", "M02",
     "Como cliente quiero ver que tallas y colores están realmente disponibles, para no comprar algo que luego "
     "me cancelen.",
     "Dado un producto con variantes agotadas, cuando abro su ficha, entonces esas combinaciones aparecen "
     "deshabilitadas.\n"
     "Dado que una variante tiene menos de 5 unidades, entonces se muestra el aviso Quedan N unidades."),
    ("HU-03", "M04",
     "Como invitado quiero armar mi carrito sin crear una cuenta, para decidir sin fricción, y no perderlo "
     "cuando finalmente me registre.",
     "Dado que agrego productos sin sesión iniciada, cuando inicio sesión, entonces las líneas de mi carrito "
     "de invitado se suman a las de mi cuenta sin duplicarse.\n"
     "Dado un carrito de invitado sin actividad por 7 días, entonces el sistema lo marca como ABANDONADO."),
    ("HU-04", "M06",
     "Como cliente quiero completar la compra en pocos pasos y recibir un código de seguimiento, para saber "
     "que mi pedido está en marcha.",
     "Dado un carrito con al menos una línea, cuando confirmó dirección, envío y pago, entonces el sistema "
     "responde con el código CS-AAAA-NNNNNN y el pedido queda en estado PENDIENTE.\n"
     "Dado que una variante quedó sin stock mientras yo compraba, entonces el sistema no crea el pedido, "
     "informa qué talla falló y deja el carrito intacto."),
    ("HU-05", "M08",
     "Como cliente quiero enterarme de cada avance de mi pedido, para no tener que escribir por WhatsApp "
     "preguntando.",
     "Dado un cambio de estado de mi pedido, entonces aparece una notificación en mi bandeja con la fecha y "
     "el nuevo estado.\n"
     "Dado que consulto el pedido, entonces veo la línea de tiempo completa con quién y cuándo hizo cada cambio."),
    ("HU-06", "M14",
     "Como administrador quiero ajustar el stock indicando el motivo, para que el inventario del sistema "
     "coincida con el del almacén y quede explicado.",
     "Dado un ajuste de stock, entonces se registra en el kardex el stock anterior, el nuevo, el motivo y mi usuario.\n"
     "Dado un intento de dejar el stock en negativo, entonces el sistema lo rechaza."),
    ("HU-07", "M15",
     "Como diseñador quiero revisar el arte que subió el cliente antes de estampar, para evitar mermas por "
     "archivos de mala calidad.",
     "Dado un pedido con líneas personalizadas en estado PAGADO, cuando apruebo el arte, entonces el pedido "
     "puede pasar a EN_PRODUCCION.\n"
     "Dado que rechazo el arte con una observación, entonces el cliente recibe la notificación con el motivo y "
     "el pedido no avanza."),
    ("HU-08", "M11",
     "Como gerente quiero ver en una sola pantalla como va la venta y que me falta reponer, para decidir sin "
     "pedir reportes a nadie.",
     "Dado que ingreso al tablero, entonces veo ventas del día y del mes, pedidos por estado, los cinco "
     "productos más vendidos y las variantes bajo el stock mínimo.\n"
     "Dado un pedido nuevo, entonces los indicadores lo reflejan en la siguiente carga."),
    ("HU-09", "M09",
     "Como cliente quiero leer opiniones de gente que si compró el producto, para confiar en la talla y en la "
     "calidad del estampado.",
     "Dado un producto con reseñas aprobadas, entonces se muestran con su calificación y el promedio.\n"
     "Dado que intento reseñar un producto que no compré, entonces el sistema me lo impide."),
    ("HU-10", "M16",
     "Como administrador quiero que cada persona vea solo lo que le corresponde, para proteger la información "
     "del negocio.",
     "Dado un usuario con rol VENDEDOR, cuando intenta abrir la gestión de usuarios, entonces el sistema "
     "responde 403 y no muestra la opción en el menú.\n"
     "Dado cualquier acceso administrativo, entonces queda registrado en la bitácora."),
]

# ------------------------------------------------------------- tecnologias
TECNOLOGIAS = [
    ("Capa de presentación", "React 19 + Vite + Tailwind CSS + React Router",
     "El equipo ya cuenta con el proyecto coral_shop desarrollado en React. Una SPA evita recargar la página "
     "completa en cada filtro del catálogo y permite construir el personalizador de estampado con una "
     "interacción fluida.",
     "Decisión del equipo, complementaria al backend del curso."),
    ("Lenguaje del servidor", "Java 17 (LTS)",
     "Versión con soporte extendido que ejecuta sobre la JVM. La sesión 1 del curso describe la plataforma Java "
     "y la relación entre Java SE, el JRE y la JVM; Java 17 es la base sobre la que corre todo lo demás.",
     "S01 - Arquitectura Java"),
    ("Componentes web", "Jakarta Servlet API 6 (Servlets y Filtros)",
     "La sesión 1 concluye que el Servlet cumple el rol de CONTROLADOR dentro del patrón MVC. Se usa esa misma "
     "idea: el servlet recibe la petición, delega en el servicio y devuelve la respuesta.",
     "S01 - Arquitectura Java / Clase 4 - MVC"),
    ("Vista", "React en el navegador (el servlet responde JSON)",
     "En clase la Vista se resuelve con JSP. Como el cliente es una SPA, la Vista se externaliza al navegador y "
     "el servlet responde JSON en lugar de hacer forward a un JSP. Los roles de Modelo y Controlador se "
     "mantienen intactos.",
     "S01 y Clase 4 (adaptación justificada)"),
    ("Modelo", "JavaBeans y DTO",
     "La sesión 1 define el JavaBean como la clase que representa la estructura de una tabla, es decir la capa "
     "MODELO. El proyecto usa un JavaBean por tabla y DTO específicos para las respuestas de la API.",
     "S01 - Arquitectura Java"),
    ("Contenedor web", "Apache Tomcat 10.1",
     "La sesión 3 distingue Web Server, Web Container y Application Server: el contenedor web es el responsable "
     "de implementar la API de Servlets y gestionar su ciclo de vida. Tomcat basta porque el proyecto no "
     "necesita EJB ni JMS.",
     "S03 - JSP y JDBC / S02 - Tecnología Web"),
    ("Acceso a datos", "JDBC (java.sql y javax.sql)",
     "La sesión 3 desarrolla Connection, Statement, PreparedStatement y ResultSet como la vía estándar de "
     "acceso a bases de datos relacionales desde Java. Los DAO del proyecto se construyen exactamente sobre "
     "esas clases.",
     "S03 - JSP y JDBC"),
    ("Pool de conexiones", "HikariCP sobre javax.sql.DataSource",
     "La sesión 3 introduce DriverManager.getConnection(). Abrir una conexión por petición no escala, por lo "
     "que se usa la interfaz DataSource del paquete javax.sql, también parte de la API JDBC vista en clase.",
     "S03 - JSP y JDBC"),
    ("Manejo de sesión", "HttpSessión y JSESSIONID",
     "La clase 4 explica el sessión scope y como el servidor crea la sesión, envía la cookie JSESSIONID y la "
     "recupera en cada petición. Ese mecanismo sostiene el carrito del invitado.",
     "Clase 4 - Request, sessión y application"),
    ("Base de datos", "PostgreSQL 16",
     "Motor relacional de licencia libre con integridad referencial, restricciones CHECK y buen soporte de "
     "índices, necesario para un inventario por variante y para pedidos inmutables.",
     "S03 (JDBC es agnóstico del motor)"),
    ("Serialización", "Gson",
     "Convierte JavaBeans a JSON y viceversa dentro del servlet, que es lo que reemplaza al forward hacia el JSP.",
     "Complemento de la adaptación de la Vista"),
    ("Seguridad", "JWT (HS256) + BCrypt",
     "El JWT permite que la API sea sin estado para el cliente React; BCrypt protege las contraseñas. Ambos se "
     "aplican en un Filter, que es el punto de la API de Servlets pensado para responsabilidades transversales.",
     "Jakarta Servlet Filter (S01)"),
    ("Construcción", "Maven (empaquetado WAR)",
     "Gestiona dependencias y produce el WAR que se despliega en el contenedor web.",
     "S02 - Despliegue de aplicaciones web"),
    ("Despliegue", "Docker y Docker Compose",
     "La sesión 2 trata los contenedores como responsables de la configuración y el despliegue de aplicaciones "
     "web, y señala que reducen los conflictos entre desarrollo y operaciones. Se define un compose con los "
     "servicios tomcat y postgres.",
     "S02 - Tecnología Web: Web Container"),
    ("Pruebas", "JUnit 5, Mockito, Postman y Swagger",
     "Sostienen el ciclo TDD rojo-verde-refactor sobre la capa de servicio y permiten probar la API sin depender "
     "del frontend.",
     "Metodología adoptada por el equipo"),
    ("Control de versiones", "Git y GitHub",
     "Trabajo en paralelo de los cinco integrantes con ramas por funcionalidad.",
     "Práctica del curso"),
]

# ------------------------------------------------------------- API REST
ENDPOINTS = [
    ("POST", "/api/v1/auth/register", "Público", "Registra un cliente. Devuelve 201 o 409 si el correo ya existe.", "AuthServlet"),
    ("POST", "/api/v1/auth/login", "Público", "Valida credenciales y devuelve el JWT y el rol.", "AuthServlet"),
    ("GET", "/api/v1/products", "Público", "Lista paginada con filtros q, categoría, talla, color, precio y orden.", "ProductServlet"),
    ("GET", "/api/v1/products/{slug}", "Público", "Ficha del producto con imágenes, variantes y reseñas aprobadas.", "ProductServlet"),
    ("GET", "/api/v1/categories", "Público", "Árbol de categorías activas.", "CategoryServlet"),
    ("GET", "/api/v1/print-options", "Público", "Técnicas, zonas y tamaños de estampado vigentes con sus costos.", "CustomizationServlet"),
    ("POST", "/api/v1/customizations/preview", "Público", "Sube el arte, genera el mockup y devuelve el recargo calculado.", "CustomizationServlet"),
    ("GET", "/api/v1/cart", "Sesión o JWT", "Devuelve el carrito del usuario o el de la sesión del invitado.", "CartServlet"),
    ("POST", "/api/v1/cart/items", "Sesión o JWT", "Agrega una línea. 409 si no hay stock.", "CartServlet"),
    ("PUT", "/api/v1/cart/items/{id}", "Sesión o JWT", "Cambia la cantidad de una línea.", "CartServlet"),
    ("DELETE", "/api/v1/cart/items/{id}", "Sesión o JWT", "Elimina una línea del carrito.", "CartServlet"),
    ("POST", "/api/v1/coupons/validate", "CLIENTE", "Valida un cupón contra el subtotal actual.", "CouponServlet"),
    ("POST", "/api/v1/orders", "CLIENTE", "Crea el pedido de forma transaccional. 201 o 409 por stock.", "OrderServlet"),
    ("GET", "/api/v1/orders", "CLIENTE", "Historial de pedidos del usuario autenticado.", "OrderServlet"),
    ("GET", "/api/v1/orders/{code}", "CLIENTE", "Detalle y línea de tiempo de un pedido.", "OrderServlet"),
    ("POST", "/api/v1/reviews", "CLIENTE", "Registra una reseña de comprador verificado.", "ReviewServlet"),
    ("GET", "/api/v1/admin/dashboard", "ADMIN", "Indicadores del tablero.", "AdminReportServlet"),
    ("POST", "/api/v1/admin/products", "ADMIN", "Alta de producto.", "AdminProductServlet"),
    ("POST", "/api/v1/admin/variants", "ADMIN", "Alta de variante con SKU generado.", "AdminVariantServlet"),
    ("POST", "/api/v1/admin/inventory/adjust", "ADMIN", "Ajuste de stock con motivo; escribe en el kardex.", "InventoryServlet"),
    ("PATCH", "/api/v1/admin/orders/{id}/status", "VENDEDOR / ADMIN", "Cambia el estado validando la transición.", "AdminOrderServlet"),
    ("PATCH", "/api/v1/admin/customizations/{id}/approval", "DISENADOR", "Aprueba o rechaza el arte del cliente.", "AdminOrderServlet"),
    ("GET", "/api/v1/admin/reports/sales", "ADMIN", "Reporte de ventas por periodo, exportable a CSV.", "AdminReportServlet"),
    ("GET", "/api/v1/admin/audit", "ADMIN", "Consulta paginada de la bitácora.", "AuditServlet"),
]

# ------------------------------------------------------ estructura y clases
ARBOL_PAQUETES = """coral_shop_backend/
|-- pom.xml                          Dependencias y empaquetado WAR (Maven)
|-- Dockerfile                       Imagen de la aplicación sobre tomcat:10.1-jdk17
|-- docker-compose.yml               Servicios tomcat y postgres
|-- sql/
|   |-- schema.sql                   Creación de las 28 tablas, claves e índices
|   |-- seed.sql                     Datos simulados para la demostración
`-- src/
    |-- main/
    |   |-- java/pe/edu/utp/coralshop/
    |   |   |-- config/              DataSourceProvider, AppConfig, JwtProperties
    |   |   |-- web/
    |   |   |   |-- controller/      Servlets: un servlet por recurso de la API
    |   |   |   |-- filter/          CorsFilter, JwtAuthenticationFilter, RoleAuthorizationFilter
    |   |   |   `-- listener/        AppContextListener (arranque y cierre del pool)
    |   |   |-- service/             Reglas de negocio y control de la transacción
    |   |   |   `-- impl/            Implementaciones de cada interfaz de servicio
    |   |   |-- dao/                 Interfaces DAO
    |   |   |   `-- jdbc/            Implementaciones con PreparedStatement y ResultSet
    |   |   |-- model/               JavaBeans: una clase por tabla
    |   |   |   |-- dto/             Objetos de entrada y salida de la API
    |   |   |   `-- enums/           OrderStatus, MovementType, DiscountType, ApprovalStatus
    |   |   |-- exception/           Excepciones de negocio propias
    |   |   `-- útil/                JsonUtil, PasswordUtil, JwtUtil, SkuGenerator, Validator
    |   `-- webapp/WEB-INF/web.xml   Registro de filtros y parámetros de contexto
    `-- test/java/pe/edu/utp/coralshop/
        |-- service/                 Pruebas unitarias con JUnit 5 y Mockito
        `-- dao/                     Pruebas de integración sobre una base de pruebas"""

CLASES = [
    ("model", "Role, AppUser, Address, Category, Product, ProductImage, Size, Color, ProductVariant, "
     "InventoryMovement, PrintTechnique, PrintZone, PrintSize, Design, Customization, Cart, CartItem, "
     "WishlistItem, Coupon, ShippingMethod, Order, OrderItem, OrderStatusHistory, Payment, Review, "
     "Notification, AuditLog, PasswordResetToken",
     "Un JavaBean por tabla: atributos privados, constructor vacío, getters y setters. Sin lógica de negocio."),
    ("model.dto", "LoginRequest, AuthResponse, ProductCardDto, ProductDetailDto, VariantDto, "
     "CustomizationRequest, CustomizationPriceDto, CartDto, CartItemDto, CheckoutRequest, OrderDto, "
     "OrderTimelineDto, DashboardDto, PageDto<T>, ApiError",
     "Aislan la forma de la API de la forma de las tablas. Evitan exponer campos sensibles como password_hash."),
    ("model.enums", "OrderStatus, MovementType, DiscountType, ApprovalStatus, PaymentStatus, UserRole",
     "Valores cerrados del dominio. OrderStatus además declara sus transiciones válidas."),
    ("web.controller", "AuthServlet, ProductServlet, CategoryServlet, CustomizationServlet, CartServlet, "
     "CouponServlet, OrderServlet, ReviewServlet, WishlistServlet, AdminProductServlet, AdminVariantServlet, "
     "InventoryServlet, AdminOrderServlet, AdminUserServlet, AdminReportServlet, AuditServlet",
     "Extienden HttpServlet. Leen la petición, delegan en el servicio y escriben JSON. No contienen SQL ni "
     "reglas de negocio."),
    ("web.filter", "CorsFilter, EncodingFilter, JwtAuthenticationFilter, RoleAuthorizationFilter, "
     "RequestLoggingFilter",
     "Implementan jakarta.servlet.Filter. Resuelven en un solo punto lo transversal: codificación, CORS, "
     "autenticación, autorización por rol y registro de peticiones."),
    ("service", "AuthService, ProductService, CategoryService, InventoryService, CustomizationService, "
     "PricingService, CartService, CouponService, OrderService, ReviewService, ReportService, "
     "NotificationService, AuditService",
     "Contienen las reglas RN-01 a RN-14. OrderService es la única clase que abre y cierra la transacción "
     "del pedido."),
    ("dao / dao.jdbc", "UserDao, AddressDao, CategoryDao, ProductDao, ProductImageDao, VariantDao, "
     "SizeDao, ColorDao, InventoryDao, PrintOptionDao, DesignDao, CustomizationDao, CartDao, CouponDao, "
     "ShippingDao, OrderDao, OrderItemDao, PaymentDao, ReviewDao, NotificationDao, AuditDao",
     "Interfaz más implementación JDBC. Único lugar del sistema donde aparece SQL. Reciben la Connection "
     "cuando participan en una transacción."),
    ("útil", "JsonUtil, PasswordUtil, JwtUtil, SkuGenerator, OrderCodeGenerator, Validator, ImageStorage, "
     "MockupRenderer",
     "Utilidades sin estado. SkuGenerator y OrderCodeGenerator implementan las reglas RN-12 y RN-13."),
    ("exception", "StockInsuficienteException, TransicionInvalidaException, CuponInvalidoException, "
     "RecursoNoEncontradoException, CredencialesInvalidasException, AccesoDenegadoException",
     "Excepciones de negocio propias. Un manejador las traduce a códigos HTTP: 409, 404, 401 y 403."),
    ("config", "DataSourceProvider, AppContextListener, JwtProperties",
     "Crean el pool de conexiones al arrancar el contexto y lo cierran al detenerlo."),
]

ALGORITMOS = [
    ("Carrito en memoria de sesión", "HashMap<String, CartItem>",
     "La clave combina el identificador de la variante con el hash de la personalización. Agregar, buscar y "
     "eliminar una línea son O(1), frente a O(n) si se recorriera una lista.", "M04, RF-15 a RF-17"),
    ("Listados del catálogo", "ArrayList<ProductCardDto>",
     "Acceso por índice O(1) para paginar los resultados que devuelve el ResultSet.", "M01, RF-01"),
    ("Ordenamiento de resultados", "Comparator + Collections.sort (TimSort, O(n log n))",
     "Comparadores encadenados por precio, valoración y fecha para resolver los criterios de RF-03.", "M01, RF-03"),
    ("Filtrado combinado", "Stream API con predicados compuestos",
     "Los filtros que no conviene resolver en SQL se componen como Predicate y se aplican en una sola pasada.",
     "M01, RF-02"),
    ("Árbol de categorías", "Estructura de árbol n-ario recorrida en profundidad (recursión)",
     "category se autorreferencia con parent_id. El menú se arma con un recorrido DFS que respeta "
     "display_order.", "M01, RF-05"),
    ("Máquina de estados del pedido", "EnumMap<OrderStatus, EnumSet<OrderStatus>>",
     "Declara las transiciones permitidas y valida cada cambio en O(1), aplicando la regla RN-08.",
     "M15, RF-41"),
    ("Cola de producción de estampados", "Queue<OrderItem> (LinkedList, FIFO)",
     "Los pedidos aprobados se atienden en el orden en que se aprobaron, para que el taller no altere la "
     "prioridad.", "M15, RF-42"),
    ("Cálculo de precios", "BigDecimal con RoundingMode.HALF_UP",
     "Evita el error de redondeo de los tipos de punto flotante en importes de dinero. Implementa RN-04 y RN-05.",
     "M03, M06, RF-13"),
    ("Generación de SKU y de código de pedido", "Concatenación por patrón + secuencia de base de datos",
     "Implementa RN-12 y RN-13 garantizando unicidad con una restricción UNIQUE.", "M12, M06"),
    ("Resguardo de contraseñas", "BCrypt (hash adaptativo con sal, factor 12)",
     "Hash lento por diseño, resistente a ataques de fuerza bruta. Implementa RNF-01.", "M10, RF-28"),
    ("Búsqueda en base de datos", "Índices B-tree sobre sku, slug, email y order_code",
     "Convierten la búsqueda de O(n) a O(log n) sobre las columnas más consultadas.", "Transversal"),
    ("Reserva de stock", "SELECT ... FOR UPDATE dentro de la transacción",
     "Bloquea la fila de la variante para que dos compras simultáneas no vendan la misma última unidad. "
     "Implementa RN-02.", "M06, RF-21"),
    ("Recálculo del promedio de valoración", "Media incremental almacenada en product.avg_rating",
     "Evita recorrer todas las reseñas en cada listado del catálogo.", "M09, RF-26"),
]

# ------------------------------------------------------------- cronograma
CRONOGRAMA = [
    ("Sprint 0", "Semanas 9 y 10", "Diagnóstico y diseño",
     "Análisis del negocio, definición de funcionalidades, arquitectura y modelo de datos. Este informe.",
     "Completado"),
    ("Sprint 1", "Semanas 11 y 12", "Cimientos del backend",
     "Proyecto Maven, docker compose, schema.sql, pool de conexiones, JavaBeans y DAO base. Módulos M16 y M10 "
     "(usuarios, roles, autenticación JWT).", "Planificado"),
    ("Sprint 2", "Semanas 13 y 14", "Catálogo e inventario",
     "Módulos M01, M02, M12, M13 y M14. Conexión del frontend React con la API real.", "Planificado"),
    ("Sprint 3", "Semanas 15 y 16", "Personalización y compra",
     "Módulos M03, M04, M05, M06, M07 y M08. Transacción del pedido y máquina de estados.", "Planificado"),
    ("Sprint 4", "Semana 17", "Backoffice y cierre",
     "Módulos M09, M11, M15, M17, M18, M19 y M20. Datos simulados, pruebas de extremo a extremo y despliegue.",
     "Planificado"),
    ("Sprint 5", "Semana 18", "Exposición",
     "Ensayo de la demostración y reparto de la exposición entre los cinco integrantes.", "Planificado"),
]

GLOSARIO = [
    ("Contenedor web", "Componente del servidor que implementa la API de Servlets y gestiona su ciclo de vida. "
     "En este proyecto, Apache Tomcat."),
    ("DAO", "Data Access Object. Clase cuya única responsabilidad es leer y escribir en la base de datos."),
    ("DTF", "Direct to Film. Técnica de estampado digital que permite tiradas cortas a color sin pedido mínimo."),
    ("DTO", "Data Transfer Object. Objeto que transporta datos entre capas con la forma que necesita la API."),
    ("JavaBean", "Clase Java con atributos privados, constructor vacío y getters y setters, que representa la "
     "estructura de una tabla. Es la capa Modelo del patrón MVC."),
    ("JDBC", "Java Database Connectivity. API estándar de Java para ejecutar SQL sobre bases de datos "
     "relacionales (paquetes java.sql y javax.sql)."),
    ("JSESSIONID", "Cookie con la que el servidor identifica la sesión HTTP de un navegador."),
    ("JWT", "JSON Web Token. Credencial firmada que el cliente envía en cada petición para autenticarse sin "
     "que el servidor guarde estado."),
    ("Kardex", "Registro cronológico de todas las entradas, salidas y ajustes de existencias."),
    ("MVC", "Modelo, Vista y Controlador. Patrón que separa datos, presentación y coordinación."),
    ("Servlet", "Clase Java que atiende peticiones HTTP dentro de un contenedor web. Cumple el rol de "
     "Controlador."),
    ("SKU", "Stock Keeping Unit. Código único que identifica un artículo concreto del almacén."),
    ("SPA", "Single Page Application. Aplicación web que actualiza la vista sin recargar la página completa."),
    ("Variante", "Combinación concreta de producto, talla y color. Es la unidad que tiene stock y SKU."),
]

REFERENCIAS = [
    "Apache Software Foundation. (2024). Apache Tomcat 10.1 Documentation. https://tomcat.apache.org/tomcat-10.1-doc/",
    "Eclipse Foundation. (2024). Jakarta Servlet Specification 6.0. https://jakarta.ee/specifications/servlet/6.0/",
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
    "Oracle. (2024). Java Platform, Standard Edition 17 Documentation. https://docs.oracle.com/en/java/javase/17/",
    "Osterwalder, A. y Pigneur, Y. (2011). Generación de modelos de negocio. Deusto.",
    "PostgreSQL Global Development Group. (2024). PostgreSQL 16 Documentation. https://www.postgresql.org/docs/16/",
]
