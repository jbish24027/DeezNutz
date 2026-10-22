import re, sys
dll = r"C:/1. AUTHORIA/mods/[NoDelete] Bottled Shaders/SKSE/Plugins/CommunityShaders.dll"
data = open(dll, 'rb').read()
keys = [
    # head-only (after the installed build)
    "IgnorePresetParticles", "EnableCloudsEdge", "HDRWeighting", "DisableGameDithering", "MoonType",
    "EnableShadows", "LoadPresetRaindrops", "GetLightNightWeight",
    # present in installed-era source
    "enbraindrops.png", "MotionStretch", "MotionTransparency",
    "DisableWrongSkyMath", "FixBlackCrush", "UseProceduralGradientWeights", "ProceduralGradientWeightCurve",
    "GradientIntensity", "GradientDesaturation", "GradientTopIntensity", "GradientTopCurve", "GradientTopColorFilter",
    "GradientMiddleIntensity", "GradientMiddleColorFilter", "GradientHorizonIntensity", "GradientHorizonColorFilter",
    "CloudsIntensity", "CloudsCurve", "CloudsDesaturation", "CloudsOpacity", "CloudsColorFilter", "CloudsVertexAlphaBoost",
    "CloudsEdgeClamp", "CloudsEdgeIntensity", "CloudsEdgeFadeRange", "CloudsEdgeMoonMultiplier",
    "SunIntensity", "SunDesaturation", "SunColorFilter", "MoonIntensity", "MoonColorFilter", "MoonCurve",
    "DirectLightingIntensity", "DirectLightingCurve", "DirectLightingDesaturation", "DirectLightingColorFilter",
    "DirectLightingColorFilterAmount", "AmbientLightingIntensity", "AmbientLightingDesaturation",
    "AmbientLightingCurve", "AmbientLightingColorFilter",
    "PointLightingIntensity", "FogColorMultiplier", "FogColorCurve", "FogAmountMultiplier", "FogCurveMultiplier",
    "FogColorFilter", "FogColorFilterAmount", "ColorPow",
    "FogHeight", "FogDensity", "FogHeightMultiplier", "FogDistanceMultiplier",
    "ScatteringColor", "ColorFromSun", "AirGlowIntensity", "AirGlowRange", "SunGlowIntensity", "SunGlowRange",
    "AtmosphereThickness", "HorizonRange", "DustVolume", "DustDensity", "DustDarkening", "ShadowAmount",
    "MoonGlowAmount", "CloudsLightingSunMultiplier", "CloudsLightingSunMinIntensity", "CloudsLightingMoonIntensity",
    "CloudsLightingDensity", "CloudsLightingDesaturation", "CloudsLightingForwardScattering",
    "EnableCloudsLightingFromMoon", "CalculateCloudsEdgeFromScattering",
    "MultiplicativeAmount", "EnableImageBasedLighting", "GlowIntensity", "SkyColorAmount", "RangeFactor",
    "SunRaysMultiplier", "UseLinearMath",
    "VOLUMETRICFOG", "VOLUMETRICRAYS", "GAMEVOLUMETRICRAYS", "SKYSCATTERING", "IMAGEBASEDLIGHTING",
    "ENVIRONMENT", "SKYLIGHTING", "CLOUDSHADOWS", "TIMEOFDAY", "COLORCORRECTION",
    "EnableMultipleWeathers", "EnableLocationWeather", "IgnoreWeatherSystem", "IgnoreWeatherSystemInterior",
    "_weatherlist.ini", "_locationweather.ini", "_worldspaceweatherlist.ini",
    "DawnDuration", "SunriseTime", "DayTime", "SunsetTime", "DuskDuration", "NightTime",
]
for k in keys:
    a = data.count(k.encode('ascii'))
    w = data.count(k.encode('utf-16-le'))
    print(f"{k:36s} ascii={a} utf16={w}")
# find [FOG]-style category literals: look for exact null-terminated "FOG"
print('exact FOG\\0 occurrences', len(re.findall(rb'\x00FOG\x00', data)))
