"""Partial NGIO grass-cache regeneration driver (Magpie Manor + Morskom Estate areas).

How NGIO-NG 1.6.8 really behaves (pilots 2026-08-19):
  * It regenerates EVERY cell of every listed worldspace, EXCEPT cells listed as done in PrecacheGrass.txt
    (one line per cell: cell_<WorldspaceEditorID>_<x>_<y>, grid -64..64).  -> we pre-fill that file.
  * Output files are always BASE-named (<ws>x####y####.cgid). Grass Cache Helper's season suffix only applies
    when READING. -> rename outputs ourselves for the seasonal passes.
  * An output for a cell whose base file already exists is APPENDED to that file through the VFS (corrupts it).
    -> stage the Default base files of the whole processed area out of the mod before each pass.
  * Existing files never prevent generation.

Usage (MO2 CLOSED for every command):
  python grass_regen.py stage WIN|SPR|SUM|AUT|DEF   - stage Default files out, write progress file, pin season
  python grass_regen.py collect WIN|SPR|SUM|AUT|DEF - after the game run: sort outputs into the cache mods
  python grass_regen.py finish                       - restore staged Default files + inis, final verification
  python grass_regen.py status                       - show what is staged / pending
"""
import os, sys, re, shutil, subprocess, json, time

INST = r"C:\1. AUTHORIA"
MODS = os.path.join(INST, "mods")
OVR = os.path.join(INST, "overwrite", "Grass")
TRIGGER = os.path.join(INST, "Stock Game", "PrecacheGrass.txt")
INI_DIR = os.path.join(MODS, "Authoria - MCM and INI Settings", "SKSE", "Plugins")
GRASS_INI = os.path.join(INI_DIR, "GrassControl.ini")
SEASON_INI = os.path.join(INI_DIR, "po3_SeasonsOfSkyrim.ini")
JOB = os.environ.get("GRASS_REGEN_JOB", "2026-08-19 - grass regen magpie-morskom")
BACKUP = os.path.join(INST, "_backups", JOB)
STAGED = os.path.join(BACKUP, "staged-default")
STATE = os.path.join(BACKUP, "state.json")
ORIG_LIST = "aaaLucOblivionRealm;AlftandWorld;AXGodsforsakenRockWorld;AXOffshoreIslandWorld;Blackreach;BlindCliffCaveWorld;BloatedMansGrottoWorld;BloatedMansGrottoWorldDUPLICATE001;BluePalaceWingWorld;BSHeartland;BSKHyorkerIsle;BSKTestWorld;ccBGSSSE067DeadlandsWorld;ccKRTSSE001QNWorld;CYRBiomeTesting;CYRCrowsWoodWorld;CYRFrostfireGlade;CYRGreenLeafGlade;CYRTestWorld;DarkwaterWorld;DeepwoodRedoubtWorld;Dimfrost;DLC01Boneyard;DLC01FalmerValley;DLC01SoulCairn;DLC1AncestorsGladeWorld;DLC1ForebearsHoldout;DLC1HunterHQWorld;DLC1VampireCastleCourtyard;DLC2SolstheimWorld;EastEmpireWarehouse;ECSSShiveringIsles;ECSSzDummyMarkerWorld;EldergleamSanctuaryWorld;FallowstoneCaveWorldEnd;FallowstoneCaveWorldStart;FrostmereCryptWorld;GRVECemeteryWorld;JaphetsFollyWorld;KarthspireRedoubtWorld;KatariahWorld;KR2Deadlands;ksws07World;LabyrinthianWorld04;mannyGFDesert;mannyGFL;mannyGFO;mannyGFOasisCave;MossMotherCavernWorld;OlenIceCapitol;OlenPaleCross;OlenveldBlackWormFort;OlenveldSCExpansionWS;OlenveldUnderWorld;OlenveldUW2;OlenveldWS;PalePass;RedEagleRedoubtWorld;SEVAPstartforest;ShadowgreenCavernWorld;SkuldafnWorld;Sovngarde;Tamriel;WhiterunDragonsreachWorld;WindhelmPitWorldspace;WindPassWorld;WyrmstoothWorld;zAoMWitchWorld;zBMLamaeWorld;zCHOldForestWorld;zCHTrueEndWorld;zCOBruiantWorld;zDcdGhostSea;zGHCradleWoodsWorld;zGHFelixRealm;zLrhLalanoaRealm;zRevNamiraRealm"

SEASONS = {"WIN": (1, ".WIN", "Winter"), "SPR": (2, ".SPR", "Spring"), "SUM": (3, ".SUM", "Summer"),
           "AUT": (4, ".AUT", "Autumn"),
           "DEF": (3, "", "Default")}   # Default pass = SUMMER state (Season Type 3), like the July cache; seasons-off (0) gave bare Dawnstar cells

# target cells (what we want regenerated) and the staging area (targets + margin that NGIO may also write)
_cells = os.environ.get("GRASS_REGEN_CELLS", "")
if _cells:
    TARGETS = [tuple(int(v) for v in c.split(",")) for c in _cells.split(";") if c.strip()]
    STAGE_AREA = [(x+dx, y+dy) for (x, y) in TARGETS for dx in range(-3, 4) for dy in range(-3, 4)]
