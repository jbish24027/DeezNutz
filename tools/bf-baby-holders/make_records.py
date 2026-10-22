"""Writes records.json for housecarl_create: Authoria - Kaidan Holds Baby."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYER, KAIDAN_REF, KAIDAN_NPC = "000014:Skyrim.esm", "002F9C:0Kaidan.esp", "002F9A:0Kaidan.esp"
BABIES = ["05D17D", "05D17E", "05D182", "05D183", "061CFF", "061D00", "061D01", "061D02", "061D03", "061D04"]


def prop(name, obj, alias="-1"):
    return {"type": "ScriptObjectProperty", "fields": {"Name": name, "Flags": "Edited", "Object": obj, "Alias": alias}}


def script(name, props):
    return {"type": "ScriptEntry", "fields": {"Name": name},
            "sets": [{"path": "Properties", "verb": "Add", "compose": p} for p in props]}


def vmad(name, props):
    return {"field_path": "VirtualMachineAdapter", "compose": {"type": "VirtualMachineAdapter",
            "sets": [{"path": "Scripts", "verb": "Add", "compose": script(name, props)}]}}


def cond(data_type, fields, op="EqualTo", value="1", sets=()):
    return {"type": "ConditionFloat", "fields": {"CompareOperator": op, "ComparisonValue": value},
            "sets": [{"path": "Data", "compose": {"type": data_type, "fields": fields, "sets": list(sets)}}]}


IS_KAIDAN = cond("GetIsIDConditionData", {"RunOnType": "Subject"}, sets=[{"path": "Object", "value": KAIDAN_NPC}])

crib_props = [prop("PlayerRef", PLAYER), prop("QuestScript", "@AuthKBS_Quest"),
              prop("AuthKBS_CribEmpty", "@AuthKBS_CribEmpty"), prop("AuthKBS_CribFull", "@AuthKBS_CribFull"),
              prop("CribFolded", "@AuthKBS_CribFolded"),
              prop("AuthKBS_CribMenuEmpty", "@AuthKBS_CribMenuEmpty"), prop("AuthKBS_CribMenuFull", "@AuthKBS_CribMenuFull")]


def crib(edid, model):
    return {"record_type": "Container", "editorid": edid, "ops": [
        {"field_path": "Name", "value": "Crib"},
        {"field_path": "Model", "compose": {"type": "Model", "fields": {"File": model}}},
        {"field_path": "Weight", "value": "0"}]}


def button(text):
    return {"type": "MessageButton", "sets": [{"path": "Text", "value": text}]}


def menu(edid, desc, buttons):
    return {"record_type": "Message", "editorid": edid, "ops": [
        {"field_path": "Description", "value": desc},
        {"field_path": "Flags", "value": "MessageBox"},
        {"field_path": "MenuButtons", "op": "ReplaceAll", "composes": [button(b) for b in buttons]}]}


def topic(edid, branch, prompt):
    return [
        {"record_type": "DialogBranch", "editorid": branch, "ops": [
            {"field_path": "Quest", "value": "@AuthKBS_Quest"},
            {"field_path": "Flags", "value": "TopLevel"}]},
        {"record_type": "DialogTopic", "editorid": edid, "ops": [
            {"field_path": "Name", "value": prompt},
            {"field_path": "Quest", "value": "@AuthKBS_Quest"},
            {"field_path": "Branch", "value": "@" + branch},
            {"field_path": "Category", "value": "Topic"},
            {"field_path": "Subtype", "value": "Custom"},
            {"field_path": "Priority", "value": "50"}]}]


def lines(edid, parent, texts, conds, tif):
    out = []
    for i, t in enumerate(texts, 1):
        flags = "Random" if i < len(texts) else "Random, RandomEnd"
        out.append({"record_type": "DialogResponses", "editorid": f"{edid}_{i}", "parent": parent, "ops": [
            {"field_path": "Responses", "op": "Add", "compose": {"type": "DialogResponse",
                "fields": {"Emotion": "Happy", "EmotionValue": "50", "ResponseNumber": "1"},
                "sets": [{"path": "Text", "value": t}]}},
            {"field_path": "Flags", "compose": {"type": "DialogResponseFlags", "fields": {"Flags": flags}}},
            {"field_path": "Conditions", "op": "ReplaceAll", "composes": conds},
            {"field_path": "VirtualMachineAdapter", "compose": {"type": "DialogResponsesAdapter", "sets": [
                {"path": "Scripts", "verb": "Add", "compose": {"type": "ScriptEntry", "fields": {"Name": tif}}},
                {"path": "ScriptFragments.FileName", "value": tif},
                {"path": "ScriptFragments.OnEnd", "compose": {"type": "ScriptFragment",
                    "fields": {"ScriptName": tif, "FragmentName": "Fragment_0"}}}]}}]})
    return out


records = [
    {"record_type": "GlobalShort", "editorid": "AuthKBS_CanHand", "ops": [{"field_path": "Data", "value": "0"}]},
    {"record_type": "FormList", "editorid": "AuthKBS_BabyItems", "ops": [
        {"field_path": "Items", "op": "ReplaceAll", "values": [f"{b}:BeeingFemale.esm" for b in BABIES]}]},
    menu("AuthKBS_CribMenuEmpty", "The crib is empty.", ["Lay the baby down", "Fold up the crib", "Leave"]),
    menu("AuthKBS_CribMenuFull", "The baby is asleep.", ["Pick the baby up", "Leave"]),
    {"record_type": "MiscItem", "editorid": "AuthKBS_CribFolded", "ops": [
        {"field_path": "Name", "value": "Folded Crib"},
        {"field_path": "Model", "compose": {"type": "Model", "fields": {"File": "Authoria\\BabyCrib\\CribEmpty.nif"}}},
        {"field_path": "Weight", "value": "6"}, {"field_path": "Value", "value": "40"}]},
    crib("AuthKBS_CribEmpty", "Authoria\\BabyCrib\\CribEmpty.nif"),
    crib("AuthKBS_CribFull", "Authoria\\BabyCrib\\CribBaby.nif"),
    {"record_type": "ConstructibleObject", "editorid": "AuthKBS_CribRecipe", "ops": [
        {"field_path": "CreatedObject", "value": "@AuthKBS_CribFolded"},
        {"field_path": "CreatedObjectCount", "value": "1"},
        {"field_path": "WorkbenchKeyword", "value": "07866A:Skyrim.esm"},
        {"field_path": "Items", "op": "ReplaceAll", "composes": [
            {"type": "ContainerEntry", "sets": [{"path": "Item", "compose": {"type": "ContainerItem", "fields": {"Item": it, "Count": n}}}]}
            for it, n in (("06F993:Skyrim.esm", "4"), ("0800E4:Skyrim.esm", "3"), ("0DB5D2:Skyrim.esm", "1"))]}]},
    {"record_type": "Quest", "editorid": "AuthKBS_Quest", "ops": [
        {"field_path": "Name", "value": "Kaidan Holds the Baby"},
        {"field_path": "Flags", "value": "StartGameEnabled"},
        {"field_path": "Priority", "value": "60"},
        {"field_path": "Aliases", "op": "ReplaceAll", "composes": [
            {"type": "QuestAlias", "fields": {"ID": "0", "Name": "Player"}, "sets": [{"path": "ForcedReference", "value": PLAYER}]},
            {"type": "QuestAlias", "fields": {"ID": "1", "Name": "Kaidan"}, "sets": [{"path": "ForcedReference", "value": KAIDAN_REF}]}]},
        {"field_path": "VirtualMachineAdapter", "compose": {"type": "QuestAdapter", "sets": [
            {"path": "Scripts", "verb": "Add", "compose": script("AuthKBS_QuestScript", [
                prop("PlayerRef", PLAYER), prop("KaidanRef", KAIDAN_REF),
                prop("AuthKBS_BabyItems", "@AuthKBS_BabyItems"), prop("AuthKBS_CanHand", "@AuthKBS_CanHand")])},
            {"path": "Aliases", "verb": "Add", "compose": {"type": "QuestFragmentAlias", "sets": [
                {"path": "Property", "compose": prop("", "@AuthKBS_Quest", "0")},
                {"path": "Scripts", "verb": "Add", "compose": script("AuthKBS_PlayerAlias", [
                    prop("QuestScript", "@AuthKBS_Quest"), prop("AuthKBS_BabyItems", "@AuthKBS_BabyItems")])}]}},
            {"path": "Aliases", "verb": "Add", "compose": {"type": "QuestFragmentAlias", "sets": [
                {"path": "Property", "compose": prop("", "@AuthKBS_Quest", "1")},
                {"path": "Scripts", "verb": "Add", "compose": script("AuthKBS_KaidanAlias", [
                    prop("QuestScript", "@AuthKBS_Quest"), prop("AuthKBS_BabyItems", "@AuthKBS_BabyItems")])}]}}]}}]},
]
records += topic("AuthKBS_GiveTopic", "AuthKBS_GiveBranch", "Can you hold the baby for a while?")
records += topic("AuthKBS_TakeTopic", "AuthKBS_TakeBranch", "I'll take the baby back now.")

give_conds = [IS_KAIDAN,
              cond("GetGlobalValueConditionData", {"RunOnType": "Subject"}, sets=[{"path": "Global", "value": "@AuthKBS_CanHand"}]),
              cond("GetItemCountConditionData", {"RunOnType": "Subject"}, value="0",
                   sets=[{"path": "ItemOrList", "value": "@AuthKBS_BabyItems"}])]
take_conds = [IS_KAIDAN,
              cond("GetItemCountConditionData", {"RunOnType": "Subject"}, op="GreaterThan", value="0",
                   sets=[{"path": "ItemOrList", "value": "@AuthKBS_BabyItems"}])]

GIVE = ["Come here, little one. I've got you.",
        "Hand them over, love. Go on, I'll keep them safe.",
        "Look at that face. Aye, I've got them. Take a breath, lass."]
TAKE = ["Here you go, back to your mama. No trouble at all.",
        "Already? They like me better, you know.",
        "Careful now. They only just dozed off."]
records += lines("AuthKBS_Give", "AuthKBS_GiveTopic", GIVE, give_conds, "AuthKBS_TIF_Give")
records += lines("AuthKBS_Take", "AuthKBS_TakeTopic", TAKE, take_conds, "AuthKBS_TIF_Take")

order = ["GlobalShort", "FormList", "Message", "Quest", "MiscItem", "Container", "ConstructibleObject"]
head = [r for r in records if r["record_type"] in order]
head.sort(key=lambda r: order.index(r["record_type"]))
records = head + [r for r in records if r["record_type"] not in order]
json.dump(records, open(os.path.join(HERE, "records.json"), "w", encoding="utf-8"), indent=1)
print(len(records), "records")
