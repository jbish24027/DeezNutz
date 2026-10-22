"""addrrefs.py <dll> <rva hex> [ctx]  - list every instruction that references a data RVA (rip-relative)."""
import sys, re, pefile, capstone
pe = pefile.PE(sys.argv[1]); target = int(sys.argv[2], 16); ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
data = pe.get_memory_mapped_image()
text = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
tva = text.VirtualAddress; code = data[tva:tva + text.Misc_VirtualSize]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cands = set()
for i in range(len(code) - 4):
    disp = int.from_bytes(code[i:i+4], 'little', signed=True)
    for ilen_after in range(0, 5):  # imm bytes after disp
        if tva + i + 4 + ilen_after + disp == target:
            cands.add((tva + i, ilen_after))
for pos, extra in sorted(cands):
    for back in range(2, 8):
        st = pos - back
        insns = list(md.disasm(code[st - tva: st - tva + 16], st, count=1))
        if insns and insns[0].address + insns[0].size == pos + 4 + extra and 'rip' in insns[0].op_str:
            # print some context: re-disassemble from a bit before
            pre = list(md.disasm(code[st - tva - 24: st - tva + 40], st - 24))
            print('----', hex(st))
            for x in pre:
                if x.address >= st - 24:
                    print(f'  {x.address:08x}: {x.mnemonic} {x.op_str}' + ('   <==' if x.address == st else ''))
            break
