import sys, os, pickle, struct, json, warnings, math
warnings.filterwarnings('ignore')
OLD=r'C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/7b213a74-5dbb-466e-845a-b77c408e90d7/scratchpad'
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/carriages'); sys.path.insert(0, OLD+'/tools')
import deck; os.chdir(OLD)
from deck import hits_at
na, nf = pickle.load(open('near_refs.pkl','rb')); info_all, br = pickle.load(open('bases.pkl','rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
res = pickle.load(open('elevated_res.pkl','rb'))
fin = {o['formid'].upper():o for o in json.load(open(r'C:/1. AUTHORIA/_tools/carriages/fit_ops_final.json'))}
flag=0
for r in res:
    key='%06X:'%r['g'][1]
    f=[o for k,o in fin.items() if k.startswith(key) and r['g'][0].split('.')[0].lower() in k.lower()]
    z=float(f[0]['value'].split(',')[2]) if f else r['z']
    refs={k:v for k,v in nf.items() if v[1]==r['world'] and v[3] in info and math.dist(v[2][:2],(r['nx'],r['ny']))<3000}
    out=[]
    for k,v in refs.items():
        for h in hits_at({k:v},info,r['nx'],r['ny'],'A',sc): out.append((round(h),os.path.basename(info[v[3]])[:30]))
    above=[h for h in out if z+8<h[0]<=z+170 and 'roof' not in h[1]]
    if above:
        flag+=1
        print('%s %-8s %-28s x %6.0f y %6.0f final z %6.0f  surfaces ABOVE the cart: %s   (all: %s)'%(key,r['src'],r['kind'],r['nx'],r['ny'],z,above,sorted(h for h in out if -700<h[0]<z+500)))
print('flagged',flag,'of',len(res))
