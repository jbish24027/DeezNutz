"""Add always-keep items to Outfit Wheeler's saved outfits.

Outfit Wheeler strips every worn armor/clothing piece that is not in the outfit
it is about to equip (only slot-39 shield items are exempt), and with
bAutoStashInactive=1 it also moves each stripped piece into the wardrobe chest.
An item that IS in the target outfit's list is skipped by both loops, so the
fix for "keep my backpack / jewellery on" is to put those items into every
saved outfit.

*** rawID is the ONLY field that works. ***
The DLL reads plugin + localID first, but that path is broken: it resolves the
form and then keeps it only if formType == 0 (a LookupForm<TESForm> footgun -
TESForm::FORMTYPE is FormType::None). Real armor has formType 0x1A, so the
check always fails and it falls through to the rawID branch. An entry with
rawID 0 is silently dropped at load. So every entry MUST carry the correct
RUNTIME FormID, which this script computes from the live load order:

    regular plugin:  (loadIndex << 24) | localID
    light plugin:    0xFE000000 | (eslIndex << 12) | (localID & 0xFFF)

The index model is calibrated against the rawIDs the mod wrote itself; run
--calibrate to re-check it after any load-order change.

Usage:
    python add_keepers.py --list
    python add_keepers.py --calibrate
    python add_keepers.py --add "Plugin.esp|0x81E" --only "casual dress" --apply
    python add_keepers.py --repair --apply      # fill in any rawID 0 entries
    python add_keepers.py --remove "Plugin.esp|0x81E" --apply

Nothing is written without --apply; MO2 must be closed and the game not running.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import struct
import sys

ROOT = "C:/1. AUTHORIA"


def _active_profile():
    """The profile MO2 currently has selected.

    This used to be hard-coded to "DEEZ CS NUTZ". On 2026-08-30 the selected
    profile was "DEEZ CS NUTZ - PBR", which carries 10 more active plugins, so
    every rawID this script wrote was computed against the WRONG load order.
    The wheel then re-resolved them on launch and rewrote the file to garbage.
    Never hard-code the profile again.
    """
    ini = os.path.join(ROOT, "ModOrganizer.ini")
    with open(ini, encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            if line.strip().startswith("selected_profile"):
                name = line.split("=", 1)[1].strip()
                m = re.match(r"@ByteArray\((.*)\)\s*$", name)
                if m:
                    name = m.group(1)
                path = os.path.join(ROOT, "profiles", name)
                if not os.path.isdir(path):
                    sys.exit("selected profile %r not found under profiles/" % name)
                return path
    sys.exit("no selected_profile in %s" % ini)


PROFILE = _active_profile()
DATA = ROOT + "/overwrite/SKSE/Plugins/PrismaOutfitWheel.json"
BACKUPS = ROOT + "/_backups"
KNOWN_GOOD = os.path.dirname(os.path.abspath(__file__)) + "/outfits.known-good.json"


# --------------------------------------------------------------------------
# runtime FormID resolution
# --------------------------------------------------------------------------

def _plugin_files():
    """plugin filename (lower) -> path of the mod that wins the VFS."""
    found = {}
    modlist = os.path.join(PROFILE, "modlist.txt")
    with open(modlist, encoding="utf-8-sig", errors="replace") as fh:
        mods = [ln.rstrip("\r\n")[1:] for ln in fh if ln.startswith("+")]
    for mod in mods:                      # modlist.txt is highest-priority first
        folder = os.path.join(ROOT, "mods", mod)
        try:
            names = os.listdir(folder)
        except OSError:
            continue
        for name in names:
            low = name.lower()
            if low.endswith((".esp", ".esm", ".esl")) and low not in found:
                found[low] = os.path.join(folder, name)
    stock = os.path.join(ROOT, "Stock Game", "Data")
    if os.path.isdir(stock):
        for name in os.listdir(stock):
            low = name.lower()
            if low.endswith((".esp", ".esm", ".esl")) and low not in found:
                found[low] = os.path.join(stock, name)
    return found


def _is_light(path, name):
    if name.lower().endswith(".esl"):
        return True
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
    except OSError:
        return False
    if head[:4] != b"TES4":
        return False
    return bool(struct.unpack_from("<I", head, 8)[0] & 0x200)


_INDEX = None


def load_indices():
    """plugin filename (lower) -> ('FULL'|'ESL', index) in live load order.

    A plugin listed in plugins.txt WITHOUT an asterisk is inactive and skipped.
    A plugin absent from plugins.txt entirely is an implicit master (the vanilla
    masters and the CC content) - those DO load and DO consume indices.
    """
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    active, listed = set(), set()
    with open(os.path.join(PROFILE, "plugins.txt"),
              encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("*"):
                active.add(line[1:].lower())
                listed.add(line[1:].lower())
            else:
                listed.add(line.lower())
    with open(os.path.join(PROFILE, "loadorder.txt"),
              encoding="utf-8-sig", errors="replace") as fh:
        order = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

    files = _plugin_files()
    full = light = 0
    idx = {}
    for name in order:
        low = name.lower()
        if low in listed and low not in active:
            continue
        path = files.get(low)
        if path is None:
            continue
        if _is_light(path, name):
            idx[low] = ("ESL", light)
            light += 1
        else:
            idx[low] = ("FULL", full)
            full += 1
    _INDEX = idx
    return idx


def runtime_formid(plugin, local):
    kind_index = load_indices().get(plugin.lower())
    if kind_index is None:
        sys.exit("plugin not active in this profile: %s" % plugin)
    kind, index = kind_index
    if kind == "ESL":
        return 0xFE000000 | ((index & 0xFFF) << 12) | (local & 0xFFF)
    return ((index & 0xFF) << 24) | (local & 0xFFFFFF)


def wheels(doc):
    """The wheel list in BOTH file shapes.

    2.x wrote {"wheels": [...]} at the top level. Outfit Wheeler 3.0 (first launch
    2026-09-03/04) rewrote the file as {"activeTargetActorID": N, "actors": {"0x…":
    {"formMeta": …, "profile": {"wheels": [...]}}}, "wardrobeContainerFormID": 0}.
    Every actor's wheels are concatenated in file order (one actor so far, the
    player 0x00000007), so wheel/slot indices in snapshots stay stable while
    there is a single actor. Items still carry plugin + localID + rawID, and 3.0
    resolves plugin+localID FIRST (rawID is the fallback), so a reindex here
    keeps the fallback consistent rather than being the only thing that saves you.
    """
    if "wheels" in doc:
        return wheels(doc)
    actors = doc.get("actors")
    if isinstance(actors, dict) and actors:
        out = []
        for actor in actors.values():
            out.extend(actor["profile"]["wheels"])
        return out
    sys.exit("unrecognised wheel JSON shape - top-level keys: %s" % list(doc))


def calibrate(doc):
    """Re-derive every plugin index from the rawIDs the mod wrote itself."""
    ok = bad = 0
    for wheel in wheels(doc):
        for slot in wheel["slots"]:
            for item in slot["items"]:
                if not item["rawID"]:
                    continue
                mine = runtime_formid(item["plugin"], int(item["localID"], 16))
                if mine == item["rawID"]:
                    ok += 1
                else:
                    bad += 1
                    print("MISMATCH %-45s theirs 0x%08X mine 0x%08X"
                          % (item["plugin"], item["rawID"], mine))
    print("calibration: %d match, %d mismatch" % (ok, bad))
    return bad == 0


# --------------------------------------------------------------------------

def reindex(doc):
    """Recompute EVERY rawID from plugin + localID against the live load order.

    rawID is a runtime FormID, so adding, removing or disabling ANY plugin
    invalidates every stored one. Worse, the DLL then re-resolves the stale
    rawID against the new order, finds whatever mod now sits at that index,
    and REWRITES the entry's plugin name to match - so after one game launch
    the plugin+localID pair is corrupt too and this cannot recover it.
    Run this BEFORE launching, every time the plugin list changes.
    """
    changed = same = 0
    for wname, i, slot in filled(doc):
        for item in slot["items"]:
            want = runtime_formid(item["plugin"], int(item["localID"], 16))
            if want == item["rawID"]:
                same += 1
                continue
            print("reindex %-20s %-45s %s  0x%08X -> 0x%08X"
                  % (slot["name"], item["plugin"], item["localID"],
                     item["rawID"], want))
            item["rawID"] = want
            changed += 1
    print("reindex: %d unchanged, %d rewritten" % (same, changed))
    return changed


def stale(doc):
    """Entries whose stored rawID does not match the live load order."""
    out = []
    for wname, i, slot in filled(doc):
        for item in slot["items"]:
            if runtime_formid(item["plugin"], int(item["localID"], 16)) != item["rawID"]:
                out.append((slot["name"], item))
    return out


def snapshot(doc):
    """Save outfit contents as plugin + localID only - no runtime FormIDs.

    This is the load-order-independent record of what each outfit contains,
    and the only thing that survives a load-order change intact.
    """
    data = {"outfits": []}
    for wi, wheel in enumerate(wheels(doc)):
        for si, slot in enumerate(wheel["slots"]):
            if not slot.get("hasOutfit"):
                continue
            data["outfits"].append({
                "wheel": wi, "slot": si, "name": slot["name"],
                "items": [{"plugin": it["plugin"], "localID": it["localID"]}
                          for it in slot["items"]],
            })
    with open(KNOWN_GOOD, "w", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(data, indent=1, ensure_ascii=False))
    total = sum(len(o["items"]) for o in data["outfits"])
    print("snapshot: %d outfits, %d items -> %s"
          % (len(data["outfits"]), total, KNOWN_GOOD))


def restore(doc, source):
    """Rebuild every outfit's item list from a snapshot or an old wheel JSON."""
    with open(source, encoding="utf-8-sig") as fh:
        src = json.load(fh)
    if "outfits" in src:
        outfits = {(o["wheel"], o["slot"]): o for o in src["outfits"]}
    else:                                   # an old PrismaOutfitWheel.json
        outfits = {}
        for wi, wheel in enumerate(wheels(src)):
            for si, slot in enumerate(wheel["slots"]):
                if slot.get("hasOutfit"):
                    outfits[(wi, si)] = {"name": slot["name"], "items": slot["items"]}
    hit = 0
    for wi, wheel in enumerate(wheels(doc)):
        for si, slot in enumerate(wheel["slots"]):
            want = outfits.get((wi, si))
            if want is None:
                continue
            if want["name"] != slot["name"]:
                sys.exit("slot %d/%d is %r here but %r in the source - refusing"
                         % (wi, si, slot["name"], want["name"]))
            slot["items"] = [{"localID": it["localID"], "plugin": it["plugin"],
                              "rawID": runtime_formid(it["plugin"],
                                                      int(it["localID"], 16))}
                             for it in want["items"]]
            slot["hasOutfit"] = True
            print("restored %-20s %d pieces" % (slot["name"], len(slot["items"])))
            hit += 1
    print("restore: %d outfits from %s" % (hit, os.path.basename(source)))


