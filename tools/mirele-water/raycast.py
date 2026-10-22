"""Ray-cast the LAND heightfield from the save's camera and render it, to validate
the camera model against the screenshot."""
import sys, math, glob, os
import numpy as np
from PIL import Image
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from waterscan import scan_plugin

def cellfid(x, y):
    return 0x009B4F + (-13 - y) * 0x21 + (-x)

CELLS = {}
for x in range(-12, 4):
    for y in range(-24, -8):
        CELLS[(x, y)] = cellfid(x, y) + 0x1000

syn = glob.glob(r'C:\1. AUTHORIA\mods\*\Authoria - Output - Synthesis Worldspace.esp')[0]
want = set(CELLS.values())
Hs = scan_plugin(syn, want)
Hv = scan_plugin(r'C:\1. AUTHORIA\Stock Game\Data\Skyrim.esm', want)
print('LAND from synthesis: %d, vanilla: %d, cells wanted %d' % (len(Hs), len(Hv), len(want)))

# build one big array: index by (gx, gy) global vertex
XS = sorted({k[0] for k in CELLS}); YS = sorted({k[1] for k in CELLS})
NX = len(XS) * 32 + 1; NY = len(YS) * 32 + 1
G = np.full((NX, NY), np.nan)
for (cx, cy), lid in CELLS.items():
    Hm = Hs.get(lid) or Hv.get(lid)
    if Hm is None:
        continue
    ox = (cx - XS[0]) * 32; oy = (cy - YS[0]) * 32
    for vy in range(33):
        for vx in range(33):
            G[ox + vx, oy + vy] = Hm[(vx, vy)]
X0 = XS[0] * 4096.0; Y0 = YS[0] * 4096.0
print('grid %dx%d covering x %.0f..%.0f y %.0f..%.0f, nan frac %.3f'
      % (NX, NY, X0, X0 + (NX - 1) * 128, Y0, Y0 + (NY - 1) * 128, np.isnan(G).mean()))

def terrain(wx, wy):
    fx = (wx - X0) / 128.0; fy = (wy - Y0) / 128.0
    i = int(fx); j = int(fy)
    if i < 0 or j < 0 or i >= NX - 1 or j >= NY - 1:
        return np.nan
    tx = fx - i; ty = fy - j
    a = G[i, j]; b = G[i+1, j]; c = G[i, j+1]; d = G[i+1, j+1]
    return (a*(1-tx)+b*tx)*(1-ty) + (c*(1-tx)+d*tx)*ty

def render(pitchdeg, zoff, back, out, w=480, h=270, hfov=85.0):
    th = math.radians(295.317); p = math.radians(pitchdeg)
    f = np.array([math.sin(th)*math.cos(p), math.cos(th)*math.cos(p), -math.sin(p)])
    r = np.array([math.cos(th), -math.sin(th), 0.0])
    u = np.cross(r, f); u /= np.linalg.norm(u)
    C = np.array([1139.57, -59578.77, 881.22 + zoff]) - f*back
    fpx = (w/2)/math.tan(math.radians(hfov/2))
    img = np.zeros((h, w, 3), np.uint8)
    for sy in range(h):
        for sx in range(w):
            d = f + (sx - w/2 + .5)/fpx*r + (h/2 - sy - .5)/fpx*u
            d = d/np.linalg.norm(d)
            t = 40.0; hit = None
            while t < 30000:
                P = C + t*d
                g = terrain(P[0], P[1])
                if np.isnan(g):
                    t *= 1.05; continue
                if P[2] <= g:
                    hit = (t, P, g); break
                t += max(24.0, t*0.01)
            if hit is None:
                img[sy, sx] = (150, 180, 220)   # sky
            else:
                t, P, g = hit
                if g < 600.0:
                    img[sy, sx] = (20, 40, 160)   # under water plane -> water
                else:
                    v = int(max(0, min(255, 255 - t/60)))
                    img[sy, sx] = (v//2 + 40, v//2 + 60, 40)
    Image.fromarray(img).resize((w*2, h*2), Image.NEAREST).save(out)
    print('wrote', out)

if __name__ == '__main__':
    sp = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\6ee3b2d8-54bc-47e2-981c-5bda94dbf0ea\scratchpad'
    render(9.345, 144, 148, sp + r'\rc_p9.png')
