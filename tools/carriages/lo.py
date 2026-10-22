import os
ROOT=r'C:\1. AUTHORIA'
def read(p):
    return [l.rstrip('\r\n') for l in open(p,encoding='utf-8-sig',errors='replace')]
def resolve(profile):
    pd=os.path.join(ROOT,'profiles',profile)
    mods=[l[1:] for l in read(os.path.join(pd,'modlist.txt')) if l.startswith('+')]  # highest priority first
    active={l[1:].lower() for l in read(os.path.join(pd,'plugins.txt')) if l.startswith('*')}
    order=[l for l in read(os.path.join(pd,'loadorder.txt')) if l and not l.startswith('#')]
    base={'skyrim.esm','update.esm','dawnguard.esm','hearthfires.esm','dragonborn.esm'}
    # index files per mod root
    cand={}
    for m in reversed(mods):  # low->high so high overwrites
        d=os.path.join(ROOT,'mods',m)
        try: fs=os.listdir(d)
        except: continue
        for f in fs:
            if f.lower().endswith(('.esp','.esm','.esl')): cand[f.lower()]=os.path.join(d,f)
    ov=os.path.join(ROOT,'overwrite')
    for f in os.listdir(ov):
        if f.lower().endswith(('.esp','.esm','.esl')): cand[f.lower()]=os.path.join(ov,f)
    data=os.path.join(ROOT,'Stock Game','Data')
    out=[]
    for p in order:
        pl=p.lower()
        if pl in base or pl in active or not pl.endswith('.esp') and pl not in active and os.path.exists(os.path.join(data,p)) and pl.startswith('cc'):
            path=cand.get(pl) or (os.path.join(data,p) if os.path.exists(os.path.join(data,p)) else None)
            if pl in active or pl in base or path: out.append((p,path))
    return out
if __name__=='__main__':
    import sys
    r=resolve(sys.argv[1]); print(len(r)); print(r[:8]); print([x for x in r if x[1] is None][:10]); print(r[-5:])
