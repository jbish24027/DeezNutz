"""One command per round, for any design built with build_skirt_rig.py: build, verify, stride check, render, a diff of the
stage against the installed mod and (optionally) the install - ONE summary table plus <work>/STATE.md and state.json. The
checks live in here so no round can skip them.

  python rebuild.py <design.py ...> [target ...] [--install[=label]] [--xml-only] [--skip-build] [--no-render] [--no-stride]
                    [--mod=<installed mod folder>] [--bodies=f,gb]

Steps: builds (one process per design, in parallel) -> verify_rig.py per design -> stride_check.py and pose_render.py per
target (parallel) -> every file in the stage compared with the installed mod (NEW / CHG) and attributed to the design that
wrote it (from <work>/<name>_report.json) -> with --install: the files of every design that built, verified ALL OK and owns
no foreign change are copied in, after a backup of every replaced file.
--xml-only: a tuning round. Refuses when any staged mesh / osd / osp differs from the installed one (that is a mesh round and
needs a relaunch); otherwise installs the XMLs alone and tells the user `smp reset`.
Install target: the design's `install` key (absolute path of the mod folder) or --mod=. Backups: the design's `backups` key,
else <work>/backups/ - never inside the mods tree. Optional design key `items` = ['<FormID> <comment>', ...] writes
<work>/<name>_console.txt with player.additem / equipitem lines + smp reset (drop it in the game folder, run `bat <file>`).
Run it with the same Python the builder uses (numpy; opencv only for the renders)."""
import os, sys, re, json, time, subprocess, datetime, filecmp, shutil
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE)
import smpkit
PY = sys.executable
POOL = 6


def norm(p): return p.replace(os.sep, '/').replace(chr(92), '/')


def run_all(jobs, parallel=True):
    """jobs: {key: (argv, cwd, logfile)} -> {key: exit code}; up to POOL at once"""
    out, procs, keys, i = {}, {}, list(jobs), 0
    while i < len(keys) or procs:
        while i < len(keys) and (len(procs) < POOL if parallel else not procs):
            k = keys[i]; argv, cwd, logf = jobs[k]; i += 1
            os.makedirs(os.path.dirname(logf), exist_ok=True)
            procs[k] = (subprocess.Popen([PY] + argv, cwd=cwd, stdout=open(logf, 'w', encoding='utf-8'), stderr=subprocess.STDOUT), logf)
        for k, (p, logf) in list(procs.items()):
            if p.poll() is not None:
                out[k] = p.returncode; procs.pop(k)
                with open(logf, 'a', encoding='utf-8') as f: f.write(f'\nEXIT {p.returncode}\n')
        time.sleep(0.2)
    return out


def rd(f): return open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''


def build_summary(text, g):
    """per-target numbers from the build log (lines start with '<target>:')"""
    s = dict(error='Traceback' in text)
    m = re.findall(r'bones per shape \{[^}]*\}', text); s['bones'] = max((int(x) for b in m for x in re.findall(r': (\d+)', b)), default=None)
    sec = '\n'.join(l for l in text.splitlines() if l.startswith(f'{g}:') or l.startswith(f'{g}_'))
    m = re.search(r'lining to the trousers at rest: p10 ([-\d.]+) median ([-\d.]+); free share p10 ([-\d.]+) median ([-\d.]+)', sec)
    s['lining'] = (m.group(1), m.group(2)) if m else None; s['free'] = (m.group(3), m.group(4)) if m else None
    m = re.search(r'legs collider pulled in at (\d+) of (\d+) pts \(max ([\d.]+)\)', sec); s['pullin'] = (m.group(1), m.group(3)) if m else None
    m = re.search(r'(\d+) thigh leashes', sec); s['leashes'] = int(m.group(1)) if m else 0
    return s


def verify_summary(text):
    fails = [l.strip() for l in text.splitlines() if l.startswith('  FAIL')]
    return dict(ok=text.count('  ok   '), fail=len(fails), fails=fails,
                verdict='ALL OK' if 'ALL OK' in text else ('ERR' if 'Traceback' in text else ('CHECK' if text else 'none')))


