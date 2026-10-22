"""Bake clearance margin into outfit shells: push shell verts to >= MARGIN outside
the player's live-morphed body (weight 0.78 + her RaceMenu morphs, applied via each
outfit's own tri). Push along the body's true vertex normals (computed from triangles).
Applies the same delta to _0 and _1. In-place with backups. --apply to write."""
import os, sys, json, struct, shutil
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif
from weld_taper import shape_buffers, write_pos, layout

APPLY = '--apply' in sys.argv
MARGIN = 0.28
WEIGHT = 0.78
BK = r"C:\1. AUTHORIA\backups\clearance-20260731"
PRESET = r"C:/1. AUTHORIA/mods/Authoria - RaceMenu Preset - Bish Base/SKSE/Plugins/CharGen/Presets/bish - breton.jslot"
BODY_NIF = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
BODY_NIF0 = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_0.nif"

SKIP_ITEMS = ('necklace', 'choker', 'earring', 'heels', 'bag', 'airpod', 'glasses', 'chanel', 'ring')
SKIP_SHAPES = ('feet', 'thighs', 'hands', 'virtualbody', 'virtualground', 'decal')
PUSH_CAP = 0.55
TARGETS = []
DRESSES = ('seradefault', 'seradefaultsleeveless', 'seradress', 'serasundress',
           'serasweater', 'serasweaterdress')
_root = r"C:/1. AUTHORIA/mods/Authoria - UBE Converter Output/meshes/!UBE/kw_stuff"
for f in sorted(os.listdir(_root)):
    if f.lower().endswith('_1.nif') and f[:-6].rstrip('_').lower() in DRESSES:
        TARGETS.append(os.path.join(_root, f))

def trip_morphs(path):
    if not os.path.exists(path): return {}
    d = open(path, 'rb').read()
    if d[:4] != b'PIRT': return {}
    o = 4; ns = struct.unpack_from('<H', d, o)[0]; o += 2
    out = {}
    for _ in range(ns):
        ln = d[o]; o += 1
        sname = d[o:o+ln].decode('ascii', 'replace'); o += ln
        nm = struct.unpack_from('<H', d, o)[0]; o += 2
        ms = {}
        for _m in range(nm):
            ml = d[o]; o += 1
            name = d[o:o+ml].decode('ascii', 'replace'); o += ml
            mult = struct.unpack_from('<f', d, o)[0]; o += 4
            nd = struct.unpack_from('<H', d, o)[0]; o += 2
            arr = np.frombuffer(d, '<i2', nd * 4, o).reshape(-1, 4) if nd else np.zeros((0, 4), '<i2')
            ms[name] = (mult, arr)
            o += nd * 8
        out[sname] = ms
    return out

def apply_morphs(pos, morphs, values):
    out = pos.copy()
    for name, val in values.items():
        m = morphs.get(name)
        if m is None: continue
        mult, arr = m
        if not len(arr): continue
        idx = arr[:, 0].astype(np.uint16).astype(np.int64)
        ok = idx < len(out)
        out[idx[ok]] += arr[ok, 1:4].astype(np.float32) * (mult * val)
    return out

def shape_triangles(nif, block_shapes):
    """shape name -> global-index triangle array, from skin partitions."""
    tris = {}
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        sh = nif.parse_shape(i)
        if sh['skin_ref'] < 0: continue
        si = nif.parse_skin_instance(sh['skin_ref'])
        if si['partition_ref'] < 0: continue
        sp = nif.parse_skin_partition(si['partition_ref'])
        allt = []
        for p in sp.get('partitions', []):
            vm = p.get('vertex_map')
            tc = p.get('tris_copy') or p.get('tris') or []
            for a, b, c in tc:
                if vm:
                    if a < len(vm) and b < len(vm) and c < len(vm):
                        allt.append((vm[a], vm[b], vm[c]))
                else:
                    allt.append((a, b, c))
        if allt:
            tris[sh['name']] = np.array(allt, np.int64)
    return tris

def vertex_normals(pos, tris):
    n = np.zeros_like(pos)
    a, b, c = pos[tris[:, 0]], pos[tris[:, 1]], pos[tris[:, 2]]
    fn = np.cross(b - a, c - a)
    for k in range(3):
        np.add.at(n, tris[:, k], fn)
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    return n / ln

