r"""Build "Authoria - Patch - Grassreach Northern Roads Land.esp" (2026-09-03, v2 after review).

Northern Roads re-sculpts 34 Blackreach LAND records and paints vanilla LCaveDirt (025414:Skyrim.esm), which carries no
grass. Grassreach's own trick is a grass-bearing twin of that texture, LCaveDirtBlackreachGrass (000800:FS_BlackreachGrass.esp,
same texture set). This patch copies Northern Roads' 34 LAND records byte-for-byte (heights, normals, colours, every
layer and alpha map, the Dwemer road) and swaps ONLY the LCaveDirt layer FormID for Grassreach's twin.

Cell wrappers (v2): each LAND needs its CELL record as group anchor. An EMPTY partial CELL (v1) is what DynDOLOD ships,
but the Synthesis RemoveLandscapeVertexColor patcher (Mutagen) re-serialises the winning CELL as the parent of its LAND
copy, and Mutagen turns an empty partial CELL into DATA=0/LTMP=0, which clears HasWater and nulls the lighting template
in its output. So v2 carries a VERBATIM copy of the CELL record that wins immediately before this patch's load position
(Northern Roads - Lux patch.esp x21, Northern Roads.esp x12, Authoria - Patch - Requiem - Lock Chests Have Keys.esp x1),
with its FormID links remapped and the extra masters (Lux.esp) declared. The WRLD record is Northern Roads' copy.

Options:
  --grassreach-parity   per quadrant, where Grassreach's own paint of the same cell uses the BARE twin
                        (LCaveDirtBlackreach 0006D7) as base or carries no grass texture at all, map LCaveDirt to the
                        bare twin instead (closer to the mod author's hand paint; the Silent City floor stays mostly bare).
                        Default (off) = every LCaveDirt entry becomes the grass twin (the user's "grass at the city" choice).
  --out <folder>        write elsewhere (default: the mod folder in the instance)

Load AFTER every master and BEFORE "Authoria - Output - Synthesis Worldspace.esp"; re-run that Synthesis group after
building (it overrides LAND with its own copy), then re-bake Blackreach with grass_regen_blackreach.py.
Usage: python build_nr_land_patch.py [--grassreach-parity] [--out <folder>]
"""
import os, sys, struct, re, zlib, collections

INST = r"C:\1. AUTHORIA"
PROFILE = os.path.join(INST, "profiles", "DEEZ CS NUTZ - PBR")
MOD_NAME = "Authoria - Patch - Grassreach Northern Roads Land"
PLUGIN = MOD_NAME + ".esp"
OUT_DIR = os.path.join(INST, "mods", MOD_NAME)
if "--out" in sys.argv: OUT_DIR = sys.argv[sys.argv.index("--out") + 1]
PARITY = "--grassreach-parity" in sys.argv
BLACKREACH = 0x01EE62
OLD_TEX = 0x025414           # LCaveDirt (Skyrim.esm)
GRASS_TWIN = 0x000800        # LCaveDirtBlackreachGrass (FS_BlackreachGrass.esp)
BARE_TWIN = 0x0006D7         # LCaveDirtBlackreach (FS_BlackreachGrass.esp), no grass
GRASSREACH = "FS_BlackreachGrass.esp"; NR = "Northern Roads.esp"
CELL_FORMID_SUBS = {b"LTMP", b"XLCN", b"XCIM", b"XCWT", b"XOWN", b"XILL", b"XCCM", b"XCAS", b"XEZN", b"XCMO"}   # one u32 each
CELL_FORMID_LISTS = {b"XCLR"}                                                                                   # u32 array
CELL_PLAIN_SUBS = {b"EDID", b"FULL", b"DATA", b"XCLC", b"XCLL", b"TVDT", b"MHDT", b"LNAM", b"XCLW", b"XNAM", b"XWCN", b"XWCS", b"XWCU", b"XWEM"}

# ---- profile order + plugin lookup ----
def read_lines(path):
    return [l.rstrip("\r") for l in open(path, encoding="utf-8-sig").read().split("\n")]
