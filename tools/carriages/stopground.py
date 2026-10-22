import sys,os,math,pickle
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from land import scan_land,height
from lo import resolve
from refpos import iter_world_refs
from plug import Plugin
M='C:/1. AUTHORIA/mods/'
refs={}
for f in [M+'Carriage Stops of Skyrim/simpleCarriageExpansion.esp',M+'Animated Carriages Take You Everywhere/Animated Carriages Take You Everywhere.esp']:
    for r in iter_world_refs(f):
        if r['gid'][0] in('simplecarriageexpansion.esp','animated carriages take you everywhere.esp'): refs[r['gid']]=r
tg={(r['world'],(math.floor(r['pos'][0]/4096),math.floor(r['pos'][1]/4096))) for r in refs.values()}
lo=resolve('DEEZ CS NUTZ - PICTA')
van={};fin={}
for p,path in lo:
    if not path: continue
    if p.lower() in('skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm'): scan_land(path,tg,van)
    scan_land(path,tg,fin)
C=Plugin(M+'Carriage Stops of Skyrim/simpleCarriageExpansion.esp')
def nm(b): return C.recs[b][1] if b in C.recs else str(b)
out=[]
for g,r in refs.items():
    n=nm(r['base'])
    if n not in('sm_sce_activator','sm_sce_WRBrazier01'): continue
    x,y,z=r['pos'][:3]; gv=height(van,r['world'],x,y); gf=height(fin,r['world'],x,y)
    if gv is None or gf is None: continue
    out.append((round(gf-gv),n,hex(g[1]),round(z-gv),round(z-gf),[round(x),round(y)]))
for o in sorted(out,key=lambda o:-abs(o[0])): 
    if abs(o[0])>8 or abs(o[4])>40: print(o)
pickle.dump((van,fin),open('land_stops.pkl','wb'))
print(len(out),'benches+braziers checked')
