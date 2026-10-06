# -*- coding: utf-8 -*-
"""
Restaura la acentuacion espanola en los literales de cadena de los scripts.

Se aplica UNICAMENTE a los tokens de tipo STRING, de modo que los nombres de
funciones, variables y argumentos del codigo Python quedan intactos. Los
identificadores del dominio (nombres de tabla, campos, clases Java y valores de
enumeracion) se protegen antes de aplicar las reglas.

Uso:  python acentos.py archivo1.py archivo2.py ...
Es idempotente: volver a ejecutarlo sobre un archivo ya corregido no lo altera.
"""

import io
import re
import sys
import tokenize

# --------------------------------------------------------------------------
# 1. Tokens que NUNCA deben acentuarse (valores de enumeracion y codigo)
# --------------------------------------------------------------------------
PROTEGIDOS = [
    "EN_PRODUCCION", "LIBERACION", "PROMOCION", "DISENADOR", "DISENO",
    "MONTO_FIJO", "el sitio publica politicas", "El sitio publica politicas",
]

# --------------------------------------------------------------------------
# 2. Palabras sueltas (se generan las variantes minuscula, Capitalizada y MAYUSCULA)
# --------------------------------------------------------------------------
PALABRAS = {
    # ---- ene
    "ano": "año", "anos": "años",
    "diseno": "diseño", "disenos": "diseños", "disenar": "diseñar",
    "disena": "diseña", "disenan": "diseñan", "disenada": "diseñada",
    "disenado": "diseñado", "disenador": "diseñador", "disenadores": "diseñadores",
    "tamano": "tamaño", "tamanos": "tamaños",
    "pequena": "pequeña", "pequenas": "pequeñas",
    "pequeno": "pequeño", "pequenos": "pequeños",
    "campana": "campaña", "campanas": "campañas",
    "senala": "señala", "senalar": "señalar", "senalado": "señalado",
    "resena": "reseña", "resenas": "reseñas", "resenar": "reseñar",
    "resenado": "reseñado", "resenados": "reseñados",
    "manana": "mañana",
    "anadir": "añadir", "anade": "añade", "anaden": "añaden",
    "anadido": "añadido", "anadiria": "añadiría",
    "dueno": "dueño", "duenos": "dueños",
    "espanola": "española", "espanol": "español",

    # ---- nombres propios
    "peru": "perú", "damian": "damián", "aaron": "aarón",
    "geronimo": "gerónimo", "jesus": "jesús",

    # ---- adverbios y conectores
    "ademas": "además", "asi": "así", "aqui": "aquí", "despues": "después",
    "segun": "según", "mas": "más", "tambien": "también", "ahi": "ahí",

    # ---- adjetivos y sustantivos esdrujulos o llanos con tilde
    "ultimo": "último", "ultima": "última", "ultimos": "últimos", "ultimas": "últimas",
    "unico": "único", "unica": "única", "unicos": "únicos", "unicas": "únicas",
    "unicamente": "únicamente",
    "rapido": "rápido", "rapida": "rápida", "rapidos": "rápidos", "rapidas": "rápidas",
    "practica": "práctica", "practicas": "prácticas", "practico": "práctico",
    "basico": "básico", "basica": "básica", "basicos": "básicos", "basicas": "básicas",
    "automatico": "automático", "automatica": "automática",
    "automaticos": "automáticos", "automaticas": "automáticas",
    "automaticamente": "automáticamente",
    "logico": "lógico", "logica": "lógica", "logicos": "lógicos", "logicas": "lógicas",
    "grafico": "gráfico", "grafica": "gráfica", "graficos": "gráficos",
    "tecnico": "técnico", "tecnica": "técnica", "tecnicos": "técnicos",
    "tecnicas": "técnicas",
    "publico": "público", "publicos": "públicos", "publicas": "públicas",
    "especifico": "específico", "especifica": "específica",
    "especificos": "específicos", "especificas": "específicas",
    "especificamente": "específicamente",
    "critico": "crítico", "critica": "crítica", "criticos": "críticos",
    "criticas": "críticas",
    "estrategico": "estratégico", "estrategica": "estratégica",
    "estrategicas": "estratégicas", "estrategicos": "estratégicos",
    "academico": "académico", "academica": "académica",
    "analisis": "análisis",
    "diagnostico": "diagnóstico", "diagnosticos": "diagnósticos",
    "metodo": "método", "metodos": "métodos", "metodologia": "metodología",
    "catalogo": "catálogo", "catalogos": "catálogos",
    "articulo": "artículo", "articulos": "artículos",
    "parametro": "parámetro", "parametros": "parámetros",
    "maquina": "máquina", "maquinas": "máquinas",
    "pagina": "página", "paginas": "páginas",
    "codigo": "código", "codigos": "códigos",
    "numero": "número", "numeros": "números", "numerico": "numérico",
    "minimo": "mínimo", "minima": "mínima", "minimos": "mínimos", "minimas": "mínimas",
    "maximo": "máximo", "maxima": "máxima", "maximos": "máximos", "maximas": "máximas",
    "optimo": "óptimo", "optima": "óptima",
    "proximo": "próximo", "proxima": "próxima", "proximos": "próximos",
    "termino": "término", "terminos": "términos",
    "indice": "índice", "indices": "índices",
    "limite": "límite", "limites": "límites",
    "movil": "móvil", "moviles": "móviles",
    "facil": "fácil", "faciles": "fáciles", "facilmente": "fácilmente",
    "dificil": "difícil", "dificiles": "difíciles",
    "util": "útil", "utiles": "útiles",
    "estandar": "estándar", "estandares": "estándares",
    "imagenes": "imágenes", "margenes": "márgenes", "ordenes": "órdenes",
    "jovenes": "jóvenes", "volumenes": "volúmenes",
    "caracteristica": "característica", "caracteristicas": "características",
    "multiples": "múltiples", "multiple": "múltiple",
    "generico": "genérico", "generica": "genérica",
    "periodico": "periódico", "telefonico": "telefónico",
    "simultaneas": "simultáneas", "simultaneo": "simultáneo",
    "area": "área", "areas": "áreas",
    "sintoma": "síntoma", "sintomas": "síntomas",
    "raiz": "raíz", "raices": "raíces",
    "pais": "país", "paises": "países",
    "integro": "íntegro",
    "comun": "común",
    "razon": "razón",
    "telefono": "teléfono",
    "bitacora": "bitácora",
    "teoria": "teoría", "teorico": "teórico",

    # ---- terminados en -ia con tilde
    "linea": "línea", "lineas": "líneas",
    "dia": "día", "dias": "días",
    "via": "vía", "vias": "vías",
    "guia": "guía", "guias": "guías",
    "garantia": "garantía", "garantias": "garantías",
    "categoria": "categoría", "categorias": "categorías",
    "galeria": "galería", "galerias": "galerías",
    "auditoria": "auditoría",
    "ingenieria": "ingeniería",
    "jerarquia": "jerarquía", "jerarquica": "jerárquica",
    "jerarquicas": "jerárquicas", "jerarquico": "jerárquico",
    "geografico": "geográfico", "geografica": "geográfica",
    "historico": "histórico", "historica": "histórica", "historicos": "históricos",
    "economico": "económico", "economica": "económica",
    "politico": "político", "politica": "política", "politicas": "políticas",
    "ecologico": "ecológico",
    "tecnologico": "tecnológico", "tecnologica": "tecnológica",
    "tecnologia": "tecnología", "tecnologias": "tecnologías",
    "electronico": "electrónico", "electronica": "electrónica",

    # ---- formas verbales
    "estan": "están", "esten": "estén",
    "sera": "será", "seran": "serán",
    "construiran": "construirán", "incorporaran": "incorporarán",
    "priorizaran": "priorizarán", "escribira": "escribirá",
    "obligaria": "obligaría", "haria": "haría", "exigiria": "exigiría",
    "implicaria": "implicaría", "permitiria": "permitiría",
    "costaria": "costaría", "multiplicaria": "multiplicaría",
    "tendria": "tendría", "seria": "sería", "deberia": "debería",
    "podria": "podría", "podrian": "podrían",
    "demostro": "demostró", "concentro": "concentró", "confirmo": "confirmó",
    "origino": "originó", "ejecuto": "ejecutó", "solicito": "solicitó",
    "consumio": "consumió", "devolvio": "devolvió", "subio": "subió",
    "quedo": "quedó", "compro": "compró", "compre": "compré",
    "fallo": "falló",

    # ---- segunda pasada de vocabulario
    "arbol": "árbol", "busqueda": "búsqueda", "calculo": "cálculo",
    "recalculo": "recálculo", "gestion": "gestión", "modulo": "módulo",
    "modulos": "módulos", "ningun": "ningún", "problematica": "problemática",
    "proposito": "propósito", "serigrafia": "serigrafía",
    "tipografia": "tipografía", "titulo": "título", "titulos": "títulos",
    "vineta": "viñeta", "vinetas": "viñetas", "maria": "maría",
    "agnostico": "agnóstico", "almacen": "almacén", "ambito": "ámbito",
    "ambiguedades": "ambigüedades", "anadirlos": "añadirlos",
    "autonomo": "autónomo", "boton": "botón", "cercania": "cercanía",
    "contrasena": "contraseña", "contrasenas": "contraseñas",
    "cronologico": "cronológico", "demas": "demás", "envio": "envío",
    "envios": "envíos", "estatico": "estático", "estetico": "estético",
    "exito": "éxito", "fisica": "física", "fisico": "físico",
    "fisicamente": "físicamente", "foranea": "foránea", "foraneas": "foráneas",
    "limena": "limeña", "logistica": "logística", "mayusculas": "mayúsculas",
    "menu": "menú", "mensajeria": "mensajería", "nucleo": "núcleo",
    "rubrica": "rúbrica", "subcategorias": "subcategorías",
    "traves": "través", "reves": "revés", "vacio": "vacío",
    "volatil": "volátil", "cupon": "cupón", "patron": "patrón",
    "identico": "idéntico", "identica": "idéntica",
    "explicito": "explícito", "explicita": "explícita",
    "explicitamente": "explícitamente",
    "existia": "existía", "reune": "reúne", "confia": "confía",
    "enfrian": "enfrían", "envia": "envía", "envian": "envían",
    "reenvia": "reenvía", "agoto": "agotó", "mostro": "mostró",
    "aplico": "aplicó", "emplearan": "emplearán", "quedaran": "quedarán",
    "ofreciendoles": "ofreciéndoles",

    # ---- excepciones al patron -sion / -xion
    "conexion": "conexión",
}