MODS = [l[1:] for l in read_lines(os.path.join(PROFILE, "modlist.txt")) if l.startswith("+")]
_plugins_txt = [l for l in read_lines(os.path.join(PROFILE, "plugins.txt")) if l and not l.startswith("#")]
_active = {l[1:] for l in _plugins_txt if l.startswith("*")}
_listed = {l.lstrip("*") for l in _plugins_txt}
_order = [l for l in read_lines(os.path.join(PROFILE, "loadorder.txt")) if l and not l.startswith("#")]
# engine order = loadorder.txt; game-managed masters (Skyrim.esm, DLC, CC) are absent from plugins.txt and always active
PLUGINS = [n for n in _order if n in _active or n not in _listed]
POS = {n: i for i, n in enumerate(PLUGINS)}
def find(name):
    for m in MODS:
        p = os.path.join(INST, "mods", m, name)
        if os.path.exists(p): return p
    p = os.path.join(INST, "Stock Game", "Data", name)
    if os.path.exists(p): return p
    raise SystemExit("not found: " + name)
def masters_of(d):
    hsz = struct.unpack_from("<I", d, 4)[0]
    return [m.decode("latin1") for m in re.findall(rb"MAST..([^\x00]+)\x00", d[24:24 + hsz])], 24 + hsz
def subs(body):
    o = 0; big = None
    while o + 6 <= len(body):
        t = body[o:o + 4]; n = struct.unpack_from("<H", body, o + 4)[0]; o += 6
        if t == b"XXXX": big = struct.unpack_from("<I", body, o)[0]; o += n; continue
        if big is not None: n = big; big = None
        yield t, body[o:o + n]; o += n
def sub(t, payload):
    assert len(payload) < 0xFFFF
    return t + struct.pack("<H", len(payload)) + payload
def rec(sig, flags, fid, body, formver, unk):
    return sig + struct.pack("<IIIHHHH", len(body), flags, fid, 0, 0, formver, unk) + body
def grp(label4, typ, payload):
    return b"GRUP" + struct.pack("<I", 24 + len(payload)) + label4 + struct.pack("<IHHHH", typ, 0, 0, 0, 0) + payload
def record_body(d, a):
    sz = struct.unpack_from("<I", d, a + 4)[0]; fl = struct.unpack_from("<I", d, a + 8)[0]
    body = d[a + 24:a + 24 + sz]
    if fl & 0x40000: body = zlib.decompress(body[4:])
    return body, fl & ~0x40000, struct.unpack_from("<H", d, a + 20)[0], struct.unpack_from("<H", d, a + 22)[0]

def blackreach_walk(d, ms, on_rec):
    """Call on_rec(sig, offset, cell_fid_or_None, chain) for every record under the Blackreach worldspace of plugin d."""
    def walk(a, e, chain, cell):
        while a + 24 <= e:
            t = d[a:a + 4]; sz = struct.unpack_from("<I", d, a + 4)[0]
            if t == b"GRUP":
                lab = d[a + 8:a + 12]; typ = struct.unpack_from("<I", d, a + 12)[0]
                c = struct.unpack_from("<I", lab)[0] if typ == 6 else cell
                walk(a + 24, a + sz, chain + [(typ, lab)], c); a += sz; continue
            on_rec(t, a, cell, chain); a += 24 + sz
    a = masters_of(d)[1]
    while a + 24 <= len(d):
        t = d[a:a + 4]; sz = struct.unpack_from("<I", d, a + 4)[0]
        if t == b"GRUP" and d[a + 8:a + 12] == b"WRLD":
            b = a + 24; e = a + sz
            while b + 24 <= e:
                tt = d[b:b + 4]; ssz = struct.unpack_from("<I", d, b + 4)[0]
                if tt == b"WRLD" and (struct.unpack_from("<I", d, b + 12)[0] & 0xFFFFFF) == BLACKREACH:
                    on_rec(b"WRLD", b, None, [])
                if tt == b"GRUP":
                    lab = struct.unpack_from("<I", d, b + 8)[0]; typ = struct.unpack_from("<I", d, b + 12)[0]
                    if typ == 1 and (lab & 0xFFFFFF) == BLACKREACH and ms[lab >> 24] == "Skyrim.esm": walk(b + 24, b + ssz, [], None)
                    b += ssz; continue
                b += 24 + ssz
            break
        a += sz if t == b"GRUP" else 24 + sz

