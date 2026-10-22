"""Prepare (in the scratchpad only) the SMP-restored copies for every buried mesh
found by the audit. Nothing in the MO2 instance is modified.

  A) Velothi HIMBO/3BA builds + Falmer Slayer UBE builds: keep the built geometry,
     re-add the root NiStringExtraData -> the source mod's xml.
  B) volsCloaks UBE copies: transplant (SMP source container + UBE geometry) so the
     VirtualBody/VirtualGround collision shapes come back.
Outputs go to  scratchpad\restore_out\<mod layout>.
"""
import os, sys, struct, shutil, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nif_extradata import add_smp_extradata
from niflib import Nif
from bsa_audit import read_bsa_index, extract
from smp_audit import enabled_mods, MODS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'restore_out')
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
MODLIST = enabled_mods()

def find_bsa(name):
    for m in MODLIST:
        p = os.path.join(MODS, m, name)
        if os.path.isfile(p): return p
    raise FileNotFoundError(name)

# ---- A) re-add extra data ----
A = [
    # (winner mod, rel path, xml string to point at)  -- xml strings copied verbatim from the SMP sources
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmet_0.nif', r'meshes\pulcharmsolis\indoril wayfarer\TSXML.xml'),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmet_1.nif', r'meshes\pulcharmsolis\indoril wayfarer\TSXML.xml'),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmetwithscarfm_0.nif', r'meshes\pulcharmsolis\indoril wayfarer\TSXML.xml'),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmetwithscarfm_1.nif', r'meshes\pulcharmsolis\indoril wayfarer\TSXML.xml'),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\ashlander seer\bootsm_0.nif', r'meshes\pulcharmsolis\RedoranExile\REXML.xml'),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\ashlander seer\bootsm_1.nif', r'meshes\pulcharmsolis\RedoranExile\REXML.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlander seer\bootsf_0.nif', r'meshes\pulcharmsolis\RedoranExile\REXML.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlander seer\bootsf_1.nif', r'meshes\pulcharmsolis\RedoranExile\REXML.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\camonnatong\steelglovesf_0.nif', r'meshes\pulcharmsolis\camonnatong\data.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\camonnatong\steelglovesf_1.nif', r'meshes\pulcharmsolis\camonnatong\data.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlanderwarrior\steelbodyf_0.nif', r'meshes\pulcharmsolis\ashlanderwarrior\data.xml'),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlanderwarrior\steelbodyf_1.nif', r'meshes\pulcharmsolis\ashlanderwarrior\data.xml'),
    ('Authoria - Bodyslide Output - UBE', r'meshes\!ube\falmerslayer\falmerslayerhelmet.nif', r'meshes\falmerslayer\hood.xml'),
    ('Authoria - Bodyslide Output - UBE', r'meshes\!ube\falmerslayer\falmerslayerfaceguard.nif', r'meshes\falmerslayer\hood.xml'),
]
# sanity: the xml strings must match what the SMP sources reference (checked in pair_check) and exist
for mod, rel, xml in A:
    src = os.path.join(MODS, mod, rel)
    dst = os.path.join(OUT, rel)
    mode = add_smp_extradata(src, dst, xml)
    print('A  %-70s %s' % (rel, mode))

# ---- B) volsCloaks transplant (multi-shape by name) ----
def bone_name(n, bi):
    return n.s(struct.unpack_from('<I', n.data, n.offsets[bi])[0])

def shape_map(n):
    m = {}
    for i in n.blocks_of('BSTriShape'):
        ts = n.trishape(i)
        if ts['skin'] < 0: continue
        m[ts['name']] = (i, ts)
    return m

