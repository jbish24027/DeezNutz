r"""Outfit Wheeler 3.0 "cannot unequip" fix (2026-09-03).

3.0's DLL calls ActorEquipManager::EquipObject with a_forceEquip = TRUE at all six call sites (the Papyrus
"abPreventRemoval" flag), so every piece the wheel equips is locked against removal in the vanilla inventory AND in the
wheel's own panel, whose UnequipObject passes a_forceEquip = FALSE. 2.8 passed FALSE everywhere (0 force-equip blocks in
its DLL, 6 in 3.0). This script flips the six equip sites to FALSE and lets the wheel's manual item toggle unequip with
FORCE (so pieces already locked in a save can be freed by clicking them in Edit Mode).

x64 arg layout of the CommonLib wrapper: rcx=manager rdx=actor r8=object r9=extraData [rsp+20]=count [rsp+28]=slot
[rsp+30]=queueEquip [rsp+38]=forceEquip [rsp+40]=playSounds [rsp+48]=applyNow. The compiler emits the three byte stores
as C6 44 24 48 01 / C6 44 24 40 01 / C6 44 24 38 XX, so the block is matched as a whole and only the last byte changes.

Usage: python patch_forceequip.py [--check | --apply | --revert]   (default --check; game/MO2 must be closed to apply)
"""
import os, sys, re, hashlib, shutil, subprocess, datetime

DLL = r"C:\1. AUTHORIA\mods\Outfit Wheeler - Dynamic Equipment Manager\SKSE\Plugins\OutfitWheeler-DynamicEquipmentManager.dll"
BACKUP_DIR = r"C:\1. AUTHORIA\_backups\2026-09-03 - Outfit Wheeler 3.0 forceequip patch"
ORIG_MD5 = "d206a75e8f42529310f9b4fcc0fbf2b5"      # shipped 3.0.0 DLL
EQUIP_BLOCK = bytes.fromhex("C644244801C644244001C6442438")      # [48]=1 [40]=1 [38]=?  -> next byte is forceEquip
TOGGLE_UNEQUIP_RVA = 0x3EEBC                                   # ToggleItemEquip's UnequipObject call (3.0.0)
IMAGE_BASE = 0x180000000

def sections(d):
    import struct
    pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
    out = []
    for i in range(nsec):
        s = pe + 24 + opt + i * 40; vsize, va, rsize, raw = struct.unpack_from("<IIII", d, s + 8); out.append((va, vsize, raw, rsize))
    return out
def rva2off(secs, rva):
    for va, vs, raw, rs in secs:
        if va <= rva < va + max(vs, rs): return raw + (rva - va)
    raise SystemExit(f"rva {rva:#x} not in any section")

def analyse(d):
    equip = [(m.start() + len(EQUIP_BLOCK), d[m.start() + len(EQUIP_BLOCK)]) for m in re.finditer(re.escape(EQUIP_BLOCK), d)]
    secs = sections(d); call_off = rva2off(secs, TOGGLE_UNEQUIP_RVA)
    win = d[call_off - 48:call_off]
    i = win.rfind(bytes.fromhex("C6442438"))
    toggle = (call_off - 48 + i + 4, win[i + 4]) if i >= 0 else None
    return equip, toggle

def main():
    mode = "--apply" if "--apply" in sys.argv else "--revert" if "--revert" in sys.argv else "--check"
    d = bytearray(open(DLL, "rb").read()); md5 = hashlib.md5(d).hexdigest()
    equip, toggle = analyse(d)
    print(f"DLL {len(d)} bytes md5 {md5} ({'shipped 3.0.0' if md5 == ORIG_MD5 else 'NOT the shipped 3.0.0 file'})")
    print("EquipObject arg blocks (offset, forceEquip):", [(hex(o), v) for o, v in equip])
    print("ToggleItemEquip UnequipObject forceEquip:", (hex(toggle[0]), toggle[1]) if toggle else "pattern not found")
    if mode == "--check": return
    running = subprocess.run(["powershell", "-NoProfile", "-Command",
        "Get-Process ModOrganizer,SkyrimSE,skse64_loader -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name"],
        capture_output=True, text=True).stdout.strip()
    if running: raise SystemExit("ABORT: running: " + running)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%H%M%S")
    shutil.copy2(DLL, os.path.join(BACKUP_DIR, f"OutfitWheeler-DynamicEquipmentManager.dll.{md5[:8]}.{stamp}"))
    if not toggle: raise SystemExit("toggle-unequip pattern not found - re-verify TOGGLE_UNEQUIP_RVA for this build")
    equip_sites = [(o, v) for o, v in equip if o != toggle[0]]      # the same byte prefix also matches the toggle's unequip block
    if mode == "--apply":
        if md5 != ORIG_MD5: raise SystemExit("refusing: unknown DLL build - re-verify the offsets with --check and update ORIG_MD5")
        assert len(equip_sites) == 6 and all(v == 1 for _, v in equip_sites) and toggle[1] == 0, (equip_sites, toggle)
        for o, _ in equip_sites: d[o] = 0
        d[toggle[0]] = 1
    else:
        if not all(v == 0 for _, v in equip_sites): raise SystemExit("revert: DLL is not in patched state")
        for o, _ in equip_sites: d[o] = 1
        d[toggle[0]] = 0
    open(DLL, "wb").write(d)
    e2, t2 = analyse(bytes(d))
    print("after:", [(hex(o), v) for o, v in e2], "| toggle unequip force =", t2[1], "| md5", hashlib.md5(d).hexdigest())

if __name__ == "__main__": main()