# ---- 1. Northern Roads: WRLD + 34 LAND ----
nr = open(find(NR), "rb").read()
nr_ms = masters_of(nr)[0] + [NR]
wrld = None; land = {}   # cell_local -> dict(block, sub, land_fid, flags, body, fv, unk)
def nr_rec(t, a, cell, chain):
    global wrld
    if t == b"WRLD":
        body, fl, fv, unk = record_body(nr, a); wrld = (fl, body, fv, unk)
    elif t == b"LAND":
        body, fl, fv, unk = record_body(nr, a); fid = struct.unpack_from("<I", nr, a + 12)[0]
        assert nr_ms[fid >> 24] == "Skyrim.esm" and nr_ms[cell >> 24] == "Skyrim.esm"
        land[cell & 0xFFFFFF] = dict(block=[l for ty, l in chain if ty == 4][0], sub=[l for ty, l in chain if ty == 5][0],
                                     land_fid=fid & 0xFFFFFF, flags=fl, body=body, fv=fv, unk=unk)
blackreach_walk(nr, nr_ms, nr_rec)
assert wrld and len(land) == 34, (bool(wrld), len(land))
for st, sd in subs(wrld[1]):
    if st in (b"XEZN", b"XLCN", b"WNAM", b"CNAM", b"NAM2", b"NAM3", b"ZNAM"):
        fid = struct.unpack_from("<I", sd, 0)[0]; assert fid == 0 or nr_ms[fid >> 24] == "Skyrim.esm", (st, f"{fid:08X}")

# ---- 2. Grassreach parity mask (per cell, per quadrant) ----
parity = {}   # (cell, quadrant) -> True when the bare twin should be used
if PARITY:
    gr = open(find(GRASSREACH), "rb").read(); gr_ms = masters_of(gr)[0] + [GRASSREACH]
    def gr_rec(t, a, cell, chain):
        if t != b"LAND" or (cell & 0xFFFFFF) not in land: return
        body = record_body(gr, a)[0]; base = {}; layers = collections.defaultdict(set)
        for st, sd in subs(body):
            if st in (b"BTXT", b"ATXT"):
                fid = struct.unpack_from("<I", sd, 0)[0]; q = sd[4]
                if fid and gr_ms[fid >> 24] == GRASSREACH:
                    (base.__setitem__(q, fid & 0xFFFFFF) if st == b"BTXT" else layers[q].add(fid & 0xFFFFFF))
                elif st == b"BTXT": base[q] = fid
        for q in range(4):
            has_grass = base.get(q) == GRASS_TWIN or GRASS_TWIN in layers[q]
            parity[(cell & 0xFFFFFF, q)] = (base.get(q) == BARE_TWIN) or not has_grass
    blackreach_walk(gr, gr_ms, gr_rec)

# ---- 3. pre-patch CELL winners (walk every plugin that loads before this patch) ----
cut = POS.get(PLUGIN)
before = PLUGINS[:cut] if cut is not None else PLUGINS
cell_win = {}    # cell_local -> (plugin, flags, body, fv, unk, masters)
cache_paths = set()
for n in before:
    try: p = find(n)
    except SystemExit: continue
    d = open(p, "rb").read()
    if b"CELL" not in d: continue
    ms = masters_of(d)[0] + [n]
    if "Skyrim.esm" not in ms: continue
    def on(t, a, cell, chain, d=d, n=n, ms=ms):
        if t != b"CELL": return
        fid = struct.unpack_from("<I", d, a + 12)[0]
        if ms[fid >> 24] != "Skyrim.esm" or (fid & 0xFFFFFF) not in land: return
        body, fl, fv, unk = record_body(d, a)
        if fl & 0x4000: return                      # a partial form never becomes the copied wrapper
        cell_win[fid & 0xFFFFFF] = (n, fl, body, fv, unk, ms)
    blackreach_walk(d, ms, on)
assert len(cell_win) == 34, len(cell_win)

