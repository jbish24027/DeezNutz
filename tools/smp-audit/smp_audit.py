"""Audit: SMP meshes buried by static copies (loose-vs-loose), across every ENABLED
mod of the active MO2 profile, plus the overwrite folder.

Output: smp_audit_result.json + printed summary.
"""
import os, sys, json, struct, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

INSTANCE = r"C:\1. AUTHORIA"
PROFILE = "DEEZ CS NUTZ"
MODS = os.path.join(INSTANCE, "mods")
OVERWRITE = os.path.join(INSTANCE, "overwrite")
HDT_TAG = b"HDT Skinned Mesh Physics Object"

def enabled_mods():
    """Return enabled mod folder names, HIGHEST priority first (modlist.txt line order)."""
    out = []
    with open(os.path.join(INSTANCE, "profiles", PROFILE, "modlist.txt"), encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if not line or line.startswith("#"):
                continue
            if line.startswith("+"):
                name = line[1:]
                if name.endswith("_separator"):
                    continue
                out.append(name)
    return out

def walk_files(root):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            ext = f.lower().rsplit('.', 1)[-1] if '.' in f else ''
            if ext in ('nif', 'xml'):
                full = os.path.join(dp, f)
                rel = os.path.relpath(full, root).replace('/', '\\').lower()
                yield rel, full

def smp_info(path):
    """Parse the nif header + NiStringExtraData blocks. Returns (is_smp, [xml paths], error)."""
    try:
        with open(path, 'rb') as fh:
            data = fh.read()
    except OSError as e:
        return None, [], str(e)
    if not data.startswith(b"Gamebryo File Format") and not data.startswith(b"NetImmerse File Format"):
        return None, [], 'not a nif'
    if HDT_TAG not in data:
        return False, [], None
    # full header parse to confirm a NiStringExtraData block actually carries the tag
    try:
        pos = data.index(b'\n') + 1
        version, = struct.unpack_from('<I', data, pos); pos += 4
        pos += 1
        pos += 4  # user version
        num_blocks, = struct.unpack_from('<I', data, pos); pos += 4
        bs_ver, = struct.unpack_from('<I', data, pos); pos += 4
        for _ in range(3):
            n = data[pos]; pos += 1 + n
        if bs_ver == 130:
            n = data[pos]; pos += 1 + n
        num_types, = struct.unpack_from('<H', data, pos); pos += 2
        types = []
        for _ in range(num_types):
            n, = struct.unpack_from('<I', data, pos); pos += 4
            types.append(data[pos:pos+n].decode('latin1')); pos += n
        type_idx = struct.unpack_from('<%dH' % num_blocks, data, pos); pos += 2*num_blocks
        sizes = struct.unpack_from('<%dI' % num_blocks, data, pos); pos += 4*num_blocks
        num_strings, = struct.unpack_from('<I', data, pos); pos += 4
        pos += 4
        strings = []
        for _ in range(num_strings):
            n, = struct.unpack_from('<I', data, pos); pos += 4
            strings.append(data[pos:pos+n].decode('latin1')); pos += n
        num_groups, = struct.unpack_from('<I', data, pos); pos += 4
        pos += 4*num_groups
        xmls = []
        is_smp = False
        for i in range(num_blocks):
            t = types[type_idx[i] & 0x7FFF]
            if t == 'NiStringExtraData':
                name_i, str_i = struct.unpack_from('<II', data, pos)
                name = strings[name_i] if name_i != 0xFFFFFFFF else ''
                val = strings[str_i] if str_i != 0xFFFFFFFF else ''
                if name == 'HDT Skinned Mesh Physics Object':
                    is_smp = True
                    xmls.append(val)
            pos += sizes[i]
        return is_smp, xmls, None
    except Exception as e:
        # tag present but header unparseable: treat as SMP-tagged (conservative) and flag
        return True, [], 'parse error: %s' % e

def main():
    t0 = time.time()
    mods = enabled_mods()
    print('enabled mods: %d' % len(mods))
    providers = {}   # rel path -> list of (prio, modname, fullpath) ; prio 0 = highest
    sources = [('overwrite', OVERWRITE)] + [(m, os.path.join(MODS, m)) for m in mods]
    missing = []
    for prio, (name, root) in enumerate(sources):
        if not os.path.isdir(root):
            missing.append(name); continue
        for rel, full in walk_files(root):
            providers.setdefault(rel, []).append((prio, name, full))
    print('walked %d sources in %.0fs; %d distinct nif/xml paths; missing folders: %d' % (len(sources), time.time()-t0, len(providers), len(missing)))
    nifs = {k: v for k, v in providers.items() if k.endswith('.nif')}
    xmls = {k: v for k, v in providers.items() if k.endswith('.xml')}
    contended = {k: v for k, v in nifs.items() if len(v) >= 2}
    print('nif paths: %d, contended (2+ loose providers): %d' % (len(nifs), len(contended)))
    buried = []      # winner static, lower provider SMP
    smp_winners = []  # winner SMP (for xml check)
    errors = []
    n_checked = 0
    for rel, provs in contended.items():
        provs = sorted(provs)
        infos = []
        for prio, name, full in provs:
            is_smp, xl, err = smp_info(full)
            if err and is_smp is None:
                errors.append((rel, name, err)); infos.append((prio, name, None, xl)); continue
            infos.append((prio, name, is_smp, xl))
        n_checked += 1
        win = infos[0]
        lower_smp = [x for x in infos[1:] if x[2]]
        if win[2] is False and lower_smp:
            buried.append({'path': rel, 'winner': win[1], 'smp_providers': [x[1] for x in lower_smp], 'all': [(x[1], x[2]) for x in infos]})
        if win[2]:
            smp_winners.append((rel, win[1], win[3]))
    print('checked %d contended paths in %.0fs' % (n_checked, time.time()-t0))
    # xml existence check for SMP winners (loose providers only; note BSAs not covered)
    missing_xml = []
    for rel, winner, xl in smp_winners:
        for x in xl:
            key = x.replace('/', '\\').lower().lstrip('\\')
            if key.startswith('data\\'):
                key = key[5:]
            if key not in xmls:
                missing_xml.append({'path': rel, 'winner': winner, 'xml': x})
    result = {'enabled_mods': len(mods), 'nif_paths': len(nifs), 'contended': len(contended), 'buried': buried,
              'smp_winners_contended': len(smp_winners), 'missing_xml_among_contended_smp_winners': missing_xml, 'errors': errors[:50], 'n_errors': len(errors)}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smp_audit_result.json'), 'w', encoding='utf-8') as fh:
        json.dump(result, fh, indent=1)
    # summary
    print('\n=== BURIED SMP MESHES (winner static, an SMP copy exists lower): %d' % len(buried))
    by_winner = {}
    for b in buried:
        by_winner.setdefault(b['winner'], []).append(b)
    for w, items in sorted(by_winner.items(), key=lambda kv: -len(kv[1])):
        print('\n[%s] buries %d:' % (w, len(items)))
        for b in items:
            print('   %s   <- SMP in: %s' % (b['path'], ', '.join(b['smp_providers'])))
    print('\n=== contended SMP winners whose xml is not provided loose: %d' % len(missing_xml))
    for m in missing_xml[:40]:
        print('   %s (winner %s) -> %s' % (m['path'], m['winner'], m['xml']))
    print('\nerrors: %d' % len(errors))
    for e in errors[:10]:
        print('   ', e)
    # also dump the provider map for nifs in output-ish mods for the BSA follow-up
    outputs = [m for m in mods if 'output' in m.lower() or 'bodyslide' in m.lower()]
    print('\noutput-like mods: %s' % outputs)

if __name__ == '__main__':
    main()
