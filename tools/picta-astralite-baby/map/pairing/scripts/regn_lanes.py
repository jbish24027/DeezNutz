import json, os, re, collections
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
def rows(fn):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return []
    L=open(p,encoding='utf-8').read().splitlines()
    return [json.loads(x) for x in L[1:] if x.strip()]
def parse_weathers(r):
    ws={}
    for f in r.get('fields',[]):
        m=re.match(r'Weather\.Weathers\[(\d+)\]\.(\w+)$',f['path'])
        if not m: continue
        i=int(m.group(1)); k=m.group(2)
        d=ws.setdefault(i,{})
        if k=='Weather':
            d['w']=f.get('value'); d['w_ed']=(f.get('link') or {}).get('editorid')
        elif k=='Chance': d['chance']=float(f.get('value'))
        elif k=='Global':
            if 'value' in f:
                d['g']=f['value']; d['g_ed']=(f.get('link') or {}).get('editorid')
            else: d['g']=None; d['g_ed']=None
    return [ws[i] for i in sorted(ws)]
lane=json.load(open(os.path.join(D,'lanediff.json')))
pbr_idx={n.lower():i for i,n in enumerate(lane['pbr_order'])}
pic_only=set(n.lower() for n in lane['only_pic'])
# implicit masters precede everything
implicit=['skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm']
for i,n in enumerate(implicit): pbr_idx[n]=-100+i
pic=rows('regn_picta_winners.jsonl')
tree={r['formid']:r for r in rows('regn_picta_tree.jsonl')}
src_files={'Astralite Weathers.esp':'regn_src_AstraliteWeathers.jsonl','Astralite ENB.esp':'regn_src_AstraliteENB.jsonl',
 'Seasonal Weathers Framework - Astralite Weathers.esp':'regn_src_SWFAstralite.jsonl','Wyrmstooth-Astralite-Weather-Patch.esp':'regn_src_WyrmAstralite.jsonl',
 'Authoria - Patch - Snowy Holds Seasonal Snowfall.esp':'regn_src_SnowyHolds.jsonl','Helios_Astralite.esp':'regn_src_HeliosAstralite.jsonl',
 'Helios_Astralite_Seasonal.esp':'regn_src_HeliosAstraliteSeasonal.jsonl'}
src={}
for pl,fn in src_files.items():
    for r in rows(fn): src.setdefault(r['formid'],{})[pl]=r
out={}
need_read=collections.defaultdict(list)
allf=set(r['formid'] for r in pic)|set(src)
picmap={r['formid']:r for r in pic}
for fid in sorted(allf):
    t=tree.get(fid)
    touch=t['touchers'] if t else None
    rec={'formid':fid}
    if fid in picmap:
        r=picmap[fid]; rec['editorid']=r.get('editorid'); rec['pic_winner']=r['winner']; rec['pic_weathers']=parse_weathers(r)
    else:
        rec['pic_winner']=None
    if touch is None:
        rec['note']='not in PICTA weather-REGN set; providers unknown'
        common=[]
    else:
        common=[p for p in touch if p.lower() not in pic_only]
    pbrp=common+[p for p in src.get(fid,{})]
    pbrp=[p for p in pbrp if p.lower() in pbr_idx]
    if not pbrp:
        rec['pbr_winner']=None
    else:
        w=max(pbrp,key=lambda p:pbr_idx[p.lower()])
        rec['pbr_winner']=w; rec['pbr_providers']=sorted(pbrp,key=lambda p:pbr_idx[p.lower()])
        if w in src.get(fid,{}):
            rec['pbr_weathers']=parse_weathers(src[fid][w]); 
            if not rec.get('editorid'): rec['editorid']=src[fid][w].get('editorid')
        elif fid in picmap and picmap[fid]['winner']==w:
            rec['pbr_weathers']=rec['pic_weathers']
        else:
            need_read[w].append(fid)
    out[fid]=rec
json.dump(out,open(os.path.join(D,'regn_lanes_stage1.json'),'w'),indent=1)
print('records',len(out))
print('need_read:',{k:len(v) for k,v in need_read.items()})
json.dump(need_read,open(os.path.join(D,'need_read.json'),'w'),indent=1)
c=collections.Counter((r['pic_winner'],r.get('pbr_winner')) for r in out.values())
for k,v in c.most_common(): print(v,k)
