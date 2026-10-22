"""Check every WTHR value in the baby ESL against records_manifest.json (new) and the forward source (old)."""
import os, sys, json, struct
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_esp import parse
from vfs import winner
PROFILE = 'DEEZ CS NUTZ - PICTA x ASTRALITE'
MAN = json.load(open(r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design\finalize\records_manifest.json', encoding='utf-8'))
esl = parse(winner(PROFILE, 'Authoria - Patch - Picta x Astralite.esp')[1])
srcs = {n: parse(winner(PROFILE, n)[1]) for n in ['Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp', 'Authoria - Patch - Picta Seasonal.esp']}
TIMES = {'Sunrise': 0, 'Day': 1, 'Sunset': 2, 'Night': 3}
DIRS = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']
edid2fid = {r['edid']: r['formid'] for r in esl['records']}
mi = {m: i for i, m in enumerate(esl['masters'])}
problems = 0; checked = 0
def rec_by_local(p, local, plugin_masters, want_master):
    for r in p['records']:
        f = int(r['formid'], 16)
        if (f & 0xFFFFFF) == local and r['sig'] == 'WTHR' and plugin_masters[f >> 24] == want_master:
            return r
for key, ov in MAN['overrides'].items():
    local = int(key.split(':')[0], 16)
    rec = rec_by_local(esl, local, esl['masters'], 'Picta - Weathers of Aurbis.esm')
    src = rec_by_local(srcs[ov['forward_from']], local, srcs[ov['forward_from']]['masters'], 'Picta - Weathers of Aurbis.esm')
    dal = [b for s, b in rec['subs'] if s == 'DALC']; sdal = [b for s, b in src['subs'] if s == 'DALC']
    hn = struct.unpack('<4I', [b for s, b in rec['subs'] if s == 'HNAM'][0])
    data = [b for s, b in rec['subs'] if s == 'DATA'][0]
    nn = struct.unpack('<I', [b for s, b in rec['subs'] if s == 'NNAM'][0])[0]
    for op in ov['ops']:
        f = op['field']; checked += 1
        if f.startswith('DirectionalAmbientLightingColors'):
            _, t, d = f.split('.')
            ti = TIMES[t]; di = DIRS.index(d)
            got = list(dal[ti][di*4:di*4+3]); old = list(sdal[ti][di*4:di*4+3])
            if got != op['new'] or old != op['old']:
                problems += 1; print('DALC MISMATCH', key, f, 'got', got, 'new', op['new'], 'srcold', old, 'manold', op['old'])
            if dal[ti][di*4+3] != sdal[ti][di*4+3]:
                problems += 1; print('alpha byte changed', key, f)
        elif f.startswith('VolumetricLighting.'):
            t = f.split('.')[1]
            want = int(edid2fid[op['new']], 16)
            if hn[TIMES[t]] != want:
                problems += 1; print('HNAM MISMATCH', key, t, hex(hn[TIMES[t]]), op['new'], hex(want))
        elif f == 'VisualEffect':
            if nn != int(edid2fid[op['new']], 16):
                problems += 1; print('NNAM MISMATCH', key, hex(nn), op['new'])
        elif f in ('VisualEffectBegin', 'VisualEffectEnd'):
            b = data[15] if f.endswith('Begin') else data[16]
            if abs(b / 255.0 - op['new']) > 1e-6:
                problems += 1; print('VE byte MISMATCH', key, f, b, op['new'])
        elif f == 'SkyStatics':
            tn = [struct.unpack('<I', b)[0] for s, b in rec['subs'] if s == 'TNAM']
            want = [(mi[x.split(':')[1]] << 24) | int(x.split(':')[0], 16) for x in op['new']]
            if tn[-12:] != want:
                problems += 1; print('TNAM MISMATCH', key)
        else:
            problems += 1; print('UNHANDLED', key, f)
    # Night DALC / Night VL untouched
    if dal[3] != sdal[3]:
        problems += 1; print('NIGHT DALC CHANGED', key)
    shn = struct.unpack('<4I', [b for s, b in src['subs'] if s == 'HNAM'][0])
    smast = srcs[ov['forward_from']]['masters']
    def nm(fid, masters, me):
        return (masters[fid >> 24] if (fid >> 24) < len(masters) else me, fid & 0xFFFFFF)
    if nm(hn[3], esl['masters'], 'baby') != nm(shn[3], smast, 'src'):
        problems += 1; print('NIGHT VL CHANGED', key, hex(hn[3]), hex(shn[3]))
print('checked ops', checked, 'problems', problems)
