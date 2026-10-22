import numpy as np
from PIL import Image
a=np.asarray(Image.open(r'C:/1. AUTHORIA/overwrite/Root/ScreenShot320.png').convert('RGB')).astype(np.float32)
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
k=np.ones(15)/15
cols=range(1750,3450,10); rows=[]
for x in cols:
    c=np.convolve(lum[1350:2100,x],k,'same')
    # going down from the cut, find first row where lum exceeds T (dry beach)
    r=None
    for T in [25]:
        idx=np.where(c[60:]>T)[0]
        # need sustained
        for i in idx:
            if c[60+i:60+i+40].mean()>T: r=1350+60+i; break
        break
    rows.append(r if r else -1)
rows=np.array(rows,float); cols=np.array(list(cols),float)
m=rows>0
np.save('obsedge.npy', np.vstack([cols[m],rows[m]]))
p=np.polyfit(cols[m],rows[m],1); res=rows[m]-np.polyval(p,cols[m])
print('observed water->beach edge: n=%d  slope=%.5f row@1920=%.0f  rms=%.1f'%(m.sum(),p[0],np.polyval(p,1920),res.std()))
print('samples:', [(int(cols[m][i]),int(rows[m][i])) for i in range(0,m.sum(),15)])
