; Inno Setup script for the Wardrobe Lookbook desktop app.
; Build the app first:  .\.venv\Scripts\pyinstaller.exe wardrobe.spec
; Then compile:          & "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" installer.iss
; Output: installer_output\WardrobeLookbook-Setup.exe

#define AppName "Wardrobe Lookbook"
#define AppVersion "1.0.0"
#define AppExe "WardrobeLookbook.exe"
#define Publisher "Akhil"

[Setup]
AppId={{B6E2D7A1-7C3E-49E2-9A1C-WARDROBE0001}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#Publisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#AppExe}
SetupIconFile=assets\app.ico
OutputDir=installer_output
OutputBaseFilename=WardrobeLookbook-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Clean in-place upgrades: close the running app during update, don't force a reboot.
CloseApplications=yes
RestartApplications=no
; Per-machine install needs admin; drop to lowest for a per-user install with no UAC.
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; The entire PyInstaller onedir output.
Source: "dist\WardrobeLookbook\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
; WebView2 Evergreen bootstrapper (run only if the runtime is missing).
Source: "vendor\MicrosoftEdgeWebview2Setup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
; Provision the WebView2 runtime silently if it isn't already present.
Filename: "{tmp}\MicrosoftEdgeWebview2Setup.exe"; Parameters: "/silent /install"; \
  StatusMsg: "Installing WebView2 runtime..."; Check: WebView2Missing; Flags: waituntilterminated
; Offer to launch after install.
Filename: "{app}\{#AppExe}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[Code]
function WebView2Missing: Boolean;
var
  v: string;
begin
  { Evergreen runtime registers its version (pv) under this client GUID. }
  Result := not (
    RegQueryStringValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', v)
    or RegQueryStringValue(HKCU, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', v)
  );
end;
