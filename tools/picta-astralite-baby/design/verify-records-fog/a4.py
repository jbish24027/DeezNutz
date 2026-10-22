import json
exec(open('a2.py').read().split('pref=')[0])
d=load('wthr_dawnwarmth.jsonl')
mot=set('%06X:Mists of Tamriel.esp'%i for i in range(0x80B,0x817))
RF={'000834:Astralite ENB.esp':'Lite','000812:Astralite ENB.esp':'Heavy','00081C:Astralite ENB.esp':'Rain','00081D:Astralite ENB.esp':'DistRain'}
both=[]
for k,(e,f) in sorted(d.items(), key=lambda x:str(x[1][0])):
    if not e or not e.startswith(('SkyrimClear','SkyrimCloudy','SkyrimFog')): continue
    items=[v for p,v in f.items() if p.startswith('SkyStatics[')]
    m=len(mot & set(items)); ve=f.get('VisualEffect'); r=RF.get(ve, 'none' if 'null' in str(ve) else ve)
    print(f'{e:26s} ring={r:28s} MoT={m}')
    if m and r!='none': both.append(e)
print('ring+MoT together:', both)
