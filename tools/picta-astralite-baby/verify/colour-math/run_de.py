"""Colour distance Picta->Astralite and Picta->baby in the low-share cells (are they below a just-noticeable step?)."""
import sys, os
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
exec(open(os.path.join(H, 'run_share.py')).read().split("out = {}")[0])
for w, hs, nm in (('19FC05', 7.5, 'horizon(dome_hor_away)'), ('19FC05', 7.5, 'clouds'), ('19FD05', 7.5, 'clouds'), ('19FD05', 7.5, 'horizon(dome_hor_away)'),
                  ('19FD02', 7.5, 'fog_far'), ('19FD02', 7.5, 'horizon(dome_hor_away)'), ('19FE05', 18.5, 'amb_XPlus'), ('19FE05', 7.5, 'fog_far'),
                  ('19FE02', 7.5, 'horizon(dome_hor_away)'), ('19FE03', 7.5, 'clouds'), ('19FA01', 7.5, 'horizon(dome_hor_away)'), ('19FC01', 7.5, 'horizon(dome_hor_away)')):
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    RP, RB = REC['P'][w], REC['B'][w]
    L0 = RP['_layers'][0]
    sz = cm.sunz(hs, 7.5, 18.5)
    a = cm.comps(XP, RP, hs, cm.clmt_mid, cm.PICTA_CL, sz)
    b = cm.comps(XB, RB, hs, cm.clmt_mid, cm.PICTA_CL, sz)
    a['cloud'], b['cloud'] = a[f'cloud_base_L{L0}'], b[f'cloud_base_L{L0}']
    k, fa = CH[nm]
    va = fm.Astra({fm.colour_partner(w): 1.0}).vis(fa, hs)
    print(w, hs, nm, 'dE(P,A)=%.4f dE(P,B)=%.4f' % (fm.de_ok(a[k], va), fm.de_ok(a[k], b[k])))
