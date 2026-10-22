"""Authoria lighting overlay for the Picta-on-Bottled lane (2026-10-15/16).

Runs as the LAST stage of picta_darken_v3_full.py (imported there) and extends its plan with:
  1. base enbseries.ini: [WEATHER] EnableLocationWeather=true  (Effects 11 reads enbseries\\_locationweather.ini only then)
  2. enbseries\\_locationweather.ini: ONE section [0] (= interior cells, no worldspace) of bare `<location id, low 24 bits>=<fake id>`
     lines (no inline comments: Effects 11 reads the section through the Windows profile API, whose buffer is 32 KB; names live
     in _locationweather.readme.txt). AA001 house-like, AA004 inn, AA007 dungeon - Picta's own 1.0.1 fake ids - generated from
     overlay\\interior_locations.json (a houseCARL LCTN census classified by LocType keyword). APStartCell has no Location.
  3. enbseries\\Authoria - Interiors\\{House,Inn,Dungeon}.ini: MINIMAL files that hold only the tuned interior keys. Every key or
     period a routed file omits inherits the live base enbseries.ini (SettingManager per-period definedMask) and every omitted fx
     row inherits the root fx ini (ExtendedEffect baseFloatValue), so the window sky, fog, tonemap and per-hue grade stay today's.
     [BLOOM]/[LENS] are never written: the base ini's IgnoreWeatherSystemInterior=true makes them dead text in a routed file.
  4. enbseries\\Authoria - Summer\\*.ini: copies of the (nudged) sunny master inis with the summer Day deltas, routed by the
     injected summer weather ids 5AFA01.. (records in Authoria - Patch - Picta Seasonal.esp, Picta esm FormID space).
  5. the year-round 'tiny bit Cabbage/AMON' nudge, restricted to the files listed in tune_values.json (global_nudge.files).
  6. enbseries\\_weatherlist.ini: sections WEATHER951/954/957 (interiors) and WEATHER961/963/964 (summer).
Values live in overlay\\tune_values.json so a retune is a JSON edit + `picta_darken_v3_full.py --write` (+ sync_root_twin.py --write).
In-game Effects 11 saves made inside a routed room land in the generated file and are erased by the next --write: copy them
into tune_values.json. Standalone: `python picta_authoria_overlay.py --selftest [--dump]` dry-runs against the live override.
"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OVERLAY_DIR = os.path.join(HERE, 'overlay')
VALUES = os.path.join(OVERLAY_DIR, 'tune_values.json')
LOCATIONS = os.path.join(OVERLAY_DIR, 'interior_locations.json')
SECTION_LIMIT = 32766          # GetPrivateProfileSection buffer ceiling (bytes, non-comment payload of one section)

INTERIOR_FILES = {'house': ('Authoria - Interiors/House.ini', 'AA001'), 'inn': ('Authoria - Interiors/Inn.ini', 'AA004'), 'dungeon': ('Authoria - Interiors/Dungeon.ini', 'AA007')}
INTERIOR_SECTIONS = {'house': 'WEATHER951', 'inn': 'WEATHER954', 'dungeon': 'WEATHER957'}
MASTER_DIR = os.path.join('Picta - Weathers', '00_Master')
# summer: planned master file -> (summer file, list section, weather ids)
SUMMER = [
    ('A01_Clear.ini', 'Authoria - Summer/A01_Clear_Summer.ini', 'WEATHER961', '5AFA01, 5AFA02'),
    ('A02_Clear_Mist.ini', 'Authoria - Summer/A02_Clear_Mist_Summer.ini', 'WEATHER963', '5AFA03'),
    ('B01_Lightly_Cloudy.ini', 'Authoria - Summer/B01_Lightly_Cloudy_Summer.ini', 'WEATHER964', '5AFB01, 5AFB02'),
]

# ---- interior key map: tune_values field -> [(section, key)], in the order the file is written ----------------------
E, F, L, P, VF = 'ENVIRONMENT', 'FIRE', 'LIGHTSPRITE', 'PARTICLE', 'VOLUMETRICFOG'
EB, EE, EA, EP = 'ENBBLOOM.FX', 'ENBEFFECT.FX', 'ENBADAPTATION.FX', 'ENBEFFECTPOSTPASS.FX'
FX_SECTIONS = {EB, EE, EA, EP}            # written as 'Key = value' like Picta's weather files
INTERIOR_KEYS = [
    ('ambient_day', [(E, 'AmbientLightingIntensityInteriorDay')]), ('ambient_night', [(E, 'AmbientLightingIntensityInteriorNight')]),
    ('ambient_desat_day', [(E, 'AmbientLightingDesaturationInteriorDay')]), ('ambient_desat_night', [(E, 'AmbientLightingDesaturationInteriorNight')]),
    ('point_day', [(E, 'PointLightingIntensityInteriorDay')]), ('point_night', [(E, 'PointLightingIntensityInteriorNight')]),
    ('point_curve_day', [(E, 'PointLightingCurveInteriorDay')]), ('point_curve_night', [(E, 'PointLightingCurveInteriorNight')]),
    ('colorpow', [(E, 'ColorPowInteriorDay'), (E, 'ColorPowInteriorNight')]),
    ('fog_color_multiplier', [(E, 'FogColorMultiplierInteriorDay'), (E, 'FogColorMultiplierInteriorNight')]),
    ('fire_day', [(F, 'IntensityInteriorDay')]), ('fire_night', [(F, 'IntensityInteriorNight')]),
    ('fire_curve_day', [(F, 'CurveInteriorDay')]), ('fire_curve_night', [(F, 'CurveInteriorNight')]),
    ('lightsprite_day', [(L, 'IntensityInteriorDay')]), ('lightsprite_night', [(L, 'IntensityInteriorNight')]),
    ('lightsprite_curve', [(L, 'CurveInteriorDay'), (L, 'CurveInteriorNight')]),
    ('particle_day', [(P, 'IntensityInteriorDay')]), ('particle_night', [(P, 'IntensityInteriorNight')]),
    ('particle_lighting_influence', [(P, 'LightingInfluenceInteriorDay'), (P, 'LightingInfluenceInteriorNight')]),
    ('particle_ambient_influence', [(P, 'AmbientInfluenceInteriorDay'), (P, 'AmbientInfluenceInteriorNight')]),
    ('particle_point_influence', [(P, 'PointLightingInfluenceInteriorDay'), (P, 'PointLightingInfluenceInteriorNight')]),
    ('volumetric_fog_opacity', [(VF, 'OpacityInteriorDay'), (VF, 'OpacityInteriorNight')]),
    ('bloom_near_intensity', [(EB, 'Bloom.|- Interior - Near Intensity')]), ('bloom_near_threshold', [(EB, 'Bloom.|- Interior - Near Threshold')]),
    ('bloom_near_feathering', [(EB, 'Bloom.|- Interior - Near Threshold Feathering')]), ('bloom_far_intensity', [(EB, 'Bloom.|- Interior - Far Intensity')]),
    ('bloom_sky_intensity', [(EB, 'Bloom.|- Interior - Sky Intensity')]),
    ('bloom_mixing_intensity', [(EE, 'Bloom Mixing.|- Interior - Intensity')]), ('bloom_mixing_saturation', [(EE, 'Bloom Mixing.|- Interior - Saturation')]),
    ('bloom_blend_amount', [(EE, 'Bloom Blending.|- Interior - Linear Blend Amount')]),
    ('cg_exposure_ev', [(EE, 'CG.HDR.|- Interior - Exposure (in EVs)')]), ('cg_contrast', [(EE, 'CG.HDR.|- Interior - Contrast')]),
    ('cg_saturation', [(EE, 'CG.HDR.|- Interior - Saturation')]), ('cg_gamma', [(EE, 'CG.HDR.|- Interior - Gamma')]),
    ('cg_gamma_correction', [(EE, 'CG.HDR.|- Interior - Gamma Correction')]), ('cg_color_balance', [(EE, 'CG.HDR.|- Interior - Color Balance')]),
    ('cg_tint', [(EE, 'CG.HDR.|- Interior - Tint')]),
    ('uc2_shoulder_strength', [(EE, 'Tonemap.|- Interior - UC2 - Shoulder Strength')]), ('uc2_linear_angle', [(EE, 'Tonemap.|- Interior - UC2 - Linear Angle')]),
    ('uc2_toe_strength', [(EE, 'Tonemap.|- Interior - UC2 - Toe Strength')]), ('uc2_linear_white', [(EE, 'Tonemap.|- Interior - UC2 - Linear White')]),
    ('adaptation_ev', [(EA, 'Adaptation.|- Interior - Exposure Compensation (in EVs)')]),
    ('adaptation_darkness_att', [(EA, 'Adaptation.|- Interior - Darkness Attenuation')]), ('adaptation_lightness_att', [(EA, 'Adaptation.|- Interior - Lightness Attenuation')]),
    ('kisuite_midtone_saturation', [(EP, 'CG.KiSuite.|- Interior - Midtone Saturation')]), ('kisuite_midtone_tint', [(EP, 'CG.KiSuite.|- Interior - Midtone Tint')]),
    ('kisuite_shadow_saturation', [(EP, 'CG.KiSuite.|- Interior - Shadow Saturation')]), ('kisuite_vibrance', [(EP, 'CG.KiSuite.|- Interior - Vibrance')]),
]
INERT_FIELDS = ('bloom_amount',)          # [BLOOM] Amount: dead in a routed file while the base IgnoreWeatherSystemInterior flag is true

def interior_keys():
    return dict(INTERIOR_KEYS)

# ---- ini helpers (byte-preserving, CRLF-safe, keep 'key = value' spacing) -------------------------------------------
def _fmt(v):
    if isinstance(v, str):
        return v
    if isinstance(v, (list, tuple)):
        return ', '.join(_fmt(x) for x in v)
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    s = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    if '.' not in s: s += '.0'
    return s

def _num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def _vec(v):
    try: return [float(x) for x in v.split(',')]
    except (TypeError, ValueError, AttributeError): return None

def edit_ini(data, edits, must_exist=True, label=''):
    """edits: {(SECTION, key): callable(old_str)->new_str | plain value}. Returns (bytes, n_changed)."""
    eol = b'\r\n' if b'\r\n' in data else b'\n'
    out = []; sec = ''; done = set()
    for ln in data.split(eol):
        s = ln.decode('utf-8', 'replace'); t = s.strip()
        if t.startswith('[') and t.endswith(']'):
            sec = t[1:-1].upper(); out.append(ln); continue
        if '=' in t and not t.startswith(';') and not t.startswith('//'):
            k, v = t.split('=', 1); k = k.strip(); v = v.strip()
            e = edits.get((sec, k))
            if e is not None and (sec, k) not in done:
                nv = e(v) if callable(e) else _fmt(e)
                if nv is not None and nv != v:
                    i = s.index('='); sp = ' ' if s[i + 1:i + 2] == ' ' else ''
                    ln = (s[:i + 1] + sp + nv).encode('utf-8')
                done.add((sec, k))
        out.append(ln)
    missing = [k for k in edits if k not in done]
    if missing and must_exist:
        raise AssertionError('overlay %s: keys not found: %s' % (label, missing[:8]))
    return eol.join(out), len(done)

def mul(f):
    return lambda old: (None if _num(old) is None else _fmt(_num(old) * f))

def add(d, cap=None):
    """add d; with cap, never push a value above cap (a value already above cap stays as it is)."""
    def _f(old):
        x = _num(old)
        if x is None: return None
        y = x + d
        if cap is not None: y = min(y, max(x, cap))
        return _fmt(y)
    return _f

def mul_vec(ms, clamp=1.0):
    def _f(old):
        v = _vec(old)
        if v is None or len(v) < 3: return None
        return ', '.join(_fmt(min(clamp, x * m) if clamp else x * m) for x, m in zip(v[:3], ms)) + (', ' + _fmt(v[3]) if len(v) > 3 else '')
    return _f

def add_alpha(d):
    def _f(old):
        v = _vec(old)
        if v is None or len(v) != 4: return None
        return ', '.join(_fmt(x) for x in v[:3]) + ', ' + _fmt(max(0.0, v[3] + d))
    return _f

# ---- the stages ------------------------------------------------------------------------------------------------------
def load_values():
    with open(VALUES, encoding='utf-8') as f:
        return json.load(f)

def build_locationweather(locs):
    """Bare lines only inside the one [0] section; names go to the readme. Asserts the API ceiling."""
    entries = sorted(locs['locations'], key=lambda e: (e['class'], e['editorid']))
    body = ''.join('%s=%s\r\n' % (e['masked_id'], INTERIOR_FILES[e['class']][1]) for e in entries)
    assert len(body.encode('ascii')) < SECTION_LIMIT - 2, 'location section exceeds the Windows profile-API buffer'
    head = ('; Authoria 2026-10-16: Effects 11 location weather for INTERIORS. The one section [0] = cells with no worldspace.\r\n'
            '; <interior LOCATION FormID, low 24 bits>=<fake weather id>; fake ids are routed in _weatherlist.ini to Authoria - Interiors\\*.ini\r\n'
            '; (AA001 house-like, AA004 inn, AA007 dungeon). No comments inside the section: it is read through a 32 KB API buffer.\r\n'
            '; Names: _locationweather.readme.txt. Generated from _tools\\picta-bridge\\overlay\\interior_locations.json (%s, %d locations).\r\n'
            '[0]\r\n' % (locs.get('generated'), len(entries)))
    readme = ['Authoria interior routing (Effects 11 _locationweather.ini), generated %s from a houseCARL LCTN census (%d locations).' % (locs.get('generated'), len(entries)),
              'The AP start room (APStartCell) has no Location and keeps the base enbseries.ini; so does every interior whose location carries no LocType keyword.',
              'Entries from ESL-flagged plugins are light-slot dependent: regenerate interior_locations.json after load-order changes.', '']
    for e in entries:
        readme.append('%s=%s  %-9s %s%s' % (e['masked_id'], INTERIOR_FILES[e['class']][1], e['class'], e['editorid'], ' (light plugin)' if e.get('light_plugin') else ''))
    return (head + body).encode('ascii'), ('\r\n'.join(readme) + '\r\n').encode('utf-8')

def build_interior_file(cls, fake, vals):
    """Minimal routed file: only the tuned keys, grouped by section in map order."""
    sections = {}; order = []
    for field, keys in INTERIOR_KEYS:
        if field in INERT_FIELDS or field not in vals or vals[field] is None: continue
        for sec, key in keys:
            if sec not in sections: sections[sec] = []; order.append(sec)
            sections[sec].append((key, vals[field]))
    lines = ['; Authoria interior template (%s), 2026-10-16. MINIMAL overlay: only these keys change; every other key and period inherits the live' % cls,
             '; base enbseries.ini and the root fx inis (Effects 11 per-period inheritance). Routed by _locationweather.ini fake weather id %s.' % fake,
             '; Values: _tools\\picta-bridge\\overlay\\tune_values.json (an in-game Effects 11 save made in a routed room lands HERE and is lost on rebuild).']
    for sec in order:
        lines.append('[%s]' % sec)
        for key, val in sections[sec]:
            lines.append(('%s = %s' if sec in FX_SECTIONS else '%s=%s') % (key, _fmt(val)))
        lines.append('')
    return ('\r\n'.join(lines) + '\r\n').encode('utf-8')

def summer_edits(S):
    e = {}
    pers = ['Day'] + (['Sunrise', 'Sunset'] if S.get('apply_same_to_sunrise_sunset') else [])
    cap = S.get('cg_saturation_cap_day')
    for p in pers:
        m = S.get('direct_intensity_mult_day') if p == 'Day' else S.get('direct_intensity_mult_sunrise_sunset', 1.0)
        if m and m != 1.0: e[(E, 'DirectLightingIntensity' + p)] = mul(m)
        if S.get('direct_desat_day') is not None: e[(E, 'DirectLightingDesaturation' + p)] = S['direct_desat_day']
        am = S.get('ambient_intensity_mult_day')
        if am and am != 1.0: e[(E, 'AmbientLightingIntensity' + p)] = mul(am)
        if S.get('adaptation_ev_delta_day'): e[(EA, 'Adaptation.|- %s - Exposure Compensation (in EVs)' % p)] = add(S['adaptation_ev_delta_day'])
        if S.get('cg_saturation_delta_day'): e[(EE, 'CG.HDR.|- %s - Saturation' % p)] = add(S['cg_saturation_delta_day'], cap)
        if S.get('cg_contrast_delta_day'): e[(EE, 'CG.HDR.|- %s - Contrast' % p)] = add(S['cg_contrast_delta_day'])
        cb = S.get('cg_color_balance_day')
        if cb and list(cb) != [1.0, 1.0, 1.0]: e[(EE, 'CG.HDR.|- %s - Color Balance' % p)] = mul_vec(cb, clamp=None)
        if S.get('cg_tint_day'): e[(EE, 'CG.HDR.|- %s - Tint' % p)] = S['cg_tint_day']
        if S.get('kisuite_midtone_saturation_delta_day'): e[(EP, 'CG.KiSuite.|- %s - Midtone Saturation' % p)] = add(S['kisuite_midtone_saturation_delta_day'])
        if S.get('kisuite_midtone_tint_day'): e[(EP, 'CG.KiSuite.|- %s - Midtone Tint' % p)] = S['kisuite_midtone_tint_day']
        if S.get('kisuite_shadow_tint_day'): e[(EP, 'CG.KiSuite.|- %s - Shadow Tint' % p)] = S['kisuite_shadow_tint_day']
        if S.get('bloom_mixing_delta_day'): e[(EE, 'Bloom Mixing.|- %s - Intensity' % p)] = add(S['bloom_mixing_delta_day'])
        if S.get('sun_color_filter_day'): e[('SKY', 'SunColorFilter' + p)] = S['sun_color_filter_day']
        if S.get('clouds_color_filter_day'): e[('SKY', 'CloudsColorFilter' + p)] = S['clouds_color_filter_day']
    if S.get('ambient_desat_day') is not None: e[(E, 'AmbientLightingDesaturationDay')] = S['ambient_desat_day']
    for p, f in (('Day', 'direct_color_filter_day'), ('Sunrise', 'direct_color_filter_sunrise'), ('Sunset', 'direct_color_filter_sunset')):
        if S.get(f): e[(E, 'DirectLightingColorFilter' + p)] = S[f]
    return e

def nudge_edits(G):
    periods = [p for p in G.get('periods_affected', []) if p in ('Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night')]
    gl = {}
    for p in periods:
        if G.get('cg_saturation_delta'): gl[(EE, 'CG.HDR.|- %s - Saturation' % p)] = add(G['cg_saturation_delta'], G.get('cg_saturation_cap'))
        if G.get('cg_contrast_delta'): gl[(EE, 'CG.HDR.|- %s - Contrast' % p)] = add(G['cg_contrast_delta'])
        cb = G.get('cg_color_balance')
        if cb and list(cb) != [1.0, 1.0, 1.0]: gl[(EE, 'CG.HDR.|- %s - Color Balance' % p)] = mul_vec(cb, clamp=None)
        if G.get('cg_tint_amount_delta'): gl[(EE, 'CG.HDR.|- %s - Tint' % p)] = add_alpha(G['cg_tint_amount_delta'])
        if G.get('kisuite_midtone_saturation_delta'): gl[(EP, 'CG.KiSuite.|- %s - Midtone Saturation' % p)] = add(G['kisuite_midtone_saturation_delta'])
        kt = G.get('kisuite_midtone_tint')
        if kt and kt[3] > 0: gl[(EP, 'CG.KiSuite.|- %s - Midtone Tint' % p)] = kt
        if G.get('kisuite_shadow_saturation_delta'): gl[(EP, 'CG.KiSuite.|- %s - Shadow Saturation' % p)] = add(G['kisuite_shadow_saturation_delta'])
        if G.get('bloom_mixing_delta'): gl[(EE, 'Bloom Mixing.|- %s - Intensity' % p)] = add(G['bloom_mixing_delta'])
        if G.get('bloom_mixing_saturation_delta'): gl[(EE, 'Bloom Mixing.|- %s - Saturation' % p)] = add(G['bloom_mixing_saturation_delta'])
        if G.get('adaptation_ev_delta'): gl[(EA, 'Adaptation.|- %s - Exposure Compensation (in EVs)' % p)] = add(G['adaptation_ev_delta'])
        dm = G.get('direct_color_filter_day_rgb_multipliers')
        if dm and list(dm) != [1.0, 1.0, 1.0]: gl[(E, 'DirectLightingColorFilter%s' % p)] = mul_vec(dm, clamp=1.0)
    return gl, periods

def apply(plan, DST, DSTM, NEW, log=print):
    """plan: list of (dst_path, bytes, how, changes, rel). Returns the extended plan."""
    V = load_values()
    with open(LOCATIONS, encoding='utf-8') as f:
        locs = json.load(f)
    by_rel = {p[4].replace('/', os.sep).lower(): i for i, p in enumerate(plan)}
    def get(rel):
        i = by_rel.get(rel.replace('/', os.sep).lower())
        if i is None: raise AssertionError('overlay: planned file missing: ' + rel)
        return i
    def put(i, data, tag):
        dst, _, how, ch, rel = plan[i]
        plan[i] = (dst, data, how, ch + [('OVERLAY', tag, 0, 1)], rel)
    added = []

    # 5. global nudge first (summer copies derive from nudged masters), only on the listed files
    G = V.get('global_nudge') or {}
    gl_edits, periods = nudge_edits(G)
    files = [f.replace('/', os.sep).lower() for f in G.get('files', [])]
    nudged = 0
    if gl_edits and files:
        for rel in files:
            i = get(rel)
            data2, n = edit_ini(plan[i][1], gl_edits, must_exist=True, label=rel)
            put(i, data2, 'global nudge'); nudged += 1
    log('overlay: global nudge on %d files (%s; %d keys per period)' % (nudged, ', '.join(periods) or 'no periods', len(gl_edits) // max(1, len(periods))))

    # 3. interiors (minimal files)
    for cls, (rel, fake) in INTERIOR_FILES.items():
        data = build_interior_file(cls, fake, V['interiors'][cls])
        n = data.count(b'=')
        added.append((os.path.join(DST, rel.replace('/', os.sep)), data, 'authoria interior', [('OVERLAY', cls, 0, 1)] * n, rel.replace('/', os.sep)))
    log('overlay: 3 minimal interior files (%d keys each; [BLOOM]/[LENS] omitted as inert)' % sum(len(k) for _, k in INTERIOR_KEYS))

    # 4. summer copies
    se = summer_edits(V['summer']['e11'])
    for src, rel, section, ids in SUMMER:
        data = plan[get(os.path.join(MASTER_DIR, src))][1]
        data2, n = edit_ini(data, se, must_exist=True, label=rel)
        hdr = ('; Authoria summer variant 2026-10-16 of %s (warm sunny Day rows only; overlay/tune_values.json). Weather ids %s = PIC_WTHR_SUMMER_* injected into the Picta esm by Authoria - Patch - Picta Seasonal.esp.\r\n' % (src, ids)).encode('utf-8')
        added.append((os.path.join(DST, rel.replace('/', os.sep)), hdr + data2, 'authoria summer', [('OVERLAY', 'summer', 0, 1)] * n, rel.replace('/', os.sep)))
    log('overlay: %d summer files (%d edited keys each)' % (len(SUMMER), len(se)))

    # 2. location weather file (+ readme)
    lw, readme = build_locationweather(locs)
    added.append((os.path.join(DST, '_locationweather.ini'), lw, 'authoria interiors map', [('OVERLAY', 'locations', 0, len(locs['locations']))], '_locationweather.ini'))
    added.append((os.path.join(DST, '_locationweather.readme.txt'), readme, 'authoria interiors map', [], '_locationweather.readme.txt'))

    # 6. weather list sections
    i = get('_weatherlist.ini'); wl = plan[i][1]
    secs = []
    for cls, (rel, fake) in INTERIOR_FILES.items():
        name = INTERIOR_SECTIONS[cls]
        assert ('[%s]' % name).encode() not in wl, name
        secs.append('[%s]\r\nFileName=%s\r\nWeatherIDs=%s\r\n' % (name, rel, fake))
    for src, rel, section, ids in SUMMER:
        assert ('[%s]' % section).encode() not in wl, section
        for wid in ids.split(','):
            assert re.search(rb'(?im)^WeatherIDs=.*\b' + wid.strip().encode() + rb'\b', wl) is None, wid
        secs.append('[%s]\r\nFileName=%s\r\nWeatherIDs=%s\r\n' % (section, rel, ids))
    tail = ('\r\n; Authoria 2026-10-16 lighting overlay: interior templates by location (fake ids, see _locationweather.ini) and the summer sunny variants.\r\n' + '\r\n'.join(secs)).encode('utf-8')
    put(i, wl + (b'' if wl.endswith(b'\r\n') else b'\r\n') + tail, 'list sections')

    # 1. base ini gate
    i = get('enbseries.ini')
    data2, n = edit_ini(plan[i][1], {('WEATHER', 'EnableLocationWeather'): 'true'}, must_exist=True, label='enbseries.ini')
    put(i, data2, 'EnableLocationWeather')
    log('overlay: EnableLocationWeather=true, %d list sections, %d location lines' % (len(secs), len(locs['locations'])))
    return plan + added

if __name__ == '__main__' and '--selftest' in sys.argv:
    DSTM = r'C:\1. AUTHORIA\mods\Authoria - Picta 1.1.2 - Darkened to 1.0.1'; DST = os.path.join(DSTM, 'enbseries')
    plan = []
    for dp, dn, fn in os.walk(DST):
        for f in fn:
            p = os.path.join(dp, f); rel = os.path.relpath(p, DST)
            plan.append((p, open(p, 'rb').read(), 'live', [], rel))
    plan.append((os.path.join(DSTM, 'enbseries.ini'), open(os.path.join(DSTM, 'enbseries.ini'), 'rb').read(), 'live', [], 'enbseries.ini'))
    out = apply(plan, DST, DSTM, None)
    print('selftest OK: plan grew from %d to %d files' % (len(plan), len(out)))
    if '--dump' in sys.argv:
        d = os.path.join(OVERLAY_DIR, 'selftest-out'); os.makedirs(d, exist_ok=True)
        for dst, data, how, ch, rel in out:
            if (ch and ch[-1][0] == 'OVERLAY') or how.startswith('authoria'):
                p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(data)
                print('  would write', rel, len(data), 'bytes')
        print('dumped overlay outputs to', d)
