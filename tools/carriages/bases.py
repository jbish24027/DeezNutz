import sys,os,pickle,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lo import resolve
from plug import Plugin,subs
na,nf=pickle.load(open('near_refs.pkl','rb'))
bases={v[3] for v in list(na.values())+list(nf.values())}
paths={p.lower():path for p,path in resolve('DEEZ CS NUTZ - PICTA') if path}
info={}
# the winning base record: scan plugins in load order, last one wins
order=[p.lower() for p,path in resolve('DEEZ CS NUTZ - PICTA') if path]
need_files={}
for p in order:
    pass
for f in sorted({b[0] for b in bases}):
    if f in paths:
        P=Plugin(paths[f])
        for b in bases:
            if b[0]==f and b in P.recs:
                v=P.recs[b]; d=dict(subs(v[3])); info[b]=(v[0],v[1],d.get('MODL',b'').rstrip(b'\0').decode('cp1252','replace'))
KEY=('bridge','plank','dock','walkway','platform','floor','pier','boardwalk','stair','ramp')
br={b:i for b,i in info.items() if i[0] in('STAT','MSTT','ACTI','FURN','MISC') and any(k in (i[1]+i[2]).lower() for k in KEY)}
print(len(bases),'bases;',len(br),'bridge-like');
pickle.dump((info,br),open('bases.pkl','wb'))
models=sorted({('meshes/'+i[2].replace(chr(92),'/')).lower() for i in br.values() if i[2]})
json.dump(models,open('bridge_models.json','w'),indent=0); print(len(models),'models')
