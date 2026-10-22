p = 'baby_model.py'
s = open(p, encoding='utf-8').read()
# gamut guard helper
a = "def donor_colour(mix, field, slot):"
assert a in s
s = s.replace(a, '''def gamut_guard(old, target, hi=255.0):
    """keep target's luminance, pull its chroma back toward old's chroma until no channel exceeds hi"""
    target = np.asarray(target, float)
    if target.max() <= hi: return target
    yt = Y(target); uo = unit(old); ut = unit(target)
    lo_s, hi_s = 0.0, 1.0
    for _ in range(40):
        m = (lo_s + hi_s) / 2; c = yt * lerp(uo, ut, m)
        if c.max() <= hi: lo_s = m
        else: hi_s = m
    return yt * lerp(uo, ut, lo_s)

def donor_colour(mix, field, slot):''', 1)
a = "            target = np.clip(xs[3 * i:3 * i + 3], 0, 255)"
assert a in s
s = s.replace(a, "            target = np.clip(gamut_guard(old[s], xs[3 * i:3 * i + 3], 254.4), 0, 255)")
a = "        target = tgt * (Y(old) / Y(tgt)); base = np.round(target); best = None"
assert a in s
s = s.replace(a, "        target = gamut_guard(old, tgt * (Y(old) / Y(tgt)), 254.4); base = np.round(target); best = None")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
