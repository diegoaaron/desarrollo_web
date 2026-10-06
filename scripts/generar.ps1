# Regenera todos los entregables usando SIEMPRE el interprete del entorno virtual
# del proyecto. Es el punto de entrada unico: no invocar python "a pelo".
#
#   .\scripts\generar.ps1              # figuras + informe + presentacion + PDFs
#   .\scripts\generar.ps1 -SinPdf      # omite la exportacion a PDF (no requiere Office)

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

Write-Host "[1/4] Figuras..." -ForegroundColor Cyan
& $py (Join-Path $scripts "figuras.py")
if ($LASTEXITCODE -ne 0) { throw "figuras.py fallo" }

Write-Host "[2/4] Mockups (Anexo B)..." -ForegroundColor Cyan
& $py (Join-Path $scripts "mockups.py")
if ($LASTEXITCODE -ne 0) { throw "mockups.py fallo" }

Write-Host "[3/4] Informe..." -ForegroundColor Cyan
& $py (Join-Path $scripts "informe.py")
if ($LASTEXITCODE -ne 0) { throw "informe.py fallo" }

Write-Host "[4/4] Presentacion..." -ForegroundColor Cyan
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
