"""Compact per-file per-period colour table of the live Picta E11 preset (effective = routed file over base)."""
import json, os
S = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(S, "picta_e11_colour.json"), encoding="utf-8"))
P = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night", "InteriorDay", "InteriorNight"]
K = {
    "sky_top_filter": ("SKY", "GradientTopColorFilter"), "sky_top_int": ("SKY", "GradientTopIntensity"),
    "sky_mid_filter": ("SKY", "GradientMiddleColorFilter"),
    "sky_horizon_filter": ("SKY", "GradientHorizonColorFilter"), "sky_horizon_int": ("SKY", "GradientHorizonIntensity"),
    "sky_gradient_int": ("SKY", "GradientIntensity"), "sky_gradient_desat": ("SKY", "GradientDesaturation"),
    "clouds_filter": ("SKY", "CloudsColorFilter"), "clouds_int": ("SKY", "CloudsIntensity"), "clouds_desat": ("SKY", "CloudsDesaturation"),
    "sun_filter": ("SKY", "SunColorFilter"), "sun_desat": ("SKY", "SunDesaturation"), "moon_filter": ("SKY", "MoonColorFilter"),
    "scat_color": ("SKYSCATTERING", "ScatteringColor"), "scat_from_sun": ("SKYSCATTERING", "ColorFromSun"), "scat_int": ("SKYSCATTERING", "Intensity"),
    "scat_amount": ("SKYSCATTERING", "Amount"), "airglow": ("SKYSCATTERING", "AirGlowIntensity"), "airglow_range": ("SKYSCATTERING", "AirGlowRange"),
    "sunglow": ("SKYSCATTERING", "SunGlowIntensity"), "clouds_light_desat": ("SKYSCATTERING", "CloudsLightingDesaturation"),
    "direct_filter": ("ENVIRONMENT", "DirectLightingColorFilter"), "direct_filter_amt": ("ENVIRONMENT", "DirectLightingColorFilterAmount"),
    "direct_desat": ("ENVIRONMENT", "DirectLightingDesaturation"), "direct_int": ("ENVIRONMENT", "DirectLightingIntensity"), "direct_curve": ("ENVIRONMENT", "DirectLightingCurve"),
    "ambient_desat": ("ENVIRONMENT", "AmbientLightingDesaturation"), "ambient_int": ("ENVIRONMENT", "AmbientLightingIntensity"),
    "fog_filter": ("ENVIRONMENT", "FogColorFilter"), "fog_filter_amt": ("ENVIRONMENT", "FogColorFilterAmount"), "fog_color_mult": ("ENVIRONMENT", "FogColorMultiplier"),
    "fog_color_curve": ("ENVIRONMENT", "FogColorCurve"), "fog_amount_mult": ("ENVIRONMENT", "FogAmountMultiplier"), "fog_curve_mult": ("ENVIRONMENT", "FogCurveMultiplier"),
    "colorpow": ("ENVIRONMENT", "ColorPow"),
    "volfog_filter": ("VOLUMETRICFOG", "ColorFilter"), "volfog_int": ("VOLUMETRICFOG", "Intensity"), "volfog_opacity": ("VOLUMETRICFOG", "Opacity"),
    "godray_filter": ("GAMEVOLUMETRICRAYS", "ColorFilter"), "godray_desat": ("GAMEVOLUMETRICRAYS", "Desaturation"),
    "ibl_mult": ("IMAGEBASEDLIGHTING", "MultiplicativeAmount"),
}
FXP = {"Dawn": "Dawn", "Sunrise": "Sunrise", "Day": "Day", "Sunset": "Sunset", "Dusk": "Dusk", "Night": "Night", "InteriorDay": "Interior", "InteriorNight": "Interior"}
out = {}
files = ["BASE"] + list(E["effective"].keys())
for f in files:
    eff = E["base"]["colour"] if f == "BASE" else E["effective"][f]
    own = {} if f == "BASE" else E["files"][f]["colour"]
    row = {}
    for p in P:
        d = {}
        for name, (sec, k) in K.items():
            v = eff.get(sec, {}).get(k + p)
            d[name] = v
        fx = eff.get("ENBEFFECT.FX", {}); pp = eff.get("ENBEFFECTPOSTPASS.FX", {})
        fp = FXP[p]
        d["cg_saturation"] = fx.get(f"CG.HDR.|- {fp} - Saturation")
        d["cg_tint"] = fx.get(f"CG.HDR.|- {fp} - Tint")
        d["cg_color_balance"] = fx.get(f"CG.HDR.|- {fp} - Color Balance")
        d["cg_exposure_ev"] = fx.get(f"CG.HDR.|- {fp} - Exposure (in EVs)")
        d["bloom_mix_saturation"] = fx.get(f"Bloom Mixing.|- {fp} - Saturation")
        d["kisuite_midtone_tint"] = pp.get(f"CG.KiSuite.|- {fp} - Midtone Tint")
        d["kisuite_shadow_tint"] = pp.get(f"CG.KiSuite.|- {fp} - Shadow Tint")
        d["kisuite_midtone_sat"] = pp.get(f"CG.KiSuite.|- {fp} - Midtone Saturation")
        d["kisuite_vibrance"] = pp.get(f"CG.KiSuite.|- {fp} - Vibrance")
        row[p] = d
    inherited = sorted({k for sec, kv in eff.items() for k in kv if k not in own.get(sec, {})}) if f != "BASE" else []
    out[f] = {"periods": row, "mod": (E["base"]["mod"] if f == "BASE" else E["files"][f]["mod"]),
              "n_colour_keys_own": sum(len(v) for v in own.values()), "n_inherited_from_base": len(inherited)}
json.dump(out, open(os.path.join(S, "picta_e11_colour_table.json"), "w"), indent=1)
for f in files:
    o = out[f]
    print(f[:60].ljust(60), o["mod"][:30], "own", o["n_colour_keys_own"], "inherit", o["n_inherited_from_base"])
