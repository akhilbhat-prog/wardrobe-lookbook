"""Generate assets/app.ico -- a simple editorial 'W' mark for the desktop app."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "app.ico")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

SIZE = 256
PAPER = (244, 243, 239)
OXBLOOD = (110, 36, 51)


def font(px):
    for name in ("georgiab.ttf", "georgia.ttf", "timesbd.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


img = Image.new("RGBA", (SIZE, SIZE), OXBLOOD + (255,))
d = ImageDraw.Draw(img)
# thin paper keyline border
d.rectangle([8, 8, SIZE - 9, SIZE - 9], outline=PAPER + (255,), width=3)
f = font(190)
text = "W"
box = d.textbbox((0, 0), text, font=f)
w, h = box[2] - box[0], box[3] - box[1]
d.text(((SIZE - w) / 2 - box[0], (SIZE - h) / 2 - box[1]), text, font=f, fill=PAPER + (255,))

img.save(OUT, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("wrote", OUT)
