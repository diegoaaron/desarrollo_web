# Abre el .docx en Word, actualiza el indice (campo TOC) y exporta una copia en PDF.
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [Parameter(Mandatory = $true)][string]$Pdf
)

$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $false)

    # Actualizar campos e indice
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Repaginate()

    $doc.Save()
    $doc.SaveAs([ref]$Pdf, [ref]17)   # 17 = wdFormatPDF
    Write-Output ("Paginas: " + $doc.ComputeStatistics(2))
    $doc.Close($false)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "PDF: $Pdf"
