#!/usr/bin/env python3
r"""MFO 1.1.4 -- make HealExcludedWeapon creature-only (stop stripping signature weapons).

THE BUG (marth Follower Overhaul 1.1.4, native/Logistics.cpp HealExcludedWeapon, called
from ServiceFollower every 5 s per follower, BEFORE the bLogistics gate):

    if (!bad || (!Catalog::IsExcluded(bad->GetFormID()) && !IsCreatureWeapon(bad))) continue;
    ... swap the wielded weapon for the best carried playable one, then
    RemoveItem(bad, kStoreInContainer, player)  -> "[heal] ... returned-to-player"

Catalog::IsExcluded is true for EVERY quest/unique weapon in mfo_items.json -- i.e. every
custom follower's signature weapon (Kaidan's Nodachi why=quest, Crucible's Tear why=unique).
The heal was written for invisible CREATURE weapons MFO had wrongly looted; the IsExcluded
half strips legitimate signature gear out of followers' hands and dumps it on the player.
IsStockGear (#69) exempts shed/economy but was never applied to the heal. Unchanged
upstream v1.1.3 -> HEAD (2026-09-06).

THE PATCH: two bytes. In the guard,

    9F398  e8 e3 ac 03 00      call  Catalog::IsExcluded
    9F39D  84 c0               test  al, al
    9F39F  75 18               jne   heal          <-- NOP NOP
    9F3A1  48 8b ce            mov   rcx, rsi
    9F3A4  e8 77 39 01 00      call  IsCreatureWeapon
    9F3A9  84 c0               test  al, al
    9F3AB  75 0c               jne   heal

so an excluded-but-playable weapon falls through to the creature test and is left alone;
a creature weapon still heals exactly as before. No other instruction changes. Nothing
jumps onto 9F39F/9F3A0 (only 9F3AD is a landing pad) and .reloc has no entry there.

Identity is pinned to the upstream CI artifact: releases/v1.1.4/MANIFEST.txt in the
marthofdoom/MFO repo lists dll sha256 286e2452... -- this script refuses anything else.
After ANY MFO update: run --check; a new version needs the offsets re-derived
(_tools\mfo-heal-patch\README.md has the method), never blind-applied.

usage: patch_heal.py --check | --apply | --revert   [--dll PATH]
"""
import argparse, hashlib, os, shutil, subprocess, sys, time

DEFAULT_DLL = r'C:\1. AUTHORIA\mods\marth Follower Overhaul\SKSE\Plugins\MFO.dll'
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup')

VERSION = '1.1.4'
SIZE = 2089472
SHA_STOCK = '286e245233785df4755f4b657865a05930d26e1f5690e04f5eebe03211e368f3'
OFF = 0x9E79F                     # file offset of the jne (RVA 0x9F39F, .text raw 0x400 / va 0x1000)
STOCK_BYTES = bytes.fromhex('7518')
PATCH_BYTES = bytes.fromhex('9090')
CTX_OFF = OFF - 16
# -16..+16 around the site, with the two patch bytes wildcarded (None)
CTX = [0xf0, 0x48, 0x85, 0xf6, 0x74, 0x18, 0x8b, 0x4e, 0x14, 0xe8, 0xe3, 0xac, 0x03, 0x00, 0x84, 0xc0,
       None, None,
       0x48, 0x8b, 0xce, 0xe8, 0x77, 0x39, 0x01, 0x00, 0x84, 0xc0, 0x75, 0x0c, 0xff, 0xc3]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def patched_sha():
    # computed, not hard-coded: stock bytes with the two-byte swap
    return None  # filled at runtime from the real stock file when available


def ctx_ok(d):
    if len(d) < CTX_OFF + len(CTX):
        return False
    for i, want in enumerate(CTX):
        if want is not None and d[CTX_OFF + i] != want:
            return False
    return True


def state(d):
    """'stock' | 'patched' | 'unknown'"""
    if len(d) != SIZE or not ctx_ok(d):
        return 'unknown'
    site = d[OFF:OFF + 2]
    if site == STOCK_BYTES:
        return 'stock' if sha256(d) == SHA_STOCK else 'unknown'
    if site == PATCH_BYTES:
        # patched file must hash to stock once the two bytes are put back
        back = bytearray(d)
        back[OFF:OFF + 2] = STOCK_BYTES
        return 'patched' if sha256(bytes(back)) == SHA_STOCK else 'unknown'
    return 'unknown'


def running(names=('SkyrimSE.exe', 'ModOrganizer.exe')):
    try:
        out = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return []
    return [n for n in names if n.lower() in out.lower()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true')
    g.add_argument('--apply', action='store_true')
    g.add_argument('--revert', action='store_true')
    ap.add_argument('--dll', default=DEFAULT_DLL)
    a = ap.parse_args()

    d = open(a.dll, 'rb').read()
    st = state(d)
    print('MFO.dll  size=%d  sha256=%s' % (len(d), sha256(d)))
    print('state: %s  (expects upstream %s, dll sha %s...)' % (st.upper(), VERSION, SHA_STOCK[:12]))
    if st == 'unknown':
        print('REFUSING: this is not the byte-identical upstream %s build this patch was derived for.' % VERSION)
        print('          Re-derive the HealExcludedWeapon guard offset for this build first (see README.md).')
        return 2 if not a.check else 1
    if a.check:
        if st == 'stock':
            print('Heal is STOCK: excluded (quest/unique) weapons WILL be stripped from followers. Run --apply.')
            return 1
        print('Heal is PATCHED (creature-only). OK.')
        return 0

    busy = running()
    if busy:
        print('REFUSING: %s running -- close it first.' % ', '.join(busy))
        return 3

    if a.apply:
        if st == 'patched':
            print('Already patched. Nothing to do.')
            return 0
        os.makedirs(BACKUP_DIR, exist_ok=True)
        bk = os.path.join(BACKUP_DIR, 'MFO.dll.stock-v%s.%s' % (VERSION, time.strftime('%Y%m%d-%H%M%S')))
        shutil.copy2(a.dll, bk)
        new = bytearray(d)
        new[OFF:OFF + 2] = PATCH_BYTES
        new = bytes(new)
        assert state(new) == 'patched'
        tmp = a.dll + '.tmp'
        open(tmp, 'wb').write(new)
        os.replace(tmp, a.dll)
        print('APPLIED: %04X-%04X %s -> %s' % (OFF, OFF + 1, STOCK_BYTES.hex(), PATCH_BYTES.hex()))
        print('backup:  %s' % bk)
        print('sha256 now %s' % sha256(new))
        return 0

    if a.revert:
        if st == 'stock':
            print('Already stock. Nothing to do.')
            return 0
        new = bytearray(d)
        new[OFF:OFF + 2] = STOCK_BYTES
        new = bytes(new)
        assert sha256(new) == SHA_STOCK
        tmp = a.dll + '.tmp'
        open(tmp, 'wb').write(new)
        os.replace(tmp, a.dll)
        print('REVERTED to stock (sha256 %s)' % SHA_STOCK)
        return 0


if __name__ == '__main__':
    sys.exit(main())