else:
    TARGETS = [(x, y) for x in range(19, 24) for y in range(-3, 2)]             + [(x, y) for x in range(6, 12) for y in range(24, 30)]             + [(x, y) for x in range(8, 11) for y in range(30, 33)]
    STAGE_AREA = [(x, y) for x in range(16, 27) for y in range(-6, 5)]             + [(x, y) for x in range(3, 15) for y in range(21, 36)]
    assert len(TARGETS) == 70

TARGET_SET = set(TARGETS); STAGE_SET = set(STAGE_AREA) | TARGET_SET

def pad(v):
    return ("-" + f"{abs(v):03d}") if v < 0 else f"{v:04d}"
def fname(x, y, suf=""):
    return f"Tamrielx{pad(x)}y{pad(y)}{suf}.cgid"
def parse_name(f):
    m = re.match(r"^Tamrielx(-?\d+)y(-?\d+)(\.\w\w\w)?\.cgid$", f, re.I)
    return (int(m.group(1)), int(m.group(2)), (m.group(3) or "").upper()) if m else None
def grass_dir(mod):
    d = os.path.join(MODS, f"Authoria - Grass Cache - {mod}")
    sub = [s for s in os.listdir(d) if s.lower() == "grass"][0]
    return os.path.join(d, sub)
def mo2_closed():
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return "modorganizer.exe" not in out and "skyrimse.exe" not in out
def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"staged": False, "passes": {}}
def save_state(s):
    os.makedirs(BACKUP, exist_ok=True); json.dump(s, open(STATE, "w"), indent=1)

def set_season(n):
    b = open(SEASON_INI, "rb").read()
    new, k = re.subn(rb"Season Type = \d", b"Season Type = %d" % n, b, count=1)
    assert k == 1
    open(SEASON_INI, "wb").write(new)
def set_grasscontrol(only_list):
    b = open(GRASS_INI, "rb").read().decode("utf-8")
    b, k1 = re.subn(r"(?m)^Updating-Cache = \w+", "Updating-Cache = true", b)
    b, k2 = re.subn(r"(?m)^Only-pregenerate-world-spaces = .*$", "Only-pregenerate-world-spaces = " + only_list, b)
    assert k1 == 1 and k2 == 1, (k1, k2)
    open(GRASS_INI, "wb").write(b.encode("utf-8"))

def write_progress():
    lines = [f"cell_Tamriel_{x}_{y}" for x in range(-64, 65) for y in range(-64, 65) if (x, y) not in TARGET_SET]
    crlf = chr(13) + chr(10)
    with open(TRIGGER, "wb") as f:
        f.write((crlf.join(lines) + crlf).encode("ascii"))
    return len(lines)

def cmd_stage(season):
    assert season in SEASONS, season
    assert mo2_closed(), "MO2 / the game is running — close it first"
    st = load_state()
    os.makedirs(OVR, exist_ok=True)
    leftovers = [f for f in os.listdir(OVR) if f.lower().endswith(".cgid")]
    assert not leftovers, f"overwrite\\Grass is not empty: {leftovers[:5]}"
    # stage Default base files for the whole area (only once; they stay out until finish)
    os.makedirs(STAGED, exist_ok=True)
    dd = grass_dir("Default"); moved = 0
    for (x, y) in sorted(STAGE_SET):
        p = os.path.join(dd, fname(x, y))
        if os.path.exists(p):
            shutil.move(p, os.path.join(STAGED, fname(x, y))); moved += 1
    st["staged"] = True
    n = write_progress()
    set_season(SEASONS[season][0])
    set_grasscontrol("Tamriel")
    st["passes"][season] = {"staged_at": time.strftime("%Y-%m-%d %H:%M:%S"), "collected": False}
    save_state(st)
    print(f"[stage {season}] Default files newly staged out: {moved} (total staged now: {len(os.listdir(STAGED))})")
    print(f"[stage {season}] PrecacheGrass.txt written with {n} done-cells (todo = {len(TARGET_SET)} target cells)")
    print(f"[stage {season}] Season Type = {SEASONS[season][0]}, Only-pregenerate-world-spaces = Tamriel, Updating-Cache = true")
    print("NOW: user opens MO2 and presses Play; wait for 'Grass generation finished' and the game to close.")

