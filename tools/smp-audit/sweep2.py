"""Full sweep: (1) every loose nif WINNER's SMP status + xml existence (loose or BSA);
(2) UBE twins: meshes\!ube\<rest> winner vs meshes\<rest> winner SMP status.
Writes sweep2_result.json and prints a summary. Read-only."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smp_audit import enabled_mods, walk_files, smp_info, INSTANCE, MODS, OVERWRITE, PROFILE
from bsa_audit import read_bsa_index, extract, smp_of_bytes, VANILLA_PREFIX

def norm(x):
    k = x.replace('/', '\\').lower().lstrip('\\')
    return k[5:] if k.startswith('data\\') else k

def main():
    t0 = time.time()
    mods = enabled_mods()
    providers = {}
    sources = [('overwrite', OVERWRITE)] + [(m, os.path.join(MODS, m)) for m in mods]
    for prio, (name, root) in enumerate(sources):
        for rel, full in walk_files(root):
            providers.setdefault(rel, []).append((prio, name, full))
    loose_nif = {k: sorted(v)[0] for k, v in providers.items() if k.endswith('.nif')}
    loose_xml = {k for k in providers if k.endswith('.xml')}
    # BSA index (for xml existence + UBE twin sources)
    with open(os.path.join(INSTANCE, 'profiles', PROFILE, 'archives.txt'), encoding='utf-8') as fh:
        archives = [l.strip() for l in fh if l.strip()]
    bsa_files = {}
    for prio, (name, root) in enumerate(sources):
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if f.lower().endswith('.bsa'):
                    bsa_files.setdefault(f.lower(), []).append((prio, name, os.path.join(dp, f)))
    bsa_nifs = {}; bsa_xmls = set()
    for i, a in enumerate(archives):
        al = a.lower()
        if al.startswith(VANILLA_PREFIX) or al not in bsa_files:
            continue
        prio, name, path = sorted(bsa_files[al])[0]
        idx, err = read_bsa_index(path)
        if err: continue
        for rel, meta in idx.items():
            if rel.endswith('.nif'):
                bsa_nifs.setdefault(rel, []).append((i, a, name, path, meta))
            elif rel.endswith('.xml'):
                bsa_xmls.add(rel)
    print('indexed: %d loose nif winners, %d bsa nif paths (%.0fs)' % (len(loose_nif), len(bsa_nifs), time.time()-t0), flush=True)
    # (1) sweep all loose winners
    smp_winners = {}
    errors = 0
    for n, (rel, (prio, mod, full)) in enumerate(loose_nif.items()):
        s, x, e = smp_info(full)
        if s:
            smp_winners[rel] = (mod, x)
        if e and s is None:
            errors += 1
        if n % 10000 == 0:
            print('  ... %d/%d (%.0fs)' % (n, len(loose_nif), time.time()-t0), flush=True)
    print('loose SMP winners: %d (errors %d) (%.0fs)' % (len(smp_winners), errors, time.time()-t0), flush=True)
    missing_xml = []
    for rel, (mod, xl) in smp_winners.items():
        for x in xl:
            k = norm(x)
            if k not in loose_xml and k not in bsa_xmls:
                missing_xml.append({'path': rel, 'winner': mod, 'xml': x})
    # (2) UBE twins
    twins = []
    for rel, (prio, mod, full) in loose_nif.items():
        if not rel.startswith('meshes\\!ube\\'):
            continue
        src = 'meshes\\' + rel[len('meshes\\!ube\\'):]
        ube_smp = rel in smp_winners
        if src in loose_nif:
            src_smp = src in smp_winners; src_where = loose_nif[src][1]
        elif src in bsa_nifs:
            copies = sorted(bsa_nifs[src], key=lambda x: x[0]); i, a, m2, p2, meta = copies[-1]
            try:
                src_smp, _ = smp_of_bytes(extract(p2, meta)); src_where = a
            except Exception:
                continue
        else:
            continue
        if src_smp and not ube_smp:
            twins.append({'ube_path': rel, 'ube_winner': mod, 'source': src, 'source_where': src_where})
    res = {'loose_smp_winners': len(smp_winners), 'missing_xml': missing_xml, 'ube_twins_lost_smp': twins,
           'smp_winner_mods': sorted({v[0] for v in smp_winners.values()})}
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sweep2_result.json'), 'w'), indent=1)
    print('\n=== SMP winners whose xml exists nowhere (loose or BSA): %d' % len(missing_xml))
    byx = {}
    for m in missing_xml:
        byx.setdefault((m['winner'], m['xml']), []).append(m['path'])
    for (w, x), paths in sorted(byx.items()):
        print('   [%s] -> %s   (%d meshes, e.g. %s)' % (w, x, len(paths), paths[0]))
    print('\n=== UBE twins that lost SMP (source SMP, !UBE copy static): %d' % len(twins))
    byw = {}
    for t in twins:
        byw.setdefault(t['ube_winner'], []).append(t)
    for w, items in sorted(byw.items(), key=lambda kv: -len(kv[1])):
        print('\n[%s] %d:' % (w, len(items)))
        for t in items[:80]:
            print('   %s   (source %s in %s)' % (t['ube_path'], t['source'], t['source_where']))
        if len(items) > 80: print('   ... %d more' % (len(items)-80))
    print('done %.0fs' % (time.time()-t0))

if __name__ == '__main__':
    main()
