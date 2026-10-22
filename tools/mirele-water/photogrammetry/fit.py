import numpy as np
ys=np.load('cutrows.npy'); xs=np.arange(3840)
good=ys>0
m = good & (xs>=1650)
X,Y = xs[m].astype(float), ys[m].astype(float)
for it in range(8):
    p=np.polyfit(X,Y,1); r=Y-np.polyval(p,X); s=r.std()
    keep=np.abs(r)<2.5*s
    if keep.all(): break
    X,Y=X[keep],Y[keep]
p=np.polyfit(X,Y,1); r=Y-np.polyval(p,X)
print(f'ROBUST n={len(X)} slope={p[0]:.6f} px/px  intercept(x=0)={p[1]:.2f}  rms={r.std():.2f}px max={np.abs(r).max():.2f}')
print('angle from horizontal = %.3f deg' % (np.degrees(np.arctan(p[0]))))
print('row at x=1920 (centre): %.2f' % np.polyval(p,1920))
print('row at x=1700: %.2f   x=3800: %.2f' % (np.polyval(p,1700), np.polyval(p,3800)))
# quadratic test: is it curved?
q=np.polyfit(X,Y,2); rq=Y-np.polyval(q,X)
print('quad coeff a=%.3e  rms=%.2f' % (q[0], rq.std()))
np.save('fitp.npy', p)
