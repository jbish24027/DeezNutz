"""Read-only: MoT MCM switch state in the PICTA saves (enable-state changeforms of the MoT parent markers).
Run with python -B so nothing is written next to the borrowed parser."""
import sys, glob, os
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import load, parse_body
from changeforms import read_formid_array, parse_change_forms, resolve, decompress, decode_initial

SAVES = sorted(glob.glob(r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ - PICTA\saves\*.ess'), key=os.path.getmtime)
TARGETS = {0x005B1A: 'VolMist parent A (InitiallyDisabled)', 0x005B1B: 'VolMist parent B (InitiallyDisabled)',
           0x005B1C: 'VolMist parent C (InitiallyDisabled)', 0x005B1D: 'k747AnimatedDistantMistsSwitch (initially enabled)'}
for path in SAVES:
    hdr, body = load(path)
    fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
    names = [p if isinstance(p, str) else str(p) for p in plugins]
    try: idx = [n.lower() for n in names].index('mists of tamriel.esp')
    except ValueError:
        print(os.path.basename(path), 'MoT not in plugin list'); continue
    formids = read_formid_array(body, flt['formIDArrayCountOffset'])
    forms = None
    for wv in (True, False):
        try:
            f, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], wv)
            if end == flt['globalDataTable3Offset']: forms = f; break
        except Exception: pass
    print(os.path.basename(path), f'MoT index {idx:02X}, changeforms {len(forms) if forms else None}')
    want = {(idx << 24) | k: v for k, v in TARGETS.items()}
    seen = set()
    for cf in forms or []:
        fid = resolve(cf['rtype'], cf['rval'], formids)
        if fid in want:
            d = decompress(cf); init, _ = decode_initial(d, cf['flags']) if d else ({}, 0)
            rf = init.get('recordFlags')
            print(f'   {fid:08X} {want[fid]}: changeflags 0x{cf["flags"]:08X} recordFlags {hex(rf) if rf is not None else None} -> '
                  + ('DISABLED' if (rf is not None and rf & 0x800) else 'ENABLED' if rf is not None else 'no form-flag change'))
            seen.add(fid)
    for fid, v in want.items():
        if fid not in seen: print(f'   {fid:08X} {v}: no changeform -> plugin default')

# sanity: how many changeforms resolve into MoT's index at all, and a sample
from collections import Counter
path = SAVES[-1]; hdr, body = load(path); fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
formids = read_formid_array(body, flt['formIDArrayCountOffset'])
forms, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)
c = Counter((resolve(cf['rtype'], cf['rval'], formids) or 0) >> 24 for cf in forms)
print('changeforms in index A1:', c.get(0xA1, 0), '| plugin[0xA1] =', plugins[0xA1])
print('sample A1 forms:', [hex(resolve(cf['rtype'], cf['rval'], formids)) for cf in forms if ((resolve(cf['rtype'], cf['rval'], formids) or 0) >> 24) == 0xA1][:12])
