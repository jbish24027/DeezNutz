"""Generic Helga-style cloth rig for a mesh region: a grid of chain bones (columns around an axis,
rows along it), placed on the mesh surface, parented row-by-row under an anchor bone, and a smooth
(multi-bone) skinning of the region's vertices onto that grid.

Modelled on Fuse00's Helga dress rig (14 columns x 9 rows, ~4 bones per vertex spread over ~2
columns and ~3 rows, bone frame: local x = along the chain, local z = outward normal, local y =
tangent). Works for a skirt (axis = vertical through the pelvis, rows going down) and for a bell
sleeve (axis = the forearm, rows going toward the hand).
"""
import numpy as np

def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


class ClothRig:
    def __init__(self, prefix, columns, origin, axis, ref, parent, rows_t, spacing_t):
        """prefix: bone name prefix; columns: list of column names (evenly spaced angles, first at
        phi=0 = ref direction); origin/axis: the cylinder axis (axis = chain direction); ref: the
        phi=0 direction (perpendicularised to axis); parent: the anchor body bone; rows_t: the t
        (along-axis) value of every row, row 0 = static anchor ring; spacing_t: nominal row spacing."""
        self.prefix = prefix
        self.columns = list(columns)
        self.ncol = len(columns)
        self.origin = np.asarray(origin, dtype=float)
        self.u = unit(axis)
        r = np.asarray(ref, dtype=float)
        r = r - self.u * (r @ self.u)
        self.e1 = unit(r)
        self.e2 = np.cross(self.u, self.e1)
        self.parent = parent
        self.rows_t = list(rows_t)
        self.nrow = len(rows_t)
        self.spacing_t = spacing_t
        self.dphi = 2 * np.pi / self.ncol
        self.radius = None           # [row][col] surface radius, filled by fit()

    # -------------------------------------------------------------- geometry
    def name(self, c, r):
        return '%s_%s_%02d' % (self.prefix, self.columns[c], r)

    def cyl(self, P):
        """cylindrical coords of points: t along the axis, r from the axis, phi (0..2pi)."""
        D = P - self.origin
        t = D @ self.u
        Q = D - np.outer(t, self.u)
        r = np.linalg.norm(Q, axis=1)
        phi = np.arctan2(Q @ self.e2, Q @ self.e1) % (2 * np.pi)
        return t, r, phi

    def fit(self, P, mask):
        """Measure the surface radius per (row, column) cell from the region's vertices."""
        t, r, phi = self.cyl(P[mask])
        R = np.full((self.nrow, self.ncol), np.nan)
        for ri, tr in enumerate(self.rows_t):
            for ci in range(self.ncol):
                dphi = np.abs((phi - ci * self.dphi + np.pi) % (2 * np.pi) - np.pi)
                m = (dphi <= self.dphi * 0.75) & (np.abs(t - tr) <= self.spacing_t * 0.75)
                if m.sum() >= 3:
                    R[ri, ci] = r[m].mean()
        # fill holes: from the same row's neighbours, else from the neighbouring rows
        for ri in range(self.nrow):
            row = R[ri]
            if np.all(np.isnan(row)):
                continue
            for ci in range(self.ncol):
                if np.isnan(row[ci]):
                    for d in range(1, self.ncol):
                        cands = [row[(ci - d) % self.ncol], row[(ci + d) % self.ncol]]
                        cands = [x for x in cands if not np.isnan(x)]
                        if cands:
                            row[ci] = np.mean(cands); break
        for ri in range(self.nrow):
            if np.all(np.isnan(R[ri])):
                src = [k for k in range(self.nrow) if not np.all(np.isnan(R[k]))]
                near = min(src, key=lambda k: abs(k - ri))
                R[ri] = R[near]
        self.radius = R
        return R

    def bone_world(self, c, r):
        """(R 3x3, T) world transform of bone (col c, row r). Frame: x = chain dir, z = outward, y = z x x."""
        phi = c * self.dphi
        out = np.cos(phi) * self.e1 + np.sin(phi) * self.e2
        T = self.origin + self.u * self.rows_t[r] + out * self.radius[r, c]
        x = self.u; z = out; y = np.cross(z, x)
        R = np.stack([x, y, z], axis=1)           # columns = local axes in world
        return R, T

    def bones(self):
        """[(name, parent_name, R, T, row)] for every bone, row 0 first."""
        out = []
        for r in range(self.nrow):
            for c in range(self.ncol):
                par = self.parent if r == 0 else self.name(c, r - 1)
                R, T = self.bone_world(c, r)
                out.append((self.name(c, r), par, R, T, r))
        return out

    # -------------------------------------------------------------- skinning
    def weights(self, P, sig_phi=0.55, sig_t=0.9, keep=4):
        """Smooth grid weights for points P: gaussian in (phi, t) over the nearest cells.
        Points before row 0 (t < rows_t[0]) stick to row 0; past the last row, to the last row."""
        t, r, phi = self.cyl(P)
        out = []
        rows_t = np.array(self.rows_t)
        for k in range(len(P)):
            acc = {}
            # column weights
            dphi = np.abs((phi[k] - np.arange(self.ncol) * self.dphi + np.pi) % (2 * np.pi) - np.pi)
            wc = np.exp(-(dphi / (sig_phi * self.dphi)) ** 2)
            tk = min(max(t[k], rows_t[0]), rows_t[-1])
            wr = np.exp(-((tk - rows_t) / (sig_t * self.spacing_t)) ** 2)
            for ri in np.argsort(-wr)[:3]:
                for ci in np.argsort(-wc)[:2]:
                    acc[(ci, ri)] = wc[ci] * wr[ri]
            items = sorted(acc.items(), key=lambda kv: -kv[1])[:keep]
            tot = sum(w for _, w in items)
            out.append({self.name(ci, ri): w / tot for (ci, ri), w in items})
        return out


def blend(rig_w, base_w, d, min_w=0.02):
    """Mix rig weights (share d) with the vertex's existing NON-cloth weights (share 1-d)."""
    out = {}
    if d < 1.0 and base_w:
        tot = sum(base_w.values())
        for b, w in base_w.items():
            out[b] = out.get(b, 0.0) + w / tot * (1.0 - d)
    if d > 0.0:
        for b, w in rig_w.items():
            out[b] = out.get(b, 0.0) + w * d
    out = {b: w for b, w in out.items() if w >= min_w}
    tot = sum(out.values())
    return {b: w / tot for b, w in out.items()}


def stats(wmap, prefix):
    import re
    ncol = []; nrow = []; top = []
    for w in wmap:
        cs = set(); rs = set()
        for b, v in w.items():
            m = re.match(re.escape(prefix) + r'_(\w+)_(\d\d)$', b)
            if m and v > 0.02:
                cs.add(m.group(1)); rs.add(m.group(2))
        if cs:
            ncol.append(len(cs)); nrow.append(len(rs)); top.append(max(w.values()))
    if not ncol:
        return 'no rig weights'
    return 'rig verts %d: columns/vert %.2f rows/vert %.2f top-weight %.2f' % (len(ncol), np.mean(ncol), np.mean(nrow), np.mean(top))
