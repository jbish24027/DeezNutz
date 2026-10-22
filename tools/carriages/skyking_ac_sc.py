"""Authoria - Skyking Carriages - Over Outputs, SC Horses build (2026-10-17).
Same method as skyking_ac.py (left untouched), but the Animated Carriage carriages now come from
"Animated Carriage - SC Horses Patch" instead of the disabled "Animated Carriage - Witcher Horses":
  the 8 base meshes (carriage01/02/b01/b02 + _shadow) AND the 16 colour variants
  (_Appa/_Black/_Gray/_Palomino) that the SC patch's carriage activators point at.
1) Every shape on one of the four vanilla carriage materials (prisoner carriage atlas, Markarth wood, farmhouse wood
   wall, Riften canal planks) gets a byte copy of the matching Skyking material (shader block + texture set) from
   Skyking's own prisonercarriage01.nif. Geometry, UVs, nodes, controllers, the horse and harness shapes and every
   other block stay byte-identical; the shader keeps the target's own name string, vertex-colour bit and texset index.
   The 3 static carts from "Animated Carriage" are converted the same way as before.
2) Skyking's own vanilla carriage meshes + the Skyking Embers XD burnt cart, copied verbatim, also at the PG Patcher
   duplicate paths (unchanged COPIES list).
The 4 cart-horse meshes in clutter\\vicn\\cart\\horse\\ are NOT touched (the SC patch provides them).
Writes IN PLACE into the existing output folder (overwrites same-named files, never deletes, leaves meta.ini alone).
Usage: python -I skyking_ac_sc.py [--tmp <dir>] [--write]"""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nifmat import Doc, raw_types, tobytes_ordered, shader, texset, shapes
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WRITE = '--write' in sys.argv
TMPDIR = sys.argv[sys.argv.index('--tmp') + 1] if '--tmp' in sys.argv else os.path.dirname(os.path.abspath(__file__))
MODS = r'C:\1. AUTHORIA\mods'
DST = os.path.join(MODS, 'Authoria - Skyking Carriages - Over Outputs')
SK = os.path.join(MODS, 'Skyking Carriages')
SKE = os.path.join(MODS, 'Skyking Carriages - Embers XD Patch')
SCP = os.path.join(MODS, 'Animated Carriage - SC Horses Patch')
DONOR = os.path.join(SK, r'meshes\furniture\prisonercarriage\prisonercarriage01.nif')
DONOR_SHAPES = {'prisonercarriage01': 'FrontHorseCarriage01:3', 'mrkwood01': 'FrontHorseCarriage01:2',
                'woodwall01': 'PrisonerCarriage:0', 'riftencanalplanks01': 'PrisonerCarriage:1'}
VANILLA_TEX = {'prisonercarriage01': r'textures\furniture\prisonercarriage\prisonercarriage01.dds',
               'mrkwood01': r'textures\architecture\markarth\mrkwood01.dds',
               'woodwall01': r'textures\architecture\farmhouse\woodwall01.dds',
               'riftencanalplanks01': r'textures\architecture\riften\riftencanalplanks01.dds'}
VC_FLAG = 0x20
SC_NAMES = []
for base in ('carriage01', 'carriage02', 'carriageb01', 'carriageb02'):
    SC_NAMES += [base, base + '_shadow'] + [base + suf for suf in ('_Appa', '_Black', '_Gray', '_Palomino')]
AC_FILES = [(SCP, r'meshes\clutter\vicn\cart\%s.nif' % n, r'meshes\clutter\vicn\cart\%s.nif' % n) for n in SC_NAMES]
AC_FILES += [(os.path.join(MODS, 'Animated Carriage'), r'meshes\clutter\vicn\cart\%s.nif' % n,
              (r'meshes\clutter\vicn\cart\%s.nif' % n).lower())
             for n in (r'CartStatic\CartA', r'CartStatic\CartB', 'CartATEST')]
