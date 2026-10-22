"""
Confidence-gated colour classifier for armour textures.

Whole-atlas averaging was measured wrong 3 times in 4 on dark robes, so this
never asserts a colour it is not confident about. It returns a verdict plus a
confidence, and anything below the bar is handed to a human (me) to look at.

Two ideas make it work where averaging failed:
  1. Judge the DOMINANT chroma cluster, not the mean. An atlas mixes garment,
     trim, boots and props; the mean of those is always mud.
  2. Refuse to guess when the texture is too dark or too desaturated for hue to
     mean anything -- that is exactly the case that produced the wrong answers.
"""

import os
import numpy as np
from PIL import Image

BUCKETS = ['ORF_Red', 'ORF_Brown', 'ORF_Gold', 'ORF_Yellow', 'ORF_Green',
           'ORF_Blue', 'ORF_Purple', 'ORF_Pink']


def _hue_bucket(h, s, v):
    if h < 12 or h >= 335:
        return 'ORF_Red'
    if h < 42:
        return 'ORF_Brown' if v < 0.5 else 'ORF_Gold'
    if h < 68:
        return 'ORF_Gold' if v > 0.45 else 'ORF_Brown'
    if h < 82:
        return 'ORF_Yellow'
    if h < 168:
        return 'ORF_Green'
    if h < 262:
        return 'ORF_Blue'
    if h < 300:
        return 'ORF_Purple'
    return 'ORF_Pink'


def classify(png_path):
    """-> (keyword, confidence 0..1, debug dict)"""
    try:
        im = Image.open(png_path).convert('RGBA')
    except Exception as e:
        return None, 0.0, {'error': str(e)}
    a = np.asarray(im).astype(np.float32) / 255.0
    if a.size == 0:
        return None, 0.0, {'error': 'empty'}
    rgb, al = a[..., :3], a[..., 3]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)

    keep = (al > 0.35)
    if keep.sum() < 64:
        keep = np.ones_like(al, bool)
    V, S = v[keep], s[keep]

    # --- achromatic decision first -------------------------------------
    lit = V > 0.04
    if lit.sum() < 32:
        return 'ORF_Black', 0.9, {'reason': 'almost no lit pixels'}
    Vl, Sl = V[lit], S[lit]
    chroma_frac = float((Sl > 0.28).mean())
    medv = float(np.median(Vl))

    if chroma_frac < 0.12:
        if medv < 0.16:
            return 'ORF_Black', 0.85, {'chroma': chroma_frac, 'v': medv}
        if medv > 0.68:
            return 'ORF_White', 0.85, {'chroma': chroma_frac, 'v': medv}
        return 'ORF_Grey', 0.7, {'chroma': chroma_frac, 'v': medv}

    # --- dominant chroma cluster ---------------------------------------
    r, g, b = rgb[..., 0][keep], rgb[..., 1][keep], rgb[..., 2][keep]
    mxv, mnv = np.maximum.reduce([r, g, b]), np.minimum.reduce([r, g, b])
    d = mxv - mnv
    h = np.zeros_like(mxv)
    nz = d > 1e-6
    rm = nz & (mxv == r)
    gm = nz & (mxv == g)
    bm = nz & (mxv == b)
    h[rm] = (60 * ((g[rm] - b[rm]) / d[rm]) + 360) % 360
    h[gm] = 60 * ((b[gm] - r[gm]) / d[gm]) + 120
    h[bm] = 60 * ((r[bm] - g[bm]) / d[bm]) + 240

    sel = (S > 0.28) & (V > 0.06)
    if sel.sum() < 32:
        return ('ORF_Black' if medv < 0.2 else 'ORF_Grey'), 0.55, {'reason': 'weak chroma'}
    hs, ss, vs = h[sel], S[sel], V[sel]
    # AREA-weighted, not saturation-weighted. Trim and embroidery are tiny and
    # very saturated; the garment is large and moderate. Weighting by saturation
    # let gold scrollwork outvote a navy dress. Area is the honest signal.
    w = np.ones_like(ss)

    hist = np.zeros(36)
    idx = (hs / 10).astype(int) % 36
    np.add.at(hist, idx, w)
    # smooth circularly so a hue straddling a bin edge is not split
    hist = sum(np.roll(hist, k) for k in (-1, 0, 1))
    top = int(hist.argmax())
    share = float(hist[top] / max(hist.sum(), 1e-6))

    inbin = (idx == top) | (idx == (top + 1) % 36) | (idx == (top - 1) % 36)
    hh = float(np.median(hs[inbin])) if inbin.sum() else float(np.median(hs))
    vv = float(np.median(vs[inbin])) if inbin.sum() else float(np.median(vs))
    sv = float(np.median(ss[inbin])) if inbin.sum() else float(np.median(ss))

    kw = _hue_bucket(hh, sv, vv)

    # confidence: how dominant the cluster is, how coloured, how lit
    conf = min(1.0, share * 1.7) * min(1.0, chroma_frac * 3.2) * min(1.0, (sv / 0.45))
    if vv < 0.12:
        conf *= 0.45          # dark textures are where averaging went wrong
    return kw, round(float(conf), 3), {'hue': round(hh, 1), 'sat': round(sv, 2),
                                       'val': round(vv, 2), 'share': round(share, 2),
                                       'chroma': round(chroma_frac, 2)}
