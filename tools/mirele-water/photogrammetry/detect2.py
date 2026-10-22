import numpy as np
from PIL import Image
a = np.asarray(Image.open(r'C:/1. AUTHORIA/overwrite/Root/ScreenShot320.png').convert('RGB')).astype(np.float32)
R,G,B=a[...,0],a[...,1],a[...,2]
lum=0.299*R+0.587*G+0.114*B
# far water is PALE (sky reflection). land below it is dark green/grey.
# scan for the sharp luminance DROP going downward, in x 1400..2500, y 820..1000
ys=[]; xs=[]
for x in range(1350,2650):
    col=lum[820:1000,x]
    # sharp step: max of (mean of 12 above) - (mean of 12 below)
    best=None; bestd=0
    for i in range(12,len(col)-12):
        d=col[i-12:i].mean()-col[i:i+12].mean()
        if d>bestd: bestd=d; best=i
    if bestd>18:
        ys.append(best+820); xs.append(x)
xs=np.array(xs,float); ys=np.array(ys,float)
print('n=',len(xs))
X,Y=xs,ys
for it in range(10):
    p=np.polyfit(X,Y,1); r=Y-np.polyval(p,X); s=r.std()
    k=np.abs(r)<2.0*s
    if k.all(): break
    X,Y=X[k],Y[k]
p=np.polyfit(X,Y,1); r=Y-np.polyval(p,X)
print('FAR CUT n=%d slope=%.6f  row@x=1920: %.2f  rms=%.2f max=%.2f'%(len(X),p[0],np.polyval(p,1920),r.std(),np.abs(r).max()))
print('angle %.3f deg'%np.degrees(np.arctan(p[0])))
np.save('farcut.npy',p)
