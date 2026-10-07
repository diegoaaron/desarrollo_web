# -*- coding: utf-8 -*-
"""
Convierte un documento Markdown de clase_entregables/ a PDF.

Renderiza el .md a HTML con la identidad visual del proyecto (Arial, paleta Coral)
y lo imprime a PDF con Microsoft Edge en modo headless, que ya viene con Windows.

Uso:
    python md_a_pdf.py ../clase_entregables/Analisis_Brecha_Codigo_vs_Arquitectura.md
    (el PDF se escribe junto al .md, con el mismo nombre)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

NAVEGADORES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]

CSS = """
@page { size: A4; margin: 2cm 1.8cm; }
body { font-family: Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #2b1a20; }
h1 { color: #3D1927; font-size: 20pt; border-bottom: 3px solid #6D2E46; padding-bottom: 6px; margin-top: 0; }
h2 { color: #6D2E46; font-size: 15pt; border-bottom: 1px solid #D9AFAF; padding-bottom: 3px;
     margin-top: 26px; page-break-after: avoid; }
h3 { color: #3D1927; font-size: 12pt; margin-top: 18px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px; font-size: 9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #6D2E46; color: #fff; text-align: left; padding: 5px 6px; }
td { border: 1px solid #D9AFAF; padding: 4px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #FBF7F2; }
code { font-family: Consolas, monospace; font-size: 8.8pt; background: #F3ECE4; padding: 1px 3px; border-radius: 3px; }
pre { background: #F3ECE4; padding: 8px 10px; border-left: 3px solid #A26769; font-size: 8.5pt;
      white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { margin: 10px 0; padding: 6px 12px; background: #FBF7F2; border-left: 4px solid #A26769; color: #3D1927; }
blockquote p { margin: 4px 0; }
hr { border: none; border-top: 1px solid #D9AFAF; margin: 20px 0; }
"""


def buscar_navegador():
    for ruta in NAVEGADORES:
        if ruta.exists():
            return ruta
    sys.exit("No se encontró Microsoft Edge ni Google Chrome para imprimir el PDF.")


def convertir(md_path: Path) -> Path:
    cuerpo = markdown.markdown(md_path.read_text(encoding="utf-8"),
                               extensions=["tables", "fenced_code", "sane_lists", "toc"])
    html = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            f"<title>{md_path.stem}</title><style>{CSS}</style></head><body>{cuerpo}</body></html>")
    pdf_path = md_path.with_suffix(".pdf")
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "documento.html"
        html_path.write_text(html, encoding="utf-8")
        subprocess.run([str(buscar_navegador()), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={Path(tmp) / 'perfil'}",
                        f"--print-to-pdf={pdf_path.resolve()}", html_path.as_uri()],
                       check=True, capture_output=True)
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(convertir(Path(sys.argv[1])))
