import os
d = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(d, 'final2_model.py'); s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new)
# one ESL for every VL variant: K (VOLI copy intensities) fixed from the half-strength alive solve
rep("""    for amt in (0.5, 1.0):
        for br in ('alive', 'newly_on'):
            Dv = dials(); Dv['VOL_AMOUNT'] = amt; Dv['VL_BRANCH'] = br
            K_fixed = VLR.get((amt, 'alive'), {}).get('_K') if br == 'newly_on' else None""",
"""    for amt in (0.5, 1.0):
        for br in ('alive', 'newly_on'):
            Dv = dials(); Dv['VOL_AMOUNT'] = amt; Dv['VL_BRANCH'] = br
            K_fixed = None if (amt, br) == (0.5, 'alive') else VLR[(0.5, 'alive')]['_K']""")
rep("""e11_edits_full_alive=e11_plan(r, VLR[(1.0, 'alive')]))""",
"""e11_edits_full_alive=e11_plan(r, VLR[(1.0, 'alive')]), e11_edits_full_newly_on=e11_plan(r, VLR[(1.0, 'newly_on')]))""")
rep("""    nlines = {k: sum(len(f[k]) for f in plan['files'].values()) for k in ('e11_edits', 'e11_edits_newly_on', 'e11_edits_full_alive')}""",
"""    nlines = {k: sum(len(f[k]) for f in plan['files'].values()) for k in ('e11_edits', 'e11_edits_newly_on', 'e11_edits_full_alive', 'e11_edits_full_newly_on')}""")
rep("""    P(f'== E11 LINES routed files: alive(0.5) {nlines["e11_edits"]}  newly_on(0.5) {nlines["e11_edits_newly_on"]}  alive(1.0) {nlines["e11_edits_full_alive"]}; Night/Interior in alive: {len(nightkeys)}')""",
"""    P(f'== E11 LINES routed files: {nlines}; Night/Interior in alive: {len(nightkeys)}')""")
open(p, 'w', encoding='utf-8').write(s)
b = os.path.join(d, 'build_stage2.py'); t = open(b, encoding='utf-8').read()
old = "PLANKEY = {'alive': 'e11_edits', 'newly_on': 'e11_edits_newly_on', 'alive_full': 'e11_edits_full_alive'}[branch]"
assert old in t
t = t.replace(old, "PLANKEY = {'alive': 'e11_edits', 'newly_on': 'e11_edits_newly_on', 'alive_full': 'e11_edits_full_alive', 'newly_on_full': 'e11_edits_full_newly_on'}[branch]")
t = t.replace("if branch == 'newly_on':", "if branch in ('newly_on', 'newly_on_full'):")
t = t.replace("(branch == 'newly_on' and ", "(branch in ('newly_on', 'newly_on_full') and ")
open(b, 'w', encoding='utf-8').write(t)
print('ok', t.count("newly_on_full"))
