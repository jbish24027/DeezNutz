"""(d) installed E11 fork + twin vs stage/alive (md5) and vs the Darkened mod (whitelisted line diff). Read-only."""
import hashlib, json, os, re, sys

INST = r"C:\1. AUTHORIA"
M = os.path.join(INST, "mods")
LP = "\\\\?\\"
FORK = os.path.join(M, "Authoria - Picta x Astralite - E11")
BTWIN = os.path.join(M, "Authoria - Picta x Astralite - Root twin")
DARK = os.path.join(M, "Authoria - Picta 1.1.2 - Darkened to 1.0.1")
SHIP = os.path.join(M, "[NoDelete] Picta ENB 1.1.2 - Data (shipped)")
JDOF = os.path.join(M, "Authoria - Picta - July Depth of Field (AMON ADOF)")
STAGE = os.path.join(INST, r"_tools\picta-astralite-baby\design\finalize\stage\alive")

WL = {"SKY": {"GradientTopColorFilter", "GradientHorizonColorFilter", "CloudsColorFilter"},
      "ENVIRONMENT": {"FogColorFilter", "DirectLightingColorFilter"},
      "SKYSCATTERING": {"ScatteringColor"},
      "GAMEVOLUMETRICRAYS": {"Intensity", "ColorFilter"}}
PERIODS = ("Dawn", "Sunrise", "Day", "Sunset", "Dusk")


def md5(p):
    return hashlib.md5(open(LP + p, "rb").read()).hexdigest()


def tree(base):
    out = {}
    for dp, _, fn in os.walk(LP + base):
        for f in fn:
            p = os.path.join(dp, f)[len(LP):]
            out[os.path.relpath(p, base)] = p
    return out


ok = True
# 1. md5 vs stage
for name, inst in (("Authoria - Picta x Astralite - E11", FORK), ("Authoria - Picta x Astralite - Root twin", BTWIN)):
    st = tree(os.path.join(STAGE, name)); it = tree(inst)
    only_s = sorted(set(st) - set(it)); only_i = sorted(set(it) - set(st))
    diff = sorted(r for r in set(st) & set(it) if md5(st[r]) != md5(it[r]))
    print(f"[{name}] stage {len(st)} files, installed {len(it)}; only-in-stage {only_s}; only-installed {only_i}; md5 diffs {diff}")
    ok &= not diff and not only_s

# 2. source mapping for each fork file
fork = tree(FORK)
src_override = {
    r"enbseries\enbeffectpostpass.fx.ini": os.path.join(SHIP, r"enbseries\enbeffectpostpass.fx.ini"),
    r"enbseries\enblens.fx.ini": os.path.join(SHIP, r"enbseries\enblens.fx.ini"),
    r"enbseries\enbpresetoverlays.ini": os.path.join(SHIP, r"enbseries\enbpresetoverlays.ini"),
    r"enbseries\enbdepthoffield.fx.ini": os.path.join(JDOF, r"enbseries\enbdepthoffield.fx.ini"),
    r"enbseries\Authoria - Picta x Astralite\B01_Lightly_Cloudy_PictaPure.ini": os.path.join(DARK, r"enbseries\Picta - Weathers\00_Master\B01_Lightly_Cloudy.ini"),
}
dark = tree(DARK)
dark_enb = {r for r in dark if r.lower().startswith("enbseries\\") or r.lower() in ("enbseries.ini", "picta - weathers of aurbis.ini")}
missing_from_fork = sorted(r for r in dark_enb if r not in fork)
print("Darkened enbseries/ini files missing from fork:", missing_from_fork)
print("Darkened files not enbseries:", sorted(set(dark) - dark_enb))

viol, wl_lines, files_changed, nonini = [], 0, [], []
identical = 0
per_file = {}
for rel, p in sorted(fork.items()):
    if rel in ("manifest.json", "meta.ini"):
        continue
    src = src_override.get(rel) or (dark.get(rel))
    if not src or not os.path.exists(src):
        print("NO SOURCE for", rel); ok = False; continue
    a, b = open(src, "rb").read(), open(p, "rb").read()
    if a == b:
        identical += 1
        continue
    files_changed.append(rel)
    if not rel.lower().endswith(".ini"):
        nonini.append(rel); continue
    al, bl = a.split(b"\r\n"), b.split(b"\r\n")
    if len(al) != len(bl):
        viol.append((rel, "LINE COUNT", len(al), len(bl))); continue
    crlf_a, crlf_b = a.count(b"\r\n"), b.count(b"\r\n")
    lf_b = b.count(b"\n")
    if crlf_a != crlf_b or lf_b != crlf_b:
        viol.append((rel, "CRLF", crlf_a, crlf_b, lf_b))
    sec = None
    n = 0
    for i, (x, y) in enumerate(zip(al, bl)):
        xs = x.decode("utf-8", "replace").strip()
        if xs.startswith("[") and xs.endswith("]"):
            sec = xs[1:-1]
        if x == y:
            continue
        ys = y.decode("utf-8", "replace").strip()
        kx = xs.split("=", 1)[0].strip(); ky = ys.split("=", 1)[0].strip()
        if kx != ky:
            viol.append((rel, i + 1, "KEY CHANGED", xs, ys)); continue
        if rel.lower() == r"enbseries\_weatherlist.ini":
            if sec == "WEATHER901" and kx == "FileName":
                n += 1; continue
            viol.append((rel, i + 1, sec, xs, ys)); continue
        fam = per = None
        for p_ in PERIODS:
            if kx.endswith(p_) and kx[:-len(p_)] in WL.get(sec, ()):
                fam, per = kx[:-len(p_)], p_
        if fam is None:
            viol.append((rel, i + 1, sec, xs, ys))
        else:
            n += 1
    per_file[rel] = n
    wl_lines += n
print(f"fork files identical to source: {identical}; changed: {len(files_changed)}; non-ini changed: {nonini}")
print(f"whitelisted changed lines: {wl_lines}")
print("violations:", len(viol))
for v_ in viol[:40]:
    print("  ", v_)
print("per-file whitelisted counts:")
for k, n in per_file.items():
    print(f"  {n:4d}  {k}")
# 3. specific byte-identity checks
for rel in [r"enbseries\Authoria - Interiors\Dungeon.ini", r"enbseries\Authoria - Interiors\House.ini",
            r"enbseries\Authoria - Interiors\Inn.ini", r"enbseries\_locationweather.ini", "enbseries.ini"]:
    print(f"  {rel:50s} fork==Darkened: {md5(os.path.join(FORK, rel)) == md5(os.path.join(DARK, rel))}")
# interior/Picta-Interior templates all identical?
inter = [r for r in fork if "interiors" in r.lower()]
print("  all interior templates identical:", all(md5(fork[r]) == md5(os.path.join(DARK, r)) for r in inter), len(inter))
# manifest.json consistency
man = json.load(open(os.path.join(FORK, "manifest.json"), encoding="utf-8"))
mf = man.get("files", {})
bad = [k for k, h in mf.items() if md5(os.path.join(FORK, k.replace("/", "\\"))) != h]
print(f"manifest.json: {len(mf)} entries; md5 mismatches vs installed: {bad}; fork files not in manifest:",
      sorted(set(r.replace('\\', '/') for r in fork) - set(mf) - {"manifest.json", "meta.ini"}))
print("RESULT md5-stage:", "PASS" if ok else "FAIL")
