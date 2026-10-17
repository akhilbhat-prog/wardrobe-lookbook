# Wardrobe Lookbook

An editorial, magazine-style viewer for a 154-outfit menswear wardrobe. Browse one outfit at a
time: pick a colour for any garment (shirt, trouser, belt, shoe, watch dial/strap) and it jumps to
the nearest matching real outfit, with a backdrop-tinted image pool, a **Fit / Fill** image toggle,
category filter, search, keyboard navigation, and light/dark themes.

You can also **lock** one garment to constrain the rest, build a **wardrobe** and a **wishlist** at
the garment level (per-row ♡/✓, or bulk-add a whole outfit), and watch a live **inventory** count
strip at the top (with a Wardrobe/Wishlist toggle and a display-font switcher). The wardrobe and
wishlist persist to `state.json` under `%APPDATA%\Wardrobe Lookbook\` (served by `GET`/`POST
/api/state`), so they survive restarts and app reinstalls.

It ships two ways from the same code:

- **Web / dev:** a Flask app you open in a browser.
- **Desktop:** a self-contained Windows app (pywebview + WebView2) packaged into an installer — no
  Python, MongoDB, or internet needed on the target machine.

## Repo layout

| Path | What |
|---|---|
| `app.py` | Flask app (serves the viewer + images; reads `viewer_data.json`) |
| `desktop.py` | Native-window launcher (pywebview) wrapping the Flask app |
| `templates/index.html` | The viewer UI (HTML/CSS/JS) |
| `static/fonts/` | Bundled Bodoni Moda + Archivo (offline fonts) |
| `img_utils.py` | 2:3 image normalization + backdrop ambient-colour helpers |
| `build_assets.py` | Builds `wardrobe_web/` + `viewer_data.json` from `wardrobe_images/` |
| `download_fonts.py` / `make_icon.py` | One-off generators for fonts / app icon |
| `wardrobe.spec` | PyInstaller build config |
| `installer.iss` | Inno Setup installer script |
| `preview.ps1` / `build.ps1` / `deploy.ps1` | Dev + packaging automation (see below) |
| `wardrobe_mongo.json`, `Wardrobe Combinations.xlsx` | Source outfit data |
| `*_colab.ipynb` | Colab notebooks used to generate the outfit images |

> **Not in the repo (by design):** `wardrobe_images/` (≈258MB source PNGs), the `.venv`, and all
> generated/build output (`wardrobe_web/`, `viewer_data.json`, `dist/`, `build/`,
> `installer_output/`, `assets/app.ico`, `vendor/*.exe`). You need `wardrobe_images/` to run
> `build_assets.py`; supply it separately.

## Prerequisites

- **Python 3.12** (Windows)
- **Inno Setup 6** — only to build the installer (`winget install JRSoftware.InnoSetup`)
- **WebView2 runtime** — preinstalled on current Windows 10/11; the installer provisions it otherwise

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe download_fonts.py      # fetch bundled fonts (if static/fonts is empty)
.\.venv\Scripts\python.exe make_icon.py           # generate assets/app.ico
.\.venv\Scripts\python.exe build_assets.py        # build wardrobe_web/ + viewer_data.json (needs wardrobe_images/)
```

The installer also bundles the WebView2 bootstrapper at `vendor/MicrosoftEdgeWebview2Setup.exe` —
download it from <https://go.microsoft.com/fwlink/p/?LinkId=2124703> if missing.

## Day-to-day workflow

```powershell
.\preview.ps1            # preview in your browser at http://localhost:5000 (live reload on edit)
.\preview.ps1 -Native    # preview in the native desktop window
.\preview.ps1 -Rebuild   # regenerate data/images first (after changing outfits or images)

.\build.ps1              # one command -> installer_output\WardrobeLookbook-Setup.exe
.\build.ps1 -Version 1.1.0   # also bump the installer version

.\deploy.ps1             # build, then update the installed app in place (one UAC prompt)
```

Edit → `preview` → `deploy`. Preview never touches the installed app; only `deploy` does.
