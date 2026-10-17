"""Build the self-contained assets for the desktop app.

Reads wardrobe_mongo.json, builds the 2:3 web JPEGs in wardrobe_web/ (same as the
web app), and writes viewer_data.json -- a flat list of the 154 outfits (colors,
shoe_type, ambient color, image URL) that the desktop build reads instead of MongoDB.

Usage:
    python build_assets.py
"""
import json
import os

import img_utils

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "wardrobe_mongo.json")
IMAGE_DIR = os.path.join(HERE, "wardrobe_images")
WEB_DIR = os.path.join(HERE, "wardrobe_web")
OUT_FILE = os.path.join(HERE, "viewer_data.json")

# Flat fields the viewer's dropdowns / breakdown read off each outfit.
VIEWER_KEYS = [
    "shirt_color", "shirt_hex",
    # Optional shirt pattern: name ("Solid"/"Micro Check"/"Stripe"/...) + accent colour.
    # Absent on solid shirts; the viewer treats a missing/"Solid" pattern as a plain colour.
    "shirt_pattern", "shirt_accent_color", "shirt_accent_hex",
    "trouser_color", "trouser_hex",
    "belt_color", "belt_hex", "shoe_color", "shoe_hex", "shoe_type",
    "dial_color", "dial_hex", "strap_color", "strap_hex",
]

CATEGORY_ORDER = {"Locked": 0, "Potential": 1, "Doubtful": 2}


def build(verbose=True):
    """Build web images + return the flat outfit list (sorted for display)."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        combinations = json.load(f)

    os.makedirs(WEB_DIR, exist_ok=True)
    outfits, missing = [], []
    for combo in combinations:
        combo_id = combo["combo_id"]
        j = combo["input_json"]
        src = os.path.join(IMAGE_DIR, f"{combo_id}.png")
        if not os.path.exists(src):
            missing.append(combo_id)
            continue

        jpg_name = f"{combo_id}.jpg"
        amb_hex = img_utils.build_web_image(src, os.path.join(WEB_DIR, jpg_name))

        rec = {
            "combo_id": combo_id,
            "category": j.get("category"),
            "amb_hex": amb_hex,
            "img": f"/images/{jpg_name}",
        }
        for k in VIEWER_KEYS:
            rec[k] = j.get(k)
        outfits.append(rec)

    outfits.sort(key=lambda o: (CATEGORY_ORDER.get(o["category"], 99), o["combo_id"]))
    if verbose and missing:
        print(f"WARNING: {len(missing)} combos have no image, skipped: {missing}")
    return outfits


def main():
    outfits = build()
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(outfits, f, ensure_ascii=False)
    print(f"Wrote {len(outfits)} outfits to viewer_data.json; web images in wardrobe_web/.")


if __name__ == "__main__":
    main()