def stride_summary(text):
    if 'Traceback' in text: return 'ERR'
    m = re.search(r'total caught/hooked/sunk (\d+)/(\d+)/(\d+)', text)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def fmt(v):
    if v is None: return '-'
    if isinstance(v, (list, tuple)): return '/'.join(str(x) for x in v)
    return str(v)


def owned_files(d, targets):
    """{relative stage path: target} of everything this design writes, from its report (+ the osp copy of a BodySlide set)"""
    rep = json.load(open(d['work'] + f'{d["name"]}_report.json')) if os.path.exists(d['work'] + f'{d["name"]}_report.json') else {}
    own = {}
    for g in targets:
        cfg = d['targets'][g]; r = rep.get(g, {})
        own[norm(cfg['xml'])] = g
        for o in r.get('outs', []):
            rel = os.path.relpath(norm(o), d['stage']).replace(os.sep, '/'); own[rel] = g
            if cfg['mode'] == 'bodyslide': own[rel[:-4] + '.osd'] = g
        if cfg['mode'] == 'bodyslide': own['CalienteTools/BodySlide/SliderSets/' + os.path.basename(norm(cfg['osp']))] = g
    return own


def stage_diff(stage, mod):
    ch = []
    for root, _, files in os.walk(stage):
        for f in files:
            s = os.path.join(root, f); rel = os.path.relpath(s, stage).replace(os.sep, '/'); t = mod + rel
            if not os.path.exists(t): ch.append((rel, 'NEW'))
            elif not filecmp.cmp(s, t, shallow=False): ch.append((rel, 'CHG'))
    return ch


def install(stage, mod, changes, bk):
    os.makedirs(bk, exist_ok=True); nb = ni = bad = 0
    for rel, kind in changes:
        s = stage + rel; t = mod + rel
        if kind == 'CHG':
            b = bk + rel; os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copy2(t, b); nb += 1
        os.makedirs(os.path.dirname(t), exist_ok=True); shutil.copy2(s, t); ni += 1
        if not filecmp.cmp(s, t, shallow=False): bad += 1
    with open(bk + 'CHANGED_FILES.txt', 'a', encoding='utf-8') as f: f.write(''.join(f'{k}|{r}\n' for r, k in changes))
    return nb, ni, bad


def console_file(d):
    items = d.get('items')
    if not items: return None
    p = d['work'] + f'{d["name"]}_console.txt'
    with open(p, 'w', encoding='utf-8') as f:
        for it in items:
            fid = str(it).split()[0]
            f.write(f'player.additem {fid} 1\nplayer.equipitem {fid}\n')
        f.write('smp reset\n')
    return p


