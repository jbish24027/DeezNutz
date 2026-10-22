import json, os, re, collections
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
def rows(fn):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return []
    L=open(p,encoding='utf-8').read().splitlines()
    return [json.loads(x) for x in L[1:] if x.strip()]
lane=json.load(open(os.path.join(D,'lanediff.json')))
pbr_idx={n.lower():i for i,n in enumerate(lane['pbr_order'])}
pic_idx={n.lower():i for i,n in enumerate(lane['pic_order'])}
for i,n in enumerate(['skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm']): pbr_idx[n]=-100+i; pic_idx[n]=-100+i
pic_only=set(n.lower() for n in lane['only_pic'])
srcs={'Astralite Weathers.esp':'wthr_src_AstraliteWeathers.jsonl','Astralite ENB.esp':'wthr_src_AstraliteENB.jsonl',
 'Wyrmstooth-Astralite-Weather-Patch.esp':'wthr_src_WyrmAstralite.jsonl','Authoria - Patch - Gray Cowl - Astralite.esp':'wthr_src_GrayCowlAstralite.jsonl',
 'Authoria - Patch - Astralite Dawn Warmth.esp':'wthr_src_DawnWarmth.jsonl','Helios_Astralite.esp':'wthr_src_HeliosAstralite.jsonl'}
src={}
for pl,fn in srcs.items():
    for r in rows(fn): src.setdefault(r['formid'],{})[pl]=r
tree={r['formid']:r for r in rows('wthr_picta_tree.jsonl')}
picw={r['formid']:r for r in rows('wthr_picta_winners.jsonl')}
sets=json.load(open(os.path.join(D,'wthr_sets.json')))
need=collections.defaultdict(list); res={}
for fid in sorted(set(sets['pbr'])):
    t=tree.get(fid); touch=t.get('touchers') if t else None
    common=[p for p in (touch or []) if p.lower() not in pic_only]
    prov=[p for p in common+list(src.get(fid,{})) if p.lower() in pbr_idx]
    if not prov:
        res[fid]={'pbr_winner':None,'note':'no PBR provider found'}; continue
    w=max(prov,key=lambda p:pbr_idx[p.lower()])
    entry={'pbr_winner':w,'pbr_providers':sorted(prov,key=lambda p:pbr_idx[p.lower()])}
    if w in src.get(fid,{}): entry['from']='src'
    elif fid in picw and picw[fid].get('winner')==w: entry['from']='picta_winner'
    else: need[w].append(fid); entry['from']='need'
    res[fid]=entry
json.dump(res,open(os.path.join(D,'wthr_pbr_resolve.json'),'w'),indent=1)
print({k:len(v) for k,v in need.items()})
for k,v in need.items(): print(k, v[:50])
print(collections.Counter(e['pbr_winner'] for e in res.values()))
json.dump(need,open(os.path.join(D,'wthr_need.json'),'w'),indent=1)
