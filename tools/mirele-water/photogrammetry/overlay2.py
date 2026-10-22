import numpy as np, json, terrain
from PIL import Image, ImageDraw
Z=np.load('Z.npy'); g=json.load(open('grid.json'))
sample=terrain.make_sampler(Z,g['xs'],g['ys'])
PX,PY,PZ=1139.57,-59578.77,881.22
def go(az,F,back,h,HOR,w=800,ht=450,out='ov.png',cellgrid=True):
    a=np.radians(az); vx,vy=np.sin(a),np.cos(a); rx,ry=np.cos(a),-np.sin(a)
    C=np.array([PX-vx*back+rx*50, PY-vy*back+ry*50, 600.0+h])
    p=np.arctan((1080.0-HOR)/F)
    Fv=np.array([np.sin(a)*np.cos(p),np.cos(a)*np.cos(p),-np.sin(p)])
    Rv=np.array([np.cos(a),-np.sin(a),0.0]); Uv=np.cross(Rv,Fv)
    sc=w/3840.
    Xg,Yg=np.meshgrid((np.arange(w)+.5)/sc,(np.arange(ht)+.5)/sc)
    d=F*Fv+(Xg-1920)[...,None]*Rv+(1080-Yg)[...,None]*Uv
    d/=np.linalg.norm(d,axis=2,keepdims=True)
    with np.errstate(divide='ignore',invalid='ignore'):
        tw=(600.-C[2])/d[...,2]
    tw=np.where((d[...,2]<0)&(tw>0),tw,np.inf)
    ts=np.geomspace(20.,80000.,1200); hit=np.full((ht,w),np.inf); ab=np.ones((ht,w),bool)
    for t in ts:
        b=(C[2]+d[...,2]*t)<=sample(C[0]+d[...,0]*t,C[1]+d[...,1]*t)
        nw=b&ab&np.isinf(hit); hit[nw]=t; ab&=~b
    water=tw<hit
    real=np.asarray(Image.open('s320_b.png').convert('RGB').resize((w,ht),Image.LANCZOS)).astype(float)
    real[water]=real[water]*0.45+np.array([0,255,120])*0.55
    im=Image.fromarray(real.astype(np.uint8)); dr=ImageDraw.Draw(im)
    if cellgrid:
        # project world x = 0,-4096,-8192 lines onto the water plane
        for wxv,c in [(0.0,(255,0,0)),(-4096.0,(255,255,0)),(-8192.0,(0,180,255))]:
            pts=[]
            for wy in np.arange(C[1]-3000, C[1]+9000, 200.0):
                P=np.array([wxv,wy,600.0])-C
                den=P@Fv
                if den<=1: continue
                u=(P@Rv)/den*F+1920; v=1080-(P@Uv)/den*F
                if -6000<u<10000: pts.append((u*sc,v*sc))
            if len(pts)>1: dr.line(pts,fill=c,width=2)
    for pl,c in [((-0.021355,1430.576),(255,60,60)),((-0.004731,906.095),(255,160,0))]:
        dr.line([(0,pl[1]*sc),(w,(pl[0]*3840+pl[1])*sc)],fill=c,width=1)
    dr.line([(0,HOR*sc),(w,HOR*sc)],fill=(255,0,255),width=1)
    dr.text((5,5),'az%.1f F%.0f back%d h%d HOR%.0f'%(az,F,back,h,HOR),fill=(255,255,0))
    im.save(out); return out
