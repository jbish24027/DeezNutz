import os, json, re, sys, collections
ROOT = r"C:\1. AUTHORIA"
prof = os.path.join(ROOT, "profiles", "DEEEZ NUTTZZZ", "modlist.txt")
mods = [l[1:].strip() for l in open(prof, encoding="utf-8-sig") if l.startswith("+")]
mods.reverse()  # low -> high priority
OAR = "meshes/actors/character/animations/openanimationreplacer"
DAR = "meshes/actors/character/animations/dynamicanimationreplacer"

def has_cond(conds, name, negated=None, depth=0):
    for c in conds or []:
        if c.get("disabled"): continue
        if c.get("condition") == name and (negated is None or bool(c.get("negated")) == negated):
            return True
        if c.get("condition") in ("AND",) and has_cond(c.get("Conditions"), name, negated, depth+1):
            return True
    return False

rows = []
for mi, m in enumerate(mods):
    base = os.path.join(ROOT, "mods", m)
    for sub in (OAR, DAR):
        p = os.path.join(base, *sub.split("/"))
        if not os.path.isdir(p):
            # case-insensitive look
            cur = base; ok = True
            for part in sub.split("/"):
                if not os.path.isdir(cur): ok=False; break
                hit = [x for x in os.listdir(cur) if x.lower()==part]
                if not hit: ok=False; break
                cur = os.path.join(cur, hit[0])
            if not ok: continue
            p = cur
        for dp, dn, fn in os.walk(p):
            cfg = None
            for n in ("user.json", "config.json"):
                if n in fn: cfg = os.path.join(dp, n); break
            darc = "_conditions.txt" in [f.lower() for f in fn]
            if not cfg and not darc: continue
            hkx = []
            for dp2, dn2, fn2 in os.walk(dp):
                if dp2 != dp and any(x.lower() in ("config.json","user.json","_conditions.txt") for x in fn2): continue
                for f in fn2:
                    if f.lower().endswith(".hkx"):
                        hkx.append(os.path.relpath(os.path.join(dp2, f), dp).replace("\\","/").lower())
            if cfg:
                try: j = json.load(open(cfg, encoding="utf-8-sig"))
                except Exception as e: continue
                if "priority" not in j: continue
                conds = j.get("conditions", [])
                fem = "F" if has_cond(conds,"IsFemale",False) else ("M" if has_cond(conds,"IsFemale",True) else "-")
                rows.append(dict(mod=m, mi=mi, dir=dp, pri=j["priority"], fem=fem, ovr=j.get("overrideAnimationsFolder"), hkx=hkx, disabled=j.get("disabled",False)))
            else:
                txt = open(os.path.join(dp,[f for f in fn if f.lower()=="_conditions.txt"][0]), encoding="utf-8", errors="ignore").read()
                lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith(";")]
                fem = "-"
                for l in lines:
                    if re.match(r"(?i)not\s+isfemale", l): fem="M"
                    elif re.match(r"(?i)isfemale", l) and not l.upper().endswith("OR"): fem="F"
                try: pri = int(os.path.basename(dp))
                except: pri = 0
                rows.append(dict(mod=m, mi=mi, dir=dp, pri=pri, fem=fem, ovr=None, hkx=hkx, disabled=False, dar=True))

# resolve override folders
for r in rows:
    if r["ovr"] and not r["hkx"]:
        cand = [os.path.join(os.path.dirname(r["dir"]), r["ovr"]), os.path.join(r["dir"], r["ovr"])]
        for c in cand:
            if os.path.isdir(c):
                r["hkx"] = [os.path.relpath(os.path.join(a,f), c).replace("\\","/").lower() for a,_,fs in os.walk(c) for f in fs if f.lower().endswith(".hkx")]
                break
json.dump(rows, open(sys.argv[1], "w"), indent=1)
fem_files = collections.defaultdict(list)
for r in rows:
    if r["fem"]=="F" and not r["disabled"]:
        for h in r["hkx"]: fem_files[h].append((r["pri"], r["mod"]))
print(len(rows), "submods;", len(fem_files), "files touched by IsFemale submods")
for h in sorted(fem_files):
    print(h, "|", len(fem_files[h]), "|", sorted(set(x[1] for x in fem_files[h]))[:4])
