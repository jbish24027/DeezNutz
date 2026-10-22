import numpy as np, json, terrain
from PIL import Image
Z=np.load('Z.npy'); g=json.load(open('grid.json'))
sample=terrain.make_sampler(Z,g['xs'],g['ys'])
PX,PY,PZ=1139.57,-59578.77,881.22
print('terrain z at player xy: %.1f  (player feet z %.1f)'%(sample(np.array([PX]),np.array([PY]))[0],PZ))
for az in [270,274.093,278,282]:
    a=np.radians(az); vx,vy=np.sin(a),np.cos(a); rx,ry=np.cos(a),-np.sin(a)
    for back in [140,180,220]:
        cx=PX-vx*back+rx*50; cy=PY-vy*back+ry*50
        t=np.arange(0,4000,4.0)
        z=sample(cx+vx*t, cy+vy*t)
        # first crossing below 600 going out
        idx=np.where(z<600)[0]
        d=t[idx[0]] if len(idx) else -1
        # also where it comes back above 600
        if len(idx):
            after=np.where(z[idx[0]:]>=600)[0]
            d2=t[idx[0]+after[0]] if len(after) else -1
        else: d2=-1
        print('az=%.3f back=%3d  cam=(%.0f,%.0f)  first wet at D=%.0f  dry again at D=%.0f'%(az,back,cx,cy,d,d2))
