import sys,struct,os
sys.path.insert(0,os.path.dirname(__file__))
from plug import Plugin,subs
from collections import Counter
A=Plugin(sys.argv[1]); B=Plugin(sys.argv[2])
ra={k:v for k,v in A.recs.items()}; rb=B.recs
own_a={k for k in ra if k[0]==A.name.lower()}; own_b={k for k in rb if k[0]==B.name.lower()}
print('A own',len(own_a),'B own',len(own_b))
la={k[1] for k in own_a}; lb={k[1] for k in own_b}
print('local ids shared',len(la&lb),'onlyA',len(la-lb),'onlyB',len(lb-la))
ova={k for k in ra if k not in own_a}; ovb={k for k in rb if k not in own_b}
print('A overrides',Counter(k[0] for k in ova)); print('B overrides',Counter(k[0] for k in ovb))
# compare refs by local id: DATA and NAME
same=diffpos=diffother=0; dz=[]
for lid in sorted(la&lb):
    va=ra[(A.name.lower(),lid)]; vb=rb[(B.name.lower(),lid)]
    if va[0]!=vb[0]: diffother+=1; continue
    if va[0]!='REFR' and va[0]!='ACHR': 
        if va[3]!=vb[3]: diffother+=1
        continue
    sa=dict(subs(va[3])); sb=dict(subs(vb[3]))
    pa=struct.unpack('<6f',sa['DATA']); pb=struct.unpack('<6f',sb['DATA'])
    if pa==pb: same+=1
    else:
        diffpos+=1; dz.append((pb[2]-pa[2], ((pb[0]-pa[0])**2+(pb[1]-pa[1])**2)**.5))
print('refs same pos',same,'moved',diffpos,'other diffs',diffother)
if dz:
    import statistics as st
    print('dz median',st.median(d[0] for d in dz),'max',max(d[0] for d in dz),'min',min(d[0] for d in dz),'xy moved median',st.median(d[1] for d in dz),'max',max(d[1] for d in dz))
