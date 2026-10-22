"""Graft an SMP hair mesh into an existing facegen head nif, in place of the static hair shape(s).

The result mirrors what the Creation Kit + jg1's SMP FaceGen produce: the hair nif's physics bone
nodes are copied under the face file's 'NPC Head [Head]' node with their local transforms, the hair
shape (geometry, skin instance, skin data, skin partition) is copied verbatim and renamed to the
head-part EditorID the record lists, the shader keeps the face file's own texture paths, and the
root gets the 'HDT Skinned Mesh Physics Object' extra data naming the physics xml.

Nothing about the head, eyes, brows, tint or any other shape is touched.
"""
import os, re, struct, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import nifrw

PHYS = "HDT Skinned Mesh Physics Object"
STANDARD_PREFIXES = ("NPC ", "Scene Root", "BSFaceGenNiNodeSkinned")

# --- nifrw only knows NiNode; BSFadeNode (facegen root) has the identical layout
_orig_slots = nifrw.slots
def _slots(t, b):
    if t == "BSFadeNode":
        return _orig_slots("NiNode", b)
    return _orig_slots(t, b)
nifrw.slots = _slots
nifrw.NAMED.add("BSFadeNode")

# --- some bakes carry junk bytes after the footer; the parse is complete before that check fires, so keep going
_orig_load = nifrw.Doc.load
def _load(self, path):
    try:
        _orig_load(self, path)
    except AssertionError as ex:
        if "trailing bytes" not in str(ex):
            raise
        self.trailing_junk = str(ex)
nifrw.Doc.load = _load


class GraftError(Exception):
    pass


def node_name(doc, i):
    t, b = doc.blocks[i]
    if t not in ("NiNode", "BSFadeNode"):
        return None
    si = struct.unpack_from("<I", b, 0)[0]
    return doc.strings[si] if si < len(doc.strings) else None


def node_index(doc):
    return {node_name(doc, i): i for i, (t, b) in enumerate(doc.blocks) if t in ("NiNode", "BSFadeNode")}


def parent_map(doc):
    pm = {}
    for i, (t, b) in enumerate(doc.blocks):
        if t in ("NiNode", "BSFadeNode"):
            for c in nifrw.parse_node(b)["children"]:
                if c >= 0:
                    pm[c] = i
    return pm


def shapes(doc):
    return [i for i, (t, b) in enumerate(doc.blocks) if t in ("BSTriShape", "BSDynamicTriShape")]


def is_standard(name):
    return name is None or name == "NPC" or any(name.startswith(p) for p in STANDARD_PREFIXES) or name.lower().endswith(".nif")


def hair_physics_xml(doc):
    for i, (t, b) in enumerate(doc.blocks):
        if t == "NiStringExtraData":
            n, s = struct.unpack_from("<II", b, 0)
            if doc.strings[n] == PHYS:
                return doc.strings[s]
    return None


def subtree(doc, i):
    """all node indices under node i (inclusive), depth-first"""
    out = [i]
    t, b = doc.blocks[i]
    for c in nifrw.parse_node(b)["children"]:
        if c >= 0 and doc.blocks[c][0] in ("NiNode", "BSFadeNode"):
            out.extend(subtree(doc, c))
    return out


def set_children(doc, i, children):
    t, b = doc.blocks[i]
    n = nifrw.parse_node(b)
    n["children"] = children
    doc.blocks[i][1] = nifrw.build_node(n)


def add_extra(doc, i, extra_idx):
    t, b = doc.blocks[i]
    n = nifrw.parse_node(b)
    n["extra"] = n["extra"] + [extra_idx]
    doc.blocks[i][1] = nifrw.build_node(n)


def copy_block(F, H, hi, refmap, strmap):
    """append H block hi into F; refs/strings remapped via the maps (which must be complete)."""
    t, b = H.blocks[hi]
    nb = bytearray(b)
    nifrw.remap_block(t, nb, refmap, strmap)
    F.blocks.append([t, nb])
    return len(F.blocks) - 1


HAIRTINT = 6  # BSLightingShaderProperty shader type; its last 12 bytes are the Hair Tint Color


