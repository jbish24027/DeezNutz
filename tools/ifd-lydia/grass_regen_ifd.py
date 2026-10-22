r"""NGIO grass-cache generation for IFD Lydia's new worldspace (0ICBBanditFortressWorld).

Same mechanics as _tools/magpie-manor/grass_regen.py (proven 2026-08-19), simplified:
  * the worldspace is NEW, so no existing cache files need staging and no PrecacheGrass.txt pre-fill
    is needed - an EMPTY PrecacheGrass.txt in Stock Game is the trigger;
  * Only-pregenerate-world-spaces is pinned to this one worldspace for the run, so the pass takes
    seconds instead of walking all of Tamriel;
  * outputs land BASE-named in overwrite\Grass; `collect` renames them with the season suffix and
    moves them into the matching "Authoria - Grass Cache - <Season>" mod.

Usage (MO2 CLOSED for every command; reopen MO2 and press Play for each run):
  python grass_regen_ifd.py stage DEF|WIN|SPR|SUM|AUT   - pin season + worldspace, write the trigger
  <launch the game from MO2 once; NGIO generates, deletes the trigger and the game exits>
  python grass_regen_ifd.py collect DEF|WIN|SPR|SUM|AUT - move outputs into the season's cache mod
  ... repeat stage/collect for the other four seasons ...
  python grass_regen_ifd.py finish                       - restore the inis, remove any leftover trigger
  python grass_regen_ifd.py status
"""
import os, sys, re, shutil, subprocess, json

INST = r"C:\1. AUTHORIA"
MODS = os.path.join(INST, "mods")
OVR = os.path.join(INST, "overwrite", "Grass")
TRIGGER = os.path.join(INST, "Stock Game", "PrecacheGrass.txt")
INI_DIR = os.path.join(MODS, "Authoria - MCM and INI Settings", "SKSE", "Plugins")
GRASS_INI = os.path.join(INI_DIR, "GrassControl.ini")
SEASON_INI = os.path.join(INI_DIR, "po3_SeasonsOfSkyrim.ini")
WS = "0ICBBanditFortressWorld"
JOB = os.environ.get("GRASS_REGEN_JOB", "2026-08-21 - grass regen IFD Lydia worldspace")
BACKUP = os.path.join(INST, "_backups", JOB)
STATE = os.path.join(BACKUP, "state.json")
SEASONS = {"WIN": (1, ".WIN", "Winter"), "SPR": (2, ".SPR", "Spring"), "SUM": (3, ".SUM", "Summer"),
           "AUT": (4, ".AUT", "Autumn"), "DEF": (3, "", "Default")}   # Default pass = summer state (Season Type 3)

def mo2_closed():
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return "modorganizer.exe" not in out and "skyrimse.exe" not in out and "skse64_loader.exe" not in out
def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"backed_up": False, "passes": {}}
def save_state(s):
    os.makedirs(BACKUP, exist_ok=True); json.dump(s, open(STATE, "w"), indent=1)
def grass_dir(season_name):
    d = os.path.join(MODS, f"Authoria - Grass Cache - {season_name}")
    sub = [s for s in os.listdir(d) if s.lower() == "grass"]
    if not sub:
        os.makedirs(os.path.join(d, "Grass"), exist_ok=True); return os.path.join(d, "Grass")
    return os.path.join(d, sub[0])
def backup_inis(state):
    if state["backed_up"]: return
    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(GRASS_INI, os.path.join(BACKUP, "GrassControl.ini.orig"))
    shutil.copy2(SEASON_INI, os.path.join(BACKUP, "po3_SeasonsOfSkyrim.ini.orig"))
    state["backed_up"] = True; save_state(state)
def set_season(n):
    b = open(SEASON_INI, "rb").read()
    new, k = re.subn(rb"Season Type = \d", b"Season Type = %d" % n, b, count=1)
    assert k == 1, "Season Type line not found"
    open(SEASON_INI, "wb").write(new)
def set_grasscontrol(only_list):
    t = open(GRASS_INI, "rb").read().decode("utf-8")
    t, k1 = re.subn(r"(?m)^Updating-Cache = \w+", "Updating-Cache = true", t)
    t, k2 = re.subn(r"(?m)^Only-pregenerate-world-spaces = .*$", "Only-pregenerate-world-spaces = " + only_list, t)
    assert k1 == 1 and k2 == 1, (k1, k2)
    open(GRASS_INI, "wb").write(t.encode("utf-8"))

