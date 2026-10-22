import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from landscan import read_masters, iter_records, subrecords
path = sys.argv[1]
types = {t.encode() for t in sys.argv[2].split(',')}
with open(path, 'rb') as f: data = f.read()
masters, start = read_masters(data)
for typ, formid, flags, body in iter_records(data, start, types):
    e = None; m = None
    for st, p in subrecords(body):
        if st == b'EDID': e = p.rstrip(b'\0').decode('cp1252', 'replace')
        if st == b'MODL': m = p.rstrip(b'\0').decode('cp1252', 'replace')
    print(f"{typ.decode()} {formid & 0xFFFFFF:06X} {e} -> {m}")