j = json.load(open(PRESET, encoding='utf-8-sig'))
HER = {m['name']: sum(k['value'] for k in m['keys']) for m in j['bodyMorphs']}
HER = {k: v for k, v in HER.items() if abs(v) > 1e-6}
ref_body = np.array(shape_buffers(Nif(BODY_NIF))['BaseShape']['positions'], np.float32)

report = []
for n1 in sorted(TARGETS):
    n0 = n1[:-6] + '0.nif'
    tri = n1[:-6].rstrip('_') + '.tri'
    if not os.path.exists(tri):
        tri = None
    try:
        nif1 = Nif(n1)
        shapes1 = shape_buffers(nif1)
        tris1 = shape_triangles(nif1, shapes1)
    except Exception as e:
        report.append((n1, 'PARSE FAIL %s' % e, 0)); continue
    morphs = trip_morphs(tri) if tri else {}
    # find the body copy: 29298 verts matching the reference body
    body_name = None
    for name, info in shapes1.items():
        if info['positions'] is not None and len(info['positions']) == len(ref_body):
            pos = np.array(info['positions'], np.float32)
            if np.abs(pos[::97] - ref_body[::97]).max() < 0.6:
                body_name = name; break
    if body_name is None:
        # no body copy inside: use the naked reference directly
        body_pos1 = ref_body
        body_tri_morphs = trip_morphs(r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent.tri").get('BaseShape', {})
        body_tris = None
    else:
        body_pos1 = np.array(shapes1[body_name]['positions'], np.float32)
        body_tri_morphs = morphs.get(body_name, {})
        body_tris = tris1.get(body_name)
    # body at her weight+morphs
    shapes0 = None
    body_w = body_pos1
    if n0 and os.path.exists(n0):
        try:
            shapes0 = shape_buffers(Nif(n0))
        except Exception:
            shapes0 = None
    if body_name and shapes0 and shapes0.get(body_name) is not None        and shapes0[body_name]['positions'] is not None:
        b0 = np.array(shapes0[body_name]['positions'], np.float32)
        if len(b0) == len(body_pos1): body_w = b0 + (body_pos1 - b0) * WEIGHT
    elif not body_name:
        try:
            nb0 = np.array(shape_buffers(Nif(BODY_NIF0))['BaseShape']['positions'], np.float32)
            if len(nb0) == len(body_pos1): body_w = nb0 + (body_pos1 - nb0) * WEIGHT
        except Exception:
            pass
    body_live = apply_morphs(body_w, body_tri_morphs, HER)
    if body_tris is not None and len(body_tris):
        normals = vertex_normals(body_live, body_tris)
    else:
        # fallback: radial from vertical axis
        normals = body_live - np.array([[0, 0, 0]], np.float32)
        normals[:, 2] = 0
        ln = np.linalg.norm(normals, axis=1, keepdims=True); ln[ln == 0] = 1
        normals = normals / ln

    if any(k in os.path.basename(n1).lower() for k in SKIP_ITEMS):
        continue
    changed_total = 0
    per_shape = {}
    bufs = {}
    # rank shells innermost-first for stepped margins (preserves layer separation)
    shell_rank = {}
    med = []
    for name, info in shapes1.items():
        if name == body_name or info['positions'] is None or info['writer'] is None: continue
        if name.lower() in SKIP_SHAPES or any(name.lower().startswith(s) for s in SKIP_SHAPES): continue
        pos1 = np.array(info['positions'], np.float32)
        if len(pos1) < 50 or len(pos1) == len(ref_body): continue
        sample = pos1[::max(1, len(pos1)//300)]
        d2s = ((sample[:, None, :] - body_live[None, ::9, :]) ** 2).sum(axis=2)
        med.append((float(np.median(np.sqrt(d2s.min(axis=1)))), name))
    for rank, (_m, nm) in enumerate(sorted(med)):
        shell_rank[nm] = min(rank, 3)
    for name, info in shapes1.items():
        if name == body_name or info['positions'] is None or info['writer'] is None: continue
        if name.lower() in SKIP_SHAPES or any(name.lower().startswith(s) for s in SKIP_SHAPES): continue
        pos1 = np.array(info['positions'], np.float32)
        if len(pos1) < 50 or len(pos1) == len(ref_body): continue
        margin_here = MARGIN + 0.05 * shell_rank.get(name, 0)
        s0info = shapes0.get(name) if shapes0 else None
        pos0 = np.array(s0info['positions'], np.float32) if s0info and s0info['positions'] is not None and len(s0info['positions']) == len(pos1) else None
        pos_w = pos0 + (pos1 - pos0) * WEIGHT if pos0 is not None else pos1
        shell_live = apply_morphs(pos_w, morphs.get(name, {}), HER)
        # nearest live body vert per shell vert (chunked)
        n = len(shell_live)
        push = np.zeros((n, 3), np.float32)
        for c0 in range(0, n, 2048):
            ch = shell_live[c0:c0+2048]
            d2 = ((ch[:, None, :] - body_live[None, :, :]) ** 2).sum(axis=2)
            ni = d2.argmin(axis=1)
            bp = body_live[ni]; bn = normals[ni]
            rel = ch - bp
            signed = (rel * bn).sum(axis=1)   # + outside, - inside
            deficit = np.minimum(margin_here - signed, PUSH_CAP)
            m = (deficit > 0) & (np.sqrt(d2[np.arange(len(ch)), ni]) < 3.0 + margin_here)
            push[c0:c0+2048][m] = bn[m] * deficit[m, None]
        # --- midsection front/sides only ---
        bz = body_live[:, 2]
        hip, chest = np.percentile(bz, 52), np.percentile(bz, 78)
        zc = shell_live[:, 2]
        keep = (zc >= hip) & (zc <= chest) & (shell_live[:, 1] > -1.5)
        push[~keep] = 0.0
        moved = int((np.abs(push).max(axis=1) > 0.005).sum())
        if moved == 0: continue
        per_shape[name] = (moved, float(np.abs(push).max()))
        changed_total += moved
        # apply same push to _1 and _0 buffers
        for which, nf, inf in (('1', nif1, info), ('0', None, s0info)):
            if which == '0':
                if s0info is None or pos0 is None: continue
                if '0' not in bufs:
                    bufs['0'] = (Nif(n0), None)
                    bufs['0'] = (bufs['0'][0], bytearray(bufs['0'][0].data))
                nifX, buf = bufs['0']
                base = pos0
                winfo = shape_buffers(nifX)[name]
            else:
                if '1' not in bufs:
                    bufs['1'] = (nif1, bytearray(nif1.data))
                nifX, buf = bufs['1']
                base = pos1
                winfo = info
            newpos = base + push
            for vi in range(len(newpos)):
                if abs(push[vi][0]) + abs(push[vi][1]) + abs(push[vi][2]) > 0.005:
                    write_pos(buf, winfo['writer'], vi, tuple(float(x) for x in newpos[vi]))
    if changed_total and APPLY:
        for which, path in (('1', n1), ('0', n0)):
            if which in bufs:
                rel = os.path.relpath(path, r"C:/1. AUTHORIA/mods")
                dst = os.path.join(BK, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst): shutil.copy2(path, dst)
                with open(path, 'wb') as f: f.write(bytes(bufs[which][1]))
                Nif(path)  # reparse sanity
    if changed_total:
        report.append((n1, per_shape, changed_total))

print('%s MIDSECTION | margin=%.2f weight=%.2f | items adjusted: %d' % ('APPLIED' if APPLY else 'DRY-RUN', MARGIN, WEIGHT, len(report)))
for p, per, tot in report:
    rel = p.replace('C:/1. AUTHORIA/mods/Authoria - UBE Converter Output/meshes/!UBE/', '')
    if isinstance(per, str):
        print('  %-70s %s' % (rel[:70], per)); continue
    print('  %-70s pushed=%d  %s' % (rel[:70], tot,
        ', '.join('%s(%d,max %.2f)' % (k, v[0], v[1]) for k, v in sorted(per.items())[:4])))
