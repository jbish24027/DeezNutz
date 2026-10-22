"""Find every file free_jaw deployed where a HAIR-type shape's weights changed
(they must follow the head and should never have been touched). Writes the
offending relative paths to redo_list.txt. Read-only."""
import os, sys, struct, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif
ex = {}
exec(open(os.path.join(SP, 'free_jaw.py')).read().split('bpos = np.array')[0]
     .replace("APPLY = '--apply' in sys.argv", "APPLY=False"), ex)
walk, skin_offset = ex['walk_partition'], ex['skin_offset']

MODS = r"C:/1. AUTHORIA/mods"
BK5 = r"C:/1. AUTHORIA/backups/neckbib5-20260801"
EXCL = re.compile(r'hair|wig|scalp|beard|brow|lash', re.I)

bad = []
n = 0
for dp, _d, fs in os.walk(BK5):
    for f in fs:
        if not f.lower().endswith('.nif'): continue
        prev = os.path.join(dp, f)
        rel = os.path.relpath(prev, BK5)
        live = os.path.join(MODS, rel)
        if not os.path.exists(live): continue
        n += 1
        try:
            a, b = Nif(prev), Nif(live)
        except Exception:
            continue
        for i in range(a.num_blocks):
            if a.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
            s = a.parse_shape(i)
            if s['skin_ref'] < 0 or not EXCL.search(s['name'] or ''): continue
            pl = walk(a, a.parse_skin_instance(s['skin_ref'])['partition_ref'])
            dso = skin_offset(pl['desc'], pl['dsize'], pl['vsize'],
                              a.btype(i) == 'BSDynamicTriShape')
            if dso is None or pl['vbuf_off'] is None: continue
            seg = slice(pl['vbuf_off'], pl['vbuf_off'] + pl['dsize'])
            if a.data[seg] != b.data[seg]:
                bad.append((rel, s['name'])); break
print('files compared: %d | hair-altered: %d' % (n, len(bad)))
seen = []
for rel, nm in bad:
    print('  %-92s %s' % (rel, nm))
    if rel not in seen: seen.append(rel)
out = os.path.join(SP, 'redo_list.txt')
with open(out, 'w', encoding='utf-8') as fh:
    for rel in seen: fh.write(rel + '\n')
    fh.write('FaceGeom\\SeranaMultiformNG.esp\n')     # skipped entirely, needs the redo too
print('redo list ->', out)
