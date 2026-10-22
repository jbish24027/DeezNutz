"""Outfit Wheeler 3.0.0 - switch the DLL's auto system OFF (context tracking, active-slot bookkeeping, event-driven auto-stash).

Why a patch: the master flag (`autoSystemEnabled`) has NO INI key in 3.0.0 and NO checkbox in the Settings panel. Its
built-in default is 1 (.data byte, file offset 0xDAE1A) and the panel's save routine re-sends `true` because the
checkbox element does not exist. The bAutoCity/bAutoHome/bAutoSwim INI keys are parsed but never read by any logic.

What the patch does:
  1. DLL: file offset 0xDAE1A  01 -> 00   (static default of the master flag; the evaluator at 0x2AC20 and the context
     function at 0x2C020 both exit at once when it is 0)
  2. modals.js: `const autoSystemVal = chkAutoSystem ? chkAutoSystem.checked : true;` -> `: false` so a Settings save
     cannot flip the flag back on for the session.

Usage: python patch_autosystem.py --check | --apply | --revert
Re-check on every Outfit Wheeler update: a new build moves the offset (search the INI loader for the 6 `setne` stores
into consecutive .data bytes; the master flag is the one that has no INI-key string reference).
"""
import hashlib, os, shutil, sys, datetime

MOD = r"C:\1. AUTHORIA\mods\Outfit Wheeler - Dynamic Equipment Manager"
DLL = os.path.join(MOD, r"SKSE\Plugins\OutfitWheeler-DynamicEquipmentManager.dll")
JS = os.path.join(MOD, r"PrismaUI\views\PrismaOutfitWheel\modals.js")
BACKUP_ROOT = r"C:\1. AUTHORIA\_backups"
BACKUP_DIR = os.path.join(BACKUP_ROOT, "2026-09-05 - Outfit Wheeler auto system off")

OFFSET = 0xDAE1A                       # autoSystemEnabled static default (3.0.0, forceequip-patched build)
SIGNATURE_OFF = 0xDAE18                # 7 flag bytes: autoClose, autoStash, MASTER, city, home, combat, swim
KNOWN_ORIG_MD5 = {"e3dedd079dc3b7785dd25cae263c3410"}   # 3.0.0 + forceequip patch, master ON

JS_OLD = "    const autoSystemVal = chkAutoSystem ? chkAutoSystem.checked : true;"
JS_NEW = ("    const autoSystemVal = chkAutoSystem ? chkAutoSystem.checked : false;"
          " // Authoria patch: auto system stays off (no checkbox exists; true would re-enable it)")


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def state():
    d = open(DLL, 'rb').read()
    sig = d[SIGNATURE_OFF:SIGNATURE_OFF + 7]
    js = open(JS, 'rb').read()
    js_state = 'patched' if JS_NEW.encode() in js else ('original' if JS_OLD.encode() in js else 'UNKNOWN')
    return d, sig, js, js_state


def check():
    d, sig, js, js_state = state()
    print(f"DLL md5 {md5(DLL)} | flag bytes @0x{SIGNATURE_OFF:X}: {sig.hex(' ')} | master @0x{OFFSET:X} = {d[OFFSET]}"
          f" -> auto system {'OFF' if d[OFFSET] == 0 else 'ON'}")
    print(f"modals.js: {js_state} | CRLF: {b'\\r\\n' in js}")
    ok_sig = all(b in (0, 1) for b in sig) and sig[0] == 1
    if not ok_sig:
        print("WARNING: flag-byte signature does not look like 3.0.0 - re-locate the offset before applying")
    return d, js, js_state, ok_sig


def apply():
    d, js, js_state, ok_sig = check()
    if md5(DLL) not in KNOWN_ORIG_MD5 and d[OFFSET] != 0:
        if not ok_sig:
            sys.exit("refusing: unknown build")
        print("note: DLL md5 not in the known list, signature still matches - continuing")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for src in (DLL, JS):
        dst = os.path.join(BACKUP_DIR, os.path.basename(src))
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    if d[OFFSET] != 0:
        nd = bytearray(d); nd[OFFSET] = 0
        open(DLL, 'wb').write(nd)
    if js_state == 'original':
        open(JS, 'wb').write(js.replace(JS_OLD.encode(), JS_NEW.encode(), 1))
    print("applied; backups in", BACKUP_DIR)
    check()


def revert():
    d, js, js_state, ok_sig = check()
    if d[OFFSET] == 0:
        nd = bytearray(d); nd[OFFSET] = 1
        open(DLL, 'wb').write(nd)
    if js_state == 'patched':
        open(JS, 'wb').write(js.replace(JS_NEW.encode(), JS_OLD.encode(), 1))
    print("reverted")
    check()


if __name__ == '__main__':
    a = sys.argv[1] if len(sys.argv) > 1 else '--check'
    {'--check': check, '--apply': apply, '--revert': revert}[a]()
