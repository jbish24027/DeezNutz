"""Read-only: for profile PBR, resolve each active plugin to its winning file, then list
top-level GRUP labels (record types) and record counts for weather-relevant types."""
import os, struct, json, sys

ROOT = "C:/1. AUTHORIA"
PROF = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ - PBR"
OUT = os.path.dirname(os.path.abspath(__file__))
TYPES = {b"WTHR", b"REGN", b"CLMT", b"VOLI", b"IMGS", b"LGTM", b"WRLD", b"GLOB", b"LTEX"}

def read_lines(p):
    with open(p, "r", encoding="utf-8-sig", errors="replace") as f:
        return [l.rstrip("\r\n") for l in f]

mods = []  # priority low->high
for l in read_lines(f"{ROOT}/profiles/{PROF}/modlist.txt"):
    if l.startswith("+"):
        mods.append(l[1:])
mods.reverse()  # modlist top = highest priority; reversed => low..high

plugins = []
for l in read_lines(f"{ROOT}/profiles/{PROF}/plugins.txt"):
    if l.startswith("#") or not l.strip():
        continue
    act = l.startswith("*")
    plugins.append((l.lstrip("*"), act))

# file index: lowercase name -> winning path
idx = {}
data = f"{ROOT}/Stock Game/Data"
for fn in os.listdir(data):
    idx[fn.lower()] = ("<Stock Game>", os.path.join(data, fn))
for m in mods:
    d = f"{ROOT}/mods/{m}"
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if fn.lower().endswith((".esp", ".esm", ".esl")):
            idx[fn.lower()] = (m, os.path.join(d, fn))

def top_groups(path):
    res = {}
    with open(path, "rb") as f:
        hdr = f.read(24)
        if hdr[:4] != b"TES4":
            return None, None
        size = struct.unpack("<I", hdr[4:8])[0]
        flags = struct.unpack("<I", hdr[8:12])[0]
        f.seek(24 + size)
        while True:
            g = f.read(24)
            if len(g) < 24:
                break
            if g[:4] != b"GRUP":
                break
            gsize = struct.unpack("<I", g[4:8])[0]
            label = g[8:12]
            res[label.decode("latin-1")] = gsize
            f.seek(gsize - 24, 1)
    return res, flags

out = []
order = 0
for name, act in plugins:
    if not act:
        continue
    w = idx.get(name.lower())
    if not w:
        out.append({"order": order, "plugin": name, "mod": None, "groups": None})
        order += 1
        continue
    groups, flags = top_groups(w[1])
    hit = {k: v for k, v in (groups or {}).items() if k.encode() in TYPES}
    out.append({"order": order, "plugin": name, "mod": w[0], "esl": bool(flags & 0x200) if flags is not None else None,
                "esm": bool(flags & 1) if flags is not None else None, "groups": hit})
    order += 1

with open(os.path.join(OUT, f"groups_{PROF.replace(' ', '_')}.json"), "w") as f:
    json.dump(out, f, indent=1)
for r in out:
    g = r["groups"] or {}
    keys = [k for k in g if k in ("WTHR", "REGN", "CLMT", "VOLI", "IMGS", "LGTM")]
    if keys:
        print(r["order"], r["plugin"], "|", r["mod"], "|", {k: g[k] for k in keys})
print("active", order)
