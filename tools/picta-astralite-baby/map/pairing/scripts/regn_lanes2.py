import json, os, re, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
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
st=json.load(open(os.path.join(D,'regn_lanes_stage1.json')))
lane=json.load(open(os.path.join(D,'lanediff.json')))
pbr_idx={n.lower():i for i,n in enumerate(lane['pbr_order'])}
for i,n in enumerate(['skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm']): pbr_idx[n]=-100+i
reads={}
for fn,pl in [('regn_read_Dawnguard.jsonl','Dawnguard.esm'),('regn_read_Skyrim.jsonl','Skyrim.esm'),('regn_read_BrumaUWC.jsonl','Beyond Skyrim Bruma - Universal Weather Compatibility.esp'),('regn_read_Dragonborn.jsonl','Dragonborn.esm'),('regn_read_BSHeartland.jsonl','BSHeartland.esm')]:
    for r in rows(fn): reads[(r['formid'],pl)]=r
ws={}
for r in rows('regn_worldspace.jsonl'):
    for f in r['fields']:
        if f['path']=='Worldspace':
            ws[r['formid']]=((f.get('link') or {}).get('editorid'), f.get('value'))
for fid,rec in st.items():
    if rec.get('pbr_winner') and 'pbr_weathers' not in rec:
        k=(fid,rec['pbr_winner'])
        if k in reads: rec['pbr_weathers']=parse_weathers(reads[k])
    if rec.get('pbr_winner') is None and rec.get('pic_winner') and rec['pic_winner'].lower().startswith('cc'):
        rec['pbr_winner']=rec['pic_winner']; rec['pbr_weathers']=rec['pic_weathers']; rec['note']='CC implicit, same both lanes'
    rec['worldspace']=ws.get(fid,(None,None))[0]
missing=[f for f,r in st.items() if r.get('pbr_winner') and 'pbr_weathers' not in r]
print('missing pbr weathers', missing)
json.dump(st,open(os.path.join(D,'regn_lanes.json'),'w'),indent=1)
# summary of exterior regions with weather differing per lane
c=collections.Counter(r['worldspace'] for r in st.values())
print(c)
