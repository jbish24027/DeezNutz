"""Ops manifest for the Beeing Female Requiem consumable patch (2026-10-21)."""
import json, os
VIP = "08CDEC:Skyrim.esm"   # VendorItemPotion
ALCH = {  # formid: (value, BF keyword to keep or None, flags)
    "0038C9:BeeingFemale.esm": (50, "00BA3A:BeeingFemale.esm", "NoAutoCalc, Medicine"),     # contraception low
    "0038CB:BeeingFemale.esm": (100, "00BA3A:BeeingFemale.esm", "NoAutoCalc, Medicine"),    # contraception medium
    "006E86:BeeingFemaleBasicAddOn.esp": (150, "00BA3A:BeeingFemale.esm", "NoAutoCalc, Medicine"),  # contraception high
    "00E55D:BeeingFemale.esm": (50, None, "NoAutoCalc"),     # wash out 60
    "00B4D5:BeeingFemale.esm": (75, None, "NoAutoCalc"),     # wash out 75
    "00E55B:BeeingFemale.esm": (100, None, "NoAutoCalc"),    # wash out 100
    "06D54F:BeeingFemale.esm": (50, "06D54C:BeeingFemale.esm", "NoAutoCalc, Medicine"),     # fertility mild
    "06D551:BeeingFemale.esm": (100, "06D54C:BeeingFemale.esm", "NoAutoCalc, Medicine"),    # fertility potent
    "000D72:BeeingFemaleSE_Opt.esp": (100, "000D6F:BeeingFemaleSE_Opt.esp", "NoAutoCalc, Medicine"),  # abortion draught
}
COOKPOT = ["00B4D4:BeeingFemale.esm", "00BF9E:BeeingFemale.esm", "00D52C:BeeingFemale.esm", "00EAC1:BeeingFemale.esm",
           "00EAC2:BeeingFemale.esm", "00EAC3:BeeingFemale.esm", "010051:BeeingFemale.esm", "06D550:BeeingFemale.esm",
           "06D552:BeeingFemale.esm", "006E88:BeeingFemaleBasicAddOn.esp", "000D73:BeeingFemaleSE_Opt.esp"]
ops = []
for fid, (val, kw, flags) in ALCH.items():
    ops += [{"formid": fid, "field_path": "Value", "value": str(val)},
            {"formid": fid, "field_path": "Weight", "value": "0.5"},
            {"formid": fid, "field_path": "Flags", "value": flags},
            {"formid": fid, "field_path": "Keywords", "op": "ReplaceAll", "values": [VIP] + ([kw] if kw else [])}]
for fid in COOKPOT:
    ops += [{"formid": fid, "field_path": "Conditions", "op": "Add",
             "compose": {"type": "ConditionFloat", "fields": {"CompareOperator": "EqualTo", "ComparisonValue": "1", "Flags": "OR"}}},
            {"formid": fid, "field_path": "Conditions[0].Data", "op": "Set",
             "compose": {"type": "HasPerkConditionData", "sets": [{"path": "Perk", "value": "0BE127:Skyrim.esm"}]}},
            {"formid": fid, "field_path": "Conditions", "op": "Add",
             "compose": {"type": "ConditionFloat", "fields": {"CompareOperator": "EqualTo", "ComparisonValue": "1"}}},
            {"formid": fid, "field_path": "Conditions[1].Data", "op": "Set",
             "compose": {"type": "HasKeywordConditionData", "sets": [{"path": "Keyword", "value": "AD3A3B:Requiem.esp"}]}}]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requiem_ops.json")
json.dump(ops, open(out, "w"), indent=1)
print(out, len(ops))
