"""xref.py <dll> <string> [before] [after]
Find rip-relative references to a string and print disassembly around each reference.
Also annotates other string references seen in the window."""
import sys, re, pefile, capstone

dll, needle = sys.argv[1], sys.argv[2].encode()
before = int(sys.argv[3],0) if len(sys.argv) > 3 else 0x200
after = int(sys.argv[4],0) if len(sys.argv) > 4 else 0x200
pe = pefile.PE(dll)
data = pe.get_memory_mapped_image()
base = pe.OPTIONAL_HEADER.ImageBase
text = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
tva, tsz = text.VirtualAddress, text.Misc_VirtualSize
code = data[tva:tva + tsz]

targets = [m.start() for m in re.finditer(re.escape(needle), data)]
print('string RVAs', [hex(t) for t in targets])
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False

def strat(rva):
    if 0 <= rva < len(data):
        s = data[rva:rva + 80]
        e = s.find(b'\0')
        s = s[:e if e >= 0 else 80]
        if len(s) >= 4 and all(32 <= c < 127 for c in s):
            return s.decode()
    return None

# scan for rip-relative lea/mov to targets: 4-byte disp at i, next ip at i+4 (+imm)
hits = []
for i in range(len(code) - 4):
    disp = int.from_bytes(code[i:i + 4], 'little', signed=True)
    for extra in (0,):
        nxt = tva + i + 4 + extra
        if nxt + disp in targets:
            hits.append(tva + i)
print('refs', [hex(h) for h in hits])
for h in hits[: int(sys.argv[5]) if len(sys.argv) > 5 else 4]:
    start = max(tva, h - before)
    print('=' * 20, hex(h))
    # sync: disassemble from start, may desync briefly
    for ins in md.disasm(code[start - tva:h - tva + after], start):
        ann = ''
        m = re.search(r'\[rip ([+-]) (0x[0-9a-f]+)\]', ins.op_str)
        if m:
            t = ins.address + ins.size + (int(m.group(2), 16) * (1 if m.group(1) == '+' else -1))
            s = strat(t)
            ann = f'   ; {hex(t)} {s!r}' if s else f'   ; {hex(t)}'
        print(f'{ins.address:08x}: {ins.mnemonic} {ins.op_str}{ann}')
