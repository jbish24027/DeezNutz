import numpy as np
from PIL import Image
a = np.asarray(Image.open(r'C:/1. AUTHORIA/overwrite/Root/ScreenShot320.png').convert('RGB')).astype(np.float32)
R,G,B = a[...,0],a[...,1],a[...,2]
lum = 0.299*R+0.587*G+0.114*B
bluedom = B - np.maximum(R,G)
# water mask: blue dominant OR very dark
water = ((bluedom > 4) | (lum < 14)) & (lum < 60)
ys = []
Y0,Y1 = 1150, 1750
W = 40
for x in range(3840):
    col = water[Y0:Y1, x]
    # cumulative: find first y where mean of next W rows >= 0.85 and mean of previous W rows <= 0.25
    best=None
    cs = np.concatenate([[0], np.cumsum(col.astype(np.float32))])
    for i in range(W, len(col)-W):
        after = (cs[i+W]-cs[i])/W
        before = (cs[i]-cs[i-W])/W
        if after>=0.85 and before<=0.25:
            best=i+Y0; break
    ys.append(best if best is not None else -1)
ys=np.array(ys)
np.save('cutrows.npy', ys)
good = ys>0
print('columns with detection:', good.sum())
xs=np.arange(3840)
# restrict to right-hand region where water band is present
for lo,hi in [(1500,3839),(1600,3839),(1700,3500),(2000,3839)]:
    m = good & (xs>=lo)&(xs<=hi)
    if m.sum()<10: continue
    p=np.polyfit(xs[m],ys[m],1)
    res=ys[m]-np.polyval(p,xs[m])
    print(f'x {lo}-{hi}: n={m.sum()} slope={p[0]:.6f} intercept={p[1]:.2f} rms={res.std():.3f} max|res|={np.abs(res).max():.2f}')
print('sample:', [(x,int(ys[x])) for x in range(1500,3840,200)])