# ---- 4. masters ----
needed = {"Skyrim.esm", GRASSREACH, NR}
for c, (n, fl, body, fv, unk, ms) in cell_win.items():
    for st, sd in subs(body):
        if st in CELL_FORMID_SUBS:
            fid = struct.unpack_from("<I", sd, 0)[0]
            if fid: needed.add(ms[fid >> 24])
        elif st in CELL_FORMID_LISTS:
            for i in range(0, len(sd), 4):
                fid = struct.unpack_from("<I", sd, i)[0]
                if fid: needed.add(ms[fid >> 24])
        elif st not in CELL_PLAIN_SUBS: raise SystemExit(f"unhandled CELL subrecord {st} in {n}")
MASTERS = sorted(needed, key=lambda m: POS[m])
MI = {m: i for i, m in enumerate(MASTERS)}
assert MASTERS[0] == "Skyrim.esm"
if cut is not None: assert all(POS[m] < cut for m in MASTERS)

def remap_from(ms):
    def f(fid):
        if fid == 0: return 0
        src = ms[fid >> 24]
        return (MI[src] << 24) | (fid & 0xFFFFFF)
    return f

# ---- 5. rewrite LAND bodies ----
swapped = bare = reindexed = 0
def rewrite_land(cell, body):
    global swapped, bare, reindexed
    out = bytearray(); rm = remap_from(nr_ms)
    for st, sd in subs(body):
        if st in (b"BTXT", b"ATXT"):
            fid = struct.unpack_from("<I", sd, 0)[0]; q = sd[4]
            if fid and nr_ms[fid >> 24] == "Skyrim.esm" and (fid & 0xFFFFFF) == OLD_TEX:
                if parity.get((cell, q)): new = (MI[GRASSREACH] << 24) | BARE_TWIN; bare += 1
                else: new = (MI[GRASSREACH] << 24) | GRASS_TWIN; swapped += 1
            else:
                new = rm(fid)
                if new != fid: reindexed += 1
            sd = struct.pack("<I", new) + sd[4:]
        out += sub(st, sd)
    return bytes(out)
def rewrite_cell(body, ms):
    out = bytearray(); rm = remap_from(ms)
    for st, sd in subs(body):
        if st in CELL_FORMID_SUBS: sd = struct.pack("<I", rm(struct.unpack_from("<I", sd, 0)[0])) + sd[4:]
        elif st in CELL_FORMID_LISTS: sd = b"".join(struct.pack("<I", rm(struct.unpack_from("<I", sd, i)[0])) for i in range(0, len(sd), 4))
        out += sub(st, sd)
    return bytes(out)

# ---- 6. assemble ----
by_block = collections.OrderedDict()
for c in sorted(land):
    L = land[c]; by_block.setdefault(L["block"], collections.OrderedDict()).setdefault(L["sub"], []).append(c)
world_children = b""; ngroups = 2   # top WRLD group + world-children group
for blk, subblocks in by_block.items():
    block_payload = b""
    for sb, cs in subblocks.items():
        sub_payload = b""
        for c in cs:
            L = land[c]; n, cfl, cbody, cfv, cunk, cms = cell_win[c]
            cell_rec = rec(b"CELL", cfl & ~0x4000, c, rewrite_cell(cbody, cms), cfv, cunk)
            land_rec = rec(b"LAND", L["flags"], L["land_fid"], rewrite_land(c, L["body"]), L["fv"], L["unk"])
            sub_payload += cell_rec + grp(struct.pack("<I", c), 6, grp(struct.pack("<I", c), 9, land_rec)); ngroups += 2
        block_payload += grp(sb, 5, sub_payload); ngroups += 1
    world_children += grp(blk, 4, block_payload); ngroups += 1
wrld_rec = rec(b"WRLD", wrld[0], BLACKREACH, wrld[1], wrld[2], wrld[3])
top = grp(b"WRLD", 0, wrld_rec + grp(struct.pack("<I", BLACKREACH), 1, world_children))
nrec = 1 + 34 * 2
hdr = sub(b"HEDR", struct.pack("<fIi", 1.7, nrec + ngroups, 0x800))
hdr += sub(b"CNAM", b"Authoria\x00")
desc = ("Northern Roads Blackreach land with Grassreach's grass-bearing cave dirt layer" + (" (Grassreach parity mask)" if PARITY else "") +
        ". Cells are verbatim copies of the pre-patch winners. Built 2026-09-03 by build_nr_land_patch.py v2.\x00")
