import os
M = 'C:/1. AUTHORIA/mods/'
def tree(root):
    out = set()
    for r, d, f in os.walk(root):
        for x in f:
            out.add(os.path.relpath(os.path.join(r, x), root).replace(os.sep, '/').lower())
    return out
D = tree(M + 'Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries')
S = tree(M + '[NoDelete] Picta ENB 1.1.2 - Data (shipped)/enbseries')
only = sorted(S - D)
print(len(D), len(S), len(only))
print('\n'.join(only))
