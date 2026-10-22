"""Strip the placeholder shaders the UBE Converter minted onto SMP collision-only shapes.

Usage: strip_collision_shaders.py <in.nif> <out.nif> [shape names...]

For every BSTriShape named in the list (default: the Mage's Daily shawl proxies) the shader
reference is cleared, the NiAVObject flags are set to the plain BSTriShape default 0x8000E
(what the mod author's own ShapeData / BodySlide build carries), and the orphaned
BSLightingShaderProperty + BSShaderTextureSet blocks are dropped with a header rebuild.
Every other block must come out byte-identical after reference renumbering; the script
verifies that and refuses to write otherwise. Geometry, skinning, partitions, the physics
xml link and the BODYTRI link are never touched.
"""
import sys, struct, hashlib
sys.path.insert(0, "C:/1. AUTHORIA/_tools/magic-pariah-mm-rig")
from nifrw import Doc, rebuild, reachable, block_refs, slots, remap_block, parse_shape_hdr, build_shape

DEFAULT = ['bodyC', 'VirtualGround', 'shawlC', 'shawlFC', 'shawlBeltC', 'shawlF']
PLAIN_FLAGS = 0x8000E

def census(doc):
    c = {}
    for t, _ in doc.blocks:
        c[t] = c.get(t, 0) + 1
    return c

def texset_paths(b):
    n = struct.unpack_from('<I', b, 0)[0]; o = 4; out = []
    for _ in range(n):
        ln = struct.unpack_from('<I', b, o)[0]; o += 4
        out.append(b[o:o + ln].decode('latin-1')); o += ln
    assert o == len(b), 'BSShaderTextureSet size mismatch'
    return out

