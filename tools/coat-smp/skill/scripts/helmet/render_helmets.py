"""render_helmets: each built helmet (its first men's variant) coloured by what moves it - the head grey, each flap chain its own hue
(the lining riding it the same), the cheek guards magenta, the hidden colliders faint - front / side / back / left. Writes
WORK/renders/helmets_<name>.png. usage: render_helmets.py <designs.py> [helmet ...]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import build_helmet_rig as W
from smpkit import checks as K
C = W.C


def hue(k, n):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb((k / max(n, 1)) % 1.0, 0.75, 0.95); return (int(b * 255), int(g * 255), int(r * 255))


def main(dp, helmets):
    import cv2
    W.use_designs(dp); rep = json.load(open(W.WORK + 'helmets_report.json')); os.makedirs(W.WORK + 'renders/', exist_ok=True)
    for h in helmets or list(rep):
        H = W.HELMETS[h]; p = H['prefix']; v = next(v for v in H['variants'] if v.lstrip('_').startswith('m') and not v.endswith('_0'))
        r = rep[h]['variants'][v]; n, T = C.load(r['out']); C.to_world(T); G = []
        for t in T:
            if t.name.startswith(p + ' '):
                G.append((t.pos, t.tris, None, None, (70, 70, 90))); continue
            dom = []
            for w in t.w:
                b = max(w, key=w.get)
                dom.append(b)
            col = np.full((len(t.pos), 3), 150, int)
            for i, b in enumerate(dom):
                if b.startswith(p + ' Guard'):
                    k = int(b.split('Guard')[1].split()[0]); col[i] = hue(k, r['n_chains'])
                elif b.startswith(p + ' Cheek'): col[i] = (200, 60, 200)
            cols = {}
            for ti, tri in enumerate(t.tris): cols.setdefault(tuple(col[tri[0]]), []).append(ti)
            for c_, tis in cols.items(): G.append((t.pos, t.tris[np.array(tis)], None, None, tuple(int(x) for x in c_)))
        img = np.hstack([K.render(G, vw, S=13.0, W=440, Z0=140, Z1=100) for vw in ('front', 'side', 'back', 'left')])
        cv2.putText(img, f'{h}: {r["n_chains"]} chains{" closed" if r["closed"] else ""}, cheeks {r["kind"]}, curtain {r["curtain"]} + lining {r["lining"]} pts', (8, 16), 0, 0.5, (255, 255, 255), 1)
        out = W.WORK + f'renders/helmets_{h}.png'; cv2.imwrite(out, img); print(out)


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2:])
