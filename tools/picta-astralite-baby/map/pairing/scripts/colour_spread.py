import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from pairing import ast_class, pbr_ed, A
# within each Astralite class, how far apart are the regional variants' record colours?
KEYS=['SkyUpperColor','HorizonColor','FogNearColor','FogFarColor','SunlightColor','AmbientColor','SunColor']
TOD=['Sunrise','Day','Sunset','Night']
def rgb(s):
    try:
        p=[int(x) for x in str(s).split(',')[:3]]; return p
    except: return None
groups=collections.defaultdict(list)
for fid,a in A['pbr'].items():
    c=ast_class(a.get('editorid'))
    if c in ('clear','clearA','cloudy','cloudyA','fog','rain','rainstorm','snow','snowstorm'):
        groups[c].append(a)
out={}
for c,lst in groups.items():
    res={}
    for k in KEYS:
        for t in TOD:
            vals=[rgb((a.get(k) or {}).get(t)) for a in lst]
            vals=[v for v in vals if v]
            if len(vals)<2: continue
            mean=[sum(v[i] for v in vals)/len(vals) for i in range(3)]
            dev=max(max(abs(v[i]-mean[i]) for i in range(3)) for v in vals)
            res[f'{k}.{t}']=(round(dev,1),[round(x) for x in mean])
    out[c]={'n':len(lst),'members':sorted(a.get('editorid') for a in lst),'max_dev_from_mean':res}
json.dump(out,open(os.path.join(D,'astralite_class_colour_spread.json'),'w'),indent=1)
for c,v in out.items():
    devs=sorted(v['max_dev_from_mean'].items(), key=lambda kv:-kv[1][0])
    print(c, v['n'], 'largest deviations:', [(k,d[0]) for k,d in devs[:6]], ' median dev:', sorted(d[0] for d in v['max_dev_from_mean'].values())[len(devs)//2] if devs else None)
# Same for Picta: compare masters' own pairs that share an E11 ini (A01/A02, B01/B02)
P=A['pic']
def get(ed):
    for fid,a in P.items():
        if a.get('editorid')==ed: return a
for x,y in [('PIC_WTHR_MASTER_A01_Clear','PIC_WTHR_MASTER_A02_Clear_Aurora'),('PIC_WTHR_MASTER_B01_Lightly_Cloudy','PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora'),('PIC_WTHR_MASTER_A01_Clear','PIC_WTHR_SUMMER_A01_Clear')]:
    a=get(x); b=get(y); diffs=[]
    for k in KEYS:
        for t in TOD:
            va=rgb((a.get(k) or {}).get(t)); vb=rgb((b.get(k) or {}).get(t))
            if va and vb and va!=vb: diffs.append((f'{k}.{t}',va,vb))
    print(x,'vs',y,'differing colour slots:',len(diffs), diffs[:6])
