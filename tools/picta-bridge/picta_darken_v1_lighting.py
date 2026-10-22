"""Build 'Authoria - Picta 1.1.2 - Darkened to 1.0.1': copies of the 1.1.2 weather inis whose brightness-driving keys are scaled
down so that, averaged over all weathers, they sit at the 1.0.1 level (keys where 1.1.2 is already darker are left alone).
Only the per-weather inis under enbseries\\ are touched; the base enbseries.ini and the Root twin stay as shipped.
--write creates the mod folder + inserts its (disabled) line above the 1.1.2 Data mod in all 8 modlists; --enable turns it on in
the PICTA + Preset Studio lanes (use together with s15_picta_ab.py to111). Default = dry run."""
import os, sys, re, glob, shutil, statistics
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WRITE = '--write' in sys.argv; ENABLE = '--enable' in sys.argv
INST = r'C:\1. AUTHORIA'; MODS = os.path.join(INST, 'mods')
S13 = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\e4556cce-f5d1-44c7-8bc9-e39b38c252f1\scratchpad\s13'
SRC = os.path.join(MODS, '[NoDelete] Picta ENB 1.1.2 - Data (shipped)')
DST = os.path.join(MODS, 'Authoria - Picta 1.1.2 - Darkened to 1.0.1')
ANCHOR = '[NoDelete] Picta ENB 1.1.2 - Data (shipped)'; NEW = os.path.basename(DST)
SEL = [('ENVIRONMENT', re.compile(r'^(Ambient|Direct|Point|Sky)LightingIntensity')), ('SKY', re.compile(r'^(Clouds|Gradient)Intensity')),
       ('ENBBLOOM.FX', re.compile(r'Intensity'))]

def load(root):
    vals = {}
    for p in glob.glob(os.path.join(root, '**', 'enbseries', '**', '*.ini'), recursive=True):
        if os.path.basename(p).lower().startswith('_'): continue
        sec = ''
        for ln in open(p, encoding='utf-8', errors='replace'):
            ln = ln.strip()
            if ln.startswith('['): sec = ln.strip('[]').upper(); continue
            if '=' in ln and not ln.startswith(';'):
                k, v = ln.split('=', 1)
                try: fv = float(v.strip())
                except ValueError: continue
                vals.setdefault((sec, k.strip()), []).append(fv)
    return vals
old = load(os.path.join(S13, 'e101')); new = load(os.path.join(S13, 'e'))
factors = {}
for (sec, k), vs in new.items():
    if (sec, k) not in old or not any(sec == s and rx.search(k) for s, rx in SEL): continue
    a = statistics.mean(old[(sec, k)]); b = statistics.mean(vs)
    if b > 0 and a > 0 and b > a * 1.02: factors[(sec, k)] = a / b
print('%d keys get darkened (factor = 1.0.1 mean / 1.1.2 mean):' % len(factors))
for (sec, k), f in sorted(factors.items()): print('   [%s] %-42s x%.3f' % (sec, k, f))

def fmt(orig, val):
    dec = len(orig.split('.')[1]) if '.' in orig else 0
    return ('%.' + str(max(dec, 3)) + 'f') % val

changed_files = 0; changed_vals = 0; plan = []
src_inis = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.join(SRC, 'enbseries')) for f in fn if f.lower().endswith('.ini')]  # os.walk: the folder name has [brackets], glob would choke
print('weather inis found in the live 1.1.2 mod:', len(src_inis))
for p in src_inis:
    if os.path.basename(p).lower().startswith('_'): continue
    if os.path.dirname(p).lower() == os.path.join(SRC, 'enbseries').lower(): continue   # root-level fx inis are Root-twinned: leave them
    raw = open(p, 'rb').read(); eol = b'\r\n' if b'\r\n' in raw else b'\n'
    sec = ''; out = []; n = 0
    for ln in raw.split(eol):
        s = ln.decode('utf-8', 'replace'); t = s.strip()
        if t.startswith('['): sec = t.strip('[]').upper(); out.append(ln); continue
        if '=' in t and not t.startswith(';'):
            k, v = t.split('=', 1); key = (sec, k.strip())
            if key in factors:
                try: fv = float(v.strip())
                except ValueError: out.append(ln); continue
                nv = fmt(v.strip(), fv * factors[key]); out.append((s[:s.index('=') + 1] + nv).encode('utf-8')); n += 1; continue
        out.append(ln)
    if n:
        changed_files += 1; changed_vals += n; plan.append((os.path.relpath(p, SRC), eol.join(out)))
print('files with changes: %d  values scaled: %d  (dry run)' % (changed_files, changed_vals) if not WRITE else 'writing...')
if WRITE:
    import subprocess
    if 'modorganizer' in subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower() or 'skyrimse' in subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower():
        sys.exit('MO2 or the game is running - aborting')
    if os.path.isdir(DST): shutil.rmtree(DST)
    for rel, data in plan:
        d = os.path.join(DST, rel); os.makedirs(os.path.dirname(d), exist_ok=True); open(d, 'wb').write(data)
    open(os.path.join(DST, 'meta.ini'), 'wb').write(('[General]\r\nmodid=0\r\nversion=1.0\r\ncomments=Picta ENB 1.1.2 weather inis with the brightness keys scaled down to the 1.0.1 average (%d keys, %d values in %d files). Built 2026-10-12 because the user found the 1.1.x rework too bright. Load directly ABOVE the 1.1.2 Data mod; only meaningful while that mod is enabled. Rebuild with s15_picta_darken.py after any Picta update.\r\n' % (len(factors), changed_vals, changed_files)).encode('utf-8'))
    open(os.path.join(DST, 'README-darkened.txt'), 'wb').write(('Factors (1.0.1 mean / 1.1.2 mean), applied to every weather ini value of that key:\r\n' + ''.join('  [%s] %s x%.3f\r\n' % (s, k, f) for (s, k), f in sorted(factors.items()))).encode('utf-8'))
    print('mod written: %d files, %d values' % (changed_files, changed_vals))
    for ml in sorted(glob.glob(os.path.join(INST, 'profiles', '*', 'modlist.txt'))):
        prof = os.path.basename(os.path.dirname(ml)); raw = open(ml, 'rb').read()
        eol = b'\r\n' if raw.count(b'\r\n') >= raw.count(b'\n') // 2 else b'\n'; trailing = raw.endswith(eol)
        lines = (raw[:-len(eol)] if trailing else raw).split(eol)
        bak = ml + '.bak-darkened-20261012'
        if not os.path.exists(bak): shutil.copy2(ml, bak)
        want = b'+' if (ENABLE and prof in ('DEEZ CS NUTZ - PICTA', 'Authoria - Preset Studio - HPH')) else b'-'
        have = [i for i, l in enumerate(lines) if l[1:] == NEW.encode()]
        if have: lines[have[0]] = want + NEW.encode(); where = have[0]
        else:
            idx = [i for i, l in enumerate(lines) if l[1:] == ANCHOR.encode()]
            if not idx: print('%-36s skipped: no Picta ENB entries in this modlist at all (same as the other Picta folders)' % prof); continue
            assert len(idx) == 1, (prof, idx)
            lines.insert(idx[0], want + NEW.encode()); where = idx[0]
        open(ml, 'wb').write(eol.join(lines) + (eol if trailing else b''))
        print('%-36s %s at line %d (above %s)' % (prof, want.decode(), where + 1, ANCHOR[:30]))