def main(argv):
    paths = [a for a in argv if a.lower().endswith('.py')]
    if not paths: print(__doc__); return 1
    inst_arg = next((a for a in argv if a.startswith('--install')), None)
    label = inst_arg.split('=', 1)[1] if inst_arg and '=' in inst_arg else datetime.datetime.now().strftime('%H%M')
    xml_only = '--xml-only' in argv; skip_build = '--skip-build' in argv
    do_render = '--no-render' not in argv; do_stride = '--no-stride' not in argv
    mod_arg = next((norm(a.split('=', 1)[1]) for a in argv if a.startswith('--mod=')), None)
    bodies = next((a.split('=', 1)[1].split(',') for a in argv if a.startswith('--bodies=')), None)
    free = [a for a in argv if not a.startswith('--') and not a.lower().endswith('.py')]
    designs = {}
    for p in paths:
        d = smpkit.load_design(p); d['path'] = os.path.abspath(p)
        tg = [g for g in (bodies or free or list(d['targets'])) if g in d['targets']] or list(d['targets'])
        d['run_targets'] = tg; designs[d['name']] = d
    t0 = time.time(); st = {n: {} for n in designs}
    logs = {n: d['work'] + 'logs/' for n, d in designs.items()}
    # ---- build
    if not skip_build:
        rc = run_all({n: ([HERE + 'build_skirt_rig.py', d['path']] + d['run_targets'], d['work'], logs[n] + f'{n}_build.log') for n, d in designs.items()})
    for n, d in designs.items():
        text = rd(logs[n] + f'{n}_build.log')
        st[n]['build'] = {g: build_summary(text, g) for g in d['run_targets']}
        st[n]['build_err'] = 'Traceback' in text or (not skip_build and rc[n] != 0) or not text
    ok_b = [n for n in designs if not st[n]['build_err']]
    # ---- verify + stride + render
    run_all({n: ([HERE + 'verify_rig.py', designs[n]['path']] + designs[n]['run_targets'], designs[n]['work'], logs[n] + f'{n}_verify.log') for n in ok_b})
    for n in ok_b: st[n]['verify'] = verify_summary(rd(logs[n] + f'{n}_verify.log'))
    jobs = {}
    for n in ok_b:
        for g in designs[n]['run_targets']:
            if do_stride: jobs[(n, g, 'stride')] = ([HERE + 'stride_check.py', designs[n]['path'], g], designs[n]['work'], logs[n] + f'{n}_{g}_stride.log')
            if do_render: jobs[(n, g, 'render')] = ([HERE + 'pose_render.py', designs[n]['path'], g], designs[n]['work'], logs[n] + f'{n}_{g}_render.log')
    rcj = run_all(jobs)
    for (n, g, k), r in rcj.items():
        text = rd(logs[n] + f'{n}_{g}_{k}.log')
        if k == 'stride': st[n].setdefault('stride', {})[g] = stride_summary(text)
        else: st[n].setdefault('render', {})[g] = designs[n]['work'] + f'{n}_{g}_pose.png' if r == 0 and 'wrote' in text else 'FAILED (see log; needs opencv)'
    # ---- stage vs installed mod
    for n, d in designs.items():
        mod = mod_arg or d.get('install'); st[n]['mod'] = norm(mod).rstrip('/') + '/' if mod else None
        if not st[n]['mod'] or not os.path.isdir(st[n]['mod']): st[n]['changes'] = None; continue
        own = owned_files(d, d['run_targets']); ch = stage_diff(d['stage'], st[n]['mod'])
        st[n]['changes'] = [(rel, k) for rel, k in ch if rel in own]
        st[n]['foreign'] = [(rel, k) for rel, k in ch if rel not in own]
    # ---- install
    if inst_arg:
        for n, d in designs.items():
            s = st[n]
            if s['changes'] is None: print(f'{n}: NOT installed - no install folder (design key install= or --mod=)'); continue
            if n not in ok_b or s['verify']['verdict'] != 'ALL OK': print(f'{n}: NOT installed - build error or verify not ALL OK'); continue
            if s['foreign']: print(f'{n}: NOT installed - {len(s["foreign"])} changed stage files belong to other designs / targets: ' + ', '.join(r for r, k in s['foreign'][:8])); continue
            todo = s['changes']
            if xml_only:
                mesh = [r for r, k in todo if not r.lower().endswith('.xml')]
                if mesh: print(f'{n}: NOT installed - --xml-only but these staged files differ from the installed ones (a mesh round, relaunch needed): ' + ', '.join(mesh[:8])); continue
            if not todo: print(f'{n}: nothing to install - the stage equals the installed mod'); continue
            bk = norm(d.get('backups') or d['work'] + 'backups/').rstrip('/') + f'/{n}-{label}-{datetime.datetime.now():%Y%m%d}/'
            nb, ni, bad = install(d['stage'], s['mod'], todo, bk)
            s['installed'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M'); s['installed_stride'] = s.get('stride')
            print(f'{n}: installed {ni} files into {s["mod"]} ({nb} replaced files backed up to {bk}); mismatches after copy: {bad}; '
                  + ('XML only -> tell the user: smp reset (no relaunch, no BodySlide, no mesh patcher)' if xml_only else
                     'meshes changed -> tell the user: relaunch; BodySlide the set(s) if a BodySlide target changed; re-run any mesh patcher that outranks this mod'))
    # ---- table
    sp = {}
    print(f'\n{"design target":22s} {"build":5s} {"bones":5s} {"lining p10/med":14s} {"free p10/med":12s} {"pull-in n/max":13s} {"leash":5s} {"verify":11s} {"stride c/h/s":14s} {"chg":4s} installed / stride at last install')
    for n, d in designs.items():
        s = st[n]; v = s.get('verify', {}); stp = d['work'] + 'state.json'
        prev = sp.setdefault(stp, json.load(open(stp)) if os.path.exists(stp) else {}).get(n, {})
        for g in d['run_targets']:
            b = s['build'].get(g, {}); sn = (s.get('stride') or {}).get(g); was = (s.get('installed_stride') or prev.get('installed_stride') or {}).get(g)
            print(f'{(n + " " + g):22s} {("ERR" if s["build_err"] else "ok"):5s} {fmt(b.get("bones")):5s} {fmt(b.get("lining")):14s} {fmt(b.get("free")):12s} {fmt(b.get("pullin")):13s} '
                  f'{fmt(b.get("leashes")):5s} {(v.get("verdict", "-") + " " + str(v.get("fail", ""))):11s} {fmt(sn):14s} '
                  f'{(str(len(s["changes"])) if s.get("changes") is not None else "?"):4s} {s.get("installed") or prev.get("installed") or "-"} / {fmt(was)}')
        for f in v.get('fails', [])[:8]: print(f'      {f}')
        for g, r in (s.get('render') or {}).items(): print(f'      render {g}: {r}')
        if s.get('foreign') and not inst_arg: print(f'      note: {len(s["foreign"])} changed stage files belong to other designs / targets: ' + ', '.join(r for r, k in s['foreign'][:6]))
        if s.get('changes') is None: print(f'      (no install folder known: design key install= or --mod= to compare with the installed mod)')
        c = console_file(d)
        if c: print(f'      console file: {c}')
    print(f'({(time.time() - t0) / 60:.1f} min; logs in <work>/logs/; renders in <work>/)')
    # ---- state files (one per work folder)
    for stp, state in sp.items():
        for n, d in designs.items():
            if d['work'] + 'state.json' != stp: continue
            s = st[n]; prev = state.get(n, {})
            state[n] = dict(last_run=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), targets=d['run_targets'], build='ERR' if s['build_err'] else 'ok',
                            bones={g: s['build'].get(g, {}).get('bones') for g in d['run_targets']}, verify=s.get('verify', {}).get('verdict'),
                            verify_fails=s.get('verify', {}).get('fails', []), stride=s.get('stride'), changed=len(s['changes']) if s.get('changes') is not None else None,
                            mod=s.get('mod'), installed=s.get('installed', prev.get('installed')), installed_stride=s.get('installed_stride', prev.get('installed_stride')))
        json.dump(state, open(stp, 'w'), indent=1)
        with open(os.path.dirname(stp) + '/STATE.md', 'w', encoding='utf-8') as f:
            f.write('# SMP build state (written by rebuild.py; read this, not the history)\n\n'
                    'stride = caught/hooked/sunk summed over stride_check.py rows (hooked is what reads as "stuck"); verify = verify_rig.py verdict.\n'
                    'Offline checks pose the legs and swing the chains; they cannot see lag, momentum or a spin. The in-game test is the verdict.\n\n'
                    '| design | target | last run | build | bones | verify | stride now | staged files differing from the mod | installed | stride at last install |\n|---|---|---|---|---|---|---|---|---|---|\n')
            for n, s in state.items():
                for g in s.get('targets', []):
                    f.write(f'| {n} | {g} | {s["last_run"]} | {s["build"]} | {(s.get("bones") or {}).get(g)} | {s["verify"]} | {fmt((s.get("stride") or {}).get(g))} | {s.get("changed")} | {s.get("installed") or "-"} | {fmt((s.get("installed_stride") or {}).get(g))} |\n')
            f.write('\nVerify fails still open:\n' + ''.join(f'- {n}: {x}\n' for n, s in state.items() for x in (s.get('verify_fails') or [])) + '\n'
                    'After a mesh install the user owes: relaunch (+ BodySlide of changed sets, + any mesh patcher that outranks the mod). XML-only install: smp reset.\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
