#!/usr/bin/env python3
"""Generate the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Draws a Vice City neon-sunset scene with PIL, pastes make.fun's ghost
mascot driving a convertible, and captions it. Output: 1200x675 PNG.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
random.seed(6)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz):
    return ImageFont.truetype(BOLD, sz)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")

# --- sky gradient: deep purple -> magenta -> orange ---
stops = [(0.0, (26, 11, 46)), (0.45, (120, 20, 90)), (0.75, (255, 46, 136)), (1.0, (255, 154, 61))]
horizon = 470
for y in range(horizon):
    t = y / horizon
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            col = lerp(c0, c1, (t - t0) / (t1 - t0))
            break
    d.line([(0, y), (W, y)], fill=col)

# --- sun with glow ---
sx, sy, sr = 600, 330, 95
for r, alpha in [(190, 28), (155, 45), (122, 70)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 211, 25, alpha))
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 211, 25, 255))
# sun slats (retro)
for i, yy in enumerate(range(sy + 10, sy + sr, 15)):
    half = int(math.sqrt(max(sr * sr - (yy - sy) ** 2, 0)))
    d.rectangle([sx - half, yy, sx + half, yy + 6], fill=(255, 154, 61, 255))

# --- skyline silhouettes ---
d.rectangle([0, horizon - 130, W, horizon], fill=(20, 8, 43, 255))
x = -20
while x < W:
    bw = random.randint(55, 130)
    bh = random.randint(60, 130)
    top = horizon - bh
    d.rectangle([x, top, x + bw, horizon], fill=(16, 6, 36, 255))
    # antenna
    if random.random() < 0.4:
        d.line([(x + bw // 2, top), (x + bw // 2, top - 26)], fill=(16, 6, 36, 255), width=3)
        d.ellipse([x + bw // 2 - 3, top - 32, x + bw // 2 + 3, top - 26], fill=(255, 94, 120, 255))
    # lit windows
    for wy in range(top + 12, horizon - 8, 22):
        for wx in range(x + 8, x + bw - 8, 18):
            if random.random() < 0.28:
                col = random.choice([(255, 211, 25), (255, 94, 120), (120, 220, 255)])
                d.rectangle([wx, wy, wx + 7, wy + 10], fill=col + (255,))
    x += bw + random.randint(2, 14)

# --- ground: dark road with neon reflections ---
d.rectangle([0, horizon, W, H], fill=(13, 6, 24, 255))
for _ in range(90):
    rx = random.randint(0, W)
    rw = random.randint(2, 6)
    rh = random.randint(15, 70)
    col = random.choice([(255, 46, 136), (255, 154, 61), (0, 229, 255), (255, 211, 25)])
    d.rectangle([rx, horizon + 4, rx + rw, horizon + 4 + rh], fill=col + (random.randint(40, 110),))

# --- palm trees ---
def palm(px, py, s, flip=1):
    # trunk: gentle curve
    pts = []
    for i in range(11):
        t = i / 10
        pts.append((px + flip * t * t * 36 * s, py - t * 140 * s))
    d.line(pts, fill=(10, 4, 22, 255), width=int(9 * s))
    tx, ty = pts[-1]
    # fronds: drooping parabolas fanning out from the crown
    for k, ang in enumerate([-150, -110, -70, -30, 10, 50]):
        rad = math.radians(ang)
        length = 62 * s
        fx = tx + flip * math.cos(rad) * length
        fy = ty + math.sin(rad) * length * 0.55 + 26 * s
        mx = tx + flip * math.cos(rad) * length * 0.55
        my = ty + math.sin(rad) * length * 0.18 - 14 * s
        pts2 = []
        for i in range(9):
            t = i / 8
            # quadratic bezier through (tx,ty), (mx,my), (fx,fy)
            bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t * t * fx
            by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t * t * fy
            pts2.append((bx, by))
        d.line(pts2, fill=(10, 4, 22, 255), width=int(5 * s))

palm(90, 560, 1.15, flip=1)
palm(1120, 575, 1.0, flip=-1)
palm(210, 600, 0.7, flip=-1)

# --- convertible with the make.fun ghost driving ---
car_x, car_y = 430, 478
# neon underglow
d.ellipse([car_x - 20, car_y + 62, car_x + 380, car_y + 92], fill=(255, 46, 136, 70))
# car body
d.rounded_rectangle([car_x, car_y, car_x + 360, car_y + 62], radius=22, fill=(24, 8, 46, 255))
d.polygon([(car_x + 40, car_y), (car_x + 110, car_y - 34), (car_x + 250, car_y - 34), (car_x + 300, car_y)],
          fill=(24, 8, 46, 255))
d.polygon([(car_x + 120, car_y - 28), (car_x + 240, car_y - 28), (car_x + 235, car_y - 4), (car_x + 125, car_y - 4)],
          fill=(120, 220, 255, 255))
# wheels
for wx in (car_x + 55, car_x + 265):
    d.ellipse([wx, car_y + 38, wx + 56, car_y + 94], fill=(5, 2, 10, 255))
    d.ellipse([wx + 16, car_y + 54, wx + 40, car_y + 78], fill=(200, 200, 210, 255))

ghost = Image.open("makefun-mark-1024.png").convert("RGBA")
ghost = ghost.resize((150, 150), Image.LANCZOS).rotate(-6, resample=Image.BICUBIC, expand=True)
img.paste(ghost, (car_x + 150, car_y - 118), ghost)

# --- captions ---
def text_block(lines, y, size, stroke=7):
    f = font(size)
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f, stroke_width=stroke)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text(((W - tw) / 2, y), line, font=f, fill=(255, 255, 255, 255),
               stroke_width=stroke, stroke_fill=(10, 4, 22, 255))
        y += th + 6
    return y

text_block(["WAITED 13 YEARS", "FOR GTA 6"], 28, 88, stroke=8)
text_block(["MY AGENT GOT BORED AND", "STARTED EARNING ON MAKE.FUN"], 588, 38, stroke=5)

img.save("meme.png")
print("saved meme.png", img.size)
