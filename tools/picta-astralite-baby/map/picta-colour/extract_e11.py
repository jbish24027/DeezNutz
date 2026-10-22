"""Extract every COLOUR-relevant E11 key per period from the live Picta-lane preset (VFS winners). READ-ONLY.
Output: picta_e11_colour.json = {routing:..., base:{SECTION:{key:value}}, files:{relpath:{...}}, effective:{relpath:{...}}}
'effective' = routed file overlaid on the base ini (E11 SettingManager inheritance: omitted keys inherit base).
"""
import os, re, json, sys
S = os.path.dirname(os.path.abspath(__file__))
vfs = json.load(open(os.path.join(S, "vfs_enb_picta.json"), encoding="utf-8"))

def winner(rel):
    v = vfs.get(rel.lower().replace("\\", "/"))
    return (v["path"], v["winner"]) if v else (None, None)

def parse_ini(path):
    secs = {}; order = []
    sec = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            l = raw.rstrip("\r\n")
            s = l.strip()
            if not s or s.startswith(";") or s.startswith("//"):
                continue
            m = re.match(r"^\[(.+)\]\s*$", s)
            if m:
                sec = m.group(1).strip(); secs.setdefault(sec, {}); order.append(sec); continue
            if "=" in s and sec is not None:
                k, v = s.split("=", 1)
                secs[sec][k.strip()] = v.strip()
    return secs

PERIODS = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night", "InteriorDay", "InteriorNight"]
COLOUR_SECTIONS = {
    "ENVIRONMENT": re.compile(r"^(DirectLighting(Intensity|Curve|Desaturation|ColorFilterAmount|ColorFilter)|AmbientLighting(Intensity|Desaturation)|PointLightingDesaturation|Fog(ColorMultiplier|ColorCurve|AmountMultiplier|CurveMultiplier|ColorFilterAmount|ColorFilter)|ColorPow)"),
    "SKY": re.compile(r".*"),
    "SKYSCATTERING": re.compile(r".*"),
    "VOLUMETRICFOG": re.compile(r".*"),
    "IMAGEBASEDLIGHTING": re.compile(r".*"),
    "CLOUDSHADOWS": re.compile(r".*"),
    "GAMEVOLUMETRICRAYS": re.compile(r".*"),
    "VOLUMETRICRAYS": re.compile(r".*"),
    "RAYS": re.compile(r".*"),
    "SKYLIGHTING": re.compile(r".*"),
    "PROCEDURALSUN": re.compile(r".*"),
    "SUNGLARE": re.compile(r".*"),
    "WATER": re.compile(r".*"),
    "TIMEOFDAY": re.compile(r".*"),
    "WEATHER": re.compile(r".*"),
    "EFFECT": re.compile(r"^(UseOriginal|EnableCloudsScattering|EnableProceduralSun|EnableImageBasedLighting|EnableSkylighting|EnableDirectionalSkyLighting|EnableVolumetricRays|EnableSunRays|EnableCloudShadows|EnableAdaptation|EnableBloom|EnablePostPassShader)"),
    "ENBEFFECT.FX": re.compile(r"(Saturation|Tint|Color Balance|Exposure|Contrast|Gamma|Hue|Vibrance|Temperature|Color)", re.I),
    "ENBEFFECTPOSTPASS.FX": re.compile(r"(Saturation|Tint|Color|Hue|Vibrance|Channel Mix|Temperature|Split|Lift|Gain|LUT)", re.I),
    "ENBBLOOM.FX": re.compile(r"(Tint|Color|Saturation)", re.I),
}

def colour_view(secs):
    out = {}
    for sec, rx in COLOUR_SECTIONS.items():
        if sec not in secs: continue
        d = {k: v for k, v in secs[sec].items() if rx.search(k)}
        if d: out[sec] = d
    return out

# --- routing ---
wl_path, wl_mod = winner("enbseries/_weatherlist.ini")
wl = parse_ini(wl_path)
routing = {}
for sec, kv in wl.items():
    fn = kv.get("FileName"); ids = kv.get("WeatherIDs")
    if not fn: continue
    rel = "enbseries/" + fn.replace("\\", "/")
    p, m = winner(rel)
    routing[sec] = {"FileName": fn, "WeatherIDs": [x.strip() for x in (ids or "").split(",") if x.strip()],
                    "winner_mod": m, "exists": bool(p and os.path.exists(p))}

base_path, base_mod = winner("enbseries.ini")
base = parse_ini(base_path)
res = {"routing_file": {"path": wl_path, "mod": wl_mod}, "routing": routing,
       "base": {"path": base_path, "mod": base_mod, "colour": colour_view(base)},
       "files": {}, "effective": {}}

# fx root inis
for fx in ["enbeffect.fx.ini", "enbeffectpostpass.fx.ini", "enbbloom.fx.ini", "enbadaptation.fx.ini"]:
    p, m = winner("enbseries/" + fx)
    if p:
        secs = parse_ini(p)
        # root fx inis hold one section per technique; collect colour keys
        flat = {}
        for sec, kv in secs.items():
            d = {k: v for k, v in kv.items() if re.search(r"(Saturation|Tint|Color|Hue|Vibrance|Channel Mix|Temperature|Exposure|Gamma)", k, re.I)}
            if d: flat[sec] = d
        res.setdefault("root_fx", {})[fx] = {"path": p, "mod": m, "colour": flat}

files = sorted({v["FileName"] for v in routing.values()})
# location interior templates too
for f in files:
    rel = "enbseries/" + f.replace("\\", "/")
    p, m = winner(rel)
    if not p or not os.path.exists(p):
        res["files"][f] = {"missing": True}; continue
    secs = parse_ini(p)
    cv = colour_view(secs)
    res["files"][f] = {"path": p, "mod": m, "colour": cv}
    eff = json.loads(json.dumps(res["base"]["colour"]))
    for sec, kv in cv.items():
        eff.setdefault(sec, {}).update(kv)
    res["effective"][f] = eff

json.dump(res, open(os.path.join(S, "picta_e11_colour.json"), "w", encoding="utf-8"), indent=1)
print("routed files", len(files), "missing", [f for f, v in res["files"].items() if v.get("missing")])
print("base", base_path, base_mod)
for fx, v in res.get("root_fx", {}).items(): print("root fx", fx, v["mod"])
