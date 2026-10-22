"""Merge the ground fit and the bridge-deck fit into one op list for houseCARL. Writes fit_ops_final.json + fit_final.csv."""
import sys, os, pickle, json, csv, struct, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import hits_at
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
na, nf = pickle.load(open('near_refs.pkl', 'rb')); info_all, br = pickle.load(open('bases.pkl', 'rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
res = pickle.load(open('elevated_res.pkl', 'rb'))
ops = json.load(open('fit_ops.json'))
by_id = {o['formid']: o for o in ops}
NAMES = {'animated carriage additional route.esp': 'Animated Carriage Additional Route.esp',
         'animated carriage additional route 0.esp': 'Animated Carriage Additional Route 0.esp',
         'aclinewhiterun.esp': 'ACLine_Whiterun.esp', 'acline_whiterun.esp': 'ACLine_Whiterun.esp',
         'acar_gg markarth outskirts_northern roads compatibility patch.esp': 'ACAR_GG Markarth Outskirts_Northern Roads compatibility patch.esp',
         'acar_jks solitude outskirts compatibility patch.esp': 'ACAR_JKs Solitude Outskirts compatibility patch.esp',
         'authoria - patch - animated carriage nr - no additional routes.esp': 'Authoria - Patch - Animated Carriage NR - No Additional Routes.esp'}
rows = []; kinds = {}
for r in res:
    z = r['nz']; kind = r['kind']
    if not kind.startswith('deck-'):
        zf = hits_at({k: v for k, v in nf.items() if v[1] == r['world']}, info, r['nx'], r['ny'], 'A', sc)
        if not any(abs(h - r['zsrc']) <= 20 for h in zf):
            up = [h for h in zf if r['zsrc'] + 20 < h <= r['zsrc'] + 160]
            if up: z = min(up) + 2; kind = 'raised-onto-deck'
    kinds[kind.split('+')[0]] = kinds.get(kind.split('+')[0], 0) + 1
    fid = '%06X:%s' % (r['g'][1], NAMES[r['g'][0]])
    changed = abs(z - r['z']) > 2 or abs(r['nx'] - r['x']) >= 1 or abs(r['ny'] - r['y']) >= 1
    if changed:
        by_id[fid] = {'formid': fid, 'field_path': 'Placement.Position', 'value': '%.4f, %.4f, %.4f' % (r['nx'], r['ny'], z)}
    elif fid in by_id:
        del by_id[fid]
    rows.append([fid, r['src'], kind, round(r['z'], 1), round(z, 1), round(z - r['z'], 1)])
final = list(by_id.values())
json.dump(final, open('fit_ops_final.json', 'w'), indent=0)
with open('fit_final_bridges.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['formid', 'source', 'decision', 'z_now', 'z_new', 'dz']); w.writerows(rows)
print(kinds); print('total ops', len(final))
for row in rows:
    if row[2].startswith('raised'): print('  raised', row)
