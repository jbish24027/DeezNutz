import json
exec(open('a2.py').read().split('pref=')[0])
d=load('wthr_dawnwarmth.jsonl')
mot=['%06X:Mists of Tamriel.esp'%i for i in range(0x80B,0x817)]
for k,(e,f) in d.items():
    if e in ('SkyrimClear','SkyrimClear_A','SkyrimCloudy','SkyrimFog','SkyrimOvercastRain','SkyrimOvercastSnow','SkyrimStormRain','SkyrimStormSnow','SkyrimCloudy_A'):
        items=[v for p,v in f.items() if p.startswith('SkyStatics[')]
        n=sum(1 for m in mot if m in items)
        others=[v for v in items if 'Skyrim.esm' not in v and 'Mists of Tamriel' not in v]
        print(e, 'items',len(items),'MoT',n,'nonvanilla',others[:20], 'flags',f.get('Flags'))
