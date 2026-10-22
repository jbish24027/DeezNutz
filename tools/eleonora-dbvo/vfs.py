import os

ROOT = r'C:\1. AUTHORIA'
PROFILE = os.path.join(ROOT, 'profiles', 'DEEZ CS NUTZ - PBR')
MODS = os.path.join(ROOT, 'mods')
DATA = os.path.join(ROOT, 'Stock Game', 'Data')


def enabled_mods():
    """highest priority first"""
    out = []
    with open(os.path.join(PROFILE, 'modlist.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            if line[0] == '+':
                out.append(line[1:])
    return out


def active_plugins():
    """Every plugin the game loads, in load order.

    MO2 leaves the always-on plugins (Skyrim.esm, the DLC, every Creation Club
    plugin, _ResourcePack.esl) out of plugins.txt entirely, so reading only the
    '*' rows silently drops 60 plugins. The authority is loadorder.txt minus the
    plugins.txt rows that carry no '*'.
    """
    disabled = set()
    with open(os.path.join(PROFILE, 'plugins.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            if line[0] != '*':
                disabled.add(line.lower())
    out = []
    with open(os.path.join(PROFILE, 'loadorder.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            if line.lower() not in disabled:
                out.append(line)
    return out


def plugin_paths():
    """plugin filename(lower) -> (winning path, owning mod)"""
    mods = enabled_mods()
    winner = {}
    # lowest priority first so higher priority overwrites
    for mod in reversed(mods):
        d = os.path.join(MODS, mod)
        try:
            for name in os.listdir(d):
                low = name.lower()
                if low.endswith(('.esp', '.esm', '.esl')):
                    winner[low] = (os.path.join(d, name), mod)
        except (FileNotFoundError, NotADirectoryError):
            continue
    # base game data is lowest of all -> only fill gaps
    try:
        for name in os.listdir(DATA):
            low = name.lower()
            if low.endswith(('.esp', '.esm', '.esl')) and low not in winner:
                winner[low] = (os.path.join(DATA, name), '<Stock Game>')
    except FileNotFoundError:
        pass
    return winner
