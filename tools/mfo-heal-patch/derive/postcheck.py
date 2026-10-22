import sys, hashlib, glob
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
live = r'C:\1. AUTHORIA\mods\marth Follower Overhaul\SKSE\Plugins\MFO.dll'
bks = sorted(glob.glob(r'C:\1. AUTHORIA\_tools\mfo-heal-patch\backup\MFO.dll.stock-*'))
stock = bks[-1]
print('backup used:', stock)
def insns(p):
    d = open(p, 'rb').read()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    off = 0x9F340 - 0x1000 + 0x400
    return d, [(i.address, i.mnemonic, i.op_str) for i in md.disasm(d[off:off + (0x9F5C8 - 0x9F340)], 0x9F340)]
ds, a = insns(stock); dl, b = insns(live)
print('stock sha256', hashlib.sha256(ds).hexdigest())
print('live  sha256', hashlib.sha256(dl).hexdigest())
print('byte diffs at', [hex(i) for i in range(len(ds)) if ds[i] != dl[i]])
sa, sb = set(a), set(b)
print('instruction count stock/live:', len(a), len(b))
print('removed:', sorted(sa - sb))
print('added:  ', sorted(sb - sa))
