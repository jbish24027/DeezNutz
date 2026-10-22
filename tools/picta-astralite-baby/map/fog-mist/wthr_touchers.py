"""For a profile: list active plugins (in load order) that carry a top-level WTHR/VOLI/CLMT/REGN GRUP. Header walk only."""
import os, struct, sys, json
INST = "C:/1. AUTHORIA"
def resolve(profile):
    ml = [l.rstrip("\n") for l in open(f"{INST}/profiles/{profile}/modlist.txt", encoding="utf-8")]
    enabled = [l[1:] for l in ml if l.startswith("+")]
    idx = {}
    for n in reversed(enabled):  # lowest priority first, higher overwrite
        root = f"{INST}/mods/{n}"
        try:
            for e in os.listdir(root):
                if e.lower().endswith((".esp", ".esm", ".esl")):
                    idx[e.lower()] = (n, f"{root}/{e}")
        except Exception:
            pass
    data = f"{INST}/Stock Game/Data"
    for e in os.listdir(data):
        if e.lower().endswith((".esp", ".esm", ".esl")) and e.lower() not in idx:
            idx[e.lower()] = ("Data", f"{data}/{e}")
    return idx
def grups(path):
    out = set()
    with open(path, "rb") as f:
        hdr = f.read(24)
        sz = struct.unpack_from("<I", hdr, 4)[0]
        f.seek(24 + sz)
        while True:
            h = f.read(24)
            if len(h) < 24: break
            gsz = struct.unpack_from("<I", h, 4)[0]
            out.add(h[8:12].decode("latin1"))
            f.seek(gsz - 24, 1)
    return out
profile = sys.argv[1]
idx = resolve(profile)
lines = open(f"{INST}/profiles/{profile}/plugins.txt", encoding="utf-8", errors="replace").read().splitlines()
act = [l[1:] for l in lines if l.startswith("*")]
res = []
for i, p in enumerate(act):
    r = idx.get(p.lower())
    if not r: continue
    try:
        g = grups(r[1])
    except Exception as e:
        continue
    hit = sorted(g & {"WTHR", "VOLI", "CLMT", "REGN", "IMGS", "SPGD", "RFCT"})
    if hit:
        res.append((i, p, r[0], hit))
for row in res:
    print(row)
