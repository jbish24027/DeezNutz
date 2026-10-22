"""Install the staged hairline swaps over the graft mod. Dry-run unless --apply. Refuses while MO2 or the game runs."""
import os, sys, json, shutil, subprocess, time
sys.path.insert(0, "C:/1. AUTHORIA/_tools/smp-coverage")
import hairgraft, nifrw
BS = chr(92)
sp = "C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/8714b13a-8cba-4f6e-a284-eaf1cd40c73c/scratchpad"
stage = sp + "/staging/hairline"
mod = "C:/1. AUTHORIA/mods/Authoria - SMP Hair Grafts/meshes/actors/character/facegendata/facegeom"
park = "C:/1. AUTHORIA/_staging/smp-grafts-prehairline-" + time.strftime("%Y%m%d-%H%M")
apply = "--apply" in sys.argv
def lp(p):
    p = os.path.normpath(p)
    return (BS + BS + "?" + BS + p) if len(p) > 240 and not p.startswith(BS + BS + "?") else p
tl = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
running = [x for x in ("modorganizer.exe", "skyrimse.exe") if x in tl]
if running and apply:
    print("REFUSED: still running:", running); sys.exit(2)
rep = json.load(open(sp + "/staging/hairline_report.json"))
files = [d["rel"] for d in rep["done"]]
print("staged files:", len(files), "| failed in staging:", len(rep["failed"]), "| running:", running or "none")
missing = [r for r in files if not os.path.exists(lp(os.path.join(mod, r)))]
print("staged files with no installed counterpart:", len(missing), missing[:5])
if not apply:
    print("dry run only; pass --apply to install"); sys.exit(0)
n = 0
for r in files:
    src, dst = os.path.join(stage, r), os.path.join(mod, r)
    keep = os.path.join(park, r)
    os.makedirs(lp(os.path.dirname(keep)), exist_ok=True)
    if os.path.exists(lp(dst)):
        shutil.move(lp(dst), lp(keep))
    shutil.copy2(lp(src), lp(dst)); n += 1
print("installed", n, "| old files parked at", park)
# verify a sample + totals
bad = 0
for r in files:
    d = nifrw.Doc(lp(os.path.join(mod, r)))
    if not hairgraft.hair_physics_xml(d): bad += 1
print("verify: installed files lacking the physics tag:", bad)
