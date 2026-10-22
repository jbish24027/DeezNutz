import os, sys, hashlib


def tree(r):
    o = {}
    for dp, dn, fn in os.walk(r):
        for f in fn:
            p = os.path.join(dp, f)
            o[os.path.relpath(p, r).lower().replace('\\', '/')] = hashlib.md5(open(p, 'rb').read()).hexdigest()
    return o


if __name__ == '__main__':
    inst = tree(sys.argv[1])
    new = {}
    for sub in sys.argv[2:]:
        new.update(tree(sub))
    only_i = sorted(set(inst) - set(new))
    only_n = sorted(set(new) - set(inst))
    chg = sorted(k for k in set(inst) & set(new) if inst[k] != new[k])
    print('installed only:', only_i)
    print('new only:', only_n)
    print('changed:', chg)
    print('same:', len(set(inst) & set(new)) - len(chg))
