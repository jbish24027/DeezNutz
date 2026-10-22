import os, sys, json
ROOT="C:/1. AUTHORIA"; PROF=sys.argv[1]
mods=[l.rstrip("\r\n")[1:] for l in open(f"{ROOT}/profiles/{PROF}/modlist.txt",encoding="utf-8-sig") if l.startswith("+")]
mods.reverse()  # low -> high
win={}
prov={}
for m in mods:
    d=f"{ROOT}/mods/{m}"
    for sub in ("enbseries",):
        p=os.path.join(d,sub)
        if os.path.isdir(p):
            for dp,dn,fn in os.walk(p):
                for f in fn:
                    rel=os.path.relpath(os.path.join(dp,f),d).replace("\\","/").lower()
                    prov.setdefault(rel,[]).append(m); win[rel]=m
    for f in ("enbseries.ini","enblocal.ini"):
        if os.path.isfile(os.path.join(d,f)):
            rel=f.lower(); prov.setdefault(rel,[]).append(m); win[rel]=m
json.dump({"winner":win,"providers":prov},open(f"enb_vfs_{PROF.replace(' ','_')}.json","w"),indent=1)
from collections import Counter
print(Counter(win.values()))
for rel in sorted(win):
    if rel.endswith(".ini") and ("/" not in rel.replace("enbseries/","",1) or rel.count("/")<=1):
        print(rel, "<-", win[rel], "| providers:", prov[rel])
