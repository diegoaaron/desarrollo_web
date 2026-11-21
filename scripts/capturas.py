# -*- coding: utf-8 -*-
"""Capturas reales de la aplicación para el informe y la presentación (Anexo B).

Requiere la aplicación levantada en local con el perfil demo (ver README §3.1):
PostgreSQL en Docker, backend en :8082 con SPRING_PROFILES_ACTIVE=dev,demo y
DEMO_ADMIN_PASSWORD, y frontend en :5173. Usa Microsoft Edge instalado (channel="msedge"),
así que no descarga navegadores.

    ..\\.venv\\Scripts\\python capturas.py --admin-password <DEMO_ADMIN_PASSWORD>

Recorre la historia de referencia: un cliente demo personaliza 12 polos bordados en el
pecho izquierdo (4 S, 4 M, 4 L), paga (primero rechazado y luego aprobado) y el
administrador avanza el pedido. Cada ejecución crea un pedido nuevo con datos ficticios.
"""

import argparse
import re
import os

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "clase_entregables", "figuras", "capturas")
TIENDA = "http://localhost:5173"
CLIENTE = ("renzo.paredes@demo.coralshop.pe", "Cliente2026")
ADMIN = "admin@demo.coralshop.pe"
PRODUCTO = 10          # Polo clásico de algodón (datos demo)
TARJETA_OK = "4111 1111 1111 1111"
TARJETA_RECHAZADA = "4000 0000 0000 0002"


def logo_demo(ruta):
    """Logo ficticio para la demo: un círculo azul con las iniciales «LM»."""
    img = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((40, 40, 560, 560), fill=(60, 110, 143, 255))
    d.text((300, 300), "LM", font=ImageFont.truetype("arialbd.ttf", 190),
           fill=(255, 255, 255, 255), anchor="mm")
    img.save(ruta)


class Capturador:
    def __init__(self, page):
        self.pg = page

    def foto(self, nombre, completa=False, espera=900):
        self.pg.wait_for_timeout(espera)
        ruta = os.path.join(SALIDA, nombre + ".png")
        if completa:
            # Página completa: la cabecera fija deja de flotar y se omite el pie de página.
            self.pg.evaluate("""() => {
                for (const e of document.querySelectorAll('body *')) {
                    const p = getComputedStyle(e).position;
                    if (p === 'sticky' || p === 'fixed') e.style.position = 'static';
                }
                document.querySelectorAll('footer').forEach(f => f.style.display = 'none');
                window.scrollTo(0, 0);
            }""")
            self.pg.wait_for_timeout(300)
        self.pg.screenshot(path=ruta, full_page=completa)
        if completa:
            self.pg.evaluate("() => document.querySelectorAll('footer').forEach(f => f.style.display = '')")
        print("  ok", nombre)

    def ir(self, ruta, espera=1800):
        self.pg.goto(TIENDA + ruta)
        self.pg.wait_for_load_state("load")
        self.pg.wait_for_timeout(espera)

    def login(self, correo, clave):
        self.ir("/login", 600)
        self.pg.fill("input[name=email]", correo)
        self.pg.fill("input[type=password]", clave)
        self.pg.click("button[type=submit]")
        self.pg.wait_for_url(lambda u: "/login" not in u, timeout=15000)
        self.pg.wait_for_timeout(800)

    def volcar(self):
        """Ayuda de depuración: texto visible y botones de la pantalla actual."""
        print(self.pg.url)
        print(self.pg.inner_text("body")[:2500])
        for el in self.pg.query_selector_all("button, input, select"):
            t = (el.inner_text() or el.get_attribute("name") or el.get_attribute("type") or "")
            print("  EL", el.evaluate("e => e.tagName"), t.strip().replace("\n", " ")[:70])


