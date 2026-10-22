"""Put each grafted head's baked hair colour back (2026-10-18).

hairgraft.py used the SMP hair nif's own shader for grafted shapes, so their Hair Tint Color (the last 12 bytes of a
HairTint BSLightingShaderProperty, baked by the CK from the record's HairColor) became the SMP file's default.
The beard and brows kept the real colour, so hair and beard no longer match.

For every head the graft mod wins, this reads the ORIGINAL bake (the next provider, loose or BSA) and copies each
HairTint shape's colour from the same-named shape there. A shape the bake lacks (an extra '_N' piece) takes the
colour of its base shape. Nothing else in the file changes; each output is checked byte for byte.

usage: s40_tint_fix.py <providers.jsonl from housecarl_asset_status> <out staging dir>
writes <out>/files/<data-relative path> and <out>/tintfix_report.json
"""
import json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hairgraft, nifrw  # hairgraft patches nifrw for BSFadeNode and junk-after-footer
from bsareader import BSA

MO2 = r"C:\1. AUTHORIA"
GRAFT_MOD = "Authoria - SMP Hair Grafts"
DATA = os.path.join(MO2, "Stock Game", "Data")
SHAPES = ("BSTriShape", "BSDynamicTriShape", "BSSubIndexTriShape")
LONG = "\\\\?\\"


def lp(p):
    p = os.path.abspath(p)
    return p if len(p) < 240 else LONG + p


def mod_dir(name):
    if name == "overwrite":
        return os.path.join(MO2, "overwrite")
    if name == "Data":
        return DATA
    return os.path.join(MO2, "mods", name)


_bsa_cache, _bsa_index = {}, None


def find_bsa(name):
    global _bsa_index
    if _bsa_index is None:
        _bsa_index = {}
        for root in [DATA] + [os.path.join(MO2, "mods", m) for m in os.listdir(os.path.join(MO2, "mods"))]:
            try:
                for f in os.listdir(root):
                    if f.lower().endswith(".bsa"):
                        _bsa_index.setdefault(f.lower(), []).append(os.path.join(root, f))
            except OSError:
                pass
    hits = _bsa_index.get(name.lower(), [])
    return hits[0] if hits else None


def read_provider(prov, rel):
    if prov["kind"] == "loose":
        with open(lp(os.path.join(mod_dir(prov["name"]), rel)), "rb") as f:
            return f.read()
    path = find_bsa(prov["name"])
    if not path:
        raise FileNotFoundError("archive not found: " + prov["name"])
    if path not in _bsa_cache:
        _bsa_cache[path] = BSA(path)
    return _bsa_cache[path].read(rel)


def hair_tints(doc):
    """{shape name lower: (shader block index, 12 colour bytes)} for HairTint shapes"""
    out = {}
    for i, (t, b) in enumerate(doc.blocks):
        if t not in SHAPES:
            continue
        sh = nifrw.parse_shape_hdr(b)
        if sh["shader"] < 0:
            continue
        st, sb = doc.blocks[sh["shader"]]
        if st == "BSLightingShaderProperty" and struct.unpack_from("<I", sb, 0)[0] == 6:
            out[doc.name_of(i).lower()] = (sh["shader"], bytes(sb[-12:]))
    return out


def doc_from_bytes(data, tmp):
    with open(tmp, "wb") as f:
        f.write(data)
    return nifrw.Doc(tmp)


def main(prov_file, out):
    rows = [json.loads(l) for l in open(prov_file, encoding="utf-8")][1:]
    rows = [r for r in rows if r.get("winner_mod") == GRAFT_MOD and r["path"].lower().endswith(".nif")]
    tmp = os.path.join(out, "_tmp_orig.nif")
    os.makedirs(out, exist_ok=True)
    rep = {"patched": [], "unchanged": [], "no_original": [], "errors": [], "unmatched_shapes": []}
    for n, r in enumerate(rows):
        rel = r["path"]
        try:
            below = [p for p in r["providers"] if p["name"] != GRAFT_MOD]
            if not below:
                rep["no_original"].append(rel)
                continue
            O = doc_from_bytes(read_provider(below[0], rel), tmp)
            otint = {k: v[1] for k, v in hair_tints(O).items()}
            src = os.path.join(mod_dir(GRAFT_MOD), rel)
            G = nifrw.Doc(lp(src))
            before = G.tobytes()
            changes = []
            for name, (shi, col) in hair_tints(G).items():
                want = otint.get(name) or otint.get(re.sub(r"_\d+$", "", name))
                if want is None:
                    rep["unmatched_shapes"].append([rel, name])
                    continue
                if want != col:
                    nb = bytearray(G.blocks[shi][1])
                    nb[-12:] = want
                    G.blocks[shi][1] = nb
                    changes.append([name, struct.unpack("<3f", col), struct.unpack("<3f", want)])
            if not changes:
                rep["unchanged"].append(rel)
                continue
            after = G.tobytes()
            diff = sum(1 for a, b in zip(before, after) if a != b)
            if len(after) != len(before) or diff > 12 * len(changes):
                raise RuntimeError("unexpected byte change: len %d->%d, %d bytes differ" % (len(before), len(after), diff))
            dst = os.path.join(out, "files", rel)
            os.makedirs(os.path.dirname(lp(dst)), exist_ok=True)
            with open(lp(dst), "wb") as f:
                f.write(after)
            rep["patched"].append({"path": rel, "original": below[0]["name"], "changes": changes})
        except Exception as e:
            rep["errors"].append([rel, repr(e)])
        if n % 500 == 0:
            print(n, "/", len(rows), flush=True)
    if os.path.exists(tmp):
        os.remove(tmp)
    json.dump(rep, open(os.path.join(out, "tintfix_report.json"), "w"), indent=1)
    print({k: len(v) for k, v in rep.items()})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
