"""smpkit checks: offline verification helpers used by verify_rig.py, stride_check.py and pose_render.py.
None of this simulates physics - it poses bones by hand and measures the skinned result (see references/testing.md
for what that can and cannot catch)."""
import os, subprocess, shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
import numpy as np
import smpkit
from smpkit import core as C

# ==================== source-vs-output identity ====================
class Matcher:
    def __init__(self, P, U):
        self.P, self.U = P, U
        self.cells = defaultdict(list)
        for i, p in enumerate(P): self.cells[tuple(np.floor(p * 100).astype(int))].append(i)
        # canonical id per source vertex: the first vertex with the same position and UV
        self.canon = np.arange(len(P))
        for i in range(len(P)):
            for j in self.near(P[i], U[i]):
                if j < self.canon[i]: self.canon[i] = j

    def near(self, p, u):
        c = np.floor(p * 100).astype(int); out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in self.cells.get((c[0] + dx, c[1] + dy, c[2] + dz), ()):
                        if np.abs(self.P[j] - p).max() < 1e-4 and np.abs(self.U[j] - u).max() < 1e-5: out.append(j)
        return out
def compare(t, outs):
    M = Matcher(t.pos, t.uv)
    src = defaultdict(int)
    for tri in t.tris: src[frozenset(int(M.canon[i]) for i in tri)] += 1
    got = defaultdict(int); new = 0
    for o in outs:
        cid = []
        for p, u in zip(o.pos, o.uv):
            m = M.near(p, u); cid.append(int(M.canon[m[0]]) if m else -1)
        for tri in o.tris:
            k = frozenset(cid[i] for i in tri)
            if -1 not in k and k in src: got[k] += 1
            else: new += 1
    kept = sum(min(c, got.get(k, 0)) for k, c in src.items())
    extra = sum(max(0, got.get(k, 0) - c) for k, c in src.items())
    return len(t.tris), kept, new, extra

# ==================== posing physics chains (swing / curl) ====================
LIM = dict(out=0.45, inn=0.25, side=0.08)
LIM1 = dict(out=0.85, inn=0.25, side=0.12)
def bone_world(T):
    s2b = {}
    for t in T: s2b.update(t.s2b)
    return {b: np.linalg.inv(C.tb2m(m)) for b, m in s2b.items()}
def chains(Gw, p, nrow=5):
    out = []
    for k in range(40):
        bs = [f'{p} Skirt{k:02d} {r}' for r in range(nrow + 1)]
        if bs[1] not in Gw: break
        out.append(bs)
    return out
def flare(Gw, ch, cx, cy, th1, th):
    """every chain out (th > 0) or in (th < 0) about its own tangent"""
    Dm = {}
    for bs in ch:
        p0 = Gw[bs[0]][:3, 3]; a = np.arctan2(p0[0] - cx, p0[1] - cy)
        radial = np.array([np.sin(a), np.cos(a), 0.0]); tang = np.array([np.cos(a), -np.sin(a), 0.0])
        D = np.eye(4)
        for r in range(1, len(bs)):
            if bs[r] not in Gw: break
            piv = (D @ np.r_[Gw[bs[r - 1]][:3, 3], 1])[:3]
            R1 = rot(D[:3, :3] @ tang, 1.0, piv); dn = (R1 @ np.r_[piv - [0, 0, 5], 1])[:3] - (piv - [0, 0, 5])
            sg = 1.0 if dn @ radial > 0 else -1.0
            D = rot(D[:3, :3] @ tang, sg * (th1 if r == 1 else th), piv) @ D; Dm[bs[r]] = D.copy()
    return Dm
def skin(pos, wts, Dm):
    P = np.c_[pos, np.ones(len(pos))]
    return np.array([(sum(x * Dm.get(b, np.eye(4)) for b, x in w.items()) @ P[i])[:3] for i, w in enumerate(wts)])