def transplant_multi(donor_path, src_path, out_path):
    D = Nif(donor_path); S = Nif(src_path)
    footer_len = len(D.data) - D.end
    dm = shape_map(D); sm = shape_map(S)
    log = []
    for name, (si_, sts) in sm.items():
        if name not in dm:
            log.append('  source shape %r not in donor -> skipped' % name); continue
        di, dts = dm[name]
        dsi = D.skininstance(dts['skin']); ssi = S.skininstance(sts['skin'])
        dsd = D.skindata(dsi['data']); ssd = S.skindata(ssi['data'])
        dverts, dsp, _ = D.vertices(dsi['partition']); sverts, ssp, _ = S.vertices(ssi['partition'])
        assert dsp['nverts'] == ssp['nverts'] and dsp['vsize'] == ssp['vsize'] and dsp['vflags'] == ssp['vflags'], name
        uvd = max(max(abs(a-b) for a, b in zip(x['uv'], y['uv'])) for x, y in zip(dverts, sverts))
        assert uvd < 1e-6, (name, uvd)
        # T from shared bones (Spine2 preferred, else first shared)
        dnames = [bone_name(D, b) for b in dsi['bones']]; snames = [bone_name(S, b) for b in ssi['bones']]
        shared = [nm for nm in snames if nm in dnames]
        assert shared, name
        ref = 'NPC Spine2 [Spn2]' if 'NPC Spine2 [Spn2]' in shared else shared[0]
        xd = dsd['bones'][dnames.index(ref)]['xf']; xs = ssd['bones'][snames.index(ref)]['xf']
        Rd = xd[:9]; Rs = xs[:9]
        RtR = [sum(Rd[3*k+i]*Rs[3*k+j] for k in range(3)) for i in range(3) for j in range(3)]
        rot_dev = max(abs(RtR[i] - (1.0 if i in (0, 4, 8) else 0.0)) for i in range(9))
        assert rot_dev < 5e-3, (name, rot_dev)
        dt = [xs[9+i]-xd[9+i] for i in range(3)]
        T = tuple(sum(Rd[3*k+i]*dt[k] for k in range(3)) for i in range(3))
        # positions & bounds
        keep_offset = 28 if dsp['vsize'] >= 28 else dsp['vsize']
        # attribute prefix length: pos(16)+uv(4)+normal(4)+tangent(4) = 28 for vsize 40; for vsize 32/36 layouts recompute
        lay = D.vertex_layout(dsp['vflags'], dsp['vsize'])
        prefix = lay['weights'] if 'weights' in lay else dsp['vsize']
        dv = dsp['vdata_off']; sv = ssp['vdata_off']; vs = dsp['vsize']
        newpos = []
        for k in range(dsp['nverts']):
            srcb = bytes(S.data[sv + k*vs: sv + k*vs + prefix])
            x, y, z = struct.unpack_from('<3f', srcb, 0)
            x, y, z = x + T[0], y + T[1], z + T[2]
            newpos.append((x, y, z))
            D.data[dv + k*vs: dv + k*vs + prefix] = struct.pack('<3f', x, y, z) + srcb[12:prefix]
        xs_ = [p[0] for p in newpos]; ys_ = [p[1] for p in newpos]; zs_ = [p[2] for p in newpos]
        c = ((min(xs_)+max(xs_))/2, (min(ys_)+max(ys_))/2, (min(zs_)+max(zs_))/2)
        r = max(math.dist(p, c) for p in newpos)
        struct.pack_into('<4f', D.data, dts['bound_off'], c[0], c[1], c[2], r)
        log.append('  %r: %d verts, T=(%.2f,%.2f,%.2f), bound r=%.1f' % (name, len(newpos), T[0], T[1], T[2], r))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as fh:
        fh.write(bytes(D.data))
    V = Nif(out_path); assert len(V.data) - V.end == footer_len
    return log

B = [
    (r'HDT-SMP for Cloaks and Capes\meshes\clothes\volsCloaks\FluffyCloak_F.nif', r'Authoria - UBE Converter Output\meshes\!ube\clothes\volscloaks\fluffycloak_f.nif', r'meshes\!ube\clothes\volscloaks\fluffycloak_f.nif'),
    (r'HDT-SMP for Cloaks and Capes\meshes\clothes\volsCloaks\hoodedF_0.nif', r'Authoria - UBE Converter Output\meshes\!ube\clothes\volscloaks\hoodedf_0.nif', r'meshes\!ube\clothes\volscloaks\hoodedf_0.nif'),
    (r'HDT-SMP for Cloaks and Capes\meshes\clothes\volsCloaks\hoodedF_1.nif', r'Authoria - UBE Converter Output\meshes\!ube\clothes\volscloaks\hoodedf_1.nif', r'meshes\!ube\clothes\volscloaks\hoodedf_1.nif'),
]
for donor, src, rel in B:
    log = transplant_multi(os.path.join(MODS, donor), os.path.join(MODS, src), os.path.join(OUT, rel))
    print('B  %s' % rel); print('\n'.join(log))
print('built into', OUT)
