#!/usr/bin/env python3
"""
Gera o logo/mascote do Guto (guto-mascote.png) a partir da arte original:
  1. remove o fundo branco externo (flood-fill a partir das bordas; preserva
     brancos internos como dentes/papel da máquina);
  2. recorta num círculo focando rosto + máquina de escrever;
  3. exporta PNG RGBA 320x320 com alpha circular.

O aro (borda) e a sombra do "emblema" ficam no CSS (.brand-ico / .guto-ico
em index.html), não na imagem.

Requisitos: Pillow.  (criar venv:  python3 -m venv venv && venv/bin/pip install pillow)

Uso:
  python scripts/logo_circle.py ORIGEM.png guto-mascote.png [cy_frac] [r_frac]

Parâmetros usados na versão atual (arte IMG_4855.PNG = senhor c/ máquina):
  cy_frac = 0.42   # centro vertical do círculo (fração da altura) — menor sobe o recorte
  r_frac  = 0.48   # raio (fração; limitado a metade da largura)
"""
from PIL import Image, ImageDraw, ImageChops
from collections import deque
import sys

src, dst = sys.argv[1], sys.argv[2]
cyf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.42
rf = float(sys.argv[4]) if len(sys.argv) > 4 else 0.48

im = Image.open(src).convert("RGBA")
W, H = im.size
px = im.load()
TOL = 36  # tolerância p/ considerar um pixel "branco"


def white(p):
    return p[0] >= 255 - TOL and p[1] >= 255 - TOL and p[2] >= 255 - TOL


# 1) flood-fill do branco externo (conectado às bordas) -> transparente
vis = bytearray(W * H)
dq = deque()
for x in range(W):
    dq.append((x, 0)); dq.append((x, H - 1))
for y in range(H):
    dq.append((0, y)); dq.append((W - 1, y))
while dq:
    x, y = dq.popleft()
    if x < 0 or y < 0 or x >= W or y >= H:
        continue
    i = y * W + x
    if vis[i]:
        continue
    vis[i] = 1
    p = px[x, y]
    if not white(p):
        continue
    px[x, y] = (p[0], p[1], p[2], 0)
    dq.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

# 2) círculo focando rosto + máquina
cx = W / 2
cy = H * cyf
r = min(W / 2, H * rf)
box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
crop = im.crop(box)
s = crop.size[0]
mask = Image.new("L", (s, s), 0)
ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
crop.putalpha(ImageChops.multiply(crop.split()[3], mask))

# 3) exporta
crop = crop.resize((320, 320), Image.LANCZOS)
crop.save(dst)
print("ok", box, "->", crop.size)
