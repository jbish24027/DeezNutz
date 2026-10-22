import sys,os,math,pickle,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from refpos import iter_world_refs
from land import height
from plug import Plugin
M='C:/1. AUTHORIA/mods/'
OWN=('simplecarriageexpansion.esp','animated carriages take you everywhere.esp')
refs={}
for f in [M+'Carriage Stops of Skyrim/simpleCarriageExpansion.esp',M+'Animated Carriages Take You Everywhere/Animated Carriages Take You Everywhere.esp']:
    for r in iter_world_refs(f):
        if r['gid'][0] in OWN: refs[r['gid']]=r
C=Plugin(M+'Carriage Stops of Skyrim/simpleCarriageExpansion.esp')
nm=lambda b: C.recs[b][1] if b in C.recs else '?'
van,fin=pickle.load(open('land_stops.pkl','rb'))
def R(h): return refs[('simplecarriageexpansion.esp',h)]
moves={}   # local id -> (x,y,z)
def group(brz):
    b=R(brz); return [g[1] for g,r in refs.items() if r['world']==b['world'] and math.dist(r['pos'][:2],b['pos'][:2])<25 and nm(r['base']) not in('sm_sce_activator','sm_sce_marker','MapMarker')]
def shift(ids,dx,dy,dz):
    for i in ids:
        x,y,z=R(i)['pos'][:3]; moves[i]=(x+dx,y+dy,z+dz)
# height-only fixes (ground under them moved by our landscape mods)
for brz,dz in ((0xb9,None),(0xd6,None)):
    b=R(brz); x,y=b['pos'][:2]; d=height(fin,b['world'],x,y)-height(van,b['world'],x,y); shift(group(brz),0,0,d)
for bench in (0xba,0xd2):
    b=R(bench); x,y=b['pos'][:2]; d=height(fin,b['world'],x,y)-height(van,b['world'],x,y); shift([bench],0,0,d)
# slides along the bench's long axis
moves[0x8f]=(17138.0,-46971.0,-106.0)      # Riverwood: clear Ivy's brazier
moves[0xb1]=(172395.0,-88747.0,10501.0)    # Riften: clear JK wall end
# Ivarstead: whole stop moved 225 units
b=R(0x99); dx,dy=79674-b['pos'][0],-69263-b['pos'][1]; moves[0x99]=(79674.0,-69263.0,10867.0)
zb=R(0x9a); gd=10906-zb['pos'][2]
shift(group(0x9a),dx,dy,gd)
ops=[]
for i,(x,y,z) in sorted(moves.items()):
    r=R(i); print(hex(i),nm(r['base']),[round(v) for v in r['pos'][:3]],'->',[round(x),round(y),round(z)])
    ops.append({'formid':'%06X:simpleCarriageExpansion.esp'%i,'field_path':'Placement.Position','value':'%.4f, %.4f, %.4f'%(x,y,z)})
json.dump(ops,open('stop_ops.json','w'),indent=0); print(len(ops),'ops')
