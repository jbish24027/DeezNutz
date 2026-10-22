import json, os
base = "C:/1. AUTHORIA/profiles"
def load(p):
    out=[]; act=set()
    with open(os.path.join(base,p,"plugins.txt"),encoding="utf-8-sig") as f:
        for ln in f:
            ln=ln.rstrip("\r\n")
            if not ln or ln.startswith("#"): continue
            a = ln.startswith("*")
            name = ln[1:] if a else ln
            out.append(name)
            if a: act.add(name.lower())
    return out, act
pbr, pbra = load("DEEZ CS NUTZ - PBR")
pic, pica = load("DEEZ CS NUTZ - PICTA")
only_pbr=[n for n in pbr if n.lower() in pbra and n.lower() not in pica]
only_pic=[n for n in pic if n.lower() in pica and n.lower() not in pbra]
print("PBR-only active:", len(only_pbr))
for n in only_pbr: print("  ", pbr.index(n)+1, n)
print("PICTA-only active:", len(only_pic))
for n in only_pic: print("  ", pic.index(n)+1, n)
out = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing/lanediff.json"
json.dump({"pbr_order":pbr,"pbr_active":sorted(pbra),"pic_order":pic,"pic_active":sorted(pica),"only_pbr":only_pbr,"only_pic":only_pic},open(out,"w"),indent=1)
