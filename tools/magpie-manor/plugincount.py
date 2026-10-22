import os, struct, sys, io

INST = r"C:\1. AUTHORIA"
PROFILE = os.path.join(INST, "profiles", "DEEZ CS NUTZ")
MODS = os.path.join(INST, "mods")
STOCK = os.path.join(INST, "Stock Game", "Data")

def read_lines(p):
    with open(p, encoding="utf-8-sig", errors="replace") as f:
        return [l.rstrip("\r\n") for l in f]

# modlist: first line = highest priority
enabled = [l[1:] for l in read_lines(os.path.join(PROFILE, "modlist.txt")) if l.startswith("+")]
# map plugin filename (lower) -> path, highest priority wins (first seen)
where = {}
for m in enabled:
    d = os.path.join(MODS, m)
    try:
        for fn in os.listdir(d):
            ln = fn.lower()
            if ln.endswith((".esp", ".esm", ".esl")) and ln not in where:
                where[ln] = os.path.join(d, fn)
    except FileNotFoundError:
        pass
# overwrite folder has top priority actually
ow = os.path.join(INST, "overwrite")
for fn in os.listdir(ow):
    ln = fn.lower()
    if ln.endswith((".esp", ".esm", ".esl")):
        where[ln] = os.path.join(ow, fn)
# stock game lowest
for fn in os.listdir(STOCK):
    ln = fn.lower()
    if ln.endswith((".esp", ".esm", ".esl")) and ln not in where:
        where[ln] = os.path.join(STOCK, fn)

def flags_of(path):
    with open(path, "rb") as f:
        hdr = f.read(24)
    if hdr[0:4] != b"TES4":
        return None
    return struct.unpack_from("<I", hdr, 8)[0]

active = [l[1:] for l in read_lines(os.path.join(PROFILE, "plugins.txt")) if l.startswith("*")]
loadorder = [l for l in read_lines(os.path.join(PROFILE, "loadorder.txt")) if l and not l.startswith("#")]
active_set = set(a.lower() for a in active)
# implicit = in loadorder but not in plugins.txt as * (and not present as unchecked line)
plugins_lines = set(l.lstrip("*").lower() for l in read_lines(os.path.join(PROFILE, "plugins.txt")) if l and not l.startswith("#"))
implicit = [p for p in loadorder if p.lower() not in plugins_lines]

full = []; light = []; missing = []
for p in list(implicit) + active:
    path = where.get(p.lower())
    if not path:
        missing.append(p); continue
    fl = flags_of(path)
    if fl is None:
        missing.append(p); continue
    is_light = bool(fl & 0x200) or p.lower().endswith(".esl")
    (light if is_light else full).append(p)

print(f"active (checked) plugins: {len(active)}; implicit: {len(implicit)}; total considered: {len(active)+len(implicit)}")
print(f"FULL (take a 0x00-0xFD slot): {len(full)}   LIGHT (ESL/flagged): {len(light)}   unresolved: {len(missing)}")
print(f"free full slots (254 cap incl. game masters, FE/FF reserved): {254 - len(full)}")
if missing:
    print("unresolved:", missing[:20])
# show last 15 full plugins in load order for context
print("\nlast 15 FULL plugins in load order:")
fullset = set(f.lower() for f in full)
tail = [p for p in loadorder if p.lower() in fullset][-15:]
for p in tail: print("  ", p)
