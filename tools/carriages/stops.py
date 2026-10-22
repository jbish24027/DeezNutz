"""Clipping scan for Carriage Stops of Skyrim (+ ACTYE bench moves)."""
import sys, os, math, pickle, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plug import Plugin, subs
from lo import resolve
from refpos import iter_world_refs
from scanmod import scan

M = r'C:/1. AUTHORIA/mods/'
OWN = ('simplecarriageexpansion.esp', 'animated carriages take you everywhere.esp')
stop_refs = {}
for f in [M + 'Carriage Stops of Skyrim/simpleCarriageExpansion.esp', M + 'Animated Carriages Take You Everywhere/Animated Carriages Take You Everywhere.esp']:
    for r in iter_world_refs(f):
        if r['gid'][0] in OWN: stop_refs[r['gid']] = r
tg = set()
for r in stop_refs.values():
    x, y = r['pos'][:2]
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1): tg.add((r['world'], (math.floor(x / 4096) + dx, math.floor(y / 4096) + dy)))
lo = resolve('DEEZ CS NUTZ - PICTA')
AUTH = {'skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm', 'unofficial skyrim special edition patch.esp'}
author, final = {}, {}
for p, path in lo:
    if not path: continue
    if p.lower() in AUTH: scan(path, author, p, tg)
    scan(path, final, p, tg)
# carriage stops may not see everything persistent; fine for clutter
paths = {p.lower(): path for p, path in lo if path}
# base names
need = {v[3] for v in final.values()} | {r['base'] for r in stop_refs.values()}
info = {}
for f in sorted({b[0] for b in need}):
    if f not in paths: continue
    P = Plugin(paths[f])
    for b in need:
        if b[0] == f and b in P.recs:
            v = P.recs[b]; d = dict(subs(v[3])); info[b] = (v[0], v[1], d.get('MODL', b'').rstrip(b'\0').decode('cp1252', 'replace'))
# cluster stop objects into stops
stops = []
for g, r in stop_refs.items():
    for s in stops:
        if s['world'] == r['world'] and any(math.dist(r['pos'][:2], q['pos'][:2]) < 900 for q in s['objs']):
            s['objs'].append(r); break
    else:
        stops.append(dict(world=r['world'], objs=[r]))
SKIP_T = {'SOUN', 'LIGH', 'ASPC', 'TXST', 'IDLM'}
report = []
for s in stops:
    hits = {}
    names = sorted({info.get(o['base'], ('', '?', ''))[1] for o in s['objs']})
    for o in s['objs']:
        bt = info.get(o['base'], ('', '', ''))
        if bt[0] in ('', 'STAT') and 'marker' in bt[1].lower(): continue
        for k, v in final.items():
            if k[0] in OWN or v[4] or v[6] or v[1] != o['world']: continue
            if v[2][2] < -29000: continue
            if math.dist(v[2][:2], o['pos'][:2]) > 220 or abs(v[2][2] - o['pos'][2]) > 300: continue
            a = author.get(k)
            if a is not None and a[2][:3] == v[2][:3] and a[3] == v[3]: continue
            bi = info.get(v[3], ('?', '?', ''))
            if bi[0] in SKIP_T or 'marker' in (bi[1] + bi[2]).lower() or bi[0] == '?': continue
            if bi[0] in ('GRAS',): continue
            hits[k] = (v[0], bi[0], bi[1], round(math.dist(v[2][:2], o['pos'][:2])), round(v[2][2] - o['pos'][2]))
    cx = sum(o['pos'][0] for o in s['objs']) / len(s['objs']); cy = sum(o['pos'][1] for o in s['objs']) / len(s['objs'])
    report.append(dict(world=s['world'][1], center=(round(cx), round(cy)), n=len(s['objs']), names=names[:6], hits=sorted(hits.values(), key=lambda h: h[3])))
pickle.dump(report, open('stops_report.pkl', 'wb'))
print(len(stops), 'stops')
for r in sorted(report, key=lambda r: -len(r['hits'])):
    print('== stop at', r['center'], 'world', r['world'], 'objects', r['n'], r['names'][:4])
    for h in r['hits'][:8]: print('     ', h)
