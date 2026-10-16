# Build a fresh installer AND update the installed app in place, in one command.
#
#   .\deploy.ps1                 # rebuild, then silently update the installed app
#   .\deploy.ps1 -Version 1.1.0  # bump version, rebuild, then update
#
# Triggers one UAC admin prompt (the install writes to Program Files). The running
# app is closed automatically during the update; relaunch it from the Start menu.
param([string]$Version = "")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Version) { & "$PSScriptRoot\build.ps1" -Version $Version }
else          { & "$PSScriptRoot\build.ps1" }

$setup = Join-Path $PSScriptRoot "installer_output\WardrobeLookbook-Setup.exe"
if (-not (Test-Path $setup)) { throw "Installer not found at $setup" }

Write-Host "Updating the installed app (approve the admin prompt) ..." -ForegroundColor Cyan
Start-Process -FilePath $setup `
    -ArgumentList "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART" `
    -Verb RunAs -Wait

Write-Host "Updated. Launch 'Wardrobe Lookbook' from the Start menu." -ForegroundColor Green
