# Exporta la presentacion a PDF con PowerPoint, para poder revisarla lamina a lamina.
param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [Parameter(Mandatory = $true)][string]$Pdf
)

$ErrorActionPreference = "Stop"
$pp = New-Object -ComObject PowerPoint.Application
try {
    $deck = $pp.Presentations.Open($Pptx, $true, $false, $false)  # solo lectura, sin ventana
    $deck.SaveAs($Pdf, 32)   # 32 = ppSaveAsPDF
    Write-Output ("Laminas: " + $deck.Slides.Count)
    $deck.Close()
}
finally {
    $pp.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
Write-Output "PDF: $Pdf"
