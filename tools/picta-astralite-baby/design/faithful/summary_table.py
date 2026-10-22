import sys
sys.argv=['x']
exec(open('faithful_model.py',encoding='utf-8').read().split("# ---------------- evaluation ----------------")[0])
out=[]
def hs(c):
    h,s=hsv(c); return f"{h:3.0f}/{s:.2f}"
for fid,lab in (('19FA01','CLEAR A01 (partner SkyrimClear)'),('19FC01','CLOUDY C01 (SkyrimCloudy)'),('19FD02','FOG D02 (SkyrimFog)'),('19FD03','RAIN D03 (SkyrimOvercastRain)')):
    out.append(f"\n{lab}   cells = hue/HSVsat  Picta-now -> BABY [Astralite own lane] lumaB/P")
    for ch in ('top','hor','clouds','fogfar','sunlight','DALC.DirectionalXPlus'):
        row=[]
        for t,nm in ((7.5,'dawn 07:30'),(13.0,'day 13:00'),(18.5,'dusk 18:30'),(22.0,'night 22:00')):
            p=P_out(ch,fid,t); b=B_out(ch,fid,t); a=A_out(ch,fid,t)
            row.append(f"{nm}: {hs(p)} -> {hs(b)} [{hs(a)}] x{L(b)/L(p):.3f}")
        out.append(f"  {ch.replace('DALC.Directional','ambient '):12s} " + ' | '.join(row))
    for t,nm in ((7.5,'dawn'),(18.5,'dusk')):
        pc=dome(PIC[fid],E_P[FILE_OF[fid]],t,VIEWS['hor_sun']); bc=dome(B_REC[fid],B_E[FILE_OF[fid]],t,VIEWS['hor_sun']); nc=dome(NAIVE[fid],E_P[FILE_OF[fid]],t,VIEWS['hor_sun'])
        out.append(f"  dome horizon toward sun {nm}: Picta {hs(pc)} -> BABY {hs(bc)} x{L(bc)/L(pc):.3f}; naive {hs(nc)} x{L(nc)/L(pc):.2f}")
open('summary_table.txt','w').write('\n'.join(out)); print('\n'.join(out))
