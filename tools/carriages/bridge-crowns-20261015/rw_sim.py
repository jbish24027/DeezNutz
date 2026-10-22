import sys, os, pickle, struct, warnings, math
warnings.filterwarnings('ignore')
OLD=r'C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/7b213a74-5dbb-466e-845a-b77c408e90d7/scratchpad'
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/carriages'); sys.path.insert(0, OLD+'/tools')
import deck; os.chdir(OLD)
from deck import hits_at
na, nf = pickle.load(open('near_refs.pkl','rb')); info_all, br = pickle.load(open('bases.pkl','rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
refs={k:v for k,v in nf.items() if v[1]==('skyrim.esm',60) and v[3] in info and math.dist(v[2][:2],(24300,-39440))<2500}
def top(x,y,z):
    hs=[h for h in hits_at(refs,info,x,y,'A',sc) if -600<h<z+220]
    return max(hs) if hs else None
def run(chain,label):
    worst=0; where=None
    for (n1,x1,y1,z1),(n2,x2,y2,z2) in zip(chain,chain[1:]):
        L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//25))
        for i in range(steps+1):
            t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t
            tp=top(x,y,z)
            if tp is not None and tp-z>worst: worst=tp-z; where=(n1,n2,round(t,2),round(z),round(tp))
    print(label,'worst sink',round(worst),'at',where)
C=(24589.473,-39996.625); D=(24300.309,-39440.72); E=(24021.299,-38890.727)
base=[('80C',*C,-13.9204),('80D',*D,73.0),('80E',*E,-36.4326)]
run(base,'A) 80D -> 73 only:')
# B) plus two new markers halfway, each on the deck top + 2
def mid(p,q): return ((p[0]+q[0])/2,(p[1]+q[1])/2)
m1=mid(C,D); m2=mid(D,E)
z1=top(m1[0],m1[1],200)+2; z2=top(m2[0],m2[1],200)+2
print('   midpoints: CD',[round(v) for v in m1],'deck',round(z1),' DE',[round(v) for v in m2],'deck',round(z2))
run([('80C',*C,-13.9204),('n1',*m1,z1),('80D',*D,73.0),('n2',*m2,z2),('80E',*E,-36.4326)],'B) 80D -> 73 + 2 new markers:')
# C) 80D raised a little higher to cover the chord sag
for zz in (80,90,100):
    run([('80C',*C,-13.9204),('80D',*D,float(zz)),('80E',*E,-36.4326)],'C) 80D -> %d only:'%zz)
