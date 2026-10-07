# -*- coding: utf-8 -*-
"""
Modelo de datos de Coral Shop.

Fuente de verdad única del esquema para los entregables: la usan el generador de
figuras (diagramas entidad-relación) y el generador del informe (diccionario de campos).

Refleja el esquema REAL que crean las migraciones Flyway del backend
(backend/src/main/resources/db/migration, V1 a V5). Si se agrega una migración que
cambia tablas o campos, se actualiza este archivo en el mismo commit.

Cada campo es una tupla: (nombre, tipo, llave, descripción)
  llave: 'PK' | 'FK -> tabla.campo' | 'PK, FK -> tabla.campo' (clave primaria compuesta)
         | 'UQ' | 'UQ*' (única compuesta) | ''
"""

MODULOS = {
    "seguridad": ("Seguridad y usuarios", "#6D2E46"),
    "catalogo": ("Catálogo e inventario", "#3C6E8F"),
    "personalizacion": ("Personalización y mayoreo", "#A26769"),
    "compra": ("Pedidos, envíos y pagos", "#4E7A5A"),
    "soporte": ("Contenido y fidelización", "#8A6D3B"),
}

ESTADOS_PEDIDO = ("PENDIENTE_PAGO, PAGADO, EN_PRODUCCION, LISTO_PARA_ENVIO, ENVIADO, "
                  "ENTREGADO o CANCELADO")

