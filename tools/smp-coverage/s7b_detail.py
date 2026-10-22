import json, collections, re, os
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
npcs = json.load(open(sp + r"\npc_hair.json"))
hcls = json.load(open(sp + r"\hair_class.json"))
def bucket(n):
    if n["fg_phys"]: return "A"
    if n["hair_phys"]: return "B" if n["fg"] else "B2"
    if n["equiv"]: return "C"
    return "D"
named = [n for n in npcs if n["name"]]
print("== B named by face winner")
for k, v in collections.Counter(n["fg_win"] for n in named if bucket(n) == "B").most_common(40):
    print(" ", v, k)
print("== B named by defining plugin")
for k, v in collections.Counter(n["plugin"] for n in named if bucket(n) == "B").most_common(30):
    print(" ", v, k)
print("== D named, prov None: model paths")
for k, v in collections.Counter(n["model"].lower() for n in named if bucket(n) == "D" and n["prov"] is None).most_common(25):
    print(" ", v, repr(k))
print("== D named vanilla stems by provider")
for k, v in collections.Counter((n["prov"], os.path.basename(n["model"]).lower()) for n in named if bucket(n) == "D" and n["fam"] == "vanilla").most_common(40):
    print(" ", v, k)
print("== D named 'other' by hair-defining plugin + provider")
for k, v in collections.Counter((n["hair_def"], n["prov"]) for n in named if bucket(n) == "D" and n["fam"] in ("other", "KS Hairdos", "HG Hairdos", "Apachii")).most_common(40):
    print(" ", v, k)
print("== D named 'other' stems + a sample path")
seen = {}
for n in named:
    if bucket(n) == "D" and n["fam"] in ("other", "KS Hairdos", "HG Hairdos"):
        s = os.path.basename(n["model"]).lower()
        seen.setdefault(s, [0, n["model"], n["hair_def"]])[0] += 1
for s, (c, p, d) in sorted(seen.items(), key=lambda kv: -kv[1][0])[:60]:
    print(" ", c, s, "|", p, "|", d)
print("== C named: hair -> equivalent")
for k, v in collections.Counter((os.path.basename(n["model"]).lower(), n["equiv"][0] if n["equiv"] else None) for n in named if bucket(n) == "C").most_common(40):
    print(" ", v, k)
print("== B2 named by plugin")
for k, v in collections.Counter(n["plugin"] for n in named if bucket(n) == "B2").most_common(15):
    print(" ", v, k)
print("== A named by face winner")
for k, v in collections.Counter(n["fg_win"] for n in named if bucket(n) == "A").most_common(15):
    print(" ", v, k)
