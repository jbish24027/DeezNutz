"""Set the ESL (light) flag on an override-only plugin and add CNAM/SNAM to its TES4 header.

usage: python esl_header.py <plugin path> <author> <description>
Only the TES4 header record is rewritten; every other byte is kept as is.
"""
import struct, sys, hashlib

path, author, desc = sys.argv[1], sys.argv[2], sys.argv[3]
data = open(path, 'rb').read()
assert data[:4] == b'TES4', 'not a plugin'
size, flags, formid, vc, formver, unk = struct.unpack_from('<IIIIHH', data, 4)
hdr_end = 24 + size
body = data[24:hdr_end]
rest = data[hdr_end:]

subs = []
i = 0
while i + 6 <= len(body):
    sig = body[i:i+4]
    ln = struct.unpack_from('<H', body, i+4)[0]
    subs.append((sig, body[i+6:i+6+ln]))
    i += 6 + ln
assert i == len(body), 'header subrecords did not tile'
sigs = [s for s, _ in subs]
print('before: flags %08X formver %d subrecords %s' % (flags, formver, ' '.join(s.decode() for s in sigs)))
assert b'CNAM' not in sigs and b'SNAM' not in sigs, 'header already has author/description'

# check override-only: every top-level record FormID (outside groups' GRUP wrappers) must belong to a master
nmast = sigs.count(b'MAST')
own_index = nmast  # the plugin's own index = number of masters
def walk(buf, depth=0):
    j = 0
    found_own = 0
    while j + 24 <= len(buf):
        sig = buf[j:j+4]
        if sig == b'GRUP':
            gsize = struct.unpack_from('<I', buf, j+4)[0]
            found_own += walk(buf[j+24:j+gsize])
            j += gsize
        else:
            rsize = struct.unpack_from('<I', buf, j+4)[0]
            fid = struct.unpack_from('<I', buf, j+12)[0]
            if (fid >> 24) == own_index:
                found_own += 1
            j += 24 + rsize
    return found_own
own = walk(rest)
print('records defined by this plugin (own master index %02X): %d' % (own_index, own))
assert own == 0, 'plugin defines new records; refusing to flag ESL blindly'

new_subs = []
for s, v in subs:
    new_subs.append((s, v))
    if s == b'HEDR':
        new_subs.append((b'CNAM', author.encode('cp1252') + b'\0'))
        new_subs.append((b'SNAM', desc.encode('cp1252') + b'\0'))
new_body = b''.join(s + struct.pack('<H', len(v)) + v for s, v in new_subs)
new_flags = flags | 0x200
new_hdr = b'TES4' + struct.pack('<IIIIHH', len(new_body), new_flags, formid, vc, formver, unk)
out = new_hdr + new_body + rest
open(path, 'wb').write(out)
print('after:  flags %08X size %d -> %d bytes, md5 %s' % (new_flags, len(data), len(out), hashlib.md5(out).hexdigest()))
