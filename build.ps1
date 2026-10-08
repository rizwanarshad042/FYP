$ErrorActionPreference = 'Stop'

$miktexBin = Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'
$pdflatex = Join-Path $miktexBin 'pdflatex.exe'
$bibtex = Join-Path $miktexBin 'bibtex.exe'

if (-not (Test-Path $pdflatex) -or -not (Test-Path $bibtex)) {
    throw "MiKTeX was not found at $miktexBin. Install MiKTeX or update the path in build.ps1."
}

& $pdflatex '-interaction=nonstopmode' '-file-line-error' 'main.tex'
& $bibtex 'main'
& $pdflatex '-interaction=nonstopmode' '-file-line-error' 'main.tex'
& $pdflatex '-interaction=nonstopmode' '-file-line-error' 'main.tex'

if (-not (Test-Path 'main.pdf')) {
    throw 'The LaTeX build did not produce main.pdf.'
}

Write-Host 'Build complete: main.pdf'