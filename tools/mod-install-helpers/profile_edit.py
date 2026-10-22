"""Insert/remove mod + plugin lines across every MO2 profile, keeping all four
profile files in lockstep (modlist / plugins / loadorder / plugingroups).

MO2 writes these as UTF-8 WITHOUT BOM, CRLF. We match that exactly.
Idempotent: an entry that already exists is removed first, then re-inserted at
the requested anchor, so re-running never duplicates.

Used as a library:
    from profile_edit import Profiles
    P = Profiles()                      # all profiles under <instance>/profiles
    P.add_mods([("Dynamic Combat Collision", "Dynamic Collision Adjustment Setting Fix", "above")])
    P.add_plugins([("Foo.esp", "Bar.esp", "below", "Gameplay - Armors and Weapons")])
    P.write()                           # or P.write(dry=True)
"""
import os, io, sys

INSTANCE = r"C:\1. AUTHORIA"


def read_lines(p):
    with open(p, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8-sig')
    lines = text.split('\r\n') if '\r\n' in text else text.split('\n')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def write_lines(p, lines, dry=False):
    body = '\r\n'.join(lines) + '\r\n'
    if dry:
        return
    with open(p, 'wb') as f:
        f.write(body.encode('utf-8'))


class Profile:
    FILES = ('modlist.txt', 'plugins.txt', 'loadorder.txt', 'plugingroups.txt')

    def __init__(self, root, name):
        self.name = name
        self.dir = os.path.join(root, name)
        self.data = {}
        for f in self.FILES:
            p = os.path.join(self.dir, f)
            self.data[f] = read_lines(p) if os.path.exists(p) else None

    # ---- generic helpers -------------------------------------------------
    def _find(self, fname, pred):
        L = self.data[fname]
        if L is None:
            return -1
        for i, ln in enumerate(L):
            if pred(ln):
                return i
        return -1

    def _drop(self, fname, pred):
        L = self.data[fname]
        if L is None:
            return 0
        n = len(L)
        self.data[fname] = [ln for ln in L if not pred(ln)]
        return n - len(self.data[fname])

    # ---- mods (modlist.txt) ---------------------------------------------
    def add_mod(self, mod, anchor, where='above', enabled=True):
        f = 'modlist.txt'
        self._drop(f, lambda ln: ln[1:] == mod and ln[:1] in '+-')
        i = self._find(f, lambda ln: ln[1:] == anchor and ln[:1] in '+-')
        if i < 0:
            raise KeyError(f"[{self.name}] modlist anchor not found: {anchor!r}")
        at = i if where == 'above' else i + 1
        self.data[f].insert(at, ('+' if enabled else '-') + mod)
        return at

    def has_mod(self, mod):
        return self._find('modlist.txt', lambda ln: ln[1:] == mod and ln[:1] in '+-') >= 0

    def mod_enabled(self, mod):
        i = self._find('modlist.txt', lambda ln: ln[1:] == mod and ln[:1] in '+-')
        return i >= 0 and self.data['modlist.txt'][i].startswith('+')

    def remove_mod(self, mod):
        return self._drop('modlist.txt', lambda ln: ln[1:] == mod and ln[:1] in '+-')

    # ---- plugins (plugins.txt / loadorder.txt / plugingroups.txt) --------
    def add_plugin(self, plugin, anchor, where='below', group=None, active=True):
        # plugins.txt : '*Name.esp' active, 'Name.esp' inactive
        f = 'plugins.txt'
        self._drop(f, lambda ln: ln.lstrip('*') == plugin)
        i = self._find(f, lambda ln: ln.lstrip('*') == anchor)
        if i < 0:
            raise KeyError(f"[{self.name}] plugins.txt anchor not found: {anchor!r}")
        self.data[f].insert(i if where == 'above' else i + 1,
                            ('*' if active else '') + plugin)
        # loadorder.txt : bare names
        f = 'loadorder.txt'
        self._drop(f, lambda ln: ln == plugin)
        i = self._find(f, lambda ln: ln == anchor)
        if i < 0:
            raise KeyError(f"[{self.name}] loadorder.txt anchor not found: {anchor!r}")
        self.data[f].insert(i if where == 'above' else i + 1, plugin)
        # plugingroups.txt : 'Name.esp|Group', kept sorted by plugin name
        if group and self.data['plugingroups.txt'] is not None:
            f = 'plugingroups.txt'
            self._drop(f, lambda ln: ln.split('|')[0] == plugin)
            hdr = [ln for ln in self.data[f] if ln.startswith('#')]
            body = [ln for ln in self.data[f] if not ln.startswith('#')]
            body.append(f"{plugin}|{group}")
            body.sort(key=lambda s: s.split('|')[0].lower())
            self.data[f] = hdr + body

    def group_of(self, plugin):
        L = self.data['plugingroups.txt']
        if L is None:
            return None
        for ln in L:
            if ln.split('|')[0] == plugin:
                return ln.split('|', 1)[1] if '|' in ln else None
        return None

    def preceding_group(self, plugin):
        """Group of the nearest PRECEDING plugin in loadorder that has one."""
        L = self.data['loadorder.txt']
        if L is None:
            return None
        try:
            i = L.index(plugin)
        except ValueError:
            return None
        for j in range(i - 1, -1, -1):
            g = self.group_of(L[j])
            if g:
                return g
        return None

    def has_plugin(self, plugin):
        return self._find('loadorder.txt', lambda ln: ln == plugin) >= 0

    def remove_plugin(self, plugin):
        n = self._drop('plugins.txt', lambda ln: ln.lstrip('*') == plugin)
        n += self._drop('loadorder.txt', lambda ln: ln == plugin)
        n += self._drop('plugingroups.txt', lambda ln: ln.split('|')[0] == plugin)
        return n

    def save(self, dry=False, suffix=None):
        for f in self.FILES:
            if self.data[f] is None:
                continue
            p = os.path.join(self.dir, f)
            if suffix and not dry and os.path.exists(p):
                bak = p + suffix
                if not os.path.exists(bak):
                    with open(p, 'rb') as a, open(bak, 'wb') as b:
                        b.write(a.read())
            write_lines(p, self.data[f], dry)


class Profiles:
    def __init__(self, root=None, names=None):
        root = root or os.path.join(INSTANCE, 'profiles')
        self.root = root
        names = names or sorted(d for d in os.listdir(root)
                                if os.path.isdir(os.path.join(root, d)))
        self.items = [Profile(root, n) for n in names]

    def __iter__(self):
        return iter(self.items)

    def save(self, dry=False, suffix=None):
        for p in self.items:
            p.save(dry, suffix)