STAGED = os.path.join(BACKUP, "staged-default")

def stage_out_default():
    """NGIO writes BASE-named files. If a base file for a cell already exists it APPENDS through the
    VFS and corrupts it. Before any seasonal pass, move this worldspace's Default base files aside."""
    src = grass_dir("Default"); os.makedirs(STAGED, exist_ok=True); moved = 0
    for f in list(os.listdir(src)):
        if re.match(rf"^{re.escape(WS)}x-?\d+y-?\d+\.cgid$", f, re.I):
            shutil.move(os.path.join(src, f), os.path.join(STAGED, f)); moved += 1
    already = len(os.listdir(STAGED))
    print(f"[stage] moved {moved} Default base file(s) aside ({already} now held safe in the backup)")
    return moved

def restore_staged_default():
    if not os.path.isdir(STAGED): return 0
    dst = grass_dir("Default"); n = 0
    for f in list(os.listdir(STAGED)):
        shutil.move(os.path.join(STAGED, f), os.path.join(dst, f)); n += 1
    print(f"[finish] restored {n} Default base file(s)")
    return n

def stage(season):
    assert mo2_closed(), "close MO2 / the game first"
    n, suf, name = SEASONS[season]
    st = load_state(); backup_inis(st)
    if season != "DEF":
        stage_out_default()
    set_grasscontrol(WS); set_season(n)
    open(TRIGGER, "wb").write(b"")   # empty trigger: nothing is done yet in this worldspace
    st["passes"][season] = {"staged": True, "collected": False}; save_state(st)
    print(f"[stage {season}] Season Type = {n}, Only-pregenerate-world-spaces = {WS}, Updating-Cache = true")
    print("[stage] trigger written. Now open MO2, press Play, wait for the game to close itself, close MO2, then run: collect", season)

def collect(season):
    assert mo2_closed(), "close MO2 / the game first"
    assert not os.path.exists(TRIGGER), "PrecacheGrass.txt still exists - the run did not finish"
    n, suf, name = SEASONS[season]
    dest = grass_dir(name); moved = 0; other = []
    for f in sorted(os.listdir(OVR)) if os.path.isdir(OVR) else []:
        m = re.match(rf"^{re.escape(WS)}x(-?\d+)y(-?\d+)\.cgid$", f, re.I)
        if not m:
            other.append(f); continue
        target = os.path.join(dest, f[:-5] + suf + ".cgid")
        shutil.move(os.path.join(OVR, f), target); moved += 1
    st = load_state(); st["passes"].setdefault(season, {})["collected"] = moved; save_state(st)
    print(f"[collect {season}] moved {moved} cell file(s) into {dest}")
    if other: print("[collect] left untouched in overwrite\\Grass (not this worldspace):", other[:10], "..." if len(other) > 10 else "")
    if moved == 0: print("[collect] WARNING: nothing generated - either the worldspace has no grass or the run did not happen")

def finish():
    assert mo2_closed(), "close MO2 / the game first"
    restore_staged_default()
    shutil.copy2(os.path.join(BACKUP, "GrassControl.ini.orig"), GRASS_INI)
    shutil.copy2(os.path.join(BACKUP, "po3_SeasonsOfSkyrim.ini.orig"), SEASON_INI)
    if os.path.exists(TRIGGER): os.remove(TRIGGER); print("[finish] removed leftover PrecacheGrass.txt")
    print("[finish] GrassControl.ini and po3_SeasonsOfSkyrim.ini restored from backup")
    status()

def status():
    st = load_state()
    print("job:", JOB); print("trigger present:", os.path.exists(TRIGGER)); print("passes:", json.dumps(st.get("passes", {})))
    for season, (n, suf, name) in SEASONS.items():
        d = grass_dir(name)
        cnt = len([f for f in os.listdir(d) if f.lower().startswith(WS.lower()) and f.lower().endswith(suf.lower() + ".cgid")])
        print(f"  {name:8} {cnt} file(s) for {WS}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "stage": stage(sys.argv[2].upper())
    elif cmd == "collect": collect(sys.argv[2].upper())
    elif cmd == "finish": finish()
    else: status()
