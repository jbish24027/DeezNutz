"""Resolve the effective Data/enbseries tree per lane and extract fog-relevant E11 keys from base + routed weather inis."""
import os, re, json, configparser, collections, statistics as st
INST = "C:/1. AUTHORIA"; MODS = INST + "/mods"
H = os.path.dirname(os.path.abspath(__file__))
SECTIONS = {"ENVIRONMENT": re.compile(r"^Fog", re.I), "VOLUMETRICFOG": None, "GAMEVOLUMETRICRAYS": None,
            "VOLUMETRICRAYS": None, "PARTICLE": None, "EFFECT": re.compile(r"(Fog|VolumetricRays|Particle)", re.I),
            "WEATHER": None}
def tree(profile):
    ml = [l.rstrip("\n") for l in open(f"{INST}/profiles/{profile}/modlist.txt", encoding="utf-8")]
    enabled = [l[1:] for l in ml if l.startswith("+")]
    win = {}
    for n in enabled:  # top = highest priority; first seen wins
        root = f"{MODS}/{n}"
        cands = []
        if os.path.isfile(root + "/enbseries.ini"): cands.append(("enbseries.ini", root + "/enbseries.ini"))
        if os.path.isdir(root + "/enbseries"):
            for dp, dn, fn in os.walk(root + "/enbseries"):
                for f in fn:
                    full = os.path.join(dp, f).replace("\\", "/")
                    cands.append(("enbseries/" + os.path.relpath(full, root + "/enbseries").replace("\\", "/"), full))
        for rel, full in cands:
            k = rel.lower()
            if k not in win: win[k] = (n, full)
    return win
def read_ini(path):
    secs = collections.OrderedDict(); cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if not s or s.startswith((";", "#", "//")): continue
        m = re.match(r"^\[(.+?)\]", s)
        if m: cur = m.group(1).strip().upper(); secs.setdefault(cur, {}); continue
        if cur and "=" in s:
            k, v = s.split("=", 1); secs[cur][k.strip()] = v.split(";")[0].strip()
    return secs
def fogkeys(secs):
    out = {}
    for sec, rx in SECTIONS.items():
        for k, v in secs.get(sec, {}).items():
            if rx is None or rx.search(k):
                out[f"{sec}.{k}"] = v
    return out
def weatherlist(path):
    secs = read_ini(path)
    res = []
    for s, kv in secs.items():
        if s.startswith("WEATHER") and "FileName" in kv:
            res.append({"section": s, "file": kv["FileName"], "ids": [x.strip() for x in kv.get("WeatherIDs", "").split(",") if x.strip()]})
    return res
out = {}
for prof, tag in [("DEEZ CS NUTZ - PICTA", "picta"), ("DEEZ CS NUTZ - PBR", "pbr")]:
    t = tree(prof)
    lane = {"base_provider": t.get("enbseries.ini", ("-", ""))[0]}
    lane["base"] = fogkeys(read_ini(t["enbseries.ini"][1])) if "enbseries.ini" in t else {}
    wl = t.get("enbseries/_weatherlist.ini")
    lane["weatherlist_provider"] = wl[0] if wl else None
    lane["weathers"] = []
    if wl:
        for w in weatherlist(wl[1]):
            k = ("enbseries/" + w["file"].replace("\\", "/")).lower()
            prov = t.get(k)
            row = {"section": w["section"], "file": w["file"], "ids": w["ids"], "provider": prov[0] if prov else "MISSING"}
            if prov: row["keys"] = fogkeys(read_ini(prov[1]))
            lane["weathers"].append(row)
    # providers of every enbseries path (summary)
    lane["providers"] = collections.Counter(v[0] for v in t.values())
    out[tag] = lane
json.dump(out, open(H + "/e11_fog_keys.json", "w"), indent=1, default=str)
for tag, lane in out.items():
    print("=====", tag, "base:", lane["base_provider"], "weatherlist:", lane["weatherlist_provider"])
    print("  providers:", dict(lane["providers"]))
    print("  base fog keys:")
    for k, v in lane["base"].items():
        if any(x in k for x in ["FogAmountMultiplierDay", "FogAmountMultiplierNight", "FogAmountMultiplierDawn", "FogCurveMultiplierDay", "FogColorMultiplierDay", "FogColorMultiplierNight",
                                "VOLUMETRICFOG.", "GAMEVOLUMETRICRAYS.Intensity", "GAMEVOLUMETRICRAYS.RangeFactor", "PARTICLE.IntensityDay", "PARTICLE.IntensityNight", "IgnoreWeather", "EFFECT.", "WEATHER."]):
            print("    ", k, "=", v)
    print("  routed:", len(lane["weathers"]), "missing:", sum(1 for w in lane["weathers"] if w["provider"] == "MISSING"))