def cmd_collect(season):
    assert season in SEASONS, season
    assert mo2_closed(), "MO2 / the game is running — close it first"
    st = load_state()
    assert season in st["passes"], f"pass {season} was never staged"
    assert not os.path.exists(TRIGGER), "PrecacheGrass.txt still exists — the run did not finish"
    num, suf, mod = SEASONS[season]
    outs = [f for f in os.listdir(OVR) if f.lower().endswith(".cgid")]
    target_out, other_out, foreign = [], [], []
    for f in outs:
        pn = parse_name(f)
        if not pn: foreign.append(f); continue
        x, y, s = pn
        if s: foreign.append(f); continue          # NGIO never writes suffixed names; anything else is odd
        (target_out if (x, y) in TARGET_SET else other_out).append((x, y, f))
    print(f"[collect {season}] outputs: {len(outs)} total, {len(target_out)} target, {len(other_out)} margin/other, {len(foreign)} unexpected")
    if foreign: print("  UNEXPECTED names (left in overwrite):", foreign[:10])
    missing = sorted(TARGET_SET - {(x, y) for x, y, _ in target_out})
    if missing: print(f"  WARNING: {len(missing)} target cells produced no file: {[fname(x,y) for x,y in missing][:10]}")
    # sizes sanity
    small = [f for _, _, f in target_out if os.path.getsize(os.path.join(OVR, f)) < 40]
    if small: print("  WARNING: suspiciously small outputs:", small[:10])
    old_dir = os.path.join(BACKUP, f"old-{season}"); os.makedirs(old_dir, exist_ok=True)
    disc_dir = os.path.join(BACKUP, f"discarded-{season}"); os.makedirs(disc_dir, exist_ok=True)
    dest = grass_dir(mod); placed = 0; replaced = 0
    for x, y, f in target_out:
        newname = fname(x, y, suf)
        old = os.path.join(dest, newname)
        if os.path.exists(old):
            shutil.move(old, os.path.join(old_dir, newname)); replaced += 1
        shutil.move(os.path.join(OVR, f), os.path.join(dest, newname)); placed += 1
    for x, y, f in other_out:
        shutil.move(os.path.join(OVR, f), os.path.join(disc_dir, f))
    st["passes"][season].update({"collected": True, "placed": placed, "replaced_old": replaced, "discarded": len(other_out),
                                 "missing": [fname(x, y) for x, y in missing], "collected_at": time.strftime("%Y-%m-%d %H:%M:%S")})
    save_state(st)
    print(f"[collect {season}] placed {placed} files into 'Authoria - Grass Cache - {mod}' ({replaced} old ones moved to {old_dir}); {len(other_out)} margin outputs -> {disc_dir}")
    if season == "DEF":
        # staged target files are superseded by fresh outputs; keep them in staged folder (finish will restore only non-targets)
        pass

def cmd_finish():
    assert mo2_closed(), "MO2 / the game is running — close it first"
    st = load_state()
    done = [s for s in SEASONS if st["passes"].get(s, {}).get("collected")]
    print("passes collected:", done)
    dd = grass_dir("Default"); restored = 0; superseded = 0
    if os.path.isdir(STAGED):
        for f in os.listdir(STAGED):
            pn = parse_name(f); x, y, _ = pn
            if (x, y) in TARGET_SET and st["passes"].get("DEF", {}).get("collected") and os.path.exists(os.path.join(dd, f)):
                # DEF pass produced a fresh file for this target: keep the staged original as the 'old' copy
                shutil.move(os.path.join(STAGED, f), os.path.join(BACKUP, "old-DEF", f)); superseded += 1
            else:
                shutil.move(os.path.join(STAGED, f), os.path.join(dd, f)); restored += 1
        try: os.rmdir(STAGED)
        except OSError: pass
    print(f"[finish] restored {restored} staged Default files; {superseded} target originals kept as old-DEF copies")
    # inis
    set_season(5)
    b = open(GRASS_INI, "rb").read().decode("utf-8")
    b, k = re.subn(r"(?m)^Only-pregenerate-world-spaces = .*$", "Only-pregenerate-world-spaces = " + ORIG_LIST, b)
    b = re.sub(r"(?m)^;ORIGINAL \(restore after the Magpie/Morskom regen\): Only-pregenerate-world-spaces = .*\r?\n", "", b)
    open(GRASS_INI, "wb").write(b.encode("utf-8"))
    print("[finish] po3 Season Type = 5; Only-pregenerate-world-spaces restored to the full list; Updating-Cache left = true (deliberate)")
    if os.path.exists(TRIGGER): os.remove(TRIGGER); print("[finish] removed leftover PrecacheGrass.txt")
    left = [f for f in os.listdir(OVR) if f.lower().endswith(".cgid")] if os.path.isdir(OVR) else []
    print("[finish] overwrite\\Grass leftovers:", left[:5] if left else "none")
    st["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S"); save_state(st)
    cmd_status()

def cmd_status():
    st = load_state()
    print(json.dumps(st, indent=1))
    for mod in ["Default", "Winter", "Spring", "Summer", "Autumn"]:
        n = len([f for f in os.listdir(grass_dir(mod)) if f.lower().endswith(".cgid")])
        print(f"  {mod:8s} files now: {n}")
    print("  staged Default files:", len(os.listdir(STAGED)) if os.path.isdir(STAGED) else 0)
    print("  overwrite\\Grass:", len([f for f in os.listdir(OVR)]) if os.path.isdir(OVR) else "n/a")
    print("  PrecacheGrass.txt:", "present" if os.path.exists(TRIGGER) else "absent")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stage": cmd_stage(sys.argv[2].upper())
    elif cmd == "collect": cmd_collect(sys.argv[2].upper())
    elif cmd == "finish": cmd_finish()
    elif cmd == "status": cmd_status()
    else: print(__doc__)
