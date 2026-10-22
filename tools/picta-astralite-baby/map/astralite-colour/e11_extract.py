"""Read-only: extract what Bottled Effects11 will actually read from the PBR lane's enbseries files.
Mirrors SettingManager::LoadSettingFromFile (GetPrivateProfileString semantics: first section match,
first key match, case-insensitive; TOD suffixes Dawn..InteriorNight; bare key fills all periods first)."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
SOUL = "C:/1. AUTHORIA/mods/[NoDelete] Soul Core ENB - Data"
NATBASE = "C:/1. AUTHORIA/mods/Authoria - Effects 11 Core - NAT (plain)/enbseries.ini"
TODS = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night", "InteriorDay", "InteriorNight"]

reg = []
for l in open(os.path.join(HERE, "registered_settings.txt")):
    p = l.strip().split("|")
    if len(p) >= 3:
        reg.append((p[0].upper(), p[1], p[2]))

def read_ini(path):
    secs = {}
    cur = None
    with open(path, encoding="latin-1") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith(";"):
                continue
            m = re.match(r"^\[(.+?)\]", line)
            if m:
                name = m.group(1).strip().upper()
                cur = name
                secs.setdefault(name, {"__dup__": name in secs})
                continue
            if cur is None or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip().lower()
            # first occurrence wins (GetPrivateProfileString), but only within the first section instance
            d = secs[cur]
            if k not in d:
                d[k] = v.strip()
    return secs

def tofloat(v):
    try:
        return float(v)
    except Exception:
        return None

def tocolor(v):
    parts = [x.strip() for x in v.split(",")]
    if len(parts) != 3:
        return None
    try:
        return [float(x) for x in parts]
    except Exception:
        return None

def extract(path):
    ini = read_ini(path)
    out = {}
    for cat, key, typ in reg:
        sec = ini.get(cat)
        if not sec:
            continue
        rec = {}
        if typ in ("TimeOfDay", "ColorTimeOfDay"):
            conv = tofloat if typ == "TimeOfDay" else tocolor
            base = sec.get(key.lower())
            if base is not None and conv(base) is not None:
                rec["ALL"] = conv(base)
            for t in TODS:
                v = sec.get((key + t).lower())
                if v is not None and conv(v) is not None:
                    rec[t] = conv(v)
        else:
            v = sec.get(key.lower())
            if v is not None:
                rec["value"] = v
        if rec:
            out[f"{cat}.{key}"] = rec
    # ignore flags
    flags = {c: {"IgnoreWeatherSystem": s.get("ignoreweathersystem"), "IgnoreWeatherSystemInterior": s.get("ignoreweathersysteminterior")}
             for c, s in ini.items() if isinstance(s, dict)}
    unread_colour_keys = {}
    regset = {(c, k.lower()) for c, k, t in reg}
    for c, s in ini.items():
        for k in s:
            if k == "__dup__":
                continue
            kk = k
            for t in TODS:
                if kk.endswith(t.lower()):
                    kk = kk[: -len(t)]
                    break
            if ("color" in k or "desat" in k or "tint" in k or "saturation" in k) and (c, kk) not in regset:
                unread_colour_keys.setdefault(c, []).append(k)
    return out, flags, unread_colour_keys

COLOUR_RE = re.compile(r"Color|Desaturation|ColorFromSun|ColorPow|ScatteringColor|SkyColorAmount|Gradient.*(Intensity|Curve)|Clouds(Intensity|Curve|Opacity)|AmbientLighting|DirectLighting|FogColor|ColorBalance|Saturation|Exposure|Brightness|Contrast|Intensity|Amount|Curve|Opacity", re.I)

base_vals, base_flags, base_unread = extract(NATBASE)
weatherlist = read_ini(os.path.join(SOUL, "enbseries", "_weatherlist.ini"))
routes = {}
for sec, d in weatherlist.items():
    fn = d.get("filename")
    ids = d.get("weatherids")
    if fn and ids:
        routes[fn] = [x.strip() for x in ids.split(",") if x.strip()]

files = {}
for fn in sorted(os.listdir(os.path.join(SOUL, "enbseries"))):
    if fn.lower().endswith(".ini") and fn not in ("_weatherlist.ini",) and not fn.lower().startswith("enb"):
        vals, flags, unread = extract(os.path.join(SOUL, "enbseries", fn))
        files[fn] = {"routed_ids": routes.get(fn, []), "values": vals, "unread_colour_like_keys": unread}

missing_files = [fn for fn in routes if fn not in files]
# effective honoured categories (ignore flags come from BASE enbseries.ini per Bottled SettingManager)
honour = {}
for c, f in base_flags.items():
    honour[c] = {"exterior_uses_weather_files": (str(f.get("IgnoreWeatherSystem") or "false").lower() != "true"),
                 "interior_uses_weather_files": (str(f.get("IgnoreWeatherSystemInterior") or "true").lower() != "true")}

json.dump({"base_file": NATBASE, "base_values": base_vals, "category_weather_honour": honour,
           "base_unread_colour_like_keys": base_unread, "weatherlist_routes": routes,
           "routed_files_missing_on_disk": missing_files, "weather_files": files},
          open(os.path.join(HERE, "soulcore_e11_colour_keys.json"), "w"), indent=1)
print("routes", len(routes), "missing files:", missing_files)
print("honour (exterior uses weather files):", {c: v["exterior_uses_weather_files"] for c, v in honour.items() if c in {r[0] for r in reg}})
