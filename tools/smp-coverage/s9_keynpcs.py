import json, collections, os
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
npcs = json.load(open(sp + r"\npc_hair.json"))
outs = {o["fid"]: o for o in json.load(open(sp + r"\npc_outfit.json"))}
def bucket(n):
    if n["fg_phys"]: return "A"
    if n["hair_phys"]: return "B" if n["fg"] else "B2"
    if n["equiv"]: return "C"
    return "D"
names = ["Lydia", "Serana", "Kaidan", "Inigo", "Auri", "Lucien", "Mrissi", "Remiel", "Aela", "Jenassa", "Ysolda", "Carlotta Valentia",
         "Elisif the Fair", "Jarl Balgruuf the Greater", "Ulfric Stormcloak", "General Tullius", "Legate Rikke", "Delphine", "Esbern",
         "Farkas", "Vilkas", "Njada Stonearm", "Ria", "Brynjolf", "Vex", "Karliah", "Mjoll the Lioness", "Uthgerd the Unbroken",
         "Camilla Valerius", "Sven", "Faendal", "Gerdur", "Hod", "Ralof", "Hadvar", "Astrid", "Babette", "Cicero", "Nazir",
         "Tolfdir", "Mirabelle Ervine", "Brelyna Maryon", "Onmund", "J'zargo", "Isran", "Valerica", "Frea", "Neloth", "Eleonora",
         "Zora Fair-Child", "Rumarin", "Anum-La", "Vilja", "Sofia", "Recorder", "Hjalmar", "Danica Pure-Spring", "Hulda", "Saadia",
         "Irileth", "Proventus Avenicci", "Adrianne Avenicci", "Belethor", "Nazeem", "Olfina Gray-Mane", "Idolaf Battle-Born",
         "Maven Black-Briar", "Ingun Black-Briar", "Haelga", "Svana Far-Shield", "Grelka", "Marcurio", "Sapphire", "Tonilia",
         "Illia", "Erik the Slayer", "Benor", "Annekke Crag-Jumper", "Eola", "Taarie", "Endarie", "Jordis the Sword-Maiden",
         "Argis the Bulwark", "Iona", "Calder", "Gregor", "Rayya", "Valdimar", "Birna", "Ranmir", "Suvaris Atheron"]
seen = set()
rows = []
for n in npcs:
    if n["name"] in names and n["name"] not in seen:
        seen.add(n["name"])
        o = outs.get(n["fid"], {})
        body = o.get("body") or []
        rows.append((n["name"], bucket(n), n["fam"], os.path.basename(n["model"] or "") or "(no model)", n["fg_win"] or "no bake",
                     o.get("outfit_eid"), "yes" if o.get("any_phys") else ("no" if o.get("outfit") else "-"),
                     (body[0][1] or body[0][0]) if body else "-", body[0][3] if body else "-"))
for r in sorted(rows, key=lambda r: names.index(r[0])):
    print(" | ".join(str(x) for x in r))
missing = [x for x in names if x not in seen]
print("not found:", missing)
# counts for unnamed too
c = collections.Counter(bucket(n) for n in npcs if not n["name"])
print("UNNAMED", sorted(c.items()))
# B named by hair style (vanilla) top
c = collections.Counter(os.path.basename(n["model"]).lower() for n in npcs if n["name"] and bucket(n) == "B")
print("B styles top", c.most_common(12))
# how many B named have face winner = vanilla BSA / original mod BSA vs overhaul
# A list
print("== A named")
for n in npcs:
    if n["name"] and bucket(n) == "A":
        print("  ", n["name"], "|", n["plugin"], "|", n["fg_win"], "|", os.path.basename(n["model"] or ""))
