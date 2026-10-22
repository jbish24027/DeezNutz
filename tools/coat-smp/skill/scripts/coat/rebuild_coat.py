"""One command per round for COAT designs (build_coat_rig.py): build, verify, the POSED checks, renders of every moving layer
alone + slit ray-casts, a diff against the installed mods and (optionally) the install - ONE summary table plus state.json /
STATE.md in the design file's work folder. The checks live in here so no round can skip them.

  python rebuild_coat.py <designs.py> <design ...|all> [--install[=label]] [--bodies=m,f] [--skip-build] [--no-render]
  --pieces=A,B[,Design:C]  the pieces (bone families: BeltTip, Flap, Hang, Skirt, ...) the job is allowed to change; the per-piece
      regression (piece_regress.py: physics, root, bone shares, rest height over each collider, copy offset from the drawn surface)
      compares the stage with the installed files and every piece frozen in <work>/approved_pieces.json (APPROVED.md) with its
      approved build - any other changed piece is a FAIL and holds the install.

Posed checks per design and body:
  swing_stride (hooked / sunk)   jump_check (hooked)   idle_check (sunk into the legs, knees out 8 deg)
  flap_jump (strap points pushed the wrong way by a leg piece)
  hang_check (every hanging piece - belt tail, sash end, strap, bag: points inside the mail when the skirt swings while the
              piece lags at rest, of those past its collider's catch; and legs-only contacts with its collider = twitch)
  layer_check (designs with extra skirt layers: legs-only contacts / points past the catch between two layers)
  lining_check (a sheet with a lining behind it: lining points through the sheet in three synthetic poses - chains swinging
      alternately, every chain flared, a thigh raised; a lining weighed differently from its sheet shows at the first step)
  clip_check (men, when smpkit settings name the game's clips: the legs stride through the game's own walk / run / sprint with the
      skirt held at rest - points deeper than the leg catch = the trousers showing through until the cloth reacts)
The table shows each number next to the value recorded at the LAST INSTALL of that design.
--install copies only when every named design built, verified ALL OK and no file outside the named designs changed in the
stage (the shared .osp is allowed whenever a women's set was built). The design file names the installed mods (MOD_M, MOD_F)
and may name BACKUPS (default <work>/backups/ - never inside the mods tree); every replaced file is backed up first.
Run it with the same Python the builder uses (numpy; opencv only for the renders)."""
import os, sys, re, json, time, subprocess, datetime, filecmp, shutil
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import build_coat_rig as W
PY = sys.executable
POOL = 8


def run_all(jobs, parallel=True):
    out, procs, keys = {}, {}, list(jobs)
    i = 0
    while i < len(keys) or procs:
        while i < len(keys) and (len(procs) < POOL if parallel else not procs):
            k = keys[i]; argv, logf = jobs[k]; i += 1
            os.makedirs(os.path.dirname(logf), exist_ok=True)
            procs[k] = (subprocess.Popen([PY] + argv, cwd=HERE, stdout=open(logf, 'w', encoding='utf-8'), stderr=subprocess.STDOUT), logf)
        for k, (p, logf) in list(procs.items()):
            if p.poll() is not None:
                out[k] = p.returncode; procs.pop(k)
                with open(logf, 'a', encoding='utf-8') as f: f.write(f'\nEXIT {p.returncode}\n')
        time.sleep(0.2)
    return out


def rd(f): return open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''
def norm(p): return p.replace(os.sep, '/').replace(chr(92), '/')
def bodies_of(d, bodies): return [g for g in bodies if g in W.DESIGNS[d]]
def xml_path(d, g): cfg = W.DESIGNS[d][g]; return norm(cfg['stage']) + norm(cfg['xml'])
def shapes_in(xmlp): return set(re.findall(r'shape name="([^"]+)"', rd(xmlp)))


def verify_summary(text):
    fails = [l.strip() for l in text.splitlines() if l.startswith('  FAIL')]
    return dict(ok=text.count('  ok   '), fail=len(fails), fails=fails, verdict='ALL OK' if 'ALL OK' in text else ('CHECK' if text else 'none'))


