"""For each buried pair (static loose winner vs SMP source), extract the SMP source
(from BSA or loose), list shapes/verts/bones, and test topology equality per shape
so we know whether a geometry transplant is possible."""
import os, sys, json, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niflib import Nif
from bsa_audit import read_bsa_index, extract
from smp_audit import enabled_mods, INSTANCE, MODS

SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'donors')
os.makedirs(SCR, exist_ok=True)
MODLIST = enabled_mods()

def find_bsa(name):
    for m in MODLIST:
        p = os.path.join(MODS, m, name)
        if os.path.isfile(p): return p
    return None

PAIRS = [
    # (static winner mod, rel path, smp source: ('bsa', bsa name) or ('mod', mod name))
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmet_1.nif', ('bsa', 'Armors of the Velothi.bsa')),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\indoril wayfarer\helmetwithscarfm_1.nif', ('bsa', 'Armors of the Velothi.bsa')),
    ('Authoria - Bodyslide Output - HIMBO', r'meshes\pulcharmsolis\ashlander seer\bootsm_1.nif', ('bsa', 'Armors of the Velothi.bsa')),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlander seer\bootsf_1.nif', ('bsa', 'Armors of the Velothi.bsa')),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\camonnatong\steelglovesf_1.nif', ('bsa', 'Armors of the Velothi Pt2.bsa')),
    ('Authoria - Bodyslide Output - 3BA', r'meshes\pulcharmsolis\ashlanderwarrior\steelbodyf_1.nif', ('bsa', 'Armors of the Velothi Pt2.bsa')),
    ('Armors of the Velothi Pt. II - HIMBO', r'meshes\pulcharmsolis\ashlanderwarrior\fpm_1.nif', ('bsa', 'Armors of the Velothi Pt2.bsa')),
    ('Pig Iron Set - HIMBO Refit', r'meshes\pulcharmsolis\pigiron\m\fp_1.nif', ('bsa', 'PigIronSet.bsa')),
    ('Pig Iron Set - HIMBO Refit', r'meshes\pulcharmsolis\pigiron\m\fp_1.nif', ('mod', 'Pig Iron Set - Complex Material')),
    ('Authoria - Bodyslide Output - NSFW', r'meshes\weapons\vergi armoury\einarbow\dd - einar backpack_1.nif', ('mod', 'DD - Vergi Armoury by Vergi')),
    ('Authoria - Bodyslide Output - NSFW', r'meshes\weapons\vergi armoury\einarbow\dd - einar backpack_1.nif', ('mod', 'Authoria - Bodyslide Output - UBE')),
]

def get_source(rel, src):
    kind, name = src
    if kind == 'mod':
        return os.path.join(MODS, name, rel)
    bsa = find_bsa(name)
    idx, err = read_bsa_index(bsa)
    meta = idx[rel.lower()]
    data = extract(bsa, meta)
    out = os.path.join(SCR, name.replace(' ', '_') + '__' + rel.replace('\\', '__'))
    with open(out, 'wb') as fh: fh.write(data)
    return out

def bone_name(n, bi):
    return n.s(struct.unpack_from('<I', n.data, n.offsets[bi])[0])

def shapes(n):
    out = []
    for i in n.blocks_of('BSTriShape'):
        ts = n.trishape(i)
        if ts['skin'] < 0:
            out.append((ts['name'], None, ts['nverts'], None, None, ts)); continue
        si = n.skininstance(ts['skin'])
        verts, sp, lay = n.vertices(si['partition'])
        tris = []
        for p in sp['parts']:
            vm = p['vmap']; t = p['tris'] or []
            if p.get('tris_copy'):
                tris.extend(p['tris_copy'])          # SSE: shape-global indices
            elif vm and all(x < len(vm) for x in t):
                tris.extend([vm[x] for x in t])
            else:
                tris.extend(t)
        bones = [bone_name(n, b) for b in si['bones']]
        out.append((ts['name'], sp['nverts'], len(verts), sorted(tuple(tris[i:i+3]) for i in range(0, len(tris), 3)), [v['uv'] for v in verts], ts, bones, sp['vsize'], [v['pos'] for v in verts]))
    return out

def posdiff(a, b):
    import math
    d = [math.dist(x, y) for x, y in zip(a, b)]
    return (sum(d)/len(d), max(d)) if d else (0, 0)

def has_smp(n):
    for i in n.blocks_of('NiStringExtraData'):
        name_i, str_i = struct.unpack_from('<II', n.data, n.offsets[i])
        if n.s(name_i) == 'HDT Skinned Mesh Physics Object':
            return n.s(str_i)
    return None

for winner, rel, src in PAIRS:
    wpath = os.path.join(MODS, winner, rel)
    spath = get_source(rel, src)
    W = Nif(wpath); S = Nif(spath)
    print('=== %s\n    static winner: %s | SMP source: %s' % (rel, winner, src[1]))
    print('    source xml: %s ; winner xml: %s' % (has_smp(S), has_smp(W)))
    ws = shapes(W); ss = shapes(S)
    print('    winner shapes: %s' % [(x[0], x[2]) for x in ws])
    print('    source shapes: %s' % [(x[0], x[2]) for x in ss])
    # match by vertex count + tris + uv
    for s in ss:
        if s[0].lower().startswith('virtual'): continue
        cands = [w for w in ws if w[2] == s[2]]
        ok = []
        for w in cands:
            if w[3] is None or s[3] is None: continue
            same_t = w[3] == s[3]
            uvd = max(max(abs(a-b) for a, b in zip(x, y)) for x, y in zip(w[4], s[4])) if same_t else None
            pd = posdiff(w[8], s[8]) if same_t else None
            wb = set(w[6]); sb = set(s[6])
            ok.append(dict(winner_shape=w[0], same_tris=same_t, uvdiff=uvd, vsize_same=(w[7] == s[7]), posdiff_mean_max=pd,
                           bones_only_in_source=sorted(sb - wb), bones_only_in_winner=sorted(wb - sb)))
        nonstd = sorted(b for b in s[6] if not b.startswith('NPC ') and not b.startswith('CME '))
        print('    source shape %r (%s v, vsize %s, bones %d, non-NPC bones %s): candidates %s' % (s[0], s[2], s[7], len(s[6]), nonstd[:10], ok))