def bake_hair_tint(F, fshapes, name):
    """12 colour bytes of the bake's HairTint for shape `name`, else the first HairTint shape in the bake, else None"""
    order = ([fshapes[name]] if name in fshapes else []) + [i for n, i in fshapes.items() if n != name]
    for si in order:
        sh = nifrw.parse_shape_hdr(F.blocks[si][1])
        if sh["shader"] < 0:
            continue
        st, sb = F.blocks[sh["shader"]]
        if st == "BSLightingShaderProperty" and struct.unpack_from("<I", sb, 0)[0] == HAIRTINT:
            return bytes(sb[-12:])
    return None


def shape_deps(H, si):
    """blocks a shape references: skin instance (+data, partition), shader (+texture set), alpha, extra data"""
    t, b = H.blocks[si]
    sh = nifrw.parse_shape_hdr(b)
    deps = {}
    for key in ("skin", "shader", "alpha"):
        if sh[key] >= 0:
            deps[key] = sh[key]
    deps["extra"] = [e for e in sh["extra"] if e >= 0]
    if "skin" in deps:
        st, sb = H.blocks[deps["skin"]]
        data, part, root = struct.unpack_from("<iii", sb, 0)
        nb = struct.unpack_from("<I", sb, 12)[0]
        deps["skin_data"] = data
        deps["skin_part"] = part
        deps["skin_root"] = root
        deps["bones"] = list(struct.unpack_from("<%di" % nb, sb, 16))
    if "shader" in deps:
        refs, _ = nifrw.slots(*H.blocks[deps["shader"]])
        tex = struct.unpack_from("<i", H.blocks[deps["shader"]][1], refs[-1])[0]
        deps["texset"] = tex
    return sh, deps