def check_jobs(d, g):
    p = W.DESIGNS[d]['prefix']; sh = shapes_in(xml_path(d, g)); jobs = {}
    if f'{p} Skirt Front' in sh:
        jobs['ss'] = 'swing_stride.py'; jobs['jc'] = 'jump_check.py'; jobs['idle'] = 'idle_check.py'; jobs['lining'] = 'lining_check.py'
        if g == 'm' and clips_configured(): jobs['clips'] = 'clip_check.py'
    if f'{p} Flap Points' in sh: jobs['flap'] = 'flap_jump.py'
    # 2026-10-13 (Claude, SoS Winterhold): + every 'tail' piece the design names (its bag 'Bolsa' and canteen 'Cantil' were skipped)
    tails_ = [pc[0] for pc in W.DESIGNS[d].get(g, {}).get('pieces', ()) if len(pc) > 3 and pc[3] == 'tail']
    if any(f'{p} {k} Points' in sh for k in ('Tip', 'Sash', 'Tail', 'Flap', 'Bag', 'Hang', *tails_)): jobs['hang'] = 'hang_check.py'
    if any(f'{p} {k}' in sh for k in W.LAYER_COLL): jobs['layer'] = 'layer_check.py'
    return jobs


def clips_configured():
    try:
        from smpkit import setting
        return bool(setting('SKELETON_HKX_M')) and bool((setting('CLIPS') or {}).get('m'))
    except Exception:
        return False


def parse_check(kind, text):
    if 'Traceback' in text: return 'ERR'
    if kind in ('ss', 'jc'):
        m = re.search(r'total caught/hooked/sunk (\d+)/(\d+)/(\d+)', text); return (int(m.group(2)), int(m.group(3))) if m else None
    if kind == 'flap':
        m = re.findall(r'[FSB]\s+\d+/\s*(\d+)', text); return sum(map(int, m)) if m else None
    if kind == 'idle':
        m = re.search(r'knees out\s+8 deg, fwd 0:(.*)', text)
        return sum(int(x) for x in re.findall(r'caught/sunk\s+\d+/\s*(\d+)', m.group(1))) if m else None
    if kind == 'hang':
        m = re.search(r'SUMMARY inside/past-collider worst: (.*)', text)
        past = max((int(b) for a, b in re.findall(r'(\d+)/(\d+)', m.group(1))), default=0) if m else None
        con = sum(int(x) for x in re.findall(r' c(\d+)', text)); pressed = len(re.findall(r'^  FAIL', text, re.M))
        return (past, con, pressed)
    if kind == 'clips':
        m = re.search(r'SUMMARY clips worst unseen/frame: (\d+)', text); return int(m.group(1)) if m else None
    if kind == 'lining':
        m = re.search(r'SUMMARY lining through/deepest worst: (\d+)/([\d.]+)', text); return (int(m.group(1)), float(m.group(2))) if m else None
    if kind == 'layer':
        m = re.search(r'SUMMARY layer legs-only contacts/past-catch worst: (.*)', text)
        if not m: return None
        pr = re.findall(r'(\d+)/(\d+)', m.group(1)); return (max((int(a) for a, b in pr), default=0), max((int(b) for a, b in pr), default=0))


def fmt_checks(c):
    if not c: return '-'
    parts = []
    for k, lab in (('ss', 'ss'), ('jc', 'jc'), ('idle', 'idle'), ('flap', 'flap'), ('hang', 'hang'), ('layer', 'layer'), ('lining', 'lining'), ('clips', 'clips')):
        if k in c:
            v = c[k]; parts.append(f'{lab} ' + ('/'.join(map(str, v)) if isinstance(v, (list, tuple)) else str(v)))
    return ' '.join(parts)


def mods():
    """{installed mod folder: its stage folder} from the design file"""
    out = {}
    if W.MOD_M and W.STAGE_M: out[norm(W.MOD_M).rstrip('/') + '/'] = norm(W.STAGE_M).rstrip('/') + '/'
    if W.MOD_F and W.STAGE_F: out[norm(W.MOD_F).rstrip('/') + '/'] = norm(W.STAGE_F).rstrip('/') + '/'
    return out


