import sys,os,pickle,statistics as st
sys.path.insert(0,os.path.dirname(__file__))
from land import height
from refpos import iter_world_refs
V=pickle.load(open('land_vanilla.pkl','rb')); N=pickle.load(open('land_nr.pkl','rb')); P=pickle.load(open('land_picta.pkl','rb'))
A='arch/'
def q(xs):
    xs=sorted(xs); n=len(xs); return [round(xs[int(n*p)],1) for p in (0,.05,.25,.5,.75,.95)]+[round(xs[-1],1)]
for f,ref in [('ACAR/Animated Carriage Additional Route.esp',V),('ACAR/Animated Carriage Additional Route 0.esp',V),('ACNR/Animated Carriage Additional Route NR.esp',N),('ACNR/Animated Carriage Additional Route 0 NR.esp',N),('CSOS/simpleCarriageExpansion.esp',V)]:
    R=iter_world_refs(A+f); off=[];dg=[]
    for r in R:
        x,y,z=r['pos'][:3]; g=height(ref,r['world'],x,y); gp=height(P,r['world'],x,y)
        if g is None: continue
        off.append(z-g); dg.append(gp-g)
    print(f,len(R)); print('  z-ground(src)  quantiles',q(off)); print('  ourGround-srcGround',q(dg)); print('  |dg|>16:',sum(abs(d)>16 for d in dg),' |dg|>64:',sum(abs(d)>64 for d in dg))
