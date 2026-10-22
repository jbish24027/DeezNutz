import json
from wlib import *
W = winners()
dw = plugin_records("Authoria - Patch - Astralite Dawn Warmth.esp")
res = {}
from collections import Counter
prevc = Counter(); diffs_total = 0
for fid, rec in dw.items():
    st = W["WTHR"][fid]["stack"]
    i = st.index("Authoria - Patch - Astralite Dawn Warmth.esp")
    prev = st[i-1]
    after = st[i+1:]
    pr = plugin_records(prev).get(fid)
    if pr is None:
        res[fid] = {"editorid": rec["editorid"], "prev": prev, "note": "prev not dumped"}
        prevc[prev + " (NOT DUMPED)"] += 1
        continue
    a, b = rec["fields"], pr["fields"]
    keys = set(a) | set(b)
    ignore = {"FormVersion", "VersionControl", "Version2", "MajorRecordFlagsRaw", "SkyrimMajorRecordFlags"}
    d = [k for k in keys if k not in ignore and a.get(k) != b.get(k)]
    diffs_total += len(d)
    prevc[prev] += 1
    res[fid] = {"editorid": rec["editorid"], "prev": prev, "after": after, "ndiff": len(d), "diff_keys": d[:20]}
json.dump(res, open("noop_check_dawnwarmth.json", "w"), indent=1)
print("prev providers", prevc)
print("total diffs", diffs_total)
for fid, r in res.items():
    if r.get("ndiff") or r.get("note") or r.get("after"):
        print(fid, r)
