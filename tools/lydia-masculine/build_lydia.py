"""Build the Lydia masculine idle/sit OAR mod. Usage: python -I build_lydia.py <rows.json> <scope.json> <bsa_root> <out_mod_dir>"""
import json, os, shutil, sys

rows_path, scope_path, bsa, out = sys.argv[1:5]
rows = json.load(open(rows_path))
scope = json.load(open(scope_path))
ANIM = os.path.join(bsa, "meshes", "actors", "character", "animations")
OAR = os.path.join(out, "meshes", "actors", "character", "animations", "OpenAnimationReplacer", "Authoria Lydia Masculine")
LYDIA = {"condition": "IsActorBase", "requiredVersion": "1.0.0.0",
         "Actor base": {"pluginName": "Skyrim.esm", "formID": "A2C8E"}}
used = set(r["pri"] for r in rows)
made = []


def write_sub(name, desc, pri, conds, files, extra=None):
    assert pri not in used, pri
    used.add(pri)
    d = os.path.join(OAR, name)
    os.makedirs(d, exist_ok=True)
    cfg = {"name": name, "description": desc, "priority": pri}
    if extra:
        cfg.update(extra)
    cfg["conditions"] = conds
    with open(os.path.join(d, "config.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
    for src, rel in files:
        dst = os.path.join(d, *rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    made.append((pri, name, len(files)))


def find(mod, sub):
    hit = [r for r in rows if r["mod"] == mod and os.path.basename(r["dir"]) == sub]
    assert len(hit) == 1, (mod, sub, len(hit))
    return hit[0]


def src_file(r, rel):
    base = r["dir"]
    cfg = json.load(open(os.path.join(base, "config.json"), encoding="utf-8-sig"))
    ovr = cfg.get("overrideAnimationsFolder")
    for root in ([os.path.join(os.path.dirname(base), ovr), os.path.join(base, ovr)] if ovr else []) + [base]:
        for dp, _, fs in os.walk(root):
            for f in fs:
                if os.path.relpath(os.path.join(dp, f), root).replace("\\", "/").lower() == rel:
                    return os.path.join(dp, f), cfg
    raise FileNotFoundError((r["dir"], rel))


def twin(mod, sub, src_rel, dst_rel, pri, label):
    r = find(mod, sub)
    pairs = []
    cfg = None
    for s, d in zip(src_rel, dst_rel):
        p, cfg = src_file(r, s)
        pairs.append((p, d))
    # Drop the "is male" gate, and any OR group built around it (MFAP: "male OR one of the
    # vanilla opposite-gender women") - Lydia is the target, so the gate is replaced by hers.
    def male_gate(c):
        return c.get("condition") == "IsFemale" and c.get("negated")
    conds = [c for c in cfg.get("conditions", [])
             if not male_gate(c)
             and not (c.get("condition") == "OR" and any(male_gate(x) for x in c.get("Conditions", [])))]
    conds.append(LYDIA)
    extra = {k: v for k, v in cfg.items()
             if k not in ("name", "description", "priority", "conditions", "overrideAnimationsFolder", "disabled")}
    write_sub(label, f"Lydia copy of '{mod} / {sub}' (priority {cfg['priority']}), so she plays what a male NPC plays.",
              pri, conds, pairs, extra)


# 1. Plain male standing idle and chair set, in place of the female set she reads.
files = [(os.path.join(ANIM, "male", f), "female/" + f.lower()) for f in scope]
files += [(os.path.join(ANIM, f), f) for f in ("aobarstoolidleplayer.hkx", "special_jarlchairidlewr.hkx")]
write_sub("Lydia 00 Male Base Idle and Chairs",
          "Vanilla male standing idles and chair animations for Lydia, beating the feminine idle and sitting mods.",
          900100, [LYDIA], files)

# 2. Improved Table Sit (unisex) above the base, as for a man.
for i, sub in enumerate(["aMain Transitions Idles", "aMain Transitions Idles HH", "bLifted Hands Idles", "bLifted Hands Idles HH"]):
    twin("Improved Table Sit Transition Animations", sub, ["aobartableidleplayer.hkx"], ["aobartableidleplayer.hkx"],
         900101 + i, f"Lydia 0{i+1} Table Sit {sub}")

# 3. Male Furniture Animation Pack chairs, moved from the male path to her female path.
for n, p in [(1, 888888127), (2, 888888130), (3, 888888131), (4, 888888132), (5, 888888167), (6, 888888170)]:
    twin("Male Furniture Animation Pack", f"Chair {n}", ["male/chair_idlebasevar1.hkx"], ["female/chair_idlebasevar1.hkx"],
         p + 1000000, f"Lydia 1{n} Male Chair {n}")

# 4. Male Furniture Animation Pack throne.
twin("Male Furniture Animation Pack", "Jarl Sit", ["special_jarlchairidlewr.hkx"], ["special_jarlchairidlewr.hkx"],
     889888115, "Lydia 20 Male Jarl Sit")

# 5. Ground and ledge sitting: vanilla, then Take a Seat, then the male cross-legged set.
write_sub("Lydia 30 Male Base Ground and Ledge Sit",
          "Vanilla cross-legged and ledge sitting for Lydia, beating the feminine versions.",
          998889000, [LYDIA], [(os.path.join(ANIM, f), f) for f in ("idlesit_crosslegged.hkx", "idlesitledge.hkx")])
for n in range(1, 7):
    twin("Take a Seat - New Sitting Animations for OAR or DAR", f"Sitting Animation {n}",
         ["idlesitledge.hkx", "idlesit_crosslegged.hkx"], ["idlesitledge.hkx", "idlesit_crosslegged.hkx"],
         998889000 + n, f"Lydia 3{n} Take a Seat {n}")
for n, p in [(1, 888888128), (2, 888888129), (3, 888888167), (4, 888888169)]:
    twin("Male Furniture Animation Pack", f"Cross Legged {n}", ["idlesit_crosslegged.hkx"], ["idlesit_crosslegged.hkx"],
         p + 110001000, f"Lydia 4{n} Male Cross Legged {n}")

with open(os.path.join(OAR, "..", "Authoria Lydia Masculine", "config.json"), "w", encoding="utf-8") as f:
    json.dump({"name": "Authoria - Lydia Masculine Idles and Sitting", "author": "Authoria",
               "description": "Lydia only: male standing idles and sitting, mirroring what a male NPC plays."}, f, indent=4)
for m in sorted(made):
    print(m)
