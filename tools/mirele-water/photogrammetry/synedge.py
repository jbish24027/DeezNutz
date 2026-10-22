import numpy as np, json, terrain
Z=np.load('Z.npy'); g=json.load(open('grid.json'))
sample=terrain.make_sampler(Z,g['xs'],g['ys'])
PX,PY,PZ=1139.57,-59578.77,881.22
HOR=756.86
def campos(az,back,height,side=50.0):
    a=np.radians(az); vx,vy=np.sin(a),np.cos(a); rx,ry=np.cos(a),-np.sin(a)
    return np.array([PX-vx*back+rx*side, PY-vy*back+ry*side, 600.0+height])
def rays(az,F,cols,rws):
    p=np.arctan((1080.0-HOR)/F); a=np.radians(az)
    Fv=np.array([np.sin(a)*np.cos(p),np.cos(a)*np.cos(p),-np.sin(p)])
    Rv=np.array([np.cos(a),-np.sin(a),0.0]); Uv=np.cross(Rv,Fv)
    U,V=np.meshgrid(cols-1920.0, 1080.0-rws)
    d=F*Fv + U[...,None]*Rv + V[...,None]*Uv
    return d
def plane_hit(C,d):
    t=(600.0-C[2])/d[...,2]
    bad=(d[...,2]>=0)|(t<=0)
    t=np.where(bad,np.nan,t)
    return C[0]+d[...,0]*t, C[1]+d[...,1]*t, t
def syn_edge(az,F,back,height,cols,T=100.0):
    C=campos(az,back,height)
    rws=np.arange(1300,2160,2.0)
    d=rays(az,F,cols,rws)
    wx,wy,t=plane_hit(C,d)
    dep=600.0-sample(np.nan_to_num(wx),np.nan_to_num(wy))
    out=[]
    for j in range(len(cols)):
        col=dep[:,j]
        idx=np.where(col<T)[0]
        out.append(rws[idx[0]] if len(idx) else np.nan)
    return np.array(out)
