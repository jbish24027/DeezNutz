"""Darken v2: give Picta 1.1.2 the GRADE of Picta 1.0.1 (tone curve, gamma, exposure, eye adaptation, bloom mixing), keep 1.1.2's
skies, clouds, colours and fixes. Builds on v1 (the 30 lighting/sky/bloom-intensity keys already scaled to the 1.0.1 averages).

Per weather file 1.1.2 routes (and every other 1.1.2 weather ini): grade keys get the MEDIAN of the category-matched 1.0.1 weather
files (clear->clear, lightly cloudy->lightly cloudy, cloudy, overcast, storm; same rain/snow/fog flags when 1.0.1 has them; a
same-named 1.0.1 file wins outright). Root fx inis (used for any weather the list does not route): per-weather groups get the
median over all routed 1.0.1 exterior files; root-only groups (CG.AGIS, Adaptation.Advanced) get 1.0.1's own root values.
Colour keys (saturation, colour balance, hue, tint) are never touched.

--report: print the mapping + per-key changes only.   --write: rebuild the override mod (MO2 and the game must be closed)."""
import os, sys, re, statistics, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WRITE = '--write' in sys.argv
MODS = r'C:\1. AUTHORIA\mods'
OLD = os.path.join(MODS, '[NoDelete] Picta ENB 1.0.1 - Data (shipped)', 'enbseries')
NEW = os.path.join(MODS, '[NoDelete] Picta ENB 1.1.2 - Data (shipped)', 'enbseries')
DST = os.path.join(MODS, 'Authoria - Picta 1.1.2 - Darkened to 1.0.1', 'enbseries')
GRADE_SECTIONS = ('ENBEFFECT.FX', 'ENBADAPTATION.FX')
COLOUR = re.compile(r'saturat|colou?r balance|hue|tint|vibran', re.I)
def grade_key(sec, k):
    if sec not in GRADE_SECTIONS or COLOUR.search(k): return False
    return k.startswith(('Tonemap.', 'CG.HDR.', 'Adaptation.', 'Bloom Mixing.', 'Bloom Blending.', 'CG.AGIS.'))

def parse(path):
    out = {}; sec = ''
    for ln in open(path, encoding='utf-8', errors='replace'):
        t = ln.strip()
        if not t or t.startswith(';') or t.startswith('//'): continue
        if t.startswith('[') and t.endswith(']'): sec = t[1:-1].upper(); continue
        if '=' in t:
            k, v = t.split('=', 1); out[(sec, k.strip())] = v.strip()
    return out
def routed(root):
    wl = parse(os.path.join(root, '_weatherlist.ini'))
    return sorted({v.replace('/', os.sep) for (s, k), v in wl.items() if k.lower() == 'filename'})
def fnum(v):
    try: return float(v)
    except ValueError: return None
def category(rel):
    n = os.path.basename(rel).lower()
    sky = ('storm' if 'storm' in n else 'overcast' if 'overcast' in n else 'light' if 'lightly_cloudy' in n else
           'cloudy' if 'cloudy' in n else 'clear' if 'clear' in n else None)
    pre = 'snow' if 'snow' in n else 'rain' if ('rain' in n or 'drizzle' in n) else ''
    fog = 'fog' if ('fog' in n or 'mist' in n) else ''
    return sky, pre, fog

old_files = [r for r in routed(OLD) if os.path.exists(os.path.join(OLD, r)) and not r.lower().startswith('picta - interiors')]
old_data = {r: parse(os.path.join(OLD, r)) for r in old_files}
old_by_base = {os.path.basename(r).lower(): r for r in old_files}
def median_over(files, sec, k):
    vs = [fnum(old_data[f][(sec, k)]) for f in files if (sec, k) in old_data[f]]
    vs = [v for v in vs if v is not None]
    return statistics.median(vs) if vs else None
def donors(rel):
    b = os.path.basename(rel).lower()
    if b in old_by_base: return [old_by_base[b]], 'same file'
    sky, pre, fog = category(rel)
    if sky is None: return old_files, 'all 1.0.1 exteriors'
    pool = [f for f in old_files if category(f)[0] == sky]
    for want in ((pre, fog), (pre, None), (None, None)):
        c = [f for f in pool if (want[0] is None or category(f)[1] == want[0]) and (want[1] is None or category(f)[2] == want[1])]
        if c: return c, '%s%s%s x%d' % (sky, '+' + pre if want[0] else '', '+' + fog if want[1] else '', len(c))
    return old_files, 'all 1.0.1 exteriors (no %s match)' % sky

