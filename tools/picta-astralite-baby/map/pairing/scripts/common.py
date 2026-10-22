import json, os, re, collections
D = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/pairing"
def rows(fn):
    p=os.path.join(D,fn)
    if not os.path.exists(p): return []
    L=open(p,encoding='utf-8').read().splitlines()
    return [json.loads(x) for x in L[1:] if x.strip()]
def parse_wthr(r):
    a={'formid':r['formid'],'editorid':r.get('editorid'),'source':r.get('source'),'winner':r.get('winner')}
    ct=[]
    for f in r.get('fields',[]):
        p=f['path']; v=f.get('value'); link=f.get('link') or {}
        m=re.match(r'CloudTextures\[(\d+)\]$',p)
        if m:
            if v: ct.append((int(m.group(1)),v))
            continue
        if p in ('Precipitation','VisualEffect'):
            a[p]=link.get('editorid') if v else None
        elif '.' in p:
            top,sub=p.split('.',1)
            if top in ('ImageSpaces','VolumetricLighting'):
                a.setdefault(top,{})[sub]=link.get('editorid') if v else None
            else:
                a.setdefault(top,{})[sub]=v
        elif p=='CloudTextures': pass
        elif p in ('SkyUpperColor','HorizonColor','FogNearColor','FogFarColor','SunlightColor','AmbientColor','SunColor','ImageSpaces','VolumetricLighting'):
            pass
        else:
            a[p]=v
    a['cloud_layers']=len(ct); a['cloud_textures']=sorted(set(t for i,t in ct))
    for k in ('WindSpeed','SunGlare','SunDamage','TransDelta','FogDistanceDayNear','FogDistanceDayFar','FogDistanceNightNear','FogDistanceNightFar','FogDistanceDayPower','FogDistanceNightPower','FogDistanceDayMax','FogDistanceNightMax','WindDirection'):
        if k in a and a[k] is not None:
            try: a[k]=float(a[k])
            except: pass
    if isinstance(a.get('WindSpeed'),float) and a['WindSpeed']<=1.0: a['wind_0_255']=round(a['WindSpeed']*255)
    return a
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
            if 'value' in f: d['g']=f['value']; d['g_ed']=(f.get('link') or {}).get('editorid')
            else: d['g']=None; d['g_ed']=None
    return [ws[i] for i in sorted(ws)]
def bucket(g_ed):
    if not g_ed: return (None,None,None)
    m=re.match(r'(SN_)?Season_(Common|Spring|Summer|Autumn|Winter)_(PleasantA|Pleasant|Overcast|Rain_Storm|Rain|Snow_Storm|Snow)$',g_ed)
    if not m: return ('other',None,g_ed)
    return ('SN' if m.group(1) else 'plain', m.group(2), m.group(3))
