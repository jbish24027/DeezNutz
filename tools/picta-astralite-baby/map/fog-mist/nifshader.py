"""Minimal SSE NIF parser: dump every BSEffectShaderProperty (source/greyscale texture, falloff, emissive) and
BSLightingShaderProperty texture set paths.  Read-only.  Usage: python nifshader.py file1.nif [file2.nif ...]"""
import struct, sys, json

def rd(fmt, b, o):
    v = struct.unpack_from(fmt, b, o)
    return v, o + struct.calcsize(fmt)

def parse(path):
    b = open(path, "rb").read()
    nl = b.index(b"\n")
    o = nl + 1
    (ver,), o = rd("<I", b, o)
    o += 1  # endian
    (uver, nblk), o = rd("<II", b, o)
    (bsver,), o = rd("<I", b, o)
    for _ in range(3):
        ln = b[o]; o += 1 + ln
    if bsver >= 103:
        ln = b[o]; o += 1 + ln
    (ntypes,), o = rd("<H", b, o)
    types = []
    for _ in range(ntypes):
        (ln,), o = rd("<I", b, o)
        types.append(b[o:o+ln].decode("latin1")); o += ln
    tidx = struct.unpack_from(f"<{nblk}H", b, o); o += 2 * nblk
    sizes = struct.unpack_from(f"<{nblk}I", b, o); o += 4 * nblk
    (nstr, maxlen), o = rd("<II", b, o)
    strings = []
    for _ in range(nstr):
        (ln,), o = rd("<I", b, o)
        strings.append(b[o:o+ln].decode("latin1")); o += ln
    (ngrp,), o = rd("<I", b, o)
    o += 4 * ngrp
    out = []
    for i in range(nblk):
        t = types[tidx[i] & 0x7FFF]
        start = o
        if t == "BSEffectShaderProperty":
            p = start
            (name,), p = rd("<i", b, p)
            (nex,), p = rd("<I", b, p); p += 4 * nex
            (ctrl,), p = rd("<i", b, p)
            (f1, f2), p = rd("<II", b, p)
            (uo0, uo1, us0, us1), p = rd("<4f", b, p)
            (ln,), p = rd("<I", b, p); src = b[p:p+ln].decode("latin1"); p += ln
            clamp, li, envlod, ub = b[p], b[p+1], b[p+2], b[p+3]; p += 4
            (fsa, fso, fsop, fstop), p = rd("<4f", b, p)
            (er, eg, eb, ea), p = rd("<4f", b, p)
            (emult, softd), p = rd("<2f", b, p)
            (ln,), p = rd("<I", b, p); grey = b[p:p+ln].decode("latin1"); p += ln
            out.append({"blk": i, "type": t, "name": strings[name] if 0 <= name < len(strings) else None,
                        "flags1": hex(f1), "flags2": hex(f2), "uv_scale": [round(us0, 3), round(us1, 3)],
                        "source": src, "greyscale": grey, "lighting_influence": li,
                        "falloff": [round(x, 4) for x in (fsa, fso, fsop, fstop)],
                        "emissive_rgba": [round(x, 4) for x in (er, eg, eb, ea)], "emissive_mult": round(emult, 4),
                        "soft_depth": round(softd, 3), "controller": ctrl})
        elif t == "BSShaderTextureSet":
            p = start
            (n,), p = rd("<I", b, p)
            ts = []
            for _ in range(n):
                (ln,), p = rd("<I", b, p); ts.append(b[p:p+ln].decode("latin1")); p += ln
            out.append({"blk": i, "type": t, "textures": [x for x in ts if x]})
        elif t == "BSPSysSimpleColorModifier":
            p = start
            (name,), p = rd("<i", b, p)
            p += 4  # order
            (target,), p = rd("<i", b, p)
            p += 1  # active
            vals, p = rd("<6f", b, p)
            cols, p = rd("<12f", b, p)
            out.append({"blk": i, "type": t, "fade": [round(x, 3) for x in vals],
                        "colors": [[round(x, 3) for x in cols[k*4:k*4+4]] for k in range(3)]})
        o = start + sizes[i]
    return {"bsver": bsver, "blocks": nblk, "shaders": out}

if __name__ == "__main__":
    res = {}
    for f in sys.argv[1:]:
        try:
            res[f] = parse(f)
        except Exception as e:
            res[f] = {"error": repr(e)}
    print(json.dumps(res, indent=1))
