# Balgruuf facegen: retint HumanBeardMedium04 to the bake's hair tint and point it + 0BalgruufBeardHL at TSOS beard textures.
import sys, struct
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import nifrw
src, dst = sys.argv[1], sys.argv[2]
d = nifrw.Doc(src)
REPL = {r"textures\actors\character\beards\beardshort06.dds": r"textures\0TSOS\!COR\beard\beardshort06.dds",
        r"textures\actors\character\beards\beardshort06_n.dds": r"textures\0TSOS\!COR\beard\beardshort06_n.dds",
        r"textures\0TSOS\!COR\beard\beardshort05_hd.dds": r"textures\0TSOS\!COR\beard\beardshort05.dds",
        r"textures\0TSOS\!COR\beard\beardshort05_hd_n.dds": r"textures\0TSOS\!COR\beard\beardshort05_n.dds"}
def shader_of(name):
    for t, b in d.blocks:
        if t in ("BSDynamicTriShape", "BSTriShape") and d.strings[struct.unpack('<i', b[:4])[0]] == name:
            return nifrw.parse_shape_hdr(b)["shader"]
def texset_of(si):
    b = d.blocks[si][1]; n = struct.unpack('<I', b[8:12])[0]; o = 12 + 4*n + 4 + 8 + 16
    return struct.unpack('<i', b[o:o+4])[0]
def fix_texset(ti):
    b = d.blocks[ti][1]; n = struct.unpack('<I', b[:4])[0]; o = 4; out = [b[:4]]; changed = 0
    for _ in range(n):
        L = struct.unpack('<I', b[o:o+4])[0]; s = b[o+4:o+4+L].decode('latin1'); o += 4 + L
        if s.lower() in {k.lower(): 0 for k in REPL}:
            s = next(v for k, v in REPL.items() if k.lower() == s.lower()); changed += 1
        e = s.encode('latin1'); out.append(struct.pack('<I', len(e)) + e)
    out.append(b[o:]); d.blocks[ti][1] = b"".join(out); return changed
ref = shader_of("0Hair6"); tint = d.blocks[ref][1][-12:]
s = shader_of("HumanBeardMedium04"); b = d.blocks[s][1]; d.blocks[s][1] = b[:-12] + tint
print("tint", struct.unpack('<3f', tint), "paths fixed",
      fix_texset(texset_of(s)), fix_texset(texset_of(shader_of("0BalgruufBeardHL"))))
d.save(dst)
