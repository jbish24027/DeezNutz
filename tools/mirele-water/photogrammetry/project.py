import numpy as np, synedge
NEAR=(-0.021355,1430.576); FAR=(-0.004731,906.095)
def worldline(az,F,back,h,p,cols=np.arange(1700,3800,50.0)):
    C=synedge.campos(az,back,h)
    rws=np.polyval(p,cols)
    d=synedge.rays(az,F,cols,np.array([0.0]))*0  # placeholder
    # build rays one-per-column at its own row
    pp=np.arctan((1080.0-synedge.HOR)/F); a=np.radians(az)
    Fv=np.array([np.sin(a)*np.cos(pp),np.cos(a)*np.cos(pp),-np.sin(pp)])
    Rv=np.array([np.cos(a),-np.sin(a),0.0]); Uv=np.cross(Rv,Fv)
    U=cols-1920.0; V=1080.0-rws
    d=F*Fv + U[:,None]*Rv + V[:,None]*Uv
    t=(600.0-C[2])/d[:,2]
    wx=C[0]+d[:,0]*t; wy=C[1]+d[:,1]*t
    return wx,wy,C
def describe(az,F,back,h):
    out={}
    for nm,p in [('near',NEAR),('far',FAR)]:
        wx,wy,C=worldline(az,F,back,h,p)
        # fit x = a*y + b  (near-vertical line in map coords)
        A=np.polyfit(wy,wx,1)
        rr=wx-np.polyval(A,wy)
        bearing=np.degrees(np.arctan2(1.0,A[0]))  # direction of line: dy=1,dx=A[0]
        out[nm]=dict(x_at_player_y=np.polyval(A,-59578.77), dxdy=A[0],
                     bearing=bearing, rms=rr.std(),
                     xmin=wx.min(), xmax=wx.max(), ymin=wy.min(), ymax=wy.max(), camx=C[0], camy=C[1], camz=C[2])
    return out
