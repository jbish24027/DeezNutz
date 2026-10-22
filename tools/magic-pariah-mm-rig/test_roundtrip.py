import sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc, rebuild, reachable, slots

SP = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8d6204d3-5065-49b7-8bd8-da1d0615990c\scratchpad"
FILES = [
    SP + r"\mp\Magic Pariah\CalienteTools\BodySlide\ShapeData\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif",
    SP + r"\mm\Meandering Meadowlark 3BA\CalienteTools\BodySlide\ShapeData\Meandering Meadowlark Dress 3BA\Meandering Meadowlark Dress 3BA.nif",
    SP + r"\mp\Magic Pariah\CalienteTools\BodySlide\ShapeData\Magic Pariah Top\Magic Pariah Top.nif",
]
ok_all = True
for p in FILES:
    raw = open(p, 'rb').read()
    doc = Doc(p)
    out = doc.tobytes()
    print(p.split('\\')[-1], '| blocks', len(doc.blocks), '| strings', len(doc.strings),
          '| roots', doc.roots, '| export', doc.export_info)
    same = out == raw
    print('  identity round-trip byte-exact:', same, len(raw), len(out))
    ok_all &= same
    for i, (t, b) in enumerate(doc.blocks):
        slots(t, b)
    reach = reachable(doc)
    unreach = sorted(set(range(len(doc.blocks))) - reach)
    print('  reachable', len(reach), 'of', len(doc.blocks), '| unreachable:', unreach[:10])
    nd, m = rebuild(doc)
    out2 = nd.tobytes()
    same2 = out2 == raw
    print('  rebuild(all) byte-exact:', same2, '| strings kept', len(nd.strings), 'of', len(doc.strings))
    if not same2:
        k = next((i for i in range(min(len(raw), len(out2))) if raw[i] != out2[i]), None)
        print('   first diff at', k, raw[k - 8:k + 8] if k is not None else '', out2[k - 8:k + 8] if k is not None else '')
print('ALL IDENTITY OK' if ok_all else 'IDENTITY FAILED')
