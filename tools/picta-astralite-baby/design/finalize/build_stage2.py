"""DRY-RUN stage of the baby's two E11-side mods from final_plan.json (reads C:/1. AUTHORIA, writes only to ./stage).

  Authoria - Picta x Astralite - E11   : full fork of every file an Effects 11 editor Save can write, plus the plugin ini
  Authoria - Picta x Astralite - Root twin : copy of the Picta Root twin, Root/enbseries.ini mirrored from the fork

Branch 'alive'   : VL already renders today -> plugin ini byte copy, only routed Dawn..Dusk GVR keys change.
Branch 'newly_on': VL dead today -> plugin ini fVolumetricLightingIntensity=1.0, GVR Intensity 0 for every exterior period
                   of the base ini, the 13 MQ files and the PictaPure B01 copy, and IntensityNight 0 in the 24 routed files.
Usage: python -I -B build_stage.py [alive|newly_on]
VERIFY: only whitelisted (section, key, period) lines differ; no Night/Interior line outside the newly_on list; every
other file md5-identical to its source; line counts and CRLF unchanged; manifest.json written (md5 per output file).
"""
import os, sys, json, shutil, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
MODS = 'C:/1. AUTHORIA/mods'
SRC_DARK = MODS + '/Authoria - Picta 1.1.2 - Darkened to 1.0.1'
SRC_TWIN = MODS + '/Authoria - Picta ENB - Root twin'
EXTRA = [('[NoDelete] Picta ENB 1.1.2 - Data (shipped)', 'enbseries/enbeffectpostpass.fx.ini'),
         ('[NoDelete] Picta ENB 1.1.2 - Data (shipped)', 'enbseries/enblens.fx.ini'),
         ('[NoDelete] Picta ENB 1.1.2 - Data (shipped)', 'enbseries/enbpresetoverlays.ini'),
         ('Authoria - Picta - July Depth of Field (AMON ADOF)', 'enbseries/enbdepthoffield.fx.ini')]
PURE_REL = 'enbseries/Authoria - Picta x Astralite/B01_Lightly_Cloudy_PictaPure.ini'
PURE_WL = 'Authoria - Picta x Astralite/B01_Lightly_Cloudy_PictaPure.ini'
WHITELIST = {('SKY', 'GradientTopColorFilter'), ('SKY', 'GradientHorizonColorFilter'), ('SKY', 'CloudsColorFilter'),
             ('ENVIRONMENT', 'FogColorFilter'), ('ENVIRONMENT', 'DirectLightingColorFilter'),
             ('SKYSCATTERING', 'ScatteringColor'),
             ('GAMEVOLUMETRICRAYS', 'Intensity'), ('GAMEVOLUMETRICRAYS', 'ColorFilter')}
branch = sys.argv[1] if len(sys.argv) > 1 else 'alive'
PLANKEY = {'alive': 'e11_edits', 'newly_on': 'e11_edits_newly_on', 'alive_full': 'e11_edits_full_alive', 'newly_on_full': 'e11_edits_full_newly_on'}[branch]
OUT = os.path.join(HERE, 'stage', branch)
MOD_E11 = OUT + '/Authoria - Picta x Astralite - E11'
MOD_TWIN = OUT + '/Authoria - Picta x Astralite - Root twin'
plan = json.load(open(os.path.join(HERE, 'final2_plan.json'), encoding='utf-8'))

def lp(p):
    bs = chr(92); return bs + bs + '?' + bs + os.path.abspath(p).replace('/', bs)
def md5b(b): return hashlib.md5(b).hexdigest()
def rd(p): return open(lp(p) if len(p) > 200 else p, 'rb').read()
def wr(p, b):
    os.makedirs(lp(os.path.dirname(p)), exist_ok=True); open(lp(p), 'wb').write(b)

if os.path.isdir(lp(OUT)): shutil.rmtree(lp(OUT))
sources = {}   # rel -> source bytes
sources['enbseries.ini'] = rd(SRC_DARK + '/enbseries.ini')
sources['Picta - Weathers of Aurbis.ini'] = rd(SRC_DARK + '/Picta - Weathers of Aurbis.ini')
for root, dirs, files in os.walk(SRC_DARK + '/enbseries'):
    for f in files:
        src = os.path.join(root, f); rel = os.path.relpath(src, SRC_DARK).replace(os.sep, '/')
        sources[rel] = rd(src)
for mod, rel in EXTRA: sources[rel] = rd(MODS + '/' + mod + '/' + rel)
sources[PURE_REL] = sources['enbseries/Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini']   # verbatim Picta B01

def edit_lines(b, edits):
    """edits: list of (section, full_key, new_value). Keeps CRLF, order, comments; returns new bytes + count."""
    txt = b.decode('utf-8'); eol = '\r\n' if '\r\n' in txt else '\n'; lines = txt.split(eol)
    sec = None; idx = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*\[(.+)\]\s*$', ln)
        if m: sec = m.group(1); continue
        if '=' in ln and sec and not ln.lstrip().startswith(';'): idx[(sec, ln.split('=', 1)[0].strip())] = i
    n = 0
    for sec_, key, val in edits:
        i = idx[(sec_, key)]; k = lines[i].split('=', 1)[0]; new = k + '=' + val
        if new != lines[i]: lines[i] = new; n += 1
    return eol.join(lines).encode('utf-8'), n

out = dict(sources)
planned = {}   # rel -> set of (section, key)
fp = plan['files']
for fn, f in fp.items():
    rel = 'enbseries/' + fn
    ed = f[PLANKEY]
    out[rel], n = edit_lines(out[rel], [(e['section'], e['key'], e['new']) for e in ed])
    planned[rel] = {(e['section'], e['key']) for e in ed}
