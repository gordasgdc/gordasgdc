#!/usr/bin/env python3
"""Generează bannerele de profil (light/dark) în assets/. Paleta Cinema; font Inter (OFL).
Rulare: python3 -I tools/make_banner.py [director_preview_extern]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
W, H, S = 1600, 400, 2
F = os.path.expanduser("~/Library/Fonts/")
THEMES = {
  "dark":  dict(bg="#141B1D", fg="#EEECE5", sub="#A6B3B1", acc="#93C4BF", line="#2A3538"),
  "light": dict(bg="#EEECE5", fg="#141B1D", sub="#4F5E5C", acc="#2B6E68", line="#C9CCC4"),
}
def font(n, px): return ImageFont.truetype(F + n, px * S)
def make(name, c):
    im = Image.new("RGB", (W*S, H*S), c["bg"]); d = ImageDraw.Draw(im)
    m = 72
    # cadru de film: două bare orizontale subțiri (letterbox 2.39:1) și marcaje de colț
    for y in (56, H-56): d.line([(m*S, y*S), ((W-m)*S, y*S)], fill=c["line"], width=2*S)
    for x in (m, W-m):
        for y in (56, H-56): d.ellipse([(x-4)*S, (y-4)*S, (x+4)*S, (y+4)*S], fill=c["acc"])
    # titlu
    d.text((m*S, 118*S), "Cristi Gordas", font=font("Inter-Bold.otf", 92), fill=c["fg"])
    d.text((m*S+4, 232*S), "Colorist  ·  Filmmaker  ·  Tool builder", font=font("Inter-ExtraLight.otf", 34), fill=c["sub"])
    d.text((m*S+4, 292*S), "GDC  ·  gordas.dev", font=font("Inter-Bold.otf", 22), fill=c["acc"])
    # rampă de gri (9 trepte, ca o scară de expunere) în dreapta
    x0, y0, w, h = 1130, 118, 40, 160
    for i in range(9):
        t = i/8
        g = int(255*(t**(1/1.0))) if name == "dark" else int(255*t)
        shade = (int(20+ (238-20)*t), int(27+(236-27)*t), int(29+(229-29)*t))
        d.rectangle([(x0+i*w)*S, y0*S, (x0+(i+1)*w-4)*S, (y0+h)*S], fill=shade, outline=c["line"], width=S)
    d.rectangle([(x0+4*w)*S, (y0+h+14)*S, (x0+5*w-4)*S, (y0+h+20)*S], fill=c["acc"])  # marcaj gri 18%
    im = im.resize((W, H), Image.LANCZOS)
    return im
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
for n, c in THEMES.items():
    im = make(n, c); p = os.path.join(out, f"banner-{n}.png"); im.save(p, optimize=True); print(p, os.path.getsize(p))
    if len(sys.argv) > 1: im.save(os.path.join(sys.argv[1], f"banner-{n}.png"))
