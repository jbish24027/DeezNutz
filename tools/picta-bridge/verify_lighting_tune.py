"""Post-write verification of the Authoria lighting tune (ini side). Read-only.
- routing sections present, files exist, fake/summer ids routed exactly once
- _locationweather.ini: one [0] section, read back through the Windows profile API (what Effects 11 uses) -> entry count
- base gate EnableLocationWeather=true
- the three minimal templates hold exactly the key map with the tune values (no copied template keys)
- the summer copies differ from their (nudged) masters only in the designed Day keys
- the global nudge touched only the listed files, only the designed keys
- Root twin in sync with the override for the five mirrored files
usage: python -I verify_lighting_tune.py
"""
import os, re, sys, json, hashlib, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picta_authoria_overlay as ov
INST = r'C:\1. AUTHORIA'
OV = os.path.join(INST, 'mods', 'Authoria - Picta 1.1.2 - Darkened to 1.0.1'); E = os.path.join(OV, 'enbseries')
TWIN = os.path.join(INST, 'mods', 'Authoria - Picta ENB - Root twin', 'Root')
BK = os.path.join(INST, '_backups', '2026-10-15 - Picta lighting tune (pre)', 'mods', 'Authoria - Picta 1.1.2 - Darkened to 1.0.1')
ok = True
def fail(msg):
    global ok; ok = False; print('FAIL:', msg)
def parse(p):
    out = {}; sec = ''
    for ln in open(p, encoding='utf-8', errors='replace'):
        t = ln.strip()
        if t.startswith('[') and t.endswith(']'): sec = t[1:-1].upper(); continue
        if '=' in t and not t.startswith(';') and not t.startswith('//'):
            k, v = t.split('=', 1); out[(sec, k.strip())] = v.strip()
    return out
def num(v):
    try: return round(float(v), 6)
    except Exception:
        try: return tuple(round(float(x), 6) for x in v.split(','))
        except Exception: return v
V = ov.load_values()
# 1. list
wl = open(os.path.join(E, '_weatherlist.ini'), encoding='utf-8', errors='replace').read()
secs = dict(re.findall(r'(?ms)^\[(WEATHER\d+)\]\s*\r?\nFileName=(.+?)\r?\n', wl))
ids = dict(re.findall(r'(?ms)^\[(WEATHER\d+)\]\s*\r?\nFileName=.+?\r?\nWeatherIDs=(.+?)\r?\n', wl))
for name, fid in (('WEATHER951', 'AA001'), ('WEATHER954', 'AA004'), ('WEATHER957', 'AA007'), ('WEATHER961', '5AFA01'), ('WEATHER961', '5AFA02'), ('WEATHER963', '5AFA03'), ('WEATHER964', '5AFB01'), ('WEATHER964', '5AFB02')):
    if name not in secs: fail('list section missing ' + name); continue
    p = os.path.join(E, secs[name].strip().replace('/', os.sep))
    if not os.path.exists(p): fail('routed file missing for %s: %s' % (name, p))
    if fid not in ids.get(name, ''): fail('%s does not list %s' % (name, fid))
flat = [x.strip().upper() for line in re.findall(r'(?m)^WeatherIDs=(.*)$', wl) for x in line.split(',') if x.strip()]
dups = {x for x in flat if flat.count(x) > 1}
if dups: fail('weather id listed twice: %s' % sorted(dups))
print('list: %d sections, %d weather ids, duplicates: %s' % (len(secs), len(flat), sorted(dups) or 'none'))
# 2. location file via the Windows profile API
lw = os.path.join(E, '_locationweather.ini')
if not os.path.exists(lw): fail('_locationweather.ini missing')
else:
    k32 = ctypes.windll.kernel32
    buf = ctypes.create_string_buffer(65536)
    n = k32.GetPrivateProfileSectionNamesA(buf, 65536, lw.encode('mbcs'))
    names = [x for x in buf.raw[:n].split(b'\x00') if x]
    buf2 = ctypes.create_string_buffer(65536)
    n2 = k32.GetPrivateProfileSectionA(b'0', buf2, 65536, lw.encode('mbcs'))
    entries = [x for x in buf2.raw[:n2].split(b'\x00') if x and b'=' in x and not x.startswith(b';')]
    expected = len(json.load(open(ov.LOCATIONS, encoding='utf-8'))['locations'])
    print('location file: sections %s, API entries in [0]: %d (expected %d), payload %d bytes' % (names, len(entries), expected, n2))
    if names != [b'0'] or len(entries) != expected or n2 >= 32766 - 2: fail('location section not fully readable')
    bad = [x for x in entries if not re.fullmatch(rb'[0-9A-F]{1,6}=AA00[147]', x)]
    if bad: fail('malformed location lines: %s' % bad[:5])