def swing(Gw, ch, cx, cy, world_axis, th1, th):
    """every joint turns about world_axis (pivot = the parent bone), split into out/in + sideways and clamped to the limits"""
    Dm = {}
    for bs in ch:
        p0 = Gw[bs[0]][:3, 3]; a = np.arctan2(p0[0] - cx, p0[1] - cy)
        radial = np.array([np.sin(a), np.cos(a), 0.0]); tang = np.array([np.cos(a), -np.sin(a), 0.0])
        D = np.eye(4)
        for r in range(1, len(bs)):
            if bs[r] not in Gw: break
            L = LIM1 if r == 1 else LIM; t = th1 if r == 1 else th
            v = np.asarray(world_axis, float) * t
            # out/in = about the tangent; positive = the lower part goes outward
            o = float(v @ tang); s = float(v @ radial)
            piv = (D @ np.r_[Gw[bs[r - 1]][:3, 3], 1])[:3]
            R1 = rot(D[:3, :3] @ tang, 1.0, piv); dn = (R1 @ np.r_[piv - [0, 0, 5], 1])[:3] - (piv - [0, 0, 5])
            sg = 1.0 if dn @ radial > 0 else -1.0
            o = float(np.clip(o * sg, -L['inn'], L['out'])) * sg
            s = float(np.clip(s, -L['side'], L['side']))
            M = rot(D[:3, :3] @ radial, s, piv) @ rot(D[:3, :3] @ tang, o, piv) if (o or s) else np.eye(4)
            D = M @ D; Dm[bs[r]] = D.copy()
    return Dm

# ==================== rotations, a kick pose, skinning whole shapes ====================
def rot(axis, th, piv):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    Rm = np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K
    M = np.eye(4); M[:3, :3] = Rm; M[:3, 3] = piv - Rm @ piv; return M
TOTAL, CEN, SIG = 1.0, 25.0, 40.0    # pose test: total outward kick (rad) over a chain, centred 25 deg right of front, spread 40 deg


def pose(chains, cx, cy):
    """chains: [(bones top->bottom, bind positions, pivot positions per bone)] -> {bone: world delta}"""
    Dm = {}
    for bones, pos, piv in chains:
        c = pos[0]; ang = np.degrees(np.arctan2(c[0] - cx, c[1] - cy))
        g = np.exp(-(((ang - CEN + 180) % 360 - 180) / SIG) ** 2); th = TOTAL * g / len(bones)
        axis = np.array([np.cos(np.radians(ang)), -np.sin(np.radians(ang)), 0.0])
        D = np.eye(4)
        for b, p in zip(bones, piv):
            pw = (D @ np.r_[p, 1])[:3]; D = rot(axis, th, pw) @ D; Dm[b] = D.copy()
    return Dm
def skin_shapes(T, Dm):
    out = []
    for t in T:
        P = np.c_[t.pos, np.ones(len(t.pos))]; Q = np.zeros((len(P), 3))
        for i, w in enumerate(t.w):
            M = sum(x * Dm.get(b, np.eye(4)) for b, x in w.items()); Q[i] = (M @ P[i])[:3]
        out.append(Q)
    return out

# ==================== textured software render (needs opencv-python; textures via texconv) ====================
TEX = None                # png cache folder for converted textures (set by the caller)
TEXROOTS = []             # folders holding textures\... (mod folders), searched in order
_warned = []


