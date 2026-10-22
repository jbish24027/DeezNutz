"""Python port of AutoCombatLink.cpp's signature scan, run against the AutoCombat.dll file
mapped as an image. Prints the RVAs it resolves so they can be compared with the hand
disassembly (pilot 0xF7894, enabled 0xF7763 for the 2026-10 build)."""
import sys, struct, pefile

pe = pefile.PE(sys.argv[1])
img = pe.get_memory_mapped_image()
secs = []
for s in pe.sections:
    size = max(s.Misc_VirtualSize, s.SizeOfRawData)
    secs.append((s.VirtualAddress, s.VirtualAddress + size, s.Characteristics))
EXEC, WRITE = 0x20000000, 0x80000000

def sec_of(a):
    for b, e, f in secs:
        if b <= a < e:
            return (b, e, f)
def writable(a):
    s = sec_of(a)
    return s and (s[2] & WRITE) and not (s[2] & EXEC)
B = lambda a: img[a]
D = lambda a: struct.unpack_from('<i', img, a)[0]
rip = lambda m: (m & 0xC7) == 0x05

def find_string(t):
    n = t.encode() + b'\0'; out = []
    for b, e, f in secs:
        if f & EXEC: continue
        i = img.find(n, b, e)
        while i != -1:
            out.append(i); i = img.find(n, i + 1, e)
    return out

def lea_refs(target):
    out = []
    for b, e, f in secs:
        if not (f & EXEC): continue
        for p in range(b, e - 7):
            if img[p] in (0x48, 0x4C) and img[p+1] == 0x8D and rip(img[p+2]) and p + 7 + D(p+3) == target:
                out.append(p)
    return out

def movzx(a):
    if not sec_of(a) or not sec_of(a+6): return None
    if B(a) != 0x0F or B(a+1) != 0xB6 or not rip(B(a+2)): return None
    t = a + 7 + D(a+3)
    return t if writable(t) else None

def before(f, w):
    for back in range(7, w + 1):
        t = movzx(f - back)
        if t: return t

def toggled_after(f, w):
    for fwd in range(w):
        at = f + fwd; t = movzx(at)
        if not t: continue
        sete = False
        for k in range(7, 0x30):
            x = at + k
            if B(x) == 0x0F and B(x+1) == 0x94: sete = True
            if B(x) == 0x86 and rip(B(x+1)) and x + 6 + D(x+2) == t:
                if sete: return t
                break

def near(text, toggle):
    for s in find_string(text):
        for l in lea_refs(s):
            t = toggled_after(l, 0x200) if toggle else before(l, 0x40)
            if t: return t

a = near("Auto-pilot is active.", False)
b = near("auto-pilot turned off", False)
c = near("Auto Combat: ON", True)
print('pilot(menu)', hex(a or 0), 'pilot(stop)', hex(b or 0), 'enabled', hex(c or 0))
print('initial bytes', img[a] if a else None, img[c] if c else None)
