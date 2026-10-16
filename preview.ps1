# Preview the viewer WITHOUT building or touching the installed app.
#
#   .\preview.ps1            # open in your browser (http://localhost:5000); live-reloads on edit
#   .\preview.ps1 -Native    # open in the native desktop window instead
#   .\preview.ps1 -Rebuild   # first regenerate data/images (needed after data/image changes)
#
# Template / CSS / JS edits show up on a browser refresh. Stop with Ctrl+C.
param([switch]$Native, [switch]$Rebuild)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if ($Rebuild) {
    Write-Host "Regenerating viewer_data.json + wardrobe_web/ ..." -ForegroundColor Cyan
    & $py build_assets.py
}

if ($Native) {
    Write-Host "Opening native preview window (close it to stop)..." -ForegroundColor Cyan
    & $py desktop.py
} else {
    Write-Host "Preview at http://localhost:5000  (Ctrl+C to stop)" -ForegroundColor Cyan
    Start-Process "http://localhost:5000"
    & $py app.py
}
