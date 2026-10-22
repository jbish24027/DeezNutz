Authoria - Oil Lamp Traps
=========================
Created 2026-08-16. No plugin. Four meshes + one Light Placer json.
Fixes the hanging oil-lamp traps (TrapFallingOilLamp01, mesh traps\oiltrap\oiltrap01.nif):
  1. their glow was twice as bright as every other Embers XD fire in this build
  2. they cast no light at all

WHY THE GLOW WAS TOO BRIGHT
The winning mesh came from "MIC - Embers XD Patch" (June 2024). It was built against an
older Embers XD. Embers XD 3.2.6 (CS flame style, the version installed) ships these
values in its own copies of the same four meshes:
    glow planes    Emissive Multiple 0.35   (MIC copy: 0.75 on oiltrap01, 1.0 on the other three)
    flame sprites  Emissive Multiple 2.0    (MIC copy: 4.0)
So the MIC copy was exactly 2x Embers' CS calibration. Every other Embers fire in the
build (braziers, campfires, fireplaces) already runs at glow 0.5 / flames 2.0.

WHAT THE MESHES HERE ARE
Byte-for-byte copies of the MIC patch meshes (MIC's higher-poly pot is kept) with ONLY
the five Emissive Multiple floats per file changed to Embers 3.2.6's values:
    meshes\traps\oiltrap\oiltrap01.nif             glow 0.75 -> 0.35, flames 4.0 -> 2.0
    meshes\traps\oiltrap\oiltrapdestroyed.nif      glow 1.0  -> 0.35, flames 4.0 -> 2.0   (the falling pot)
    meshes\traps\oiltrap\oiltrapprojectile01.nif   glow 1.0  -> 0.35, flames 4.0 -> 2.0
    meshes\traps\oillamptrap02\oillamptrap01.nif    glow 1.0  -> 0.35, flames 4.0 -> 2.0
Verified: 11 bytes differ per file, all inside those five floats.
This mod must sit ABOVE "MIC - Embers XD Patch" in MO2 priority (it does; it is right
above it in the Lighting - Embers XD group).
Still too bright? Lower the glow planes further. Embers' own next step down is 0.25
(what it uses for the firepit side glows). Do not touch the flames again - 2.0 is what
every other Embers fire uses.

THE LIGHT (LightPlacer\Authoria\Authoria_OilLampTraps_LP.json)
Attached to the base object TrapFallingOilLamp01 (0x90EFC~Skyrim.esm), so it follows the
pot when it falls and dies with it.
    bulb    Lux_RuinsFakeFlickerNS  - the same bulb Lux itself uses for the trap lamps it
            relit (fallbacks: Lux_FakeFlickerNS, then EmbersXD_EmbersLightSmall)
    radius  400  (bulb default is 250; the lamps hang 150-250 units above the floor)
    fade    0.8  (= Lux CS's exterior hanging-lantern value; candles are 0.35-0.5, braziers 1.5)
    flags   InverseSquare|Flicker|IgnoreScale|Linear   (Lux CS's own token string, minus
            PortalStrict - lamps hang over doorways and should light both sides)
    point   [0, 0, -5]  = the flame position. Derived from the mesh, not guessed: the
            flame emitters sit at z -13+8 and the two glow billboards at z -4.5..-5.
            The pot spans z -22..+22 (ObjectBounds).
Ground pool too weak?  raise fade (1.0, 1.2).  Too strong?  lower it (0.5).  One number.

WHY THERE IS A blackList - READ BEFORE ADDING LIGHT ELSEWHERE
Vanilla links many trap lamps to a light ref, and Lux re-links 57 of them to its own
light (Lux_RuinsFakeFlickerNS / Lux_MineFakeFlickerNS placed 3-120 units from the pot).
Those lamps ARE lit already. Lux CS does not bury interior refs (it only ships
Lux CS - Bulbs.esp and Lux Orbis CS.esp), so a blanket light would double-light them.
Census 2026-08-16: 204 lamp refs in the load order. 75 carry a linked light ref, 129 do
not (the screenshot lamp 0009B0EE is one of the 129). The 74 below are blacklisted:
  0x74029~Skyrim.esm                           lamp winner Skyrim.esm                           its light sits   34.7 units away
  0x74015~Skyrim.esm                           lamp winner Skyrim.esm                           its light sits   55.8 units away
  0x74654~Skyrim.esm                           lamp winner Skyrim.esm                           its light sits   24.8 units away
  0x7B646~BSHeartland.esm                      lamp winner BSHeartland.esm                      its light sits    8.1 units away
  0x7B649~BSHeartland.esm                      lamp winner BSHeartland.esm                      its light sits    8.7 units away
  0x7B64B~BSHeartland.esm                      lamp winner BSHeartland.esm                      its light sits    8.7 units away
  0xFAC4B~BSHeartland.esm                      lamp winner BSHeartland.esm                      its light sits   22.3 units away
  0xFAD36~BSHeartland.esm                      lamp winner BSHeartland.esm                      its light sits   27.0 units away
  0x7984F7~Siege at Icemoth.esp                lamp winner Siege at Icemoth.esp                 its light sits   11.7 units away
  0x52598A~Wyrmstooth.esp                      lamp winner Wyrmstooth.esp                       its light sits   21.8 units away
  0x525987~Wyrmstooth.esp                      lamp winner Wyrmstooth.esp                       its light sits    8.8 units away
  0x525A6A~Wyrmstooth.esp                      lamp winner Wyrmstooth.esp                       its light sits    9.4 units away
  0x173C5C~3DNPC.esp                           lamp winner 3DNPC.esp                            its light sits   33.2 units away
  0x1C1B80~3DNPC.esp                           lamp winner 3DNPC.esp                            its light sits  110.6 units away
  0x1C1B55~3DNPC.esp                           lamp winner 3DNPC.esp                            its light sits   15.7 units away
  0x1C1B87~3DNPC.esp                           lamp winner 3DNPC.esp                            its light sits    3.4 units away
  0x2981F7~3DNPC.esp                           lamp winner 3DNPC.esp                            its light sits   41.0 units away
  0x92B32~Skyrim.esm                           lamp winner Lux.esp                              its light sits   28.6 units away
  0x92B67~Skyrim.esm                           lamp winner Lux.esp                              its light sits   38.4 units away
  0x93CFB~Skyrim.esm                           lamp winner Lux.esp                              its light sits  119.4 units away
  0x94A4B~Skyrim.esm                           lamp winner Lux.esp                              its light sits  108.9 units away
  0x94A4D~Skyrim.esm                           lamp winner Lux.esp                              its light sits   56.8 units away
  0xBF898~Skyrim.esm                           lamp winner Lux.esp                              its light sits  148.9 units away
  0xBF8A2~Skyrim.esm                           lamp winner Lux.esp                              its light sits   81.7 units away
  0xBF8A9~Skyrim.esm                           lamp winner Lux.esp                              its light sits   37.2 units away
  0xBF8AD~Skyrim.esm                           lamp winner Lux.esp                              its light sits   33.5 units away
  0xAC7E0~Skyrim.esm                           lamp winner Lux.esp                              its light sits   36.1 units away
  0x93C42~Skyrim.esm                           lamp winner Lux.esp                              its light sits   58.3 units away
  0x93C47~Skyrim.esm                           lamp winner Lux.esp                              its light sits   37.7 units away
  0x93C48~Skyrim.esm                           lamp winner Lux.esp                              its light sits   49.0 units away
  0x93C4A~Skyrim.esm                           lamp winner Lux.esp                              its light sits   99.2 units away
  0x94AB4~Skyrim.esm                           lamp winner Lux.esp                              its light sits   24.7 units away
  0xA3DEE~Skyrim.esm                           lamp winner Lux.esp                              its light sits    8.4 units away
  0x913AF~Skyrim.esm                           lamp winner Lux.esp                              its light sits   20.7 units away
  0x913B0~Skyrim.esm                           lamp winner Lux.esp                              its light sits   18.7 units away
  0x9AA5A~Skyrim.esm                           lamp winner Lux.esp                              its light sits   18.0 units away
  0xA317E~Skyrim.esm                           lamp winner Lux.esp                              its light sits   75.4 units away
  0xD297D~Skyrim.esm                           lamp winner Lux.esp                              its light sits   36.2 units away
  0x9A6A~Dawnguard.esm                         lamp winner Lux.esp                              its light sits   39.3 units away
  0xB7F46~Skyrim.esm                           lamp winner Lux.esp                              its light sits   18.0 units away
  0x85E0A~Skyrim.esm                           lamp winner Lux.esp                              its light sits   78.7 units away
  0x85E14~Skyrim.esm                           lamp winner Lux.esp                              its light sits   37.3 units away
  0xAB1F9~Skyrim.esm                           lamp winner Lux.esp                              its light sits   44.1 units away
  0x186BA~Dawnguard.esm                        lamp winner Lux.esp                              its light sits   29.0 units away
  0xA3E03~Skyrim.esm                           lamp winner Lux.esp                              its light sits   19.6 units away
  0xA60A~Dawnguard.esm                         lamp winner Lux.esp                              its light sits   34.0 units away
  0xA60D~Dawnguard.esm                         lamp winner Lux.esp                              its light sits   40.2 units away
  0x9D5E8~Skyrim.esm                           lamp winner Lux.esp                              its light sits  132.0 units away
  0x34EDD~Skyrim.esm                           lamp winner Lux.esp                              its light sits   31.0 units away
  0xD5481~Skyrim.esm                           lamp winner Lux.esp                              its light sits   22.0 units away
  0xD5484~Skyrim.esm                           lamp winner Lux.esp                              its light sits   27.2 units away
  0x6FCE2~Skyrim.esm                           lamp winner Lux.esp                              its light sits   55.2 units away
  0x6FD9E~Skyrim.esm                           lamp winner Lux.esp                              its light sits   31.9 units away
  0x9B0F4~Skyrim.esm                           lamp winner Lux.esp                              its light sits   27.9 units away
  0x653A9~Skyrim.esm                           lamp winner Lux.esp                              its light sits   45.6 units away
  0x8BBEB~Skyrim.esm                           lamp winner Lux.esp                              its light sits   32.2 units away
  0x8BBEC~Skyrim.esm                           lamp winner Lux.esp                              its light sits   36.3 units away
  0x8D2B3~Skyrim.esm                           lamp winner Lux.esp                              its light sits   32.5 units away
  0xE40FB~Skyrim.esm                           lamp winner Lux.esp                              its light sits   47.2 units away
  0xE40FE~Skyrim.esm                           lamp winner Lux.esp                              its light sits   27.0 units away
  0xE4103~Skyrim.esm                           lamp winner Lux.esp                              its light sits   10.3 units away
  0x39937~Skyrim.esm                           lamp winner Lux.esp                              its light sits   35.1 units away
  0x39942~Skyrim.esm                           lamp winner Lux.esp                              its light sits   83.2 units away
  0xA5001~Skyrim.esm                           lamp winner Lux.esp                              its light sits  192.9 units away
  0xA4FFE~Skyrim.esm                           lamp winner Lux.esp                              its light sits  171.1 units away
  0xB7D9C~Skyrim.esm                           lamp winner Lux.esp                              its light sits   38.2 units away
  0x46E43~Skyrim.esm                           lamp winner Lux.esp                              its light sits   45.1 units away
  0x46E45~Skyrim.esm                           lamp winner Lux.esp                              its light sits   39.1 units away
  0x9C6~ccbgssse016-umbra.esm                  lamp winner Lux - Umbra CC.esp                   its light sits    9.9 units away
  0x9D7~ccbgssse016-umbra.esm                  lamp winner Lux - Umbra CC.esp                   its light sits    3.7 units away
  0xD14BF~SM_Astrid.esp                        lamp winner Lux - Heart of Ice Astrid patch.esp  its light sits   70.9 units away
  0xD15E2~SM_Astrid.esp                        lamp winner Lux - Heart of Ice Astrid patch.esp  its light sits   71.8 units away
  0xD1700~SM_Astrid.esp                        lamp winner Lux - Heart of Ice Astrid patch.esp  its light sits   79.6 units away
  0xD1765~SM_Astrid.esp                        lamp winner Lux - Heart of Ice Astrid patch.esp  its light sits  103.8 units away
The 75th linked lamp, 0x6E707~Skyrim.esm, is NOT blacklisted: its "light" is 1447 units
away and initially disabled, so that lamp is dark and gets the LP light.
Not verified: whether some of the 129 unlinked lamps have an UNLINKED room light close
by (Lux relights rooms without always linking). If you find a lamp that looks
double-lit, console-click it, copy its ref ID, and add "0x<id>~<plugin>" to blackList.
Deliberately not lit: the two decorative statics that share the mesh -
LuxVia_TrapOilLampStatic (Lux Via lights its own two placements) and
GG_CisternTrapOilLampStatic (not placed anywhere in this load order).

VERIFY IN GAME
Console-click a lamp and run  logLP  - it lists the Light Placer lights on it.
ReloadLP  re-reads the json without restarting.
The glow change needs the mesh to load fresh: start the game normally; if you were
already standing next to a lamp in the save, leave the cell and come back.
