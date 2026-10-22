import struct

class R:
    def __init__(s,d): s.d=d; s.o=0
    def u32(s):
        v=struct.unpack('<I',s.d[s.o:s.o+4])[0]; s.o+=4; return v
    def i32(s):
        v=struct.unpack('<i',s.d[s.o:s.o+4])[0]; s.o+=4; return v
    def u16(s):
        v=struct.unpack('<H',s.d[s.o:s.o+2])[0]; s.o+=2; return v
    def u8(s):
        v=s.d[s.o]; s.o+=1; return v
    def f(s):
        v=struct.unpack('<f',s.d[s.o:s.o+4])[0]; s.o+=4; return v
    def sstr(s):
        n=s.u8(); v=s.d[s.o:s.o+n]; s.o+=n; return v
    def lstr(s):
        n=s.u32(); v=s.d[s.o:s.o+n]; s.o+=n; return v

def parse(path):
    d=open(path,'rb').read()
    i=d.index(b'\x0a'); hdr=d[:i]
    r=R(d); r.o=i+1
    ver=r.u32(); endian=r.u8(); uv=r.u32(); nb=r.u32()
    uv2=r.u32()
    exp=[r.sstr() for _ in range(3)]
    nt=r.u16()
    types=[r.lstr().decode('latin1') for _ in range(nt)]
    btypes=[r.u16() for _ in range(nb)]
    sizes=[r.u32() for _ in range(nb)]
    ns=r.u32(); maxs=r.u32()
    strs=[r.lstr().decode('latin1') for _ in range(ns)]
    ng=r.u32()
    for _ in range(ng): r.u32()
    blocks=[]
    p=r.o
    for k in range(nb):
        blocks.append((k, types[btypes[k]], p, sizes[k]))
        p+=sizes[k]
    return dict(hdr=hdr,ver=ver,uv=uv,uv2=uv2,exp=exp,types=types,strs=strs,blocks=blocks,data=d,endoff=p)
