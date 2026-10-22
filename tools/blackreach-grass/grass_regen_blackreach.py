r"""NGIO grass-cache regeneration for the Blackreach worldspace (Grassreach install, 2026-09-03).

Derived from _tools/ifd-lydia/grass_regen_ifd.py (proven 2026-08-21) with the one difference that matters:
Blackreach ALREADY has cache files (9 cells x 5 seasons). NGIO writes BASE-named files and APPENDS to an
existing base file through the VFS, corrupting it - so the Default base files are moved aside BEFORE the
pass, and every old Blackreach cache file (all five season mods) is backed up and replaced by the new bake.
Blackreach is in none of the Seasons of Skyrim worldspace whitelists, so ONE pass covers all seasons: the
base output is kept in the Default mod and copied with the .WIN/.SPR/.SUM/.AUT suffixes into the others.

Usage (MO2 CLOSED for every command):
  python grass_regen_blackreach.py stage     - back up + park the old Blackreach cache files, pin the inis, write the trigger
  <open MO2, press Play; NGIO generates Blackreach only (~10 s), deletes the trigger, the game exits; close MO2>
  python grass_regen_blackreach.py collect   - move the new files into all five cache mods
  python grass_regen_blackreach.py finish    - restore the inis (and the old files if the bake produced nothing)
  python grass_regen_blackreach.py status
"""
import os, sys, re, shutil, subprocess, json

INST = r"C:\1. AUTHORIA"
MODS = os.path.join(INST, "mods")
OVR = os.path.join(INST, "overwrite", "Grass")
TRIGGER = os.path.join(INST, "Stock Game", "PrecacheGrass.txt")
GRASS_INI = os.path.join(MODS, "Authoria - MCM and INI Settings", "SKSE", "Plugins", "GrassControl.ini")
_SEASON_OVR = os.path.join(INST, "overwrite", "SKSE", "Plugins", "po3_SeasonsOfSkyrim.ini")
_SEASON_MOD = os.path.join(MODS, "Authoria - MCM and INI Settings", "SKSE", "Plugins", "po3_SeasonsOfSkyrim.ini")
SEASON_INI = _SEASON_OVR if os.path.exists(_SEASON_OVR) else _SEASON_MOD   # overwrite wins the VFS
WS = "Blackreach"
JOB = os.environ.get("GRASS_REGEN_JOB", "2026-09-03 - grass regen Blackreach")
BACKUP = os.path.join(INST, "_backups", JOB)
STATE = os.path.join(BACKUP, "state.json")
OLD = os.path.join(BACKUP, "old-cache")          # every old Blackreach cache file, per season mod
SEASONS = [("Default", ""), ("Winter", ".WIN"), ("Spring", ".SPR"), ("Summer", ".SUM"), ("Autumn", ".AUT")]
PAT = re.compile(rf"^{re.escape(WS)}x-?\d+y-?\d+(\.(WIN|SPR|SUM|AUT))?\.cgid$", re.I)

def mo2_closed():
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return "modorganizer.exe" not in out and "skyrimse.exe" not in out and "skse64_loader.exe" not in out
def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"backed_up": False, "staged": False, "collected": None}
def save_state(s):
    os.makedirs(BACKUP, exist_ok=True); json.dump(s, open(STATE, "w"), indent=1)
def grass_dir(season_name):
    d = os.path.join(MODS, f"Authoria - Grass Cache - {season_name}")
    sub = [s for s in os.listdir(d) if s.lower() == "grass"]
    return os.path.join(d, sub[0]) if sub else os.path.join(d, "Grass")
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

def park_old():
    """Move every old Blackreach cache file out of all five mods into the backup (append-corruption guard)."""
    total = 0
    for name, suf in SEASONS:
        src = grass_dir(name); dst = os.path.join(OLD, name); os.makedirs(dst, exist_ok=True)
        for f in list(os.listdir(src)):
            if PAT.match(f):
                shutil.move(os.path.join(src, f), os.path.join(dst, f)); total += 1
    print(f"[stage] parked {total} old {WS} cache file(s) in {OLD}")
    return total
