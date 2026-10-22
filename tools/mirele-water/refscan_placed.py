"""Placed-reference census for a block of Tamriel exterior cells.

(Originally written as refscan.py; renamed because a parallel lane took that
filename for a save-game ChangeForm scanner.)

Walks every ACTIVE plugin in the MO2 profile load order, descends into the
Tamriel worldspace GRUP, and pulls every placed reference (REFR/ACHR/ACRE/PGRE/
PMIS/PARW/PBAR/PBEA/PCON/PFLA/PHZD) that lives in the target cells, plus every
reference in any other cell context whose XY falls inside the target block
(this catches the worldspace persistent cell and grid-less CELL overrides).

Outputs JSON to refs.json in this directory.
"""
import json
import os
import struct
import zlib
from collections import defaultdict

ROOT = r"C:\1. AUTHORIA"
PROFILE = os.path.join(ROOT, "profiles", "DEEZ CS NUTZ")
MODS = os.path.join(ROOT, "mods")
STOCK = os.path.join(ROOT, "Stock Game", "Data")
OUT = os.path.join(ROOT, "_tools", "mirele-water", "refs.json")

TAMRIEL = 0x0000003C
TARGET_GRIDS = {(x, y) for x in (-1, 0, 1) for y in (-16, -15, -14)}

BLOCK_X0, BLOCK_X1 = -1 * 4096.0, 2 * 4096.0        # -4096 .. 8192
BLOCK_Y0, BLOCK_Y1 = -16 * 4096.0, -13 * 4096.0     # -65536 .. -53248

REF_TYPES = {b"REFR", b"ACHR", b"ACRE", b"PGRE", b"PMIS", b"PARW",
             b"PBAR", b"PBEA", b"PCON", b"PFLA", b"PHZD"}

FLAG_DELETED = 0x00000020
FLAG_DISABLED = 0x00000800
FLAG_COMPRESSED = 0x00040000
FLAG_PERSISTENT = 0x00000400


