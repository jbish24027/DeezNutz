import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(HERE, "dumps")

FILEMAP = {
    "Authoria - Patch - Astralite Dawn Warmth.esp": "WTHR__DawnWarmth.jsonl",
    "Astralite ENB.esp": "WTHR__AstraliteENB.jsonl",
    "Astralite Weathers.esp": "WTHR__AstraliteWeathers.jsonl",
    "Helios_Astralite.esp": "WTHR__HeliosAstralite.jsonl",
    "Authoria - Patch - Snowy Holds Seasonal Snowfall.esp": "WTHR__SnowyHolds.jsonl",
    "Wyrmstooth-Astralite-Weather-Patch.esp": "WTHR__WyrmAstralite.jsonl",
    "Mists of Tamriel.esp": "WTHR__MistsOfTamriel.jsonl",
    "Astralite ENB - ECSS.esp": "WTHR__ECSS.jsonl",
    "Authoria - Master Patch - Dragon Tweaks.esp": "WTHR__DragonTweaks.jsonl",
    "Authoria - Patch - Gray Cowl - Astralite.esp": "WTHR__GrayCowlAstralite.jsonl",
    "Skyrim.esm": "WTHR__Skyrim.jsonl",
    "Update.esm": "WTHR__Update.jsonl",
    "Lux.esp": "WTHR__Lux.jsonl",
    "Grand Solitude - The Walls of High King Erling.esp": "WTHR__GrandSolitude.jsonl",
    "BluePalaceTerrace.esp": "WTHR__BPT.jsonl",
    "Moonpath Music - Sky and Lighting fix - merged.esp": "WTHR__Moonpath.jsonl",
    "Dawnguard.esm": "WTHR__Dawnguard.jsonl",
    "Dragonborn.esm": "WTHR__Dragonborn.jsonl",
    "Helios.esp": "WTHR__Helios.jsonl",
    "NAT-ENB.esp": "WTHR__NATENB.jsonl",
}

def load_jsonl(p):
    rows = []
    with open(p, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for l in lines[1:]:
        if l.strip():
            rows.append(json.loads(l))
    return rows

_cache = {}
def plugin_records(plugin):
    if plugin in _cache:
        return _cache[plugin]
    fn = FILEMAP.get(plugin)
    d = {}
    if fn and os.path.exists(os.path.join(DUMPS, fn)):
        for r in load_jsonl(os.path.join(DUMPS, fn)):
            f = {}
            for x in r["fields"]:
                f[x["path"]] = x.get("value", x.get("note"))
            d[r["formid"]] = {"editorid": r.get("editorid"), "fields": f}
    _cache[plugin] = d
    return d

def winners():
    return json.load(open(os.path.join(HERE, "winners_DEEZ_CS_NUTZ_-_PBR.json")))

TODS = ["Sunrise", "Day", "Sunset", "Night", "EarlySunrise", "LateSunrise", "EarlySunset", "LateSunset"]
COLOR_FIELDS = ["SkyUpperColor", "SkyLowerColor", "HorizonColor", "FogNearColor", "FogFarColor", "AmbientColor",
                "SunlightColor", "SunColor", "StarsColor", "SkyStaticsColor", "EffectLightingColor",
                "CloudLodDiffuseColor", "CloudLodAmbientColor", "WaterMultiplierColor", "SunGlareColor",
                "MoonGlareColor", "UnknownColor"]
DALC_AXES = ["DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus", "DirectionalYMinus",
             "DirectionalZPlus", "DirectionalZMinus", "Specular", "Scale"]
FOG_DIST = ["FogDistanceDayNear", "FogDistanceDayFar", "FogDistanceDayPower", "FogDistanceDayMax",
            "FogDistanceNightNear", "FogDistanceNightFar", "FogDistanceNightPower", "FogDistanceNightMax"]

def rgb(s):
    if s is None or not isinstance(s, str) or "," not in s:
        return None
    p = s.split(",")
    return [int(p[0]), int(p[1]), int(p[2])]

def extract_colour(f):
    out = {"flags": f.get("Flags"), "colors": {}, "dalc": {}, "fog_distance": {}, "clouds": [], "volumetric": {},
           "imagespaces": {}, "precipitation": f.get("Precipitation"), "visual_effect": f.get("VisualEffect"),
           "sun_glare": f.get("SunGlare"), "sun_damage": f.get("SunDamage"), "wind_speed": f.get("WindSpeed"),
           "trans_delta": f.get("TransDelta"), "lightning_color": f.get("LightningColor"),
           "nam0_state": f.get("NAM0DataTypeState")}
    for c in COLOR_FIELDS:
        d = {}
        for t in TODS:
            v = f.get(f"{c}.{t}")
            if v is not None:
                d[t] = rgb(v)
        out["colors"][c] = d
    for t in TODS:
        base = f"DirectionalAmbientLightingColors.{t}"
        if f"{base}.DirectionalXPlus" in f:
            dd = {}
            for a in DALC_AXES:
                v = f.get(f"{base}.{a}")
                dd[a] = rgb(v) if a != "Scale" else v
            fr = f.get(f"{base}.Fresnel") or f.get(f"{base}.FresnelPower")
            if fr is not None:
                dd["Fresnel"] = fr
            out["dalc"][t] = dd
    for k in FOG_DIST:
        out["fog_distance"][k] = f.get(k)
    i = 0
    while f"Clouds[{i}]" in f:
        en = f.get(f"Clouds[{i}].Enabled")
        tex = f.get(f"CloudTextures[{i}]")
        layer = {"i": i, "enabled": en, "texture": tex, "colors": {}, "alphas": {}}
        for t in TODS:
            v = f.get(f"Clouds[{i}].Colors.{t}")
            if v is not None:
                layer["colors"][t] = rgb(v)
            a = f.get(f"Clouds[{i}].Alphas.{t}")
            if a is not None:
                layer["alphas"][t] = a
        out["clouds"].append(layer)
        i += 1
    for t in TODS:
        v = f.get(f"VolumetricLighting.{t}")
        if v is not None:
            out["volumetric"][t] = v
        v = f.get(f"ImageSpaces.{t}")
        if v is not None:
            out["imagespaces"][t] = v
    return out
