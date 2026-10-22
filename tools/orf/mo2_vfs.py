"""
Local reimplementation of MO2 loose-file precedence.

modlist.txt is stored HIGHEST priority first. A mod line starts with '+' when
enabled, '-' when disabled. Separators end in '_separator' and are skipped.
'overwrite' sits above every mod.

Loose files beat BSA-packed. This resolver only handles loose files and says so
when it finds nothing, so a BSA-only asset is reported as such rather than
silently treated as absent -- that distinction matters, because a mod whose
textures live in a BSA needs an extraction step, not a shrug.
"""

import os

INSTANCE = r'C:\1. AUTHORIA'
MODS = os.path.join(INSTANCE, 'mods')
OVERWRITE = os.path.join(INSTANCE, 'overwrite')


def load_order(profile='DEEZ CS NUTZ'):
    """Enabled mod folder names, highest priority first."""
    path = os.path.join(INSTANCE, 'profiles', profile, 'modlist.txt')
    out = []
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            line = line.rstrip('\n').rstrip('\r')
            if not line or line.startswith('#'):
                continue
            flag, name = line[0], line[1:]
            if name.endswith('_separator'):
                continue
            if flag == '+':
                out.append(name)
    return out


class Vfs:
    def __init__(self, profile='DEEZ CS NUTZ'):
        self.order = load_order(profile)
        self._index = None

    def build_index(self, subdirs=('textures', 'meshes')):
        """
        One pass over every enabled mod, recording which mod provides which
        Data-relative path. Later mods in self.order are HIGHER priority, so we
        walk in reverse and let higher priority overwrite.
        """
        idx = {}
        roots = [(m, os.path.join(MODS, m)) for m in reversed(self.order)]
        roots.append(('overwrite', OVERWRITE))
        for mod, root in roots:
            for sub in subdirs:
                base = os.path.join(root, sub)
                if not os.path.isdir(base):
                    continue
                for dp, _dn, fn in os.walk(base):
                    rel_dir = os.path.relpath(dp, root).lower()
                    for f in fn:
                        idx[os.path.join(rel_dir, f.lower())] = (mod, os.path.join(dp, f))
        self._index = idx
        return len(idx)

    def resolve(self, data_rel_path):
        """-> (mod_name, absolute_path) or (None, None) if no loose provider."""
        if self._index is None:
            raise RuntimeError('call build_index() first')
        key = data_rel_path.lower().replace('/', '\\').lstrip('\\')
        return self._index.get(key, (None, None))
