import sys, os, pickle, struct, json, warnings, math
warnings.filterwarnings('ignore')
OLD=r'C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/7b213a74-5dbb-466e-845a-b77c408e90d7/scratchpad'
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/carriages'); sys.path.insert(0, OLD+'/tools')
import deck; os.chdir(OLD)
from deck import hits_at
na, nf = pickle.load(open('near_refs.pkl','rb')); info_all, br = pickle.load(open('bases.pkl','rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
W=('skyrim.esm',60)
# final marker chain (winner positions), travel order 80A -> 811
chain=[('80A',25123.635,-41245.33,-148.4548),('80B',24928.318,-40582.434,-123.3426),('80C',24589.473,-39996.625,-13.9204),
       ('80D',24300.309,-39440.72,-37.9624),('80E',24021.299,-38890.727,-36.4326),('80F',23718.111,-38371.75,-137.4331),
       ('810',23500.49,-37697.305,-162.4758),('811',23793.043,-37023.008,-157.2823)]
refs={k:v for k,v in nf.items() if v[1]==W}
# per-ref hits so we know WHICH object each surface belongs to
def hits_by_ref(x,y):
    out=[]
    for k,v in refs.items():
        if v[3] not in info or math.dist(v[2][:2],(x,y))>3000: continue
        zs=hits_at({k:v},info,x,y,'A',sc)
        for z in zs: out.append((round(z),os.path.basename(info[v[3]])[:28]))
    return sorted(out)
print('--- surfaces at each marker (z, mesh)')
for n,x,y,z in chain:
    print(n,'marker z %.0f'%z,[h for h in hits_by_ref(x,y) if -600<h[0]<600])
print('--- deck profile along the chain, every 40 units: s, interp z, top deck surface below interp+220, gap (deck - cart)')
worst=[]
for (n1,x1,y1,z1),(n2,x2,y2,z2) in zip(chain,chain[1:]):
    L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//40))
    for i in range(steps+1):
        t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t
        hs=[h for h in hits_by_ref(x,y) if -600<h[0]<z+220]
        top=max(hs) if hs else None
        gap=(top[0]-z) if top else None
        print('%s-%s t=%.2f  cart z %6.0f  top %s  gap %s'%(n1,n2,t,z,top,None if gap is None else round(gap)))
        if gap is not None and gap>15: worst.append((n1,n2,t,round(z),top,round(gap)))
print('--- segments where the cart is more than 15 under the top surface:')
for w in worst: print(w)
