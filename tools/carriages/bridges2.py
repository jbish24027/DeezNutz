import sys,os,pickle
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lo import resolve
from plug import Plugin,subs
hits,markers=pickle.load(open('bridge_hits.pkl','rb'))
bases={b for lst in hits.values() for (k,pl,b,kind,dz) in lst if b[0]!='animatedcarriage.esm'}
paths={p.lower():path for p,path in resolve('DEEZ CS NUTZ - PICTA') if path}
info={}
for f in sorted({b[0] for b in bases}):
    if f not in paths: continue
    P=Plugin(paths[f])
    for b in bases:
        if b[0]==f and b in P.recs:
            v=P.recs[b]; d=dict(subs(v[3])); info[b]=(v[0],v[1],d.get('MODL',b'').rstrip(b'\0').decode('cp1252','replace'))
def isbridge(b):
    i=info.get(b); 
    return i and ('bridge' in (i[1]+i[2]).lower() or 'dock' in (i[1]+i[2]).lower() or 'plank' in i[2].lower() or 'walkway' in i[2].lower())
out={}
for key,lst in hits.items():
    br=[(k,pl,info[b][1],info[b][2],kind,dz) for (k,pl,b,kind,dz) in lst if isbridge(b)]
    if br: out[key]=br
print('elevated markers with a changed BRIDGE-like object under them:',len(out),'of',len(markers))
from collections import Counter
c=Counter((x[1],x[2]) for v in out.values() for x in v); print(c.most_common(30))
pickle.dump(out,open('bridge_review.pkl','wb'))
