import sys, math, pickle
exec(open('bridges5.py').read().split("for name,chain in CH.items():")[0])
NEW={'Markarth':{'ED2':-7455,'ED3':-7175,'ED4':-7236.5,'ED5':-7406},'Rorikstead':{'9D1':-5777.5},'Windhelm':{'966':-12730,'967':-12603.5,'968':-12651.5},'Riverwood':{'80D':80}}
SEG={'Markarth':('ED1','ED0'),'Rorikstead':('9CF','9D3'),'Windhelm':('965','96A'),'Riverwood':('80B','80F')}
def deck(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if h[1]=='up' and z-120<h[0]<=z+220 and 'roof' not in h[2] and 'gallows' not in h[2] and h[2]!='sbridge01.nif']
    return max(hs)[0] if hs else None
for name in ['Markarth','Windhelm','Rorikstead','Riverwood']:
    chain=CH[name]; i0=[p[0] for p in chain].index(SEG[name][0]); i1=[p[0] for p in chain].index(SEG[name][1])
    cx=sum(p[1] for p in chain)/len(chain); cy=sum(p[2] for p in chain)/len(chain); refs=refs_near(cx,cy)
    print('=====',name,' s(units)  deck  old-chord  new-chord   [sink+ / float-]')
    s=0
    for a,b in zip(chain[i0:i1],chain[i0+1:i1+1]):
        (n1,x1,y1,z1),(n2,x2,y2,z2)=a,b; L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//50))
        za1=NEW[name].get(n1,z1); za2=NEW[name].get(n2,z2)
        for i in range(steps+1):
            if i==0 and a is not chain[i0]: continue
            t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; zo=z1+(z2-z1)*t; zn=za1+(za2-za1)*t
            d=deck(refs,x,y,max(zo,zn))
            tag=('<-'+n1) if i==0 else ''
            print('  %5.0f  %7s  %7.0f  %7.0f   %s   %s'%(s+t*L,'-' if d is None else '%.0f'%d,zo,zn,'' if d is None else '%+.0f'%(d-zn),tag))
        s+=L
    print('  <-'+chain[i1][0])
