import json, os
src = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\91294a0d-ce03-47eb-8c5f-7425e9bd2ed4\tasks\wvo1huma5.output"
out = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(src, encoding='utf-8'))["result"]
json.dump(r["final"], open(os.path.join(out, "design_final.json"), "w", encoding="utf-8"), indent=1)
json.dump(r["judges"], open(os.path.join(out, "design_judges.json"), "w", encoding="utf-8"), indent=1)
json.dump(r["verdicts"], open(os.path.join(out, "design_verdicts.json"), "w", encoding="utf-8"), indent=1)
json.dump(r["designs"], open(os.path.join(out, "design_pitches.json"), "w", encoding="utf-8"), indent=1)
for k in ("final", "judges", "verdicts"):
    print(k, len(json.dumps(r[k])))
for j in r["judges"]:
    if j:
        print("WINNER", j["winner"], [(s["key"], s["total"]) for s in j["scores"]])
for v in r["verdicts"]:
    if v:
        print("VERDICT", v["verdict"][:400])
        for f in v["findings"]:
            print("  ", f["severity"], "|", f["claim"][:200])
