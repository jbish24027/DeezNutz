"""Read-only scan: every container reference inside every player-home cell of an MO2 profile.

Player home = a cell whose location (or a parent location) carries LocTypePlayerHouse,
or a cell owned by PlayerFaction / the Player.
Outputs, next to this script:
  home_containers_report.md     per-home summary
  home_containers_refs.csv      every container reference with persistence / ownership / plugin-name check
  permalinks_candidates.txt     the refs in the 0xID~Plugin form the Crafting Pulls ini needs (LotD cells excluded)
Usage: python scan_home_containers.py ["profile name"]
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


def is_active(n):
    nl = n.lower()
    return nl in active or nl in implicit or (nl.startswith("cc") and nl.endswith((".esm", ".esl")))


plugins = [n for n in lo if is_active(n)]

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
        nl = n.lower()
        if nl.endswith((".esm", ".esp", ".esl")):
            vfs[nl] = s + "/" + n
print("active plugins:", len(plugins), "| vfs plugin files:", len(vfs))


def subrecords(body):
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
    ms = []
    for st, b in subrecords(d[24:24 + size]):
        if st == b"MAST":
            ms.append(zstr(b).lower())
    return ms, 24 + size


def glob(fid, masters, me):
    i = fid >> 24
    return ((masters[i] if i < len(masters) else me), fid & 0xFFFFFF)


# ---------------- pass 1: KYWD, LCTN, CELL, CONT (winner = last plugin in load order)
kywd = {}
lctn = {}
cell = {}
cont = {}


def pass1(d, me):
    masters, start = masters_of(d)

    def walk(off, end):
        while off < end:
            t = d[off:off + 4]
            if t == b"GRUP":
                gsize, label, gtype = struct.unpack_from("<IIi", d, off + 4)
                if gtype == 0 and d[off + 8:off + 12] not in (b"KYWD", b"LCTN", b"CELL", b"CONT", b"WRLD"):
                    off += gsize
                    continue
                if gtype in (6, 8, 9, 10):  # cell children hold no CELL/KYWD/LCTN/CONT records
                    off += gsize
                    continue
                walk(off + 24, off + gsize)
                off += gsize
            else:
                size, flags, fid = struct.unpack_from("<III", d, off + 4)
                if t in (b"KYWD", b"LCTN", b"CELL", b"CONT"):
                    gid = glob(fid, masters, me)
                    subs = subrecords(body_of(d, off, size, flags))
                    if t == b"KYWD":
                        for st, b in subs:
                            if st == b"EDID":
                                kywd[gid] = zstr(b)
                    elif t == b"LCTN":
                        rec = {"edid": "", "full": "", "kw": [], "parent": None}
                        for st, b in subs:
                            if st == b"EDID":
                                rec["edid"] = zstr(b)
                            elif st == b"FULL":
                                rec["full"] = zstr(b)
                            elif st == b"KWDA":
                                rec["kw"] = [glob(x, masters, me) for x in struct.unpack_from("<%dI" % (len(b) // 4), b, 0)]
                            elif st == b"PNAM":
                                rec["parent"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                        lctn[gid] = rec
                    elif t == b"CELL":
                        rec = {"edid": "", "full": "", "xown": None, "xlcn": None, "interior": None, "winner": me}
                        for st, b in subs:
                            if st == b"EDID":
                                rec["edid"] = zstr(b)
                            elif st == b"FULL":
                                rec["full"] = zstr(b)
                            elif st == b"XOWN":
                                rec["xown"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                            elif st == b"XLCN":
                                rec["xlcn"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                            elif st == b"DATA":
                                rec["interior"] = bool(b[0] & 1)
                        old = cell.get(gid)
                        if old:
                            for k in ("edid", "full"):
                                if not rec[k]:
                                    rec[k] = old[k]
                            if rec["interior"] is None:
                                rec["interior"] = old["interior"]
                        cell[gid] = rec
                    elif t == b"CONT":
                        rec = {"edid": "", "full": "", "respawn": False}
                        for st, b in subs:
                            if st == b"EDID":
                                rec["edid"] = zstr(b)
                            elif st == b"FULL":
                                rec["full"] = zstr(b)
                            elif st == b"DATA":
                                rec["respawn"] = bool(b[0] & 2)
                        cont[gid] = rec
                off += 24 + size

    walk(start, len(d))


# ---------------- pass 2: REFR records inside home cells (winner = last plugin in load order)
refs = {}


def pass2(d, me, homes):
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
                    cg = glob(label, masters, me)
                    if cg in homes:
                        walk(off + 24, off + gsize, (cg, gtype))
                else:
                    walk(off + 24, off + gsize, ctx)
                off += gsize
            else:
                size, flags, fid = struct.unpack_from("<III", d, off + 4)
                if t == b"REFR" and ctx:
                    gid = glob(fid, masters, me)
                    rec = {"cell": ctx[0], "group": ctx[1], "flags": flags, "base": None, "xown": None, "xesp": None, "winner": me}
                    if not (flags & 0x20):
                        for st, b in subrecords(body_of(d, off, size, flags)):
                            if st == b"NAME":
                                rec["base"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                            elif st == b"XOWN":
                                rec["xown"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                            elif st == b"XESP":
                                rec["xesp"] = glob(struct.unpack_from("<I", b, 0)[0], masters, me)
                    old = refs.get(gid)
                    if old and rec["base"] is None:
                        rec["base"] = old["base"]
                    refs[gid] = rec
                off += 24 + size

    walk(start, len(d), None)


missing = []
for n in plugins:
    p = vfs.get(n.lower())
    if not p:
        missing.append(n)
        continue
    d = open(p, "rb").read()
    try:
        pass1(d, n.lower())
    except Exception as ex:
        print("pass1 FAIL", n, ex)
print("pass1 done %.0fs: kywd %d lctn %d cell %d cont %d; plugin files not found: %s" % (time.time() - T0, len(kywd), len(lctn), len(cell), len(cont), missing))

PLAYERFACTION = ("skyrim.esm", 0x000DB1)
PLAYER = ("skyrim.esm", 0x000007)
lth = [g for g, e in kywd.items() if e.lower() == "loctypeplayerhouse"]
print("LocTypePlayerHouse:", lth)


def loc_is_home(g, depth=0):
    r = lctn.get(g)
    if not r or depth > 4:
        return False
    if any(k in lth for k in r["kw"]):
        return True
    return loc_is_home(r["parent"], depth + 1) if r["parent"] else False


homes = {}
for g, c in cell.items():
    why = []
    if c["xlcn"] and loc_is_home(c["xlcn"]):
        why.append("LocTypePlayerHouse")
    if c["xown"] == PLAYERFACTION:
        why.append("owner=PlayerFaction")
    elif c["xown"] == PLAYER:
        why.append("owner=Player")
    if why:
        homes[g] = why
print("home cells:", len(homes))

for n in plugins:
    p = vfs.get(n.lower())
    if not p:
        continue
    d = open(p, "rb").read()
    try:
        pass2(d, n.lower(), homes)
    except Exception as ex:
        print("pass2 FAIL", n, ex)
print("pass2 done %.0fs: refs in home cells %d" % (time.time() - T0, len(refs)))

# ---------------- evaluate
orig_case = {n.lower(): n for n in plugins}


def fmt(g):
    return "0x%06X~%s" % (g[1], orig_case.get(g[0], g[0]))


def name_of(g):
    if g in cont:
        return cont[g]["edid"] or cont[g]["full"]
    if g in lctn:
        return lctn[g]["edid"]
    if g == PLAYERFACTION:
        return "PlayerFaction"
    if g == PLAYER:
        return "Player"
    return "%s:%06X" % (g[0], g[1]) if g else ""


def category(edid, full):
    s = (edid + " " + full).lower()
    if any(k in s for k in ("displaycase", "display case", "bookshelf", "book shelf", "bookcase", "weaponrack", "mannequin", "plaque", "shelf")):
        return "display"
    if any(k in s for k in ("barrel", "sack", "satchel", "knapsack", "basket", "crate", "urn", "pot", "bucket", "pouch", "bag", "cask", "keg", "jar")):
        return "loose"
    if any(k in s for k in ("chest", "strongbox", "strong box", "safe", "lockbox", "coffer", "trunk", "cache", "vault", "storage")):
        return "chest"
    if any(k in s for k in ("cupboard", "wardrobe", "dresser", "end table", "endtable", "nightstand", "night stand", "drawer", "cabinet", "desk", "table", "counter", "cart", "icebox", "box", "closet", "armoire", "hutch")):
        return "furniture"
    return "other"


rows = []
for g, r in refs.items():
    if r["flags"] & 0x20:
        continue
    if r["base"] not in cont:
        continue
    c = cell[r["cell"]]
    owner = r["xown"] or c["xown"]
    if owner is None:
        own = "none"
    elif owner == PLAYERFACTION:
        own = "PlayerFaction"
    elif owner == PLAYER:
        own = "Player"
    else:
        own = "OTHER:" + name_of(owner)
    b = cont[r["base"]]
    rows.append({
        "cell_edid": c["edid"], "cell_name": c["full"], "cell_plugin": r["cell"][0], "cell_why": "+".join(homes[r["cell"]]),
        "ref": fmt(g), "defined_in": orig_case.get(g[0], g[0]), "plugin_has_space": " " in orig_case.get(g[0], g[0]),
        "base_edid": b["edid"], "base_name": b["full"], "respawns": b["respawn"],
        "persistent": bool(r["group"] == 8 or (r["flags"] & 0x400)), "disabled": bool(r["flags"] & 0x800),
        "enable_parent": bool(r.get("xesp")), "category": category(b["edid"], b["full"]),
        "owner": own, "winner": orig_case.get(r["winner"], r["winner"]), "interior": c["interior"],
    })
rows.sort(key=lambda x: (x["cell_plugin"], x["cell_edid"], x["ref"]))
with open(OUT + "/home_containers_refs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

per = OrderedDict()
for x in rows:
    k = (x["cell_plugin"], x["cell_edid"], x["cell_name"], x["cell_why"], x["interior"])
    s = per.setdefault(k, {"n": 0, "pers": 0, "space": 0, "disabled": 0, "resp": 0, "other": 0})
    s["n"] += 1
    s["pers"] += x["persistent"]
    s["space"] += x["plugin_has_space"]
    s["disabled"] += x["disabled"]
    s["resp"] += x["respawns"]
    s["other"] += x["owner"].startswith("OTHER")
lines = ["# Player-home container references - profile %s - %s" % (PROFILE, time.strftime("%Y-%m-%d %H:%M")), "",
         "Home cells found: %d (with at least one container: %d). Container refs: %d. Full list: home_containers_refs.csv" % (len(homes), len(per), len(rows)), "",
         "| Plugin | Cell | Name | Why home | Int | Containers | Persistent | Plugin has space | Disabled | Respawning | Other owner |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
for k, s in per.items():
    lines.append("| %s | %s | %s | %s | %s | %d | %d | %d | %d | %d | %d |" % (k[0], k[1], k[2], k[3], "yes" if k[4] else "no", s["n"], s["pers"], s["space"], s["disabled"], s["resp"], s["other"]))
with_cont = set((x["cell_plugin"], x["cell_edid"]) for x in rows)
empties = [(g, cell[g]) for g in homes if (g[0], cell[g]["edid"]) not in with_cont]
lines += ["", "Home cells with no container: %d" % len(empties)] + ["- %s %s %s (%s)" % (g[0], c["edid"], c["full"], "+".join(homes[g])) for g, c in sorted(empties)]
open(OUT + "/home_containers_report.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

cand = [";Player-home container permalinks, generated %s from profile %s" % (time.strftime("%Y-%m-%d"), PROFILE),
        ";Only references whose defining plugin has no space in its name can be linked (the mod's parser strips spaces).",
        ";Legacy of the Dragonborn cells are left out (covered by the LotD ini).",
        ";[temporary] = not persistent as shipped: the mod cannot reach it while you are away from that home."]
def tags(x):
    t = []
    if not x["persistent"]:
        t.append("temporary")
    if x["disabled"]:
        t.append("initially disabled" + (", enable parent" if x["enable_parent"] else ""))
    if x["respawns"]:
        t.append("respawns")
    if x["owner"].startswith("OTHER"):
        t.append("owner " + x["owner"][6:])
    return ("  [" + "; ".join(t) + "]") if t else ""


def emit(path, header, selected):
    out = list(header)
    cur = None
    for x in selected:
        key = (x["cell_plugin"], x["cell_edid"], x["cell_name"])
        if key != cur:
            cur = key
            n = sum(1 for y in selected if (y["cell_plugin"], y["cell_edid"]) == key[:2])
            p = sum(1 for y in selected if (y["cell_plugin"], y["cell_edid"]) == key[:2] and y["persistent"])
            out.append(";-- %s | %s | %s  (%d containers, %d persistent)" % (key + (n, p)))
        out.append("%s  ;%s [%s]%s" % (x["ref"], x["base_name"] or x["base_edid"], x["category"], tags(x)))
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")


linkable = [x for x in rows if not x["plugin_has_space"] and x["cell_plugin"] != "legacyofthedragonborn.esm"]
emit(OUT + "/permalinks_candidates.txt", cand, linkable)

REC = {("skyrim.esm", "WhiterunBreezehome"), ("skyrim.esm", "RiftenHoneyside"), ("skyrim.esm", "MarkarthVlindrelHall"),
       ("skyrim.esm", "WindhelmHjerim"), ("skyrim.esm", "SolitudeProudspireManor"), ("skyrim.esm", "WinterholdCollegeArchMageQuarters"),
       ("hearthfires.esm", "BYOHHouse1Falkreath"), ("hearthfires.esm", "BYOHHouse1FalkreathBasement"),
       ("hearthfires.esm", "BYOHHouse2Hjaalmarch"), ("hearthfires.esm", "BYOHHouse2HjaalmarchBasement"),
       ("hearthfires.esm", "BYOHHouse3Pale"), ("hearthfires.esm", "BYOHHouse3PaleBasement"),
       ("dragonborn.esm", "DLC2RRSeverinHouse"), ("update.esm", "ccEEJSSE003Interior01"), ("update.esm", "ccVSVSSE004FarmhouseInterior"),
       ("cceejsse001-hstead.esm", "0EEJSSE001House"), ("cceejsse001-hstead.esm", "0EEJSSE001HouseBasement"),
       ("magpiemanor.esp", "0MAGPIEManorMain"), ("magpiemanor.esp", "0MAGGrotto"), ("morskom.esp", "MEInt01"), ("morskom.esp", "MEInt02"),
       ("0kaidan.esp", "aaAutumnwatchLodge"), ("bsheartland.esm", "CYRBrumaWhitePineLodge"), ("bsheartland.esm", "CYRBrumaBasementPlayerHouse")}
recommended = [x for x in linkable if (x["cell_plugin"], x["cell_edid"]) in REC and x["category"] in ("chest", "furniture") and not x["respawns"]]
emit(OUT + "/permalinks_recommended.txt",
     [";Recommended player-home storage permalinks: real homes only, chests and storage furniture only, no barrels/sacks/display cases/bookshelves, nothing that respawns.",
      ";Generated %s from profile %s. [temporary] entries need the persistence patch before the mod can reach them from elsewhere." % (time.strftime("%Y-%m-%d"), PROFILE)],
     recommended)
print("container refs in home cells:", len(rows), "| linkable (plugin name without spaces, not LotD):", len(linkable), "| of which persistent:", sum(1 for x in linkable if x["persistent"]))
print("recommended subset:", len(recommended), "| persistent:", sum(1 for x in recommended if x["persistent"]), "| temporary:", sum(1 for x in recommended if not x["persistent"]), "| initially disabled w/ enable parent:", sum(1 for x in recommended if x["disabled"] and x["enable_parent"]))
from collections import Counter
print("recommended by category:", dict(Counter(x["category"] for x in recommended)))
print("all linkable by category:", dict(Counter(x["category"] for x in linkable)))
print("elapsed %.0fs" % (time.time() - T0))
