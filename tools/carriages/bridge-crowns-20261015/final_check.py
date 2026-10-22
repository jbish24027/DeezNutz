import sys, math, pickle
exec(open('bridges5.py').read().split("for name,chain in CH.items():")[0])
def deck(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if h[1]=='up' and z-120<h[0]<=z+220 and 'roof' not in h[2] and 'gallows' not in h[2] and h[2]!='sbridge01.nif']
    return max(hs)[0] if hs else None
FINAL={
 'Riverwood':[('80B',24928.318,-40582.434,-123.3426),('80C',24589.473,-39996.625,-13.9204),('80D',24300.309,-39440.72,80.0),('80E',24021.299,-38890.727,-36.4326),('80F',23718.111,-38371.75,-137.4331)],
 'Markarth':[('ED1',-145749.55,17107.896,-7430.086),('ED2',-145514.53,17737.746,-7437.0),('800',-145374.8,18169.1,-7262.0),('ED3',-145273.83,18480.705,-7206.0),('ED4',-145106.22,19105.668,-7217.0),('801',-145022.1,19322.6,-7260.0),('ED5',-144844.64,19780.629,-7446.0),('ED0',-144607.08,20412.389,-7526.029)],
 'Rorikstead':[('9CF',-114102.195,-14599.685,-5946.801),('9D0',-113330.516,-14259.642,-5884.969),('9D1',-112678.08,-14116.131,-5791.0),('802',-112331.6,-14043.7,-5793.0),('9D2',-111688.09,-13909.3125,-5872.4575),('9D3',-111173.92,-13749.217,-5933.612)],
 'Windhelm':[('965',115865.98,32711.316,-12678.2295),('966',115967.82,32142.943,-12742.0),('967',116162.27,31265.771,-12604.0),('968',116359.57,30588.088,-12652.0),('969',116587.086,29771.27,-12745.185),('96A',116956.58,29322.428,-12816.899)],
}
for name,chain in FINAL.items():
    cx=sum(p[1] for p in chain)/len(chain); cy=sum(p[2] for p in chain)/len(chain); refs=refs_near(cx,cy)
    sink=(0,None); fl=(0,None); onbridge=[]
    for a,b in zip(chain,chain[1:]):
        (n1,x1,y1,z1),(n2,x2,y2,z2)=a,b; L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//25))
        for i in range(steps+1):
            t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t; d=deck(refs,x,y,z)
            if d is None: continue
            g=d-z
            if g>sink[0]: sink=(g,(n1,n2,round(t,2)))
            if -g>fl[0] and not (a is chain[0] or b is chain[-1]): fl=(-g,(n1,n2,round(t,2)))
    print('%-10s AS WRITTEN: worst sink %3.0f at %s | worst float (excluding the two approach segments) %3.0f at %s'%(name,sink[0],sink[1],fl[0],fl[1]))
