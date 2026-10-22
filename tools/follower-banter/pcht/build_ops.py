"""Build housecarl_apply ops that make every PC Head Tracking SNDR list every Eleonora clip in its folder."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ELEO = r"C:\1. AUTHORIA\mods\Eleonora - PC Head Tracking Voice Type\sound\fx\PC Head Tracking"

rows = [json.loads(l) for l in open(os.path.join(HERE, "sndr_winner.jsonl"), encoding="utf-8")][1:]
ops, report = [], []
for r in rows:
    files = [f["value"] for f in r["fields"] if f.get("path", "").startswith("SoundFiles") and "value" in f]
    if not files:
        report.append((r["editorid"], "no files listed", 0, 0)); continue
    first = files[0]
    m = re.match(r"(?i)^(data\\)?sound\\fx\\PC Head Tracking\\(.+)\\[^\\]+$", first)
    if not m:
        report.append((r["editorid"], "unparsed " + first, len(files), 0)); continue
    prefix = first[: first.lower().index("pc head tracking")] + "PC Head Tracking\\"
    sub = m.group(2)
    folder = os.path.join(ELEO, sub)
    have = sorted(f for f in os.listdir(folder) if f.lower().endswith(".wav")) if os.path.isdir(folder) else []
    if not have:
        report.append((r["editorid"], sub + " (Eleonora folder empty - unchanged)", len(files), 0)); continue
    new = [prefix + sub + "\\" + f for f in have]
    if [x.lower() for x in new] == [x.lower() for x in files]:
        report.append((r["editorid"], sub + " (already complete)", len(files), len(have))); continue
    ops.append({"formid": r["formid"], "field_path": "SoundFiles", "op": "ReplaceAll", "values": new})
    report.append((r["editorid"], sub, len(files), len(have)))

json.dump(ops, open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8"), indent=1)
for e, s, a, b in report:
    print(f"{e:24} {a:>3} -> {b:>3}  {s}")
print("ops:", len(ops))
