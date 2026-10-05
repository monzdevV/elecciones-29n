"""Genera src/og.png (1200x630) con el cartograma de escaños."""
import json, importlib.util
from PIL import Image, ImageDraw, ImageFont
spec = importlib.util.spec_from_file_location("b", "build.py"); 
src = open("build.py", encoding="utf-8").read()
CARTO = {}
exec(src[src.index("CARTO = {"):src.index("SLUG_ALIASES")], {}, locals_ := {}); CARTO = locals_["CARTO"]
d = json.load(open("data/provincias.json", encoding="utf-8"))
F = "C:/Windows/Fonts/"
big = ImageFont.truetype(F + "ARIALNB.TTF", 84); mid = ImageFont.truetype(F + "ARIALN.TTF", 32); sm = ImageFont.truetype(F + "ARIALNB.TTF", 15)
INK, PAPER, SEPIA = (28, 36, 51), (247, 248, 246), (201, 138, 60)
SEQ = [(246, 236, 220), (236, 214, 178), (222, 186, 130), (200, 150, 85), (165, 112, 55), (128, 82, 40)]
im = Image.new("RGB", (1200, 630), INK); dr = ImageDraw.Draw(im)
dr.text((64, 70), "Elecciones", font=big, fill=PAPER)
dr.text((64, 160), "generales", font=big, fill=PAPER)
dr.text((64, 250), "29 de noviembre", font=big, fill=SEPIA)
dr.text((64, 340), "de 2026", font=big, fill=PAPER)
dr.text((64, 470), "Mesa electoral · voto por correo · escaños", font=mid, fill=(200, 205, 215))
dr.text((64, 512), "por provincia · simulador D'Hondt", font=mid, fill=(200, 205, 215))
dr.text((64, 572), "ELECCIONES29N", font=sm, fill=SEPIA)
q = lambda n: 0 if n <= 2 else 1 if n == 3 else 2 if n == 4 else 3 if n <= 6 else 4 if n <= 11 else 5
x0, y0, s, g = 640, 70, 50, 4
for p in d["provincias"]:
    r, c, code = CARTO[p["slug"]]
    n = p.get("escanos2026") or p["escanos2023"]
    x, y = x0 + (c - 1) * (s + g), y0 + (r - 1) * (s + g)
    col = SEQ[q(n)]
    dr.rectangle([x, y, x + s, y + s], fill=col)
    fg = PAPER if q(n) >= 4 else INK
    dr.text((x + 4, y + 3), code, font=sm, fill=fg)
    t = str(n); w = dr.textlength(t, font=sm)
    dr.text((x + s - w - 4, y + s - 19), t, font=sm, fill=fg)
im.save("src/og.png", optimize=True)
print("og ok")
