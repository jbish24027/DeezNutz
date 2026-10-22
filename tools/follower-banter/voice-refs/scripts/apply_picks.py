"""Write the user's 21-22 Oct voice-test picks into chosen_refs.json (key "_settings") and the voice-refs copy."""
import json, os
S = os.path.dirname(os.path.abspath(__file__))
SET = {
    "Ashe": {"prefer_refs": [1], "seed": 7, "speed": 1.0, "status": "settled", "user": "take 1 is closest on each"},
    "Gore": {"prefer_refs": [4, 3], "seed": 77, "speed": 1.0, "status": "settled 22 Oct: new clip 4 + clip 3 seed 77",
             "user": "01 new clip 4 is good. 02 new clip 4 is the only time he says bow correctly but I liked seed 77",
             "note": "clip 4 tends to end rising - keep the QA reroll; 'bow' (weapon) is misread by clip 3, consider a respelling"},
    "Inigo": {"prefer_refs": [1, 3], "seed": 7, "speed": 1.0, "status": "settled",
              "user": "02 take 1 and take 3 are good, 04 take 1 is great"},
    "Kaidan": {"prefer_refs": [3], "seed": 42, "speed": 0.82, "status": "settled 22 Oct: clip 3 at speed 0.82",
               "user": "01 feels like he lost his accent a little. 02 .82 is best",
               "note": "slowing can thin his accent on some lines - check accent in the first full-run batch"},
    "Lucien": {"prefer_refs": [3, 2, 1], "seed": 42, "speed": 1.0, "status": "settled; mixed picks, make takes from clips 3 and 2",
               "user": "01 take 3 is great 02 take 1 is best 03 take 3, 04 take 2, and 05 take 2 are best"},
    "Redcap": {"prefer_refs": [1], "seed": 7, "speed": 1.0, "status": "settled", "user": "take ones are best"},
    "Remiel": {"prefer_refs": [1, 2], "seed": 42, "speed": 1.0, "status": "settled; best takes were clip 1 (3) and clip 2 (2)",
               "user": "take 1, 02 take 3, 03 take 2, 04 take 3, 05 take 1 best"},
    "Serana": {"prefer_refs": [1], "seed": 7, "speed": 1.0, "status": "settled", "user": "take 1 is best"},
    "Val Serano": {"prefer_refs": [1], "seed": 7, "speed": 0.92, "status": "settled 22 Oct: clip 1 at speed 0.92",
                   "user": "take 1 is best but needs a tiny bit more time between words / .92 is good"},
    "Xelzaz": {"prefer_refs": [2], "seed": 31, "speed": 1.0, "status": "settled", "user": "take 2 is closest"},
    "Luna": {"prefer_refs": [1, 2], "seed": 7, "speed": 1.0, "status": "settled 22 Oct: all takes good, keep as is", "user": "Lunas lines were all so good"},
}
for p in (os.path.join(S, "chosen_refs.json"), os.path.join(os.path.dirname(S), "chosen_refs.json")):
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    if os.path.basename(os.path.dirname(p)) == "voice-refs":   # keep the top copy in step with the scripts copy
        d = json.load(open(os.path.join(S, "chosen_refs.json"), encoding="utf-8"))
    d["_settings"] = SET
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok")
