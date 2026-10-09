$ErrorActionPreference = 'Stop'

$miktexBin = Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'
$pdflatex = Join-Path $miktexBin 'pdflatex.exe'
$bibtex = Join-Path $miktexBin 'bibtex.exe'

if (-not (Test-Path $pdflatex) -or -not (Test-Path $bibtex)) {
    throw "MiKTeX was not found at $miktexBin. Install MiKTeX or update the path in build.ps1."
}

& $pdflatex '-jobname=F26-131' '-interaction=nonstopmode' '-file-line-error' 'main.tex'
& $bibtex 'F26-131'
& $pdflatex '-jobname=F26-131' '-interaction=nonstopmode' '-file-line-error' 'main.tex'
& $pdflatex '-jobname=F26-131' '-interaction=nonstopmode' '-file-line-error' 'main.tex'

if (-not (Test-Path 'F26-131.pdf')) {
    throw 'The LaTeX build did not produce F26-131.pdf.'
}

Write-Host 'Build complete: F26-131.pdf'