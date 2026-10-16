# Build a fresh installer from the current code, in one command.
#
#   .\build.ps1                 # rebuild data+exe+installer
#   .\build.ps1 -Version 1.1.0  # also bump the installer version first
#   .\build.ps1 -Fonts          # also re-download the bundled fonts (rarely needed)
#
# Output: installer_output\WardrobeLookbook-Setup.exe
param([string]$Version = "", [switch]$Fonts)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py   = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$pyi  = Join-Path $PSScriptRoot ".venv\Scripts\pyinstaller.exe"
$iscc = Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"
if (-not (Test-Path $iscc)) { throw "Inno Setup compiler not found at $iscc" }

if ($Version) {
    Write-Host "Setting installer version to $Version" -ForegroundColor Cyan
    (Get-Content installer.iss) -replace '(#define AppVersion ").*(")', "`${1}$Version`${2}" |
        Set-Content installer.iss -Encoding UTF8
}

Write-Host "[1/3] Building data + images (viewer_data.json, wardrobe_web/) ..." -ForegroundColor Cyan
& $py build_assets.py

if ($Fonts) {
    Write-Host "[*]   Refreshing bundled fonts ..." -ForegroundColor Cyan
    & $py download_fonts.py
}

Write-Host "[2/3] Building the app executable ..." -ForegroundColor Cyan
& $pyi --noconfirm wardrobe.spec

Write-Host "[3/3] Building the installer ..." -ForegroundColor Cyan
& $iscc installer.iss | Select-Object -Last 2

Write-Host "Done -> installer_output\WardrobeLookbook-Setup.exe" -ForegroundColor Green
