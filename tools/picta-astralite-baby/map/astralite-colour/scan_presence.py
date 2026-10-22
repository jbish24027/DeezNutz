"""Read-only structural scan: per active plugin in a profile's load order, list the FormIDs (as
'OBJID:Master.esm') of records in top-level WTHR/REGN/CLMT/VOLI/IMGS/WRLD groups. Record headers only;
no record contents are interpreted here (contents come from houseCARL)."""
import os, struct, json, sys, zlib

ROOT = "C:/1. AUTHORIA"
PROF = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ - PBR"
OUT = os.path.dirname(os.path.abspath(__file__))
WANT = {b"WTHR", b"REGN", b"CLMT", b"VOLI", b"IMGS", b"WRLD"}

def read_lines(p):
    with open(p, "r", encoding="utf-8-sig", errors="replace") as f:
        return [l.rstrip("\r\n") for l in f]

mods = [l[1:] for l in read_lines(f"{ROOT}/profiles/{PROF}/modlist.txt") if l.startswith("+")]
mods.reverse()
plug_state = {}
for l in read_lines(f"{ROOT}/profiles/{PROF}/plugins.txt"):
    if l.startswith("#") or not l.strip():
        continue
    plug_state[l.lstrip("*").lower()] = l.startswith("*")

idx = {}
data = f"{ROOT}/Stock Game/Data"
for fn in os.listdir(data):
    if fn.lower().endswith((".esp", ".esm", ".esl")):
        idx[fn.lower()] = ("<Stock Game>", os.path.join(data, fn), fn)
for m in mods:
    d = f"{ROOT}/mods/{m}"
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if fn.lower().endswith((".esp", ".esm", ".esl")):
            idx[fn.lower()] = (m, os.path.join(d, fn), fn)

order = []
for l in read_lines(f"{ROOT}/profiles/{PROF}/loadorder.txt"):
    if l.startswith("#") or not l.strip():
        continue
    k = l.lower()
    st = plug_state.get(k)
    if st is None:
        # implicit master / CC: active if a file exists
        if k in idx:
            order.append(l)
    elif st:
        order.append(l)

def parse_header(buf):
    # TES4 record: subrecords include MAST
    masters = []
    pos = 0
    while pos < len(buf):
        t = buf[pos:pos+4]; sz = struct.unpack("<H", buf[pos+4:pos+6])[0]
        if t == b"MAST":
            masters.append(buf[pos+6:pos+6+sz].rstrip(b"\0").decode("latin-1"))
        pos += 6 + sz
    return masters

def scan(path, selfname):
    res = {}
    with open(path, "rb") as f:
        hdr = f.read(24)
        size = struct.unpack("<I", hdr[4:8])[0]
        flags = struct.unpack("<I", hdr[8:12])[0]
        body = f.read(size)
        masters = parse_header(body)
        while True:
            g = f.read(24)
            if len(g) < 24 or g[:4] != b"GRUP":
                break
            gsize = struct.unpack("<I", g[4:8])[0]
            label = g[8:12]
            if label not in WANT:
                f.seek(gsize - 24, 1)
                continue
            end = f.tell() + gsize - 24
            ids = []
            while f.tell() < end:
                h = f.read(24)
                if h[:4] == b"GRUP":
                    sz = struct.unpack("<I", h[4:8])[0]
                    f.seek(sz - 24, 1)  # skip child groups (WRLD children)
                    continue
                dsz = struct.unpack("<I", h[4:8])[0]
                rflags = struct.unpack("<I", h[8:12])[0]
                fid = struct.unpack("<I", h[12:16])[0]
                hi = fid >> 24
                owner = masters[hi] if hi < len(masters) else selfname
                ids.append(("%06X:%s" % (fid & 0xFFFFFF, owner), bool(rflags & 0x20)))
                f.seek(dsz, 1)
            res[label.decode()] = ids
            f.seek(end)
    return res, masters, flags

out = []
for i, name in enumerate(order):
    w = idx[name.lower()]
    res, masters, flags = scan(w[1], w[2])
    if res:
        out.append({"slot": i, "plugin": w[2], "mod": w[0], "esl": bool(flags & 0x200), "esm": bool(flags & 1),
                    "masters": masters, "records": {k: [x[0] for x in v] for k, v in res.items()},
                    "deleted": {k: [x[0] for x in v if x[1]] for k, v in res.items() if any(x[1] for x in v)}})
json.dump({"profile": PROF, "order": order, "plugins": out},
          open(os.path.join(OUT, f"presence_{PROF.replace(' ', '_')}.json"), "w"), indent=0)
print(len(order), "active;", len(out), "with weather-type groups")
for r in out:
    print(r["slot"], r["plugin"], {k: len(v) for k, v in r["records"].items()})
