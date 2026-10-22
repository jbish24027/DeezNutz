import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
picw={r['formid']:parse_wthr(r) for r in rows('wthr_picta_winners.jsonl') if r.get('fields')}
srcs={'Astralite Weathers.esp':'wthr_src_AstraliteWeathers.jsonl','Astralite ENB.esp':'wthr_src_AstraliteENB.jsonl',
 'Wyrmstooth-Astralite-Weather-Patch.esp':'wthr_src_WyrmAstralite.jsonl','Authoria - Patch - Gray Cowl - Astralite.esp':'wthr_src_GrayCowlAstralite.jsonl',
 'Authoria - Patch - Astralite Dawn Warmth.esp':'wthr_src_DawnWarmth.jsonl','Helios_Astralite.esp':'wthr_src_HeliosAstralite.jsonl'}
src={}
for pl,fn in srcs.items():
    for r in rows(fn): src.setdefault(r['formid'],{})[pl]=parse_wthr(r)
res=json.load(open(os.path.join(D,'wthr_pbr_resolve.json')))
pbrw={}
for fid,e in res.items():
    if e.get('pbr_winner') is None: continue
    if e['from']=='src': a=dict(src[fid][e['pbr_winner']]); 
    else: a=dict(picw[fid])
    a['pbr_winner']=e['pbr_winner']; a['pbr_providers']=e['pbr_providers']
    # editorID in PBR lane = latest provider that has an editorid among src; else picta winner's if same
    pbrw[fid]=a
# also all Astralite-defined / overridden WTHR even if not in a region (for completeness)
for fid,d in src.items():
    if fid not in pbrw:
        # pick latest PBR plugin among src
        order=['Astralite Weathers.esp','Astralite ENB.esp','Wyrmstooth-Astralite-Weather-Patch.esp','Helios_Astralite.esp','Authoria - Patch - Gray Cowl - Astralite.esp','Authoria - Patch - Astralite Dawn Warmth.esp']
        w=[p for p in order if p in d][-1]
        a=dict(d[w]); a['pbr_winner']=w; a['pbr_providers']=[p for p in order if p in d]; a['note']='not referenced by any PBR region winner (may be a climate/script/scene weather)'
        pbrw[fid]=a
json.dump({'pic':picw,'pbr':pbrw},open(os.path.join(D,'wthr_attrs.json'),'w'),indent=1)
print(len(picw),len(pbrw))
