"""Stage the baby's Effects 11 mod (DRY RUN into scratch by default).

Reads (never writes) the live Picta E11 providers, copies every file an Effects 11 editor Save can write into
<OUT>/<MOD>/ byte-for-byte, then rewrites ONLY the planned colour-filter lines of the 24 routed outdoor weather files
(21 masters + 3 summer).  Each edited line keeps its key, its CRLF ending and Picta's number style.
Usage:  python -I -B build_baby_e11.py [--plan out/e11_rehue_plan_s0.60.json] [--out <dir>]
The real install is the same script with --out pointed at the new mod folder, run only after the user's go-ahead,
with MO2 and the game closed.
"""
import os, sys, json, shutil, hashlib, re

BASE = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/design/picta-safe"
MODS = "C:/1. AUTHORIA/mods"
MOD = "Authoria - Picta x Astralite - E11"
SRC_DARK = MODS + "/Authoria - Picta 1.1.2 - Darkened to 1.0.1"
EXTRA = [  # (provider mod, relative path) for writable E11 files Picta's override does not own
    ("[NoDelete] Picta ENB 1.1.2 - Data (shipped)", "enbseries/enbeffectpostpass.fx.ini"),
    ("[NoDelete] Picta ENB 1.1.2 - Data (shipped)", "enbseries/enblens.fx.ini"),
    ("[NoDelete] Picta ENB 1.1.2 - Data (shipped)", "enbseries/enbpresetoverlays.ini"),
    ("Authoria - Picta - July Depth of Field (AMON ADOF)", "enbseries/enbdepthoffield.fx.ini"),
]
args = sys.argv[1:]
plan_path = BASE + "/out/e11_rehue_plan_s0.60.json"
out_root = BASE + "/stage"
if '--plan' in args: plan_path = args[args.index('--plan') + 1]
if '--out' in args: out_root = args[args.index('--out') + 1]
if out_root.replace('\\', '/').lower().startswith('c:/1. authoria') and '--i-have-the-go-ahead' not in args:
    sys.exit("refusing to write under C:/1. AUTHORIA without --i-have-the-go-ahead (and MO2 + game closed)")
DST = out_root + "/" + MOD
plan = json.load(open(plan_path, encoding='utf-8'))['e11']

def lp(p):  # Windows long-path form (scratch paths exceed MAX_PATH)
    bs = chr(92)
    return bs + bs + '?' + bs + os.path.abspath(p).replace('/', bs)
def md5(p): return hashlib.md5(open(lp(p), 'rb').read()).hexdigest()
def fmt(x):
    s = f"{x:.4f}".rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'

if os.path.isdir(lp(DST)): shutil.rmtree(lp(DST))
copied = []
# 1) enbseries.ini + whole enbseries tree from the Darkened override (the plugin INI and README stay in Picta's mod)
os.makedirs(lp(DST), exist_ok=True)
shutil.copy2(SRC_DARK + "/enbseries.ini", lp(DST + "/enbseries.ini")); copied.append(("enbseries.ini", SRC_DARK))
for root, dirs, files in os.walk(SRC_DARK + "/enbseries"):
    for f in files:
        src = os.path.join(root, f); rel = os.path.relpath(src, SRC_DARK).replace('\\', '/')
        os.makedirs(lp(os.path.dirname(DST + "/" + rel)), exist_ok=True); shutil.copy2(src, lp(DST + "/" + rel)); copied.append((rel, SRC_DARK))
for mod, rel in EXTRA:
    src = MODS + "/" + mod + "/" + rel
    os.makedirs(lp(os.path.dirname(DST + "/" + rel)), exist_ok=True); shutil.copy2(src, lp(DST + "/" + rel)); copied.append((rel, mod))

# 2) apply the plan
report = []
for relw, edits in plan.items():
    p = DST + "/enbseries/" + relw
    raw = open(lp(p), 'rb').read(); txt = raw.decode('utf-8'); eol = '\r\n' if '\r\n' in txt else '\n'
    lines = txt.split(eol)
    sec = None; idx = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*\[(.+)\]\s*$', ln)
        if m: sec = m.group(1); continue
        if '=' in ln and sec and not ln.lstrip().startswith(';'):
            idx[(sec, ln.split('=', 1)[0].strip())] = i
    n = 0
    for e in edits:
        i = idx[(e['section'], e['key'])]
        key = lines[i].split('=', 1)[0]
        new = key + "=" + ", ".join(fmt(x) for x in e['new'])
        if new != lines[i]: lines[i] = new; n += 1
    open(lp(p), 'wb').write(eol.join(lines).encode('utf-8'))
    report.append((relw, n, len(edits)))

# 3) verify: every copied file identical to source except the planned lines; nothing else touched
bad = []
for rel, src_mod in copied:
    src = (SRC_DARK if src_mod == SRC_DARK else MODS + "/" + src_mod) + "/" + rel
    dst = DST + "/" + rel
    w = rel[len("enbseries/"):] if rel.startswith("enbseries/") else None
    if w in plan:
        a = open(src, 'rb').read().decode('utf-8').splitlines(); b = open(lp(dst), 'rb').read().decode('utf-8').splitlines()
        if len(a) != len(b): bad.append((rel, 'line count changed')); continue
        changed = [k for k, (x, y) in enumerate(zip(a, b)) if x != y]
        keys = {b[k].split('=', 1)[0] for k in changed}
        planned = {e['key'] for e in plan[w]}
        if not keys <= planned: bad.append((rel, 'unplanned keys changed: ' + str(sorted(keys - planned))))
        if any(re.search(r'(Night|InteriorDay|InteriorNight)$', k) for k in keys): bad.append((rel, 'night/interior key touched'))
    else:
        if md5(src) != md5(dst): bad.append((rel, 'not byte-identical'))
print(f"staged {len(copied)} files into {DST}")
for relw, n, ne in report: print(f"  {relw}: {n} lines rewritten ({ne} planned)")
print("VERIFY:", "PASS - only planned colour-filter lines differ; every other file byte-identical to its Picta source" if not bad else bad)
json.dump(dict(mod=MOD, files=len(copied), edits=report, verify_failures=bad), open(BASE + "/out/stage_report.json", 'w'), indent=1)