def owned_files(STAGES):
    own = {}
    rp = W.WORK + 'rework_report.json'
    rep = json.load(open(rp)) if os.path.exists(rp) else {}
    for d, Dz in W.DESIGNS.items():
        for g in ('m', 'f'):
            if g not in Dz: continue
            cfg = Dz[g]; st = norm(cfg['stage']).rstrip('/') + '/'
            mod = next((m for m, s in STAGES.items() if st == s), None)
            if mod is None: continue
            own[(mod, norm(cfg['xml']))] = d
            if g == 'm':
                for v in ('0', '1'): own[(mod, os.path.relpath(norm(cfg['out'].format(v)), st).replace(os.sep, '/'))] = d
            else:
                for o in rep.get(d, {}).get('f', {}).get('outs', []):
                    rel = os.path.relpath(norm(o), st).replace(os.sep, '/'); own[(mod, rel)] = d; own[(mod, rel[:-4] + '.osd')] = d
                own[(mod, 'CalienteTools/BodySlide/SliderSets/' + os.path.basename(norm(cfg['osp'])))] = 'osp'
    return own


def stage_diff(STAGES):
    ch = []
    for mod, st in STAGES.items():
        for root, _, files in os.walk(st):
            for f in files:
                s = os.path.join(root, f); rel = os.path.relpath(s, st).replace(os.sep, '/'); t = mod + rel
                if not os.path.exists(t): ch.append((mod, rel, 'NEW'))
                elif not filecmp.cmp(s, t, shallow=False): ch.append((mod, rel, 'CHG'))
    return ch


def find_in_backups(dirs, root, rel):
    """the file at rel (relative to a mod folder) inside the first backup folder holding it (with or without the mod folder level)"""
    r = rel.lower().replace(os.sep, '/')
    for d in dirs:
        base = norm(root).rstrip('/') + '/' + d
        for dp, _, fs in os.walk(base):
            for f in fs:
                p = norm(os.path.join(dp, f)); k = p[len(base) + 1:].lower()
                if k == r or k.endswith('/' + r): return p
    return None


def regress_files(d, g, STAGES, rep):
    """{'stage': (nif_1, nif_0, xml), 'mod': (...) installed, 'rels': (...)}: the files the piece regression reads"""
    cfg = W.DESIGNS[d][g]; st = norm(cfg['stage']).rstrip('/') + '/'
    mod = next((m for m, s in STAGES.items() if st == s), None)
    if g == 'm': rels = [os.path.relpath(norm(cfg['out'].format(v)), st).replace(os.sep, '/') for v in ('1', '0')]
    else: rels = [os.path.relpath(norm(rep[d]['f']['outs'][0]), st).replace(os.sep, '/'), None]
    rels.append(norm(cfg['xml']))
    return dict(rels=rels, mod=mod, stage=tuple(st + r if r else None for r in rels), installed=tuple(mod + r if (r and mod) else None for r in rels))


def piece_regression(d, g, STAGES, rep, named, lines, limits_ok=False):
    """2026-10-14 (user: 'per piece: physics, root, bone shares, rest height over the copy, copy offset from the drawn surface, vs the last
    approved install; FAIL on any change outside the job's named pieces' + 'APPROVED.md - those pieces are frozen'): the stage against the
    installed files; every piece frozen in approved_pieces.json against its approved build. -> the pieces that changed unnamed (FAIL)"""
    import piece_regress as PR
    fs = regress_files(d, g, STAGES, rep)
    if not fs['mod'] or not os.path.exists(fs['installed'][0]):
        lines.append(f'{d} {g}: piece regression - nothing installed to compare with'); return []
    new = PR.summary(fs['stage'][0], fs['stage'][2], fs['stage'][1])
    changes = PR.compare(PR.summary(fs['installed'][0], fs['installed'][2], fs['installed'][1]), new)
    apj = W.WORK + 'approved_pieces.json'
    AP = json.load(open(apj)) if os.path.exists(apj) else dict(designs={})
    for row in AP['designs'].get(d, []):
        base = [find_in_backups(row['baseline'], AP.get('backups_root', ''), r) if r else None for r in fs['rels']] if row['baseline'] else [None] * 3
        base = [b or i for b, i in zip(base, fs['installed'])]
        ch2 = PR.compare(PR.summary(base[0], base[2], base[1]), new)
        frozen = set(ch2) | set(changes) if '*' in row['pieces'] else set(row['pieces'])
        for f in frozen:
            if f in ch2: changes[f] = [f'[approved {row["row"][:16]}] ' + l for l in ch2[f]]
            else: changes.pop(f, None)
    return PR.report(f'{d} {g}', changes, named, out=lines.append, limits_ok=limits_ok)


