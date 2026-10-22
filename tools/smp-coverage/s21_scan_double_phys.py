"""Scan every grafted facegen bake: how many PHYSICS-skinned shapes (any bone not named 'NPC ...')
does each carry, max bone count, HDT tag, VirtualHead. Writes a CSV + summary."""
import sys, os, struct, csv, collections
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\smp-coverage")
import nifrw, hairgraft

root = sys.argv[1]
out = sys.argv[2]
rows = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.lower().endswith(".nif"):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        try:
            d = nifrw.Doc(p)
            tag = False
            for i, (t, b) in enumerate(d.blocks):
                if t == "NiStringExtraData":
                    n, s = struct.unpack_from("<II", b, 0)
                    if d.strings[n] == "HDT Skinned Mesh Physics Object":
                        tag = True
            phys = []
            vh = False
            for i in hairgraft.shapes(d):
                sh = nifrw.parse_shape_hdr(d.blocks[i][1])
                if sh["skin"] < 0:
                    continue
                st, sb = d.blocks[sh["skin"]]
                nb = struct.unpack_from("<I", sb, 12)[0]
                bones = [hairgraft.node_name(d, x) for x in struct.unpack_from("<%di" % nb, sb, 16)]
                name = d.name_of(i)
                if name == "VirtualHead":
                    vh = True
                    continue
                if any(not str(bn).startswith("NPC ") for bn in bones):
                    phys.append((name, nb, sh["nvert"]))
            rows.append([rel, len(phys), max([x[1] for x in phys], default=0), int(tag), int(vh),
                         ";".join("%s|%d|%d" % x for x in phys)])
        except Exception as e:
            rows.append([rel, -1, 0, 0, 0, "ERR %r" % e])

with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["file", "n_physics_shapes", "max_bones", "hdt_tag", "virtualhead", "shapes"])
    w.writerows(rows)

c = collections.Counter((r[1], r[2] > 8, r[4]) for r in rows)
print("files:", len(rows))
print("(n_physics_shapes, >8 bones, virtualhead) -> count")
for k, v in sorted(c.items()):
    print("  ", k, v)
multi = [r for r in rows if r[1] >= 2]
print("two-or-more physics shapes:", len(multi))
for r in multi:
    print("  ", r[0], "|", r[5])
