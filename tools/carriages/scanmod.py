import os, struct, zlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plug import masters, subs


def scan(path, store, plugname, tg):
    """collect REFRs (temporary + persistent with a grid) in target cells: gid -> (plugin, world, pos6, base gid, deleted, XSCL, disabled)"""
    b = open(path, 'rb').read()
    if b[:4] != b'TES4': return
    m = masters(b); name = os.path.basename(path)
    def gid(k):
        i = k >> 24; return ((m[i] if i < len(m) else name).lower(), k & 0xFFFFFF)
    s = struct.unpack('<I', b[4:8])[0]; off = 24 + s
    worlds = {w for w, g in tg}
    def walk(o, end, world, grid, persist):
        while o < end:
            sig = b[o:o + 4]; size = struct.unpack('<I', b[o + 4:o + 8])[0]
            if sig == b'GRUP':
                gt = struct.unpack('<i', b[o + 12:o + 16])[0]; lab = b[o + 8:o + 12]
                if gt == 1:
                    w = gid(struct.unpack('<I', lab)[0])
                    if w in worlds: walk(o + 24, o + size, w, None, False)
                elif gt in (4, 5): walk(o + 24, o + size, world, None, False)
                elif gt in (6, 9): walk(o + 24, o + size, world, grid, False)
                elif gt == 8: walk(o + 24, o + size, world, grid, True)
                o += size; continue
            size, flags, fid = struct.unpack('<III', b[o + 4:o + 16])
            if sig == b'CELL':
                d = b[o + 24:o + 24 + size]
                if flags & 0x40000: d = zlib.decompress(d[4:])
                grid = None
                for t, v in subs(d):
                    if t == 'XCLC': grid = struct.unpack('<ii', v[:8]); break
            elif sig == b'REFR' and world:
                d = b[o + 24:o + 24 + size]
                if flags & 0x40000: d = zlib.decompress(d[4:])
                dd = dict(subs(d))
                if 'DATA' in dd and 'NAME' in dd:
                    pos = struct.unpack('<6f', dd['DATA'][:24])
                    cg = (int(pos[0] // 4096), int(pos[1] // 4096))
                    if (world, cg) in tg:
                        store[gid(fid)] = (plugname, world, pos, gid(struct.unpack('<I', dd['NAME'][:4])[0]), bool(flags & 0x20), dd.get('XSCL'), bool(flags & 0x800), 'XESP' in dd)
            o += 24 + size
    while off < len(b):
        size = struct.unpack('<I', b[off + 4:off + 8])[0]
        if b[off + 8:off + 12] == b'WRLD': walk(off + 24, off + size, None, None, False)
        off += size