def mod_priority():
    out = []
    with open(os.path.join(PROFILE, "modlist.txt"), encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            if line.startswith("+"):
                out.append(line[1:])
    return out


def build_index():
    idx = {}
    for mod in reversed(mod_priority()):
        d = os.path.join(MODS, mod)
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for n in names:
            ln = n.lower()
            if ln.endswith((".esp", ".esm", ".esl")):
                idx[ln] = (os.path.join(d, n), mod)
    try:
        for n in os.listdir(STOCK):
            ln = n.lower()
            if ln.endswith((".esp", ".esm", ".esl")) and ln not in idx:
                idx[ln] = (os.path.join(STOCK, n), "<Stock Game>")
    except OSError:
        pass
    return idx


def load_order():
    active = set()
    with open(os.path.join(PROFILE, "plugins.txt"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("*"):
                active.add(line[1:].lower())
    order = []
    with open(os.path.join(PROFILE, "loadorder.txt"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower() in active:
                order.append(line)
    return order


def read_header(data):
    assert data[0:4] == b"TES4", data[0:4]
    size = struct.unpack_from("<I", data, 4)[0]
    flags = struct.unpack_from("<I", data, 8)[0]
    body = data[24:24 + size]
    masters = []
    pos = 0
    while pos + 6 <= len(body):
        st = body[pos:pos + 4]
        sl = struct.unpack_from("<H", body, pos + 4)[0]
        payload = body[pos + 6:pos + 6 + sl]
        if st == b"MAST":
            masters.append(payload.rstrip(b"\x00").decode("cp1252", "replace"))
        pos += 6 + sl
    return masters, bool(flags & 0x200), 24 + size


def subrecords(body):
    pos = 0
    override = None
    n = len(body)
    while pos + 6 <= n:
        st = body[pos:pos + 4]
        sl = struct.unpack_from("<H", body, pos + 4)[0]
        pos += 6
        if st == b"XXXX":
            override = struct.unpack_from("<I", body, pos)[0]
            pos += sl
            continue
        if override is not None:
            sl = override
            override = None
        yield st, body[pos:pos + sl]
        pos += sl


def rec_body(data, pos, size, flags):
    raw = data[pos + 24:pos + 24 + size]
    if flags & FLAG_COMPRESSED:
        try:
            return zlib.decompress(raw[4:])
        except zlib.error:
            return b""
    return raw


def parse_ref(sig, formid, flags, body):
    r = {"sig": sig.decode(), "formid": formid, "flags": flags,
         "deleted": bool(flags & FLAG_DELETED),
         "disabled": bool(flags & FLAG_DISABLED),
         "persistent": bool(flags & FLAG_PERSISTENT)}
    for st, pl in subrecords(body):
        if st == b"NAME" and len(pl) >= 4:
            r["base"] = struct.unpack_from("<I", pl, 0)[0]
        elif st == b"DATA" and len(pl) >= 24:
            x, y, z, rx, ry, rz = struct.unpack_from("<6f", pl, 0)
            r["pos"] = [x, y, z]
            r["rot"] = [rx, ry, rz]
        elif st == b"XSCL" and len(pl) >= 4:
            r["scale"] = struct.unpack_from("<f", pl, 0)[0]
        elif st == b"XESP" and len(pl) >= 8:
            r["xesp"] = list(struct.unpack_from("<II", pl, 0))
        elif st == b"XPRM" and len(pl) >= 12:
            r["xprm_bounds"] = list(struct.unpack_from("<3f", pl, 0))
        elif st == b"XEMI" and len(pl) >= 4:
            r["xemi"] = struct.unpack_from("<I", pl, 0)[0]
        elif st == b"XLKR" and len(pl) >= 8:
            r.setdefault("xlkr", []).append(list(struct.unpack_from("<II", pl, 0)))
        elif st == b"XLIG":
            r["xlig"] = True
        elif st in (b"XWCN", b"XWCU"):
            r["water_current"] = True
    return r


def cell_grid(body):
    for st, pl in subrecords(body):
        if st == b"XCLC" and len(pl) >= 8:
            return struct.unpack_from("<2i", pl, 0)
    return None


def cell_editorid(body):
    for st, pl in subrecords(body):
        if st == b"EDID":
            return pl.rstrip(b"\x00").decode("cp1252", "replace")
    return None


def scan_plugin(path, plugin_name):
    with open(path, "rb") as fh:
        data = fh.read()
    masters, esl, hdr_end = read_header(data)
    refs = []
    cells = {}
    target_cell_ids = set()
    persistent_cell_ids = set()
    n = len(data)

    def walk(start, end, ctx_cell):
        p = start
        while p + 24 <= end:
            sig = data[p:p + 4]
            if sig == b"GRUP":
                gsize, label, gtype = struct.unpack_from("<IIi", data, p + 4)
                if gsize < 24:
                    return
                a, b = p + 24, p + gsize
                if gtype == 0:
                    if label == 0x444C5257:
                        walk(a, b, None)
                elif gtype == 1:
                    if (label & 0x00FFFFFF) == (TAMRIEL & 0x00FFFFFF):
                        walk(a, b, None)
                elif gtype in (4, 5):
                    walk(a, b, None)
                elif gtype == 6:
                    if label in target_cell_ids or label in persistent_cell_ids:
                        walk(a, b, label)
                elif gtype in (8, 9, 10):
                    walk(a, b, ctx_cell)
                p += gsize
                continue
            size, flags, formid = struct.unpack_from("<III", data, p + 4)
            if sig == b"CELL":
                body = rec_body(data, p, size, flags)
                g = cell_grid(body)
                eid = cell_editorid(body)
                if g is not None and tuple(g) in TARGET_GRIDS:
                    target_cell_ids.add(formid)
                    cells[formid] = {"grid": list(g), "edid": eid, "flags": flags}
                elif g is None:
                    persistent_cell_ids.add(formid)
                    cells.setdefault(formid, {"grid": None, "edid": eid, "flags": flags})
            elif sig in REF_TYPES and ctx_cell is not None:
                body = rec_body(data, p, size, flags)
                r = parse_ref(sig, formid, flags, body)
                r["cell"] = ctx_cell
                if ctx_cell in target_cell_ids:
                    refs.append(r)
                else:
                    pp = r.get("pos")
                    if pp and BLOCK_X0 <= pp[0] <= BLOCK_X1 and BLOCK_Y0 <= pp[1] <= BLOCK_Y1:
                        refs.append(r)
            p += 24 + size

    walk(hdr_end, n, None)
    return refs, cells, masters, esl


def resolve_global(fid, masters, esl, plugin_name):
    mi = fid >> 24
    lo = fid & 0x00FFFFFF
    if esl and mi == 0xFE:
        return "%06X:%s" % (fid & 0x00000FFF, plugin_name)
    if mi < len(masters):
        return "%06X:%s" % (lo, masters[mi])
    return "%06X:%s" % (lo, plugin_name)


def main():
    idx = build_index()
    order = load_order()
    all_refs = defaultdict(list)
    cellrows, missing, errors = [], [], []
    scanned = 0
    for name in order:
        ent = idx.get(name.lower())
        if not ent:
            missing.append(name)
            continue
        path, mod = ent
        try:
            refs, cells, masters, esl = scan_plugin(path, name)
        except Exception as exc:                      # noqa
            errors.append("%s: %r" % (name, exc))
            continue
        scanned += 1
        for fid, ci in cells.items():
            if ci.get("grid"):
                cellrows.append({"plugin": name, "mod": mod,
                                 "cell": resolve_global(fid, masters, esl, name),
                                 "grid": ci["grid"], "edid": ci["edid"]})
        for r in refs:
            r["plugin"] = name
            r["mod"] = mod
            r["key"] = resolve_global(r["formid"], masters, esl, name)
            if "base" in r:
                r["base_key"] = resolve_global(r["base"], masters, esl, name)
            r["cell_key"] = resolve_global(r["cell"], masters, esl, name)
            all_refs[r["key"]].append(r)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"scanned": scanned, "missing": missing, "errors": errors,
                   "cells": cellrows, "refs": dict(all_refs)}, fh)
    print("scanned %d plugins, %d missing, %d errors" % (scanned, len(missing), len(errors)))
    print("unique refs: %d ; total placements: %d"
          % (len(all_refs), sum(len(v) for v in all_refs.values())))


if __name__ == "__main__":
    main()