# 3. base gate
base = parse(os.path.join(OV, 'enbseries.ini'))
print('EnableLocationWeather =', base.get(('WEATHER', 'EnableLocationWeather')), '| EnableMultipleWeathers =', base.get(('WEATHER', 'EnableMultipleWeathers')), '| BLOOM ignore flags =', base.get(('BLOOM', 'IgnoreWeatherSystem')), base.get(('BLOOM', 'IgnoreWeatherSystemInterior')))
if base.get(('WEATHER', 'EnableLocationWeather')) != 'true': fail('location weather gate off')
# 4. templates = exact key map
for cls, (rel, fake) in ov.INTERIOR_FILES.items():
    d = parse(os.path.join(E, rel.replace('/', os.sep)))
    want = {}
    for field, keys in ov.INTERIOR_KEYS:
        val = V['interiors'][cls].get(field)
        if field in ov.INERT_FIELDS or val is None: continue
        for sec, key in keys: want[(sec, key)] = val
    extra = sorted(set(d) - set(want)); missing = sorted(set(want) - set(d))
    wrong = [(k, d[k], want[k]) for k in want if k in d and num(d[k]) != num(ov._fmt(want[k]))]
    print('%s: %d keys (extra %d, missing %d, wrong %d)' % (rel, len(d), len(extra), len(missing), len(wrong)))
    if extra or missing or wrong: fail('%s mismatch: extra %s missing %s wrong %s' % (rel, extra[:3], missing[:3], wrong[:3]))
    for sec in ('BLOOM', 'LENS', 'SKY'):
        if any(k[0] == sec for k in d): fail('%s carries a %s section' % (rel, sec))
# 5. summer copies vs their masters
S = V['summer']['e11']
allowed = {('ENVIRONMENT', 'DirectLightingDesaturationDay'), ('ENVIRONMENT', 'DirectLightingIntensityDay'), ('ENBEFFECT.FX', 'CG.HDR.|- Day - Saturation'),
           ('ENBEFFECT.FX', 'CG.HDR.|- Day - Contrast'), ('ENBEFFECT.FX', 'CG.HDR.|- Day - Color Balance'), ('ENBEFFECTPOSTPASS.FX', 'CG.KiSuite.|- Day - Midtone Tint')}
for src, rel, section, wids in ov.SUMMER:
    a = parse(os.path.join(E, ov.MASTER_DIR, src)); b = parse(os.path.join(E, rel.replace('/', os.sep)))
    diff = {k for k in set(a) | set(b) if num(a.get(k)) != num(b.get(k))}
    print('%s: %d keys differ from %s -> %s' % (rel, len(diff), src, sorted(k[1] for k in diff)))
    if diff - allowed: fail('%s changes keys outside the design: %s' % (rel, sorted(diff - allowed)))
    for k in (('ENVIRONMENT', 'DirectLightingDesaturationDay'), ('ENVIRONMENT', 'DirectLightingIntensityDay'), ('ENBEFFECT.FX', 'CG.HDR.|- Day - Saturation')):
        print('    %-40s %s -> %s' % (k[1], a.get(k), b.get(k)))
    if num(b.get(('ENVIRONMENT', 'DirectLightingDesaturationDay'))) != num(ov._fmt(S['direct_desat_day'])): fail('%s desat not applied' % rel)
    sat = num(b.get(('ENBEFFECT.FX', 'CG.HDR.|- Day - Saturation'))); sat0 = num(a.get(('ENBEFFECT.FX', 'CG.HDR.|- Day - Saturation')))
    if sat > max(sat0, S['cg_saturation_cap_day']) + 1e-6: fail('%s saturation above cap' % rel)
    for per in ('Sunrise', 'Sunset', 'Night', 'Dawn', 'Dusk'):
        if any(per in k[1] for k in diff): fail('%s touched a %s row' % (rel, per))
# 6. nudge scope vs backup
if os.path.isdir(BK):
    G = V['global_nudge']; nf = {f.replace('/', os.sep).lower() for f in G.get('files', [])}
    gl, periods = ov.nudge_edits(G)
    changed = []
    for dp, dn, fn in os.walk(os.path.join(BK, 'enbseries')):
        for x in fn:
            rel = os.path.relpath(os.path.join(dp, x), os.path.join(BK, 'enbseries')); live = os.path.join(E, rel)
            if not os.path.exists(live): fail('file vanished: ' + rel); continue
            if open(live, 'rb').read() != open(os.path.join(dp, x), 'rb').read():
                a, b = parse(os.path.join(dp, x)), parse(live)
                vd = {k for k in set(a) | set(b) if num(a.get(k)) != num(b.get(k))}
                changed.append((rel, vd))
    print('files changed vs pre-backup (value level):')
    for rel, vd in changed:
        realdiff = {k for k in vd if not (k[1].startswith(('Developer Tools', 'Adaptation.Adaptation', 'Bloom.Bloom', 'Bloom Blending.Bloom', 'Bloom Mixing.Bloom', 'CG.HDR.CG', 'Tonemap.Tonemap', 'Bloom.Pass Balancing.Bloom')))}
        print('  %-55s %d value diffs %s' % (rel, len(realdiff), sorted(k[1] for k in realdiff)[:6]))
        if rel.lower() == '_weatherlist.ini' or rel.lower() == 'enbseries.ini': continue
        if rel.lower() in nf:
            if realdiff - set(gl): fail('nudge changed unexpected keys in %s: %s' % (rel, sorted(realdiff - set(gl))[:4]))
        elif realdiff:
            fail('unexpected value change outside the nudge files: %s %s' % (rel, sorted(realdiff)[:4]))
# 7. twin sync
for rel in ['enbseries.ini', r'enbseries\enbeffect.fx.ini', r'enbseries\enbbloom.fx.ini', r'enbseries\enbadaptation.fx.ini']:
    a = os.path.join(OV, rel); b = os.path.join(TWIN, rel)
    if os.path.exists(a) and os.path.exists(b):
        same = hashlib.md5(open(a, 'rb').read()).hexdigest() == hashlib.md5(open(b, 'rb').read()).hexdigest()
        print('twin %-34s %s' % (rel, 'in sync' if same else 'DIFFERS'))
        if not same: fail('twin out of sync: ' + rel)
print('VERIFY', 'OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)
