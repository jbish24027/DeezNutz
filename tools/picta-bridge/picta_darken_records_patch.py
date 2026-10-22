"""Build 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp' (ESL-flagged, override-only): the record-side brightness of
Picta 1.1.1 brought back to 1.0.1, values taken from the verified 6-lane sweep (workflow wf_43f22efe-fcd, 2026-10-12).
 - CLMT 000812:Skyrim.esm PIC_CLMT_Skyrim (from the 1.1.1 esp): TNAM sunrise end 08:00 -> 09:00, sunset begin 18:00 -> 17:00.
 - VOLI present in both esms (same FormID + EditorID): 1.0.1 record body verbatim (phase scattering, sunset intensity, range factor).
 - WTHR 23 PIC_WTHR_MASTER (from the 1.1.1 esm): NAM0 FogFar per category, night SkyUpper/SkyLower/Horizon 75; cloud layers 27/28
   colours per category + layer 27 alpha 0 on the listed weathers; DALC scaled by the per-weather k (D05/D06 sides x0.80 extra);
   mist weathers' fog distances + volumetric-lighting links back to the 1.0.1 mist set.
Masters = the 1.1.1 esm's own master list + the esm, so every FormID copied out of the esm keeps its bytes.
--write writes the plugin into the mod folder (MO2 and the game must be closed). Without it: report only."""
import os, sys, struct, zlib, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WRITE = '--write' in sys.argv
MODS = r'C:\1. AUTHORIA\mods'
ESM111 = os.path.join(MODS, '[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)', 'Picta - Weathers of Aurbis.esm')
ESP111 = os.path.join(MODS, '[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)', 'Picta - Weathers of Skyrim.esp')
ESM101 = os.path.join(MODS, '[NoDelete] Picta - Weathers of Aurbis 1.0.1 (shipped)', 'Picta - Weathers of Aurbis.esm')
OUTDIR = os.path.join(MODS, 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1')
OUTNAME = 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp'
PICTA = 'Picta - Weathers of Aurbis.esm'

def read_plugin(path):
    d = open(path, 'rb').read(); hsz = struct.unpack_from('<I', d, 4)[0]; hdr = d[24:24 + hsz]; masters = []; q = 0
    while q + 6 <= len(hdr):
        s = hdr[q:q + 4]; n = struct.unpack_from('<H', hdr, q + 4)[0]
        if s == b'MAST': masters.append(hdr[q + 6:q + 6 + n].rstrip(b'\0').decode('cp1252'))
        q += 6 + n
    recs = {}
    def walk(o, end):
        while o < end:
            sig = d[o:o + 4]
            if sig == b'GRUP':
                g = struct.unpack_from('<I', d, o + 4)[0]; walk(o + 24, o + g); o += g
            else:
                sz, fl, fid = struct.unpack_from('<III', d, o + 4)
                body = d[o + 24:o + 24 + sz]
                if fl & 0x40000: body = zlib.decompress(body[4:])
                recs[fid] = dict(sig=sig, flags=fl & ~0x40000, fid=fid, hdr=d[o + 16:o + 24], body=body)
                o += 24 + sz
    walk(24 + hsz, len(d)); return dict(masters=masters, recs=recs)
def subs(body):
    out = []; q = 0; big = None
    while q + 6 <= len(body):
        s = body[q:q + 4]; n = struct.unpack_from('<H', body, q + 4)[0]
        if s == b'XXXX': big = struct.unpack_from('<I', body, q + 6)[0]; q += 6 + n; continue
        if big is not None: n = big; big = None
        out.append([s, bytearray(body[q + 6:q + 6 + n])]); q += 6 + n
    return out
def join(sl):
    b = bytearray()
    for s, v in sl:
        if len(v) > 0xFFFF: b += b'XXXX' + struct.pack('<HI', 4, len(v)) + s + struct.pack('<H', 0) + v
        else: b += s + struct.pack('<H', len(v)) + v
    return bytes(b)
def edid(sl):
    for s, v in sl:
        if s == b'EDID': return bytes(v).rstrip(b'\0').decode('cp1252')

esm = read_plugin(ESM111); esp = read_plugin(ESP111); old = read_plugin(ESM101)
OWN = len(esm['masters'])                         # esm-local FormIDs carry this high byte
MASTERS = esm['masters'] + [PICTA]
def local(fid24): return (OWN << 24) | fid24
log = []

# ---- WTHR -------------------------------------------------------------------------------------------------------------
G = {'A': (75, 125, 75, 75), 'B': (75, 125, 75, 75), 'C': (75, 100, 75, 75), 'D': (75, 75, 75, 75), 'E': (50, 50, 50, 50)}
FOGFAR_SKIP = {0x19FD02}
L27_ALPHA0 = {0x19FA03, 0x19FB03, 0x19FC03, 0x19FC04, 0x19FC05, 0x19FD02, 0x19FD03, 0x19FD04, 0x19FD05, 0x19FD06, 0x19FE03, 0x19FE04, 0x19FE05, 0x19FE06}
DALC_K = {0x19FA03: (.833, .805, .821, .787), 0x19FB03: (.782, .755, .775, .731), 0x19FC01: (.945, .851, .941, .907),
          0x19FC02: (.820, .744, .816, .760), 0x19FC03: (.720, .631, .714, .627), 0x19FC04: (.970, .948, .969, .946),
          0x19FC05: (.779, .704, .775, .727), 0x19FD01: (.906, .820, .898, .856), 0x19FD02: (.995, .950, 1.0, .977),
          0x19FD03: (.928, .906, .928, .919), 0x19FD04: (.928, .906, .928, .919), 0x19FD05: (.764, .689, .755, .697),
          0x19FD06: (.764, .689, .755, .697), 0x19FE01: (.844, .894, .842, .846), 0x19FE02: (.837, .888, .830, .769),
          0x19FE03: (.898, .939, .902, .887), 0x19FE04: (.898, .939, .902, .887), 0x19FE05: (.738, .757, .740, .752),
          0x19FE06: (.738, .757, .740, .752)}
DALC_SIDES_EXTRA = {0x19FD05: 0.80, 0x19FD06: 0.80}
MIST_FOG = {0x19FA03: (150000.0, 125000.0, 0.90), 0x19FB03: (150000.0, 125000.0, 0.90), 0x19FC03: (150000.0, 125000.0, 0.90)}
MAX_ONLY = {0x19FD02: 0.95}
VOLI_RELINK = {0x19FA03: (0x15A001, 0x15A002, 0x15A003, 0x15A004), 0x19FB03: (0x15A005, 0x15A006, 0x15A007, 0x15A008),
               0x19FC03: (0x15A009, 0x15A010, 0x15A011, 0x15A012)}
MASTER_IDS = [0x19FA01, 0x19FA02, 0x19FA03, 0x19FB01, 0x19FB02, 0x19FB03] + [0x19FC00 + i for i in range(1, 6)] + \
             [0x19FD00 + i for i in range(1, 7)] + [0x19FE00 + i for i in range(1, 7)]
out_recs = {'WTHR': [], 'CLMT': [], 'VOLI': []}
for f24 in MASTER_IDS:
    r = esm['recs'].get(local(f24)); assert r and r['sig'] == b'WTHR', 'missing WTHR %06X' % f24
    sl = subs(r['body']); ed = edid(sl); cat = ed.split('MASTER_')[1][0]
    assert ed.startswith('PIC_WTHR_MASTER_'), ed
    ch = []
    for s, v in sl:
        if s == b'NAM0':
            assert len(v) == 17 * 16, len(v)
            if f24 not in FOGFAR_SKIP:
                for t in range(4): v[12 * 16 + t * 4:12 * 16 + t * 4 + 3] = bytes([G[cat][t]] * 3)
                ch.append('FogFar')
            for ci in (0, 7, 8): v[ci * 16 + 3 * 4:ci * 16 + 3 * 4 + 3] = bytes([75] * 3)
            ch.append('night sky 75')
        elif s == b'PNAM':
            assert len(v) == 32 * 16, len(v)
            for layer in (27, 28):
                for t in range(4): v[layer * 16 + t * 4:layer * 16 + t * 4 + 3] = bytes([G[cat][t]] * 3)
            ch.append('cloud 27/28 colour')
        elif s == b'JNAM' and f24 in L27_ALPHA0:
            assert len(v) == 32 * 16, len(v)
            for t in range(4): struct.pack_into('<f', v, 27 * 16 + t * 4, 0.0)
            ch.append('cloud 27 alpha 0')
        elif s == b'FNAM' and (f24 in MIST_FOG or f24 in MAX_ONLY):
            dn, df, nn, nf, dp, np_, dm, nm = struct.unpack('<8f', v[:32])
            if f24 in MIST_FOG: df, nf, dm = MIST_FOG[f24][0], MIST_FOG[f24][1], MIST_FOG[f24][2]; nm = dm
            else: dm = nm = MAX_ONLY[f24]
            v[:32] = struct.pack('<8f', dn, df, nn, nf, dp, np_, dm, nm); ch.append('fog distances')
        elif s == b'HNAM' and f24 in VOLI_RELINK:
            assert len(v) == 16
            hb = struct.unpack_from('<I', v, 0)[0] >> 24
            v[:] = struct.pack('<4I', *[(hb << 24) | x for x in VOLI_RELINK[f24]]); ch.append('VOLI relink')
    dal = [v for s, v in sl if s == b'DALC']
    if f24 in DALC_K:
        assert len(dal) == 4
        for t, v in enumerate(dal):
            k = DALC_K[f24][t]
            for face in range(6):
                kk = k * (DALC_SIDES_EXTRA.get(f24, 1.0) if face < 4 else 1.0)
                for c in range(3): v[face * 4 + c] = max(0, min(255, int(round(v[face * 4 + c] * kk))))
        ch.append('DALC x k')
    out_recs['WTHR'].append((r, join(sl))); log.append('%06X %-40s %s' % (f24, ed, ', '.join(ch)))

# ---- CLMT -------------------------------------------------------------------------------------------------------------
cl = None
for fid, r in esp['recs'].items():
    if r['sig'] == b'CLMT' and (fid & 0xFFFFFF) == 0x000812 and esp['masters'][fid >> 24].lower() == 'skyrim.esm': cl = r
assert cl, 'CLMT 000812 not found in the 1.1.1 esp'
sl = subs(cl['body'])
for s, v in sl:
    if s == b'TNAM':
        assert bytes(v[:4]) == bytes([0x24, 0x30, 0x6C, 0x78]), bytes(v).hex()
        v[1] = 0x36; v[2] = 0x66
    elif s == b'WLST':
        for i in range(len(v) // 12):
            for off in (0, 8):
                x = struct.unpack_from('<I', v, i * 12 + off)[0]
                if x == 0: continue
                mname = esp['masters'][x >> 24] if (x >> 24) < len(esp['masters']) else os.path.basename(ESP111)
                assert mname in MASTERS, 'WLST references %s' % mname
                struct.pack_into('<I', v, i * 12 + off, (MASTERS.index(mname) << 24) | (x & 0xFFFFFF))
clmt_fid = (MASTERS.index('Skyrim.esm') << 24) | 0x000812
out_recs['CLMT'].append((dict(cl, fid=clmt_fid), join(sl))); log.append('000812 PIC_CLMT_Skyrim TNAM -> 24 36 66 78 (sunrise end 09:00, sunset begin 17:00); WLST remapped')

# ---- VOLI -------------------------------------------------------------------------------------------------------------
old_by_e = {}
for fid, r in old['recs'].items():
    if r['sig'] == b'VOLI': old_by_e[(fid & 0xFFFFFF, edid(subs(r['body'])))] = r
n_voli = 0
for fid, r in sorted(esm['recs'].items()):
    if r['sig'] != b'VOLI' or (fid >> 24) != OWN: continue
    e = edid(subs(r['body'])); o = old_by_e.get((fid & 0xFFFFFF, e))
    if not o: continue
    if o['body'] != r['body']: out_recs['VOLI'].append((r, o['body'])); n_voli += 1
log.append('VOLI copied verbatim from 1.0.1 (differing only): %d' % n_voli)
for l in log: print(l)

# ---- write ------------------------------------------------------------------------------------------------------------
def record(sig, flags, fid, body):
    return sig + struct.pack('<III', len(body), flags & ~0x40000, fid) + struct.pack('<HHHH', 0, 0, 44, 0) + body
def group(label, recs):
    data = b''.join(recs)
    return b'GRUP' + struct.pack('<I', 24 + len(data)) + label + struct.pack('<IHHI', 0, 0, 0, 0) + data
groups = b''; nrec = 0
for sig in ('WTHR', 'CLMT', 'VOLI'):
    if out_recs[sig]:
        groups += group(sig.encode(), [record(r['sig'], r['flags'], r['fid'], body) for r, body in out_recs[sig]]); nrec += len(out_recs[sig]) + 1
hdr = b'HEDR' + struct.pack('<HfiI', 12, 1.71, nrec, 0x800)
hdr += b'CNAM' + struct.pack('<H', 9) + b'Authoria\0'
desc = b'Picta 1.1.1 record brightness back to 1.0.1 (climate timing, VOLI, WTHR fog/sky/cloud/DALC/mist). 2026-10-12.\0'
hdr += b'SNAM' + struct.pack('<H', len(desc)) + desc
for m in MASTERS:
    mb = m.encode('cp1252') + b'\0'; hdr += b'MAST' + struct.pack('<H', len(mb)) + mb + b'DATA' + struct.pack('<HQ', 8, 0)
tes4 = b'TES4' + struct.pack('<III', len(hdr), 0x200, 0) + struct.pack('<HHHH', 0, 0, 44, 0) + hdr
plugin = tes4 + groups
print('plugin: %d bytes, masters %s, WTHR %d, CLMT %d, VOLI %d' % (len(plugin), MASTERS, len(out_recs['WTHR']), len(out_recs['CLMT']), len(out_recs['VOLI'])))
# self-check: re-read and compare a few values
chk_path = os.path.join(os.environ.get('TEMP', '.'), '_picta_patch_check.esp'); open(chk_path, 'wb').write(plugin)
re_ = read_plugin(chk_path); os.remove(chk_path)
assert re_['masters'] == MASTERS and len(re_['recs']) == sum(len(v) for v in out_recs.values())
d01 = subs(re_['recs'][local(0x19FD01)]['body']); dal = [v for s, v in d01 if s == b'DALC'][1]
print('check D01 Day DALC X+ / Z+ / Z-:', tuple(dal[0:3]), tuple(dal[16:19]), tuple(dal[20:23]), '(sweep example: sides (52,80,138))')
a01 = dict((bytes(s), bytes(v)) for s, v in subs(re_['recs'][local(0x19FA01)]['body']))
print('check A01 FogFar S/D/Ss/N:', [a01[b'NAM0'][12 * 16 + t * 4] for t in range(4)], ' night SkyUpper:', a01[b'NAM0'][0 * 16 + 12])
c = [r for r in re_['recs'].values() if r['sig'] == b'CLMT'][0]
print('check CLMT TNAM:', dict((bytes(s), bytes(v)) for s, v in subs(c['body']))[b'TNAM'].hex(' '))
if WRITE:
    tl = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    if 'modorganizer' in tl or 'skyrimse' in tl: sys.exit('MO2 or the game is running - aborting')
    os.makedirs(OUTDIR, exist_ok=True); open(os.path.join(OUTDIR, OUTNAME), 'wb').write(plugin)
    open(os.path.join(OUTDIR, 'meta.ini'), 'wb').write(('[General]\r\nmodid=0\r\nversion=1.0\r\ncomments=ESL override-only patch: Picta 1.1.1 record-side brightness back to 1.0.1 (climate sunrise/sunset timing, VOLI god-ray phase, MASTER weathers fog far / night sky / haze-band clouds / directional ambient / mist fog + VL links). Built 2026-10-12 by _tools\\picta-bridge\\picta_darken_records_patch.py from the verified brightness sweep. Plugin loads right after Authoria - Picta over NAT.esp.\r\nnotes=\r\n').encode('utf-8'))
    print('written:', os.path.join(OUTDIR, OUTNAME))
