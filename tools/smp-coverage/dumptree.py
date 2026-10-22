"""Print a nif's node tree, extra data, and hair shape skinning (for eyeballing a graft). usage: dumptree.py <nif> [<nif>...]"""
import sys, struct
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\smp-coverage")
import nifrw, hairgraft

def f3(v):
    return "(" + ", ".join("%.3f" % x for x in v) + ")"

for path in sys.argv[1:]:
    d = nifrw.Doc(path)
    print("=" * 90); print(path, "| blocks", len(d.blocks), "| strings", len(d.strings))
    nodes = {i: nifrw.parse_node(b) for i, (t, b) in enumerate(d.blocks) if t in ("NiNode", "BSFadeNode")}
    def pr(i, depth):
        n = nodes[i]
        print("  " * depth + "%s [%d] flags %#x trans %s extra %s" % (hairgraft.node_name(d, i), i, n["flags"], f3(n["trans"]), n["extra"]))
        for c in n["children"]:
            if c in nodes:
                pr(c, depth + 1)
            elif c >= 0:
                t, b = d.blocks[c]
                sh = nifrw.parse_shape_hdr(b) if t in ("BSTriShape", "BSDynamicTriShape") else None
                print("  " * (depth + 1) + "<%s %s [%d] nvert %s flags %s skin %s shader %s alpha %s>" % (t, d.name_of(c), c, sh and sh["nvert"], sh and hex(sh["flags"]), sh and sh["skin"], sh and sh["shader"], sh and sh["alpha"]))
    for r in d.roots:
        pr(r, 0)
    for i, (t, b) in enumerate(d.blocks):
        if t == "NiStringExtraData":
            n, s = struct.unpack_from("<II", b, 0)
            print("  NiStringExtraData [%d]: %s = %s" % (i, d.strings[n], d.strings[s]))
    for i in hairgraft.shapes(d):
        sh = nifrw.parse_shape_hdr(d.blocks[i][1])
        if sh["skin"] < 0:
            continue
        st, sb = d.blocks[sh["skin"]]
        data, part, root = struct.unpack_from("<iii", sb, 0)
        nb = struct.unpack_from("<I", sb, 12)[0]
        bones = list(struct.unpack_from("<%di" % nb, sb, 16))
        parts = nifrw.parse_dismember(sb)["parts"] if st == "BSDismemberSkinInstance" else []
        print("  shape %-28s skin root %s parts %s bones %s" % (d.name_of(i), d.name_of(root) if root >= 0 else root, [p for f, p in parts], [hairgraft.node_name(d, x) for x in bones]))
        if sh["shader"] >= 0:
            refs, _ = nifrw.slots(*d.blocks[sh["shader"]])
            tex = struct.unpack_from("<i", d.blocks[sh["shader"]][1], refs[-1])[0]
            if tex >= 0:
                tb = d.blocks[tex][1]
                o = 0; ntex = struct.unpack_from("<I", tb, o)[0]; o += 4
                paths = []
                for _ in range(ntex):
                    ln = struct.unpack_from("<I", tb, o)[0]; o += 4
                    paths.append(tb[o:o + ln].decode("latin-1")); o += ln
                print("      textures:", [p for p in paths if p][:3])
