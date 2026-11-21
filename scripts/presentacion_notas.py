# -*- coding: utf-8 -*-
"""Notas del orador de la presentación final (presentacion.py).

Una entrada por lámina, en el mismo orden: (expositor, qué decir). Reparto de la exposición
(máx. 20 minutos, luego la demo en vivo y la ronda de preguntas):

    Diego Damián        láminas 1–7    diagnóstico del negocio            ~4 min
    Juan Franco Loayza  láminas 8–13   problemática, objetivos y solución ~5 min
    Apolo Villanueva    láminas 14–19  tecnologías y arquitectura         ~6 min
    Jian Pier Campos    láminas 20–26  datos, implementación, calidad,    ~5 min
                                       demo (con Diego al teclado) y cierre

Para cambiar el reparto se edita aquí y se vuelve a ejecutar presentacion.py."""

DIEGO = "Diego Damián"
JUAN = "Juan Franco Loayza"
APOLO = "Apolo Villanueva"
JIAN = "Jian Pier Campos"
TODOS = "Todo el grupo"

NOTAS = [
    # 1 · Portada
    (DIEGO, """
TIEMPO: 20 s.
QUÉ DECIR: Saludar y presentar al Grupo 1 y a cada integrante. El proyecto es Coral Shop: una tienda en línea de
ropa juvenil (polos, poleras, gorras y tote bags) donde el propio cliente personaliza el estampado o el bordado y
puede comprar por mayor.
IDEA CLAVE: todo lo que vamos a mostrar está implementado y lo vamos a ver funcionando en la demo.
"""),
    # 2 · Agenda
    (DIEGO, """
TIEMPO: 20 s.
QUÉ DECIR: Nombrar los bloques sin leer las descripciones: diagnóstico, problemática y objetivos, la solución,
la arquitectura, el modelo de datos, la implementación con sus pruebas, y al final la demo y las conclusiones.
Decir quién expone cada parte.
"""),
    # 3 · Empresa
    (DIEGO, """
TIEMPO: 40 s.
QUÉ DECIR: Coral Shop S.A.C. es una pequeña empresa de Lima (12 colaboradores, ~S/ 1.8 millones al año,
CIIU 4771). Su diferencial es el taller propio de estampado y bordado: el 45 % de las ventas ya es
personalizado. Misión y visión en una frase cada una.
EL PROBLEMA EN UNA LÍNEA: hoy todo se vende por Instagram y WhatsApp y el inventario está en hojas de cálculo.
PREGUNTA PROBABLE: «¿la empresa es real?» → Es un caso ficticio pero realista; los datos son simulados y
coherentes, como pide la consigna.
"""),
    # 4 · Canvas
    (DIEGO, """
TIEMPO: 40 s.
QUÉ DECIR: No leer los nueve bloques. Señalar tres: la PROPUESTA DE VALOR (diseñar y ver la prenda antes de
comprar, precio al instante, stock real, descuento por volumen), los CANALES (la tienda propia pasa a ser el
canal principal) y la RELACIÓN CON CLIENTES (historial y avisos automáticos).
CONEXIÓN: cada uno de esos bloques se convirtió en un módulo del sistema: personalizador, mayoreo, carrito,
checkout, «Mis pedidos» y campana.
"""),
    # 5 · PESTEL
    (DIEGO, """
TIEMPO: 40 s.
QUÉ DECIR: El PESTEL no es un ejercicio aparte: cada factor tiene su consecuencia en el sistema. Ejemplos:
económico → los costos de técnica y zona viven en la base, no en el código, porque el tipo de cambio sube los
insumos; social → personalizador y compra en grupo; legal (Ley 29733) → BCrypt, CSRF, diseños privados y nunca
guardar la tarjeta.
"""),
    # 6 · FODA
    (DIEGO, """
TIEMPO: 40 s.
QUÉ DECIR: Fortalezas: taller propio y comunidad de 24 mil seguidores. Debilidad principal: D1, no hay canal
digital propio. La lectura cruzada muestra que D1 condiciona a las demás: sin plataforma no se aprovecha la
comunidad, no se automatiza la cotización y no se mide nada. Por eso el proyecto ataca D1.
"""),
    # 7 · Ishikawa
    (DIEGO, """
TIEMPO: 40 s.
QUÉ DECIR: Efecto: Coral Shop pierde pedidos, stock y trazabilidad. Las espinas de tecnología, método y medición
concentran las causas que la empresa SÍ controla, y todas apuntan al mismo vacío: no hay un sistema.
TRANSICIÓN: «Juan Franco les cuenta cuánto le cuesta eso al negocio y qué nos propusimos».
"""),
    # 8 · Problemática
    (JUAN, """
TIEMPO: 45 s.
QUÉ DECIR: Leer solo la frase central con calma. Luego las cuatro cifras: 12 % de pedidos cancelados por
sobreventa de tallas, 6 horas para cotizar un estampado, 3 de cada 10 consultas que se enfrían y cero
indicadores. Son datos simulados pero coherentes con la operación.
"""),
    # 9 · Objetivos
    (JUAN, """
TIEMPO: 45 s.
QUÉ DECIR: El objetivo general y los seis específicos, cada uno con indicador y meta. Resaltar OE-2 (cotización
de 6 horas a menos de 1 minuto: hoy es instantánea), OE-3 (sobreventa de 12 % a menos de 2 %: el sistema la
impide) y OE-6 (aplicar la arquitectura del curso: 73 pruebas en verde).
"""),
    # 10 · Solución
    (JUAN, """
TIEMPO: 50 s.
QUÉ DECIR: Tres decisiones hacen distinta a la tienda: stock por variante, personalizador con zonas válidas
según la prenda, y mayoreo repartible entre tallas. Todo está implementado y corre en local.
ALCANCE: decir con naturalidad lo que queda como trabajo futuro (pasarela real, despliegue público, correo,
cupones). No son olvidos: son integraciones con terceros y ya dejamos el punto de conexión preparado.
"""),
    # 11 · Módulos
    (JUAN, """
TIEMPO: 40 s.
QUÉ DECIR: 12 módulos en cuatro dominios: tienda, compra, cliente y administración; 36 requerimientos
funcionales. Recorrer las columnas de izquierda a derecha como el camino del cliente: ve el catálogo,
personaliza, compra, sigue su pedido; y el administrador lo atiende.
"""),
    # 12 · Personalizador
    (JUAN, """
TIEMPO: 1 min.
QUÉ DECIR: Es el corazón del negocio. Contar la historia de referencia: el delegado de una promoción quiere 12
polos con el logo bordado en el pecho, 4 S, 4 M y 4 L. Hacer la cuenta en voz alta: 35 de la prenda + 15 del
bordado + 8 de la zona = 58 por polo; por 12 = 696; menos 15 % de docena = S/ 591.60.
IDEA CLAVE: aunque las tallas sean distintas, el diseño es el mismo y por eso alcanza la escala de docena. Y el
precio lo calcula el SERVIDOR: si alguien manipula el navegador, no cambia nada.
"""),
    # 13 · Casos de uso
    (JUAN, """
TIEMPO: 40 s.
QUÉ DECIR: Cuatro actores. El invitado navega y personaliza; para guardar el diseño y comprar inicia sesión y
vuelve al paso en que estaba. El cliente compra y sigue su pedido. El administrador también puede comprar (su
rol incluye al de cliente). El Sistema reacciona al evento de cambio de estado: audita y avisa.
TRANSICIÓN: «Apolo explica con qué y cómo lo construimos».
"""),
    # 14 · Tecnologías
    (APOLO, """
TIEMPO: 1 min.
QUÉ DECIR: Recorrer el stack a la izquierda. Luego lo importante, a la derecha: elegimos Spring Boot, pero NO
abandonamos lo de clase. Spring MVC entra por un Servlet, el DispatcherServlet, que hace de controlador; Tomcat
sigue siendo el contenedor web, solo que embebido; JdbcTemplate es JDBC con PreparedStatement; @Transactional
es el commit/rollback; la sesión es la misma cookie JSESSIONID; y React toma el lugar de la JSP.
PREGUNTA PROBABLE: «¿por qué no Servlets puros como en el primer informe?» → Para dedicar el tiempo a las reglas
del negocio y no a infraestructura; los conceptos son los mismos y se ven en el código.
"""),
    # 15 · Arquitectura
    (APOLO, """
TIEMPO: 1 min.
QUÉ DECIR: Arriba la vista (React en el navegador), al medio el servidor Spring Boot con su cadena de seguridad
y las tres capas, abajo PostgreSQL. A la derecha los aspectos transversales: seguridad, validación,
transacciones, trazabilidad, errores uniformes y ejecución local.
DETALLE: el navegador solo habla con un origen gracias al proxy de Vite, así la cookie y el CSRF funcionan sin
configurar CORS.
"""),
    # 16 · Cliente-servidor y MVC
    (APOLO, """
TIEMPO: 50 s.
QUÉ DECIR: Cliente-servidor: un solo servidor con los datos y las reglas, varios clientes (tienda, panel,
Swagger, Postman). MVC: modelo = records y servicios con reglas; vista = React; controlador = @RestController.
Ejemplo: al marcar «pecho izquierdo», React llama a POST /api/quotes, el controlador delega en PricingService y
React redibuja el precio.
"""),
    # 17 · Capas y flujo
    (APOLO, """
TIEMPO: 1 min.
QUÉ DECIR: Seguir la flecha: React envía POST /api/orders con la cookie y el token CSRF; Spring Security valida;
el controller revisa el formato; el service abre la transacción, recalcula precios y aplica la docena; el
repository descuenta el stock con un UPDATE condicional; se graba el pedido y se publica el evento.
IDEA CLAVE: cada capa responde con su propio código: 400 formato, 422 regla, 409 stock, 404 recurso ajeno. Si
una talla no alcanza, se deshace todo.
"""),
    # 18 · Estados
    (APOLO, """
TIEMPO: 40 s.
QUÉ DECIR: Seis estados en fila y CANCELADO solo desde los dos primeros, que repone el stock. PAGADO solo llega
con un pago aprobado. Está implementado con un EnumMap de transiciones: cualquier otro salto responde 422.
"""),
    # 19 · Eventos
    (APOLO, """
TIEMPO: 50 s.
QUÉ DECIR: Cuarto patrón de clase. Quien cambia el estado publica OrderStatusChanged y no sabe quién escucha.
AuditListener escribe la auditoría dentro de la misma transacción: si falla, no hay cambio sin rastro.
NotificationListener crea el aviso de la campana solo cuando el cambio ya se guardó.
POR QUÉ NO KAFKA: con un servidor y dos suscriptores, el bus de Spring da el mismo desacoplamiento sin
infraestructura extra.
TRANSICIÓN: «Jian Pier sigue con los datos y la implementación».
"""),
    # 20 · Datos
    (JIAN, """
TIEMPO: 50 s.
QUÉ DECIR: 27 tablas en cinco módulos, creadas por Flyway (V1 a V6) al arrancar. Cuatro decisiones: el stock
vive en la variante; las reglas del personalizador son datos (zona × técnica × recargo); una línea es un diseño
con su reparto por tallas; el pedido copia precios y dirección para no cambiar después.
DETALLE: la base protege sus reglas con CHECK e índices únicos, por ejemplo un solo pago aprobado por pedido.
"""),
    # 21 · Implementación
    (JIAN, """
TIEMPO: 50 s.
QUÉ DECIR: Paquetes por funcionalidad y dentro por capa: 17 paquetes, 131 clases, ningún controller con SQL.
A la derecha, los algoritmos que importan: EnumMap para estados, el UPDATE condicional contra la sobreventa,
SELECT FOR UPDATE contra el doble pago, Luhn para la tarjeta, bytes mágicos para saber si el archivo es de verdad
una imagen y SecureRandom para el código del pedido.
"""),
    # 22 · Pruebas
    (JIAN, """
TIEMPO: 45 s.
QUÉ DECIR: 73 pruebas automatizadas en verde. Unitarias de las reglas; de integración con Testcontainers, que
levanta un PostgreSQL real en Docker; y de seguridad: un cliente no puede ver el pedido ni el diseño de otro.
Además la colección Postman recorre toda la historia y la probamos completa en el navegador.
"""),
    # 23 · Demo
    (JIAN + " (Diego al teclado)", """
TIEMPO: 4–5 min (fuera de los 20 de exposición).
ANTES DE EXPONER: docker start coralshop-db; en IntelliJ «Backend (demo)» con DEMO_ADMIN_PASSWORD y «Frontend»;
abrir http://localhost:5173 con la sesión de Renzo (renzo.paredes@demo.coralshop.pe / Cliente2026) y otra
ventana privada con el admin. Tener el logo listo en el escritorio. Plan B: capturas del Anexo B.
GUION: seguir los 7 pasos de la lámina. En el paso 2 mostrar que con bordado la espalda no aparece. En el paso
4 usar primero 4000 0000 0000 0002 (rechazada) y luego 4111 1111 1111 1111. En el paso 5 avanzar a EN
PRODUCCIÓN y volver a la tienda para ver la campana.
"""),
    # 24 · Conclusiones
    (JIAN, """
TIEMPO: 50 s.
QUÉ DECIR: Seis conclusiones, una frase cada una, sin leer. Cerrar con: los cuatro patrones vistos en clase no
quedaron en el papel; se pueden comprobar en el código y lo acabamos de ver funcionando.
"""),
    # 25 · Trabajo futuro
    (JIAN, """
TIEMPO: 40 s.
QUÉ DECIR: Lo siguiente sería la pasarela real: es otra implementación de PaymentGateway, con webhook firmado
e idempotente. Luego expirar pedidos impagos, desplegar, enviar correo (un suscriptor más del evento) y el
backlog comercial.
"""),
    # 26 · Cierre
    (TODOS, """
TIEMPO: 10 s + preguntas.
QUÉ DECIR: Agradecer y abrir la ronda de preguntas. Cada uno responde las de su parte:
negocio → Diego; requerimientos y alcance → Juan Franco; arquitectura y tecnologías → Apolo; datos, código y
pruebas → Jian Pier.
"""),
]
