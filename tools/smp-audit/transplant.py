"""Build SMP versions of the Sons of Skyrim FEMALE hold cloaks (and the male
Markarth cloak) by geometry transplant:

  container = male SMP donor nif (Sons of Skyrim - HDT Physics for Cloaks Patch)
              -> keeps CB bone chains, skin weights, Virtual* collision shapes,
                 capeM_SoS.xml root extra data, shader
  geometry  = the static BodySlide build's positions / bitangent / uv / normal /
              tangent (same vertex order, verified: identical triangles + UVs)
              translated into the donor's frame (T from shared-bone transforms)
  extras    = texture set rewritten to the source's textures (Markarth),
              BSTriShape bound + NiSkinData per-bone bounds recomputed.

Read-only on all inputs; writes only into OUT_DIR.
"""
import sys, os, struct, math, shutil
sys.path.insert(0, os.path.dirname(__file__))
from niflib import Nif

SMP = r"C:\1. AUTHORIA\mods\Sons of Skyrim - HDT Physics for Cloaks Patch\Meshes\NordWar\SonsOfSkyrim"
F3BA = r"C:\1. AUTHORIA\mods\Authoria - Bodyslide Output - 3BA\meshes\NordWar\SonsOfSkyrim"
MHIMBO = r"C:\1. AUTHORIA\mods\Authoria - Bodyslide Output - HIMBO\meshes\NordWar\SonsOfSkyrim"
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'out')

# (out folder, out base name, donor folder, donor base, source root, source folder, source base)
JOBS = []
FEMALE = [
    ('Cloack', 'CloackF', 'Cloack', 'cloackm'),
    ('Cloack', 'CloackOfficerF', 'Cloack', 'cloackofficerm'),
    ('Cloack', 'CloackPauldronF', 'Cloack', 'cloackpauldronm'),
    ('Dawnstar', 'CloackF', 'Dawnstar', 'cloackm'),
    ('Falkreath', 'CloackF', 'Falkreath', 'cloackm'),
    ('Morthal', 'CloackF', 'Morthal', 'cloackm'),
    ('Riften', 'CloackF', 'Riften', 'cloackm'),
    ('Solitude', 'CloackF', 'Solitude', 'cloackm'),
    ('Whiterun', 'CloackF', 'Whiterun', 'cloackm'),
    ('Whiterun', 'CloackLightF', 'Whiterun', 'cloacklightm'),
    ('Winterhold', 'CloackF', 'Winterhold', 'cloackm'),
    ('Markarth', 'CloackF', 'Dawnstar', 'cloackm'),      # no Markarth donor: same 997 topology as Dawnstar
]
for of, ob, df, db in FEMALE:
    for w in ('0', '1'):
        JOBS.append((of, '%s_%s.nif' % (ob, w), df, '%s_%s.nif' % (db, w), F3BA, of, '%s_%s.nif' % (ob, w)))
for w in ('0', '1'):
    JOBS.append(('Markarth', 'CloackM_%s.nif' % w, 'Dawnstar', 'cloackm_%s.nif' % w, MHIMBO, 'Markarth', 'CloackM_%s.nif' % w))

def bone_name(n, bi):
    return n.s(struct.unpack_from('<I', n.data, n.offsets[bi])[0])

def cape_shape(n, want=None):
    for i in n.blocks_of('BSTriShape'):
        ts = n.trishape(i)
        if ts['name'].startswith('Virtual'):
            continue
        if want and ts['name'] != want:
            continue
        return i, ts
    raise RuntimeError('no cape shape')

def shader_texset_block(n, shader_block):
    d = n.data; p = n.offsets[shader_block]
    p += 4 + 4
    ned, = struct.unpack_from('<I', d, p); p += 4 + 4*ned
    p += 4 + 8 + 16
    tsi, = struct.unpack_from('<i', d, p)
    return tsi

def read_texset(n, tsi):
    d = n.data; q = n.offsets[tsi]
    cnt, = struct.unpack_from('<I', d, q); q += 4
    texs = []
    for _ in range(cnt):
        ln, = struct.unpack_from('<I', d, q); q += 4
        texs.append(bytes(d[q:q+ln]).decode('latin1')); q += ln
    return texs

def build_texset(texs):
    out = struct.pack('<I', len(texs))
    for t in texs:
        b = t.encode('latin1')
        out += struct.pack('<I', len(b)) + b
    return out

