"""FOMOD analysis helper.

Usage:
  python fomod_tool.py dump <archive_root>                    -> print steps/groups/options + file counts
  python fomod_tool.py match <archive_root> <installed_dir>   -> for each option, how many of its files match the installed folder (by hash)
  python fomod_tool.py json <archive_root> <out.json>         -> dump structure as JSON (options -> file map)
"""
import sys, os, json, hashlib
import xml.etree.ElementTree as ET


def norm(p):
    return p.replace('/', '\\').strip('\\').lower()


def lp(p):
    """Long-path-safe absolute path (\\?\ prefix)."""
    if p.startswith('\\\\?\\'):
        return p
    return '\\\\?\\' + os.path.abspath(p)


def hash_file(path):
    h = hashlib.sha256()
    with open(lp(path), 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def find_ci(root, rel):
    """Resolve rel (backslash path) under root case-insensitively. Returns abs path or None."""
    cur = root
    if rel == '':
        return root
    for part in rel.split('\\'):
        if part == '':
            continue
        try:
            entries = os.listdir(lp(cur))
        except (FileNotFoundError, NotADirectoryError):
            return None
        m = [e for e in entries if e.lower() == part.lower()]
        if not m:
            return None
        cur = os.path.join(cur, m[0])
    return cur


def files_of(root, files_el):
    """Return dict dest_rel_lower -> (src_abs, priority) for a <files> element."""
    out = {}
    if files_el is None:
        return out
    for el in files_el:
        src = el.get('source', '')
        dest = el.get('destination', '')
        prio = int(el.get('priority', '0') or 0)
        if el.tag == 'folder':
            base = find_ci(root, norm(src))
            if base is None or not os.path.isdir(lp(base)):
                out['<<MISSING FOLDER ' + src + '>>'] = (None, prio, src)
                continue
            lbase = lp(base)
            for dp, dn, fn in os.walk(lbase):
                for f in fn:
                    ap = os.path.join(dp, f)
                    rel = os.path.relpath(ap, lbase)
                    disp = os.path.join(dest, rel) if dest else rel
                    d = norm(disp)
                    out[d] = (ap, prio, disp)
        elif el.tag == 'file':
            ap = find_ci(root, norm(src))
            if ap is None or not os.path.isfile(lp(ap)):
                out['<<MISSING FILE ' + src + '>>'] = (None, prio, src)
                continue
            disp = dest if dest else os.path.basename(src)
            # if dest ends with a backslash or is a directory, put file inside
            if dest and (dest.endswith('\\') or dest.endswith('/')):
                disp = os.path.join(dest, os.path.basename(src))
            d = norm(disp)
            out[d] = (ap, prio, disp)
    return out


def parse(root):
    cfg = os.path.join(root, 'fomod', 'ModuleConfig.xml')
    tree = ET.parse(cfg)
    r = tree.getroot()
    res = {'name': r.findtext('moduleName'), 'required': {}, 'steps': [], 'conditional': []}
    req = r.find('requiredInstallFiles')
    res['required'] = files_of(root, req)
    steps = r.find('installSteps')
    if steps is not None:
        for st in steps.findall('installStep'):
            step = {'name': st.get('name'), 'groups': [], 'visible': None}
            vis = st.find('visible')
            if vis is not None:
                step['visible'] = ET.tostring(vis, encoding='unicode')
            ofg = st.find('optionalFileGroups')
            if ofg is not None:
                for g in ofg.findall('group'):
                    grp = {'name': g.get('name'), 'type': g.get('type'), 'plugins': []}
                    pl = g.find('plugins')
                    if pl is not None:
                        for p in pl.findall('plugin'):
                            opt = {'name': p.get('name'), 'files': files_of(root, p.find('files')), 'flags': {}, 'type': None}
                            cf = p.find('conditionFlags')
                            if cf is not None:
                                for fl in cf.findall('flag'):
                                    opt['flags'][fl.get('name')] = fl.text
                            td = p.find('typeDescriptor')
                            if td is not None:
                                t = td.find('type')
                                if t is not None:
                                    opt['type'] = t.get('name')
                                else:
                                    dt = td.find('dependencyType')
                                    if dt is not None:
                                        opt['type'] = 'dep:' + ET.tostring(dt, encoding='unicode')[:400]
                            grp['plugins'].append(opt)
                    step['groups'].append(grp)
            res['steps'].append(step)
    cfi = r.find('conditionalFileInstalls')
    if cfi is not None:
        pats = cfi.find('patterns')
        if pats is not None:
            for pat in pats.findall('pattern'):
                deps = pat.find('dependencies')
                res['conditional'].append({'deps': ET.tostring(deps, encoding='unicode') if deps is not None else '', 'files': files_of(root, pat.find('files'))})
    return res


def installed_index(inst):
    idx = {}
    linst = lp(inst)
    for dp, dn, fn in os.walk(linst):
        for f in fn:
            if f.lower() == 'meta.ini':
                continue
            ap = os.path.join(dp, f)
            rel = norm(os.path.relpath(ap, linst))
            idx[rel] = ap
    return idx


_hash_cache = {}


def h(p):
    if p not in _hash_cache:
        _hash_cache[p] = hash_file(p)
    return _hash_cache[p]


def match_files(fmap, idx):
    total = 0
    same = 0
    present_diff = 0
    missing = 0
    details = []
    for dest, (src, prio, disp) in fmap.items():
        if src is None:
            details.append(('MISSING-SRC', dest))
            continue
        total += 1
        if dest in idx:
            if h(idx[dest]) == h(src):
                same += 1
                details.append(('SAME', dest))
            else:
                present_diff += 1
                details.append(('DIFF', dest))
        else:
            missing += 1
            details.append(('ABSENT', dest))
    return total, same, present_diff, missing, details


def cmd_dump(root):
    res = parse(root)
    print('MODULE:', res['name'])
    print('REQUIRED files:', len(res['required']))
    for st in res['steps']:
        print('STEP:', st['name'], ('[visible cond]' if st['visible'] else ''))
        for g in st['groups']:
            print('  GROUP:', g['name'], '(', g['type'], ')')
            for p in g['plugins']:
                print('    OPTION:', p['name'], '| files:', len(p['files']), '| flags:', p['flags'], '| type:', p['type'])
    print('CONDITIONAL patterns:', len(res['conditional']))
    for c in res['conditional']:
        print('  PATTERN files:', len(c['files']), 'deps:', c['deps'][:300].replace('\n', ' '))


def cmd_match(root, inst, verbose=False):
    res = parse(root)
    idx = installed_index(inst)
    print('MODULE:', res['name'], '| installed files:', len(idx))
    t, s, d, m, det = match_files(res['required'], idx)
    print('REQUIRED: total=%d same=%d diff=%d absent=%d' % (t, s, d, m))
    if verbose:
        for k, v in det:
            if k != 'SAME':
                print('      ', k, v)
    for st in res['steps']:
        print('STEP:', st['name'])
        for g in st['groups']:
            print('  GROUP:', g['name'], '(', g['type'], ')')
            for p in g['plugins']:
                t, s, d, m, det = match_files(p['files'], idx)
                tag = ''
                if t > 0 and s == t:
                    tag = 'ALL-SAME'
                elif s > 0:
                    tag = 'PARTIAL'
                elif t > 0 and d > 0 and m == 0:
                    tag = 'ALL-PRESENT-DIFF'
                elif t == 0:
                    tag = 'NO-FILES'
                else:
                    tag = 'none'
                print('    OPTION: %-70s total=%3d same=%3d diff=%3d absent=%3d  %s  flags=%s' % (p['name'][:70], t, s, d, m, tag, p['flags'] if p['flags'] else ''))
                if verbose and tag in ('PARTIAL', 'ALL-PRESENT-DIFF'):
                    for k, v in det:
                        if k != 'SAME':
                            print('          ', k, v)
    for i, c in enumerate(res['conditional']):
        t, s, d, m, det = match_files(c['files'], idx)
        print('CONDITIONAL[%d]: total=%d same=%d diff=%d absent=%d deps=%s' % (i, t, s, d, m, c['deps'][:200].replace('\n', ' ')))
    # files in installed folder not provided by ANY option/required/conditional
    provided = set(res['required'].keys())
    for st in res['steps']:
        for g in st['groups']:
            for p in g['plugins']:
                provided |= set(p['files'].keys())
    for c in res['conditional']:
        provided |= set(c['files'].keys())
    extra = [k for k in idx if k not in provided]
    print('INSTALLED FILES NOT PROVIDED BY THIS ARCHIVE:', len(extra))
    for e in sorted(extra)[:200]:
        print('    ', e)


def all_options(res):
    """Yield (label, files) for required, every option, every conditional pattern."""
    yield ('REQUIRED', res['required'])
    for si, st in enumerate(res['steps']):
        for g in st['groups']:
            for p in g['plugins']:
                yield ('S%d %s / %s / %s' % (si, st['name'].strip(), g['name'].strip(), p['name'].strip()), p['files'])
    for i, c in enumerate(res['conditional']):
        yield ('COND[%d]' % i, c['files'])


def cmd_providers(root, inst, show_files=False):
    res = parse(root)
    idx = installed_index(inst)
    print('MODULE:', res['name'], '| installed files:', len(idx))
    # per installed file: providers
    prov = {k: {'same': [], 'diff': []} for k in idx}
    opt_stats = {}
    for label, fmap in all_options(res):
        opt_stats[label] = {'total': 0, 'same': 0, 'diff': 0, 'absent': 0, 'unique_same': 0}
        for dest, (src, prio, disp) in fmap.items():
            if src is None:
                continue
            opt_stats[label]['total'] += 1
            if dest in idx:
                if h(idx[dest]) == h(src):
                    prov[dest]['same'].append(label)
                    opt_stats[label]['same'] += 1
                else:
                    prov[dest]['diff'].append(label)
                    opt_stats[label]['diff'] += 1
            else:
                opt_stats[label]['absent'] += 1
    for dest, pr in prov.items():
        if len(pr['same']) == 1:
            opt_stats[pr['same'][0]]['unique_same'] += 1
    print('\n== PER-OPTION SUMMARY (unique_same = files only THIS option provides identically) ==')
    for label, s in opt_stats.items():
        if s['total'] == 0:
            continue
        verdict = ''
        if s['same'] == s['total'] and s['unique_same'] > 0:
            verdict = 'SELECTED (unique evidence)'
        elif s['same'] == s['total']:
            verdict = 'all files present but shared with other options'
        elif s['same'] > 0:
            verdict = 'partial'
        elif s['absent'] == s['total']:
            verdict = 'NOT selected (all absent)'
        elif s['diff'] > 0 and s['same'] == 0:
            verdict = 'NOT selected (paths present, other content)'
        print('%-95s total=%3d same=%3d uniq=%3d diff=%3d absent=%3d  %s' % (label[:95], s['total'], s['same'], s['unique_same'], s['diff'], s['absent'], verdict))
    orphans = [d for d, pr in prov.items() if not pr['same']]
    print('\n== INSTALLED FILES WITH NO IDENTICAL PROVIDER IN THIS ARCHIVE:', len(orphans), '==')
    for d in sorted(orphans):
        print('   ', d, '| diff-providers:', '; '.join(prov[d]['diff'])[:300] if prov[d]['diff'] else '(path not in archive)')
    if show_files:
        print('\n== PER-FILE PROVIDERS (files with >1 same-provider or none) ==')
        for d in sorted(prov):
            pr = prov[d]
            if len(pr['same']) != 1:
                print('   ', d)
                print('        same:', pr['same'])
                print('        diff:', pr['diff'])


def simulate(root, choices, flags_extra=None):
    """Return dest -> (src, priority, label) applying FOMOD override rules:
    highest priority wins; ties -> later in traversal order wins.
    choices: set of option labels (as printed by all_options) that are selected.
    Conditional patterns are applied if their flag deps are satisfied by selected options' flags."""
    res = parse(root)
    flags = dict(flags_extra or {})
    selected = []
    for label, fmap in all_options(res):
        if label == 'REQUIRED':
            selected.append((label, fmap))
    # gather flags of selected options
    for si, st in enumerate(res['steps']):
        for g in st['groups']:
            for p in g['plugins']:
                label = 'S%d %s / %s / %s' % (si, st['name'].strip(), g['name'].strip(), p['name'].strip())
                if label in choices:
                    selected.append((label, p['files']))
                    flags.update(p['flags'])
    # conditional patterns
    cfg = os.path.join(root, 'fomod', 'ModuleConfig.xml')
    r = ET.parse(cfg).getroot()
    cfi = r.find('conditionalFileInstalls')
    if cfi is not None:
        pats = cfi.find('patterns')
        if pats is not None:
            for i, pat in enumerate(pats.findall('pattern')):
                deps = pat.find('dependencies')
                ok = eval_deps(deps, flags)
                if ok:
                    selected.append(('COND[%d]' % i, files_of(root, pat.find('files'))))
    out = {}
    order = 0
    for label, fmap in selected:
        for dest, (src, prio, disp) in fmap.items():
            if src is None:
                continue
            order += 1
            cur = out.get(dest)
            if cur is None or prio >= cur[1]:
                out[dest] = (src, prio, label, order, disp)
    return out, flags


def eval_deps(deps, flags):
    if deps is None:
        return True
    op = deps.get('operator', 'And')
    results = []
    for child in deps:
        if child.tag == 'flagDependency':
            results.append(flags.get(child.get('flag')) == child.get('value'))
        elif child.tag == 'dependencies':
            results.append(eval_deps(child, flags))
        elif child.tag == 'fileDependency':
            results.append(True)  # cannot evaluate; assume satisfied (report)
        else:
            results.append(True)
    if not results:
        return True
    return all(results) if op == 'And' else any(results)


def load_choices(path):
    with open(path, 'r', encoding='utf-8') as f:
        return set(l.rstrip('\n') for l in f if l.strip() and not l.startswith('#'))


def cmd_simulate(root, choices_path, inst=None, outdir=None):
    choices = load_choices(choices_path)
    res = parse(root)
    known = set(label for label, _ in all_options(res))
    for c in choices:
        if c not in known:
            print('!! UNKNOWN CHOICE LABEL:', c)
    out, flags = simulate(root, choices)
    print('SIMULATED install: %d files; flags=%s' % (len(out), flags))
    if inst:
        idx = installed_index(inst)
        only_sim = sorted(set(out) - set(idx))
        only_inst = sorted(set(idx) - set(out))
        differ = sorted(d for d in set(out) & set(idx) if h(out[d][0]) != h(idx[d]))
        print('COMPARE vs installed (%d files): only-in-sim=%d only-in-installed=%d content-differ=%d' % (len(idx), len(only_sim), len(only_inst), len(differ)))
        for d in only_sim:
            print('   ONLY-SIM  ', d, '<-', out[d][2])
        for d in only_inst:
            print('   ONLY-INST ', d)
        for d in differ:
            print('   DIFFER    ', d, '<- sim from', out[d][2])
        if not only_sim and not only_inst and not differ:
            print('EXACT MATCH')
    if outdir:
        import shutil
        n = 0
        for dest, (src, prio, label, order, disp) in out.items():
            dp = os.path.join(outdir, disp.replace('/', '\\').strip('\\'))
            os.makedirs(lp(os.path.dirname(dp)), exist_ok=True)
            shutil.copy2(lp(src), lp(dp))
            n += 1
        print('WROTE %d files to %s' % (n, outdir))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'dump':
        cmd_dump(sys.argv[2])
    elif cmd == 'simulate':
        # simulate <root> <choices.txt> [--inst <dir>] [--out <dir>]
        inst = None
        outdir = None
        if '--inst' in sys.argv:
            inst = sys.argv[sys.argv.index('--inst') + 1]
        if '--out' in sys.argv:
            outdir = sys.argv[sys.argv.index('--out') + 1]
        cmd_simulate(sys.argv[2], sys.argv[3], inst, outdir)
    elif cmd == 'providers':
        cmd_providers(sys.argv[2], sys.argv[3], show_files=('-v' in sys.argv))
    elif cmd == 'match':
        cmd_match(sys.argv[2], sys.argv[3], verbose=('-v' in sys.argv))
    elif cmd == 'json':
        res = parse(sys.argv[2])
        with open(sys.argv[3], 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=1)
        print('written', sys.argv[3])