def fmt(orig, val):
    dec = len(orig.split('.')[1]) if '.' in orig else 1
    return ('%.' + str(min(max(dec, 3), 6)) + 'f') % val

def rewrite(src_path, base_path, plan_fn):
    """src = the file to start from (v1 override copy if it exists, else 1.1.2 shipped); plan_fn(sec, key, value) -> new or None"""
    raw = open(src_path, 'rb').read(); eol = b'\r\n' if b'\r\n' in raw else b'\n'
    out = []; sec = ''; n = 0; changes = []
    for ln in raw.split(eol):
        s = ln.decode('utf-8', 'replace'); t = s.strip()
        if t.startswith('[') and t.endswith(']'): sec = t[1:-1].upper(); out.append(ln); continue
        if '=' in t and not t.startswith(';'):
            k, v = t.split('=', 1); k = k.strip(); v = v.strip()
            nv = plan_fn(sec, k, v)
            if nv is not None and fnum(v) is not None and abs(nv - fnum(v)) > 1e-9:
                pre = s[:s.index('=') + 1]; sp = ' ' if s[s.index('=') + 1:s.index('=') + 2] == ' ' else ''
                out.append((pre + sp + fmt(v, nv)).encode('utf-8')); n += 1; changes.append((sec, k, fnum(v), nv)); continue
        out.append(ln)
    return eol.join(out), n, changes

if WRITE:
    tl = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    if 'modorganizer' in tl or 'skyrimse' in tl: sys.exit('MO2 or the game is running - aborting')
total_files = 0; total_vals = 0; summary = {}
new_inis = [os.path.relpath(os.path.join(dp, f), NEW) for dp, dn, fn in os.walk(NEW) for f in fn if f.lower().endswith('.ini')]
for rel in sorted(new_inis):
    base = os.path.basename(rel).lower()
    if base.startswith('_'): continue
    root_level = os.path.dirname(rel) == ''
    if root_level and base not in ('enbeffect.fx.ini', 'enbadaptation.fx.ini'): continue
    if not root_level and rel.lower().startswith('picta - interiors'): continue
    v1 = os.path.join(DST, rel); src = v1 if os.path.exists(v1) else os.path.join(NEW, rel)
    if root_level:
        old_root = parse(os.path.join(OLD, rel)); sec_of = 'ENBEFFECT.FX' if base == 'enbeffect.fx.ini' else 'ENBADAPTATION.FX'
        def plan(sec, k, v, old_root=old_root, sec_of=sec_of):
            if not grade_key(sec_of, k): return None
            if k.startswith(('CG.AGIS.', 'Adaptation.Advanced.')):
                return fnum(old_root.get(('', k), old_root.get((sec, k), ''))) if (('', k) in old_root or (sec, k) in old_root) else None
            return median_over(old_files, sec_of, k)
        how = 'root: 1.0.1 exterior median / own root'
    else:
        d, how = donors(rel)
        def plan(sec, k, v, d=d):
            return median_over(d, sec, k) if grade_key(sec, k) else None
    data, n, ch = rewrite(src, os.path.join(NEW, rel), plan)
    if n:
        total_files += 1; total_vals += n
        summary[rel] = (how, n, ch)
        if WRITE:
            os.makedirs(os.path.dirname(os.path.join(DST, rel)) or DST, exist_ok=True)
            open(os.path.join(DST, rel), 'wb').write(data)
for rel in sorted(summary):
    if rel.lower().startswith('picta - weathers' + os.sep + '00_master') or os.path.dirname(rel) == '':
        how, n, ch = summary[rel]
        day = [c for c in ch if ' Day ' in c[1] and c[1].startswith(('Tonemap.|- Day - UC2 - Linear White', 'CG.HDR.|- Day - Gamma', 'Adaptation.|- Day - Lightness'))]
        print('%-58s %-26s %4d values  %s' % (rel[-58:], how[:26], n, '; '.join('%s %.3g->%.3g' % (c[1].split(' - ')[-1][:18], c[2], c[3]) for c in day[:4])))
print('TOTAL: %d files, %d grade values %s' % (total_files, total_vals, 'written' if WRITE else '(report only)'))
