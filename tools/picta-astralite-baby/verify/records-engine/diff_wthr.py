"""Byte-level, master-remapped diff of every baby WTHR against its forward source plugin's version."""
import os, sys, struct, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_esp import parse
from vfs import winner
PROFILE = 'DEEZ CS NUTZ - PICTA x ASTRALITE'
BABY = 'Authoria - Patch - Picta x Astralite.esp'
FID1 = {'MNAM', 'NNAM', 'TNAM', 'GNAM'}
FID4 = {'IMSP', 'HNAM'}
TIMES = ['Sunrise', 'Day', 'Sunset', 'Night']
DALC_NAMES = ['XPlus', 'XMinus', 'YPlus', 'YMinus', 'ZPlus', 'ZMinus', 'Specular', 'Fresnel']
DATA_NAMES = ['WindSpeed', 'unk1', 'unk2', 'TransDelta', 'SunGlare', 'SunDamage', 'PrecipBeginFadeIn', 'PrecipEndFadeOut',
              'ThunderBeginFadeIn', 'ThunderEndFadeOut', 'ThunderFreq', 'Flags', 'LightR', 'LightG', 'LightB',
              'VisualEffectBegin', 'VisualEffectEnd', 'WindDir', 'WindDirRange']

def load(name):
    w = winner(PROFILE, name)
    return parse(w[1]), w

def norm_fid(fid, masters, self_name):
    idx = fid >> 24
    if fid == 0:
        return None
    if idx < len(masters):
        return (masters[idx], fid & 0xFFFFFF)
    return (self_name, fid & 0xFFFFFF)

def norm_rec(rec, masters, self_name):
    out = []
    for s, b in rec['subs']:
        if s in FID1:
            out.append((s, norm_fid(struct.unpack('<I', b)[0], masters, self_name)))
        elif s in FID4:
            out.append((s, tuple(norm_fid(x, masters, self_name) for x in struct.unpack('<4I', b))))
        elif s == 'SNAM':
            f, t = struct.unpack('<II', b)
            out.append((s, (norm_fid(f, masters, self_name), t)))
        else:
            out.append((s, b))
    return out

baby, bw = load(BABY)
srcs = {}
for n in ['Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp', 'Authoria - Patch - Picta Seasonal.esp']:
    srcs[n] = load(n)
report = {}
for rec in baby['records']:
    if rec['sig'] != 'WTHR':
        continue
    key = norm_fid(int(rec['formid'], 16), baby['masters'], BABY)
    src_name = 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp' if key[1] >> 12 == 0x19F else 'Authoria - Patch - Picta Seasonal.esp'
    sp, sw = srcs[src_name]
    srec = [r for r in sp['records'] if r['sig'] == 'WTHR' and norm_fid(int(r['formid'], 16), sp['masters'], src_name) == key]
    assert len(srec) == 1, (key, len(srec))
    a = norm_rec(rec, baby['masters'], BABY)
    b = norm_rec(srec[0], sp['masters'], src_name)
    diffs = []
    ca = collections.defaultdict(list); cb = collections.defaultdict(list)
    for s, v in a: ca[s].append(v)
    for s, v in b: cb[s].append(v)
    for s in sorted(set(ca) | set(cb)):
        va, vb = ca[s], cb[s]
        if s == 'TNAM':
            added = [x for x in va if x not in vb]; removed = [x for x in vb if x not in va]
            if added or removed or [x for x in va if x in vb] != vb:
                diffs.append({'sub': 'TNAM', 'added': ['%06X:%s' % (x[1], x[0]) for x in added], 'removed': removed,
                              'order_of_existing_kept': [x for x in va if x in vb] == vb, 'count_src': len(vb), 'count_baby': len(va),
                              'added_at_end': va[:len(vb)] == vb})
            continue
        if va == vb:
            continue
        if s == 'DALC':
            for ti in range(max(len(va), len(vb))):
                x = va[ti] if ti < len(va) else None; y = vb[ti] if ti < len(vb) else None
                if x == y: continue
                det = []
                for ci in range(8):
                    xx = x[ci*4:ci*4+4] if x else None; yy = y[ci*4:ci*4+4] if y else None
                    if xx != yy:
                        if ci == 7:
                            det.append((DALC_NAMES[ci], struct.unpack('<f', yy)[0] if yy else None, struct.unpack('<f', xx)[0] if xx else None))
                        else:
                            det.append((DALC_NAMES[ci], list(yy) if yy else None, list(xx) if xx else None))
                diffs.append({'sub': 'DALC', 'time': TIMES[ti], 'changes(src->baby)': det})
        elif s == 'DATA':
            x = va[0]; y = vb[0]
            det = [(DATA_NAMES[i], y[i], x[i]) for i in range(len(x)) if x[i] != y[i]]
            diffs.append({'sub': 'DATA', 'changes(src->baby)': det, 'len': (len(y), len(x))})
        elif s == 'HNAM' or s == 'IMSP':
            x = va[0]; y = vb[0]
            det = [(TIMES[i], '%06X:%s' % (y[i][1], y[i][0]) if y[i] else None, '%06X:%s' % (x[i][1], x[i][0]) if x[i] else None) for i in range(4) if x[i] != y[i]]
            diffs.append({'sub': s, 'changes(src->baby)': det})
        elif s in ('NNAM', 'MNAM', 'GNAM'):
            diffs.append({'sub': s, 'src': ['%06X:%s' % (v[1], v[0]) if v else None for v in vb], 'baby': ['%06X:%s' % (v[1], v[0]) if v else None for v in va]})
        else:
            diffs.append({'sub': s, 'src': [v.hex() if isinstance(v, bytes) else str(v) for v in vb][:3], 'baby': [v.hex() if isinstance(v, bytes) else str(v) for v in va][:3]})
    seq_a = [s for s, _ in a]; seq_b = [s for s, _ in b]
    seq_note = None
    if [s for s in seq_a if s != 'TNAM'] != [s for s in seq_b if s != 'TNAM']:
        seq_note = {'baby': [s for s in seq_a if s != 'TNAM'], 'src': [s for s in seq_b if s != 'TNAM']}
    report['%06X' % key[1]] = {'edid': rec['edid'], 'src': src_name, 'src_mod': sw[0], 'diffs': diffs, 'subrecord_sequence_mismatch': seq_note}
json.dump(report, open(os.path.join(HERE, 'wthr_diff.json'), 'w'), indent=1, default=str)
for k, v in report.items():
    subs = collections.Counter(d['sub'] for d in v['diffs'])
    print(k, v['edid'], v['src'][:30], dict(subs), 'SEQ MISMATCH' if v['subrecord_sequence_mismatch'] else '')
