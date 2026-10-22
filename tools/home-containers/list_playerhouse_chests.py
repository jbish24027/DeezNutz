"""Read-only: every placed reference of the player-house safe-storage chest bases, anywhere in the load order.
Bases = every CONT whose EditorID contains 'playerhouse' (vanilla PlayerHouseChest 000F3923 and any mod/CC twins).
Output: playerhouse_chests.txt (ini form, grouped by cell, persistence tagged) and playerhouse_chests.csv
Usage: python list_playerhouse_chests.py ["profile name"]
"""
import os, struct, zlib, sys, time, csv
from collections import OrderedDict

INST = "C:/1. AUTHORIA"
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ - PBR"
OUT = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()


def read_lines(p):
    d = open(p, "rb").read().decode("utf-8-sig")
    return [l for l in d.replace("\r\n", "\n").split("\n") if l]


lo = [l for l in read_lines(INST + "/profiles/" + PROFILE + "/loadorder.txt") if not l.startswith("#")]
pl = [l for l in read_lines(INST + "/profiles/" + PROFILE + "/plugins.txt") if not l.startswith("#")]
active = set(l[1:].lower() for l in pl if l.startswith("*"))
implicit = {"skyrim.esm", "update.esm", "dawnguard.esm", "hearthfires.esm", "dragonborn.esm"}
plugins = [n for n in lo if n.lower() in active or n.lower() in implicit or (n.lower().startswith("cc") and n.lower().endswith((".esm", ".esl")))]
ml = read_lines(INST + "/profiles/" + PROFILE + "/modlist.txt")
mods_hi_first = [l[1:] for l in ml if l.startswith("+")]
sources = [INST + "/Stock Game/Data"] + [INST + "/mods/" + m for m in reversed(mods_hi_first)] + [INST + "/overwrite"]
vfs = {}
for s in sources:
    try:
        names = os.listdir(s)
    except FileNotFoundError:
        continue
    for n in names:
        if n.lower().endswith((".esm", ".esp", ".esl")):
            vfs[n.lower()] = s + "/" + n


def subrecords(body, stop_at=None):
    o = 0
    out = []
    big = None
    L = len(body)
    while o + 6 <= L:
        st = body[o:o + 4]
        sz = struct.unpack_from("<H", body, o + 4)[0]
        o += 6
        if st == b"XXXX":
            big = struct.unpack_from("<I", body, o)[0]
            o += sz
            continue
        if big is not None:
            sz = big
            big = None
        out.append((st, body[o:o + sz]))
        o += sz
        if stop_at and st == stop_at:
            break
    return out


def body_of(d, off, size, flags):
    b = d[off + 24:off + 24 + size]
    if flags & 0x40000:
        try:
            b = zlib.decompress(b[4:])
        except Exception:
            return b""
    return b


def zstr(b):
    return b.split(b"\0", 1)[0].decode("cp1252", "replace")


def masters_of(d):
    size = struct.unpack_from("<I", d, 4)[0]
    ms = [zstr(b).lower() for st, b in subrecords(d[24:24 + size]) if st == b"MAST"]
    return ms, 24 + size


def glob(fid, masters, me):
    i = fid >> 24
    return ((masters[i] if i < len(masters) else me), fid & 0xFFFFFF)


cell = {}
cont = {}


