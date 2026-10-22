"""Insert the new mods/plugins into all 4 MO2 profiles (modlist, plugins, loadorder, plugingroups).
Re-reads every file fresh, writes CRLF without BOM. Idempotent: existing lines for our names are removed first.
Usage: python apply_profiles.py [--dry]
"""
import os, sys, io

INST = r"C:\1. AUTHORIA"
PROFILES = ["DEEZ CS NUTZ", "DEEEZ NUTTZZZ", "Authoria - Requiem Reforged - Main Profile", "Authoria - Requiem Reforged - NSFW Profile"]
DRY = '--dry' in sys.argv

NEW_MODS = [
    "Vel'dun UI - DBVO Dialogue Patch (1.0.5 carry-over)",
    "Spell Hotbar - Option 7 - White (Reskins and Presets)",
    "Spell Hotbar",
    "Authoria - Time Flies - No Spell Tome Time",
    "Time Flies - AE Fishing Patch",
    "Time Flies SE",
    "Kaidan Wig Slot 44 Patch",
]
NEW_PLUGINS = ["SpellHotbar.esp", "TimeFlies.esp", "TF-AEFishing Patch.esp", "Kaidan Wig Slot 44 Patch.esp"]


def read_lines(p):
    with open(p, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8-sig')
    lines = text.split('\r\n') if '\r\n' in text else text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return lines


def write_lines(p, lines):
    if DRY:
        return
    with open(p, 'wb') as f:
        f.write(('\r\n'.join(lines) + '\r\n').encode('utf-8'))


def find_mod(lines, name):
    for i, l in enumerate(lines):
        if l[1:] == name and l[:1] in '+-':
            return i
    return -1


def find_plain(lines, name):
    nl = name.lower()
    for i, l in enumerate(lines):
        if l.lower() == nl or l.lower() == '*' + nl:
            return i
    return -1


def do_profile(prof):
    pdir = os.path.join(INST, 'profiles', prof)
    report = []
    # ---------------- modlist ----------------
    ml_path = os.path.join(pdir, 'modlist.txt')
    ml = read_lines(ml_path)
    removed = [l for l in ml if l[1:] in NEW_MODS]
    ml = [l for l in ml if l[1:] not in NEW_MODS]
    if removed:
        report.append('modlist: removed pre-existing/auto-appended lines: %r' % removed)

    def insert_before(anchor_names, new_names_in_file_order, state_from_anchor=True, force_state=None):
        for a in anchor_names:
            i = find_mod(ml, a)
            if i >= 0:
                st = ml[i][0] if force_state is None else force_state
                for k, n in enumerate(new_names_in_file_order):
                    ml.insert(i + k, st + n)
                report.append('modlist: inserted %r before %r (state %s) at line %d' % (new_names_in_file_order, a, st, i + 1))
                return True
        report.append('!! modlist: NO ANCHOR found among %r for %r' % (anchor_names, new_names_in_file_order))
        return False

    insert_before(["Vel'dun UI"], ["Vel'dun UI - DBVO Dialogue Patch (1.0.5 carry-over)"])
    insert_before(["Wheeler Icon Embellishment - Naturally Exquisite Refinement", "Wheeler - Show in UI", "Wheeler"],
                  ["Spell Hotbar - Option 7 - White (Reskins and Presets)", "Spell Hotbar"])
    insert_before(["Immersive Carcass Carrying - Simple Hunting Overhaul", "SunHelm Survival - Compatibility Patches", "SunHelm Survival and needs"],
                  ["Authoria - Time Flies - No Spell Tome Time", "Time Flies - AE Fishing Patch", "Time Flies SE"])
    kw_enabled = False
    i = find_mod(ml, "houseCARL - Authoria - Vorstag Headpart Races")
    if i >= 0 and ml[i][0] == '+':
        ml.insert(i, "+Kaidan Wig Slot 44 Patch")
        kw_enabled = True
        report.append('modlist: inserted Kaidan Wig Slot 44 Patch (+) before houseCARL - Authoria - Vorstag Headpart Races at line %d' % (i + 1))
    else:
        j = find_mod(ml, "Authoria - Kaidan Visual Replacer")
        if j >= 0:
            ml.insert(j, "-Kaidan Wig Slot 44 Patch")
            report.append('modlist: anchor Vorstag Headpart Races disabled/absent -> inserted Kaidan Wig Slot 44 Patch (-) before Authoria - Kaidan Visual Replacer at line %d' % (j + 1))
        else:
            report.append('!! modlist: no anchor for Kaidan Wig Slot 44 Patch')
    write_lines(ml_path, ml)

    # which new mods ended up enabled in this profile
    enabled = {n: (ml[find_mod(ml, n)][0] == '+') for n in NEW_MODS if find_mod(ml, n) >= 0}
    report.append('modlist: enabled states: %s' % enabled)

    # ---------------- plugins / loadorder ----------------
    lo_path = os.path.join(pdir, 'loadorder.txt')
    pl_path = os.path.join(pdir, 'plugins.txt')
    lo = read_lines(lo_path)
    pl = read_lines(pl_path)
    lo = [l for l in lo if l.lower() not in [n.lower() for n in NEW_PLUGINS]]
    pl = [l for l in pl if l.lstrip('*').lower() not in [n.lower() for n in NEW_PLUGINS]]

    def insert_plugin_after(anchor_names, new_name):
        for a in anchor_names:
            i = find_plain(lo, a)
            j = find_plain(pl, a)
            if i >= 0:
                lo.insert(i + 1, new_name)
                if j >= 0:
                    pl.insert(j + 1, '*' + new_name)
                else:
                    pl.append('*' + new_name)
                    report.append('!! plugins.txt: anchor %r not found for %r; appended at end' % (a, new_name))
                report.append('loadorder: %r after %r (idx %d)' % (new_name, a, i + 1))
                return True
        report.append('!! loadorder: NO ANCHOR for %r among %r' % (new_name, anchor_names))
        return False

    added_plugins = []
    if enabled.get("Spell Hotbar"):
        if insert_plugin_after(["Wheeler - UI.esp"], "SpellHotbar.esp"):
            added_plugins.append(("SpellHotbar.esp", "Interface - User Interface"))
    if enabled.get("Time Flies SE"):
        if insert_plugin_after(["Wounds Overlays Applied.esp", "Wounds.esp", "Simple Hunting Overhaul.esp"], "TimeFlies.esp"):
            added_plugins.append(("TimeFlies.esp", "Gameplay - Early Loaders"))
            if enabled.get("Time Flies - AE Fishing Patch"):
                if insert_plugin_after(["TimeFlies.esp"], "TF-AEFishing Patch.esp"):
                    added_plugins.append(("TF-AEFishing Patch.esp", "Gameplay - Early Loaders"))
    if enabled.get("Kaidan Wig Slot 44 Patch"):
        if insert_plugin_after(["Authoria - Vorstag Headpart Races.esp"], "Kaidan Wig Slot 44 Patch.esp"):
            added_plugins.append(("Kaidan Wig Slot 44 Patch.esp", None))  # group resolved below
    write_lines(lo_path, lo)
    write_lines(pl_path, pl)

    # ---------------- plugingroups ----------------
    pg_path = os.path.join(pdir, 'plugingroups.txt')
    pg = read_lines(pg_path)
    header = [l for l in pg if l.startswith('#')]
    body = [l for l in pg if not l.startswith('#') and l.strip()]
    groups = {}
    for l in body:
        if '|' in l:
            n, g = l.split('|', 1)
            groups[n.lower()] = g
    body = [l for l in body if l.split('|', 1)[0].lower() not in [n.lower() for n in NEW_PLUGINS]]
    for name, grp in added_plugins:
        if grp is None:
            grp = groups.get("authoria - vorstag headpart races.esp", "Authoria - Master Patches")
        entry = '%s|%s' % (name, grp)
        # insert after the last body line whose name sorts before ours (ordinal, case-insensitive)
        pos = 0
        for k, l in enumerate(body):
            if l.split('|', 1)[0].lower() < name.lower():
                pos = k + 1
        body.insert(pos, entry)
        report.append('plugingroups: %s' % entry)
    write_lines(pg_path, header + body)
    return report


if __name__ == '__main__':
    for prof in PROFILES:
        print('=====', prof, '=====')
        for r in do_profile(prof):
            print('  ', r)
    print('DRY RUN - nothing written' if DRY else 'WRITTEN')