# --------------------------------------------------------------------------
# 3. Frases: casos donde la misma grafia puede o no llevar tilde
# --------------------------------------------------------------------------
FRASES = [
    # interrogativos indirectos
    ("Por que Coral Shop", "Por qué Coral Shop"),
    ("por que una plataforma", "por qué una plataforma"),
    ("Por que un contenedor", "Por qué un contenedor"),
    ("Que resuelve", "Qué resuelve"),
    ("que problema resuelve", "qué problema resuelve"),
    ("indicando que talla", "indicando qué talla"),
    ("indica que talla", "indica qué talla"),
    ("informa que talla", "informa qué talla"),
    ("saber quien cambio que y cuando", "saber quién cambió qué y cuándo"),
    ("registran quien hizo que y cuando", "registran quién hizo qué y cuándo"),
    ("quien y cuando hizo cada cambio", "quién y cuándo hizo cada cambio"),
    ("mira como queda", "mira cómo queda"),
    ("ver como queda", "ver cómo queda"),
    ("Como se resuelve", "Cómo se resuelve"),
    ("como se resuelve", "cómo se resuelve"),
    ("muestra como colaboran", "muestra cómo colaboran"),
    ("resume como Coral Shop", "resume cómo Coral Shop"),
    ("explica como el servidor", "explica cómo el servidor"),
    ("Donde se aplica", "Dónde se aplica"),
    ("Que puede hacer", "Qué puede hacer"),
    ("saber que me falta", "saber qué me falta"),
    ("ver como va la venta", "ver cómo va la venta"),

    # verbo estar
    ("El cliente esta autenticado", "El cliente está autenticado"),
    ("esta activo, dentro de vigencia", "está activo, dentro de vigencia"),
    ("pedido esta en marcha", "pedido está en marcha"),
    ("cuyo stock este por debajo", "cuyo stock esté por debajo"),
    ("una funcionalidad esta terminada", "una funcionalidad está terminada"),
    ("esta repartidas", "está repartidas"),
    ("no estan repartidas", "no están repartidas"),
    ("La arquitectura esta", "La arquitectura está"),
    ("que esta disponible", "que está disponible"),

    # adjetivo valido / verbo validar
    ("transiciones validas", "transiciones válidas"),
    ("Transiciones validas", "Transiciones válidas"),
    ("transicion valida", "transición válida"),
    ("una transicion no valida", "una transición no válida"),

    # otras formas ambiguas
    ("que aun no", "que aún no"),
    ("se diseno como parte", "se diseñó como parte"),
    ("Fecha en que se marco", "Fecha en que se marcó"),
    ("Tienda publica", "Tienda pública"),
    ("TIENDA PUBLICA", "TIENDA PÚBLICA"),
    ("tienda publica", "tienda pública"),
    ("Interfaz publica", "Interfaz pública"),
]