def parse_token(tok):
    plugin, _, local = tok.partition("|")
    plugin, local = plugin.strip(), local.strip()
    if not plugin or not local:
        sys.exit('bad item token %r - want "Plugin.esp|0x81E"' % tok)
    return plugin, "0x%08X" % int(local, 16)


def load():
    with open(DATA, encoding="utf-8-sig") as fh:
        return json.load(fh)


def save(doc):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(DATA, os.path.join(BACKUPS, "PrismaOutfitWheel.json.bak-%s" % stamp))
    with open(DATA, "w", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(doc, separators=(",", ":"), ensure_ascii=False))


def filled(doc):
    for wheel in wheels(doc):
        for i, slot in enumerate(wheel["slots"]):
            if slot.get("hasOutfit"):
                yield wheel["name"], i, slot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", action="append", default=[])
    ap.add_argument("--remove", action="append", default=[])
    ap.add_argument("--only", default="")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--repair", action="store_true")
    ap.add_argument("--reindex", action="store_true")
    ap.add_argument("--snapshot", action="store_true")
    ap.add_argument("--restore", nargs="?", const=KNOWN_GOOD, default=None)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    doc = load()

    if a.calibrate:
        calibrate(doc)
        bad = stale(doc)
        if bad:
            print("\n%d entries are STALE - the load order moved under them." % len(bad))
            print("run --reindex --apply BEFORE launching the game.")
        return

    if a.snapshot:
        snapshot(doc)
        return

    if a.restore:
        restore(doc, a.restore)

    if a.reindex:
        reindex(doc)

    if a.list:
        for wname, i, slot in filled(doc):
            print("%-8s [%d] %-20s %d pieces" % (wname, i, slot["name"], len(slot["items"])))
            for item in slot["items"]:
                print("        %-45s %s  raw 0x%08X%s"
                      % (item["plugin"], item["localID"], item["rawID"],
                         "   <-- DEAD, will be dropped" if not item["rawID"] else ""))
        return

    if a.repair:
        fixed = 0
        for wname, i, slot in filled(doc):
            for item in slot["items"]:
                if item["rawID"]:
                    continue
                item["rawID"] = runtime_formid(item["plugin"], int(item["localID"], 16))
                fixed += 1
                print("fixed %-20s %-45s %s -> 0x%08X"
                      % (slot["name"], item["plugin"], item["localID"], item["rawID"]))
        print("%d entries repaired" % fixed)

    want = [x.strip().lower() for x in a.only.split(",") if x.strip()]
    adds = [parse_token(t) for t in a.add]
    dels = [parse_token(t) for t in a.remove]

    for wname, i, slot in filled(doc):
        if want and slot["name"].strip().lower() not in want:
            continue
        have = {(it["plugin"], it["localID"]) for it in slot["items"]}
        for plugin, local in dels:
            if (plugin, local) in have:
                slot["items"] = [it for it in slot["items"]
                                 if (it["plugin"], it["localID"]) != (plugin, local)]
                print("- %-20s %s %s" % (slot["name"], plugin, local))
        for plugin, local in adds:
            if (plugin, local) in have:
                print("= %-20s %s %s (already there)" % (slot["name"], plugin, local))
                continue
            raw = runtime_formid(plugin, int(local, 16))
            slot["items"].append({"localID": local, "plugin": plugin, "rawID": raw})
            print("+ %-20s %s %s  raw 0x%08X" % (slot["name"], plugin, local, raw))

    if a.apply:
        save(doc)
        print("written:", DATA)
    else:
        print("\ndry run - nothing written (pass --apply)")


if __name__ == "__main__":
    main()