def load_tex(rel):
    import cv2
    if not rel or TEX is None: return None
    os.makedirs(TEX, exist_ok=True)
    png = os.path.join(TEX, os.path.splitext(os.path.basename(rel))[0] + ".png")
    if not os.path.exists(png):
        src = next((os.path.join(r, rel) for r in TEXROOTS if os.path.exists(os.path.join(r, rel))), None)
        if src is None: return None
        tc = smpkit.setting("TEXCONV") or shutil.which("texconv")
        if not tc or not (os.path.exists(tc) or shutil.which(tc)):
            if not _warned: print('textures: texconv not found (set TEXCONV) - rendering flat grey'); _warned.append(1)
            return None
        subprocess.run([tc, "-nologo", "-ft", "png", "-f", "R8G8B8A8_UNORM", "-m", "1", "-w", "1024", "-h", "1024", "-y", "-o", TEX, src],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cands = [f for f in os.listdir(TEX) if f.lower() == os.path.basename(png).lower()]
        if not cands: return None
        png = os.path.join(TEX, cands[0])
    return cv2.imread(png, cv2.IMREAD_UNCHANGED)
def render(geoms, view, S=2.4, W=330, Z0=125, Z1=0):
    import cv2
    H = int((Z0 - Z1) * S) + 10
    img = np.full((H, W, 3), 30, np.uint8); zb = np.full((H, W), -1e9)
    # front: viewer at +y looking -y (actor faces +y): screen x = -x? actor's right (-x) appears on viewer's left
    for V, T, UV, tex, col in geoms:
        V = np.asarray(V)
        if V.ndim != 2 or not len(V) or not len(T): continue      # Authoria 2026-10-18: an empty shape (a panel with no front lining)
        if view == "front": X = -V[:, 0]; D = V[:, 1]
        elif view == "back": X = V[:, 0]; D = -V[:, 1]
        elif view == 'side': X = V[:, 1]; D = -V[:, 0]       # right side: viewer at -x
        else: X = -V[:, 1]; D = V[:, 0]                      # left side: viewer at +x
        px = W / 2 + X * S; py = (Z0 - V[:, 2]) * S
        n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); nl = np.linalg.norm(n, axis=1) + 1e-9
        vd = {"front": np.array([0, 1, 0]), "back": np.array([0, -1, 0]), "side": np.array([-1, 0, 0]), "left": np.array([1, 0, 0])}[view]
        shade = 0.35 + 0.65 * np.abs(n @ vd) / nl
        for t, sh in zip(T, shade):
            xs, ys = px[t], py[t]
            x0, x1 = int(max(0, np.floor(xs.min()))), int(min(W - 1, np.ceil(xs.max())))
            y0, y1 = int(max(0, np.floor(ys.min()))), int(min(H - 1, np.ceil(ys.max())))
            if x1 < x0 or y1 < y0: continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            d = (xs[1] - xs[0]) * (ys[2] - ys[0]) - (xs[2] - xs[0]) * (ys[1] - ys[0])
            if abs(d) < 1e-9: continue
            l1 = ((gx - xs[0]) * (ys[2] - ys[0]) - (xs[2] - xs[0]) * (gy - ys[0])) / d
            l2 = ((xs[1] - xs[0]) * (gy - ys[0]) - (gx - xs[0]) * (ys[1] - ys[0])) / d
            l0 = 1 - l1 - l2; m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
            if not m.any(): continue
            z = l0 * D[t[0]] + l1 * D[t[1]] + l2 * D[t[2]]
            yy, xx = np.nonzero(m); yy += y0; xx += x0; zz = z[m]
            ok = zz > zb[yy, xx]
            if not ok.any(): continue
            yy, xx, zz = yy[ok], xx[ok], zz[ok]
            if tex is not None:
                u = (l0[m][ok] * UV[t[0], 0] + l1[m][ok] * UV[t[1], 0] + l2[m][ok] * UV[t[2], 0]) % 1.0
                v = (l0[m][ok] * UV[t[0], 1] + l1[m][ok] * UV[t[1], 1] + l2[m][ok] * UV[t[2], 1]) % 1.0
                th, tw = tex.shape[:2]; c = tex[(v * (th - 1)).astype(int), (u * (tw - 1)).astype(int)]
                if c.shape[1] == 4:
                    keep = c[:, 3] > 60; yy, xx, zz, c = yy[keep], xx[keep], zz[keep], c[keep]
                c = c[:, :3].astype(np.float64)
            else:
                c = np.tile(np.array(col, np.float64), (len(yy), 1))
            zb[yy, xx] = zz; img[yy, xx] = np.clip(c * sh, 0, 255).astype(np.uint8)
    for zl in range(10, 125, 10):
        y = int((Z0 - zl) * S); cv2.putText(img, str(zl), (2, y + 4), 0, 0.3, (120, 120, 120), 1); cv2.line(img, (18, y), (24, y), (120, 120, 120), 1)
    cv2.putText(img, view, (W - 50, 14), 0, 0.45, (255, 255, 255), 1)
    return img

# ==================== faces ====================
def faces(P, T_):
    fn = np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]); return fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)

