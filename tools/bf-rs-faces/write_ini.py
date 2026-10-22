"""Write the BF race add-on that hands out the face pool (2026-10-21).

BF appends each race add-on's baby lists (deduped), so vanilla races just gain
our faces on top of BF's RS pack. UBE races and Kaidan's Akaviri race are not in
BF's RS pack, so their sections also carry BF's original RS models.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MODS = r"C:\1. AUTHORIA\mods"
RS_INI = os.path.join(MODS, "Beeing Female NG", "BeeingFemale", "AddOn", "BFASE_RSChildren_SE_Opt.ini")
OUT = os.path.join(MODS, "Authoria - BF RS Children Faces", "BeeingFemale", "AddOn", "Authoria RS Children Faces.ini")
ME = "AuthoriaBFRSFaces"

# BF's own RS models per vanilla race, read from its ini: race section by first race id
rs = {}
cur = None
for line in open(RS_INI, encoding="utf-8", errors="replace"):
    line = line.strip()
    m = re.match(r"id=Skyrim:([0-9A-Fa-f]+)", line)
    if m:
        cur = m.group(1).upper(); rs.setdefault(cur, {}); continue
    m = re.match(r"(BabyActor_(?:Female|Male)(?:Player)?)=(.*)", line)
    if m and cur:
        rs[cur][m.group(1)] = m.group(2)

pool = {tuple(k.split("|")): v for k, v in json.load(open(os.path.join(HERE, "pool.json"))).items()}
def mine(race, sex):
    return [f"{ME}:{i:X}" for i in pool.get((race, sex), [])]

VAN = {"Nord": "13746", "Imperial": "13744", "Breton": "13741", "Redguard": "13748", "Orc": "13747",
       "HighElf": "13743", "WoodElf": "13749", "DarkElf": "13742"}
# (section label, race ids, races whose faces it gets)
SECTIONS = [
    ("Nord (vanilla + UBE)", ["Skyrim:13746", "Skyrim:7EAF3", "Skyrim:88794", "UBE_AllRace:5A184"], ["Nord"]),
    ("Imperial (vanilla + UBE)", ["Skyrim:13744", "Skyrim:88844", "UBE_AllRace:5A179"], ["Imperial"]),
    ("Breton (vanilla + UBE)", ["Skyrim:13741", "Skyrim:8883C", "UBE_AllRace:5734"], ["Breton"]),
    ("Redguard (vanilla + UBE)", ["Skyrim:13748", "Skyrim:88846", "UBE_AllRace:5A18E"], ["Redguard"]),
    ("Orc (vanilla + UBE)", ["Skyrim:13747", "Skyrim:A82B9", "UBE_AllRace:5A1B0"], ["Orc"]),
    ("Kaidan's Akaviri race (Vorstag) - Nord + Imperial faces", ["HSFVorstag:FA1"], ["Nord", "Imperial"]),
    ("UBE High Elf - BF's own RS models", ["UBE_AllRace:5A1A2"], ["HighElf"]),
    ("UBE Wood Elf - BF's own RS models", ["UBE_AllRace:5A1AC"], ["WoodElf"]),
    ("UBE Dark Elf - BF's own RS models", ["UBE_AllRace:5A198"], ["DarkElf"]),
]
out = ["# Authoria (2026-10-21): Beeing Female baby face pool from unused RS Children faces.",
       "# Built by _tools\\bf-rs-faces. BF picks one listed model at random.",
       "[AddOn]", "name=Authoria RS Children Faces",
       "description=Adds unused RS Children faces as baby models, and maps UBE races and the Akaviri race to RS children.",
       "author=Authoria", "type=race", f"required={ME}.esp,BeeingFemale_RS_PatchSE_ESPFE.esp,UBE_AllRace.esp,HSFVorstag.esp",
       "enabled=true", "hidden=false", "locked=false", f"races={len(SECTIONS)}", ""]
for n, (label, ids, races) in enumerate(SECTIONS, 1):
    out += [f"[Race{n}]", f"# {label}", "id=" + ",".join(ids)]
    for key, sex in (("BabyActor_Female", "girl"), ("BabyActor_FemalePlayer", "girl"),
                     ("BabyActor_Male", "boy"), ("BabyActor_MalePlayer", "boy")):
        vals = []
        for r in races:
            orig = rs[VAN[r]].get(key)
            if orig:
                vals.append(orig)
            if key.endswith("Player"):
                vals += mine(r, sex)
        out.append(f"{key}=" + ",".join(dict.fromkeys(vals)))
    out.append("")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\r\n").write("\n".join(out))
print(OUT)
print("\n".join(l for l in out if l.startswith(("[Race", "id=", "BabyActor_FemalePlayer"))))
