# Backlog

Next features to build, in priority order. Tomorrow starts here.

## 1. Lock a config to constrain the set
- Add a **lock toggle** per garment dropdown (shirt, trouser, belt, shoe, dial, strap).
- When a field is **locked** to a value:
  - every **other** dropdown only offers values that occur in some outfit having the locked value
    (options are computed from the locked subset);
  - **Prev / Next** navigate only within that subset, and the counter reflects the subset size.
- For now, **lock is limited to 1 field at a time**. Multi-field locking may come later.
- Implementation note: today's `onPick` does nearest-match *within the pool*. A lock makes a field
  a **hard filter**, so add a lock layer to `pool()` (in `templates/index.html`) and recompute each
  dropdown's options from the locked subset.

## 2. Wishlist
- Add a way to mark an outfit as **wishlisted** (toggle on the current outfit).

## 3. Available in wardrobe
- Add a way to mark an outfit as **available / owned**.

## 4. Inventory
- Track which outfits are marked available.
- Derive an **individual inventory of items** — the constituent garments across available outfits —
  and display it at the **top of the page**.

## Open questions (decide before building)
- **Persistence.** Wishlist / available flags and the inventory must survive restarts. The desktop
  app currently reads a read-only `viewer_data.json` and has no database. Options:
  - browser `localStorage` in the WebView — simplest, per-install, no backend change;
  - a writable JSON under `%APPDATA%\Wardrobe Lookbook\` — survives app updates, readable outside;
  - a small embedded store (e.g. SQLite) — most structured.
  Choice affects `app.py` / `desktop.py`.
- **"Individual inventory of items."** Confirm this means unique garments (e.g. "White shirt",
  "Navy trouser") decomposed from the available outfits and de-duplicated — and what each item row
  should show (name, swatch, count, which outfits use it?).
- **UI placement** of the wishlist / available toggles (caption bar vs. new controls), and how the
  top-of-page inventory coexists with the fixed no-scroll layout.
