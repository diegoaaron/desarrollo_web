# -*- coding: utf-8 -*-
"""Notas del orador de la presentación del avance 2 (avance2_presentacion.py).

Una entrada por lámina, en el mismo orden: (expositor sugerido, qué decir). El reparto es una
propuesta de 3 o 4 láminas por integrante; se cambia aquí y se vuelve a generar la PPT."""

DIEGO = "Diego Damián"
JUAN = "Juan Franco Loayza"
APOLO = "Apolo Villanueva"
JIAN = "Jian Pier Campos"

NOTAS = [
    # 1 · Portada
    (DIEGO, """
QUÉ DECIR: Saludar y presentar al grupo (Grupo 1) y el proyecto: Coral Shop, una tienda virtual de ropa juvenil
(polos, poleras, gorras y tote bags) donde el propio cliente personaliza el estampado o el bordado.
Este avance muestra la ARQUITECTURA de la solución: cómo aplicamos los cuatro patrones vistos en clase
(capas, cliente-servidor, MVC y eventos) en el código real que ya funciona.
IDEA CLAVE: no es un diseño en papel; todo lo que vamos a mostrar ya está implementado hasta la fase 4.
"""),
    # 2 · Agenda
    (DIEGO, """
QUÉ DECIR: Recorrer rápido los seis bloques. Primero dónde estamos; luego los cuatro patrones, uno por uno,
cada uno explicado con una analogía de nuestro propio taller de estampado (no del restaurante de la clase);
al final la implementación, las pruebas y lo que falta.
TIP: no leer las tarjetas; decir solo el título de cada bloque y pasar. Esta lámina dura ~30 segundos.
"""),
    # 3 · Dónde estamos
    (DIEGO, """
QUÉ DECIR: El proyecto se organiza en 7 fases. Las fases 0 a 4 están TERMINADAS e integradas en GitHub:
0 ordenar el código, 1 modelo de datos, 2 API de compra, 3 frontend de compra y 4 eventos. La siguiente es la 5
(calidad y demo) y la 6 es la pasarela de pago real.
CIFRAS: 27 tablas en PostgreSQL, 15 módulos en el backend, 44 pruebas unitarias en verde y 64 controles del
recorrido de la API.
EL CASO QUE GUÍA TODO: 12 polos con el logo bordado en el pecho, 4 de talla S, 4 M y 4 L. El cliente compra y
paga, el administrador lo lleva hasta ENTREGADO y la campana le avisa cada cambio. Ese caso ya se probó entero en
el navegador. Lo vamos a usar como ejemplo en todas las láminas.
"""),
    # 4 · Patrones vistos en clase
    (DIEGO, """
QUÉ DECIR: Son los cuatro patrones que el profesor dibujó en la pizarra. No compiten entre sí: cada uno mira el
sistema desde un nivel distinto.
- Capas: cómo se ordena el servidor por dentro.
- Cliente-servidor: qué corre en el navegador y qué en el servidor.
- MVC: cómo se separa lo que el usuario ve de los datos y de quien coordina.
- Eventos: cómo el sistema reacciona cuando pasa algo importante (un pedido cambia de estado).
TRANSICIÓN: «Empezamos por capas, con un ejemplo de nuestro propio taller».
"""),
    # 5 · Capas: el taller
    (JUAN, """
QUÉ DECIR: En clase se usó el restaurante; nosotros usamos nuestro taller de estampado y bordado.
- El VENDEDOR atiende al cliente y revisa que el pedido esté completo (tallas, colores, diseño) → es el
  Controller (capa de presentación).
- El JEFE DE TALLER aplica las reglas: qué técnica acepta cada zona del polo, qué descuento por mayoreo toca,
  cuánto cuesta → es el Service (capa de negocio).
- El ALMACENERO saca y guarda los polos por talla y color → es el Repository (capa de datos).
- El ALMACÉN es PostgreSQL.
FRASE PARA RECORDAR: «el vendedor NO entra al almacén». En el código, ningún controller usa JdbcTemplate ni
escribe SQL; todo el SQL está en los @Repository. Si mañana cambiamos de base de datos, solo se tocan los
repositorios.
"""),
    # 6 · Capas: el pedido de 12 polos
    (JUAN, """
QUÉ DECIR: Mismo patrón, ahora con el pedido real (POST /api/orders). Seguir los números rojos del diagrama:
1. PRESENTACIÓN: CustomerOrderController y el DTO CreateOrderRequest validan el FORMATO con @Valid. Si falta un
   campo o la cantidad no es válida → error 400, sin tocar la base.
2. NEGOCIO: OrderService abre UNA transacción. Revisa que el pecho acepte bordado, que el logo sea del cliente,
   reconoce que 12 polos alcanzan la escala de docena (15 % de descuento) y recalcula los precios. Regla rota → 422.
3. DATOS: descuenta el stock talla por talla con «UPDATE … WHERE stock >= ?». Si no hay 4 polos talla M, se
   deshace todo (rollback) → 409.
4. Al confirmar, se publica el evento OrderStatusChanged (lo vemos en la lámina 10).
SI PREGUNTAN «¿por qué el precio lo calcula el servidor?»: porque el navegador se puede manipular.
"""),
    # 7 · Errores por capa
    (JUAN, """
QUÉ DECIR: Una ventaja de separar en capas es que cada error dice dónde falló:
- 400 (presentación): el formato está mal; por ejemplo, subir un archivo que no es imagen o de más de 5 MB.
- 404 (negocio): pides algo que no es tuyo, como el pedido o el aviso de otro cliente. No decimos «prohibido»
  para no revelar que existe.
- 409 (negocio/datos): conflicto con el stock: «Stock insuficiente… pediste 21».
- 422 (negocio): una regla del taller: «La zona ESPALDA no admite bordado» o saltar de PAGADO a ENTREGADO.
Todo pasa por un solo @RestControllerAdvice que responde siempre con la misma forma { status, message, errors },
y el frontend muestra ese mensaje junto al campo que falló. Los mensajes son reales, sacados de las pruebas.
"""),
    # 8 · Cliente-servidor
    (APOLO, """
QUÉ DECIR: ANALOGÍA: los pedidos llegan por varios canales, pero todos van a un único taller central que tiene
la lista de precios y el stock oficiales. Ningún canal fija sus propios precios.
En el software hay tres clientes (la tienda, el panel del administrador y Postman) y UN servidor Spring Boot,
que es el único que habla con PostgreSQL.
DETALLES A MENCIONAR:
- Se comunican por HTTP con JSON; la sesión viaja en la cookie JSESSIONID (lo visto en la clase de sesiones) y
  cada escritura lleva un token CSRF.
- La campana de avisos pregunta al servidor cada 30 segundos: en cliente-servidor siempre pregunta el cliente.
- En desarrollo Vite reenvía /api al backend; en producción lo hará Vercel con la variable BACKEND_URL.
"""),
    # 9 · MVC
    (APOLO, """
QUÉ DECIR: ANALOGÍA: el MODELO es la ficha técnica del pedido (tallas, técnica, zonas, precio y sus reglas); la
VISTA es la vista previa del polo con el logo que el cliente ve en pantalla; el CONTROLADOR es el asesor de
ventas, que recibe lo que el cliente elige, actualiza la ficha y le muestra el resultado.
RELACIÓN CON CLASE: JavaBeans → Modelo, Servlets → Controlador, JSP → Vista. La única adaptación es que la vista
ya no es una JSP: es React en el navegador, y el controlador responde JSON en vez de hacer forward.
EJEMPLO DEL DIAGRAMA: el cliente marca «pecho izquierdo» → React llama a POST /api/quotes → QuoteController
llama a PricingService → vuelve el precio → React redibuja el precio y la vista previa.
VENTAJA: la misma API sirve a la tienda, al panel y a las pruebas.
"""),
    # 10 · Eventos
    (APOLO, """
QUÉ DECIR: ANALOGÍA: cuando un pedido cambia de etapa, el jefe de taller toca una campana. Control interno lo
anota en la bitácora y atención al cliente avisa al comprador. El jefe no sabe quién escucha.
EN EL CÓDIGO (ya implementado en la fase 4):
- Tres servicios PUBLICAN el evento OrderStatusChanged: OrderService (pedido creado), PaymentService (pago
  aprobado) y OrderAdminService (el admin avanza o cancela).
- El BUS es el de Spring (ApplicationEventPublisher), sin Kafka ni RabbitMQ porque tenemos un solo servidor.
- Dos SUSCRIPTORES: AuditListener escribe en audit_log dentro de la misma transacción (si falla, el cambio se
  deshace: nunca hay cambio sin rastro); NotificationListener crea el aviso de la campana después de confirmar.
- Si mañana queremos enviar correos, se agrega un EmailListener sin tocar a los publicadores.
SI PREGUNTAN por duplicados: cada evento tiene un eventId único; repetirlo no duplica nada.
"""),
    # 11 · Síntesis
    (APOLO, """
QUÉ DECIR: Resumir cómo conviven los cuatro patrones en el mismo caso de los 12 polos:
- Cliente-servidor: la tienda le pide al servidor; reglas y datos protegidos en un solo lugar.
- MVC: React (vista) llama al controlador; la misma API sirve a todos.
- Capas: el pedido atraviesa presentación, negocio y datos; errores bien separados.
- Eventos: al cambiar de estado se audita y se avisa sin tocar el flujo de pedidos.
IDEA CLAVE: cada patrón responde a una pregunta distinta, por eso se usan los cuatro a la vez.
"""),
    # 12 · Implementación: paquetes
    (JIAN, """
QUÉ DECIR: A la izquierda, la estructura real del backend: un paquete por funcionalidad (pedidos, pagos,
notificaciones, auditoría…) y, dentro de cada uno, los paquetes por capa: controller, service, repository, dto y
model. Ningún paquete mezcla capas, que es lo que pide la rúbrica. Son 15 módulos y 127 clases, y las tablas se
crean con las migraciones Flyway V1 a V6.
A la derecha, lo que ya puede hacer cada usuario:
- Tienda: catálogo, personalizador con vista previa, carrito, checkout con pago simulado, «Mis pedidos» y campana.
- Panel: bandeja de pedidos con la máquina de estados y descarga del diseño, productos, categorías y usuarios.
- Seguridad: sesión, CSRF, roles y SQL siempre con parámetros (nunca concatenado).
"""),
    # 13 · Reglas y pruebas
    (JIAN, """
QUÉ DECIR: Izquierda, las reglas del negocio que ya se cumplen:
- El precio lo calcula el servidor: base + técnica + zonas, menos el descuento por mayoreo.
- Mayoreo: 1–2 sin descuento, 3–5 al 5 %, 6–11 al 10 %, 12 o más al 15 %.
- Cada tipo de producto define qué zona acepta qué técnica.
- No hay sobreventa: si dos clientes compran la última unidad, solo uno la consigue.
- PAGADO solo con un pago aprobado; cancelar devuelve el stock.
- Cada cambio de estado se audita y genera un aviso.
Derecha, cómo lo comprobamos: 44 pruebas unitarias en verde (incluida la del evento), 64 controles del recorrido
completo de la API contra PostgreSQL, y la historia de los 12 polos hecha de punta a punta en el navegador.
"""),
    # 14 · Próximos pasos
    (JIAN, """
QUÉ DECIR: Lo que falta para la entrega final (fases 5 y 6):
- Pruebas: una de integración del pedido (stock insuficiente → 409 y rollback) y una de seguridad (nadie ve el
  pedido ni el diseño de otro).
- Demo y despliegue: datos ficticios (no usamos datos personales reales), colección Postman, frontend en Vercel
  y backend publicado.
- Documentación: informe y PPT finales con capturas reales de las pantallas y el reparto de la exposición.
- Fase 6: pasarela de pago real en sandbox; como el pago ya está detrás de la interfaz PaymentGateway, solo se
  cambia la implementación.
"""),
    # 15 · Cierre
    (JIAN, """
QUÉ DECIR: Cerrar con las cuatro ideas:
1. Las capas se pueden comprobar en el código: el vendedor no entra al almacén.
2. El servidor es la única autoridad sobre precios y stock.
3. MVC se mantiene; la vista pasó de JSP a React.
4. Los eventos ya funcionan: cada cambio se audita y se avisa al cliente.
Agradecer y abrir la ronda de preguntas. Cada integrante responde las preguntas de las láminas que expuso.
"""),
]
