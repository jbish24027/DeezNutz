"""Helga-style cloth rig on the converted Northern Folk dresses (3BA + UBE), reusing the 2026-10-18 robe SMP builder
(_tools\\robe-smp\\build_robes.py: 12-column grid under NPC Pelvis, cloth below the hip, sleeves stay on the arms,
invisible thigh/calf ring colliders sized from the matching body). Point positions are never changed, so the .tri
morph files written by the converters stay valid.
usage: python -I rig_dress.py <staged mods root> <out mods root>"""
import os, sys, json, xml.dom.minidom as md
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\robe-smp")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import build_robes as R
import importlib.util as _u
_sp = _u.spec_from_file_location('robe_make_xml', os.path.join(r'C:\1. AUTHORIA', '_tools', 'robe-smp', 'make_xml.py')); X = _u.module_from_spec(_sp); _sp.loader.exec_module(X)

XML = r"meshes\authoria cnf smp\hardanger dress f.xml"
F3BA_BODY = r"C:\1. AUTHORIA\mods\Authoria - Bodyslide Output - 3BA\meshes\actors\character\character assets\femalebody_%s.nif"
UBE_BODY = r"C:\1. AUTHORIA\mods\Authoria - Bodyslide Output - UBE\meshes\!UBE\Body\femalebody_tangent_%s.nif"
TARGETS = [
    ('f3ba', r"meshes\clothes\maidendressesofnorway\viking\Hardanger\Viking_Hardanger_black_f", ['BlackSmithTorso'], ('file', F3BA_BODY, None)),
    ('ube', r"meshes\!UBE\clothes\maidendressesofnorway\viking\Hardanger\Viking_Hardanger_black_f", ['BlackSmithTorso'], ('file', UBE_BODY, None)),
]

if __name__ == '__main__':
    stage, out = sys.argv[1], sys.argv[2]
    R.MODS = stage
    rep = []
    for mod, base, cloth, body in TARGETS:
        print('===', mod, base)
        rig, rows, r = R.build(os.path.join(out, mod), mod, base, cloth, body, XML, 'robe', print)
        rep += r
    X.SHAPES = {XML: (['BlackSmithTorso'], R.ROBE_ROWS, 'Northern Folk Hardanger dress')}
    bones = sorted({b for f in rep for b in f['bones'] if not b.startswith(R.PREFIX + '_')})
    text = X.xml_text(XML, bones); md.parseString(text.encode('utf-8'))
    for mod in ('f3ba', 'ube'):
        p = os.path.join(out, mod, XML); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8', newline='\r\n').write(text)
    json.dump(rep, open(os.path.join(out, 'rig_report.json'), 'w'), indent=1)
    print('xml bones', text.count('<bone name='), 'constraints', text.count('<generic-constraint bodyA='))
