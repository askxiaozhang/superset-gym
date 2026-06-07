#!/usr/bin/env python3
"""Generate the home-screen app icon set for the workout timer."""
import math
from PIL import Image, ImageDraw

SS = 4  # supersample factor for crisp edges

BG_TOP = (18, 21, 27)     # #12151b
BG_BOT = (10, 11, 14)     # #0a0b0e
CORAL  = (255, 111, 97)   # #ff6f61
WHITE  = (243, 245, 249)  # #f3f5f9

def vgradient(size, top, bot):
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        r = round(top[0] + (bot[0]-top[0])*t)
        g = round(top[1] + (bot[1]-top[1])*t)
        b = round(top[2] + (bot[2]-top[2])*t)
        for x in range(size):
            px[x, y] = (r, g, b)
    return img

def draw_master(scale=1.0):
    """Render a 1024px master icon. scale shrinks the artwork (for maskable safe zone)."""
    N = 1024 * SS
    img = vgradient(N, BG_TOP, BG_BOT).convert("RGBA")
    d = ImageDraw.Draw(img)
    c = N / 2
    R = (300 * SS) * scale          # ring radius
    w = (64 * SS) * scale           # ring stroke width
    bbox = [c-R, c-R, c+R, c+R]
    # ring with a gap at the top (countdown style), endpoints get round caps
    start, end = 295, 245           # PIL deg, clockwise from 3 o'clock; gap centered at top
    d.arc(bbox, start, end, fill=CORAL, width=round(w))
    for a in (start, end):
        ar = math.radians(a)
        px_, py_ = c + R*math.cos(ar), c + R*math.sin(ar)
        rr = w/2
        d.ellipse([px_-rr, py_-rr, px_+rr, py_+rr], fill=CORAL)

    # centered dumbbell, white
    s = SS * scale
    def rrect(x0, y0, x1, y1, rad, fill):
        d.rounded_rectangle([c+x0*s, c+y0*s, c+x1*s, c+y1*s], radius=rad*s, fill=fill)
    # handle bar
    rrect(-78, -19, 78, 19, 14, WHITE)
    # inner plates (big)
    rrect(-100, -62, -58, 62, 20, WHITE)
    rrect(58, -62, 100, 62, 20, WHITE)
    # outer plates (small)
    rrect(-128, -42, -104, 42, 14, WHITE)
    rrect(104, -42, 128, 42, 14, WHITE)

    return img.resize((1024, 1024), Image.LANCZOS)

std = draw_master(1.0)
msk = draw_master(0.72)   # maskable: artwork inside the 80% safe zone

def save(img, size, name):
    img.resize((size, size), Image.LANCZOS).convert("RGB").save(name, "PNG")

save(std, 180, "apple-touch-icon.png")
save(std, 192, "icon-192.png")
save(std, 512, "icon-512.png")
save(msk, 512, "icon-512-maskable.png")
save(std, 32,  "favicon-32.png")
print("icons written")
