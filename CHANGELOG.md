# Changelog

## 2026-10-17 — Outfit-level pills + an Alternatives filter

- The **Wishlist** and **Owned** filter pills are now **outfit-level**: an outfit counts as owned /
  wished only if you added *that outfit* (its `combo_id` is recorded on every one of its garments),
  not merely because all its garments happen to be present. This stops unrelated outfits flooding
  **Owned** once you own enough individual pieces.
- New **Alternatives** pill: outfits you didn't add but can fully assemble from garments you already
  own (e.g. pieces from two added outfits happen to form a third). Viewing one shows an
  *"Alternative"* tag in the caption with **✓ In wardrobe** off; clicking ✓ claims it as Owned,
  clicking again returns it to Alternatives (the shared garments stay, held by the other outfits).
- Owned / Alternatives / Wishlist are mutually exclusive. All three are derived from the existing
  garment-holder data — no persistence or `state.json` change.

## 2026-10-17 — Shared garments survive removing one outfit

- Garments are now **reference-counted by their holders** (the outfits that contain them, plus a
  `manual` sentinel for a per-row add). Removing an outfit drops only the garments it was the *last*
  holder of, so if two added outfits share a garment and you remove one, the garment — and the other
  outfit — stay whole (still listed under **Owned**/**Wishlist**, still counted in the inventory).
  Previously removing one outfit stripped shared garments and left the other as a broken subset.
- A per-row **♡/✓ turned off** still removes that garment outright (you're asserting you don't
  have/want it), even if an added outfit contained it — that outfit then reads as partially owned.
- `state.json` now stores each set as `{ "shirt|White": ["L-001","L-002"], ... }` (garment →
  holders). A legacy flat-array file is still read (each key treated as a single `manual` holder).

## 2026-10-17 — Lock, and a garment-level wardrobe / wishlist + inventory

- **Lock** a single garment (padlock per dropdown row). Locking makes that field a hard filter:
  every other dropdown only offers values co-occurring with the locked one, and Prev/Next + the
  counter navigate only the locked subset. The locked slot stays changeable (re-aims the lock).
  One field at a time; session-only.
- **Garment-level wardrobe & wishlist.** The individual garment *(slot, colour[, shoe type])* is
  the tracked unit. Per-row **♡ / ✓** icons add the shown garment to the wishlist / wardrobe, and
  the caption **♡ Wishlist** / **✓ In wardrobe** toggles bulk-add a whole outfit's garments.
  Rules: owning a garment removes it from the wishlist (wardrobe wins); wishlisting an outfit skips
  garments you already own; adding garments de-duplicates. Outfit **Wishlist / Owned** filter chips
  (with counts) are derived from whether all an outfit's garments are in a set.
- **Inventory** strip at the top: always visible, compact, count-only tiles ("Shirts · 6") per
  garment type separated by dotted rules, with a **Wardrobe / Wishlist** view toggle and an **Aa**
  font switcher (Bodoni, Playfair, Cormorant, DM Serif Display, Pinyon Script — bundled offline).
- The wardrobe & wishlist persist to `%APPDATA%\Wardrobe Lookbook\state.json` (garment-key arrays)
  via `GET`/`POST /api/state` (atomic writes). The read-only `viewer_data.json` pipeline is
  unchanged.

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
