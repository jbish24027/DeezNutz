import json
P='C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/fog-mist/'
def load(fn):
    out={}
    for i,l in enumerate(open(P+fn,encoding='utf-8')):
        r=json.loads(l)
        if i==0 and 'housecarl_artifact' in r: continue
        f=r.get('fields')
        if isinstance(f,list):
            d={}
            for x in f:
                p=x['path']; v=x.get('value',x.get('note'))
                if p in d:
                    if not isinstance(d[p],list): d[p]=[d[p]]
                    d[p].append(v)
                else: d[p]=v
            f=d
        out[r['formid']]=(r.get('editorid'),f)
    return out
pref=('SkyrimClear','SkyrimCloudy','SkyrimFog','SkyrimOvercast','SkyrimStorm')
for fn in ['wthr_dawnwarmth.jsonl','wthr_astralite_enb.jsonl']:
    d=load(fn)
    print('==',fn,len(d))
    k0=next(iter(d)); print('keys sample',list(d[k0][1].keys())[:60])
    for k,(e,f) in d.items():
        if e and e.startswith(pref):
            ve=f.get('VisualEffect'); vb=f.get('VisualEffectBegin'); vend=f.get('VisualEffectEnd')
            vl=[f.get('VolumetricLighting.'+s) for s in ('Sunrise','Day','Sunset','Night')]
            sk=f.get('SkyStatics')
            skn=len(sk) if isinstance(sk,list) else sk
            print(e,k,ve,vb,vend,vl,'statics',skn)
