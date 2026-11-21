# Regenera todos los entregables usando SIEMPRE el interprete del entorno virtual
# del proyecto. Es el punto de entrada unico: no invocar python "a pelo".
#
#   .\scripts\generar.ps1              # figuras + informe + presentacion + PDFs
#   .\scripts\generar.ps1 -SinPdf      # omite la exportacion a PDF (no requiere Office)
#
# Las capturas reales del informe (clase_entregables/figuras/capturas/) NO se regeneran aqui:
# requieren la aplicacion levantada con el perfil demo. Se toman aparte con
#   .venv\Scripts\python scripts\capturas.py --admin-password <DEMO_ADMIN_PASSWORD>

param(
    [switch]$SinPdf
)

$ErrorActionPreference = "Stop"

$raiz = Split-Path -Parent $PSScriptRoot
$py = Join-Path $raiz ".venv\Scripts\python.exe"
$scripts = Join-Path $raiz "scripts"
$entregables = Join-Path $raiz "clase_entregables"

if (-not (Test-Path $py)) {
    Write-Error @"
No existe el entorno virtual en $py
Crealo con:
    python -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt
"@
}

$env:PYTHONIOENCODING = "utf-8"

Write-Host "[1/3] Figuras..." -ForegroundColor Cyan
& $py (Join-Path $scripts "figuras.py")
if ($LASTEXITCODE -ne 0) { throw "figuras.py fallo" }

Write-Host "[2/3] Informe..." -ForegroundColor Cyan
& $py (Join-Path $scripts "informe.py")
if ($LASTEXITCODE -ne 0) { throw "informe.py fallo" }

Write-Host "[3/3] Presentacion..." -ForegroundColor Cyan
& $py (Join-Path $scripts "presentacion.py")
if ($LASTEXITCODE -ne 0) { throw "presentacion.py fallo" }

if ($SinPdf) {
    Write-Host "Listo (sin PDF)." -ForegroundColor Green
    Write-Host "Recuerda: el indice del Word queda vacio hasta ejecutar exportar.ps1." -ForegroundColor Yellow
    return
}

$docx = Join-Path $entregables "Informe_Proyecto_Final_Coral_Shop.docx"
$pptx = Join-Path $entregables "Presentacion_Proyecto_Final_Coral_Shop.pptx"

Write-Host "[+] Indice del Word y PDF..." -ForegroundColor Cyan
& (Join-Path $scripts "exportar.ps1") -Docx $docx -Pdf ($docx -replace '\.docx$', '.pdf')

Write-Host "[+] PDF de la presentacion..." -ForegroundColor Cyan
& (Join-Path $scripts "exportar_ppt.ps1") -Pptx $pptx -Pdf ($pptx -replace '\.pptx$', '.pdf')

Write-Host "Listo. Entregables en $entregables" -ForegroundColor Green
