import os, struct, json, sys
ROOT="C:/1. AUTHORIA"; PROF=sys.argv[1]
def rl(p): return [l.rstrip("\r\n") for l in open(p,encoding="utf-8-sig",errors="replace")]
mods=[l[1:] for l in rl(f"{ROOT}/profiles/{PROF}/modlist.txt") if l.startswith("+")]; mods.reverse()
st={}
for l in rl(f"{ROOT}/profiles/{PROF}/plugins.txt"):
    if l.startswith("#") or not l.strip(): continue
    st[l.lstrip("*").lower()]=l.startswith("*")
idx={}
data=f"{ROOT}/Stock Game/Data"
for fn in os.listdir(data):
    if fn.lower().endswith((".esp",".esm",".esl")): idx[fn.lower()]=os.path.join(data,fn)
for m in mods:
    d=f"{ROOT}/mods/{m}"
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if fn.lower().endswith((".esp",".esm",".esl")): idx[fn.lower()]=os.path.join(d,fn)
order=[]
for l in rl(f"{ROOT}/profiles/{PROF}/loadorder.txt"):
    if l.startswith("#") or not l.strip(): continue
    k=l.lower(); s=st.get(k)
    if (s is None and k in idx) or s: order.append(l)
full=0; light=0; res={}
# engine: masters (ESM flag or .esm/.esl) load first in their listed order, then the rest
def flags(p):
    with open(idx[p.lower()],"rb") as f: h=f.read(12)
    return struct.unpack("<I",h[8:12])[0]
info=[]
for p in order:
    fl=flags(p); ext=p.lower()[-4:]
    isl = bool(fl & 0x200) or ext==".esl"
    ism = bool(fl & 1) or ext in (".esm",".esl")
    info.append((p,isl,ism))
mastersfirst=[x for x in info if x[2]]+[x for x in info if not x[2]]
for p,isl,ism in mastersfirst:
    if isl: res[p]=("FE%03X"%light); light+=1
    else: res[p]=("%02X"%full); full+=1
want=sys.argv[2:]
for w in want: print(w, res.get(w))
print("full",full,"light",light)
json.dump(res,open(f"runtime_slots_{PROF.replace(' ','_')}.json","w"),indent=0)
