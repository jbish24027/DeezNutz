"""install_helmets: copy every file of the helmet STAGE into the design file's MOD (an installed mod folder), backing up what it
replaces to BACKUPS/helmets-<label>-<date>/ (never inside the mods tree). Identical files are skipped; every copy is verified.
usage: install_helmets.py <designs.py> [label]"""
import os, sys, shutil, filecmp, datetime
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import build_helmet_rig as W


def main(dp, label):
    W.use_designs(dp)
    import runpy
    ns = runpy.run_path(W.DESIGNS_PATH, init_globals=dict(vars(W)))
    mod = ns['MOD'].replace(os.sep, '/').rstrip('/') + '/'; bk = ns['BACKUPS'].replace(os.sep, '/').rstrip('/') + f'/helmets-{label}-{datetime.date.today():%Y%m%d}/'
    st = W.STAGE; n_new = n_chg = n_same = 0; changed = []
    for root, _, files in os.walk(st):
        for f in files:
            s = os.path.join(root, f).replace(os.sep, '/'); rel = os.path.relpath(s, st).replace(os.sep, '/'); t = mod + rel
            if os.path.exists(t):
                if filecmp.cmp(s, t, shallow=False): n_same += 1; continue
                os.makedirs(os.path.dirname(bk + rel), exist_ok=True); shutil.copy2(t, bk + rel); n_chg += 1; changed.append(('CHG', rel))
            else: n_new += 1; changed.append(('NEW', rel))
            os.makedirs(os.path.dirname(t), exist_ok=True); shutil.copy2(s, t)
    bad = [rel for k, rel in changed if not filecmp.cmp(st + rel, mod + rel, shallow=False)]
    if changed:
        os.makedirs(bk, exist_ok=True)
        with open(bk + 'CHANGED_FILES.txt', 'a', encoding='utf-8') as f: f.write(''.join(f'{k}|{rel}\n' for k, rel in changed))
    print(f'installed into {mod}: {n_new} new, {n_chg} replaced (backed up to {bk}), {n_same} already identical; mismatches after copy: {len(bad)}')
    for k, rel in changed[:60]: print(f'   {k} {rel}')
    return 0 if not bad else 1


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else datetime.datetime.now().strftime('%H%M')))
