"""Read-only E11 value reader with the engine's own semantics (Bottled 4ca678b SettingManager.cpp):
GetPrivateProfileStringA (first section / first key, case-insensitive), registration defaults and clamps, bare key fills
all periods, per-period keys override, weather file falls back per period to the base (ResolveWeatherValue)."""
import ctypes, re, os
import numpy as np

SRC = r'C:\1. AUTHORIA\_tools\picta-astralite-baby\map\e11-colour-model\src_4ca678b\src\Features\Effects11\EffectManager.cpp'
PER = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']
_k32 = ctypes.windll.kernel32
_GPPS = _k32.GetPrivateProfileStringA
_GPPS.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p]
_GPPS.restype = ctypes.c_uint32


def gpps(path, sec, key):
    buf = ctypes.create_string_buffer(256)
    n = _GPPS(sec.encode('mbcs'), key.encode('mbcs'), b'', buf, 256, path.encode('mbcs'))
    return buf.raw[:n].decode('mbcs') if n else None


def _pf(s):
    try:
        v = float(s)
    except ValueError:
        return None
    return v if np.isfinite(v) else None


def _pcol(s, lo, hi):
    parts = s.split(',')
    if len(parts) != 3:
        return None
    out = []
    for p in parts:
        v = _pf(p)
        if v is None:
            return None
        out.append(min(max(v, lo), hi))
    return np.array(out)


REG = {}
for line in open(SRC, encoding='utf-8', errors='replace'):
    m = re.search(r'Register(TimeOfDay|ColorTimeOfDay|Float|Bool)Setting\("(\w+)",\s*"(\w+)",\s*(.*)\);', line)
    if not m:
        continue
    kind, key, cat, rest = m.groups()
    if kind == 'ColorTimeOfDay':
        c = re.match(r'\{\s*([-\d.]+)f?,\s*([-\d.]+)f?,\s*([-\d.]+)f?\s*\}', rest)
        REG[(cat, key)] = dict(kind=kind, default=np.array([float(c.group(i)) for i in (1, 2, 3)]), lo=0.0, hi=10.0)
    elif kind in ('TimeOfDay', 'Float'):
        a = [x.strip().rstrip('f') for x in rest.split(',')]
        REG[(cat, key)] = dict(kind=kind, default=float(a[0]), lo=float(a[1]) if len(a) > 1 else 0.0, hi=float(a[2]) if len(a) > 2 else 10.0)


def _load(path, cat, key, start):
    """LoadSettingFromFile: returns (per-period values, defined mask)."""
    r = REG[(cat, key)]
    vals = [np.array(v, float) if r['kind'] == 'ColorTimeOfDay' else float(v) for v in start]
    mask = [False] * 8
    s = gpps(path, cat, key)
    if s is not None:
        v = _pcol(s, r['lo'], r['hi']) if r['kind'] == 'ColorTimeOfDay' else _pf(s)
        if v is not None:
            if r['kind'] != 'ColorTimeOfDay':
                v = min(max(v, r['lo']), r['hi'])
            vals = [v] * 8
            mask = [True] * 8
    for i, p in enumerate(PER):
        s = gpps(path, cat, key + p)
        if s is None:
            continue
        v = _pcol(s, r['lo'], r['hi']) if r['kind'] == 'ColorTimeOfDay' else _pf(s)
        if v is None:
            continue
        if r['kind'] != 'ColorTimeOfDay':
            v = min(max(v, r['lo']), r['hi'])
        vals[i] = v
        mask[i] = True
    return vals, mask


class E11:
    def __init__(self, base_ini, weather_ini=None):
        self.base, self.w = base_ini, weather_ini
        self.cache = {}

    def get(self, cat, key):
        """resolved per-period values for this weather (dict period -> value)."""
        ck = (cat, key)
        if ck in self.cache:
            return self.cache[ck]
        r = REG[ck]
        d = r['default']
        bvals, _ = _load(self.base, cat, key, [d] * 8)
        vals = bvals
        if self.w is not None:
            wv, mask = _load(self.w, cat, key, bvals)
            vals = [wv[i] if mask[i] else bvals[i] for i in range(8)]
        out = {p: vals[i] for i, p in enumerate(PER)}
        self.cache[ck] = out
        return out


def tod_weights(h, T):
    """EffectManager.cpp 916-985."""
    h = min(max(h % 24, 0.0), 24.0)
    nt, sr, dd, dt, ss, ud = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    tp = [nt, sr - dd, sr - dd * 0.5, sr, dt, ss, ss + ud * 0.5, ss + ud]
    tp = tp + [x + 24 for x in tp]
    fm = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0
    cpt, npt = 0.0, 24.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt:
            ci, cpt = i, t
        if t > h and npt >= t:
            ni, npt = i, t
    cf, nf = fm[ci % 8], fm[ni % 8]
    td = abs(npt - cpt) or 1.0
    b = abs(h - cpt) / td
    f = {p: 0.0 for p in PER[:6]}
    if cf == nf:
        f[cf] = 1.0
    else:
        f[cf] = min(1, max(0, 1 - b))
        f[nf] = min(1, max(0, b))
    pd = min(1.0, max(0.0, f['Day'] ** 0.6))
    if pd > 1.17549435e-38:
        if f['Sunrise'] > 1.17549435e-38:
            f['Sunrise'] = min(1, max(0, 1 - pd))
        if f['Sunset'] > 1.17549435e-38:
            f['Sunset'] = min(1, max(0, 1 - pd))
    f['Day'] = pd
    return f
