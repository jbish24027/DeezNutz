"""Compute terrain-fit positions for every Animated Carriage route marker.
Outputs fit_ops.json (houseCARL apply ops), fit_report.csv, and prints a summary. Writes nothing to the instance."""
import sys, os, pickle, math, json, struct, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refpos import iter_world_refs
from land import height
from plug import Plugin, subs

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
V = pickle.load(open('land_vanilla.pkl', 'rb')); N = pickle.load(open('land_nr.pkl', 'rb')); P = pickle.load(open('land_picta.pkl', 'rb'))
M = r'C:/1. AUTHORIA/mods/'
F = dict(
    acar=M + 'Animated Carriage Additional Route/Animated Carriage Additional Route.esp',
    acar0=M + 'Animated Carriage Additional Route/Animated Carriage Additional Route 0.esp',
    gg=M + 'Animated Carriage Additional Route - Compatibility Patches/ACAR_GG Markarth Outskirts_Northern Roads compatibility patch.esp',
    jk=M + 'Animated Carriage Additional Route - Compatibility Patches/ACAR_JKs Solitude Outskirts compatibility patch.esp',
    acline=M + 'Animated Carriage/ACLine_Whiterun.esp',
    anr=M + 'Authoria - xEdit Output/Authoria - Patch - Animated Carriage NR - No Additional Routes.esp',
    nr=r'arch/ACNR/Animated Carriage Additional Route NR.esp',
    nr0=r'arch/ACNR/Animated Carriage Additional Route 0 NR.esp',
)
# load order of the providers (earliest first); later wins
ORDER = ['acline', 'acar', 'acar0', 'gg', 'jk', 'anr']
NAME = {k: os.path.basename(v) for k, v in F.items()}
NR_NAME = {'animated carriage additional route nr.esp': 'animated carriage additional route.esp',
           'animated carriage additional route 0 nr.esp': 'animated carriage additional route 0.esp'}

refs = {}      # gid -> {key: refdict}
links = {}     # (key, gid) -> tuple of linked gids
for key in ORDER + ['nr', 'nr0']:
    pl = Plugin(F[key])
    for r in iter_world_refs(F[key]):
        g = r['gid']
        if key in ('nr', 'nr0'):
            g = (NR_NAME.get(g[0], g[0]), g[1])
        refs.setdefault(g, {})[key] = r
        d = dict(subs(pl.raw[r['fid']][3]))
        lk = []
        for t, v in subs(pl.raw[r['fid']][3]):
            if t == 'XLKR':
                kw, ref = struct.unpack('<II', v[:8])
                tg = pl.gid(ref); tg = (NR_NAME.get(tg[0], tg[0]), tg[1])
                lk.append(tg)
        links[(key, g)] = tuple(sorted(lk))
        r['base'] = (NR_NAME.get(r['base'][0], r['base'][0]), r['base'][1]) if r['base'] else None

plan = []; stats = {}; elevated = []
def bump(k): stats[k] = stats.get(k, 0) + 1

for g, prov in refs.items():
    have = [k for k in ORDER if k in prov]
    if not have: continue                 # NR-only records (not in 1.6.4) -> not used
    win = have[-1]; w = prov[win]
    world = w['world']; x, y, z = w['pos'][:3]
    gOur = height(P, world, x, y)
    if gOur is None: bump('no-ground'); continue
    src = 'keep'; nx, ny = x, y
    nrk = 'nr' if g[0] == 'animated carriage additional route.esp' else 'nr0'
    nrr = prov.get(nrk)
    if win in ('acar', 'acar0') and nrr and nrr['base'] == w['base'] and links.get((nrk, g)) == links.get((win, g)) \
            and math.dist(nrr['pos'][:2], (x, y)) < 512:
        nx, ny, nz = nrr['pos'][:3]
        off = nz - height(N, world, nx, ny); src = 'nr'
        gOur = height(P, world, nx, ny)
    elif win in ('acar', 'acar0'):
        off = (z - height(V, world, x, y)); src = 'acar'
        if 0 <= off <= 60: off = max(off - 13, -2)
    else:
        off = z - gOur; src = win          # compat patches / Authoria NR patch / ACLine: author placed it for these mods
    # elevated or sunk markers: bridges, ledges, off-world holding markers -> keep unless the ground under them moved
    if off > 60 or off < -25:
        elevated.append(dict(g=g, win=win, src=src, world=world, x=x, y=y, z=z, nx=nx, ny=ny, zsrc=(nrr['pos'][2] if src == 'nr' else z), off=off, rot=w['pos'][3:]))
        gsrc = height(N if src == 'nr' else V, world, nx, ny) if src in ('nr', 'acar') else gOur
        if abs(gOur - gsrc) < 4:
            nz = (nrr['pos'][2] if src == 'nr' else z); bump('elevated-kept')
        else:
            nz = (nrr['pos'][2] if src == 'nr' else z); bump('elevated-REVIEW')
            src += '+REVIEW'
    else:
        nz = gOur + off
    dz = nz - z; dxy = math.dist((nx, ny), (x, y))
    bump('src:' + src.split('+')[0])
    if abs(dz) <= 2 and dxy < 1:
        bump('unchanged'); continue
    plan.append(dict(g=g, win=win, src=src, world=world, x=x, y=y, z=z, nx=nx, ny=ny, nz=nz, dz=dz, dxy=dxy, rot=w['pos'][3:]))

def fid(g):
    real = {os.path.basename(v).lower(): os.path.basename(v) for v in F.values()}
    real.update({'skyrim.esm': 'Skyrim.esm', 'dragonborn.esm': 'Dragonborn.esm'})
    return '%06X:%s' % (g[1], real[g[0]])

ops = [{'formid': fid(p['g']), 'field_path': 'Placement.Position', 'value': '%.4f, %.4f, %.4f' % (p['nx'], p['ny'], p['nz'])} for p in plan if 'REVIEW' not in p['src']]
json.dump(ops, open('fit_ops.json', 'w'), indent=0)
pickle.dump(elevated, open('elevated.pkl', 'wb')); print('elevated', len(elevated))
with open('fit_report.csv', 'w', newline='') as fh:
    wcsv = csv.writer(fh); wcsv.writerow(['formid', 'winner', 'source', 'world', 'x', 'y', 'z_old', 'z_new', 'dz', 'dxy'])
    for p in plan: wcsv.writerow([fid(p['g']), p['win'], p['src'], p['world'][1], round(p['x']), round(p['y']), round(p['z'], 1), round(p['nz'], 1), round(p['dz'], 1), round(p['dxy'], 1)])
dzs = sorted(abs(p['dz']) for p in plan)
print(stats)
print('changed', len(plan), 'ops', len(ops), 'review', sum('REVIEW' in p['src'] for p in plan))
if dzs: print('|dz| quantiles', [round(dzs[int(len(dzs) * q)], 1) for q in (.25, .5, .75, .9, .99)], 'max', round(dzs[-1], 1))
print('xy moved', sum(p['dxy'] >= 1 for p in plan), 'max', round(max([p['dxy'] for p in plan] or [0]), 1))
for p in sorted(plan, key=lambda p: -abs(p['dz']))[:15]:
    print('  ', fid(p['g']), p['src'], round(p['z']), '->', round(p['nz']), 'dxy', round(p['dxy']))
