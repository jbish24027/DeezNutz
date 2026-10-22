import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
prof = sys.argv[1] if len(sys.argv) > 1 else "DEEZ_CS_NUTZ_-_PBR"
P = json.load(open(os.path.join(HERE, f"presence_{prof}.json")))
stack = {}  # (type, fid) -> [(slot, plugin, mod)]
for p in P["plugins"]:
    for t, ids in p["records"].items():
        for fid in ids:
            stack.setdefault(t, {}).setdefault(fid, []).append((p["slot"], p["plugin"], p["mod"]))
out = {}
for t, d in stack.items():
    out[t] = {fid: {"winner": v[-1][1], "winner_mod": v[-1][2], "stack": [x[1] for x in v]} for fid, v in d.items()}
json.dump(out, open(os.path.join(HERE, f"winners_{prof}.json"), "w"), indent=0)
for t in ("REGN", "WTHR", "VOLI", "CLMT"):
    from collections import Counter
    c = Counter(v["winner"] for v in out.get(t, {}).values())
    print(t, len(out.get(t, {})), c.most_common(40))