hdr += sub(b"SNAM", desc.encode("latin1"))
for m in MASTERS: hdr += sub(b"MAST", m.encode("latin1") + b"\x00") + sub(b"DATA", b"\x00" * 8)
hdr += sub(b"INTV", struct.pack("<I", 1))
tes4 = b"TES4" + struct.pack("<IIIHHHH", len(hdr), 0x200, 0, 0, 0, 44, 0) + hdr
data = tes4 + top
os.makedirs(OUT_DIR, exist_ok=True)
out = os.path.join(OUT_DIR, PLUGIN); open(out, "wb").write(data)
meta = ["[General]", "modid=0", "version=2.0", "newestVersion=", 'category="-1,"', "installationFile=", "gameName=SkyrimSE",
        "repository=", "comments=Built by _tools/blackreach-grass/build_nr_land_patch.py", "notes=", "url=", "hasCustomURL=false",
        "converted=false", "validated=false", "endorsed=0", "tracked=0", ""]
open(os.path.join(OUT_DIR, "meta.ini"), "wb").write("\r\n".join(meta).encode("utf-8"))
wins = collections.Counter(v[0] for v in cell_win.values())
print(f"wrote {out}: {len(data)} bytes | masters {MASTERS} | 1 WRLD, 34 CELL (verbatim winners: {dict(wins)}), 34 LAND | "
      f"LCaveDirt entries -> grass twin {swapped}, bare twin {bare}, road links re-indexed {reindexed} | HEDR count {nrec + ngroups}")

# ---- 7. verify by independent re-parse ----
d = open(out, "rb").read()
assert struct.unpack_from("<H", d, 20)[0] == 44 and struct.unpack_from("<I", d, 8)[0] == 0x200
ms, top_off = masters_of(d); assert ms == MASTERS
seen_land = {}; seen_cell = {}; groups = 0
def vwalk(a, e, cell):
    global groups
    while a + 24 <= e:
        t = d[a:a + 4]; sz = struct.unpack_from("<I", d, a + 4)[0]
        if t == b"GRUP":
            groups += 1; typ = struct.unpack_from("<I", d, a + 12)[0]; c = struct.unpack_from("<I", d, a + 8)[0] if typ == 6 else cell
            vwalk(a + 24, a + sz, c); a += sz; continue
        fl = struct.unpack_from("<I", d, a + 8)[0]; fid = struct.unpack_from("<I", d, a + 12)[0]
        assert not (fl & 0x40000) and not (fl & 0x4000)
        body = d[a + 24:a + 24 + sz]
        if t == b"CELL": seen_cell[fid] = [(st, sd) for st, sd in subs(body)]
        if t == b"LAND": seen_land[cell] = {struct.unpack_from("<I", sd, 0)[0] for st, sd in subs(body) if st in (b"BTXT", b"ATXT")}
        a += 24 + sz
vwalk(top_off, len(d), None)
assert len(seen_land) == 34 and len(seen_cell) == 34 and groups == ngroups and top_off + struct.unpack_from("<I", d, top_off + 4)[0] == len(d)
gi = MI[GRASSREACH]
for c, tex in seen_land.items():
    assert 0x00025414 not in tex
    assert any(f == (gi << 24) | GRASS_TWIN or f == (gi << 24) | BARE_TWIN for f in tex), c
    assert all((f >> 24) < len(MASTERS) for f in tex)
for c, ss in seen_cell.items():
    n, cfl, cbody, cfv, cunk, cms = cell_win[c]
    src = [(st, sd) for st, sd in subs(cbody)]
    assert [st for st, _ in ss] == [st for st, _ in src], c
    for (st, sd), (st2, sd2) in zip(ss, src):
        if st in CELL_FORMID_SUBS or st in CELL_FORMID_LISTS: assert len(sd) == len(sd2)
        else: assert sd == sd2, (c, st)
    assert any(st == b"DATA" for st, _ in ss) and any(st == b"XCLC" for st, _ in ss), c
print("verify: 34 LAND + 34 full CELL re-parsed; CELL bodies equal their winners apart from remapped links; no partial/compressed flags; groups", groups)
