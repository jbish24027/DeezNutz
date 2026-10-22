"""BSA side of the SMP audit.
1. Index every nif inside every ACTIVE mod BSA (profile archives.txt order = load order; vanilla/CC skipped).
2. Where a loose winner exists for the same path: extract the BSA copy, test SMP; flag BSA-SMP buried by loose-static.
3. Where 2+ BSAs carry the path and no loose copy: later BSA wins; flag static-later over SMP-earlier.
Also records every SMP mesh found in BSAs (for the twin/xml checks).
Read-only.
"""
import os, sys, json, struct, time, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smp_audit import enabled_mods, walk_files, smp_info, INSTANCE, MODS, OVERWRITE, PROFILE, HDT_TAG
import lz4.frame, lz4.block, zlib

VANILLA_PREFIX = ('skyrim - ', 'update', 'dawnguard', 'hearthfires', 'dragonborn', 'ccbgssse', 'ccqdrsse', 'ccpewsse', 'cckrtsse', 'ccasvsse', 'ccedhsse', 'ccffbsse', 'ccmtysse', 'ccrmssse', 'cctwbsse', 'ccvsvsse', 'ccafdsse', 'cceejsse', 'ccfsvsse', 'ccbgssse', '_resourcepack')

def read_bsa_index(path):
    """Return dict relpath(lower, backslash) -> (offset, size, compressed_flag) and the archive flags."""
    with open(path, 'rb') as fh:
        hdr = fh.read(36)
        if hdr[:4] != b'BSA\x00':
            return None, 'not a BSA (maybe BA2)'
        version, folder_off, aflags, nfold, nfile, tfold, tfile, fflags, pad = struct.unpack_from('<IIIIIIIHH', hdr, 4)
        fh.seek(folder_off)
        frec_size = 24 if version >= 105 else 16
        folders = []
        data = fh.read(frec_size * nfold)
        for i in range(nfold):
            if version >= 105:
                h, cnt, pad2, off = struct.unpack_from('<QIIQ', data, i*24)
            else:
                h, cnt, off = struct.unpack_from('<QII', data, i*16)
            folders.append((cnt, off))
    # file record blocks follow the folder records: region = tfold + nfold(len bytes) + 16*nfile, then the name table (tfile)
    with open(path, 'rb') as fh:
        start = folder_off + frec_size * nfold
        region = (tfold + nfold) if (aflags & 0x1) else 0
        region += 16 * nfile
        fh.seek(start)
        blk = fh.read(region)
        names = fh.read(tfile) if (aflags & 0x2) else b''
    p = 0
    entries = []
    for cnt, off in folders:
        if aflags & 0x1:
            ln = blk[p]; p += 1
            fname = blk[p:p+ln-1].decode('latin1'); p += ln
        else:
            fname = ''
        for _ in range(cnt):
            h, size, offset = struct.unpack_from('<QII', blk, p); p += 16
            entries.append([fname, size, offset])
    if aflags & 0x2:
        parts = names.split(b'\x00')
        for i, e in enumerate(entries):
            e.append(parts[i].decode('latin1') if i < len(parts) else '')
    else:
        for e in entries:
            e.append('')
    idx = {}
    default_compressed = bool(aflags & 0x4)
    embed_names = bool(aflags & 0x100)
    for fname, size, offset, name in entries:
        rel = (fname + '\\' + name).lower().replace('/', '\\')
        comp = default_compressed ^ bool(size & 0x40000000)
        idx[rel] = (offset, size & 0x3FFFFFFF, comp, embed_names, version)
    return idx, None

def extract(path, meta):
    offset, size, comp, embed, version = meta
    with open(path, 'rb') as fh:
        fh.seek(offset)
        buf = fh.read(size)
    p = 0
    if embed:
        ln = buf[0]; p = 1 + ln
    if comp:
        orig, = struct.unpack_from('<I', buf, p); p += 4
        payload = buf[p:]
        if version >= 105:
            try:
                return lz4.frame.decompress(payload)
            except Exception:
                return lz4.block.decompress(payload, uncompressed_size=orig)
        else:
            return zlib.decompress(payload)
    return buf[p:]

def smp_of_bytes(data):
    """Same logic as smp_info but on bytes."""
    if HDT_TAG not in data:
        return False, []
    import tempfile
    # reuse smp_info by writing to a temp file (simple + reliable)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.nif') as tf:
        tf.write(data); name = tf.name
    try:
        s, x, e = smp_info(name)
    finally:
        os.unlink(name)
    return (s if s is not None else True), x