def pass1(d, me):
    masters, start = masters_of(d)

    def walk(off, end):
        while off < end:
            t = d[off:off + 4]
            if t == b"GRUP":
                gsize, label, gtype = struct.unpack_from("<IIi", d, off + 4)
                if (gtype == 0 and d[off + 8:off + 12] not in (b"CELL", b"CONT", b"WRLD")) or gtype in (6, 8, 9, 10):
                    off += gsize
                    continue
                walk(off + 24, off + gsize)
                off += gsize
            else:
                size, flags, fid = struct.unpack_from("<III", d, off + 4)
                if t in (b"CELL", b"CONT"):
                    gid = glob(fid, masters, me)
                    rec = {"edid": "", "full": "", "xown": None}
                    for st, b in subrecords(body_of(d, off, size, flags)):
                        if st == b"EDID":
                            rec["edid"] = zstr(b)
                        elif st == b"FULL":
                            rec["full"] = zstr(b)
                        elif st == b"XOWN":
                            rec["xown"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                    if t == b"CELL":
                        old = cell.get(gid)
                        if old:
                            for k in ("edid", "full"):
                                if not rec[k]:
                                    rec[k] = old[k]
                        cell[gid] = rec
                    else:
                        cont[gid] = rec
                off += 24 + size

    walk(start, len(d))


for n in plugins:
    p = vfs.get(n.lower())
    if p:
        pass1(open(p, "rb").read(), n.lower())
bases = {g: r for g, r in cont.items() if "playerhouse" in r["edid"].lower()}
print("pass1 %.0fs: cells %d, conts %d, player-house chest bases: %s" % (time.time() - T0, len(cell), len(cont), ", ".join("%s:%06X %s" % (g[0], g[1], r["edid"]) for g, r in sorted(bases.items()))))

refs = {}


def pass2(d, me):
    masters, start = masters_of(d)

    def walk(off, end, ctx):
        while off < end:
            t = d[off:off + 4]
            if t == b"GRUP":
                gsize, label, gtype = struct.unpack_from("<IIi", d, off + 4)
                if gtype == 0:
                    if d[off + 8:off + 12] in (b"CELL", b"WRLD"):
                        walk(off + 24, off + gsize, None)
                elif gtype in (6, 8, 9, 10):
                    walk(off + 24, off + gsize, (glob(label, masters, me), gtype))
                else:
                    walk(off + 24, off + gsize, ctx)
                off += gsize
            else:
                size, flags, fid = struct.unpack_from("<III", d, off + 4)
                if t == b"REFR" and ctx and not (flags & 0x20):
                    base = None
                    xown = None
                    xesp = False
                    subs = subrecords(body_of(d, off, size, flags))
                    for st, b in subs:
                        if st == b"NAME":
                            base = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                        elif st == b"XOWN":
                            xown = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                        elif st == b"XESP":
                            xesp = True
                    gid = glob(fid, masters, me)
                    if base in bases:
                        refs[gid] = {"cell": ctx[0], "group": ctx[1], "flags": flags, "base": base, "xown": xown, "xesp": xesp, "winner": me}
                    elif gid in refs:
                        del refs[gid]  # a later plugin re-based it to something else
                off += 24 + size

    walk(start, len(d), None)


for n in plugins:
    p = vfs.get(n.lower())
    if p:
        pass2(open(p, "rb").read(), n.lower())
print("pass2 %.0fs: player-house chest refs: %d" % (time.time() - T0, len(refs)))

PLAYERFACTION = ("skyrim.esm", 0x000DB1)
PLAYER = ("skyrim.esm", 0x000007)
orig = {n.lower(): n for n in plugins}
rows = []
for g, r in refs.items():
    c = cell.get(r["cell"], {"edid": "?", "full": "?", "xown": None})
    owner = r["xown"] or c["xown"]
    own = "none" if owner is None else "PlayerFaction" if owner == PLAYERFACTION else "Player" if owner == PLAYER else "OTHER %s:%06X" % owner
    rows.append({"cell_plugin": r["cell"][0], "cell_edid": c["edid"], "cell_name": c["full"],
                 "ref": "0x%06X~%s" % (g[1], orig.get(g[0], g[0])), "plugin_has_space": " " in orig.get(g[0], g[0]),
                 "base": bases[r["base"]]["edid"], "persistent": bool(r["group"] == 8 or (r["flags"] & 0x400)),
                 "disabled": bool(r["flags"] & 0x800), "enable_parent": r["xesp"], "owner": own, "winner": orig.get(r["winner"], r["winner"])})
rows.sort(key=lambda x: (x["cell_plugin"], x["cell_edid"], x["ref"]))
with open(OUT + "/playerhouse_chests.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
out = [";Player-house safe-storage chests (every reference of a *PlayerHouse* chest base), profile %s, %s" % (PROFILE, time.strftime("%Y-%m-%d")),
       ";[temporary] = the mod cannot reach it while that cell is unloaded until it is flagged persistent. [SPACES] = plugin name has spaces, cannot be linked."]
cur = None
for x in rows:
    key = (x["cell_plugin"], x["cell_edid"], x["cell_name"])
    if key != cur:
        cur = key
        out.append(";-- %s | %s | %s" % key)
    t = []
    if not x["persistent"]:
        t.append("temporary")
    if x["disabled"]:
        t.append("initially disabled" + (", enable parent" if x["enable_parent"] else ""))
    if x["owner"].startswith("OTHER"):
        t.append("owner " + x["owner"][6:])
    if x["plugin_has_space"]:
        t.append("SPACES")
    out.append("%s  ;%s in %s%s" % (x["ref"], x["base"], x["cell_name"] or x["cell_edid"], ("  [" + "; ".join(t) + "]") if t else ""))
open(OUT + "/playerhouse_chests.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
print("persistent %d / temporary %d / plugin with spaces %d" % (sum(x["persistent"] for x in rows), sum(not x["persistent"] for x in rows), sum(x["plugin_has_space"] for x in rows)))
