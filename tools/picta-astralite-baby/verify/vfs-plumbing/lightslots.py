"""Light-slot check: does the baby ESL shift any light slot referenced by _locationweather/_weatherlist? Read-only."""
import os, re, struct
INST = r"C:\1. AUTHORIA"
prof = os.path.join(INST, "profiles", "DEEZ CS NUTZ - PICTA x ASTRALITE")
ESP = "Authoria - Patch - Picta x Astralite.esp"
ml = [l for l in open(os.path.join(prof, "modlist.txt"), "rb").read().decode().split("\r\n") if l.startswith("+")]
enabled = [l[1:] for l in ml]  # top = highest priority
idx = {}
for m in reversed(enabled):  # lower priority first, higher overwrites
    d = os.path.join(INST, "mods", m)
    try:
        for f in os.listdir(d):
            if f.lower().endswith((".esp", ".esm", ".esl")):
                idx[f.lower()] = os.path.join(d, f)
    except FileNotFoundError:
        pass
sg = os.path.join(INST, "Stock Game", "Data")
for f in os.listdir(sg):
    if f.lower().endswith((".esp", ".esm", ".esl")) and f.lower() not in idx:
        idx[f.lower()] = os.path.join(sg, f)
pl = open(os.path.join(prof, "plugins.txt"), "rb").read().decode().split("\r\n")
active = {l[1:].lower() for l in pl if l.startswith("*")}
lo = [l for l in open(os.path.join(prof, "loadorder.txt"), "rb").read().decode().split("\r\n") if l and not l.startswith("#")]
explicit = {l.lstrip("*").lower() for l in pl if l and not l.startswith("#")}
def light(p):
    h = open(p, "rb").read(12)
    return bool(struct.unpack_from("<I", h, 8)[0] & 0x200) or p.lower().endswith(".esl")
slots = []
for name in lo:
    n = name.lower()
    is_active = n in active or n not in explicit  # implicit masters/CC are active
    if not is_active or n not in idx:
        continue
    if light(idx[n]):
        slots.append(name)
esl_slot = slots.index(ESP)
print("light plugins active:", len(slots), "baby ESL light slot: 0x%03X" % esl_slot)
for f in ("_locationweather.ini", "_weatherlist.ini"):
    t = open(os.path.join(INST, "mods", "Authoria - Picta x Astralite - E11", "enbseries", f), "rb").read().decode("utf-8", "replace")
    refs = sorted({int(x, 16) for x in re.findall(r"\bFE([0-9A-Fa-f]{3})[0-9A-Fa-f]{3}\b", t)})
    print(f, "light slots referenced:", ["0x%03X" % r for r in refs], "max", ("0x%03X" % max(refs)) if refs else None,
          "-> any >= ESL slot:", any(r >= esl_slot for r in refs))
    for r in refs:
        print("    0x%03X" % r, slots[r] if r < len(slots) else "OUT OF RANGE")
