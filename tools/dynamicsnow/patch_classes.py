#!/usr/bin/env python3
"""DynamicSnow.dll class patch: make the sand and mud surface classes count as "other".

Why: the mod rates each landscape quad (quarter cell) by the highest class found in ANY of its
paint layers, and its rebuild loop carves every vertex of a snow/sand/mud-rated quad. A river-mud
strip rates the whole quarter cell "mud", so dirt trails and rock beside it carve at 65% depth.
With sand and mud neutralised, only quads holding a snow texture carve (quads rated 0 are skipped).

Sites (DynamicShader-DynamicSnow v2, file 796201, sha256 5b70248b...b7b56a, 903,680 bytes):
  RVA 0x28156  file 0x27556  bb 02 00 00 00  mov ebx,2  (sand)  -> bb 00 00 00 00
  RVA 0x28161  file 0x27561  bb 03 00 00 00  mov ebx,3  (mud)   -> bb 00 00 00 00

Usage:
  python patch_classes.py --check    report original / patched / unknown
  python patch_classes.py --apply    patch (writes DynamicSnow.dll.bak-pre-classpatch-YYYYMMDD first)
  python patch_classes.py --revert   restore the original bytes in place
Run with MO2 closed and the game not running (the DLL is locked while the game is up).
"""
import hashlib, sys, os, datetime

DLL = r"C:\1. AUTHORIA\mods\DynamicShader-DynamicSnow\SKSE\Plugins\DynamicSnow.dll"
ORIG_SHA256 = "5b70248b08055aa8d9b1b1a07b8faaf0fa87ae4c5a9a9874354e4285b2b7b56a"
ORIG_SIZE = 903680
SITES = [
    (0x27556, b"\xbb\x02\x00\x00\x00", b"\xbb\x00\x00\x00\x00", "sand class -> other"),
    (0x27561, b"\xbb\x03\x00\x00\x00", b"\xbb\x00\x00\x00\x00", "mud class -> other"),
]


def state(data):
    if len(data) != ORIG_SIZE:
        return "unknown (size %d, expected %d)" % (len(data), ORIG_SIZE)
    orig = all(data[o:o + 5] == a for o, a, b, _ in SITES)
    patched = all(data[o:o + 5] == b for o, a, b, _ in SITES)
    if orig:
        return "original" if hashlib.sha256(data).hexdigest() == ORIG_SHA256 else "original bytes at sites, but hash differs (other build?)"
    if patched:
        return "patched"
    return "unknown (bytes at sites: %s)" % ", ".join(data[o:o + 5].hex() for o, *_ in SITES)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    data = bytearray(open(DLL, "rb").read())
    st = state(data)
    print("DynamicSnow.dll:", st)
    print("sha256:", hashlib.sha256(data).hexdigest())
    if mode == "--check":
        return 0
    if mode == "--apply":
        if st != "original":
            print("refusing to apply: file is not the known original")
            return 1
        bak = DLL + ".bak-pre-classpatch-" + datetime.date.today().strftime("%Y%m%d")
        if not os.path.exists(bak):
            open(bak, "wb").write(data)
            print("backup written:", bak)
        for o, a, b, label in SITES:
            data[o:o + 5] = b
            print("patched %s at 0x%x" % (label, o))
    elif mode == "--revert":
        if st != "patched":
            print("refusing to revert: file is not in the patched state")
            return 1
        for o, a, b, label in SITES:
            data[o:o + 5] = a
            print("restored %s at 0x%x" % (label, o))
    else:
        print(__doc__)
        return 1
    open(DLL, "wb").write(data)
    print("now:", state(bytes(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
