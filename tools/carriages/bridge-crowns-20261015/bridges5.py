import sys, os, pickle, struct, json, warnings, math
import numpy as np
warnings.filterwarnings('ignore')
OLD=r'C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/7b213a74-5dbb-466e-845a-b77c408e90d7/scratchpad'
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/carriages'); sys.path.insert(0, OLD+'/tools')
import deck; os.chdir(OLD)
from deck import load_tris, CONV
na, nf = pickle.load(open('near_refs.pkl','rb')); info_all, br = pickle.load(open('bases.pkl','rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
W=('skyrim.esm',60)

def hits_facing(refs, px, py):
    out=[]
    for k,v in refs.items():
        tris=load_tris(info[v[3]])
        if tris is None: continue
        pos=np.array(v[2][:3]); rot=v[2][3:]; s=sc(v)
        R=CONV['A'](*rot)
        q=(R.T@(np.array([px,py,0.0])-pos))/s; d=R.T@np.array([0,0,1.0])
        v0=tris[:,0]; e1=tris[:,1]-v0; e2=tris[:,2]-v0
        pv=np.cross(d,e2); det=(e1*pv).sum(1); ok=np.abs(det)>1e-9
        inv=np.where(ok,1.0/np.where(ok,det,1),0); tv=q-v0; u=(tv*pv).sum(1)*inv
        qv=np.cross(tv,e1); w=(qv@d)*inv; t=(e2*qv).sum(1)*inv
        m=ok&(u>=0)&(w>=0)&(u+w<=1)
        for i in np.nonzero(m)[0]:
            pl=q+t[i]*d; wz=(R@(pl*s)+pos)[2]
            n=R@np.cross(e1[i],e2[i]); nz=n[2]/(np.linalg.norm(n) or 1)
            out.append((round(float(wz)),'up' if nz>0.3 else 'down' if nz<-0.3 else 'side',os.path.basename(info[v[3]])[:26]))
    return sorted(out)

CH={
 'Riverwood':[('80B',24928.318,-40582.434,-123.3426),('80C',24589.473,-39996.625,-13.9204),('80D',24300.309,-39440.72,-37.9624),('80E',24021.299,-38890.727,-36.4326),('80F',23718.111,-38371.75,-137.4331),('810',23500.49,-37697.305,-162.4758)],
 'Markarth':[('ED1',-145749.55,17107.896,-7430.086),('ED2',-145514.53,17737.746,-7480.994),('ED3',-145273.83,18480.705,-7366.533),('ED4',-145106.22,19105.668,-7352.703),('ED5',-144844.64,19780.629,-7469.8457),('ED0',-144607.08,20412.389,-7526.029),('ED6',-144134.44,20961.832,-7590.645)],
 'Rorikstead':[('9CE',-114919.2,-14752.84,-5954.746),('9CF',-114102.195,-14599.685,-5946.801),('9D0',-113330.516,-14259.642,-5884.969),('9D1',-112678.08,-14116.131,-5916.5703),('9D2',-111688.09,-13909.3125,-5872.4575),('9D3',-111173.92,-13749.217,-5933.612)],
 'Windhelm':[('963',115257.73,33698.195,-12340.372),('964',115713.95,33337.836,-12492.254),('965',115865.98,32711.316,-12678.2295),('966',115967.82,32142.943,-12744.72),('967',116162.27,31265.771,-12743.88),('968',116359.57,30588.088,-12744.72),('969',116587.086,29771.27,-12745.185),('96A',116956.58,29322.428,-12816.899),('96B',117566.69,29103.113,-12927.929)],
 'Solitude':[('B82',-64041.406,100344.31,-12762.643),('B81',-64599.35,100146.664,-12556.188),('B83',-65129.684,99903.98,-12432.739),('B84',-65641.76,99598.31,-12294.676),('B86',-66180.08,99292.41,-12414.178),('B85',-66693.914,98918.85,-12520.931),('B89',-67064.375,98629.76,-12673.54)],
}
VAN={'ED3':-7366.5,'ED4':-7372.9,'9D1':-5823.2,'9D0':-5882.9,'9D2':-5860.8,'966':-12690.4,'967':-12625.9,'968':-12655.7,'B84':-12378.1,'80D':14.7}  # 1.6.4 vanilla-road author z
def refs_near(cx,cy):
    return {k:v for k,v in nf.items() if v[1]==W and v[3] in info and math.dist(v[2][:2],(cx,cy))<3500}
def deck_top(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if h[1]=='up' and z-80<h[0]<=z+170 and 'roof' not in h[2]]
    return max(hs) if hs else None
def ceiling(refs,x,y,z):
    hs=[h for h in hits_facing(refs,x,y) if h[1]=='down' and z+20<h[0]<=z+320]
    return min(hs) if hs else None
def profile(refs,chain,step=25):
    worst=(0,None); float_=(0,None); ceil=None
    for (n1,x1,y1,z1),(n2,x2,y2,z2) in zip(chain,chain[1:]):
        L=math.dist((x1,y1),(x2,y2)); steps=max(1,int(L//step))
        for i in range(steps+1):
            t=i/steps; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; z=z1+(z2-z1)*t
            tp=deck_top(refs,x,y,z)
            if tp:
                g=tp[0]-z
                if g>worst[0]: worst=(g,(n1,n2,round(t,2),round(z),tp))
                if -g>float_[0]: float_=(-g,(n1,n2,round(t,2),round(z),tp))
            c=ceiling(refs,x,y,z)
            if c and (ceil is None or c[0]-z<ceil[0]): ceil=(c[0]-z,(n1,n2,round(t,2),round(z),c))
    return worst,float_,ceil
for name,chain in CH.items():
    cx=sum(p[1] for p in chain)/len(chain); cy=sum(p[2] for p in chain)/len(chain)
    refs=refs_near(cx,cy)
    print('=====',name,'refs',len(refs))
    for n,x,y,z in chain:
        hs=[h for h in hits_facing(refs,x,y) if z-700<h[0]<z+500]
        print('  %s z %7.0f  van %s  surfaces: %s'%(n,z,VAN.get(n,'-'),hs))
    w,f,c=profile(refs,chain)
    print('  AS-IS: worst sink %.0f at %s | worst float %.0f at %s | lowest ceiling %s'%(w[0],w[1],f[0],f[1],c))
pickle.dump(CH,open(r'C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/1ed65889-6026-405b-bce6-70a6f26a7dc4/scratchpad/chains.pkl','wb'))
