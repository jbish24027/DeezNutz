import json, os, re, collections
SP = os.path.dirname(os.path.abspath(__file__))
MODS = r"C:\1. AUTHORIA\mods"
PROFILE = r"C:\1. AUTHORIA\profiles\DEEZ CS NUTZ - PICTA"

# enabled mods in priority order (low -> high)
ml = [l.strip() for l in open(os.path.join(PROFILE, "modlist.txt"), encoding="utf-8") if l.strip()]
enabled = [l[1:] for l in reversed(ml) if l.startswith("+")]

plugin_mod = {}
for m in enabled:
    d = os.path.join(MODS, m)
    try:
        for f in os.listdir(d):
            if f.lower().endswith((".esp", ".esm", ".esl")):
                plugin_mod[f.lower()] = m  # later (higher priority) wins
    except FileNotFoundError:
        pass

def facegen_in(mod, master, fid):
    base = os.path.join(MODS, mod, "meshes", "actors", "character", "facegendata", "facegeom", master)
    if not os.path.isdir(base):
        return None
    for f in os.listdir(base):
        if f.lower() == f"00{fid}.nif".lower():
            return os.path.join(base, f)
    return None

def facegen_mods(master, fid):
    return [m for m in enabled if facegen_in(m, master, fid)]

rows = [json.loads(l) for l in open(os.path.join(SP, "kids_tree.jsonl"), encoding="utf-8")][1:]
winners = {json.loads(l)["formid"]: json.loads(l) for l in list(open(os.path.join(SP, "kids_winners.jsonl"), encoding="utf-8"))[1:]}
out = []
for r in rows:
    fid, master = r["formid"].split(":", 1)
    fg = facegen_mods(master, fid)
    win_fg = fg[-1] if fg else None
    for n in r["nodes"]:
        if n.get("is_winner"):
            continue
        hp = [d for d in n.get("deltas", []) if d.startswith("HeadParts")]
        if not hp or "ABSENT" in hp[0] or hp[0].startswith("HeadParts: 0 vs"):
            continue
        mod = plugin_mod.get(n["plugin"].lower())
        has = facegen_in(mod, master, fid) if mod else None
        out.append(dict(formid=r["formid"], editorid=r["editorid"], loser=n["plugin"], loser_mod=mod,
                        loser_facegen=bool(has), facegen_winner_mod=win_fg, winner=r["reference"]))
json.dump(out, open(os.path.join(SP, "losers.json"), "w"), indent=1)
good = [o for o in out if o["loser_facegen"] and o["loser_mod"] != o["facegen_winner_mod"]]
print("losing appearances:", len(out), " with their own unused facegen:", len(good))
c = collections.Counter(o["loser_mod"] for o in good)
for k, v in c.most_common(): print(f"  {v:4}  {k}")