# ==================== leg stride pose ====================
LEG = {'R': ('NPC R Thigh [RThg]', 'NPC R Calf [RClf]', 'NPC R Foot [Rft ]', 'NPC R Toe0 [RToe]'),
       'L': ('NPC L Thigh [LThg]', 'NPC L Calf [LClf]', 'NPC L Foot [Lft ]', 'NPC L Toe0 [LToe]')}
def stride(T, fwd=50.0, back=25.0):
    s2b = {}
    for t in T: s2b.update(t.s2b)
    Dm = {}
    for side, ang in (('R', fwd), ('L', -back)):
        hip = np.linalg.inv(C.tb2m(s2b[LEG[side][0]]))[:3, 3]
        M = rot(np.array([1.0, 0, 0]), np.radians(ang), hip)          # +x axis: positive = knee forward (+y)
        for b in LEG[side]: Dm[b] = M
    return Dm

# ==================== checks, XML reading, rest contacts ====================
ok_all = True
def check(cond, msg):
    global ok_all
    ok_all &= bool(cond)
    print(('  ok   ' if cond else '  FAIL ') + msg)
def collide(a, b):
    ok = lambda x, y: all(t not in x['no'] for t in y['tags']) and (not x['can'] or any(t in x['can'] for t in y['tags']))
    return ok(a, b) and ok(b, a)
def rest(label, pos, tris, xs, legs_out=True):
    """pairs the XML lets collide: points of a per-vertex shape within the two margins of a per-triangle shape's
    triangles (unsigned), and points of anything that sit INSIDE the legs (signed, within the legs' penetration)"""
    bad = {}
    names = [n for n in xs if n in pos]
    for a in names:
        for b in names:
            if a == b or not collide(xs[a], xs[b]): continue
            A_, B_ = xs[a], xs[b]
            if A_['kind'] == 'per-vertex-shape' and B_['kind'] == 'per-triangle-shape':
                tri, bary, d, cp = C.Surface([('s', pos[b], tris[b])]).query(pos[a], k=8)
                n = int((d < A_['margin'] + B_['margin']).sum())
                if n: bad[f'{a} -> {b}'] = (n, float(d.min()))
            elif A_['kind'] == B_['kind'] == 'per-triangle-shape' and a < b:
                for p, q in ((a, b), (b, a)):
                    _, _, d, _ = C.Surface([('s', pos[q], tris[q])]).query(pos[p], k=8)
                    n = int((d < A_['margin'] + B_['margin']).sum())
                    if n: bad[f'{p} ~ {q}'] = (n, float(d.min()))
    check(not bad, f'{label}: no rest contacts' + ('' if not bad else f' {bad}'))
def xml_info(path):
    root = ET.parse(path).getroot(); shapes = {}
    for el in root:
        if el.tag in ('per-triangle-shape', 'per-vertex-shape'):
            shapes[el.get('name')] = dict(kind=el.tag, margin=float(el.findtext('margin') or 0), pen=float(el.findtext('penetration') or 0),
                                          tags=[e.text for e in el.findall('tag')], can=[e.text for e in el.findall('can-collide-with-tag')],
                                          no=[e.text for e in el.findall('no-collide-with-tag')])
    bones = [el.get('name') for el in root if el.tag == 'bone']
    cons = [(el.get('bodyA'), el.get('bodyB')) for el in root.iter('generic-constraint')]
    return shapes, bones, cons

# ==================== simulated BodySlide builds ====================
def preset(path, name):
    if path is None: return {}
    p = next(e for e in ET.parse(path).getroot().findall('Preset') if e.get('name') == name)
    return {(s.get('name'), s.get('size')): float(s.get('value')) for s in p.findall('SetSlider')}
def morph(ss, osd, shapes, pre, size):
    """BodySlide's build: every slider at the preset's value (or the set's default), its data added at value/100"""
    out = {k: v.copy() for k, v in shapes.items()}
    for sl in ss.findall('Slider'):
        val = pre.get((sl.get('name'), size), float(sl.get(size)))
        f = val / 100.0
        if sl.get('invert') == 'true': f = 1.0 - f
        if abs(f) < 1e-9: continue
        for d in sl.findall('Data'):
            tgt = d.get('target')
            if tgt not in out: continue
            for i, x in osd[d.text.split('\\', 1)[1]].items(): out[tgt][i] += f * np.asarray(x)
    return out


