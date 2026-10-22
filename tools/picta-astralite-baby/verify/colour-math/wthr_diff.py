"""Read-only: field-level diff, Picta winner WTHR vs baby ESL WTHR (both read with houseCARL into jsonl)."""
import json, os, re, collections
H = os.path.dirname(os.path.abspath(__file__))


def load(fn):
    L = open(os.path.join(H, fn), encoding='utf-8').read().splitlines()[1:]
    out = {}
    for l in L:
        r = json.loads(l)
        out[r['formid'].split(':')[0]] = {f['path']: f.get('value', f.get('note')) for f in r['fields']}
    return out


P = load('picta_wthr_winner.jsonl')
B = load('baby_wthr_esl.jsonl')
cls = collections.Counter()
for w in P:
    p, b = P[w], B[w]
    keys = sorted(set(p) | set(b))
    d = [k for k in keys if p.get(k) != b.get(k)]
    groups = collections.Counter()
    for k in d:
        g = re.sub(r'\[\d+\]', '[]', k)
        g = re.sub(r'\.(Sunrise|Day|Sunset|Night)(\.|$)', r'.<slot>\2', g)
        groups[g] += 1
    other = [k for k in d if not (k.startswith('DirectionalAmbientLightingColors') or k.startswith('VolumetricLighting')
                                  or k.startswith('VisualEffect') or k.startswith('SkyStatics'))]
    night = [k for k in d if '.Night' in k]
    print(w, len(d), dict(groups), 'OTHER:', other[:10], 'NIGHT:', night[:5])
json.dump({'P': P, 'B': B}, open(os.path.join(H, 'wthr_pair.json'), 'w'))