# WEATHER901 -> verbatim B01 copy (the 4 vanilla tundra IDs stay on Picta's B01 values)
wl = out['enbseries/_weatherlist.ini'].decode('utf-8')
wl2 = re.sub(r'(\[WEATHER901\]\r?\nFileName=)Picta - Weathers/00_Master/B01_Lightly_Cloudy\.ini', r'\g<1>' + PURE_WL, wl)
assert wl2 != wl, 'WEATHER901 line not found'
out['enbseries/_weatherlist.ini'] = wl2.encode('utf-8')
NEWLY_ON_ZERO = []
if branch in ('newly_on', 'newly_on_full'):
    pi = out['Picta - Weathers of Aurbis.ini'].decode('utf-8')
    pi2 = re.sub(r'fVolumetricLightingIntensity=0\.0', 'fVolumetricLightingIntensity=1.0', pi); assert pi2 != pi
    out['Picta - Weathers of Aurbis.ini'] = pi2.encode('utf-8')
    mq = [r for r in out if r.startswith('enbseries/Picta - Weathers/01_Skyrim/U01_Skyrim_Main_Quest/') and r.endswith('.ini')]
    for rel in ['enbseries.ini', PURE_REL] + mq:
        ed = [('GAMEVOLUMETRICRAYS', 'Intensity' + p, '0.0') for p in ('Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night')]
        out[rel], n = edit_lines(out[rel], ed); planned[rel] = {(s, k) for s, k, v in ed}; NEWLY_ON_ZERO.append(rel)

# write fork + manifest
manifest = {}
for rel, b in out.items():
    wr(MOD_E11 + '/' + rel, b); manifest[rel] = md5b(b)
json.dump(dict(branch=branch, files=manifest), open(lp(MOD_E11 + '/manifest.json'), 'w'), indent=1)
# Root twin
twin = {}
for root, dirs, files in os.walk(SRC_TWIN):
    for f in files:
        src = os.path.join(root, f); rel = os.path.relpath(src, SRC_TWIN).replace(os.sep, '/'); twin[rel] = rd(src)
twin['Root/enbseries.ini'] = out['enbseries.ini']
for rel, b in twin.items(): wr(MOD_TWIN + '/' + rel, b)

# VERIFY
bad = []; changed_lines = 0; per_file = {}
def keyset(b):
    txt = b.decode('utf-8'); sec = None; d = {}
    for ln in txt.splitlines():
        m = re.match(r'^\s*\[(.+)\]\s*$', ln)
        if m: sec = m.group(1); continue
        if '=' in ln and sec and not ln.lstrip().startswith(';'): d[(sec, ln.split('=', 1)[0].strip())] = ln
    return d
for rel, b in out.items():
    src = sources[rel]
    if rel in planned or rel in ('enbseries/_weatherlist.ini', 'Picta - Weathers of Aurbis.ini'):
        a_, b_ = src.decode('utf-8'), b.decode('utf-8')
        if a_.count('\n') != b_.count('\n') or a_.count('\r\n') != b_.count('\r\n'): bad.append((rel, 'line count / EOL changed')); continue
        ka, kb = keyset(src), keyset(b)
        diff = [k for k in ka if ka[k] != kb.get(k)]
        changed_lines += len(diff); per_file[rel] = len(diff)
        for sec, key in diff:
            if rel == 'enbseries/_weatherlist.ini':
                if not (sec == 'WEATHER901' and key == 'FileName'): bad.append((rel, sec, key))
                continue
            if rel == 'Picta - Weathers of Aurbis.ini':
                if not (branch in ('newly_on', 'newly_on_full') and key == 'fVolumetricLightingIntensity'): bad.append((rel, sec, key))
                continue
            base = re.sub(r'(InteriorDay|InteriorNight|Dawn|Sunrise|Day|Sunset|Dusk|Night)$', '', key)
            per = key[len(base):]
            if (sec, base) not in WHITELIST: bad.append((rel, 'not whitelisted', sec, key)); continue
            if per.startswith('Interior'): bad.append((rel, 'interior touched', key)); continue
            if per == 'Night' and not (branch in ('newly_on', 'newly_on_full') and sec == 'GAMEVOLUMETRICRAYS' and base == 'Intensity'):
                bad.append((rel, 'night touched', key))
            if rel in NEWLY_ON_ZERO and not (sec == 'GAMEVOLUMETRICRAYS' and base == 'Intensity'): bad.append((rel, 'unplanned', key))
    else:
        if md5b(b) != md5b(src): bad.append((rel, 'not byte-identical'))
# twin mirrors
for r in ('Root/enbseries/enbadaptation.fx.ini', 'Root/enbseries/enbbloom.fx.ini', 'Root/enbseries/enbeffect.fx.ini', 'Root/enbseries/enbeffectpostpass.fx.ini'):
    if md5b(twin[r]) != md5b(out[r[len('Root/'):]]): bad.append((r, 'twin mirror differs from fork'))
if md5b(twin['Root/enbseries.ini']) != md5b(out['enbseries.ini']): bad.append(('Root/enbseries.ini', 'twin differs'))
rep = dict(branch=branch, fork_files=len(out), twin_files=len(twin), changed_lines=changed_lines, per_file=per_file,
           newly_on_zeroed=NEWLY_ON_ZERO, verify='PASS' if not bad else bad)
json.dump(rep, open(os.path.join(HERE, f'stage_report_{branch}.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'per_file'}, indent=1))
