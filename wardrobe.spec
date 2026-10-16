# -*- mode: python ; coding: utf-8 -*-
r"""PyInstaller spec for the Wardrobe Lookbook desktop app.

Build:  .\.venv\Scripts\pyinstaller.exe wardrobe.spec
Output: dist/WardrobeLookbook/WardrobeLookbook.exe  (onedir, windowed)
"""
from PyInstaller.utils.hooks import collect_all

datas = [
    ("templates", "templates"),
    ("static", "static"),
    ("wardrobe_web", "wardrobe_web"),
    ("viewer_data.json", "."),
]
binaries = []
hiddenimports = ["clr"]  # pythonnet, used by pywebview's Windows (WebView2) backend

# Bundle pywebview's platform backends + its native WebView2 support files.
for pkg in ("webview",):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ["desktop.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    # Not used at runtime by the desktop build (data comes from viewer_data.json):
    excludes=["pymongo", "bson", "numpy", "PIL"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="WardrobeLookbook",
    console=False,          # windowed app, no console
    icon="assets/app.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="WardrobeLookbook",
)