def tienda(c, logo, solo_hasta=None):
    pg = c.pg
    c.ir("/")
    c.foto("C01_inicio")
    c.ir("/products")
    c.foto("C02_catalogo")

    c.login(*CLIENTE)
    c.ir(f"/product/{PRODUCTO}")
    c.foto("C03_ficha", espera=400)
    pg.get_by_role("button", name="Blanco").click()
    pg.get_by_role("button", name="Bordado").click()
    pg.wait_for_timeout(400)
    pg.get_by_text("Pecho izquierdo", exact=True).first.click()
    pg.set_input_files("input[type=file]", logo)
    pg.wait_for_timeout(2500)
    fila = pg.locator("tr", has_text="Blanco")
    for i in range(3):
        fila.locator("input[type=number]").nth(i).fill("4")
    pg.wait_for_timeout(2500)
    c.foto("C04_personalizador", completa=True)
    if solo_hasta == "personalizador":
        c.volcar()
        return
    pg.get_by_role("button", name="Agregar al carrito").click()
    pg.wait_for_timeout(1200)
    c.ir("/cart")
    c.foto("C05_carrito", completa=True)
    c.ir("/checkout", 2500)
    pg.get_by_text("Envío a Lima Metropolitana").click()
    pg.wait_for_timeout(1500)
    c.foto("C06_checkout", completa=True)
    if solo_hasta == "checkout":
        c.volcar()
        return
    pg.get_by_role("button", name="Confirmar pedido e ir al pago").click()
    pg.wait_for_timeout(2500)
    c.foto("C07_pago", completa=True)
    if solo_hasta == "pago":
        c.volcar()
        return
    codigo = pg.inner_text("main").split("Pedido ")[1].split(" ")[0]

    def pagar(tarjeta):
        pg.get_by_label("Número de tarjeta").fill(tarjeta)
        pg.get_by_label("Titular").fill("RENZO PAREDES")
        pg.get_by_label("Mes").select_option("08")
        pg.get_by_label("Año").select_option("2029")
        pg.get_by_label("CVV").fill("123")
        pg.get_by_role("button", name="Pagar").click()
        pg.wait_for_timeout(2500)

    pagar(TARJETA_RECHAZADA)
    c.foto("C08_pago_rechazado", completa=True)
    pagar(TARJETA_OK)
    c.foto("C09_confirmacion", completa=True)

    c.ir("/account/orders")
    c.foto("C10_mis_pedidos", completa=True)
    pedidos = pg.evaluate("() => fetch('/api/orders/me', {credentials: 'include'}).then(r => r.json())")
    lista = pedidos["items"] if isinstance(pedidos, dict) else pedidos
    entregado = next(p for p in lista if p["status"] == "ENTREGADO")
    c.ir(f"/account/orders/{entregado['orderCode']}")
    c.foto("C11_detalle_pedido", completa=True)
    c.ir("/account/orders")
    pg.get_by_role("button", name=re.compile("^Notificaciones")).first.click()
    c.foto("C12_campana")
    return codigo


def admin(c, clave, codigo):
    pg = c.pg
    c.login(ADMIN, clave)
    c.ir("/admin")
    c.foto("C13_tablero", completa=True)
    c.ir("/admin/products")
    c.foto("C14_productos_admin", completa=True)
    c.ir("/admin/products/new")
    c.foto("C15_producto_form", completa=True)
    c.ir("/admin/categories")
    c.foto("C16_categorias")
    c.ir("/admin/orders")
    c.foto("C17_bandeja_pedidos")
    pedido = pg.evaluate("() => fetch('/api/orders?size=50', {credentials: 'include'}).then(r => r.json())")
    oid = next(o["id"] for o in pedido["items"] if o["orderCode"] == codigo)
    c.ir(f"/admin/orders/{oid}")
    pg.locator("select").first.select_option(label="En producción")
    pg.get_by_role("button", name="Actualizar estado").click()
    pg.wait_for_timeout(2000)
    c.foto("C18_detalle_admin", completa=True)
    c.ir("/admin/users")
    c.foto("C19_usuarios")
    c.ir("/api/docs", 3500)
    c.foto("C20_swagger")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--admin-password", required=True)
    ap.add_argument("--solo-hasta", default=None)
    args = ap.parse_args()
    os.makedirs(SALIDA, exist_ok=True)
    logo = os.path.join(SALIDA, "logo_LM.png")
    logo_demo(logo)
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="msedge")
        ctx = nav.new_context(viewport={"width": 1440, "height": 900}, locale="es-PE")
        c = Capturador(ctx.new_page())
        codigo = tienda(c, logo, args.solo_hasta)
        if codigo:
            ctx2 = nav.new_context(viewport={"width": 1440, "height": 900}, locale="es-PE")
            admin(Capturador(ctx2.new_page()), args.admin_password, codigo)
        nav.close()
    os.remove(logo)


if __name__ == "__main__":
    main()
