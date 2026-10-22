#!/usr/bin/env python
"""
dav_cosave.py - inspect / repair Dynamic Armor Variants state in SKSE co-saves.

DAV stores its applied per-actor variant overrides in the co-save plugin chunk
'FVAA' / 'OVAA' as plain JSON, e.g.
    {"overrides":[{"actor":20,"variants":["HT_HiddenHelmetHairOnlyPlayer"]}]}
actor 20 (0x14) is the player.

An ApplyVariant() that never gets its matching ResetVariant() sticks forever:
Helmet Toggle's HT_HiddenHelmetHairOnlyPlayer replaces EVERY biped slot 31
(hair) item with an invisible mesh, so wigs stop rendering.

    scan  <saves-dir|file>
    clear <saves-dir|file> [--actor 20] [--variant NAME] [--apply]

Dry run unless --apply. One .bak-pre-dav-<ts> per written file.
"""
import argparse, glob, json, os, shutil, struct, sys, time

DAV_PLUGIN = 'FVAA'      # u32 signature rendered little-endian
DAV_CHUNK  = 'OVAA'

def s4(v): return struct.pack('<I', v).decode('latin1')

def walk(d):
    """Return (plugins, header_len). plugins = [(sig, off_of_pluginheader, nchunks, len, [(ctype,cver,clen,coff)])]"""
    if d[:4] != b'SKSE':
        raise ValueError('not an SKSE co-save')
    fmt, skse, rt, npl = struct.unpack_from('<IIII', d, 4)
    off = 20
    plugins = []
    for _ in range(npl):
        ph = off
        sig, nch, ln = struct.unpack_from('<III', d, off); off += 12
        o = off; chunks = []
        for _ in range(nch):
            ct, cv, cl = struct.unpack_from('<III', d, o); o += 12
            chunks.append((s4(ct), cv, cl, o)); o += cl
        if o != off + ln:
            raise ValueError('chunk walk overshot plugin %r' % s4(sig))
        plugins.append((s4(sig), ph, nch, ln, chunks))
        off += ln
    if off != len(d):
        raise ValueError('plugin walk did not land on EOF (%d != %d)' % (off, len(d)))
    return plugins

def find_dav(d):
    for sig, ph, nch, ln, chunks in walk(d):
        if sig != DAV_PLUGIN:
            continue
        for ct, cv, cl, co in chunks:
            if ct == DAV_CHUNK:
                return ph, ln, co, cl, cv
    return None

def read_state(path):
    d = open(path, 'rb').read()
    hit = find_dav(d)
    if not hit:
        return d, None, None
    ph, ln, co, cl, cv = hit
    raw = d[co:co+cl]
    try:
        return d, hit, json.loads(raw.decode('utf-8'))
    except Exception as e:
        return d, hit, {'__parse_error__': str(e), '__raw__': raw.decode('latin1')}

def rewrite(d, hit, newobj):
    ph, ln, co, cl, cv = hit
    new = json.dumps(newobj, separators=(',', ':')).encode('utf-8')
    delta = len(new) - cl
    out = bytearray(d)
    out[co:co+cl] = new                                   # body
    # chunk header sits 12 bytes before the body: type, version, length
    struct.pack_into('<I', out, co - 4, len(new))
    # plugin header: signature, numChunks, length  -> length is +8
    struct.pack_into('<I', out, ph + 8, ln + delta)
    return bytes(out), delta

def verify(orig, new, delta, hit, expect_obj):
    po, pn = walk(orig), walk(new)
    assert len(po) == len(pn), 'plugin count changed'
    for a, b in zip(po, pn):
        assert a[0] == b[0], 'plugin order changed'
        assert a[2] == b[2], 'chunk count changed for %r' % a[0]
        if a[0] != DAV_PLUGIN:
            assert a[3] == b[3], 'unrelated plugin %r length changed' % a[0]
    assert len(new) == len(orig) + delta, 'size delta mismatch'
    h = find_dav(new)
    assert h, 'DAV chunk vanished'
    got = json.loads(new[h[2]:h[2]+h[3]].decode('utf-8'))
    assert got == expect_obj, 'readback mismatch'
    return True

def targets(p):
    if os.path.isdir(p):
        return sorted(glob.glob(os.path.join(p, '*.skse')))
    return [p]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['scan', 'clear'])
    ap.add_argument('path')
    ap.add_argument('--actor', type=int, default=None, help='actor id (decimal); 20 = player')
    ap.add_argument('--variant', default=None, help='only drop this variant name')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    files = targets(a.path)
    if not files:
        print('no .skse files at', a.path); return 1
    ts = time.strftime('%Y%m%d-%H%M%S')
    changed = 0

    for f in files:
        try:
            d, hit, obj = read_state(f)
        except Exception as e:
            print('SKIP %-70s %s' % (os.path.basename(f), e)); continue
        name = os.path.basename(f)
        if not hit:
            if a.cmd == 'scan': print('%-72s no DAV chunk' % name)
            continue
        ovr = (obj.get('overrides') or []) if isinstance(obj, dict) else []
        if a.cmd == 'scan':
            print('%-72s %s' % (name, json.dumps(obj, separators=(',', ':'))))
            continue

        keep = []
        dropped = []
        for e in ovr:
            if a.actor is not None and e.get('actor') != a.actor:
                keep.append(e); continue
            vs = e.get('variants', [])
            if a.variant:
                left = [v for v in vs if v != a.variant]
                gone = [v for v in vs if v == a.variant]
            else:
                left, gone = [], list(vs)
            if gone: dropped.append((e.get('actor'), gone))
            if left:
                e = dict(e); e['variants'] = left; keep.append(e)
        if not dropped:
            print('%-72s nothing to clear' % name); continue

        # DAV itself serialises 'no overrides' as null, so match that exactly
        newobj = dict(obj); newobj['overrides'] = keep if keep else None
        newd, delta = rewrite(d, hit, newobj)
        verify(d, newd, delta, hit, newobj)
        print('%-72s drop %s  (%+d bytes)%s' % (name, dropped, delta, '' if a.apply else '  [dry run]'))
        if a.apply:
            shutil.copy2(f, f + '.bak-pre-dav-' + ts)
            open(f, 'wb').write(newd)
        changed += 1

    print('\n%d file(s) %s' % (changed, 'written' if a.apply else 'would change'))
    return 0

if __name__ == '__main__':
    sys.exit(main())