COPIES = [(SK, r'meshes\clutter\common\wagonwheel01.nif', None),
          (SK, r'meshes\clutter\quest\dbbrokencart01.nif', r'meshes\_pgpatcher_dups\1\clutter\quest\dbbrokencart01.nif'),
          (SK, r'meshes\furniture\cart\cartfurndriver01.nif', None),
          (SK, r'meshes\furniture\cart\cartfurnpassanger01.nif', None),
          (SK, r'meshes\furniture\cart\cartfurnstatic01.nif', r'meshes\_pgpatcher_dups\1\furniture\cart\cartfurnstatic01.nif'),
          (SK, r'meshes\furniture\prisonercarriage\prisonercarriage01.nif', None),
          (SK, r'meshes\furniture\prisonercarriage\prisonercarriage01static.nif', r'meshes\_pgpatcher_dups\1\furniture\prisonercarriage\prisonercarriage01static.nif'),
          (SK, r'meshes\furniture\prisonercarriage\prisonercarriagefurniture01.nif', None),
          (SKE, r'meshes\clutter\helgen\burntrubblecart01.nif', r'meshes\_pgpatcher_dups\1\clutter\helgen\burntrubblecart01.nif')]


def ci(path):
    """case-insensitive resolve of an existing path"""
    parts = path.split('\\'); cur = parts[0] + '\\'
    for p in parts[1:]:
        names = {n.lower(): n for n in os.listdir(cur)}
        cur = os.path.join(cur, names[p.lower()])
    return cur


# donor materials
ddoc = Doc(DONOR); dsh = {x['name']: x for x in shapes(ddoc)}
donor = {}
for mat, sn in DONOR_SHAPES.items():
    x = dsh[sn]; s = x['s']
    assert os.path.basename(x['tex0']).split('.')[0] == mat and s['ctrl'] == -1 and s['ne'] == 0
    donor[mat] = (bytes(ddoc.blocks[x['sh']][1]), bytes(ddoc.blocks[s['ts']][1]), s)
    print('donor %-20s stype=%d f1=%08X f2=%08X  %s' % (mat, s['stype'], s['f1'], s['f2'], x['tex'][0]))

written = []
for modroot, rel, outrel in AC_FILES:
    src = ci(os.path.join(modroot, rel)); raw = open(src, 'rb').read()
    assert os.path.basename(src) == os.path.basename(rel), 'filename case differs on disk: %s vs %s' % (src, rel)
    doc = Doc(src); types = raw_types(src)
    assert tobytes_ordered(doc, types) == raw, 'round-trip not byte-exact: ' + rel
    sh = shapes(doc)
    targets = [x for x in sh if x['tex0'] in VANILLA_TEX.values()]
    assert targets, 'no vanilla carriage material shapes in ' + rel
    mat_of = {x['idx']: [m for m, t in VANILLA_TEX.items() if t == x['tex0']][0] for x in targets}
    # shader / texset blocks must not be shared across materials or with non-targets
    owner_sh, owner_ts = {}, {}
    for x in targets:
        m = mat_of[x['idx']]
        assert owner_sh.setdefault(x['sh'], m) == m and owner_ts.setdefault(x['s']['ts'], m) == m, 'shared block across materials: ' + rel
    for x in sh:
        if x['idx'] not in mat_of:
            assert x['sh'] not in owner_sh and x['s']['ts'] not in owner_ts, 'block shared with non-target in ' + rel
    for x in targets:
        s = x['s']; ds = donor[mat_of[x['idx']]][2]
        assert s['ctrl'] == -1 and s['ne'] == 0, 'target has controller/extra data: ' + x['name']
        assert (s['f1'] & ~0x880) == (ds['f1'] & ~0x880), 'SLSF1 differs: %s %08X vs %08X' % (x['name'], s['f1'], ds['f1'])
        assert (s['f2'] & ~VC_FLAG) == (ds['f2'] & ~VC_FLAG), 'SLSF2 differs: %s %08X vs %08X' % (x['name'], s['f2'], ds['f2'])
    done_sh, done_ts = set(), set()
    for x in targets:
        m = mat_of[x['idx']]; dsb, dtb, ds = donor[m]
        if x['sh'] not in done_sh:
            nb = bytearray(dsb)
            struct.pack_into('<I', nb, 4, x['s']['name'])                         # keep the target's own name string
            struct.pack_into('<I', nb, ds['f1o'] + 4, (ds['f2'] & ~VC_FLAG) | (x['s']['f2'] & VC_FLAG))
            struct.pack_into('<i', nb, ds['tso'], x['s']['ts'])                   # keep the target's own texture-set block index
            doc.blocks[x['sh']][1] = nb; done_sh.add(x['sh'])
        if x['s']['ts'] not in done_ts:
            doc.blocks[x['s']['ts']][1] = bytearray(dtb); done_ts.add(x['s']['ts'])
    out = tobytes_ordered(doc, types)
    tmp = os.path.join(TMPDIR, '_sk_sc_tmp.nif'); open(tmp, 'wb').write(out)
    chk = Doc(tmp); os.remove(tmp); orig = Doc(src)
    assert len(chk.blocks) == len(orig.blocks) and chk.strings == orig.strings
    for i in range(len(orig.blocks)):
        if i in done_sh or i in done_ts: continue
        assert bytes(chk.blocks[i][1]) == bytes(orig.blocks[i][1]), 'block %d changed unexpectedly in %s' % (i, rel)
    conv = 0
    for x in shapes(chk):
        if x['idx'] in mat_of:
            assert x['tex0'].startswith('textures\\skyking\\carriage\\'), 'not converted: ' + x['name']
            conv += 1
    print('%-58s %2d of %2d shapes -> Skyking (%d shader + %d texset blocks), verified' % (rel, conv, len(sh), len(done_sh), len(done_ts)))
    written.append((outrel, out))

