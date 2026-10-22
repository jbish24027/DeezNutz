"""Pre-flight for the BodySlide group + UBE converter run:
- every model path in Burlesque.esp and Magic Pariah.esp (MOD2..MOD5 subrecords)
- every BodySlide project's output path (duplicates = alternative builds)
- every ShapeData nif's HDT xml link, shapes and partitions
"""
import os, re, struct, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc, parse_shape_hdr, parse_dismember

SP = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8d6204d3-5065-49b7-8bd8-da1d0615990c\scratchpad"
BUR = SP + r"\mm"
MPM = r"C:\1. AUTHORIA\mods\Magic Pariah - Meadowlark Physics"


def esp_model_paths(path):
    d = open(path, 'rb').read()
    out = []
    for sig in (b'MOD2', b'MOD3', b'MOD4', b'MOD5', b'MODL'):
        for m in re.finditer(re.escape(sig), d):
            o = m.end()
            if o + 2 > len(d):
                continue
            ln = struct.unpack_from('<H', d, o)[0]
            s = d[o + 2:o + 2 + ln]
            if ln < 4 or ln > 200 or not s.endswith(b'\x00'):
                continue
            s = s[:-1]
            if not re.fullmatch(rb'[\x20-\x7e]+', s) or b'.nif' not in s.lower():
                continue
            out.append((sig.decode(), s.decode()))
    return out


for label, p in (("Burlesque", BUR + r"\Burlesque.esp"), ("Magic Pariah", MPM + r"\Magic Pariah.esp")):
    paths = esp_model_paths(p)
    print("== %s: %d model path subrecords" % (label, len(paths)))
    bad = [s for _, s in paths if s.lower().startswith('meshes')]
    uniq = sorted(set(s for _, s in paths), key=str.lower)
    for s in uniq:
        print("   ", s)
    print("   leading 'meshes\\' prefix (converter trap):", bad if bad else "none")

print()
rows = []
for d in (BUR + r"\CalienteTools\BodySlide\SliderSets", MPM + r"\CalienteTools\BodySlide\SliderSets"):
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith('.osp'):
            continue
        t = open(os.path.join(d, f), encoding='utf-8-sig').read()
        for m in re.finditer(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', t, re.S):
            name, body = m.group(1), m.group(2)
            op = re.search(r'<OutputPath>([^<]*)</OutputPath>', body)
            of = re.search(r'<OutputFile[^>]*>([^<]*)</OutputFile>', body)
            gw = re.search(r'GenWeights="(\w+)"', body)
            shapes = re.findall(r'<Shape target="([^"]+)"', body)
            rows.append((f, name, op.group(1) if op else '?', of.group(1) if of else '?',
                         gw.group(1) if gw else '?', shapes))
seen = {}
for f, name, op, of, gw, shapes in rows:
    key = (op.strip('\\/').lower() + '\\' + of.lower())
    seen.setdefault(key, []).append(name)
    print("%-42s set=%-32s out=%s\\%s  genweights=%s" % (f, name, op, of, gw))
    print("      shapes:", shapes)
print("--- shared output paths:")
for k, v in seen.items():
    if len(v) > 1:
        print("   ", k, "<-", v)
if not any(len(v) > 1 for v in seen.values()):
    print("    none")

print()
for base in (BUR + r"\CalienteTools\BodySlide\ShapeData", MPM + r"\CalienteTools\BodySlide\ShapeData"):
    for root, dirs, files in os.walk(base):
        for f in files:
            if not f.lower().endswith('.nif'):
                continue
            p = os.path.join(root, f)
            try:
                doc = Doc(p)
            except Exception as e:
                print("!! cannot parse", p, e); continue
            hdt = None
            for t, b in doc.blocks:
                if t == 'NiStringExtraData':
                    a, s = struct.unpack_from('<II', b, 0)
                    if doc.strings[a] == 'HDT Skinned Mesh Physics Object':
                        hdt = doc.strings[s]
            shp = []
            for i, (t, b) in enumerate(doc.blocks):
                if t == 'BSTriShape':
                    h = parse_shape_hdr(b)
                    parts = parse_dismember(doc.blocks[h['skin']][1])['parts'] if h['skin'] >= 0 and doc.blocks[h['skin']][0] == 'BSDismemberSkinInstance' else '-'
                    shp.append("%s%s" % (doc.name_of(i), [pp for _, pp in parts] if parts != '-' else ''))
            print("%-34s blocks=%-4d hdt=%s" % (f, len(doc.blocks), hdt))
            print("      ", shp)
