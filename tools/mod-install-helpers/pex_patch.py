"""Minimal Skyrim PEX walker: find PROPSET <prop> = <float> inside a function and patch the float.
Usage: python pex_patch.py <in.pex> <out.pex> <function_name> <property_name> <old_float> <new_float>
Prints every match found; patches all matches (expects exactly 1 unless --all).
"""
import struct, sys

ARGC = {0:0,1:3,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:3,10:2,11:2,12:2,13:2,14:2,15:3,16:3,17:3,18:3,19:3,
        20:1,21:2,22:2,23:3,24:2,25:3,26:1,27:3,28:3,29:3,30:2,31:2,32:3,33:3,34:4,35:4}
VARARG = {23, 24, 25}


class R:
    def __init__(self, data):
        self.d = data
        self.p = 0
    def u8(self):
        v = self.d[self.p]; self.p += 1; return v
    def u16(self):
        v = struct.unpack_from('>H', self.d, self.p)[0]; self.p += 2; return v
    def u32(self):
        v = struct.unpack_from('>I', self.d, self.p)[0]; self.p += 4; return v
    def i32(self):
        v = struct.unpack_from('>i', self.d, self.p)[0]; self.p += 4; return v
    def f32(self):
        v = struct.unpack_from('>f', self.d, self.p)[0]; self.p += 4; return v
    def u64(self):
        v = struct.unpack_from('>Q', self.d, self.p)[0]; self.p += 8; return v
    def s(self):
        n = self.u16(); v = self.d[self.p:self.p+n].decode('latin-1'); self.p += n; return v


def read_vardata(r):
    t = r.u8()
    off = r.p
    if t == 0:
        return ('null', None, off)
    if t == 1:
        return ('id', r.u16(), off)
    if t == 2:
        return ('str', r.u16(), off)
    if t == 3:
        return ('int', r.i32(), off)
    if t == 4:
        return ('float', r.f32(), off)
    if t == 5:
        return ('bool', r.u8(), off)
    raise ValueError('bad vardata type %d at %d' % (t, off))


def parse(data):
    r = R(data)
    magic = r.u32()
    assert magic == 0xFA57C0DE, hex(magic)
    major, minor = r.u8(), r.u8()
    gameid = r.u16()
    r.u64()  # compile time
    src = r.s(); user = r.s(); machine = r.s()
    n = r.u16()
    strings = [r.s() for _ in range(n)]
    has_debug = r.u8()
    if has_debug:
        r.u64()
        fcount = r.u16()
        for _ in range(fcount):
            r.u16(); r.u16(); r.u16(); r.u8()
            ic = r.u16()
            for _ in range(ic):
                r.u16()
    nflags = r.u16()
    for _ in range(nflags):
        r.u16(); r.u8()
    nobj = r.u16()
    funcs = []  # (objname, statename, funcname, [instructions])
    for _ in range(nobj):
        oname = strings[r.u16()]
        size_pos = r.p
        size = r.u32()
        end = size_pos + size  # size includes the 4-byte size field itself
        r.u16()  # parent
        r.u16()  # docstring
        r.u32()  # userflags
        r.u16()  # autostate
        nvar = r.u16()
        for _ in range(nvar):
            r.u16(); r.u16(); r.u32(); read_vardata(r)
        nprop = r.u16()
        for _ in range(nprop):
            r.u16(); r.u16(); r.u16(); r.u32()
            flags = r.u8()
            if flags & 4:
                r.u16()
            else:
                if flags & 1:
                    read_function(r, strings)
                if flags & 2:
                    read_function(r, strings)
        nstates = r.u16()
        for _ in range(nstates):
            sname = strings[r.u16()]
            nf = r.u16()
            for _ in range(nf):
                fname = strings[r.u16()]
                ins = read_function(r, strings)
                funcs.append((oname, sname, fname, ins))
        assert r.p == end, (r.p, end)
    return strings, funcs


def read_function(r, strings):
    r.u16(); r.u16(); r.u32(); r.u8()
    nparams = r.u16()
    for _ in range(nparams):
        r.u16(); r.u16()
    nlocals = r.u16()
    for _ in range(nlocals):
        r.u16(); r.u16()
    ni = r.u16()
    ins = []
    for _ in range(ni):
        op = r.u8()
        args = []
        for _ in range(ARGC[op]):
            args.append(read_vardata(r))
        if op in VARARG:
            cnt = read_vardata(r)
            args.append(cnt)
            for _ in range(cnt[1]):
                args.append(read_vardata(r))
        ins.append((op, args))
    return ins


if __name__ == '__main__':
    inp, outp, fname, pname, oldf, newf = sys.argv[1:7]
    oldf = float(oldf); newf = float(newf)
    data = bytearray(open(inp, 'rb').read())
    strings, funcs = parse(bytes(data))
    matches = []
    for oname, sname, fn, ins in funcs:
        if fn.lower() != fname.lower():
            continue
        for i, (op, args) in enumerate(ins):
            if op == 29:  # propset name obj value
                pn = strings[args[0][1]] if args[0][0] in ('str', 'id') else None
                if not pn or pn.lower() != pname.lower():
                    continue
                # literal directly in propset
                if args[2][0] == 'float' and abs(args[2][1] - oldf) < 1e-6:
                    matches.append((oname, sname, fn, args[2][2]))
                # or via a temp assigned just before: ASSIGN temp <float>
                elif args[2][0] == 'id' and i > 0:
                    pop, pargs = ins[i - 1]
                    if pop == 13 and pargs[0][0] == 'id' and pargs[0][1] == args[2][1] and pargs[1][0] == 'float' and abs(pargs[1][1] - oldf) < 1e-6:
                        matches.append((oname, sname, fn, pargs[1][2]))
    print('matches:', matches)
    if len(matches) != 1 and '--all' not in sys.argv:
        print('expected exactly 1 match; aborting')
        sys.exit(2)
    for m in matches:
        off = m[3]
        struct.pack_into('>f', data, off, newf)
        print('patched float at offset', off, '->', newf)
    open(outp, 'wb').write(data)
    # verify by re-parse
    strings2, funcs2 = parse(bytes(data))
    for oname, sname, fn, ins in funcs2:
        if fn.lower() == fname.lower():
            for i, (op, args) in enumerate(ins):
                if op == 29 and args[0][0] in ('str', 'id') and strings2[args[0][1]].lower() == pname.lower():
                    print('after patch:', oname, sname, fn, 'prev=', ins[i - 1] if i > 0 else None, 'propset=', args)
    print('written', outp, 'size', len(data))