for modroot, rel, dup in COPIES:
    b = open(ci(os.path.join(modroot, rel)), 'rb').read()
    written.append((rel.lower(), b))
    if dup: written.append((dup.lower(), b))

print('%d files' % len(written))
if WRITE:
    if not os.path.isdir(DST): sys.exit('REFUSE: output folder missing (this build writes in place): ' + DST)
    for rel, b in written:
        p = os.path.join(DST, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(b)
    open(os.path.join(DST, 'README-skyking-carriages-over-outputs.txt'), 'wb').write((
        'Authoria - Skyking Carriages - Over Outputs (rebuilt 2026-10-17 from the SC Horses carriage patch; first built 2026-10-12)\r\n\r\n'
        'Sits where Authoria - Carriage PBR Wood Fix sat: directly above the PG outputs, enabled in every profile.\r\n'
        'Why: both PG outputs ship copies of every carriage mesh, so Skyking Carriages placed anywhere lower never shows.\r\n\r\n'
        '1. Animated Carriage meshes: the 24 carriages from "Animated Carriage - SC Horses Patch" (carriage01, carriage02,\r\n'
        '   carriageb01, carriageb02, each plain, _shadow, _Appa, _Black, _Gray and _Palomino; the coloured ones are what the\r\n'
        '   SC patch\'s carriage activators point at), plus CartA/CartB/CartATEST from "Animated Carriage" 1.2.1.\r\n'
        '   Every shape on the vanilla prisoner-carriage atlas, Markarth wood, farmhouse wood wall or Riften canal planks\r\n'
        '   now carries a byte copy of the matching Skyking material from Skyking\'s prisonercarriage01.nif\r\n'
        '   (EnvMap/complex-material shader + textures\\skyking\\carriage\\* d/n/m). Target name string and vertex-colour bit kept.\r\n'
        '   Everything else, including the SC horse and harness shapes, is byte-identical to the SC patch.\r\n'
        '   Wheels keep their own animated geometry (Skyking\'s high-poly wheels are not grafted).\r\n'
        '   The cart-horse meshes (clutter\\vicn\\cart\\horse\\) are not in this folder: the SC patch provides them.\r\n'
        '   Until 2026-10-17 part 1 was built from "Animated Carriage - Witcher Horses" (now disabled); that build is backed up\r\n'
        '   in _backups\\2026-10-17 - sc horses switch - skyking.\r\n'
        '2. Skyking Carriages 1.2 parallax meshes + the Skyking Embers XD patch burnt cart, verbatim, also at the PG duplicate paths.\r\n\r\n'
        'If the carriage horses change again (new horse mod meshes): rebuild part 1 from the new meshes.\r\n'
        'Scripts: _tools\\carriages\\skyking_ac_sc.py (this SC Horses build) and skyking_ac.py (the old Witcher build), nifrw toolkit.\r\n').encode('utf-8'))
    print('written to', DST)
