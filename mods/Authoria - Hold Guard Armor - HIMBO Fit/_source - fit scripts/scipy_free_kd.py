"""Chunked brute-force k-nearest-neighbour + grid-accelerated ray casting (numpy only)."""
import numpy as np


def knn(query, ref, k=1, chunk=2048):
    query = np.asarray(query, np.float64); ref = np.asarray(ref, np.float64)
    rr = (ref ** 2).sum(1)
    D = np.empty((len(query), k)); I = np.empty((len(query), k), np.int64)
    for a in range(0, len(query), chunk):
        q = query[a:a + chunk]
        d2 = (q ** 2).sum(1)[:, None] + rr[None, :] - 2 * q @ ref.T
        np.maximum(d2, 0, out=d2)
        if k == 1:
            i = d2.argmin(1)[:, None]
        else:
            i = np.argpartition(d2, k, axis=1)[:, :k]
            o = np.take_along_axis(d2, i, 1).argsort(1)
            i = np.take_along_axis(i, o, 1)
        I[a:a + chunk] = i
        D[a:a + chunk] = np.sqrt(np.take_along_axis(d2, i, 1))
    return D, I


def nearest(query, ref):
    D, I = knn(query, ref, 1)
    return D[:, 0], I[:, 0]


class TriGrid:
    """uniform grid over triangles for ray queries."""
    def __init__(self, P, T, cell=1.5):
        self.P = np.asarray(P, np.float64); self.T = np.asarray(T, np.int64); self.cell = cell
        A = self.P[self.T]
        lo = np.floor(A.min(1) / cell).astype(np.int64); hi = np.floor(A.max(1) / cell).astype(np.int64)
        self.org = lo.min(0) - 1
        lo -= self.org; hi -= self.org
        self.dim = hi.max(0) + 3
        keys = []; tids = []
        span = hi - lo + 1
        for dx in range(span[:, 0].max()):
            for dy in range(span[:, 1].max()):
                for dz in range(span[:, 2].max()):
                    m = (dx < span[:, 0]) & (dy < span[:, 1]) & (dz < span[:, 2])
                    c = lo[m] + np.array([dx, dy, dz])
                    keys.append(self._key(c)); tids.append(np.where(m)[0])
        keys = np.concatenate(keys); tids = np.concatenate(tids)
        o = np.argsort(keys, kind='stable')
        self.keys = keys[o]; self.tids = tids[o]

    def _key(self, c):
        return (c[:, 0] * self.dim[1] + c[:, 1]) * self.dim[2] + c[:, 2]

    def cand(self, pts):
        c = np.floor(pts / self.cell).astype(np.int64) - self.org
        ok = np.all((c >= 0) & (c < self.dim), axis=1)
        k = self._key(np.where(ok[:, None], c, 0))
        a = np.searchsorted(self.keys, k, 'left'); b = np.searchsorted(self.keys, k, 'right')
        b = np.where(ok, b, a)
        return a, b

    def raycast(self, O, Dn, tmin, tmax, step=0.5):
        """for each ray return (t_first_positive_hit or inf, t_last_negative_hit or -inf) with hits in [tmin,tmax]."""
        O = np.asarray(O, np.float64); Dn = np.asarray(Dn, np.float64)
        n = len(O)
        ts = np.arange(tmin, tmax + 1e-9, step)
        tpos = np.full(n, np.inf); tneg = np.full(n, -np.inf)
        for a0 in range(0, n, 256):
            idx = np.arange(a0, min(n, a0 + 256))
            S = O[idx, None, :] + Dn[idx, None, :] * ts[None, :, None]  # (m, ns, 3)
            ray = np.repeat(idx, len(ts))
            # also probe the 6 face-neighbour offsets to avoid skipping cells
            pts = S.reshape(-1, 3)
            offs = np.array([[0, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) * (self.cell * 0.5)
            pairs_r = []; pairs_t = []
            for off in offs:
                a, b = self.cand(pts + off)
                cnt = b - a
                if cnt.sum() == 0:
                    continue
                rr = np.repeat(ray, cnt)
                starts = np.repeat(a, cnt)
                within = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
                pairs_r.append(rr); pairs_t.append(self.tids[starts + within])
            if not pairs_r:
                continue
            pr = np.concatenate(pairs_r); pt = np.concatenate(pairs_t)
            key = np.unique(pr * (len(self.T) + 1) + pt)
            pr = key // (len(self.T) + 1); pt = key % (len(self.T) + 1)
            V0 = self.P[self.T[pt, 0]]; V1 = self.P[self.T[pt, 1]]; V2 = self.P[self.T[pt, 2]]
            e1 = V1 - V0; e2 = V2 - V0
            d = Dn[pr]; o = O[pr]
            h = np.cross(d, e2); a_ = (e1 * h).sum(1)
            good = np.abs(a_) > 1e-12
            f = np.where(good, 1.0 / np.where(good, a_, 1), 0)
            s = o - V0
            u = f * (s * h).sum(1)
            q = np.cross(s, e1)
            v = f * (d * q).sum(1)
            t = f * (e2 * q).sum(1)
            hit = good & (u >= 0) & (v >= 0) & (u + v <= 1) & (t >= tmin) & (t <= tmax)
            pr = pr[hit]; t = t[hit]
            pos = t > 1e-6
            np.minimum.at(tpos, pr[pos], t[pos])
            np.maximum.at(tneg, pr[~pos], t[~pos])
        return tpos, tneg