def _variantes(base, acentuada):
    """Genera las tres variantes de capitalizacion de un par de palabras."""
    yield base, acentuada
    yield base.capitalize(), acentuada.capitalize()
    yield base.upper(), acentuada.upper()


_REGLAS = []
for _b, _a in PALABRAS.items():
    for _bv, _av in _variantes(_b, _a):
        _REGLAS.append((re.compile(r"\b" + _bv + r"\b"), _av))

# patrones generales de terminacion
_TERMINACIONES = [
    (re.compile(r"\b([A-Za-zÁÉÍÓÚÑáéíóúñ]+?)cion\b"), "ción"),
    (re.compile(r"\b([A-Za-zÁÉÍÓÚÑáéíóúñ]+?)sion\b"), "sión"),
    (re.compile(r"\b([A-Z0-9ÁÉÍÓÚÑ]+?)CION\b"), "CIÓN"),
    (re.compile(r"\b([A-Z0-9ÁÉÍÓÚÑ]+?)SION\b"), "SIÓN"),
]


def transformar(texto):
    # 1. proteger
    marcas = {}
    for i, tok in enumerate(PROTEGIDOS):
        marca = f"\x00{i}\x00"
        if tok in texto:
            texto = texto.replace(tok, marca)
            marcas[marca] = tok

    # 2. terminaciones -cion / -sion
    for patron, sufijo in _TERMINACIONES:
        texto = patron.sub(lambda m: m.group(1) + sufijo, texto)

    # 3. palabras sueltas
    for patron, reemplazo in _REGLAS:
        texto = patron.sub(reemplazo, texto)

    # 4. frases ambiguas
    for viejo, nuevo in FRASES:
        texto = texto.replace(viejo, nuevo)

    # 5. restaurar
    for marca, tok in marcas.items():
        texto = texto.replace(marca, tok)
    return texto


def procesar(ruta):
    src = io.open(ruta, encoding="utf-8").read()
    # desplazamiento del inicio de cada linea
    inicios = [0]
    for linea in src.splitlines(keepends=True):
        inicios.append(inicios[-1] + len(linea))

    def offset(fila, col):
        return inicios[fila - 1] + col

    cambios = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tokenize.tok_name[tok.type] not in ("STRING", "FSTRING_MIDDLE"):
            continue
        nuevo = transformar(tok.string)
        if nuevo != tok.string:
            cambios.append((offset(*tok.start), offset(*tok.end), nuevo))

    if not cambios:
        print(f"  sin cambios  {ruta}")
        return 0
    for ini, fin, nuevo in reversed(cambios):
        src = src[:ini] + nuevo + src[fin:]
    io.open(ruta, "w", encoding="utf-8").write(src)
    print(f"  {len(cambios):>4} literales corregidos  {ruta}")
    return len(cambios)


if __name__ == "__main__":
    total = 0
    for ruta in sys.argv[1:]:
        total += procesar(ruta)
    print("Total de literales corregidos:", total)
