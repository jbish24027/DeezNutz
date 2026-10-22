"""Restore 'Picta Aurbis - Nordic Winds - Patch.esp' to its recorded slot (directly after Nordic Winds.esp) in the PICTA profile's
plugins.txt (active), loadorder.txt and plugingroups.txt (group Audio - Core). MO2 dropped it when the patch MOD was disabled for
the 1.0.1 test. Idempotent; backups .bak-nordicfix-20261012; refuses to run with MO2/the game open."""
import os, sys, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
PROF = r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ - PICTA'
BASE = 'Nordic Winds.esp'; PATCH = 'Picta Aurbis - Nordic Winds - Patch.esp'
out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
if 'modorganizer' in out or 'skyrimse' in out: sys.exit('MO2 or the game is running - aborting')
JOBS = [('plugins.txt', '*' + BASE, '*' + PATCH), ('loadorder.txt', BASE, PATCH), ('plugingroups.txt', BASE + '|Audio - Core', PATCH + '|Audio - Core')]
for fn, anchor, newline in JOBS:
    path = os.path.join(PROF, fn); raw = open(path, 'rb').read()
    eol = b'\r\n' if raw.count(b'\r\n') >= raw.count(b'\n') // 2 else b'\n'; trailing = raw.endswith(eol)
    lines = (raw[:-len(eol)] if trailing else raw).split(eol)
    present = [i for i, l in enumerate(lines) if l.decode('utf-8', 'replace').lstrip('*') in (PATCH, PATCH + '|Audio - Core')]
    if present:
        i = present[0]
        if fn == 'plugins.txt' and lines[i] != newline.encode(): lines[i] = newline.encode(); print('%-16s starred existing line %d' % (fn, i + 1))
        else: print('%-16s already present at line %d' % (fn, i + 1)); continue
    else:
        idx = [i for i, l in enumerate(lines) if l == anchor.encode()]
        assert len(idx) == 1, (fn, anchor, idx)
        lines.insert(idx[0] + 1, newline.encode()); print('%-16s inserted at line %d (after %s)' % (fn, idx[0] + 2, anchor))
    bak = path + '.bak-nordicfix-20261012'
    if not os.path.exists(bak): shutil.copy2(path, bak)
    open(path, 'wb').write(eol.join(lines) + (eol if trailing else b''))
for fn, anchor, newline in JOBS:
    lines = open(os.path.join(PROF, fn), 'rb').read().split(b'\n')
    i = [k for k, l in enumerate(lines) if l.rstrip(b'\r') == newline.encode()]
    print('verify %-16s %s at line %s' % (fn, 'OK' if len(i) == 1 else 'FAIL', i[0] + 1 if i else '?'))
