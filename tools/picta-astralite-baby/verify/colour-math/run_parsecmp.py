"""Compare every E11 value the colour/VL model uses: engine-semantics reader (GetPrivateProfileStringA + defaults + bare
keys) vs the design's own parser (final_model.parse_ini_E + default_for), Picta and baby files, all 24 routed files."""
import sys, os
sys.dont_write_bytecode = True
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11, PER
D = r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design'
sys.path.insert(0, os.path.join(D, 'final'))
import final_model as fm

KEYS = [('SKY', k) for k in ('GradientIntensity', 'GradientDesaturation', 'GradientTopIntensity', 'GradientTopCurve', 'GradientTopColorFilter',
                             'GradientHorizonIntensity', 'GradientHorizonCurve', 'GradientHorizonColorFilter', 'CloudsIntensity', 'CloudsCurve',
                             'CloudsDesaturation', 'CloudsColorFilter', 'SunIntensity', 'SunDesaturation', 'SunColorFilter', 'ProceduralGradientWeightCurve')]
KEYS += [('SKYSCATTERING', k) for k in ('AtmosphereThickness', 'HorizonRange', 'Intensity', 'Amount', 'DustVolume', 'DustDensity', 'DustDarkening',
                                        'ShadowAmount', 'ColorFromSun', 'ScatteringColor', 'AirGlowIntensity', 'AirGlowRange', 'SunGlowIntensity',
                                        'SunGlowRange', 'CloudsLightingSunMultiplier', 'CloudsLightingSunMinIntensity', 'CloudsLightingDesaturation')]
KEYS += [('ENVIRONMENT', k) for k in ('DirectLightingIntensity', 'DirectLightingCurve', 'DirectLightingDesaturation', 'DirectLightingColorFilter',
                                      'DirectLightingColorFilterAmount', 'AmbientLightingIntensity', 'AmbientLightingDesaturation', 'FogColorMultiplier',
                                      'FogColorCurve', 'FogColorFilter', 'FogColorFilterAmount')]
KEYS += [('GAMEVOLUMETRICRAYS', k) for k in ('Intensity', 'RangeFactor', 'Desaturation', 'ColorFilter')]
WL = cm.weather_files(cm.FORK)
files = sorted({WL[w] for w in cm.load_records()['P']})
mism = {}
for root in (cm.DARK, cm.FORK):
    base = os.path.join(root, 'enbseries.ini')
    for fn in files:
        mine = E11(base, os.path.join(root, 'enbseries', fn.replace('/', os.sep)))
        Ed, _ = fm.parse_ini_E(os.path.join(root, 'enbseries', fn.replace('/', os.sep)))
        Eb, _ = fm.parse_ini_E(base)
        for cat, key in KEYS:
            mv = mine.get(cat, key)
            for p in PER[:6]:
                dv = Ed.get(cat, {}).get(key, {}).get(p)
                if dv is None:
                    dv = fm.default_for(key)
                if np.max(np.abs(np.asarray(mv[p], float) - np.asarray(dv, float))) > 1e-6:
                    mism.setdefault((cat, key), []).append((os.path.basename(root)[:22], fn.split('/')[-1], p, np.round(mv[p], 4).tolist(), np.round(dv, 4).tolist() if np.ndim(dv) else dv))
for k, v in mism.items():
    print(k, len(v), v[:3])
print('settings with a reader mismatch:', len(mism))
