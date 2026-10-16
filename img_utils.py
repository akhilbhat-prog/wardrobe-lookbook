"""Offline image helpers for the wardrobe viewer.

Normalizes each source photo to a 2:3 portrait (so every image fills the viewer's
fixed 2:3 frame at a consistent size) and derives an ambient backdrop color used to
tint the pool behind the figure. Used by load_mongo.py; no request-time cost.
"""
import numpy as np
from PIL import Image


def crop_to_23(im):
    """Normalize to a 2:3 portrait. When taller/narrower than 2:3, trim height biased
    toward the top (remove headroom, keep the shoes). When wider, trim width centered."""
    w, h = im.size
    target = 2 / 3  # width / height
    if abs(w / h - target) < 1e-3:
        return im
    if w / h < target:  # too tall -> crop height, bias the cut to the top
        new_h = round(w / target)
        top = round((h - new_h) * 0.6)
        return im.crop((0, top, w, top + new_h))
    new_w = round(h * target)  # too wide -> crop width centered
    left = (w - new_w) // 2
    return im.crop((left, 0, left + new_w, h))


def ambient_hex(im):
    """Backdrop-derived surround color: sample the clean scene behind the figure (top band
    + left/right columns over the upper 70%, away from the floor), with a gentle saturation
    lift so the pool reads as a hue rather than flat grey."""
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    h, w = arr.shape[:2]
    t = max(2, int(min(h, w) * 0.07))
    up = int(h * 0.70)
    patches = [
        arr[:t, :].reshape(-1, 3),
        arr[:up, :t].reshape(-1, 3),
        arr[:up, -t:].reshape(-1, 3),
    ]
    amb = np.concatenate(patches).mean(axis=0)
    g = amb.mean()
    amb = np.clip(g + (amb - g) * 1.1, 0, 255)
    return "#%02X%02X%02X" % tuple(int(round(c)) for c in amb)


def build_web_image(src_path, dst_path, max_w=1000, quality=86):
    """Crop to 2:3, downscale, save a web JPEG, and return its ambient hex."""
    im = Image.open(src_path).convert("RGB")
    im = crop_to_23(im)
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    amb = ambient_hex(im)
    im.save(dst_path, format="JPEG", quality=quality)
    return amb