TABLAS = [
    # ------------------------------------------------------------------ seguridad
    dict(nombre="roles", modulo="seguridad",
         desc="Roles del sistema. ROLE_ADMIN incluye los permisos de ROLE_USER: un administrador "
              "también compra con la misma cuenta.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del rol."),
             ("name", "VARCHAR(30)", "UQ", "ROLE_ADMIN o ROLE_USER."),
         ]),
    dict(nombre="users", modulo="seguridad",
         desc="Cuentas de clientes y administradores. La cuenta se identifica por su correo.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del usuario."),
             ("role_id", "BIGINT", "FK -> roles.id", "Rol asignado."),
             ("first_name", "VARCHAR(80)", "", "Nombre."),
             ("last_name", "VARCHAR(80)", "", "Apellido."),
             ("email", "VARCHAR(255)", "UQ", "Correo; credencial de acceso (único sin distinguir mayúsculas)."),
             ("password_hash", "VARCHAR(255)", "", "Hash BCrypt de la contraseña. Nunca texto plano."),
             ("is_active", "BOOLEAN", "", "Baja lógica de la cuenta."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de registro."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha de la última modificación."),
         ],
         restricciones=["índice único sobre lower(email)", "first_name no vacío"]),
    dict(nombre="addresses", modulo="seguridad",
         desc="Libreta de direcciones del cliente, con la división política del Perú.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la dirección."),
             ("user_id", "BIGINT", "FK -> users.id", "Dueño de la dirección."),
             ("receiver_name", "VARCHAR(160)", "", "Persona que recibe el paquete."),
             ("phone", "VARCHAR(20)", "", "Teléfono de quien recibe."),
             ("department", "VARCHAR(60)", "", "Departamento."),
             ("province", "VARCHAR(60)", "", "Provincia."),
             ("district", "VARCHAR(60)", "", "Distrito."),
             ("street", "VARCHAR(200)", "", "Calle y número."),
             ("reference", "VARCHAR(200)", "", "Referencia para el repartidor (opcional)."),
             ("is_default", "BOOLEAN", "", "Dirección sugerida por defecto en el checkout."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de alta."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha de la última modificación."),
         ],
         restricciones=["una sola dirección por defecto por usuario (índice único parcial)",
                        "formato de teléfono", "ON DELETE CASCADE desde users"]),

    # ------------------------------------------------------------------- catalogo
    dict(nombre="categories", modulo="catalogo",
         desc="Árbol de categorías del catálogo. Se autorreferencia para permitir subcategorías.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la categoría."),
             ("parent_id", "BIGINT", "FK -> categories.id", "Categoría padre; NULL si es raíz."),
             ("name", "VARCHAR(120)", "", "Nombre visible."),
             ("description", "TEXT", "", "Texto descriptivo."),
             ("is_active", "BOOLEAN", "", "Permite ocultar la categoría sin borrarla."),
         ],
         restricciones=["nombre único entre hermanos", "parent_id distinto de id"]),
    dict(nombre="brands", modulo="catalogo",
         desc="Marcas de las prendas base.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la marca."),
             ("name", "VARCHAR(120)", "UQ", "Nombre (único sin distinguir mayúsculas)."),
             ("description", "TEXT", "", "Descripción."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
         ]),
    dict(nombre="product_types", modulo="catalogo",
         desc="Tipo de prenda. Determina qué zonas y técnicas de personalización admite el producto.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del tipo."),
             ("code", "VARCHAR(30)", "UQ", "POLO, POLERA, GORRA o TOTE."),
             ("name", "VARCHAR(80)", "", "Nombre visible."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
         ]),
    dict(nombre="products", modulo="catalogo",
         desc="Modelo base de una prenda. No tiene stock: el stock vive en sus variantes.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del producto."),
             ("category_id", "BIGINT", "FK -> categories.id", "Categoría a la que pertenece."),
             ("brand_id", "BIGINT", "FK -> brands.id", "Marca (opcional)."),
             ("product_type_id", "BIGINT", "FK -> product_types.id", "Tipo de prenda."),
             ("name", "VARCHAR(180)", "", "Nombre comercial."),
             ("description", "TEXT", "", "Descripción, composición y cuidados."),
             ("base_price", "NUMERIC(12,2)", "", "Precio de la prenda sin personalizar."),
             ("is_customizable", "BOOLEAN", "", "Habilita el personalizador."),
             ("is_active", "BOOLEAN", "", "Baja lógica del producto."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de alta."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha de la última modificación."),
         ],
         restricciones=["base_price >= 0", "si is_customizable, product_type_id es obligatorio"]),
    dict(nombre="product_images", modulo="catalogo",
         desc="Galería de imágenes de un producto.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la imagen."),
             ("product_id", "BIGINT", "FK -> products.id", "Producto al que pertenece."),
             ("image_url", "TEXT", "", "URL de la imagen."),
             ("alt_text", "VARCHAR(255)", "", "Texto alternativo (accesibilidad)."),
             ("sort_order", "INTEGER", "", "Orden dentro de la galería."),
             ("is_primary", "BOOLEAN", "", "Imagen que se muestra en el listado."),
         ],
         restricciones=["una sola imagen principal por producto (índice único parcial)"]),
    dict(nombre="sizes", modulo="catalogo",
         desc="Catálogo maestro de tallas.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la talla."),
             ("name", "VARCHAR(30)", "UQ", "Única, XS, S, M, L, XL, XXL."),
             ("sort_order", "INTEGER", "", "Orden natural de la talla."),
         ]),
    dict(nombre="colors", modulo="catalogo",
         desc="Catálogo maestro de colores de prenda.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del color."),
             ("name", "VARCHAR(60)", "UQ", "Nombre del color."),
             ("hex_code", "CHAR(7)", "", "Código hexadecimal (#RRGGBB)."),
         ]),
    dict(nombre="product_variants", modulo="catalogo",
         desc="Combinación concreta de producto, talla y color. Es la unidad que se vende y se almacena.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la variante."),
             ("product_id", "BIGINT", "FK -> products.id", "Producto base."),
             ("size_id", "BIGINT", "FK -> sizes.id", "Talla."),
             ("color_id", "BIGINT", "FK -> colors.id", "Color."),
             ("sku", "VARCHAR(80)", "UQ", "Código único de inventario."),
             ("stock", "INTEGER", "", "Unidades disponibles."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de alta."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha de la última modificación."),
         ],
         restricciones=["UNIQUE (product_id, size_id, color_id)", "stock >= 0"]),

    # ------------------------------------------------------------ personalizacion
    dict(nombre="customization_techniques", modulo="personalizacion",
         desc="Técnicas de personalización con su costo base por unidad.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la técnica."),
             ("code", "VARCHAR(30)", "UQ", "ESTAMPADO o BORDADO."),
             ("name", "VARCHAR(80)", "", "Nombre visible."),
             ("description", "TEXT", "", "Descripción para el cliente."),
             ("base_cost", "NUMERIC(12,2)", "", "Costo fijo por unidad personalizada."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
         ]),
    dict(nombre="print_zones", modulo="personalizacion",
         desc="Zonas donde puede ir un diseño (pecho, espalda, mangas, frente de gorra, caras del tote).",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la zona."),
             ("code", "VARCHAR(30)", "UQ", "PECHO_IZQ, ESPALDA, GORRA_FRENTE, TOTE_CARA_A…"),
             ("name", "VARCHAR(80)", "", "Nombre visible."),
         ]),
    dict(nombre="product_type_zones", modulo="personalizacion",
         desc="Qué zona admite qué técnica en cada tipo de producto, con su tamaño máximo, su recargo y el "
              "recuadro de la vista previa.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la regla."),
             ("product_type_id", "BIGINT", "FK -> product_types.id", "Tipo de producto."),
             ("zone_id", "BIGINT", "FK -> print_zones.id", "Zona."),
             ("technique_id", "BIGINT", "FK -> customization_techniques.id", "Técnica admitida."),
             ("max_width_cm", "NUMERIC(5,1)", "", "Ancho máximo del diseño."),
             ("max_height_cm", "NUMERIC(5,1)", "", "Alto máximo del diseño."),
             ("surcharge", "NUMERIC(12,2)", "", "Recargo por unidad al usar la zona."),
             ("preview_x", "NUMERIC(5,2)", "", "Posición horizontal en la vista previa (% de la imagen)."),
             ("preview_y", "NUMERIC(5,2)", "", "Posición vertical en la vista previa (%)."),
             ("preview_w", "NUMERIC(5,2)", "", "Ancho del recuadro en la vista previa (%)."),
             ("preview_h", "NUMERIC(5,2)", "", "Alto del recuadro en la vista previa (%)."),
         ],
         restricciones=["UNIQUE (product_type_id, zone_id, technique_id)",
                        "el recuadro de la vista previa cabe dentro de la imagen (x + w <= 100, y + h <= 100)"]),
    dict(nombre="design_uploads", modulo="personalizacion",
         desc="Imágenes que sube el cliente para personalizar. Se guardan en la base porque el disco del "
              "servidor de despliegue es efímero.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del diseño."),
             ("user_id", "BIGINT", "FK -> users.id", "Cliente que lo subió."),
             ("original_filename", "VARCHAR(255)", "", "Nombre del archivo original."),
             ("content_type", "VARCHAR(30)", "", "image/png o image/jpeg."),
             ("size_bytes", "INTEGER", "", "Tamaño en bytes (máximo 5 MB)."),
             ("sha256", "CHAR(64)", "", "Huella del contenido, para detectar duplicados."),
             ("data", "BYTEA", "", "Contenido binario de la imagen."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de subida."),
         ],
         restricciones=["tipo PNG o JPG", "1 B <= size_bytes <= 5 MB", "octet_length(data) = size_bytes"]),
    dict(nombre="quantity_tiers", modulo="personalizacion",
         desc="Escalas de mayoreo. Se aplica la de mayor min_quantity que no supere la cantidad del diseño.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la escala."),
             ("min_quantity", "INTEGER", "UQ", "Cantidad mínima: 1, 3, 6 o 12."),
             ("label", "VARCHAR(60)", "", "Unidad, Paquete de 3, Paquete de 6, Docena."),
             ("discount_percent", "NUMERIC(5,2)", "", "Descuento sobre el precio unitario."),
         ],
         restricciones=["min_quantity >= 1", "0 <= discount_percent < 100"]),

    # --------------------------------------------------------------------- compra
    dict(nombre="shipping_methods", modulo="compra",
         desc="Modalidades de entrega con su costo y plazo.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del método."),
             ("code", "VARCHAR(30)", "UQ", "LIMA_METROPOLITANA, PROVINCIAS o RECOJO_TIENDA."),
             ("name", "VARCHAR(80)", "", "Nombre visible."),
             ("cost", "NUMERIC(12,2)", "", "Costo del envío."),
             ("estimated_days", "INTEGER", "", "Plazo estimado en días."),
             ("requires_address", "BOOLEAN", "", "FALSE en el recojo en tienda."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
         ]),
    dict(nombre="orders", modulo="compra",
         desc="Cabecera del pedido. Copia la dirección para que no cambie si el cliente edita su libreta.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del pedido."),
             ("order_code", "VARCHAR(20)", "UQ", "Código visible para el cliente."),
             ("user_id", "BIGINT", "FK -> users.id", "Cliente."),
             ("status", "VARCHAR(20)", "", ESTADOS_PEDIDO + "."),
             ("subtotal", "NUMERIC(12,2)", "", "Suma de las líneas antes del descuento."),
             ("discount_amount", "NUMERIC(12,2)", "", "Descuento total por mayoreo."),
             ("shipping_cost", "NUMERIC(12,2)", "", "Costo del envío."),
             ("total_amount", "NUMERIC(12,2)", "", "subtotal - descuento + envío."),
             ("shipping_method_id", "BIGINT", "FK -> shipping_methods.id", "Modalidad de entrega."),
             ("receiver_name", "VARCHAR(160)", "", "Quien recibe o recoge."),
             ("phone", "VARCHAR(20)", "", "Teléfono de contacto."),
             ("department", "VARCHAR(60)", "", "Departamento (NULL en recojo en tienda)."),
             ("province", "VARCHAR(60)", "", "Provincia."),
             ("district", "VARCHAR(60)", "", "Distrito."),
             ("street", "VARCHAR(200)", "", "Calle y número."),
             ("reference", "VARCHAR(200)", "", "Referencia."),
             ("customer_note", "VARCHAR(500)", "", "Indicaciones del cliente."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de creación."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha del último cambio."),
         ],
         restricciones=["status dentro de los siete estados",
                        "total_amount = subtotal - discount_amount + shipping_cost",
                        "la dirección va completa o vacía"]),
    dict(nombre="order_lines", modulo="compra",
         desc="Una línea es un diseño sobre un producto. Congela los precios vigentes al comprar.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador de la línea."),
             ("order_id", "BIGINT", "FK -> orders.id", "Pedido."),
             ("product_id", "BIGINT", "FK -> products.id", "Producto base."),
             ("product_name", "VARCHAR(180)", "", "Nombre del producto al comprar."),
             ("technique_id", "BIGINT", "FK -> customization_techniques.id", "Técnica; NULL si no se personaliza."),
             ("design_upload_id", "BIGINT", "FK -> design_uploads.id", "Diseño del cliente."),
             ("quantity_total", "INTEGER", "", "Unidades del diseño (todas las tallas y colores)."),
             ("tier_min_quantity", "INTEGER", "", "Escala de mayoreo aplicada."),
             ("unit_base_price", "NUMERIC(12,2)", "", "Precio unitario de la prenda."),
             ("unit_customization_price", "NUMERIC(12,2)", "", "Técnica más recargos de zona, por unidad."),
             ("discount_percent", "NUMERIC(5,2)", "", "Descuento de la escala."),
             ("line_total", "NUMERIC(12,2)", "", "Importe de la línea con descuento."),
         ],
         restricciones=["técnica y diseño van juntos", "1 <= tier_min_quantity <= quantity_total"]),
    dict(nombre="order_line_zones", modulo="compra",
         desc="Zonas elegidas para una línea, con el recargo congelado al comprar.",
         campos=[
             ("order_line_id", "BIGINT", "PK, FK -> order_lines.id", "Línea del pedido."),
             ("zone_id", "BIGINT", "PK, FK -> print_zones.id", "Zona elegida."),
             ("surcharge", "NUMERIC(12,2)", "", "Recargo aplicado."),
         ]),
    dict(nombre="order_items", modulo="compra",
         desc="Reparto de una línea entre tallas y colores. La suma de quantity es quantity_total.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del ítem."),
             ("order_line_id", "BIGINT", "FK -> order_lines.id", "Línea a la que pertenece."),
             ("variant_id", "BIGINT", "FK -> product_variants.id", "Variante (talla y color)."),
             ("sku", "VARCHAR(80)", "", "SKU al comprar."),
             ("size_name", "VARCHAR(30)", "", "Talla al comprar."),
             ("color_name", "VARCHAR(60)", "", "Color al comprar."),
             ("quantity", "INTEGER", "", "Unidades de esta talla y color."),
         ],
         restricciones=["UNIQUE (order_line_id, variant_id)", "quantity > 0"]),
    dict(nombre="order_status_history", modulo="compra",
         desc="Trazabilidad de cada cambio de estado del pedido, para «Mis pedidos» y auditoría.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del registro."),
             ("order_id", "BIGINT", "FK -> orders.id", "Pedido."),
             ("from_status", "VARCHAR(20)", "", "Estado anterior; NULL al crear el pedido."),
             ("to_status", "VARCHAR(20)", "", "Estado nuevo."),
             ("changed_by", "BIGINT", "FK -> users.id", "Quién hizo el cambio; NULL si fue el sistema."),
             ("comment", "VARCHAR(500)", "", "Observación."),
             ("changed_at", "TIMESTAMPTZ", "", "Fecha y hora del cambio."),
         ],
         restricciones=["from_status distinto de to_status"]),
    dict(nombre="payments", modulo="compra",
         desc="Intentos de pago de un pedido. SIMULADO hasta integrar la pasarela real.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del pago."),
             ("order_id", "BIGINT", "FK -> orders.id", "Pedido."),
             ("provider", "VARCHAR(30)", "", "SIMULADO o el nombre de la pasarela."),
             ("provider_reference", "VARCHAR(120)", "UQ", "Referencia de la operación."),
             ("amount", "NUMERIC(12,2)", "", "Importe cobrado."),
             ("currency", "CHAR(3)", "", "Moneda ISO 4217 (PEN)."),
             ("status", "VARCHAR(20)", "", "PENDIENTE, APROBADO o RECHAZADO."),
             ("created_at", "TIMESTAMPTZ", "", "Inicio del intento."),
             ("confirmed_at", "TIMESTAMPTZ", "", "Confirmación; obligatoria si está APROBADO."),
         ],
         restricciones=["un solo pago APROBADO por pedido (índice único parcial)", "amount > 0"]),

    # -------------------------------------------------------------------- soporte
    dict(nombre="favorites", modulo="soporte",
         desc="Productos guardados por el cliente.",
         campos=[
             ("user_id", "BIGINT", "PK, FK -> users.id", "Cliente."),
             ("product_id", "BIGINT", "PK, FK -> products.id", "Producto guardado."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha en que se guardó."),
         ]),
    dict(nombre="banners", modulo="soporte",
         desc="Banners promocionales del inicio, con vigencia opcional.",
         campos=[
             ("id", "BIGINT", "PK", "Identificador del banner."),
             ("title", "VARCHAR(180)", "", "Título."),
             ("description", "TEXT", "", "Texto de apoyo."),
             ("image_url", "TEXT", "", "Imagen."),
             ("link_url", "TEXT", "", "Destino al hacer clic."),
             ("sort_order", "INTEGER", "", "Orden en el carrusel."),
             ("is_active", "BOOLEAN", "", "Baja lógica."),
             ("starts_at", "TIMESTAMPTZ", "", "Inicio de la vigencia."),
             ("ends_at", "TIMESTAMPTZ", "", "Fin de la vigencia (posterior al inicio)."),
             ("created_at", "TIMESTAMPTZ", "", "Fecha de alta."),
             ("updated_at", "TIMESTAMPTZ", "", "Fecha de la última modificación."),
         ]),
]

TABLA_POR_NOMBRE = {t["nombre"]: t for t in TABLAS}


def relaciones():
    """Devuelve la lista de (tabla_origen, campo, tabla_destino, campo_destino)."""
    out = []
    for t in TABLAS:
        for nombre, tipo, llave, _ in t["campos"]:
            if "FK ->" in llave:
                destino = llave.split("->")[1].strip()
                td, cd = destino.split(".")
                out.append((t["nombre"], nombre, td, cd))
    return out


def totales():
    """(tablas, campos, claves foráneas) del modelo."""
    return len(TABLAS), sum(len(t["campos"]) for t in TABLAS), len(relaciones())


if __name__ == "__main__":
    n_t, n_c, n_fk = totales()
    print(f"{n_t} tablas, {n_c} campos, {n_fk} claves foráneas")
