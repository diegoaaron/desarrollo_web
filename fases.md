# Coral Shop — Plan de fases

Hoja de ruta del desarrollo desde octubre de 2026. **Este archivo es la guía de trabajo
del equipo**: cada tarea se marca `[x]` al terminarla y, si algo cambia, se actualiza
aquí primero.

- Origen: `clase_entregables/Analisis_Codigo_vs_Arquitectura_y_Negocio.md`.
- El informe del entregable 1 queda **solo como histórico**; no se toma en cuenta.
- Tecnología backend: **Spring Boot** (definitivo).

---

## Índice

1. [Objetivo del producto](#1-objetivo-del-producto)
2. [Decisiones tomadas](#2-decisiones-tomadas)
3. [Convenciones de trabajo](#3-convenciones-de-trabajo)
4. [Resumen de fases](#4-resumen-de-fases)
5. [Fase 0 — Ordenar la casa](#fase-0--ordenar-la-casa)
6. [Fase 1 — Modelo de datos del negocio](#fase-1--modelo-de-datos-del-negocio)
7. [Fase 2 — API del flujo de compra](#fase-2--api-del-flujo-de-compra)
8. [Fase 3 — Frontend del flujo de compra](#fase-3--frontend-del-flujo-de-compra)
9. [Fase 4 — Evento de dominio](#fase-4--evento-de-dominio)
10. [Fase 5 — Calidad, demo y documentación](#fase-5--calidad-demo-y-documentación)
11. [Fase 6 — Pasarela de pago real](#fase-6--pasarela-de-pago-real)
12. [Backlog (fuera del núcleo)](#backlog-fuera-del-núcleo)

---

## 1. Objetivo del producto

Tienda en línea de prendas y accesorios **personalizables**:

1. El cliente recorre la **lista de productos** (polos, poleras, gorras, tote bags).
2. Elige uno y lo **personaliza con estampado o bordado**: sube **su imagen**, escoge
   **zonas predefinidas según el tipo de producto** y ve una **vista previa**.
3. Compra **por unidad** o **por mayor** (paquetes de 3, 6, 12 o múltiplos de 12). Un
   paquete mantiene el mismo diseño, pero puede **repartirse entre tallas y colores**.
4. Sigue el flujo **carrito → checkout → pago → confirmación**.
5. Sigue su pedido **hasta la entrega**.

**Historia de referencia para la demo:** *un cliente personaliza 12 polos con su logo en el
pecho (4 S, 4 M, 4 L), paga y ve su pedido pasar de PAGADO a ENTREGADO.*

---

## 2. Decisiones tomadas

| # | Decisión | Estado |
|---|---|---|
| D1 | Backend en **Spring Boot 3.5 / Java 21**; se conserva el paquete `com.coralshop` | ✅ Definida |
| D2 | **Cantidad libre con escalas** (opción A, ver abajo) | ✅ Definida |
| D3 | Un paquete por mayor comparte **diseño, técnica y zonas** y se **reparte entre tallas y colores** | ✅ Definida |
| D4 | Técnicas: **ESTAMPADO** y **BORDADO** (el bordado tiene zonas y tamaños más limitados y mayor costo base) | ✅ Definida |
| D5 | Zonas predefinidas **por tipo de producto** (polo/polera: pecho izq., pecho centro, espalda, mangas; gorra: frente, lateral; tote: cara A, cara B) | ✅ Definida |
| D6 | Pago **simulado** en las fases 2 y 3; **pasarela real en la fase 6** | ✅ Definida |
| D7 | Imágenes del cliente: PNG/JPG de hasta 5 MB, guardadas en PostgreSQL (`bytea`), porque el disco de Railway es efímero | ✅ Definida |
| D8 | **Sin proveedores externos**: todos los productos base a personalizar se cargan y configuran desde el panel admin de Coral Shop. La integración con CJ Dropshipping que traía el backend se **eliminó** | ✅ Definida |
| D9 | Interfaz en **español**; moneda **S/ (PEN)**; direcciones con departamento, provincia y distrito | ✅ Definida |
| D10 | El servidor **siempre recalcula** precio y stock; nunca confía en importes enviados por el navegador | ✅ Definida |
| D11 | **Una sola cuenta para comprar y administrar.** Un administrador también es cliente (jerarquía `ROLE_ADMIN` ⊃ `ROLE_USER`). El login lleva a «Mi cuenta» por defecto; el botón **Admin** del header lleva al login y, tras autenticarse, al panel | ✅ Definida |
| D12 | **La cuenta se identifica por su correo.** El registro pide nombre, apellido, correo y contraseña (sin nombre de usuario). Migración `V4__user_names_replace_username.sql` | ✅ Definida |

### D2 — Regla de cantidad: opción A, cantidad libre con escalas

El cliente pide **cualquier cantidad ≥ 1** de un mismo diseño (sumando todas sus tallas y
colores) y se aplica el descuento de la **escala más alta alcanzada**:

| Cantidad total del diseño | Escala aplicada | Ejemplo |
|---|---|---|
| 1 – 2 | Unidad (sin descuento) | 2 polos → precio unitario |
| 3 – 5 | Paquete de 3 | 4 polos → precio de 3 |
| 6 – 11 | Paquete de 6 | 9 polos → precio de 6 |
| 12 o más | Paquete de 12 (docena) | 15 polos → precio de 12 |

Se descartaron la *unidad estricta* (solo 1 o paquetes exactos) y la *unidad = 1 o 2*:
bloqueaban cantidades que el cliente igual podía armar agregando unidades sueltas.

---

## 3. Convenciones de trabajo

**Arquitectura (la vista en clase)**

- Capas por funcionalidad: `com.coralshop.<modulo>.{controller, service, repository, dto, model}`.
- **Controller**: recibe HTTP, valida *formato* con DTO + `@Valid` → **400**. No toca la
  base de datos.
- **Service**: reglas de negocio y `@Transactional` → **422** si se viola una regla, **409**
  ante conflictos.
- **Repository**: único lugar con SQL (`JdbcTemplate` o JPA). Siempre parámetros `?`,
  nunca SQL concatenado.
- Cada capa conoce **solo a la de abajo**.
- Errores centralizados en un `@RestControllerAdvice` con respuesta JSON uniforme
  `{ "status", "message", "errors" }`.

**Base de datos**

- Todo cambio de esquema es una **migración Flyway nueva** (`V5__…`, `V6__…`); nunca se
  edita una migración ya aplicada.
- `snake_case`; dinero en `NUMERIC(12,2)`; fechas en `TIMESTAMPTZ`.

**Frontend**

- Un solo árbol desde `main.jsx`: `app/` (layout y router), `pages/` (pantallas),
  `features/<modulo>/{api, components, hooks, model}`, `shared/`.
- Textos en español; precios con `Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' })`.
- Las rutas mantienen la convención actual en inglés (`/products`, `/cart`, `/checkout`…).

**Git**

- Rama por fase o por tarea grande (`fase-1-modelo`, `fase-3-personalizador`…) e
  integración a `main` por *pull request*.
- Mensajes de commit en español y en infinitivo o tercera persona («Agrega…»,
  «Corrige…»).

---

## 4. Resumen de fases

| Fase | Objetivo | Depende de | Resultado visible |
|---|---|---|---|
| **0** | Ordenar la casa: limpieza, español, S/, capas en el backend | — | Código limpio, catálogo en capas |
| **1** | Modelo de datos del negocio (migración V5) | 0 | Tablas de personalización, mayoreo y pedidos |
| **2** | API del flujo de compra | 1 | Cotizar, subir diseño, crear pedido, pagar (simulado), admin de pedidos |
| **3** | Frontend del flujo de compra | 2 | Personalizador, carrito, checkout, confirmación, «Mis pedidos» |
| **4** | Evento de dominio `OrderStatusChanged` | 2 | Notificaciones al cliente y auditoría |
| **5** | Calidad, demo y documentación del entregable 2 | 3, 4 | Pruebas, datos demo, Postman, informe y PPT |
| **6** | Pasarela de pago real | 5 | Pago en *sandbox* con webhook |

Las fases 2 y 3 pueden avanzar en paralelo una vez acordados los contratos de la API
(sección «Contratos» de la fase 2).

---

## Fase 0 — Ordenar la casa

**Objetivo:** partir de una base limpia y coherente con la arquitectura en capas.

### 0.1 Frontend: limpieza

- [x] Borrar el código muerto (no alcanzable desde `main.jsx`):
  - `src/app.jsx`, `src/router/router.jsx`
  - `src/app/home/`, `src/app/login/`, `src/app/products/`
  - `src/common/` (completa), `src/components/` (completa), `src/pages/home.jsx`
  - `src/features/login/`, `src/features/cart/context/`,
    `src/features/cart/components/cartdropdown.jsx`
  - `src/features/products/component/`, `src/features/products/pages/`
  - `src/features/products/hooks/use-get-products.js`, `use-get-products-by-id.js` y
    `src/features/products/services/` (llaman a `fakestoreapi.com`)
- [x] Verificar que `npm run build` y `npm run lint` pasan tras la limpieza.

### 0.2 Frontend: idioma, moneda y errores

- [x] Traducir la interfaz al español (`index.html` con `lang="es"`).
- [x] Utilidad `formatPrice()` en `shared/` con S/; reemplazar todos los `$x.toFixed(2)`.
- [x] Categorías del header, del menú móvil y del home desde `GET /api/categories` (hoy
      están fijas en el código).
- [x] Conectar o retirar el buscador del header (hoy no hace nada).
- [x] Corregir: `categoryName.toLowerCase()` sin protección ante nulos
      (`products-page.jsx`); `useOrders.updateStatus` sin `try/catch`; error de
      `useUsers.updateRole` que reemplaza toda la página; imagen repetida de la tarjeta
      *Unisex*; formularios de contacto y suscripción sin manejador.

### 0.3 Frontend: carrito

- [x] Persistir el carrito en `localStorage` (con `try/catch`).
- [x] Quitar el tope `MAX_CART_ITEMS = 5`. La regla de cantidad real llega en la fase 3.
- [x] Quitar la barra fija de «envío gratis desde $50».

### 0.4 Backend: capas

- [x] Reorganizar paquetes: `auth`, `catalog`, `user`, cada uno con
      `controller / service / repository / dto`.
- [x] `CatalogController` → `CatalogService` → `ProductRepository` (`JdbcTemplate`).
- [x] `AdminProductController` → `ProductAdminService` (validaciones y `@Transactional`)
      → `ProductRepository`.
- [x] `AdminOverviewController` → `StatsService` → `StatsRepository`.
- [x] `GlobalExceptionHandler` (`@RestControllerAdvice`): 400 / 404 / 409 / 422 / 500
      con JSON uniforme.
- [x] Mensajes de error en español en todo el backend.
- [x] `SecurityConfig`: dejar solo las reglas de rutas que existen o existirán en la fase 2.
- [x] Eliminar la integración con CJ Dropshipping (D8): clases, pantalla de importación y
      migración `V3__remove_external_product_sources.sql`, que retira las columnas `cj_*`.

**Estado (2026-10-07):** completada en la rama `fase-0-orden`.

**Hecho cuando:** el frontend arranca sin archivos muertos y en español; ningún controller
usa `JdbcTemplate`; los endpoints actuales responden igual que antes.

---

## Fase 1 — Modelo de datos del negocio

**Objetivo:** que la base de datos soporte personalización, mayoreo, pedidos, pagos y
seguimiento. Se entrega como `backend/src/main/resources/db/migration/V5__negocio_personalizacion.sql`
(más `V6` para datos semilla si se separan). Ya existen la `V3` (retira las columnas de CJ)
y la `V4` (nombre y apellido en lugar de nombre de usuario).

> `orders` y `order_items` existen desde la V1, pero ningún flujo los usa todavía y
> están vacías; la V5 puede **recrearlas** con la estructura definitiva.

### 1.1 Catálogo

| Tabla / cambio | Campos principales | Notas |
|---|---|---|
| `product_types` | `id`, `code` UQ, `name`, `is_active` | Semilla: POLO, POLERA, GORRA, TOTE |
| `products` (alterar) | `+ product_type_id` FK, `+ is_customizable` | Los productos existentes se asignan a un tipo |

### 1.2 Personalización

| Tabla | Campos principales | Notas |
|---|---|---|
| `customization_techniques` | `id`, `code` UQ, `name`, `description`, `base_cost`, `is_active` | ESTAMPADO, BORDADO |
| `print_zones` | `id`, `code` UQ, `name` | PECHO_IZQ, PECHO_CENTRO, ESPALDA, MANGA_IZQ, MANGA_DER, GORRA_FRENTE, GORRA_LATERAL, TOTE_CARA_A, TOTE_CARA_B |
| `product_type_zones` | `id`, `product_type_id`, `zone_id`, `technique_id`, `max_width_cm`, `max_height_cm`, `surcharge`, `preview_x`, `preview_y`, `preview_w`, `preview_h` | UQ (`product_type_id`, `zone_id`, `technique_id`). Define **qué zona admite qué técnica** en cada tipo y su recargo. Las coordenadas `preview_*` (en % de la imagen) ubican el diseño en la vista previa |
| `design_uploads` | `id`, `user_id`, `original_filename`, `content_type`, `size_bytes`, `sha256`, `data` (`bytea`), `created_at` | CHECK de tipo (PNG/JPG) y tamaño (≤ 5 MB) |

### 1.3 Mayoreo

| Tabla | Campos principales | Notas |
|---|---|---|
| `quantity_tiers` | `id`, `min_quantity` UQ, `label`, `discount_percent` | Semilla tentativa: 1 → 0 %, 3 → 5 %, 6 → 10 %, 12 → 15 %. Se aplica la escala con mayor `min_quantity` ≤ cantidad (D2) |

### 1.4 Entrega, pedidos y pagos

| Tabla | Campos principales | Notas |
|---|---|---|
| `addresses` | `id`, `user_id`, `receiver_name`, `phone`, `department`, `province`, `district`, `street`, `reference`, `is_default` | Direcciones de Perú |
| `shipping_methods` | `id`, `code`, `name`, `cost`, `estimated_days`, `is_active` | Semilla: Lima Metropolitana, Provincias, Recojo en tienda |
| `orders` (recrear) | `id`, `order_code` UQ, `user_id`, `status`, `subtotal`, `discount_amount`, `shipping_cost`, `total_amount`, `shipping_method_id`, copia de la dirección (`receiver_name`, `phone`, `department`, `province`, `district`, `street`, `reference`), `customer_note`, `created_at`, `updated_at` | La dirección se **copia** al pedido para que no cambie si el cliente la edita |
| `order_lines` | `id`, `order_id`, `product_id`, `product_name`, `technique_id`, `design_upload_id`, `quantity_total`, `tier_min_quantity`, `unit_base_price`, `unit_customization_price`, `discount_percent`, `line_total` | **Una línea = un diseño** sobre un producto (D3) |
| `order_line_zones` | `order_line_id`, `zone_id`, `surcharge` | Zonas elegidas y su recargo congelado |
| `order_items` (recrear) | `id`, `order_line_id`, `variant_id`, `sku`, `size_name`, `color_name`, `quantity` | **Reparto** de la línea entre tallas y colores. CHECK: la suma de las cantidades = `quantity_total` (se valida en el Service) |
| `order_status_history` | `id`, `order_id`, `from_status`, `to_status`, `changed_by`, `comment`, `changed_at` | Trazabilidad para «Mis pedidos» |
| `payments` | `id`, `order_id`, `provider`, `provider_reference` UQ, `amount`, `currency`, `status`, `created_at`, `confirmed_at` | `provider` = SIMULADO en la fase 2; la pasarela real se agrega en la fase 6 sin cambiar la tabla |

### 1.5 Estados del pedido

```
PENDIENTE_PAGO ──pago aprobado──► PAGADO ──► EN_PRODUCCION ──► LISTO_PARA_ENVIO ──► ENVIADO ──► ENTREGADO
      │                              │
      └──────────► CANCELADO ◄───────┘   (cancelar repone el stock)
```

### 1.6 Tareas

- [ ] Escribir `V5__negocio_personalizacion.sql` con las tablas y restricciones anteriores.
- [ ] Semilla: tipos, técnicas, zonas, `product_type_zones` con recargos, escalas de
      mayoreo y métodos de envío.
- [ ] Asignar `product_type_id` a los productos existentes.
- [ ] Actualizar `scripts/esquema.py` para que refleje **el modelo real** (fuente de los
      diagramas ER del entregable 2).
- [ ] Diagrama ER actualizado (`python scripts/figuras.py`).

**Hecho cuando:** el backend arranca, Flyway aplica la V5 sin errores y JPA valida el
esquema (`ddl-auto=validate`).

---

## Fase 2 — API del flujo de compra

**Objetivo:** todas las reglas del negocio en el servidor, con pago simulado.

### 2.1 Reglas de negocio (Service)

**Precio unitario de una línea**

```
unit_customization_price = technique.base_cost + Σ surcharge(zonas elegidas)
unit_price               = product.base_price + unit_customization_price
line_total               = unit_price × quantity_total × (1 − discount_percent(escala))
```

**Regla de cantidad** (D2, opción A): `QuantityPolicy.validate(quantity_total)` exige
`quantity_total ≥ 1` (422 si no). `QuantityPolicy.tierFor(quantity_total)` devuelve la
escala con mayor `min_quantity` que no supere la cantidad.

**Creación del pedido** (`OrderService.create`, **una sola transacción**):

1. Validar que cada producto esté activo y sea personalizable, que cada zona admita la
   técnica para ese tipo de producto y que el diseño pertenezca al usuario.
2. Validar la regla de cantidad y que el reparto por tallas y colores sume `quantity_total`.
3. Recalcular todos los precios en el servidor (D10).
4. Descontar stock por variante con actualización condicional
   (`UPDATE product_variants SET stock = stock - ? WHERE id = ? AND stock >= ?`); si
   alguna no alcanza → 409 y *rollback*.
5. Crear el pedido en `PENDIENTE_PAGO`, sus líneas, zonas e ítems, y el primer registro
   del historial.

**Máquina de estados** (`OrderStatusPolicy`): solo se permiten las transiciones del
diagrama 1.5; cualquier otra → 422. `CANCELADO` repone el stock.

**Pago simulado** (`PaymentGateway` como **interfaz**; `SimulatedPaymentGateway` como
implementación): aprueba o rechaza según la tarjeta de prueba ingresada; si aprueba,
registra `payments` y pasa el pedido a `PAGADO`. La fase 6 agrega otra implementación de
la misma interfaz.

### 2.2 Contratos (endpoints)

| Método | Ruta | Rol | Descripción |
|---|---|---|---|
| GET | `/api/product-types` | público | Tipos de producto |
| GET | `/api/products?type=&category=&q=&page=` | público | Catálogo con filtros y paginación en el servidor |
| GET | `/api/products/{id}/customization-options` | público | Técnicas, zonas válidas por técnica (con recargo, medidas y coordenadas de vista previa) y escalas de mayoreo |
| POST | `/api/designs` (*multipart*) | cliente | Sube el diseño; valida tipo y peso → `{ id }` |
| GET | `/api/designs/{id}/image` | dueño o admin | Devuelve la imagen (vista previa, admin) |
| POST | `/api/quotes` | público | Cotiza líneas del carrito; devuelve precios recalculados y errores por línea |
| GET / POST / PUT / DELETE | `/api/addresses` | cliente | Direcciones del cliente autenticado |
| GET | `/api/shipping-methods` | público | Métodos de envío |
| POST | `/api/orders` | cliente | Crea el pedido (2.1) → `{ orderCode, total, status }` |
| POST | `/api/orders/{code}/payment` | cliente dueño | Pago simulado |
| GET | `/api/orders/me` | cliente | Historial del cliente |
| GET | `/api/orders/me/{code}` | cliente dueño | Detalle y línea de tiempo |
| GET | `/api/orders?status=&page=` | admin | Bandeja de pedidos (**ruta que el frontend ya llama**) |
| GET | `/api/orders/{id}` | admin | Detalle con diseños |
| PUT | `/api/orders/{id}/status` | admin | Cambio de estado con la máquina de estados (**ya llamada por el frontend**) |
| GET | `/api/users` | admin | Lista de usuarios (**ya llamada**) |
| PUT | `/api/users/{id}/role` | admin | Cambio de rol (**ya llamada**) |
| GET / POST / PUT / DELETE | `/api/categories[/{id}]` | admin para escritura | CRUD de categorías (**ya llamado**); no permite eliminar categorías en uso |
| PUT / PATCH | `/api/admin/products/{id}` | admin | Editar y activar/desactivar productos |

Cuerpo de ejemplo de `POST /api/orders`:

```json
{
  "lines": [{
    "productId": 12,
    "techniqueCode": "BORDADO",
    "zoneCodes": ["PECHO_IZQ"],
    "designId": 41,
    "items": [
      { "variantId": 101, "quantity": 4 },
      { "variantId": 102, "quantity": 4 },
      { "variantId": 103, "quantity": 4 }
    ]
  }],
  "addressId": 7,
  "shippingMethodCode": "LIMA",
  "customerNote": "Logo centrado"
}
```

### 2.3 Tareas

- [ ] Módulo `customization`: repositorios, `CustomizationService`, endpoint de opciones.
- [ ] Módulo `design`: subida *multipart* (`spring.servlet.multipart.max-file-size=5MB`),
      validación del tipo real del archivo (cabecera PNG/JPG, no solo la extensión), hash
      SHA-256.
- [ ] `PricingService` + `QuantityPolicy` + `POST /api/quotes`.
- [ ] Módulo `order`: `OrderService`, `OrderStatusPolicy`, repositorios, endpoints de
      cliente y de admin.
- [ ] Módulo `payment`: interfaz `PaymentGateway`, `SimulatedPaymentGateway`, endpoint de
      pago.
- [ ] Módulo `address` y métodos de envío.
- [ ] Completar `users` y `categories` (admin) y la edición de productos.
- [ ] Catálogo con filtros y paginación en el servidor.
- [ ] Actualizar `SecurityConfig` con las nuevas rutas y roles. Las rutas de cliente
      (`/api/orders/me/**`, `/api/addresses/**`, `/api/designs/**`) exigen `ROLE_USER`, que
      también cumple un admin (D11), y deben declararse **antes** que la regla de admin
      `/api/orders/**`.

**Hecho cuando:** con Postman se recorre *cotizar → subir diseño → crear pedido → pagar →
el admin avanza estados hasta ENTREGADO*, y cada regla rota responde 400, 409 o 422 con un
mensaje claro.

---

## Fase 3 — Frontend del flujo de compra

**Objetivo:** que el cliente recorra el flujo completo desde el navegador.

### 3.1 Pantallas y rutas

| Ruta | Pantalla | Contenido |
|---|---|---|
| `/products` | Catálogo | Filtro por tipo y categoría, búsqueda y paginación (servidor) |
| `/product/:id` | Ficha + **personalizador** | Pasos descritos en 3.2 |
| `/cart` | Carrito | Líneas personalizadas, precios cotizados por el servidor, errores por línea |
| `/checkout` | Checkout | Dirección (crear o elegir), método de envío, resumen y pago simulado |
| `/orders/:code/confirmation` | Confirmación | Código de pedido, resumen, siguiente paso |
| `/account/orders` | Mis pedidos | Lista con estado |
| `/account/orders/:code` | Detalle | Línea de tiempo de estados, diseño, reparto por tallas |
| `/admin/orders` | Bandeja (admin) | Filtro por estado, detalle, descarga del diseño, cambio de estado |

### 3.2 Personalizador (en la ficha del producto)

1. **Color** (de los colores con stock).
2. **Técnica**: estampado o bordado (solo las válidas para el tipo de producto).
3. **Zona(s)**: casillas con las zonas permitidas para esa técnica, con recargo visible.
4. **Subir imagen**: arrastrar o elegir archivo; validar tipo y tamaño en el navegador
   antes de enviarlo (el servidor vuelve a validar).
5. **Vista previa**: imagen del producto con el diseño superpuesto en cada zona, usando
   las coordenadas `preview_*` (CSS posicionado o `<canvas>`).
6. **Cantidad**: **tabla de reparto por tallas** (y colores) con el total a la vista y la
   escala alcanzada («Llevas 9 → precio de paquete de 6; agrega 3 más y obtienes precio
   de docena»). Botones rápidos para 1, 3, 6 y 12.
7. **Precio**: desglose (base + técnica + zonas − descuento) obtenido de `POST /api/quotes`.
8. **Agregar al carrito**.

### 3.3 Tareas

- [ ] `features/customization/`: hooks de opciones, subida de diseño, componente de vista
      previa, tabla de reparto por tallas.
- [ ] Carrito con líneas personalizadas, guardado en `localStorage` y cotizado al abrir
      `/cart` y `/checkout`.
- [ ] `features/checkout/`: direcciones, métodos de envío, creación del pedido y pago
      simulado.
- [ ] `features/orders/`: confirmación, «Mis pedidos», detalle con línea de tiempo.
- [ ] Admin: bandeja de pedidos conectada, detalle con descarga del diseño, cambio de
      estado solo a los estados permitidos.
- [ ] Guardas: checkout y cuenta exigen sesión; al iniciar sesión se vuelve al paso en que
      estaba el cliente.

**Hecho cuando:** la historia de referencia (§1) se completa en el navegador sin usar
Postman.

---

## Fase 4 — Evento de dominio

**Objetivo:** aplicar el cuarto estilo de arquitectura visto en clase con un caso real.

- [ ] Evento `OrderStatusChanged(eventId, orderId, fromStatus, toStatus, occurredAt)`,
      publicado por `OrderService` con `ApplicationEventPublisher`.
- [ ] Consumidor `NotificationListener` (`@TransactionalEventListener(phase = AFTER_COMMIT)`):
      registra una notificación para el cliente («Tu pedido CS-000123 pasó a EN_PRODUCCION»).
- [ ] Consumidor `AuditListener`: escribe en la tabla de auditoría.
- [ ] Nueva migración Flyway: tablas `notifications` y `audit_log`.
- [ ] Endpoints `GET /api/notifications/me` y `PUT /api/notifications/{id}/read`; campana
      de notificaciones en el header.
- [ ] Diagrama del flujo de eventos para el informe (publicador → bus → suscriptores).

**Hecho cuando:** al cambiar el estado desde el admin aparece la notificación al cliente,
y si la transacción falla no se publica ningún evento.

---

## Fase 5 — Calidad, demo y documentación

### 5.1 Pruebas

- [ ] JUnit: `PricingService`, `QuantityPolicy`, `OrderStatusPolicy` (lógica pura, TDD).
- [ ] Prueba de integración de `POST /api/orders`: stock insuficiente → 409 y *rollback*.
- [ ] Prueba de seguridad: un cliente no puede ver el pedido ni el diseño de otro.

### 5.2 Demo

- [ ] Datos de demostración (migración o script aparte): productos de los cuatro tipos con
      fotos, variantes y stock; clientes y pedidos en distintos estados. **Datos
      ficticios**.
- [ ] Colección Postman (o Swagger con `springdoc-openapi`) de toda la API.
- [ ] Verificar el despliegue: Vercel + Railway, con login, subida de diseño y pedido en
      producción.

### 5.3 Documentación del entregable 2

- [ ] Actualizar los generadores de `scripts/` con el contenido real: stack Spring Boot,
      capas, MVC, eventos, modelo de datos (desde `esquema.py`), funcionalidades, historias
      de usuario del personalizador y del mayoreo.
- [ ] Regenerar el informe y la PPT (`scripts/generar.ps1`).
- [ ] Capturas reales de las pantallas para el informe.
- [ ] Reparto de la exposición entre los cinco integrantes y ensayo con la demo.

---

## Fase 6 — Pasarela de pago real

**Objetivo:** reemplazar el pago simulado por un proveedor real en modo *sandbox*, sin
tocar la lógica de precios, stock ni pedidos.

- [ ] Elegir proveedor peruano con *sandbox*: **Mercado Pago** (Checkout Pro), **Culqi**
      o **Izipay**. Criterios: documentación, SDK Java, Yape y tarjetas, comisiones.
- [ ] Nueva implementación de `PaymentGateway` (p. ej. `MercadoPagoPaymentGateway`),
      elegida por configuración (`payment.provider=simulado|mercadopago`).
- [ ] El servidor crea la preferencia o intención de pago con el **importe del pedido
      calculado en el servidor**.
- [ ] Endpoint `POST /api/payments/webhook`: verificar la firma del proveedor, consultar el
      estado real del pago y solo entonces pasar el pedido a `PAGADO`.
- [ ] **Idempotencia**: `provider_reference` único; un webhook repetido no confirma dos
      veces ni descuenta stock dos veces.
- [ ] Expiración: los pedidos en `PENDIENTE_PAGO` por más de N minutos se cancelan y
      reponen stock (tarea programada con `@Scheduled`).
- [ ] Claves del proveedor solo en variables de entorno del servidor.
- [ ] Nunca almacenar datos de tarjeta en Coral Shop.

**Hecho cuando:** un pago en *sandbox* confirma el pedido mediante webhook, y repetir el
webhook no cambia nada.

---

## Backlog (fuera del núcleo)

Se retoman solo si el núcleo (fases 0 a 5) está terminado:

- Favoritos (la tabla `favorites` ya existe).
- Cupones de descuento.
- Reseñas de productos.
- Banners administrables (la tabla `banners` ya existe).
- Recuperación de contraseña por correo.
- Correo de confirmación de pedido (nuevo consumidor del evento de la fase 4).
