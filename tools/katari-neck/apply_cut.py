"""Apply the Katari neck cut to every mesh that shares Fuse00's 12089/4196 topology.

ONE triangle set is used for all of them. That matters: _0 and _1 are morph
targets for the same index buffer, so if their triangle lists differ the shape
breaks. The dress set is the UNION of the per-file z=110 picks across all four
world meshes, which is >= each individual pick, so nothing at the neck survives
in any of them.

Backups land beside each mesh as *.bak-neckcut-20260828.
Read-only unless --write is passed.
"""
import os, shutil, sys
sys.path.insert(0, r'C:\1. AUTHORIA\tools\nifcheck')
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\katari-neck')
import trishape_cut as tc
from neckpick import jacket_drop, dress_drop, JACKET, DRESS

M = r"C:\1. AUTHORIA\mods"
SUFFIX = ".bak-neckcut-20260828"

TARGETS = [
    r"Fuse00 - Katari Armor 3BA\meshes\Fuse00\Armor\Katari\Katari_armor_0.nif",
    r"Fuse00 - Katari Armor 3BA\meshes\Fuse00\Armor\Katari\Katari_armor_1.nif",
    r"Fuse00 - Katari Armor 3BA\CalienteTools\BodySlide\ShapeData\Fuse00 - Katari Dress\Fuse00 - Katari Dress.nif",
    r"Fuse00 - Katari Armor 3BA\CalienteTools\BodySlide\ShapeData\Fuse00 - Katari Dress (relaxed)\Fuse00 - Katari Dress (relaxed).nif",
    r"Fuse00 - Katari Armor UBE\meshes\!UBE\Fuse00\Armor\Katari\Katari_armor_0.nif",
    r"Fuse00 - Katari Armor UBE\meshes\!UBE\Fuse00\Armor\Katari\Katari_armor_1.nif",
    r"Fuse00 - Katari Armor UBE\CalienteTools\BodySlide\ShapeData\[UBE] Fuse00 - Katari Dress\[UBE] Fuse00 - Katari Dress.nif",
    r"Fuse00 - Katari Armor UBE\CalienteTools\BodySlide\ShapeData\[UBE] Fuse00 - Katari Dress (relaxed)\[UBE] Fuse00 - Katari Dress (relaxed).nif",
]


def build_sets():
    """Union of the per-file picks. Always reads the pre-cut backup when one
    exists, so re-running after a cut still derives the same sets."""
    jac, dre = set(), set()
    for rel in TARGETS:
        p = os.path.join(M, rel)
        if os.path.exists(p + SUFFIX):
            p = p + SUFFIX
        j, _ = jacket_drop(p)
        d, _ = dress_drop(p)
        jac |= j
        dre |= d
    return jac, dre


def main(write=False):
    jac, dre = build_sets()
    print(f"unified drop sets: jacket {len(jac)} tris, dress {len(dre)} tris\n")
    for rel in TARGETS:
        p = os.path.join(M, rel)
        bak = p + SUFFIX
        if write:
            if not os.path.exists(bak):
                shutil.copy2(p, bak)
            rep = tc.cut(bak if os.path.exists(bak) else p, p,
                         {JACKET: jac, DRESS: dre})
        else:
            rep = tc.cut(p, os.path.join(os.environ.get('TEMP', '.'), 'katari_dry.nif'),
                         {JACKET: jac, DRESS: dre})
        line = "  ".join(f"{n}: {t}->{k}" for n, t, d, k in rep)
        print(f"{'WROTE ' if write else 'dry   '}{rel.split(chr(92))[0]:32s} {os.path.basename(p):46s} {line}")


if __name__ == '__main__':
    main('--write' in sys.argv)
