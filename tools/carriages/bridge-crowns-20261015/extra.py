import sys, math, pickle
import numpy as np
exec(open('bridges5.py').read().split("for name,chain in CH.items():")[0])
def deck(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if h[1]=='up' and z-120<h[0]<=z+220 and 'roof' not in h[2] and 'gallows' not in h[2] and h[2]!='sbridge01.nif']
    return max(hs)[0] if hs else None
def seg(refs,a,b,step=25):
    (n1,x1,y1,z1),(n2,x2,y2,z2)=a,b; L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//step)); out=[]
    for i in range(steps+1):
        t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t; d=deck(refs,x,y,z)
        out.append((t,x,y,z,d))
    return out
def residual(refs,ch):
    sink=(0,None); fl=(0,None)
    for a,b in zip(ch,ch[1:]):
        for t,x,y,z,d in seg(refs,a,b):
            if d is None: continue
            if d-z>sink[0]: sink=(d-z,(a[0],b[0],round(t,2)))
            if z-d>fl[0]: fl=(z-d,(a[0],b[0],round(t,2)))
    return sink,fl
def balance(refs,ch,adj,rng=(-6,16,2)):
    idx={p[0]:i for i,p in enumerate(ch)}
    for rnd in range(2):
        for n in adj:
            i=idx[n]; best=None
            for off in np.arange(*rng):
                z0=ch[i][3]; ch[i][3]=z0+off
                sub=ch[max(0,i-1):i+2]; s,f=residual(refs,sub); score=max(s[0],f[0]); ch[i][3]=z0
                if best is None or score<best[0]: best=(score,off)
            ch[i][3]+=best[1]
    return ch
PLAN={'Markarth':dict(adj=['ED2','ED3','ED4','ED5'],insert=[('ED2','ED3'),('ED4','ED5')]),
      'Rorikstead':dict(adj=['9D1'],insert=[('9D1','9D2')]),
      'Windhelm':dict(adj=['966','967','968'],insert=[])}
out={}
for name,plan in PLAN.items():
    chain=[list(p) for p in CH[name]]; cx=sum(p[1] for p in chain)/len(chain); cy=sum(p[2] for p in chain)/len(chain); refs=refs_near(cx,cy)
    # step 1: adjustable markers onto deck+2
    for p in chain:
        if p[0] in plan['adj']:
            d=deck(refs,p[1],p[2],p[3]); p[3]=d+2
    # step 2: insert a marker at the worst-sag sample of each named segment (xy on the chord), z = deck+2
    new=[]
    for a_name,b_name in plan['insert']:
        i=[p[0] for p in chain].index(a_name); a,b=tuple(chain[i]),tuple(chain[i+1])
        samples=[s for s in seg(refs,a,b) if s[4] is not None and 0.15<s[0]<0.85]
        t,x,y,z,d=max(samples,key=lambda s:s[4]-s[3])
        nm='%s+'%a_name; chain.insert(i+1,[nm,x,y,d+2]); new.append(nm)
        print('%s: new marker %s at t=%.2f (%.0f, %.0f) z %.1f  (chord was %.0f, deck %.0f)'%(name,nm,t,x,y,d+2,z,d))
    chain=balance(refs,chain,plan['adj']+new)
    s,f=residual(refs,chain)
    print('%s RESIDUAL: sink %.0f at %s, float %.0f at %s'%(name,s[0],s[1],f[0],f[1]))
    for p in chain:
        old=[q for q in CH[name] if q[0]==p[0]]
        if p[0] in plan['adj'] or p[0] in new:
            print('   %-5s (%.1f, %.1f) z %.1f%s'%(p[0],p[1],p[2],p[3],'' if not old else '  (was %.1f, dz %+.0f)'%(old[0][3],p[3]-old[0][3])))
    out[name]=chain
pickle.dump(out,open('plan_chains.pkl','wb'))
