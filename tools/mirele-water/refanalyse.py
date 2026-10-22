"""Analyse refs.json: winners, movers, disabled/deleted, base object census."""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from refscan_placed import load_order, TARGET_GRIDS

d = json.load(open(os.path.join(HERE, "refs.json")))
order = load_order()
oi = {n.lower(): i for i, n in enumerate(order)}

cellgrid = {}
for c in d["cells"]:
    cellgrid[c["cell"]] = tuple(c["grid"])

refs = d["refs"]

winners = {}
movers = []
for key, places in refs.items():
    places.sort(key=lambda r: oi.get(r["plugin"].lower(), 10 ** 9))
    w = places[-1]
    winners[key] = w
    if len(places) > 1:
        ps = [tuple(round(v, 1) for v in (r.get("pos") or (0, 0, 0))) for r in places]
        if len(set(ps)) > 1:
            movers.append((key, [(r["plugin"], r.get("pos"), r.get("scale"),
                                  r["disabled"], r["deleted"]) for r in places]))

print("== winners: %d" % len(winners))
per_cell = collections.Counter(cellgrid.get(w["cell_key"], "?") for w in winners.values())
print("per cell:", dict(per_cell))

dis = [w for w in winners.values() if w["disabled"]]
dele = [w for w in winners.values() if w["deleted"]]
print("winning refs initially-disabled: %d, deleted: %d" % (len(dis), len(dele)))

# base object census
basec = collections.Counter(w.get("base_key") for w in winners.values())
print("unique base objects: %d" % len(basec))

json.dump({"winners": winners, "movers": movers,
           "bases": basec.most_common()},
          open(os.path.join(HERE, "refwin.json"), "w"))

print("\n== movers (same FormID placed at different positions): %d" % len(movers))
for k, v in movers[:60]:
    print(" ", k)
    for p in v:
        print("     ", p[0], p[1], "scale", p[2], "dis", p[3], "del", p[4])

print("\n== disabled winners")
for w in dis:
    print(" ", w["key"], "base", w.get("base_key"), "pos", w.get("pos"),
          "cell", cellgrid.get(w["cell_key"]), "by", w["plugin"])
print("\n== deleted winners")
for w in dele:
    print(" ", w["key"], "base", w.get("base_key"), "pos", w.get("pos"), "by", w["plugin"])