def replace_block(n, bi, newbytes):
    """Replace block bi's bytes with newbytes, fixing the header size table and offsets."""
    old = n.sizes[bi]
    o = n.offsets[bi]
    n.data[o:o+old] = newbytes
    n.sizes[bi] = len(newbytes)
    struct.pack_into('<I', n.data, n.sizes_off + 4*bi, len(newbytes))
    delta = len(newbytes) - old
    for j in range(bi+1, n.num_blocks):
        n.offsets[j] += delta
    n.end += delta

def bounding_sphere(points):
    xs = [p[0] for p in points]; ys = [p[1] for p in points]; zs = [p[2] for p in points]
    c = ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2)
    r = max(math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2 + (p[2]-c[2])**2) for p in points)
    return c, r

def apply_xf(xf, v):
    R = xf[:9]; t = xf[9:12]; s = xf[12]
    return tuple(s*(R[3*i]*v[0] + R[3*i+1]*v[1] + R[3*i+2]*v[2]) + t[i] for i in range(3))

def transplant(donor_path, src_path, out_path, log):
    D = Nif(donor_path)
    S = Nif(src_path)
    footer_len = len(D.data) - D.end
    assert footer_len == 8, ('unexpected footer length', footer_len)
    di, dts = cape_shape(D, 'Cape')
    si_, sts = cape_shape(S)
    dsi = D.skininstance(dts['skin']); ssi = S.skininstance(sts['skin'])
    dsd = D.skindata(dsi['data']); ssd = S.skindata(ssi['data'])
    dverts, dsp, dlay = D.vertices(dsi['partition'])
    sverts, ssp, slay = S.vertices(ssi['partition'])
    assert dsp['nverts'] == ssp['nverts'], ('vertex count mismatch', dsp['nverts'], ssp['nverts'])
    assert dsp['vsize'] == ssp['vsize'] == 40, ('vsize', dsp['vsize'], ssp['vsize'])
    assert dsp['vflags'] == ssp['vflags'], ('vflags', hex(dsp['vflags']), hex(ssp['vflags']))
    # topology guard: identical UVs and triangles (through vertex maps)
    uvd = max(max(abs(a-b) for a, b in zip(x['uv'], y['uv'])) for x, y in zip(dverts, sverts))
    def real_tris(sp):
        p = sp['parts'][0]; vm = p['vmap']; t = p['tris']
        return [vm[x] for x in t] if vm else t
    assert uvd < 1e-6, ('uv mismatch', uvd)
    assert real_tris(dsp) == real_tris(ssp), 'triangle mismatch'
    assert dsp['nparts'] == 1 and ssp['nparts'] == 1
    # frame transform T (donor <- source), from every shared bone; must agree
    dnames = [bone_name(D, b) for b in dsi['bones']]
    snames = [bone_name(S, b) for b in ssi['bones']]
    Ts = []
    for nm in snames:
        if nm in dnames:
            xd = dsd['bones'][dnames.index(nm)]['xf']; xs = ssd['bones'][snames.index(nm)]['xf']
            Rd = xd[:9]; Rs = xs[:9]
            # rotation must match (col convention: T_R = Rd^T Rs)
            RtR = [sum(Rd[3*k+i]*Rs[3*k+j] for k in range(3)) for i in range(3) for j in range(3)]
            rot_dev = max(abs(RtR[i] - (1.0 if i in (0, 4, 8) else 0.0)) for i in range(9))
            dt = [xs[9+i]-xd[9+i] for i in range(3)]
            t = tuple(sum(Rd[3*k+i]*dt[k] for k in range(3)) for i in range(3))   # Rd^T * dt
            Ts.append((nm, t, rot_dev, xd[12], xs[12]))
    assert Ts, 'no shared bones'
    # use Spine2 (the cape's anchor) as the reference; the others must agree closely
    ref = [x for x in Ts if x[0] == 'NPC Spine2 [Spn2]'][0]
    t0 = ref[1]
    ANCHORS = ('NPC Spine2 [Spn2]', 'NPC Spine1 [Spn1]', 'NPC Spine [Spn0]', 'NPC L Clavicle [LClv]',
               'NPC R Clavicle [RClv]', 'NPC L Pauldron', 'NPC R Pauldron', 'NPC L UpperArm [LUar]', 'NPC R UpperArm [RUar]')
    worst_rot = max(x[2] for x in Ts); worst_t = 0.0
    for nm, t, rot_dev, sd_, ss_ in Ts:
        dev = max(abs(t[i]-t0[i]) for i in range(3)); worst_t = max(worst_t, dev)
        if nm in ANCHORS:
            assert rot_dev < 2e-3, ('rotation differs for anchor bone', nm, rot_dev)
            assert dev < 0.05, ('T differs across anchor bones', nm, t, t0)
        else:   # arm twist bones: the two skeleton references differ by a fraction of a unit; informational
            assert rot_dev < 0.02, ('rotation differs for bone', nm, rot_dev)
            assert dev < 1.0, ('T differs across bones', nm, t, t0)
        assert abs(sd_-1) < 1e-4 and abs(ss_-1) < 1e-4, ('scale', nm, sd_, ss_)
    T = t0
    # ---- copy per-vertex geometry (first 28 bytes) with translated positions ----
    dv = dsp['vdata_off']; sv = ssp['vdata_off']; vs = dsp['vsize']
    newpos = []
    for k in range(dsp['nverts']):
        src = bytes(S.data[sv + k*vs: sv + k*vs + 28])
        x, y, z = struct.unpack_from('<3f', src, 0)
        x, y, z = x + T[0], y + T[1], z + T[2]
        newpos.append((x, y, z))
        rec = struct.pack('<3f', x, y, z) + src[12:28]
        D.data[dv + k*vs: dv + k*vs + 28] = rec
    # ---- BSTriShape bounding sphere ----
    c, r = bounding_sphere(newpos)
    struct.pack_into('<4f', D.data, dts['bound_off'], c[0], c[1], c[2], r)
    # ---- NiSkinData per-bone bounds (bone-local space) ----
    part = dsp['parts'][0]
    per_bone = {}
    for k, v in enumerate(dverts):
        for slot in range(4):
            w = v['w'][slot]
            if w > 0:
                gb = part['bones'][v['bi'][slot]]  # partition-local -> skin-instance bone index
                per_bone.setdefault(gb, []).append(newpos[k])
    sdo = D.offsets[dsi['data']]
    p = sdo + 52 + 4 + 1
    for b in range(len(dsd['bones'])):
        xf = dsd['bones'][b]['xf']
        pts = per_bone.get(b)
        if pts:
            loc = [apply_xf(xf, q) for q in pts]
            bc, br = bounding_sphere(loc)
            struct.pack_into('<4f', D.data, p + 52, bc[0], bc[1], bc[2], br)
        nv = dsd['bones'][b]['nv']
        p += 52 + 16 + 2 + (6*nv if dsd['has_vw'] else 0)
    # ---- texture set: adopt the source's textures ----
    dtsi = shader_texset_block(D, dts['shader']); stsi = shader_texset_block(S, sts['shader'])
    dtex = read_texset(D, dtsi); stex = read_texset(S, stsi)
    tex_changed = dtex != stex
    if tex_changed:
        replace_block(D, dtsi, build_texset(stex))
    # ---- write ----
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # NiFooter (num roots + root refs) sits after the last block; it moved with the bytearray edits.
    assert len(D.data) - D.end == footer_len, (len(D.data), D.end, footer_len)
    with open(out_path, 'wb') as fh:
        fh.write(bytes(D.data))
    # ---- verify by re-reading ----
    V = Nif(out_path)
    vi, vts = cape_shape(V, 'Cape')
    vsi = V.skininstance(vts['skin'])
    vverts, vsp, _ = V.vertices(vsi['partition'])
    assert len(V.data) - V.end == 8, (len(V.data), V.end)
    maxd = max(max(abs(a-b) for a, b in zip(x['pos'], y)) for x, y in zip(vverts, newpos))
    assert maxd < 1e-5, maxd
    for x, y in zip(vverts, dverts):
        assert x['w'] == y['w'] and x['bi'] == y['bi']
    vtex = read_texset(V, shader_texset_block(V, vts['shader']))
    assert vtex == stex, (vtex, stex)
    log.append('%s <- donor %s + geometry %s | T=(%.3f, %.3f, %.3f) [%d shared bones, rot dev %.4f, t dev %.3f] verts=%d bound=(%.2f,%.2f,%.2f r=%.2f) tex%s' % (
        os.path.relpath(out_path, OUT_DIR), os.path.relpath(donor_path, SMP), os.path.relpath(src_path, os.path.dirname(os.path.dirname(src_path))),
        T[0], T[1], T[2], len(Ts), worst_rot, worst_t, len(newpos), c[0], c[1], c[2], r, ' REWRITTEN -> %s' % [t for t in stex if t] if tex_changed else ' unchanged'))

if __name__ == '__main__':
    log = []
    for of, ob, df, db, sroot, sf, sb in JOBS:
        donor = os.path.join(SMP, df, db)
        src = os.path.join(sroot, sf, sb)
        out = os.path.join(OUT_DIR, 'meshes', 'NordWar', 'SonsOfSkyrim', of, ob)
        transplant(donor, src, out, log)
    for l in log:
        print(l)
    print('built %d files into %s' % (len(log), OUT_DIR))
