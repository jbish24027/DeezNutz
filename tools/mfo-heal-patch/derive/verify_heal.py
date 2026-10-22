"""Verify the three callees in HealExcludedWeapon's guard and the patch-site safety."""
import struct, hashlib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

DLL = r'C:\1. AUTHORIA\mods\marth Follower Overhaul\SKSE\Plugins\MFO.dll'
d = open(DLL, 'rb').read()
print('size', len(d), 'sha256', hashlib.sha256(d).hexdigest())
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
opt = pe + 24
so = opt + struct.unpack_from('<H', d, pe + 20)[0]
secs = {}
for i in range(nsec):
    n = d[so + i * 40:so + i * 40 + 8].rstrip(b'\0').decode()
    vs, va, rs, ro = struct.unpack_from('<IIII', d, so + i * 40 + 8)
    secs[n] = (va, vs, ro, rs)
tva, tvs, tro, trs = secs['.text']
def rva2off(r): return r - tva + tro
pva, pvs, pro, prs = secs['.pdata']
funcs = sorted((b, e) for k in range(pvs // 12) for (b, e, u) in [struct.unpack_from('<III', d, pro + k * 12)] if b and e > b)
def func_of(rva):
    for b, e in funcs:
        if b <= rva < e: return (b, e)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

def dump(name, rva, limit=None):
    f = func_of(rva)
    b, e = f if f else (rva, rva + 0x40)
    print('\n== %s  %X-%X (%d bytes) ==' % (name, b, e, e - b))
    n = 0
    for ins in md.disasm(d[rva2off(b):rva2off(e)], b):
        s = '%X  %-20s %-6s %s' % (ins.address, d[rva2off(ins.address):rva2off(ins.address) + ins.size].hex(), ins.mnemonic, ins.op_str)
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                s += '   ; [%X]' % ((ins.address + ins.size + op.mem.disp) & 0xFFFFFFFF)
        print(s); n += 1
        if limit and n >= limit: print('  ...'); break

dump('DA080 (expect Catalog::IsExcluded = g_excluded.contains)', 0xDA080, 40)
dump('B2D20 (expect IsCreatureWeapon: formFlags bit2 || IsKnownCreatureWeapon)', 0xB2D20)
dump('E9110 (expect Actor::GetEquippedObject(bool left))', 0xE9110)

# every branch target inside HealExcludedWeapon
print('\n== jump targets inside HealExcludedWeapon 9F340-9F5C8 that land in 9F395..9F3AD ==')
hits = []
for ins in md.disasm(d[rva2off(0x9F340):rva2off(0x9F5C8)], 0x9F340):
    if ins.mnemonic.startswith('j') and ins.operands and ins.operands[0].type == X86_OP_IMM:
        t = ins.operands[0].imm & 0xFFFFFFFF
        if 0x9F395 <= t <= 0x9F3AD:
            hits.append('%X %s -> %X' % (ins.address, ins.mnemonic, t))
print(hits if hits else 'none (only 9F3AD is a landing pad, from 9F384/9F393)')

# who else calls DA080 (IsExcluded) and B2D20 (IsCreatureWeapon)?  -> proves identity by fan-in
def callers(target):
    out = []
    for (b, e) in funcs:
        for ins in md.disasm(d[rva2off(b):rva2off(e)], b):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM and (ins.operands[0].imm & 0xFFFFFFFF) == target:
                out.append('%X-%X' % (b, e)); break
    return out
print('\ncallers of DA080:', len(callers(0xDA080)), 'functions')
print('callers of B2D20:', len(callers(0xB2D20)), 'functions')

# patch site bytes + context
off = rva2off(0x9F39F)
print('\npatch site file offset 0x%X  bytes: %s  (expect 7518)' % (off, d[off:off + 2].hex()))
print('context  -16..+16:', d[off - 16:off + 16].hex())
# relocation check: any .reloc entry touching 9F39F..9F3A0?
rva_rl, vs_rl, ro_rl, rs_rl = secs['.reloc']
p = ro_rl; touched = []
while p < ro_rl + vs_rl:
    page, sz = struct.unpack_from('<II', d, p)
    if sz < 8: break
    for k in range((sz - 8) // 2):
        ent = struct.unpack_from('<H', d, p + 8 + k * 2)[0]
        typ, o = ent >> 12, ent & 0xFFF
        if typ and 0x9F390 <= page + o <= 0x9F3B0: touched.append(hex(page + o))
    p += sz
print('relocations touching patch region:', touched or 'none')