def install(STAGES, changes, label):
    bk = (norm(W.BACKUPS) if W.BACKUPS else W.WORK + 'backups/').rstrip('/') + f'/coat-{label}-{datetime.datetime.now():%Y%m%d}/'
    os.makedirs(bk, exist_ok=True)
    nb = ni = bad = 0
    for mod, rel, kind in changes:
        s = STAGES[mod] + rel; t = mod + rel
        if kind == 'CHG':
            b = bk + os.path.basename(mod.rstrip('/')) + '/' + rel; os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copy2(t, b); nb += 1
        os.makedirs(os.path.dirname(t), exist_ok=True); shutil.copy2(s, t); ni += 1
        if not filecmp.cmp(s, t, shallow=False): bad += 1
    with open(bk + 'CHANGED_FILES.txt', 'a', encoding='utf-8') as f: f.write(''.join(f'{k}|{m}|{r}\n' for m, r, k in changes))
    return nb, ni, bad, bk


def main(argv):
    if not argv or not argv[0].lower().endswith('.py'): print(__doc__); return 1
    dp = os.path.abspath(argv[0]).replace(os.sep, '/'); argv = argv[1:]
    W.use_designs(dp)
    DESIGNS = list(W.DESIGNS)
    designs = [a for a in argv if a in DESIGNS] or (DESIGNS if 'all' in argv else [])
    if not designs: print(__doc__); print('designs in the file:', DESIGNS); return 1
    inst_arg = next((a for a in argv if a.startswith('--install')), None)
    label = inst_arg.split('=', 1)[1] if inst_arg and '=' in inst_arg else datetime.datetime.now().strftime('%H%M')
    skip_build = '--skip-build' in argv; do_render = '--no-render' not in argv
    bodies = next((a.split('=')[1].split(',') for a in argv if a.startswith('--bodies=')), ['m', 'f'])
    LOGS, RENDERS = W.WORK + 'logs/', W.WORK + 'renders/'
    os.makedirs(LOGS, exist_ok=True); os.makedirs(RENDERS, exist_ok=True); t0 = time.time(); st = {d: {} for d in designs}
    sp = W.WORK + 'state.json'; state = json.load(open(sp)) if os.path.exists(sp) else {}
    STAGES = mods()
    if not skip_build:      # 2026-10-13: parallel (POOL) - the shared .osp and rework_report.json writes are locked in the builder (_shared_lock)
        rc = run_all({d: ([HERE + 'build_coat_rig.py', dp, d] + bodies_of(d, bodies), LOGS + f'{d}_build.log') for d in designs}, parallel=True)
        for d in designs: st[d]['build_rc'] = rc[d]
    else:
        for d in designs: st[d]['build_rc'] = 0 if 'EXIT 0' in rd(LOGS + f'{d}_build.log') else None
    for d in designs:
        text = rd(LOGS + f'{d}_build.log'); st[d]['build_err'] = 'Traceback' in text or st[d]['build_rc'] not in (0,)
        m = re.findall(r"bones per shape \{[^}]*\}", text); st[d]['bones'] = max((int(x) for s_ in m for x in re.findall(r": (\d+)", s_)), default=None)
    ok_b = [d for d in designs if not st[d]['build_err']]
    run_all({d: ([HERE + 'verify_coat.py', dp, d] + bodies_of(d, bodies), LOGS + f'{d}_verify.log') for d in ok_b})
    for d in ok_b: st[d]['verify'] = verify_summary(rd(LOGS + f'{d}_verify.log'))
    jobs = {}
    for d in ok_b:
        for g in bodies_of(d, bodies):
            for k, script in check_jobs(d, g).items(): jobs[(d, g, k)] = ([HERE + script, dp, d, g], LOGS + f'{d}_{g}_{k}.log')
    run_all(jobs)
    for d in ok_b:
        st[d]['checks'] = {g: {k: parse_check(k, rd(LOGS + f'{d}_{g}_{k}.log')) for (dd, gg, k) in jobs if (dd, gg) == (d, g)} for g in bodies_of(d, bodies)}
    if do_render:
        rj = {(d, g): ([HERE + 'render_layers.py', dp, d, g, RENDERS + f'{d}_{g}_layers.png'], LOGS + f'{d}_{g}_render.log') for d in ok_b for g in bodies_of(d, bodies)}
        rc = run_all(rj)
        for (d, g), r in rc.items(): st[d].setdefault('renders', []).append(f'{d}_{g}_layers.png ' + ('ok' if r == 0 else 'FAILED'))
    if not STAGES:
        print('no installed mods named in the design file (MOD_M / MOD_F): the stage was built and checked but not compared or installed')
    own = owned_files(STAGES); changes = stage_diff(STAGES)
    per = {d: [] for d in designs}; foreign = []
    for mod, rel, kind in changes:
        o = own.get((mod, rel))
        if o in per: per[o].append((mod, rel, kind))
        elif o == 'osp' and any('f' in bodies_of(d, bodies) for d in designs): per[designs[0]].append((mod, rel, kind))
        else: foreign.append((mod, rel, kind, o))
    for d in designs: st[d]['changed'] = len(per[d])
    # 2026-10-14: the per-piece regression (piece_regress.py) - a piece the job did not name (--pieces=A,B or Design:A) that changed
    # against the installed files, or a frozen piece (approved_pieces.json = APPROVED.md) that changed against its approved build, holds
    # the install
    named_arg = next((a.split('=', 1)[1] for a in argv if a.startswith('--pieces=')), '')
    rep_ = json.load(open(W.WORK + 'rework_report.json')) if os.path.exists(W.WORK + 'rework_report.json') else {}
    reg_lines = []
    for d in ok_b:
        named = [x for x in named_arg.split(',') if x and ':' not in x] + [x.split(':', 1)[1] for x in named_arg.split(',') if x.startswith(d + ':')]
        st[d]['regress'] = {}
        for g in bodies_of(d, bodies):
            try: st[d]['regress'][g] = piece_regression(d, g, STAGES, rep_, named, reg_lines, limits_ok='--limits-ok' in argv)
            except Exception as e: st[d]['regress'][g] = [f'ERROR {e!r}']; reg_lines.append(f'{d} {g}: piece regression ERROR {e!r} - holds the install')
    if reg_lines: print('\n'.join(reg_lines))
    if inst_arg and STAGES:
        pressed = lambda d: sum((c.get('hang') or (0, 0, 0))[2] if isinstance(c.get('hang'), (list, tuple)) and len(c['hang']) > 2 else 0 for c in (st[d].get('checks') or {}).values())
        unnamed = lambda d: [f for v in (st[d].get('regress') or {}).values() for f in v]
        good = [d for d in designs if d in ok_b and st[d]['verify']['verdict'] == 'ALL OK' and pressed(d) == 0 and not unnamed(d)]     # v12: a piece pressed in an idle / walk stance holds the install
        held = [d for d in designs if d not in good]
        if held: print(f'NOT installed: {held} (build error, verify not ALL OK, or pieces changed that the job did not name: ' + ', '.join(f'{d} {unnamed(d)}' for d in held if d in ok_b and unnamed(d)) + ')')
        if foreign: print(f'NOT installed: {len(foreign)} changed files belong to designs not in this run:'); [print('   ', m, r, k, o) for m, r, k, o in foreign[:12]]
        if good and not held and not foreign:
            todo = [c for d in good for c in per[d]]
            if todo:
                nb, ni, bad, bk = install(STAGES, todo, label)
                print(f'installed {ni} files ({nb} backed up to {bk}), mismatches after copy: {bad}')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                for d in good: st[d]['installed'] = now; st[d]['installed_checks'] = st[d].get('checks')
            else: print('nothing to install: the stage equals the installed mods')
    print(f'\n{"design":14s} {"build":5s} {"bones":5s} {"verify":12s} {"chg":4s} {"checks now (ss hooked/sunk, jc hooked/sunk, idle sunk, flap wrong-way, hang past/legs-contacts, layer contacts/past, lining through/deepest, clips worst unseen)":82s} installed / at last install')
    for d in designs:
        s = st[d]; v = s.get('verify', {}); prev = state.get(d, {})
        for g in bodies_of(d, bodies):
            now = s.get('checks', {}).get(g); was = (s.get('installed_checks') or prev.get('installed_checks') or {}).get(g)
            print(f'{(d + " " + g):14s} {("ERR" if s["build_err"] else "ok"):5s} {str(s.get("bones")):5s} {(v.get("verdict", "-") + " " + str(v.get("fail", ""))):12s} {str(s.get("changed", "-")):4s} {fmt_checks(now):82s} {s.get("installed") or prev.get("installed") or "-"} / {fmt_checks(was)}')
        for f in v.get('fails', [])[:6]: print(f'      {f}')
        for r in s.get('renders', []): print(f'      render {r}')
    if foreign and not inst_arg: print(f'note: {len(foreign)} changed stage files belong to other designs: ' + ', '.join(r for m, r, k, o in foreign[:6]))
    print(f'({(time.time() - t0) / 60:.1f} min; logs in {LOGS}, renders in {RENDERS})')
    for d in designs:
        s = st[d]; prev = state.get(d, {})
        state[d] = dict(last_run=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), build='ERR' if s['build_err'] else 'ok', verify=s.get('verify', {}).get('verdict'),
                        verify_fails=s.get('verify', {}).get('fails', []), checks=s.get('checks'), installed=s.get('installed', prev.get('installed')),
                        installed_checks=s.get('installed_checks', prev.get('installed_checks')), changed=s.get('changed'), regress=s.get('regress'))
    json.dump(state, open(sp, 'w'), indent=1)
    with open(W.WORK + 'STATE.md', 'w', encoding='utf-8') as f:
        f.write('# Coat SMP build state (written by rebuild_coat.py; read this, not the history)\n\n'
                'checks = ss hooked/sunk (swing_stride), jc hooked/sunk (jump_check), idle sunk (knees out 8 deg), flap wrong-way pushes, '
                'hang = worst points past a hanging piece\'s collider when the skirt swings while it lags / legs-only contacts with its collider, '
                'layer = legs-only contacts / points past the catch between two skirt layers swung against each other\n\n'
                '| design | last run | build | verify | checks now | staged files differing from the mods | installed | checks at last install |\n|---|---|---|---|---|---|---|---|\n')
        for d, s in state.items():
            for g in ('m', 'f'):
                if s.get('checks') and g in s['checks']:
                    f.write(f'| {d} {g} | {s["last_run"]} | {s["build"]} | {s["verify"]} | {fmt_checks(s["checks"][g])} | {s.get("changed")} | {s["installed"] or "-"} | {fmt_checks((s.get("installed_checks") or {}).get(g))} |\n')
        f.write('\nVerify fails still open:\n' + ''.join(f'- {d}: {x}\n' for d, s in state.items() for x in (s.get('verify_fails') or [])) + '\n'
                'Offline checks pose the legs and swing the chains; they cannot see lag, momentum or a spin. The in-game test is the verdict.\n'
                'After a men\'s mesh install: relaunch (the men\'s meshes carry their shaders, no patcher rerun when the mod outranks the patcher output).\n'
                'After a women\'s mesh install: BodySlide the rebuilt sets, rerun any mesh patcher that outranks the output, relaunch. XML-only: smp reset.\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
