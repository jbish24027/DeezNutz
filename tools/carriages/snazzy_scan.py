"""Scan the Snazzy Diverse Carriages source meshes (JS Knapsacks Patch): which shapes sit on which material.
Read-only. Usage: python -I snazzy_scan.py"""
import os, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nifmat import Doc, raw_types, tobytes_ordered, shapes
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SRC = r'C:\1. AUTHORIA\mods\Snazzy Diverse Carriages - JS Knapsacks Patch\meshes'
tex_use = collections.defaultdict(set)
for f in sorted(glob.glob(os.path.join(SRC, '**', '*.nif'), recursive=True)):
    raw = open(f, 'rb').read(); doc = Doc(f)
    rt = tobytes_ordered(doc, raw_types(f)) == raw
    rel = os.path.relpath(f, SRC)
    print('== %s  roundtrip=%s' % (rel, rt))
    for x in shapes(doc):
        s = x['s']
        if x['name'].lower().startswith(('carriage01', 'wheel', 'wagonwheel', 'leftseat', 'rightseat', 'object01', 'prisonercarriage', 'fronthorse', 'frontbar', 'signwhpost')):
            print('   %-24s st=%d f1=%08X f2=%08X ctrl=%d sh=%d ts=%d  %s | %s' % (
                x['name'], s['stype'], s['f1'], s['f2'], s['ctrl'], x['sh'], s['ts'], x['tex0'], (x['tex'][5] if len(x['tex']) > 5 else '')))
        tex_use[x['tex0']].add(x['name'])
print('\n--- every diffuse used ---')
for t, n in sorted(tex_use.items()):
    print('%-70s %s' % (t, ', '.join(sorted(n))[:150]))
