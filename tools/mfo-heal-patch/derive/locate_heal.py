"""Locate HealExcludedWeapon + its call site in MFO.dll without symbols.

Chain: '[heal] ... excluded' fmt string  <- rip-relative ref inside the doHeal lambda body
       lambda body                       <- pointer in a std::function _Func_impl vftable (.rdata)
       vftable                           <- rip-relative ref in the function that builds the
                                            std::function == HealExcludedWeapon
       ServiceFollower                   <- refs "subsystem off" / "excursion cap"; contains the
                                            call to HealExcludedWeapon
Function bounds from .pdata RUNTIME_FUNCTION; every function disassembled from its own start.
"""
import struct, sys, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

DLL = r'C:\1. AUTHORIA\mods\marth Follower Overhaul\SKSE\Plugins\MFO.dll'
d = open(DLL, 'rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
opt = pe + 24
IB = struct.unpack_from('<Q', d, opt + 24)[0]
so = opt + struct.unpack_from('<H', d, pe + 20)[0]
secs = {}
for i in range(nsec):
    n = d[so + i * 40:so + i * 40 + 8].rstrip(b'\0').decode()
    vs, va, rs, ro = struct.unpack_from('<IIII', d, so + i * 40 + 8)
    secs[n] = (va, vs, ro, rs)


def rva2off(r):
    for n, (va, vs, ro, rs) in secs.items():
        if va <= r < va + max(vs, rs):
            return r - va + ro
    return None


def off2rva(o):
    for n, (va, vs, ro, rs) in secs.items():
        if ro <= o < ro + rs:
            return o - ro + va
    return None


pva, pvs, pro, prs = secs['.pdata']
funcs = []
for k in range(pvs // 12):
    b, e, u = struct.unpack_from('<III', d, pro + k * 12)
    if b and e > b:
        funcs.append((b, e))
funcs.sort()


def func_of(rva):
    lo, hi = 0, len(funcs) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        b, e = funcs[m]
        if rva < b:
            hi = m - 1
        elif rva >= e:
            lo = m + 1
        else:
            return (b, e)
    return None


def all_str_rvas(s):
    out, i = [], 0
    while True:
        i = d.find(s, i)
        if i < 0:
            return out
        out.append(off2rva(i))
        i += 1


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
tva, tvs, tro, trs = secs['.text']

# Disassemble every .pdata function from its start; collect rip-relative refs and calls.
lea_refs = {}
calls = {}
insns_by_func = {}
for (b, e) in funcs:
    off = rva2off(b)
    if off is None:
        continue
    lst = []
    for ins in md.disasm(d[off:off + (e - b)], b):
        lst.append(ins)
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                tgt = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFF
                lea_refs.setdefault(tgt, []).append(ins.address)
        if ins.mnemonic in ('call', 'jmp') and ins.operands and ins.operands[0].type == X86_OP_IMM:
            calls[ins.address] = ins.operands[0].imm & 0xFFFFFFFF
    insns_by_func[(b, e)] = lst

print('functions:', len(funcs), ' rip-refs:', sum(len(v) for v in lea_refs.values()), ' calls:', len(calls))


def refs_to(rva):
    return lea_refs.get(rva, [])


def funcs_referencing(rvas):
    out = set()
    for r in rvas:
        for a in refs_to(r):
            f = func_of(a)
            if f:
                out.add(f)
    return out


# 1. lambda body via the heal fmt string
heal_strs = all_str_rvas(b"[heal] {:08X} excluded '{}' -> {}, {} {}x\0")
print('heal fmt string RVAs:', ['%X' % r for r in heal_strs])
lam = funcs_referencing(heal_strs)
print('lambda body function(s):', ['%X-%X' % f for f in lam])

# 2. vftable pointing at the lambda body -> constructing function
rva_r, vs_r, ro_r, rs_r = secs['.rdata']
rdata = d[ro_r:ro_r + rs_r]
ctor_funcs = set()
for (lb, le) in sorted(lam):
    needle = struct.pack('<Q', IB + lb)
    i = 0
    while True:
        i = rdata.find(needle, i)
        if i < 0:
            break
        slot_rva = rva_r + i
        for slot in range(0, 8):
            vft = slot_rva - slot * 8
            for a in refs_to(vft):
                f = func_of(a)
                print('  vftable %X (slot %d) referenced at %X in %s' % (vft, slot, a, '%X-%X' % f if f else '?'))
                if f:
                    ctor_funcs.add(f)
        i += 8
# also functions that call the lambda body directly (VR path: doHeal())
for a, t in calls.items():
    if any(t == lb for (lb, le) in lam):
        f = func_of(a)
        print('  direct call to lambda at %X in %s' % (a, '%X-%X' % f if f else '?'))
        if f:
            ctor_funcs.add(f)
print('HealExcludedWeapon candidate(s):', ['%X-%X' % f for f in ctor_funcs])

# 3. ServiceFollower via its strings
sf_strs = all_str_rvas(b'subsystem off\0') + all_str_rvas(b'excursion cap\0')
sf = funcs_referencing(sf_strs)
print('ServiceFollower candidate(s):', ['%X-%X' % f for f in sf])

# 4. call from ServiceFollower into a HealExcludedWeapon candidate
for f in sf:
    for ins in insns_by_func[f]:
        t = calls.get(ins.address)
        if t is not None and any(b <= t < e for (b, e) in ctor_funcs):
            print('CALL SITE: %X  %s %s   -> HealExcludedWeapon %X   (file off %X)' % (
                ins.address, ins.mnemonic, ins.op_str, t, rva2off(ins.address)))
            print('   bytes:', d[rva2off(ins.address):rva2off(ins.address) + ins.size].hex())

# 5. dump HealExcludedWeapon disassembly with annotations
def annotate(ins):
    s = '%X  %-22s %-6s %s' % (ins.address, d[rva2off(ins.address):rva2off(ins.address) + ins.size].hex(), ins.mnemonic, ins.op_str)
    t = calls.get(ins.address)
    if t is not None:
        f = func_of(t)
        s += '    ; -> %X' % t + (' [fn %X-%X]' % f if f else '')
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            tgt = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFF
            o = rva2off(tgt)
            if o is not None:
                raw = d[o:o + 24]
                txt = raw.split(b'\0')[0]
                if txt and all(32 <= c < 127 for c in txt):
                    s += '    ; "%s"' % txt.decode()
                else:
                    s += '    ; [%X]' % tgt
    return s

out = {}
for f in sorted(ctor_funcs):
    print()
    print('===== HealExcludedWeapon %X-%X (%d bytes, file off %X) =====' % (f[0], f[1], f[1] - f[0], rva2off(f[0])))
    lines = [annotate(i) for i in insns_by_func[f]]
    out['%X-%X' % f] = lines
    for l in lines:
        print(l)
json.dump({'ib': IB, 'heal': ['%X-%X' % f for f in ctor_funcs], 'lambda': ['%X-%X' % f for f in lam],
           'servicefollower': ['%X-%X' % f for f in sf]},
          open(r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\e0cc5ba1-5c07-451b-b121-b04943705a08\scratchpad\heal_loc.json', 'w'), indent=1)