def main():
    t0 = time.time()
    mods = enabled_mods()
    # loose provider map (nif + xml)
    providers = {}
    sources = [('overwrite', OVERWRITE)] + [(m, os.path.join(MODS, m)) for m in mods]
    for prio, (name, root) in enumerate(sources):
        for rel, full in walk_files(root):
            providers.setdefault(rel, []).append((prio, name, full))
    loose_nif_winner = {k: sorted(v)[0] for k, v in providers.items() if k.endswith('.nif')}
    loose_xml = {k for k in providers if k.endswith('.xml')}
    # active BSAs
    with open(os.path.join(INSTANCE, 'profiles', PROFILE, 'archives.txt'), encoding='utf-8') as fh:
        archives = [l.strip() for l in fh if l.strip()]
    # locate each BSA file among enabled mods (highest priority provider)
    bsa_files = {}
    for prio, (name, root) in enumerate(sources):
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if f.lower().endswith('.bsa'):
                    bsa_files.setdefault(f.lower(), []).append((prio, name, os.path.join(dp, f)))
    bsa_list = []  # (load_index, bsa name, mod, path)
    missing = []
    for i, a in enumerate(archives):
        al = a.lower()
        if al.startswith(VANILLA_PREFIX):
            continue
        if al in bsa_files:
            prio, name, path = sorted(bsa_files[al])[0]
            bsa_list.append((i, a, name, path))
        else:
            missing.append(a)
    print('active mod BSAs located: %d (skipped vanilla/CC; not found in enabled mods: %d)' % (len(bsa_list), len(missing)))
    # index nifs + xmls in each BSA
    bsa_nifs = {}   # rel -> list of (load_index, bsa, mod, path, meta)
    bsa_xmls = set()
    bsa_meta_cache = {}
    for i, a, mod, path in bsa_list:
        idx, err = read_bsa_index(path)
        if err:
            print('  skip %s: %s' % (a, err)); continue
        for rel, meta in idx.items():
            if rel.endswith('.nif'):
                bsa_nifs.setdefault(rel, []).append((i, a, mod, path, meta))
            elif rel.endswith('.xml'):
                bsa_xmls.add(rel)
    print('BSA nif paths: %d, BSA xml paths: %d (%.0fs)' % (len(bsa_nifs), len(bsa_xmls), time.time()-t0))
    # A) BSA copy exists AND a loose winner exists
    cand = [rel for rel in bsa_nifs if rel in loose_nif_winner]
    print('paths with both loose winner and BSA copy: %d' % len(cand))
    buried_by_loose = []
    bsa_smp_all = {}   # rel -> (bsa, mod, xmls) for the highest-loading SMP BSA copy
    n = 0
    for rel in cand:
        # highest-loading BSA copy is the BSA-side winner
        copies = sorted(bsa_nifs[rel], key=lambda x: x[0])
        i, a, mod, path, meta = copies[-1]
        try:
            data = extract(path, meta)
        except Exception as e:
            print('  extract failed %s in %s: %s' % (rel, a, e)); continue
        s, x = smp_of_bytes(data)
        n += 1
        if s:
            bsa_smp_all[rel] = (a, mod, x)
            ws, wx, we = smp_info(loose_nif_winner[rel][2])
            if ws is False:
                buried_by_loose.append({'path': rel, 'loose_winner': loose_nif_winner[rel][1], 'bsa': a, 'bsa_mod': mod})
    print('checked %d BSA copies against loose winners (%.0fs)' % (n, time.time()-t0))
    # B) BSA-only paths carried by 2+ BSAs: later wins; flag static-later over SMP-earlier
    multi = [rel for rel, v in bsa_nifs.items() if len(v) >= 2 and rel not in loose_nif_winner]
    print('BSA-only paths carried by 2+ BSAs: %d' % len(multi))
    buried_bsa_vs_bsa = []
    m = 0
    for rel in multi:
        copies = sorted(bsa_nifs[rel], key=lambda x: x[0])
        # test the winner first; only if static, test the earlier ones
        i, a, mod, path, meta = copies[-1]
        try:
            ws, wx = smp_of_bytes(extract(path, meta))
        except Exception as e:
            continue
        m += 1
        if ws:
            bsa_smp_all[rel] = (a, mod, wx); continue
        for j, b, mod2, path2, meta2 in copies[:-1]:
            try:
                s2, x2 = smp_of_bytes(extract(path2, meta2))
            except Exception:
                continue
            if s2:
                buried_bsa_vs_bsa.append({'path': rel, 'winner_bsa': a, 'winner_mod': mod, 'smp_bsa': b, 'smp_mod': mod2}); break
    print('checked %d BSA-vs-BSA winners (%.0fs)' % (m, time.time()-t0))
    # xml existence for BSA SMP winners (loose or BSA xml)
    def norm(x):
        k = x.replace('/', '\\').lower().lstrip('\\')
        return k[5:] if k.startswith('data\\') else k
    missing_xml = []
    for rel, (a, mod, xl) in bsa_smp_all.items():
        if rel in loose_nif_winner:
            continue  # loose wins anyway
        for x in xl:
            k = norm(x)
            if k not in loose_xml and k not in bsa_xmls:
                missing_xml.append({'path': rel, 'bsa': a, 'xml': x})
    res = {'bsas': len(bsa_list), 'missing_bsas': missing, 'buried_by_loose': buried_by_loose, 'buried_bsa_vs_bsa': buried_bsa_vs_bsa,
           'bsa_smp_paths': {k: v for k, v in bsa_smp_all.items()}, 'missing_xml_bsa_winners': missing_xml}
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bsa_audit_result.json'), 'w'), indent=1)
    print('\n=== BSA SMP copies buried by a LOOSE static winner: %d' % len(buried_by_loose))
    byw = {}
    for b in buried_by_loose:
        byw.setdefault(b['loose_winner'], []).append(b)
    for w, items in sorted(byw.items(), key=lambda kv: -len(kv[1])):
        print('\n[%s] buries %d:' % (w, len(items)))
        for b in items[:60]:
            print('   %s   <- SMP in %s (%s)' % (b['path'], b['bsa'], b['bsa_mod']))
        if len(items) > 60: print('   ... %d more' % (len(items)-60))
    print('\n=== BSA-vs-BSA: static later BSA over SMP earlier BSA: %d' % len(buried_bsa_vs_bsa))
    for b in buried_bsa_vs_bsa[:60]:
        print('   %s   winner %s (%s)  <- SMP in %s (%s)' % (b['path'], b['winner_bsa'], b['winner_mod'], b['smp_bsa'], b['smp_mod']))
    print('\n=== BSA SMP winners with no xml anywhere: %d' % len(missing_xml))
    for x in missing_xml[:40]:
        print('   %s (%s) -> %s' % (x['path'], x['bsa'], x['xml']))
    print('\nSMP meshes found in BSAs (winner-side): %d' % len(bsa_smp_all))
    print('done in %.0fs' % (time.time()-t0))

if __name__ == '__main__':
    main()
