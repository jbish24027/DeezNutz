import sys, os, pickle, struct, json, warnings, math
import numpy as np
warnings.filterwarnings('ignore')
sys.argv=['x']; exec(open('bridges5.py').read().split("for name,chain in CH.items():")[0])   # reuse loaders + hits_facing + CH
def deck_any(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if z-80<h[0]<=z+170 and 'roof' not in h[2] and 'gallows' not in h[2]]
    return max(hs) if hs else None
def seg_eval(refs,a,b,step=25):
    (n1,x1,y1,z1),(n2,x2,y2,z2)=a,b; L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//step)); sink=0; fl=0
    for i in range(steps+1):
        t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t; tp=deck_any(refs,x,y,z)
        if tp: g=tp[0]-z; sink=max(sink,g); fl=max(fl,-g)
    return sink,fl
ADJ={'Riverwood':['80D'],'Markarth':['ED2','ED3','ED4','ED5'],'Rorikstead':['9D1'],'Windhelm':['966','967','968'],'Solitude':['B84']}
result={}
for name,chain in CH.items():
    cx=sum(p[1] for p in chain)/len(chain); cy=sum(p[2] for p in chain)/len(chain); refs=refs_near(cx,cy)
    ch=[list(p) for p in chain]; idx={p[0]:i for i,p in enumerate(ch)}
    print('=====',name)
    # deck profile at every marker
    for p in ch:
        d=deck_any(refs,p[1],p[2],p[3]); print('   %s z %8.1f deck %s'%(p[0],p[3],d))
    # start: adjustable markers onto deck+2
    for n in ADJ[name]:
        p=ch[idx[n]]; d=deck_any(refs,p[1],p[2],p[3])
        if d: p[3]=d[0]+2
    # greedy refine: each adjustable marker tries offsets to balance sink/float on its two segments
    for rnd in range(3):
        for n in ADJ[name]:
            i=idx[n]; best=None
            for off in np.arange(-10,61,2.5):
                z0=ch[i][3]; ch[i][3]=z0+off
                s=[seg_eval(refs,tuple(ch[j]),tuple(ch[j+1])) for j in (i-1,i) if 0<=j<len(ch)-1]
                sink=max(x[0] for x in s); fl=max(x[1] for x in s); score=max(sink,fl)
                ch[i][3]=z0
                if best is None or score<best[0]: best=(score,off,sink,fl)
            ch[i][3]+=best[1]
    tot_s=0; tot_f=0; where=None
    for j in range(len(ch)-1):
        s,f=seg_eval(refs,tuple(ch[j]),tuple(ch[j+1]))
        if s>tot_s: tot_s=s; where=(ch[j][0],ch[j+1][0])
        tot_f=max(tot_f,f)
    print('   RESULT worst sink %.0f (%s) worst float %.0f'%(tot_s,where,tot_f))
    for n in ADJ[name]:
        p=ch[idx[n]]; old=[q for q in chain if q[0]==n][0][3]
        print('   %s: z %.1f -> %.1f (dz %+.0f)'%(n,old,p[3],p[3]-old)); result[(name,n)]=(p[1],p[2],p[3])
    # bridge refs used (for the flag check)
    seen=set()
    for p in chain:
        for k,v in refs.items():
            if math.dist(v[2][:2],(p[1],p[2]))<900 and any(s in info[v[3]] for s in ('bridge','sbridge','hump')) and k not in seen:
                seen.add(k); print('   REF %06X:%s  %s  z %.0f  winner %s'%(k[1],k[0],os.path.basename(info[v[3]]),v[2][2],v[0]))
pickle.dump(result,open('newz.pkl','wb'))
