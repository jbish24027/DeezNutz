"""Second pass of the Katari neck cut: the CBBE-topology meshes.

The ground/inventory model and the base CBBE worn meshes carry a 9545-vertex
jacket instead of the 3BA/UBE 12089, so the island-by-size rule is used there
(the collar is 661 v, the two V-yoke straps 276 + 267 v - unique counts in that
shape). Their DressNew shape IS the same 4196-vertex topology as the worn
meshes, with an identical triangle list, so it reuses the exact same drop set.

Backups: *.bak-neckcut-20260828 beside each file. Read-only unless --write.
"""
import os, shutil, sys
sys.path.insert(0, r'C:\1. AUTHORIA\tools\nifcheck')
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\katari-neck')
import trishape_cut as tc
from neckpick import JACKET, DRESS
from apply_cut import build_sets, SUFFIX

M = r"C:\1. AUTHORIA\mods"
SKINNED = [
    r"Fuse00 - Katari Armor - CBBE\Meshes\Fuse00\Armor\Katari\Katari_armor_0.nif",
    r"Fuse00 - Katari Armor - CBBE\Meshes\Fuse00\Armor\Katari\Katari_armor_1.nif",
]
STATIC = [
    r"Katari Armor - Xtudo Tweaks\Meshes\Fuse00\Armor\Katari\Go_Katari_Armor.nif",
    r"Fuse00 - Katari Armor - CBBE\Meshes\Fuse00\Armor\Katari\Go_Katari_Armor.nif",
]
CBBE_ISLAND_SIZES = {661, 276, 267}


def jacket_drop_by_size(comps, tris):
    picked = [c for c in comps if len(c) in CBBE_ISLAND_SIZES]
    assert len(picked) == 3, f"expected 3 jacket islands by size, got {len(picked)}"
    dead = set().union(*[set(c) for c in picked])
    return {i for i, (a, b, c) in enumerate(tris) if a in dead or b in dead or c in dead}


def main(write=False):
    _, dress_set = build_sets()
    print(f"reusing dress drop set: {len(dress_set)} tris\n")
    for rel in SKINNED:
        p = os.path.join(M, rel)
        bak = p + SUFFIX
        _, comps, tris = tc.islands(bak if os.path.exists(bak) else p, JACKET)
        jd = jacket_drop_by_size(comps, tris)
        src = bak if os.path.exists(bak) else p
        if write and not os.path.exists(bak):
            shutil.copy2(p, bak); src = bak
        dst = p if write else os.path.join(os.environ.get('TEMP', '.'), 'k_dry.nif')
        rep = tc.cut(src, dst, {JACKET: jd, DRESS: dress_set})
        print(f"{'WROTE ' if write else 'dry   '}{os.path.basename(p):24s} " +
              "  ".join(f"{n}: {t}->{k}" for n, t, d, k in rep))
    for rel in STATIC:
        p = os.path.join(M, rel)
        bak = p + SUFFIX
        _, comps, tris = tc.static_tris(bak if os.path.exists(bak) else p, JACKET)
        jd = jacket_drop_by_size(comps, tris)
        src = bak if os.path.exists(bak) else p
        if write and not os.path.exists(bak):
            shutil.copy2(p, bak); src = bak
        dst = p if write else os.path.join(os.environ.get('TEMP', '.'), 'k_dry.nif')
        rep = tc.cut_static(src, dst, {JACKET: jd, DRESS: dress_set})
        print(f"{'WROTE ' if write else 'dry   '}{rel.split(chr(92))[0][:26]:26s} {os.path.basename(p):22s} " +
              "  ".join(f"{n}: {t}->{k}" for n, t, d, k in rep))


if __name__ == '__main__':
    main('--write' in sys.argv)
