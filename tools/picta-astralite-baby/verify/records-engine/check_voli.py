import json, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_esp import parse
ESL = r'C:\1. AUTHORIA\mods\houseCARL - Authoria - Patch - Picta x Astralite\Authoria - Patch - Picta x Astralite.esp'
MAN = json.load(open(r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design\finalize\records_manifest.json', encoding='utf-8'))
ver = json.load(open(os.path.join(HERE, 'voli_versions_DEEZ_CS_NUTZ_-_PBR.json')))
NAMES = dict(CNAM='Intensity', DNAM='CustomColorContribution', ENAM='ColorR', FNAM='ColorG', GNAM='ColorB', HNAM='DensityContribution',
             INAM='DensitySize', JNAM='DensityWindSpeed', KNAM='DensityFallingSpeed', LNAM='PhaseFunctionContribution',
             MNAM='PhaseFunctionScattering', NNAM='SamplingRepartitionRangeFactor')
esl = parse(ESL)
byedid = {r['edid']: r for r in esl['records']}
bad = 0
for r in MAN['new_records']:
    if r['type'] != 'VOLI':
        continue
    fid, plug = r['create_from'].split(':')
    key = '%s|%s' % (plug.lower(), fid)
    win = ver[key][-1]
    rec = byedid[r['editorid']]
    subs = dict(rec['subs'])
    order = [s for s, _ in rec['subs']]
    src_order = [s for s in win['subs']]
    diffs = []
    for s in set(list(subs) + list(win['subs'])):
        if s == 'EDID':
            continue
        a = subs.get(s); b = win['subs'].get(s)
        ah = a.hex() if a is not None else None
        bh = b[0] if b is not None else None
        if ah != bh:
            diffs.append((s, NAMES.get(s), struct.unpack('<f', a)[0] if a and len(a) == 4 else ah, b[1] if b else None))
    exp_int = r['set']['Intensity']; exp_rng = r['set']['SamplingRepartitionRangeFactor']
    got_int = struct.unpack('<f', subs['CNAM'])[0]; got_rng = struct.unpack('<f', subs['NNAM'])[0]
    ok_set = abs(got_int - exp_int) < 1e-6 and abs(got_rng - exp_rng) < 1e-6
    unexpected = [d for d in diffs if d[0] not in ('CNAM', 'NNAM')]
    if unexpected or not ok_set:
        bad += 1
    print(r['editorid'], rec['formid'], 'src', key, 'winner', win['plugin'], '| set ok' if ok_set else '| SET MISMATCH',
          'Int=%.6f Rng=%.3f' % (got_int, got_rng), '| other diffs:', unexpected, '| suborder', order[1:] == src_order)
print('BAD', bad)
