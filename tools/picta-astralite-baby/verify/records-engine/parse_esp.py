"""Independent binary walk of a TES5 SE plugin: header, masters, every record (type, formid, flags, form version, editorid)."""
import struct, sys, zlib, json, collections

def parse(path):
    data = open(path, 'rb').read()
    out = {'path': path, 'size': len(data)}
    # TES4 header
    sig, dsize, flags, fid, vc, fver, unk = struct.unpack_from('<4sIIIIHH', data, 0)
    assert sig == b'TES4', sig
    out['header'] = {'flags_hex': hex(flags), 'esm': bool(flags & 1), 'localized': bool(flags & 0x80), 'esl': bool(flags & 0x200), 'formversion': fver}
    p = 24; end = 24 + dsize
    masters = []; subs = []
    while p < end:
        st, ss = struct.unpack_from('<4sH', data, p); p += 6
        body = data[p:p+ss]; p += ss
        subs.append(st.decode())
        if st == b'MAST':
            masters.append(body.rstrip(b'\0').decode('cp1252'))
        if st == b'HEDR':
            ver, nrec, nextid = struct.unpack('<fII', body)
            out['header'].update({'hedr_version': ver, 'hedr_numrecords': nrec, 'hedr_nextobjectid': hex(nextid)})
        if st == b'CNAM':
            out['header']['author'] = body.rstrip(b'\0').decode('cp1252', 'replace')
    out['masters'] = masters
    out['header_subrecords'] = subs
    recs = []; groups = []
    def walk(p, end, depth):
        while p < end:
            sig = data[p:p+4]
            if sig == b'GRUP':
                gsize, label, gtype = struct.unpack_from('<I4si', data, p+4)
                groups.append({'label': label.decode('cp1252', 'replace') if gtype == 0 else label.hex(), 'type': gtype, 'size': gsize, 'depth': depth})
                walk(p+24, p+gsize, depth+1)
                p += gsize
            else:
                rsig, rsize, rflags, rfid, rvc, rfver, runk = struct.unpack_from('<4sIIIIHH', data, p)
                body = data[p+24:p+24+rsize]
                if rflags & 0x40000:
                    body = zlib.decompress(body[4:])
                # subrecords
                q = 0; subl = []; edid = None; big = None
                while q < len(body):
                    st, ss = struct.unpack_from('<4sH', body, q); q += 6
                    if st == b'XXXX':
                        big = struct.unpack_from('<I', body, q)[0]; q += ss; continue
                    if big is not None:
                        ss = big; big = None
                    sb = body[q:q+ss]; q += ss
                    subl.append((st.decode('cp1252'), sb))
                    if st == b'EDID':
                        edid = sb.rstrip(b'\0').decode('cp1252')
                recs.append({'sig': rsig.decode(), 'formid': '%08X' % rfid, 'flags': hex(rflags), 'formversion': rfver, 'edid': edid, 'subs': subl, 'depth': depth})
                p += 24 + rsize
    walk(end, len(data), 0)
    out['records'] = recs
    out['groups'] = groups
    return out

if __name__ == '__main__':
    r = parse(sys.argv[1])
    print(json.dumps({k: v for k, v in r.items() if k not in ('records',)}, indent=1))
    c = collections.Counter(x['sig'] for x in r['records'])
    print('record count', len(r['records']), dict(c))
    print('formversions', collections.Counter(x['formversion'] for x in r['records']))
    print('record flags', collections.Counter(x['flags'] for x in r['records']))
    for x in r['records']:
        print(x['sig'], x['formid'], x['edid'], x['flags'], x['formversion'], [s for s, _ in x['subs']][:60])
