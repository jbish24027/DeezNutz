r"""Outfit Wheeler 3.0: restore "re-select the worn outfit = take it off" (2026-09-03, v3 2026-09-04 after review).

2.6/2.8's Play Mode hint read "A: Equip / Unequip"; 3.0 reads "A: Equip Outfit" and its EquipSlot task simply re-equips
a full outfit (only Addon slots toggle). This patches the mod's own UI (PrismaUI/views/PrismaOutfitWheel/app.js):

1. equipOutfit(): in PLAY MODE ONLY (the studio's slot rail also routes through equipOutfit, so Edit Mode keeps the
   stock behaviour), a click / A on a FULL outfit that is currently worn stores it in the wardrobe
   (window.StashSlotOutfit - the DLL unequips the worn pieces and moves every slot piece into the chest) when
   Auto-Stash is on, else unequips the worn pieces in place (window.ToggleItemEquip, once per FormID, only when the
   wheel's active target is the player - the DLL's toggle acts on the active target actor).
2. window.openWheel(): the DLL's stash/toggle tasks rebuild the wheel with the edit-mode flag HARD-CODED ON
   (mov dl,1 before the JSON builder 0x5D110; the DLL keeps no edit-mode state for them), which threw the user into the
   3D studio after the unequip (v1 bug). The override is now a COUNTER of the rebuilds we caused (1 for the stash,
   N for N toggles) with a 1.5 s safety cap, so a genuine edit-hotkey open is never forced to Play Mode. When the last
   expected rebuild lands and the slot is no longer worn, the wheel closes if "Auto-Close on Equip" is on and
   Shift/keep-open was not used; if the slot is still worn the stash silently no-op'd (e.g. no wardrobe chest) and a
   toast says so instead of closing.
3. closeWheel(): resets the flags so nothing leaks into a later, unrelated open.
4. index.html: gamepad hint back to "Equip / Unequip".

Blocks are wrapped in begin/end marker comments so --revert strips them exactly.
Usage: python patch_reselect_unequip.py [--check | --apply | --revert]   (default --check; the game must be closed)
Re-run --check after every Outfit Wheeler update; re-apply if the markers are gone.
"""
import os, sys, hashlib, shutil, subprocess, datetime, re

VIEW = r"C:\1. AUTHORIA\mods\Outfit Wheeler - Dynamic Equipment Manager\PrismaUI\views\PrismaOutfitWheel"
APP = os.path.join(VIEW, "app.js"); INDEX = os.path.join(VIEW, "index.html")
BACKUP_DIR = r"C:\1. AUTHORIA\_backups\2026-09-03 - Outfit Wheeler 3.0 reselect-unequip patch"
B1, E1 = "// >>> Authoria reselect-unequip (begin)", "// <<< Authoria reselect-unequip (end)"
B2, E2 = "// >>> Authoria reselect-unequip playmode (begin)", "// <<< Authoria reselect-unequip playmode (end)"
B3, E3 = "// >>> Authoria reselect-unequip close (begin)", "// <<< Authoria reselect-unequip close (end)"
ANCHOR1 = "    lastEquipCallTimestamp = now;\n"
BLOCK1 = B1 + r"""
    if (!isEditModeActive() && currentWheelData && Array.isArray(currentWheelData.slots)) {
        var awSlot = currentWheelData.slots.find(function (s) { return (s.index !== undefined ? s.index : currentWheelData.slots.indexOf(s)) === slotIndex; }) || currentWheelData.slots[slotIndex];
        if (awSlot && awSlot.hasOutfit && awSlot.isAddon !== true && (awSlot.isEquipped === true || awSlot.isWorn === true)) {
            var awTarget = String(currentWheelData.activeTargetActorId || '0x00000007').toUpperCase();
            var awIsPlayer = (awTarget === '0X00000007' || awTarget === '0X00000014');
            window.__awPlayPending = 0; window.__awPlayUntil = 0; window.__awCloseAfter = false; window.__awSlotIndex = slotIndex;
            if (currentWheelData.autoStashEnabled !== false && typeof window.StashSlotOutfit === 'function') {
                window.__awPlayPending = 1; window.__awPlayUntil = Date.now() + 1500;
                window.__awCloseAfter = (keepOpen !== true && currentWheelData.autoCloseOnEquip !== false);
                window.StashSlotOutfit(JSON.stringify({ wheelIndex: currentWheelData.wheelIndex || 0, slotIndex: slotIndex }));
            } else if (typeof window.ToggleItemEquip === 'function') {
                if (!awIsPlayer) {
                    if (typeof showSaveToast === 'function') showSaveToast("Select the player first");
                    return;
                }
                var awInv = currentWheelData.playerInventory || currentWheelData.inventory || [];
                var awWorn = {};
                awInv.forEach(function (it) { if (it && it.equipped === true && it.rawID) awWorn[it.rawID] = true; });
                var awSeen = {}; var awCount = 0;
                (awSlot.items || []).forEach(function (it) {
                    if (!it || typeof it !== 'object' || !it.rawID) return;
                    if (awSeen[it.rawID]) return;
                    if (awWorn[it.rawID] !== true) return;
                    awSeen[it.rawID] = true;
                    window.ToggleItemEquip(JSON.stringify({ rawID: it.rawID, id: it.id || '' }));
                    awCount++;
                });
                if (awCount === 0) {
                    if (typeof showSaveToast === 'function') showSaveToast("Nothing to unequip");
                    return;
                }
                window.__awPlayPending = awCount; window.__awPlayUntil = Date.now() + 1500;
                window.__awCloseAfter = (keepOpen !== true && currentWheelData.autoCloseOnEquip !== false);
                if (typeof showSaveToast === 'function') showSaveToast("Outfit Unequipped");
            }
            lastEquippedSlotIndex = null;
            if (typeof updateWheelUI === 'function') updateWheelUI();
            return;
        }
    }
""" + E1 + "\n"
ANCHOR2 = ("    if (!currentWheelData || typeof currentWheelData !== 'object') {\n"
           "        currentWheelData = { slots: [], followers: [], inventory: [] };\n"
           "    }\n")
