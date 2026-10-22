"""Read-only: simulate the baby modlist from the live PICTA modlist + the spec insertions and resolve VFS winners
for every path class the spec cares about. Writes only into this scratch folder."""
import os, sys, json, collections

INST = 'C:/1. AUTHORIA'
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(HERE, '..', 'final', 'stage', sys.argv[1] if len(sys.argv) > 1 else 'alive')
ml = open(INST + '/profiles/DEEZ CS NUTZ - PICTA/modlist.txt', encoding='utf-8').read().splitlines()

FORK = 'Authoria - Picta x Astralite - E11'
TWIN = 'Authoria - Picta x Astralite - Root twin'
ESLMOD = 'houseCARL - Authoria - Patch - Picta x Astralite'
MIST = 'Authoria - Picta x Astralite - Mist assets'
ins = {'+Authoria - Picta - Bottled raindrop': '+' + FORK,
       '+Authoria - Picta ENB - Root twin': '+' + TWIN,
       '+houseCARL - Authoria - Patch - Picta Seasonal': '+' + ESLMOD,
       '+[NoDelete] Mists of Tamriel': '+' + MIST}
baby = []
for ln in ml:
    if ln in ins:
        baby.append(ins[ln])
    if ln == '+Authoria - Picta ENB - Root twin':
        baby.append('-Authoria - Picta ENB - Root twin')
    else:
        baby.append(ln)
assert len(baby) == len(ml) + 4, (len(baby), len(ml))

MIST_FILES = ['meshes/effects/distant_mounts_lite.nif', 'meshes/effects/distant_mounts_heavy.nif',
              'meshes/effects/distant_mounts_rain.nif', 'textures/effects/distant_fogs_lite.dds',
              'textures/effects/distant_fogs_heavy.dds', 'textures/effects/distant_fogs_rain.dds',
              'meshes/mistsvolumetric/skyrimvolmistbalanced.nif', 'meshes/mistsvolumetric/skyrimvolmistdense.nif',
              'meshes/mistsvolumetric/skyrimvolmistsubtle.nif', 'meshes/mistsvolumetric/solstheimvolmista.nif',
              'meshes/mistsvolumetric/solstheimvolmistb.nif', 'textures/volmist/mist1.dds']
SOUL = INST + '/mods/[NoDelete] Soul Core Plugin and Assets'

def LP(p):
    bs = chr(92)
    return bs + bs + '?' + bs + os.path.abspath(p).replace('/', bs)

def modroot(mod):
    if mod == FORK:
        return LP(os.path.join(STAGE, FORK))
    if mod == TWIN:
        return LP(os.path.join(STAGE, TWIN))
    if mod == MIST:
        return '<MIST>'
    return INST + '/mods/' + mod

def ci_tree(base):
    """lower-case rel path -> real path for the interesting subtrees of one mod folder."""
    out = {}
    if base == '<MIST>':
        for rel in MIST_FILES:
            out[rel] = 'MIST:' + rel
        return out
    if not os.path.isdir(base):
        return out
    for top in os.listdir(base):
        tl = top.lower(); tp = os.path.join(base, top)
        if os.path.isfile(tp):
            out[tl] = tp      # Data root files (enbseries.ini, plugin inis, manifest.json, esp...)
            continue
        if tl in ('enbseries', 'root'):
            for r, ds, fs in os.walk(tp):
                for f in fs:
                    out[os.path.relpath(os.path.join(r, f), base).replace(os.sep, '/').lower()] = os.path.join(r, f)
        if tl in ('meshes', 'textures'):
            for sub in ('effects', 'mistsvolumetric', 'volmist'):
                for cand in os.listdir(tp):
                    if cand.lower() == sub:
                        sp = os.path.join(tp, cand)
                        for r, ds, fs in os.walk(sp):
                            for f in fs:
                                rel = os.path.relpath(os.path.join(r, f), base).replace(os.sep, '/').lower()
                                if sub == 'effects' and not (os.path.basename(rel).startswith('distant_')):
                                    continue
                                out[rel] = os.path.join(r, f)
    return out

def resolve(lines):
    enabled = [l[1:] for l in lines if l.startswith('+') and not l.endswith('_separator')]
    owner = {}; allp = collections.defaultdict(list)
    for mod in reversed(enabled):      # lowest priority first
        for rel, real in ci_tree(modroot(mod)).items():
            owner[rel] = mod; allp[rel].append(mod)
    ow = INST + '/overwrite'
    for r, ds, fs in os.walk(ow):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), ow).replace(os.sep, '/').lower()
            if rel.startswith(('enbseries', 'root/', 'meshes/mistsvolumetric', 'textures/volmist')) or 'distant_' in rel or rel.count('/') == 0:
                owner[rel] = '<overwrite>'; allp[rel].append('<overwrite>')
    return owner, allp, enabled

bo, ba, ben = resolve(baby)
po, pa, pen = resolve(ml)
rep = collections.OrderedDict()
# 1) every enbseries path + root-level ini
fork_paths = set(k for k in ci_tree(modroot(FORK)) if k != 'manifest.json')
rep['fork_paths'] = len(fork_paths)
rep['fork_paths_not_won_by_fork'] = sorted((p, bo.get(p)) for p in fork_paths if bo.get(p) != FORK)
rep['data_enbseries_winners_baby'] = collections.Counter(v for k, v in bo.items() if k.startswith('enbseries')).most_common()
rep['data_enbseries_ini_not_in_fork_count'] = len([k for k, v in bo.items() if k.startswith('enbseries/') and k.endswith('.ini') and v != FORK])
rep['data_enbseries_ini_not_in_fork_nonregional'] = sorted(k for k, v in bo.items() if k.startswith('enbseries') and k.endswith('.ini') and v != FORK and '/01_skyrim/' not in k)
rep['root_winners_baby_enb'] = sorted((k[5:], v) for k, v in bo.items() if k.startswith('root/') and ('enb' in k))
rep['picta_twin_paths_owner_in_baby'] = sorted((k, bo.get(k)) for k in ci_tree(INST + '/mods/Authoria - Picta ENB - Root twin'))
rep['manifest_json_in_data_root_all_providers_baby'] = ba.get('manifest.json')
rep['plugin_ini_owner_baby'] = bo.get('picta - weathers of aurbis.ini'), ba.get('picta - weathers of aurbis.ini')
rep['mist_paths'] = {p: (bo.get(p), ba.get(p)) for p in MIST_FILES}
rep['mist_paths_picta_lane_providers'] = {p: pa.get(p) for p in MIST_FILES}
# 2) source assets exist loose in Soul Core?
src = {}
for p in MIST_FILES:
    hit = None
    for r, ds, fs in os.walk(SOUL):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), SOUL).replace(os.sep, '/').lower()
            if rel == p:
                hit = os.path.join(r, f)
    src[p] = hit
rep['soulcore_loose_sources'] = src
json.dump(rep, open(os.path.join(HERE, 'verify_vfs_out.json'), 'w'), indent=1, default=str)
print(json.dumps(rep, indent=1, default=str)[:12000])