def main(src, dst, names):
    raw = open(src, 'rb').read()
    doc = Doc(src)
    # structural identity: the writer orders the header's block-type table by first use, which
    # pyNifly-written files do not, so compare the parsed document rather than the raw bytes
    import io, tempfile, os
    tmp = tempfile.NamedTemporaryFile(suffix='.nif', delete=False); tmp.write(doc.tobytes()); tmp.close()
    rt = Doc(tmp.name); os.unlink(tmp.name)
    for a in ('header_str', 'version', 'endian', 'user_version', 'stream', 'export_info', 'max_filepath', 'groups', 'roots', 'strings'):
        assert getattr(rt, a) == getattr(doc, a), 'round-trip changed %s' % a
    assert [(t, bytes(b)) for t, b in rt.blocks] == [(t, bytes(b)) for t, b in doc.blocks], 'round-trip changed block data'
    if rt.tobytes() != raw:
        print('  note: header block-type table re-ordered by the writer; block data, strings, roots identical')
    assert len(set(doc.strings)) == len(doc.strings), 'duplicate strings in table'
    n0 = len(doc.blocks)
    before = {i: (t, bytes(b)) for i, (t, b) in enumerate(doc.blocks)}
    c_before = census(doc)

    drop = set(); edited = {}
    for i, (t, b) in enumerate(doc.blocks):
        if t != 'BSTriShape' or doc.name_of(i) not in names:
            continue
        h = parse_shape_hdr(b)
        name = doc.name_of(i)
        assert h['alpha'] == -1, '%s has an alpha property' % name
        sh = h['shader']
        assert sh >= 0 and doc.blocks[sh][0] == 'BSLightingShaderProperty', '%s: no lighting shader' % name
        ts = block_refs('BSLightingShaderProperty', doc.blocks[sh][1])[-1]
        assert ts >= 0 and doc.blocks[ts][0] == 'BSShaderTextureSet', '%s: shader has no texture set' % name
        paths = texset_paths(doc.blocks[ts][1])
        assert all(p == '' for p in paths), '%s: texture set is NOT empty: %r' % (name, paths)
        # nobody else may use that shader / texture set
        for j, (tj, bj) in enumerate(doc.blocks):
            if j != i and sh in [r for r in block_refs(tj, bj)]:
                raise AssertionError('shader %d shared by block %d' % (sh, j))
            if j != sh and ts in [r for r in block_refs(tj, bj)]:
                raise AssertionError('texset %d shared by block %d' % (ts, j))
        print('  %-14s block %3d flags 0x%X -> 0x%X, shader %d + texset %d (%d empty slots) dropped'
              % (name, i, h['flags'], PLAIN_FLAGS, sh, ts, len(paths)))
        h['shader'] = -1; h['flags'] = PLAIN_FLAGS
        nb = build_shape(h)
        assert len(nb) == len(b)
        doc.blocks[i][1] = bytearray(nb)
        drop |= {sh, ts}; edited[i] = (sh, ts)
    assert len(edited) == len(names), 'expected %d shapes, edited %d' % (len(names), len(edited))

    nd, refmap = rebuild(doc)
    dropped = set(range(n0)) - set(refmap)
    assert dropped == drop, 'rebuild dropped %r, expected %r' % (sorted(dropped), sorted(drop))
    strmap = {doc.strings.index(s): j for j, s in enumerate(nd.strings)}
    assert set(strmap) == set(range(len(doc.strings))), 'strings were dropped: %r' % (set(range(len(doc.strings))) - set(strmap))

    # every kept block must equal the pre-edit block after pure renumbering, except the
    # edited shape headers, which may differ ONLY in flags and the cleared shader ref
    for old, new in refmap.items():
        t, ob = before[old]
        nb = bytes(nd.blocks[new][1])
        assert nd.blocks[new][0] == t
        if old in edited:
            a = parse_shape_hdr(ob); b = parse_shape_hdr(nb)
            for k in ('name', 'extra', 'ctrl', 'trans', 'rot', 'scale', 'coll', 'bound', 'skin', 'alpha', 'vdesc', 'ntri', 'nvert', 'dsize', 'tail'):
                av, bv = a[k], b[k]
                if k == 'name': av = strmap[av]
                elif k == 'extra': av = [refmap[x] if x >= 0 else x for x in av]
                elif k in ('ctrl', 'coll', 'skin', 'alpha'): av = refmap[av] if av >= 0 else av
                assert av == bv, '%s: field %s changed' % (doc.name_of(old), k)
            assert b['shader'] == -1 and b['flags'] == PLAIN_FLAGS
        else:
            exp = bytearray(ob); remap_block(t, exp, refmap, strmap)
            assert bytes(exp) == nb, 'block %d (%s) changed beyond renumbering' % (old, t)

    out = nd.tobytes()
    open(dst, 'wb').write(out)
    chk = Doc(dst)
    assert chk.tobytes() == out
    assert reachable(chk) == set(range(len(chk.blocks))), 'unreachable blocks after rebuild'
    for i, (t, b) in enumerate(chk.blocks):
        for r in block_refs(t, b):
            assert -1 <= r < len(chk.blocks), 'dangling ref in block %d' % i
    c_after = census(chk)
    exp = dict(c_before); exp['BSLightingShaderProperty'] -= len(edited); exp['BSShaderTextureSet'] -= len(edited)
    assert c_after == exp, 'census mismatch: %r vs %r' % (c_after, exp)
    xml = [s for s in chk.strings if s.lower().endswith('.xml')]
    tri = [s for s in chk.strings if s.lower().endswith('.tri')]
    print('  blocks %d -> %d, strings %d -> %d, xml link %r, tri link %r' % (n0, len(chk.blocks), len(doc.strings), len(chk.strings), xml, tri))
    print('  sha256 in  %s' % hashlib.sha256(raw).hexdigest())
    print('  sha256 out %s' % hashlib.sha256(out).hexdigest())

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    names = sys.argv[3:] or DEFAULT
    print('== %s' % src)
    main(src, dst, names)
    print('OK')
