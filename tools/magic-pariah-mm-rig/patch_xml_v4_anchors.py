"""One-off patch for make_xml_v4.py: in top_xml() declare BOTH sleeves' anchor rows before any
<bone-default>. A <bone> declared after a mass>0 default becomes a free dynamic body (no constraint
to the forearm) and falls to the ground - that was the sinking right sleeve (2026-09-06)."""
import io
p = r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig\make_xml_v4.py"
s = io.open(p, encoding='utf-8').read()
old = """    allcons = []
    for prefix, label in (('slvL', 'left sleeve'), ('slvR', 'right sleeve')):
        bones, cons, dyn = grid_section(prefix, SLEEVE_COLS, 5, label)
        L.append(bones); allcons.append(cons)
    L += allcons
"""
new = """    parts = [grid_section(prefix, SLEEVE_COLS, 5, label) for prefix, label in (('slvL', 'left sleeve'), ('slvR', 'right sleeve'))]
    # every anchor row (mass 0 = static, rides the forearm) MUST come before the first <bone-default>:
    # a <bone> declared after a mass>0 default becomes a free body and falls to the ground.
    for bones, cons, dyn in parts:
        L.append(bones[:bones.index('<bone-default>')].rstrip('\\t'))
    for bones, cons, dyn in parts:
        L.append('\\t' + bones[bones.index('<bone-default>'):])
    for bones, cons, dyn in parts:
        L.append(cons)
"""
assert old in s, 'top_xml assembly not found'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8').write(s)
print('make_xml_v4.py patched: sleeve anchors first')
