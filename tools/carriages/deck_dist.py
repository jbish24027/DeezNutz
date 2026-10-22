import sys,os,pickle,struct,warnings; warnings.filterwarnings('ignore')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from deck import *
na,nf=pickle.load(open('near_refs.pkl','rb')); info_all,br=pickle.load(open('bases.pkl','rb'))
info={b:'meshes/'+i[2].replace(chr(92),'/').lower() for b,i in br.items() if i[2]}
hits,markers=pickle.load(open('bridge_hits.pkl','rb'))
sc=lambda v: struct.unpack('<f',v[5][:4])[0] if v[5] else 1.0
rows=[]
for fname,g,w,x,y,z,gr in markers:
    za=hits_at({k:v for k,v in na.items() if v[1]==w},info,x,y,'A',sc)
    zf=hits_at({k:v for k,v in nf.items() if v[1]==w},info,x,y,'A',sc)
    rows.append((fname,g,w,x,y,z,gr,za,zf))
pickle.dump(rows,open('deck_rows.pkl','wb'))
import collections
b=collections.Counter()
for fname,g,w,x,y,z,gr,za,zf in rows:
    if not za: b['no author deck']+=1; continue
    da=min(za,key=lambda h:abs(z-h)); off=z-da
    b['off<-40' if off<-40 else 'off-40..0' if off<0 else 'off0..40' if off<40 else 'off40..150' if off<150 else 'off>150']+=1
print(b)
for fname,g,w,x,y,z,gr,za,zf in rows[:0]: pass
nod=[(fname,hex(g[1]),round(z),round(gr),round(z-gr)) for fname,g,w,x,y,z,gr,za,zf in rows if not za]
print('no author deck sample:',nod[:25])
