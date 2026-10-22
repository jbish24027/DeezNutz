import numpy as np
PX,PY=1139.57,-59578.77
NEARp=np.array([-0.021355,1430.576]); FARp=np.array([-0.004731,906.095])
def cam(az,back,h,side=50.):
    a=np.radians(az); return np.array([PX-np.sin(a)*back+np.cos(a)*side, PY-np.cos(a)*back-np.sin(a)*side, 600.0+h])
def basis(az,F,HOR):
    p=np.arctan((1080.0-HOR)/F); a=np.radians(az)
    Fv=np.array([np.sin(a)*np.cos(p),np.cos(a)*np.cos(p),-np.sin(p)])
    Rv=np.array([np.cos(a),-np.sin(a),0.]); return Fv,Rv,np.cross(Rv,Fv)
def resid(params,az,F,lines):
    back,h,HOR=params
    C=cam(az,back,h); Fv,Rv,Uv=basis(az,F,HOR); r=[]
    for (axis,val),pl in zip(lines,[NEARp,FARp]):
        for s in np.linspace(-1500,4000,12):
            P=np.array([val, PY+s, 600.0]) if axis=='x' else np.array([PX+s, val, 600.0])
            D=P-C; den=D@Fv
            if den<=1: continue
            u=(D@Rv)/den*F+1920.; v=1080.-(D@Uv)/den*F
            if not(-2000<u<6000): continue
            r.append(v-np.polyval(pl,u))
    return np.array(r) if r else np.array([1e6])
def grid(az,F,lines,bs=np.arange(-60,460,10.),hs=np.arange(280,600,4.),Hs=np.arange(700,810,1.)):
    best=None
    for b in bs:
        for h in hs:
            for H in Hs:
                r=resid([b,h,H],az,F,lines); e=np.sqrt((r**2).mean())
                if best is None or e<best[0]: best=(e,b,h,H,np.abs(r).max(),len(r))
    return best