BLOCK2 = B2 + r"""
    if (window.__awPlayPending > 0 && Date.now() < (window.__awPlayUntil || 0)) {
        window.__awPlayPending--;
        currentWheelData.editMode = false;
        if (window.__awPlayPending === 0) {
            var awIdx = window.__awSlotIndex;
            var awS = (Array.isArray(currentWheelData.slots) ? (currentWheelData.slots.find(function (s) { return (s.index !== undefined ? s.index : currentWheelData.slots.indexOf(s)) === awIdx; }) || currentWheelData.slots[awIdx]) : null);
            var awStillWorn = !!(awS && (awS.isWorn === true || awS.isEquipped === true));
            var awClose = window.__awCloseAfter === true;
            window.__awCloseAfter = false; window.__awPlayUntil = 0;
            if (awStillWorn) {
                setTimeout(function () { if (typeof showSaveToast === 'function') showSaveToast("Outfit could not be stored (wardrobe unavailable)"); }, 0);
            } else if (awClose) {
                setTimeout(function () { if (typeof closeWheel === 'function') closeWheel(); }, 60);
            }
        }
    } else if (window.__awPlayPending > 0) {
        window.__awPlayPending = 0; window.__awCloseAfter = false; window.__awPlayUntil = 0;
    }
""" + E2 + "\n"
ANCHOR3 = "function closeWheel() {\n"
BLOCK3 = B3 + r"""
    window.__awPlayPending = 0; window.__awPlayUntil = 0; window.__awCloseAfter = false;
""" + E3 + "\n"
HINT_OLD = '<div class="gp-hint-item"><span class="gp-key">A</span><span>Equip Outfit</span></div>'
HINT_NEW = '<div class="gp-hint-item"><span class="gp-key">A</span><span>Equip / Unequip</span></div>'

def read(p): return open(p, "rb").read()
def strip(a, b, e, eol):
    return re.compile(re.escape(b) + r".*?" + re.escape(e) + eol, re.S).sub("", a)
def main():
    mode = "--apply" if "--apply" in sys.argv else "--revert" if "--revert" in sys.argv else "--check"
    a = read(APP).decode("utf-8"); i = read(INDEX).decode("utf-8"); eol = "\r\n" if "\r\n" in a else "\n"
    anchors = [x.replace("\n", eol) for x in (ANCHOR1, ANCHOR2, ANCHOR3)]
    print(f"app.js {len(a)} chars md5 {hashlib.md5(read(APP)).hexdigest()} | blocks {B1 in a}/{B2 in a}/{B3 in a} | anchors {[a.count(x) for x in anchors]}")
    print(f"index.html hint: {'Equip / Unequip' if HINT_NEW in i else ('Equip Outfit' if HINT_OLD in i else 'neither (layout changed?)')}")
    if mode == "--check": return
    running = subprocess.run(["powershell", "-NoProfile", "-Command",
        "Get-Process SkyrimSE,skse64_loader -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name"],
        capture_output=True, text=True).stdout.strip()
    if running: raise SystemExit("ABORT: running: " + running)
    os.makedirs(BACKUP_DIR, exist_ok=True); stamp = datetime.datetime.now().strftime("%m%d-%H%M%S")
    for p in (APP, INDEX): shutil.copy2(p, os.path.join(BACKUP_DIR, os.path.basename(p) + "." + stamp))
    blocks = [x.replace("\n", eol) for x in (BLOCK1, BLOCK2, BLOCK3)]
    if mode == "--apply":
        if B1 in a or B2 in a or B3 in a: raise SystemExit("already applied (use --revert first)")
        if any(a.count(x) != 1 for x in anchors): raise SystemExit(f"anchor counts {[a.count(x) for x in anchors]} - app.js changed; re-derive the patch")
        for an, bl in zip(anchors, blocks): a = a.replace(an, an + bl, 1)
        if HINT_OLD in i: i = i.replace(HINT_OLD, HINT_NEW, 1)
    else:
        if not (B1 in a or B2 in a or B3 in a): raise SystemExit("not applied")
        for b, e in ((B1, E1), (B2, E2), (B3, E3)): a = strip(a, b, e, eol)
        assert B1 not in a and B2 not in a and B3 not in a
        if HINT_NEW in i: i = i.replace(HINT_NEW, HINT_OLD, 1)
    open(APP, "wb").write(a.encode("utf-8")); open(INDEX, "wb").write(i.encode("utf-8"))
    a3 = read(APP).decode("utf-8")
    print("after: blocks", B1 in a3, B2 in a3, B3 in a3, "| md5", hashlib.md5(read(APP)).hexdigest())

if __name__ == "__main__": main()
