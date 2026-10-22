# usage: build_land.py profile out.pkl  [plugins limited set: 'vanilla' | 'nr' | 'full']
import sys,os,pickle,math,time
sys.path.insert(0,os.path.dirname(__file__))
from land import scan_land
from refpos import iter_world_refs
from lo import resolve
A='arch/'
src=[A+'ACAR/Animated Carriage Additional Route.esp',A+'ACAR/Animated Carriage Additional Route 0.esp',A+'ACNR/Animated Carriage Additional Route NR.esp',A+'ACNR/Animated Carriage Additional Route 0 NR.esp',A+'CSOS/simpleCarriageExpansion.esp',A+'ACTYE/Animated Carriages Take You Everywhere.esp',r'C:/1. AUTHORIA/mods/Animated Carriage/ACLine_Whiterun.esp',r'C:/1. AUTHORIA/mods/Authoria - xEdit Output/Authoria - Patch - Animated Carriage NR - No Additional Routes.esp']+[A+'ACARP/Animated Carriage Additional Route compatibility patches/'+f for f in os.listdir(A+'ACARP/Animated Carriage Additional Route compatibility patches') if f.endswith('.esp')]
targets=set()
for f in src:
    for r in iter_world_refs(f):
        x,y=r['pos'][:2]
        gx=math.floor(x/4096); gy=math.floor(y/4096)
        for dx in(-1,0,1):
            for dy in(-1,0,1): targets.add((r['world'],(gx+dx,gy+dy)))
print('target cells',len(targets))
prof,out,mode=sys.argv[1],sys.argv[2],sys.argv[3]
lo=resolve(prof)
if mode=='vanilla': lo=[x for x in lo if x[0].lower() in('skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm')]
elif mode=='nr': lo=[x for x in lo if x[0].lower() in('skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm','northern roads.esp')]
store={}; who={}; t=time.time()
for i,(p,path) in enumerate(lo):
    if not path: continue
    try: n=scan_land(path,targets,store)
    except Exception as e: print('ERR',p,e); continue
    if n: who[p]=n
print('scanned',len(lo),'in',round(time.time()-t),'s; cells with land',len(store))
print('plugins providing land:',len(who)); print(sorted(who.items(),key=lambda x:-x[1])[:60])
pickle.dump(store,open(out,'wb'))
