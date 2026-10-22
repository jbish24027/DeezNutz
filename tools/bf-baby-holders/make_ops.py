"""Second pass for Authoria - Kaidan Holds Baby.esp: crib/misc scripts, branch
starting topics, and the BF baby-sling ARMAs extended to UBE races and
Kaidan's Akaviri race (BF only listed vanilla races, so the sling was
invisible on Luna and Kaidan)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = "Authoria - Kaidan Holds Baby.esp"
PLAYER = "000014:Skyrim.esm"
QUEST, MISC, EMPTY, FULL = f"000804:{P}", f"000805:{P}", f"000806:{P}", f"000807:{P}"
MENU_E, MENU_F = f"000802:{P}", f"000803:{P}"


def prop(name, obj):
    return {"type": "ScriptObjectProperty", "fields": {"Name": name, "Flags": "Edited", "Object": obj, "Alias": "-1"}}


def vmad(formid, script, props):
    return {"formid": formid, "field_path": "VirtualMachineAdapter", "compose": {"type": "VirtualMachineAdapter",
            "sets": [{"path": "Scripts", "verb": "Add", "compose": {"type": "ScriptEntry", "fields": {"Name": script},
                      "sets": [{"path": "Properties", "verb": "Add", "compose": p} for p in props]}}]}}


crib_props = [prop("PlayerRef", PLAYER), prop("QuestScript", QUEST), prop("AuthKBS_CribEmpty", EMPTY),
              prop("AuthKBS_CribFull", FULL), prop("CribFolded", MISC),
              prop("AuthKBS_CribMenuEmpty", MENU_E), prop("AuthKBS_CribMenuFull", MENU_F)]

ops = [
    vmad(MISC, "AuthKBS_CribItem", [prop("PlayerRef", PLAYER), prop("AuthKBS_CribEmpty", EMPTY), prop("QuestScript", QUEST)]),
    vmad(EMPTY, "AuthKBS_Crib", crib_props),
    vmad(FULL, "AuthKBS_Crib", crib_props),
    {"formid": f"000809:{P}", "field_path": "StartingTopic", "value": f"00080A:{P}"},
    {"formid": f"00080B:{P}", "field_path": "StartingTopic", "value": f"00080C:{P}"},
]

ARMAS = ["05D17B", "05D17C", "05D17F", "05D180", "061CF9", "061CFA", "061CFB", "061CFC", "061CFD", "061CFE"]
UBE = ["005734", "005735", "05A179", "05A17A", "05A184", "05A185", "05A18E", "05A18F", "05A198", "05A199",
       "05A1A2", "05A1A3", "05A1AC", "05A1AD", "05A1B0", "05A1B1", "07A4D5", "07A4D6"]
RACES = [f"{r}:UBE_AllRace.esp" for r in UBE] + ["000FA1:HSFVorstag.esp"]
for a in ARMAS:
    for r in RACES:
        ops.append({"formid": f"{a}:BeeingFemale.esm", "field_path": "AdditionalRaces", "op": "Add", "value": r})

json.dump(ops, open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8"), indent=1)
print(len(ops), "ops")