def unpark_old():
    n = 0
    for name, suf in SEASONS:
        d = os.path.join(OLD, name)
        if not os.path.isdir(d): continue
        for f in list(os.listdir(d)):
            shutil.move(os.path.join(d, f), os.path.join(grass_dir(name), f)); n += 1
    print(f"[finish] restored {n} old cache file(s)")

def stage():
    assert mo2_closed(), "close MO2 / the game first"
    st = load_state(); backup_inis(st)
    if not st["staged"]:
        park_old()
    set_grasscontrol(WS); set_season(3)      # Default bake convention = summer state (Season Type 3)
    open(TRIGGER, "wb").write(b"")           # empty trigger = nothing done yet in this worldspace
    st["staged"] = True; save_state(st)
    print(f"[stage] Season Type = 3, Only-pregenerate-world-spaces = {WS}, Updating-Cache = true, trigger written")
    print("[stage] now: open MO2, press Play, wait for the game to close itself, close MO2, then run: collect")

def collect():
    assert mo2_closed(), "close MO2 / the game first"
    assert not os.path.exists(TRIGGER), "PrecacheGrass.txt still exists - the run did not finish"
    files = sorted(f for f in (os.listdir(OVR) if os.path.isdir(OVR) else []) if PAT.match(f))
    other = [f for f in (os.listdir(OVR) if os.path.isdir(OVR) else []) if not PAT.match(f)]
    bad = [f for f in files if os.path.getsize(os.path.join(OVR, f)) == 0]
    assert not bad, "zero-byte outputs: " + ", ".join(bad)
    for f in files:
        src = os.path.join(OVR, f)
        for name, suf in SEASONS:
            target = os.path.join(grass_dir(name), f[:-5] + suf + ".cgid")
            assert not os.path.exists(target), "target exists (old file not parked?): " + target
            if suf == "":
                continue
            shutil.copy2(src, target)
        shutil.move(src, os.path.join(grass_dir("Default"), f))
    st = load_state(); st["collected"] = len(files); save_state(st)
    print(f"[collect] {len(files)} cell file(s) -> Default (base) + 4 season copies each")
    if other: print("[collect] left untouched in overwrite\\Grass (not Blackreach):", other[:10])
    if not files: print("[collect] WARNING: nothing generated - the run did not happen or produced no grass")

def finish():
    assert mo2_closed(), "close MO2 / the game first"
    st = load_state()
    if not st.get("collected"):
        unpark_old()
    shutil.copy2(os.path.join(BACKUP, "GrassControl.ini.orig"), GRASS_INI)
    shutil.copy2(os.path.join(BACKUP, "po3_SeasonsOfSkyrim.ini.orig"), SEASON_INI)
    if os.path.exists(TRIGGER): os.remove(TRIGGER); print("[finish] removed leftover PrecacheGrass.txt")
    print("[finish] GrassControl.ini and po3_SeasonsOfSkyrim.ini restored from backup")
    status()

def status():
    st = load_state()
    print("job:", JOB, "| season ini:", SEASON_INI); print("trigger present:", os.path.exists(TRIGGER)); print("state:", json.dumps(st))
    for name, suf in SEASONS:
        d = grass_dir(name)
        cnt = len([f for f in os.listdir(d) if PAT.match(f) and f.lower().endswith(suf.lower() + ".cgid")])
        print(f"  {name:8} {cnt} {WS} file(s)")
    if os.path.isdir(OLD):
        print("  parked old:", sum(len(os.listdir(os.path.join(OLD, n))) for n, _ in SEASONS if os.path.isdir(os.path.join(OLD, n))))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"stage": stage, "collect": collect, "finish": finish}.get(cmd, status)()