def graft(facegen_path, out_path, replacements, keep_bake_textures=True, part_remap=None, xml_override=None, log=print):
    """replacements: list of dicts {name: <bake shape name to replace>, hair: <SMP hair nif path>,
    extra_names: [names of further bake shapes that duplicate the same part and must go]}.
    Every replacement's hair nif is grafted as the named shape. Returns a report dict."""
    part_remap = part_remap or {31: 131, 41: 141}
    F = nifrw.Doc(facegen_path)
    if F.stream != 100:
        raise GraftError("facegen is not an SE (stream 100) nif: stream %d" % F.stream)
    fnodes = node_index(F)
    if "BSFaceGenNiNodeSkinned" not in fnodes:
        raise GraftError("no BSFaceGenNiNodeSkinned node")
    skinned = fnodes["BSFaceGenNiNodeSkinned"]
    root = F.roots[0]
    fshapes = {F.name_of(i): i for i in shapes(F)}
    report = dict(replaced=[], removed=[], bones=[], xml=[])
    pm = parent_map(F)
    new_children = []  # shapes to append to BSFaceGenNiNodeSkinned

    report["hidden"] = []
    for rep in replacements:
        name = rep["name"]
        if rep.get("hide"):
            # keep the bake's own static shape (the engine matches head parts by name) but hide it (NiAVObject flag 0x1),
            # so the face never carries a second physics-skinned copy of the hair (crash class 2026-10-15/16)
            if name not in fshapes:
                raise GraftError("bake has no shape named %r to hide" % name)
            hi = fshapes[name]
            d = nifrw.parse_shape_hdr(F.blocks[hi][1])
            d["flags"] |= 1
            F.blocks[hi][1] = nifrw.build_shape(d)
            report["hidden"].append(name)
            continue
        replace = rep.get("replace", True)
        if replace and name not in fshapes:
            raise GraftError("bake has no shape named %r (has %s)" % (name, sorted(fshapes)))
        H = nifrw.Doc(rep["hair"])
        if H.stream != 100:
            raise GraftError("hair nif %s is not stream 100" % rep["hair"])
        xml = hair_physics_xml(H)
        companion = rep.get("companion", False) or not replace
        if not xml and not companion:
            raise GraftError("hair nif %s carries no physics extra data" % rep["hair"])
        if xml and xml_override:
            xml = xml_override.get(rep["hair"], xml)
        hnodes = node_index(H)
        if "NPC Head [Head]" not in hnodes:
            raise GraftError("hair nif has no 'NPC Head [Head]' node")
        hshapes = shapes(H)
        if not hshapes:
            raise GraftError("hair nif has no shapes")

        # --- make sure F has the standard anchor nodes the hair skins to (Head, Spine2); copy from H if missing
        for std in ("NPC Head [Head]", "NPC Spine2 [Spn2]"):
            if std in hnodes and std not in fnodes:
                t, b = H.blocks[hnodes[std]]
                n = nifrw.parse_node(b)
                n["name"] = F.sidx(std); n["extra"] = []; n["ctrl"] = -1; n["coll"] = -1; n["children"] = []; n["effects"] = []
                F.blocks.append(["NiNode", nifrw.build_node(n)])
                fnodes[std] = len(F.blocks) - 1
                rt, rb = F.blocks[root]
                rn = nifrw.parse_node(rb); rn["children"] = rn["children"] + [fnodes[std]]
                F.blocks[root][1] = nifrw.build_node(rn)
                log("  added missing anchor node %s" % std)

        # --- physics bone nodes: every non-standard node in H, copied under the same-named parent in F
        hpm = parent_map(H)
        bone_ids = [i for i, (t, b) in enumerate(H.blocks) if t in ("NiNode", "BSFadeNode") and not is_standard(node_name(H, i))]
        # drop any same-named bones already in F (idempotent re-graft)
        for bi in bone_ids:
            nm = node_name(H, bi)
            if nm in fnodes:
                old = fnodes[nm]
                if old in pm:
                    pt, pb = F.blocks[pm[old]]
                    pn = nifrw.parse_node(pb)
                    pn["children"] = [c for c in pn["children"] if c != old]
                    F.blocks[pm[old]][1] = nifrw.build_node(pn)
                del fnodes[nm]
        refmap = {}
        strmap = {si: F.sidx(s) for si, s in enumerate(H.strings)}
        # top-level bones = those whose parent is standard
        tops = [bi for bi in bone_ids if is_standard(node_name(H, hpm.get(bi, -1)))]
        order = []
        for tb in tops:
            for i in subtree(H, tb):
                if i in bone_ids and i not in order:
                    order.append(i)
        for bi in order:
            refmap[bi] = None  # placeholder, assigned below
        # copy nodes in order; children refs point to later-copied nodes, so two passes
        for bi in order:
            F.blocks.append([H.blocks[bi][0], bytearray(H.blocks[bi][1])])
            refmap[bi] = len(F.blocks) - 1
        for bi in order:
            fi = refmap[bi]
            t, b = F.blocks[fi]
            n = nifrw.parse_node(b)
            n["name"] = strmap[n["name"]]
            n["extra"] = []; n["ctrl"] = -1; n["coll"] = -1; n["effects"] = []
            n["children"] = [refmap[c] for c in n["children"] if c in refmap]
            F.blocks[fi][1] = nifrw.build_node(n)
            fnodes[node_name(F, fi)] = fi
        for tb in tops:
            pname = node_name(H, hpm[tb])
            if pname not in fnodes:
                raise GraftError("hair bone %r hangs under %r which the bake lacks" % (node_name(H, tb), pname))
            pt, pb = F.blocks[fnodes[pname]]
            pn = nifrw.parse_node(pb)
            pn["children"] = pn["children"] + [refmap[tb]]
            F.blocks[fnodes[pname]][1] = nifrw.build_node(pn)
        report["bones"].append([node_name(H, bi) for bi in order])
        # standard nodes referenced by skins map by name
        for nm, hi in hnodes.items():
            if is_standard(nm) and nm in fnodes:
                refmap[hi] = fnodes[nm]
        refmap[H.roots[0]] = skinned  # skin instance skeleton root -> BSFaceGenNiNodeSkinned

        # --- the bake's old shape: remember its shader/alpha/hair colour, then detach it
        old_tex_paths = None
        old_alpha = None
        old_tint = bake_hair_tint(F, fshapes, name)
        if replace:
            old = fshapes[name]
            osh, odeps = shape_deps(F, old)
            if keep_bake_textures and "texset" in odeps and odeps["texset"] >= 0:
                old_tex_paths = F.blocks[odeps["texset"]][1]
            if rep.get("keep_bake_alpha") and "alpha" in odeps and odeps["alpha"] >= 0:
                old_alpha = F.blocks[odeps["alpha"]][1]
        for victim in ([name] if replace else []) + list(rep.get("extra_names", [])):
            if victim in fshapes and fshapes[victim] in pm:
                vi = fshapes[victim]
                pt, pb = F.blocks[pm[vi]]
                pn = nifrw.parse_node(pb)
                pn["children"] = [c for c in pn["children"] if c != vi]
                F.blocks[pm[vi]][1] = nifrw.build_node(pn)
                report["removed"].append(victim)

        # --- copy every shape of the hair nif
        for k, si in enumerate(hshapes):
            hsh, deps = shape_deps(H, si)
            local = dict(refmap)
            # dependency blocks first (skin data/partition, texture set, alpha, shader, skin instance)
            for key in ("skin_data", "skin_part", "texset", "alpha"):
                if key in deps and deps[key] >= 0:
                    local[deps[key]] = copy_block(F, H, deps[key], local, strmap)
                    if key == "alpha" and k == 0 and old_alpha is not None:
                        # a duplicate hair shape keeps the face file's own alpha settings (the author's edge trick)
                        nb = bytearray(old_alpha)
                        nifrw.remap_block("NiAlphaProperty", nb, {}, {si2: F.sidx(s) for si2, s in enumerate(F.strings)})
                        F.blocks[local[deps[key]]][1] = nb
            if "shader" in deps:
                local[deps["shader"]] = copy_block(F, H, deps["shader"], local, strmap)
                sb = F.blocks[local[deps["shader"]]]
                if old_tint is not None and sb[0] == "BSLightingShaderProperty" and struct.unpack_from("<I", sb[1], 0)[0] == HAIRTINT:
                    # keep the bake's Hair Tint Color (the record's HairColor), not the SMP file's default (2026-10-18)
                    nb = bytearray(sb[1]); nb[-12:] = old_tint; sb[1] = nb
                if k == 0 and old_tex_paths is not None and "texset" in deps:
                    # keep the face file's own textures for the main hair shape
                    F.blocks[local[deps["texset"]]][1] = bytearray(old_tex_paths)
            if "skin" in deps:
                for bone in deps["bones"]:
                    if bone not in local:
                        raise GraftError("skin bone %r of %s not mapped" % (node_name(H, bone), H.name_of(si)))
                if deps["skin_root"] not in local:
                    local[deps["skin_root"]] = skinned
                ski = copy_block(F, H, deps["skin"], local, strmap)
                # body-part slots 31/41 -> 131/141
                st, sb = F.blocks[ski]
                if st == "BSDismemberSkinInstance":
                    d = nifrw.parse_dismember(sb)
                    d["parts"] = [(f, part_remap.get(p, p)) for f, p in d["parts"]]
                    F.blocks[ski][1] = nifrw.build_dismember(d)
                local[deps["skin"]] = ski
            for e in deps["extra"]:
                local[e] = copy_block(F, H, e, local, strmap)
            # the shape itself
            sh_idx = copy_block(F, H, si, local, strmap)
            t, b = F.blocks[sh_idx]
            d = nifrw.parse_shape_hdr(b)
            d["name"] = F.sidx(name if k == 0 else "%s_%d" % (name, k))
            F.blocks[sh_idx][1] = nifrw.build_shape(d)
            new_children.append(sh_idx)
            report["replaced"].append((name if k == 0 else "%s_%d" % (name, k), H.name_of(si), d["nvert"]))

        # --- physics tag on the root
        existing = [x for x in (hair_physics_xml(F),) if x]
        if xml and xml.lower() not in [x.lower() for x in existing]:
            F.blocks.append(["NiStringExtraData", bytearray(struct.pack("<II", F.sidx(PHYS), F.sidx(xml)))])
            add_extra(F, root, len(F.blocks) - 1)
            report["xml"].append(xml)
        fshapes = {F.name_of(i): i for i in shapes(F)}
        pm = parent_map(F)

    # attach new shapes
    set_children(F, skinned, nifrw.parse_node(F.blocks[skinned][1])["children"] + new_children)
    G, _ = nifrw.rebuild(F)
    if len(out_path) > 240 and not out_path.startswith("\\\\?\\"):
        out_path = "\\\\?\\" + os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    G.save(out_path)
    # round-trip check
    G2 = nifrw.Doc(out_path)
    assert G2.tobytes() == G.tobytes(), "round-trip mismatch"
    report["blocks"] = len(G.blocks)
    return report
