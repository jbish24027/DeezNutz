"""Print every thread of a minidump with its RIP/RSP as module+offset, plus a CrashLogger-style stack scan
(return addresses found on the stack, resolved to module+offset).  Usage: python read_dump.py hang.dmp [max-frames]
Engine offsets can then be read from the decrypted exe (see memory: steamstub-exe-decrypt-for-disasm)."""
import sys, struct, bisect
d = open(sys.argv[1], 'rb').read(); maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 24
sig, ver, nstreams, rva = struct.unpack_from("<4sIII", d, 0)
streams = {struct.unpack_from("<III", d, rva + i*12)[0]: struct.unpack_from("<III", d, rva + i*12)[1:] for i in range(nstreams)}
# modules
loc = streams[4][1]; n = struct.unpack_from("<I", d, loc)[0]; mods = []
for j in range(n):
    base, size = struct.unpack_from("<QI", d, loc + 4 + j*108); nrva = struct.unpack_from("<I", d, loc + 4 + j*108 + 0x14)[0]
    ln = struct.unpack_from("<I", d, nrva)[0]; nm = d[nrva+4:nrva+4+ln].decode('utf-16-le', 'replace').split(chr(92))[-1]
    mods.append((base, size, nm))
mods.sort(); bases = [m[0] for m in mods]
def sym(a):
    i = bisect.bisect_right(bases, a) - 1
    if i >= 0 and a < mods[i][0] + mods[i][1]: return "%s+%X" % (mods[i][2], a - mods[i][0])
    return None
# memory list (for stack bytes)
mloc = streams[5][1]; mn = struct.unpack_from("<I", d, mloc)[0]; mem = []
for j in range(mn):
    start, sz, drva = struct.unpack_from("<QII", d, mloc + 4 + j*16)
    mem.append((start, sz, drva))
def read(addr, size):
    for s, sz, r in mem:
        if s <= addr < s + sz: return d[r + (addr - s): r + (addr - s) + min(size, s + sz - addr)]
    return b""
# threads
tloc = streams[3][1]; tn = struct.unpack_from("<I", d, tloc)[0]
print("threads:", tn, " modules:", n)
for j in range(tn):
    o = tloc + 4 + j*48
    tid, susp, prio, teb = struct.unpack_from("<IIIQ", d, o)
    sstart, ssz, srva = struct.unpack_from("<QII", d, o + 0x18)
    csz, crva = struct.unpack_from("<II", d, o + 0x28)
    ctx = d[crva:crva+csz]; rip = struct.unpack_from("<Q", ctx, 0xF8)[0]; rsp = struct.unpack_from("<Q", ctx, 0x98)[0]
    print("\n--- thread %d  RIP %s  RSP %X  stack %X..%X ---" % (tid, sym(rip) or "%X" % rip, rsp, sstart, sstart + ssz))
    st = read(rsp, min(0x4000, sstart + ssz - rsp)); k = 0
    for i in range(0, len(st) - 7, 8):
        v = struct.unpack_from("<Q", st, i)[0]; s = sym(v)
        if s and not s.startswith(("ntdll", "KERNELBASE", "KERNEL32", "win32u", "USER32")) or (s and k < 3):
            print("   [rsp+%04X] %s" % (i, s)); k += 1
            if k >= maxf: break
