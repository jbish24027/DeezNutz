"""Read-only: MoT switch state (enable-state changeforms of the MoT parent markers) in the BABY's PXA saves.
Same logic as design/finalize/mot_state.py, pointed at the baby profile's saves. Run with python -B -I."""
import sys, glob, os
sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import load, parse_body
from changeforms import read_formid_array, parse_change_forms, resolve, decompress, decode_initial

SAVES = sorted(glob.glob(r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ - PICTA x ASTRALITE\saves\*.ess'), key=os.path.getmtime)
TARGETS = {0x005B1D: 'k747AnimatedDistantMistsSwitch (plugin default enabled)'}
for path in SAVES:
    hdr, body = load(path)
    fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
    names = [p if isinstance(p, str) else str(p) for p in plugins]
    lnames = [p if isinstance(p, str) else str(p) for p in light]
    try:
        idx = [n.lower() for n in names].index('mists of tamriel.esp')
    except ValueError:
        print(os.path.basename(path), 'MoT not in plugin list'); continue
    baby_in = 'authoria - patch - picta x astralite.esp' in [n.lower() for n in names + lnames]
    formids = read_formid_array(body, flt['formIDArrayCountOffset'])
    forms = None
    for wv in (True, False):
        try:
            f, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], wv)
            if end == flt['globalDataTable3Offset']:
                forms = f; break
        except Exception:
            pass
    print(os.path.basename(path)[:70], f'| MoT index {idx:02X} | changeforms {len(forms) if forms else None} | baby ESL in save plugin list: {baby_in}')
    want = {(idx << 24) | k: v for k, v in TARGETS.items()}
    seen = set(); motcount = 0
    for cf in forms or []:
        fid = resolve(cf['rtype'], cf['rval'], formids)
        if fid and (fid >> 24) == idx:
            motcount += 1
        if fid in want:
            d = decompress(cf); init, _ = decode_initial(d, cf['flags']) if d else ({}, 0)
            rf = init.get('recordFlags')
            print(f'   {fid:08X} {want[fid]}: changeflags 0x{cf["flags"]:08X} recordFlags {hex(rf) if rf is not None else None} -> '
                  + ('DISABLED' if (rf is not None and rf & 0x800) else 'ENABLED' if rf is not None else 'no form-flag change'))
            seen.add(fid)
    for fid, v in want.items():
        if fid not in seen:
            print(f'   {fid:08X} {v}: no changeform -> plugin default (enabled)')
    print('   MoT-index changeforms in this save:', motcount)
