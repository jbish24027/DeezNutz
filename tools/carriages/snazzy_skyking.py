"""Snazzy Diverse Carriages carts -> Skyking wood and metal (2026-10-18). Adds to "Authoria - Skyking Carriages - Over Outputs".
Source: the 22 GM_cartfurnstatic01* meshes from "Snazzy Diverse Carriages - JS Knapsacks Patch" (the last NON-generated
provider; the PG outputs ship copies, which this folder beats). Same graft as skyking_ac_sc.py:
  cart-body shapes get a byte copy of the matching Skyking material (shader block + texture set) from Skyking's own
  prisonercarriage01.nif. Mapping by the vanilla cart's shape names (the Snazzy carts are the vanilla CartFurnStatic01
  body with other wood textures):
    Carriage01:0, LeftSeat01:0, RightSeat01:0          -> Skyking woodwall01
    Carriage01:1                                       -> Skyking riftencanalplanks01
    Carriage01:2, Carriage01:2.001, Left/RightSeat01:2 -> Skyking mrkwood01
    every shape on Snazzy's gm_prisonercarriage01 atlas (body, nails, leather, seat irons, wheel) -> Skyking atlas
  Kept from the target: its name string, texture-set block index, and the vertex-colour / double-sided / vertex-alpha /
  skinned bits. Everything else (SMIM metalwork, rings, sacks, lanterns, canopies, all clutter, geometry) byte-identical.
Writes the same bytes at the PG Patcher duplicate paths PG_1.esp points the _Snow / _SnowLight records at.
Usage: python -I snazzy_skyking.py [--out <dir>]   (default: a dry run that builds and verifies only)"""
import os, sys, struct, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nifmat import Doc, raw_types, tobytes_ordered, shapes
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
MODS = r'C:\1. AUTHORIA\mods'
SRC = os.path.join(MODS, r'Snazzy Diverse Carriages - JS Knapsacks Patch\meshes\furniture\cart')
DONOR = os.path.join(MODS, r'Skyking Carriages\meshes\furniture\prisonercarriage\prisonercarriage01.nif')
DONOR_SHAPES = {'prisonercarriage01': 'FrontHorseCarriage01:3', 'mrkwood01': 'FrontHorseCarriage01:2',
                'woodwall01': 'PrisonerCarriage:0', 'riftencanalplanks01': 'PrisonerCarriage:1'}
BY_NAME = {'carriage01:0': 'woodwall01', 'leftseat01:0': 'woodwall01', 'rightseat01:0': 'woodwall01',
           'carriage01:1': 'riftencanalplanks01',
           'carriage01:2': 'mrkwood01', 'carriage01:2.001': 'mrkwood01', 'leftseat01:2': 'mrkwood01', 'rightseat01:2': 'mrkwood01'}
ATLAS = r'textures\furniture\prisonercarriage\gm_prisonercarriage01.dds'
DUPS = ['gm_cartfurnstatic01a_covered02', 'gm_cartfurnstatic01b_cc', 'gm_cartfurnstatic01b_covered02', 'gm_cartfurnstatic01c',
        'gm_cartfurnstatic01c_cc', 'gm_cartfurnstatic01c_covered02', 'gm_cartfurnstatic01d', 'gm_cartfurnstatic01d_covered02']
KEEP1 = 0x2 | 0x8          # SLSF1 Skinned, Vertex_Alpha
KEEP2 = 0x20 | 0x10        # SLSF2 Vertex_Colors, Double_Sided

ddoc = Doc(DONOR); dsh = {x['name']: x for x in shapes(ddoc)}
donor = {}
for mat, sn in DONOR_SHAPES.items():
    x = dsh[sn]; s = x['s']
    assert os.path.basename(x['tex0']).split('.')[0] == mat and s['ctrl'] == -1 and s['ne'] == 0
    donor[mat] = (bytes(ddoc.blocks[x['sh']][1]), bytes(ddoc.blocks[s['ts']][1]), s)

written = []
files = sorted(glob.glob(os.path.join(SRC, 'GM_cartfurnstatic01*.nif')))
assert len(files) == 22, len(files)
for src in files:
    raw = open(src, 'rb').read(); doc = Doc(src); types = raw_types(src)
    assert tobytes_ordered(doc, types) == raw, 'round-trip not byte-exact: ' + src
    sh = shapes(doc)
    mat_of = {}
    for x in sh:
        m = BY_NAME.get(x['name'].lower())
        if x['tex0'] == ATLAS: m = 'prisonercarriage01'
        if m: mat_of[x['idx']] = m
    assert mat_of, 'no cart-body shapes in ' + src
    owner_sh, owner_ts = {}, {}
    for x in sh:
        if x['idx'] in mat_of:
            m = mat_of[x['idx']]
            assert owner_sh.setdefault(x['sh'], m) == m and owner_ts.setdefault(x['s']['ts'], m) == m, 'shared block across materials: ' + src
    for x in sh:
        if x['idx'] not in mat_of:
            assert x['sh'] not in owner_sh and x['s']['ts'] not in owner_ts, 'block shared with non-target %s in %s' % (x['name'], src)
    done_sh, done_ts = set(), set()
    for x in sh:
        if x['idx'] not in mat_of: continue
        s = x['s']; dsb, dtb, ds = donor[mat_of[x['idx']]]
        assert s['ctrl'] == -1 and s['ne'] == 0, 'target has controller/extra data: ' + x['name']
        if x['sh'] not in done_sh:
            nb = bytearray(dsb)
            struct.pack_into('<I', nb, 4, s['name'])
            struct.pack_into('<II', nb, ds['f1o'], (ds['f1'] & ~KEEP1) | (s['f1'] & KEEP1), (ds['f2'] & ~KEEP2) | (s['f2'] & KEEP2))
            struct.pack_into('<i', nb, ds['tso'], s['ts'])
            doc.blocks[x['sh']][1] = nb; done_sh.add(x['sh'])
        if s['ts'] not in done_ts:
            doc.blocks[s['ts']][1] = bytearray(dtb); done_ts.add(s['ts'])
    out = tobytes_ordered(doc, types)
    tmp = os.path.join(os.environ.get('TEMP', '.'), '_snazzy_sk_tmp.nif'); open(tmp, 'wb').write(out)
    chk = Doc(tmp); os.remove(tmp); orig = Doc(src)
    assert len(chk.blocks) == len(orig.blocks) and chk.strings == orig.strings
    for i in range(len(orig.blocks)):
        if i in done_sh or i in done_ts: continue
        assert bytes(chk.blocks[i][1]) == bytes(orig.blocks[i][1]), 'block %d changed unexpectedly in %s' % (i, src)
    names = []
    for x in shapes(chk):
        if x['idx'] in mat_of:
            assert x['tex0'] == ('textures\\skyking\\carriage\\%s.dds' % mat_of[x['idx']]), 'not converted: ' + x['name']
            names.append(x['name'])
    left = sorted(set(x['tex0'] for x in shapes(chk) if x['idx'] not in mat_of and ('architecture' in x['tex0'] or 'prisonercarriage' in x['tex0'])))
    stem = os.path.basename(src)[:-4].lower()
    print('%-38s %2d shapes -> Skyking  | other wood/metal kept: %s' % (stem, len(names), ', '.join(os.path.basename(t) for t in left) or '-'))
    written.append((r'meshes\furniture\cart\%s.nif' % stem, out))
    if stem in DUPS: written.append((r'meshes\_pgpatcher_dups\1\furniture\cart\%s.nif' % stem, out))

print('%d files built' % len(written))
if OUT:
    for rel, b in written:
        p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(b)
    print('written to', OUT)
