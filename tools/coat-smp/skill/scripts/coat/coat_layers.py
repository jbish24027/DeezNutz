"""SoS Officer v2: the skirt layers a built design has, for the posed checks - the main skirt ('Skirt' chains, '<p> Skirt
Front/Side/Back' lining colliders) plus every extra layer of cfg 'groups' ('<p> <word>NN r' chains, '<p> <word> Front/...').
A design without groups has the main layer only, so the checks behave exactly as before for it."""
import sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest



def layers(d, g):
    """[(word, phys)] - the main skirt first"""
    Dz = W.DESIGNS[d]; out = [('Skirt', Dz['phys'])]
    for gw, gc in Dz[g].get('groups', {}).items(): out.append((gw, gc['phys']))
    return out


def chains(Gw, p, word):
    out = []
    for k in range(40):
        bs = [f'{p} {word}{k:02d} {r}' for r in range(12)]
        if bs[1] not in Gw: break
        out.append([b for b in bs if b in Gw])
    return out


def lining(S, p, word):
    """{side: shape} of a layer's lining colliders present in the mesh"""
    return {s: S[f'{p} {word} {s}'] for s in ('Front', 'Back', 'Side') if f'{p} {word} {s}' in S}


def lims(phys):
    l1, l = phys['SK_LIM1'], phys['SK_LIM']
    return (dict(out=-l1['lo'][0], inn=l1['hi'][0], side=l1['hi'][1]), dict(out=-l['lo'][0], inn=l['hi'][0], side=l['hi'][1]))


def pose_all(F, Gw, p, d, g, cx, cy, kind, *a, keep_lims=False):
    """every layer's chains posed the same way ('swing' axis th1 th / 'flare' th1 th / 'curl' k), each clamped to its own limits
    (keep_lims: a one-layer design keeps the limits the calling check set - hang_check's numbers stay comparable)"""
    Dm = {}
    for word, ph in layers(d, g):
        ch = chains(Gw, p, word)
        if not ch: continue
        l1, l = lims(ph)
        if not keep_lims: F.LIM1.update(l1); F.LIM.update(l)
        if kind == 'swing': Dm.update(F.swing(Gw, ch, cx, cy, *a))
        elif kind == 'flare': Dm.update(F.flare(Gw, ch, cx, cy, *a))
        elif kind == 'curl': Dm.update(F.flare(Gw, ch, cx, cy, -a[0] * l1['inn'], -a[0] * l['inn']))
    return Dm
