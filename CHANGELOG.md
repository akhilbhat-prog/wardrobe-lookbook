# Changelog

## 2026-10-16 — Initial release

First working version: the Wardrobe Lookbook as an installable Windows desktop app.

### Viewer (editorial single-outfit configurator)
- Fixed full-viewport split: controls left (~37%), image right — no page scroll.
- Per-garment colour **dropdowns** (shirt, trouser, belt, shoe, watch dial, strap) that double as
  the colour breakdown (swatch + name + hex per row; shoe row shows `shoe_type`). Changing a
  dropdown jumps to the **nearest matching real outfit**.
- **Category** filter (Locked / Potential / Doubtful), **search** (id or colour), **prev/next**
  with counter and ←/→ keys.
- Image on a **backdrop-derived colour pool**; near-crisp 0.5% edge; **Fit / Fill** toggle
  (framed vs full-bleed magazine), remembered per viewer.
- All photos normalized to **2:3** so the frame is a consistent size.
- Light + dark themes; Bodoni Moda + Archivo (bundled for offline use).

### Data / app
- All **154 outfits** served from `viewer_data.json` (built from `wardrobe_mongo.json` +
  `wardrobe_images/` by `build_assets.py`). No database required.
- Flask app (`app.py`) serves the viewer, the images, and `/api/combinations`.

### Desktop packaging
- `desktop.py` — native window via pywebview/WebView2 (no browser), clean shutdown.
- PyInstaller build (`wardrobe.spec`) → onedir app; Inno Setup installer (`installer.iss`) with
  Start-menu shortcut, uninstall, and WebView2 runtime provisioning. Fully offline + self-contained.

### Automation
- `preview.ps1` — browser/native preview (no build).
- `build.ps1` — one command → fresh installer (`-Version` bump, `-Fonts` refresh).
- `deploy.ps1` — build + update the installed app in place.

### Housekeeping
- Removed MongoDB (code, packages, loader) and the old SQLite/junk; app reads only
  `viewer_data.json`.
- Initialized git; pushed a code-only snapshot to a public GitHub repo.
