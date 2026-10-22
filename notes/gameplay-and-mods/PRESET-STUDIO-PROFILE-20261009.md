# Authoria - Preset Studio - HPH  (profile ledger, 2026-10-09)

Purpose: a RaceMenu preset-making profile where only the assets on JuntiiOP's approved list (credit-only / open permission) are available, so a preset built here can be shared.

Cloned from `DEEZ CS NUTZ - PICTA` (the profile MO2 had selected). Profile files copied: modlist, plugins, loadorder, plugingroups, settings.ini, Skyrim.ini, SkyrimPrefs.ini, skyrimcustom.ini, archives.txt, initweaks.ini, lockedorder.txt, CRDW Automatic Mode. `saves` starts empty. Backups of every touched profile file: `*.bak-presetstudio-20261009` beside the originals (all seven profiles).

## Numbers

- Mods turned OFF versus PICTA: 105
- New mod folders installed: 13 (enabled here only; written DISABLED into the other six profiles at the same neighbours)
- Plugins deactivated: 91; plugins newly active: 9
- Full-plugin count after: 231 of 254 (PICTA was 243; Dalish_Vallaslin.esp is the only new full plugin)

## Approved assets available in this profile

Already installed (kept ON): BnP Female Skin 4k + Sk fix + small update, BnP Teeth Overhaul, Body Blushing, Even More Makeup by Koralina, Lovely Makeup (folder `Ultimate Body Enhancer - Lovely Makeup` - it is the base 94271 file despite the name), Lovely Makeup 2, Natural Beauty Makeup, Lamenthia's Marks of Beauty, Koralina's Freckles and Moles, Stalker Overlay 3BA, RX'Overlays, Bees' Alchemical Tattoos (folder `Alchemy Tattoos - 4K`), Imperfect Skin Overlays, Khisartin Brows/Beards Standalone (122879), Koralina's Eyebrows for HPH, Even More Eyes by Koralina, Eyes Nouveaux (+ Daedras and Devotees), Miggyluv's Eyes, Cuyi's Bosmeri Antlers (+ Proper RaceMenu Integration), and the UBE patches of those same mods.

Installed today (new folders, neighbour in brackets):

- `Dragon Age Dalish Vallaslin Face Tattoos` [above RX'Overlays (3.0, inner folder stripped)]
- `Lyru's Tattoo pack collection 2` [above RX'Overlays (1.07)]
- `Lyru's Tattoo pack collection` [above RX'Overlays (1.10)]
- `Koralina's Makeup Tweaks` [above Even More Makeup by Koralina (4k ESL 1.2)]
- `Beauty Marks 2 - Racemenu Overlays` [above Lamenthia's (4K file; Nexus named the 4K upload '2K', the 2.98 MB size confirms 4K)]
- `Beauty Marks - Racemenu Overlays` [above Lamenthia's (4K)]
- `Koralina's Mystic Eyes` [above Even More Eyes (ESL Elf 1.1)]
- `Wearable Horns - SE` [above Cuyi's Antlers (4K + main plugin fix 1.1, ESPFE)]
- `Goam Elven Ears - Redone - Reverie Patch` [above Cuyi's Antlers (Base + Sleek + Vamp + Mature = mirrors the Reverie install)]
- `Goam Elven Ears - Redone` [above Cuyi's Antlers (Core 1.0)]
- `Goam Elven Ears - Redone - No ENB SK Fix` [above Reverie, DISABLED (enable only if ear seams show; it flattens body/head subsurface maps)]
- `Reverie - Skin` [above BnP Sk fix - WINS over BnP in this profile]
- `Female Hands Redone - CBBE 3BA` [above CBBE 3BA (3BBB) - CBBE main + 3BA wrist patch; BodySlide build owed]

Reverie FOMOD choices made: Face diffuse Sleek, face normal Mature, body normal Smooth, not dirty, shaved, Face compat Vanilla (HPH, no ECE), Body CBBE. Change by reinstalling if you want Youthful/Hardened etc.; then mirror it in the Goam Reverie patch.

Downloaded but NOT installed (kept in `downloads`): `GoamEER - BnP Patch` (481 MB, FOMOD mirrors the BnP install - only needed if BnP is the live skin) and `GoamEER - Bnp Sk fix - Extra Matte S - addon`.

## New plugins and where they load

- `Koralina's Makeup Tweaks.esp` after EvenMoreMakeup.esp (group Visuals - Racemenu Addons)
- `LyruTat.esp`, `LyruTat2.esp`, `Dalish_Vallaslin.esp` after RXOverlays.esp (Visuals - Racemenu Addons)
- `(SDZ21) Beauty Marks.esp`, `(SDZ21) Beauty Marks 2.esp` after Lamenthia's Marks of Beauty.esp (Visuals - Character Visuals)
- `Koralina's Mystic Eyes.esp` after Even More Eyes.esp (Visuals - Racemenu Addons)
- `GoamElvenEarsRedone.esp`, `PraedysHorns.esp` after CuyiAntlers.esp (Visuals - Character Visuals)

All are ESL-flagged except Dalish_Vallaslin.esp (form 44). Written into loadorder/plugins/plugingroups of all seven profiles; active only here. Header-split check: the three duplicated headers in this profile (Essential - BugFixes, Lighting - Lux Patches, Visuals - Seasons and Landscape) were already present in PICTA before this job; the other five profiles have none.

## Forced exceptions (unapproved but must stay ON - they are masters of Authoria patches)

- `Complete Vanilla Eye Overhaul (CVEO) by LDD` - master of Authoria - Master Patch - UBE. Adds 827 eye records: DO NOT pick an eye whose name comes from CVEO in a shareable preset.
- `Dunmer Scarification - New Scar Complexions` - master of Authoria - Master Patch - Races Merge. Adds Dunmer complexions: do not use them.
- `LDD - Eyebrows for Men - HPH` - master of Authoria - Output - NPC Appearances. Male brows only.
- `UBE 2.0 Community Overlays 3` - master of houseCARL - Authoria - Patch - RaceMenu UI Misc Requiem. UBE-race overlays; do not use them.

## Not covered by the approved list (left ON, be careful)

- Hair: no hair pack is on the list. Every pack (KS, Dint999, Tullius, Fuse00, Lilyrim, HG, Valkyr, Modular SMP, Vanilla Hair Remake) stays enabled because the profile needs them to load; a shareable preset must use VANILLA hair unless a pack is cleared.
- Skin: BnP needs BOTH TheNorthSisters and Khisartin contacted. Reverie (credit only) now wins over it in this profile, so facegen/screenshots use Reverie. Male skin (SkySight) is not on the list.
- Lashes: Lashivious (UBE) and its Authoria fix stay on (UBE core). HPH ecosystem kept: High Poly Head, UV Stretch Fix, ENB Brow Fix, Beards for HPH (vanilla beard refits), Expressive Facegen Morphs. `Brows for High Poly Head` is OFF (it is a refit of Hvergelmir's Brows, which is not on the list).
- Beast-race block (Fur Paint, Flawn's overlays, lion manes, crests) and the Wounds overlay system were not touched.
- ddsworkshop packs (Khisartin's Facial Hair brows page, Eyes Mod 3) are off-Nexus: not fetched.

## Mods turned OFF in this profile (vs PICTA)

- Ultimate Body Enhancer - Ancient Beauty Makeup
- Ultimate Body Enhancer - Yyvengar Bodypaints
- Ultimate Body Enhancer - Wolfpaint Face
- Ultimate Body Enhancer - Senuas Warpaints
- Ultimate Body Enhancer - Rutahs Warpaint
- Ultimate Body Enhancer - Pockys Female Makeup
- Ultimate Body Enhancer - Obis Warpaints
- Ultimate Body Enhancer - Niohoggr Warpaints
- Ultimate Body Enhancer - LDD Detail Makeup HPH
- Ultimate Body Enhancer - Havoks Lipstick Overlays
- Ultimate Body Enhancer - Female Makeup Suite
- Ultimate Body Enhancer - Fabulous Makeup 2 - Racemenu Overlays
- Ultimate Body Enhancer - Miggyluv Overlays
- Ultimate Body Enhancer - Skin Features Overlay
- Ultimate Body Enhancer - Barbarian Paints
- Ultimate Body Enhancer - Community Overlays
- Ultimate Body Enchancer - Bitch Craft
- Ultimate Body Enhancer - HIMBO Hair Racemenu
- Ultimate Body Enhancer - LDD - Eyebrows for Men
- Ultimate Body Enhancer - Lovely Makeup 3
- Ultimate Body Enhancer - Pubic Hair Overlay Collection
- Ultimate Body Enhancer - LDD - Beards
- Ultimate Body Enhancer - Koralina's Face Details for COtR
- Ultimate Body Enhancer - Koralina's Makeup for COtR
- Ultimate Body Enhancer - [LRO] UBE Hit2 Eyes
- Ultimate Body Enhancer - LDD - Eyeliner Pack for UBE
- Ultimate Body Enhancer - LDD - Modular Warpaints UBE
- Ultimate Body Enhancer - LDD - Eyes For UBE
- Ultimate Body Enhancer - Kalilies Brows
- Ultimate Body Enhancer - Brows for High Poly Head
- Ultimate Body Enhancer - Eyes for UBE
- Ultimate Body Enhancer - Eyes Of Ellxe
- Ultimate Body Enhancer - Detailed Eyebrows
- Ultimate Body Enhancer - RikiTats
- Ultimate Body Enhancer - Pretty Makeup
- Ultimate Body Enhancer - LDD - Pretty Makeup - UBE
- Ultimate Body Enhancer - Aretuza Eyes Remastered
- UBE 2.0 Community Overlays 1
- RYA makeup
- Female Makeup Suite - Face - RaceMenu Overlays
- Serval Khajiit RaceMenu Overlays
- Camp Khajiit Patterns
- Khajiit-yllux Overlays - CBBE 3BA
- HIMBO V3 Bodyhair Overlays for Racemenu
- Beast Race Bodypaints SE
- Chooey's Dint Ears Edit
- Bitchcraft Tattoos - Racemenu - ESL
- Bitchcraft Tattoos - Racemenu
- LDD - Detail Makeup - HPH
- Pocky's 4k human female makeup - STANDALONE
- Pocky's 4k human male makeup - STANDALONE
- Fabulous Makeup 2 - Racemenu Overlays
- Blackmoon's Brows
- Hiraya Brows for High Poly Head
- LDD - Detailed Eyebrows for HPH 'n UBE
- Even More Brows HPH
- SG Female Brows - Improved - SE Port Replacer
- SG Female Eyebrows
- Brows for High Poly Head
- Hvergelmir's Aesthetics - Brows 4.1
- Kyoe's Bang'n Brows PLUS PLUS
- Kalilies Brows for High Poly Head
- Kalilies Brows
- High Poly Head SV Beards
- Beards of Power HDT-SMP
- Beards of Power - Polymorph Version
- Beards by Hvergelmir - High Poly Head
- Hvergelmir's Aesthetics - Beards 5.0.1
- High Poly Pretty Face and Darker Eyebrows
- Wolfpaint - Face - Facepaint Collection for Racemenu Overlays
- Makeup Mods - Male Support
- Community Overlays Merged
- Havok's Racemenu Makeup Overlays (Lipstick)
- Skin Feature Overlays SE
- More Scar Sliders - Northborn Scars for High Poly Head
- More Scars - A Slider for Racemenu
- Miggyluv's Tattoos for Men
- Miggyluv's Facepaint for Men
- Obi's Warpaints 2K Main
- Rutah's Warpaint
- Yyvengar Bodypaints - Female and Male (CBBE)
- Niohoggr Warpaints - All in one
- Barbarian Bodypaints - Male and Female
- Hellblade - Senua's Warpaints for Racemenu
- Northborn Scars - High Poly Head
- Northborn Scars
- Fia's Eyes - addon
- Eyes Of Ellxe
- Pocky's Quirk Eyes
- Kala's Vampire Eyes - Improved - Standalone
- Kala's Beast Eyes - Improved
- Kala's Elven Eyes - Improved
- Kala's Eyes Beast Races - ESL
- Kala's Eyes Beast Races - Standalone
- Kala's Eyes - Improved
- The Witcher 3 Eyes
- The Eyes of Beauty Ai - Standalone Textures
- MikanEyes v2.5 SE
- Feral Eyes - Beast Eyes for Humanoid Races
- Lamae's Gaze - vampire eyes
- (CVEO) by LDD - Aretuza Eyes Remastered - DUMMY
- (CVEO) by LDD - Aretuza Eyes Remastered
- Orc Brow Horns Texture Replacement
- Orc Brow Horns Don't Change Color - for High Poly Heads
- ORCODONTIST - Mouth and Teeth Fix

## Plugins deactivated

- (SDZ21) Ancient Beauty Makeup UBE.esp
- (SDZ21) Fabulous Makeup 2 UBE.esp
- (SDZ21) Fabulous Makeup 2.esp
- (SDZ21) Lovely Makeup 3 UBE.esp
- (SDZ21) Lovely Makeup Male 2.esp
- (SDZ21) Lovely Makeup Male.esp
- (SDZ21) Natural Beauty Makeup Male.esp
- (SDZ21) Pretty Makeup.esp
- AFB_ScarSliderHP.esp
- AdditionalEyesByFia.esp
- AretuzaEyesRemastered_CVEObyLDD.esp
- AretuzaEyesRemastered_CVEObyLDD_UBE.esp
- BM_Brows_HPH.esp
- BRB_BeastRaceBodypaints.esp
- BarbarianPaints.esp
- Beards of Power HDT-SMP.esp
- Beards of Power.esp
- Beards.esp
- Bitchcraft Tats.esl
- Bitchcraft Tattoos - Racemenu.esp
- Brows for High Poly Head.esp
- Brows for UBE.esp
- Brows.esp
- CampKhajiitOverlay.esp
- ChooeyDintEarsEdit.esp
- Collygon - Niohoggr Warpaints.esp
- CommunityOverlays1_0T30.esp
- CommunityOverlays2_31T50.esp
- CommunityOverlays3.esp
- Even More Brows HPH.esp
- EvenMoreMakeupMale.esp
- Eyes for CotR by Aehersin UBE.esp
- FMS_FemaleMakeupSuite.esp
- FMS_FemaleMakeupSuiteMale.esp
- FeralEyes.esp
- HIMBOBodyhairOverlay.esp
- HPH SV Beards.esp
- HavoksLipPatterns.esp
- HiPoly Pretty Face and Darker Eyebrows Standalone.esp
- Hiraya Brows for High Poly Head - Male.esp
- Hiraya Brows for High Poly Head.esp
- KALA_BEAST RACE EYES.esp
- Kala's Beast Eyes - Improved.esp
- Kala's Elven Eyes - Improved.esp
- Kala's Eyes - Improved.esp
- Kala's Vampire Eyes - Improved.esp
- Kalilies Brows for High Poly Head.esp
- Kalilies Brows for UBE.esp
- KaliliesBrows.esp
- Khajiit Serval Overlays.esp
- KhajiitylluxOverlays.esp
- Koralina's COTR Details.esp
- Koralina's COtR Makeup Female.esp
- Kyoe Bangin Brows PLUS PLUS for High Poly Head.esp
- Kyoe Bangin Brows PLUS PLUS for UBE.esp
- Kyoe Bangin Brows PLUS PLUS.esp
- LDD_DetailedEyebrowsforHPH.esp
- LDD_DetailedEyebrowsforUBE.esp
- LDD_EyelinerPackUBE.esp
- LDD_LevisChoice_BeardsForUBE.esp
- LDD_LevisChoice_DetailMakeupSetforHPH.esp
- LDD_LevisChoice_EyebrowSetforMen UBE.esp
- LDD_LevisChoice_PrettyMakeupSetforUBE.esp
- LDD_ModularWarpaintsUBE.esp
- Lamenthia's Marks of Beauty Male.esp
- Lupine_YyvengarBodypaints.esp
- Miggyluv's Facepaints.esp
- Miggyluv's Tattoos.esp
- MikanEyes All in one SE.esp
- NB-Scars.esp
- ObiWarpaintsTattoos.esp
- PAN_LamaesGaze.esp
- Pocky Punk's Make Up Addon_females.esp
- Pocky Punk's Make Up Addon_males.esp
- Quirk Eyes.esp
- RikiTats.esp
- RutahWarpaints.esp
- SFO_SkinFeatureOverlays.esp
- SGEyebrows - Improved for High Poly Head.esp
- SGEyebrows - Improved for UBE.esp
- SGEyebrows - Improved.esp
- SGEyebrows.esp
- Senua's Warpaints.esp
- TW3Eyes.esp
- TheEyesOfBeauty.esp
- UBE_PubicHairOverlayCollection.esp
- Wolfpaint_Face.esp
- [ELLE] Eyes Of Ellxe UBE.esp
- [ELLE] Eyes Of Ellxe.esp
- [LRO] UBE Hit2 Eyes.esp
- koralinas_freckles_moles_male.esp

## Rollback

Delete the profile folder `profiles/Authoria - Preset Studio - HPH`. The six other profiles only gained disabled lines for the 13 new folders; restore their `*.bak-presetstudio-20261009` files only if those folders are deleted too.


## 2026-10-11 additions (user rule: everything done for PICTA is done here too)
- `BnP - UBE Skin - Freckles` (Nexus 117250: alt4 freckles body + face 4 + silky speculars, one folder) ON here and in
  PICTA, directly above `Ultimate Body Enhancer - Sayble Skin`; disabled in the other six profiles. NOT on the approved
  list (BnP needs TheNorthSisters + Khisartin) - the user chose it anyway ("do whatever you want" / "picta and preset
  studio"). Presets do not embed skin textures, so only screenshots are affected.
- `Authoria - dlss-unlocked 0.9.32 (OptiScaler NR)` OFF here and in PICTA; Bottled frame generation OFF (shared
  SettingsUser.json). DLSS upscaling and the ReShade lane preset stay.

## 2026-10-12

Bottled Shaders 1.0.7 -> 1.0.11 and the Upscaling runtime files updated in place (same mod folders as PICTA, so this profile
has them too). Compiler threads 16/4, HiZ Occlusion disabled at boot, shader cache reset (full recompile on first launch).
Details: `PICTA-DLSS5NR-PLAN-20260930.md` 2026-10-12 block and `mods\[NoDelete] Bottled Shaders\LOCAL-SHADER-EDITS.md`.

## 2026-10-12 (later)

Picta weathers 1.1.1 + ENB preset 1.1.2 + Nordic Winds patch installed (same folders as PICTA; plugin added after Nordic Winds.esp here
too), Dynamic Wind floor 12%, ReShade effects toggle on Scroll Lock. Details: `PICTA-DLSS5NR-PLAN-20260930.md` 2026-10-12 (later) block.

## 2026-10-12 (evening)

`Authoria - Carriage PBR Wood Fix` enabled here too (line 38, directly above `Authoria - PG Output - PBR`). Lush grass values restored in
the shared `SettingsUser.json`. Details: `PICTA-DLSS5NR-PLAN-20260930.md` 2026-10-12 (evening) block.

## 2026-10-12 (evening, 2)

Shared `SettingsUser.json`: `DisableVanillaTonemapping` 1 -> 0 (A/B for brightness, PP stays on). Details in the PICTA plan doc.

## 2026-10-12 (evening, 3)

Shared `SettingsUser.json`: Upscaling disabled at boot for one test launch; `DisableVanillaTonemapping` back to 1. Brightness cause =
Bottled 1.0.11 removed Inverse Square Lighting (see the PICTA plan doc); grass cache is from July (pre-Witchy Wilderness) everywhere
except the two August re-bake areas.

## 2026-10-12 (evening, 4) - A/B STATE ACTIVE: Picta lanes rolled to 1.0.1 + Upscaling off for ONE test launch

Both PICTA and Preset Studio lanes are temporarily on `[NoDelete] Picta - Weathers of Aurbis 1.0.1 (shipped)` + `[NoDelete] Picta ENB
1.0.1 - Data (shipped)`; the 1.1.1 weathers, the 1.1.2 ENB data and the Nordic Winds patch mod are disabled, the Nordic patch esp is
inactive (line kept), the fair patch esp and the 4K pack's clouds.nif are their 1.0.1 versions, the Root twin is re-synced to 1.0.1
(scratchpad `s15_picta_ab.py to101`; `to111` restores everything; backups `.bak-pictaab-20261012` / `.bak-picta111-ab` / `.shipped-111.bak-ab`).
`SettingsUser.json`: `Disable at Boot: Upscaling=true` (no DLSS/Streamline/FSR), `DisableVanillaTonemapping` back to 1.
Read the result as: sharp again -> the 1.0.11 upscaling path is the smear; normal brightness -> Picta 1.1.x is the brightness.
Then restore one change at a time. Timeline that drove this: 06:58 run (1.0.11 + Picta 1.0.1) = "okay"; 07:2x run (after the driver
update) = UI blur reported; 08:48 run (Picta 1.1.1/1.1.2) = "really bright" reported.

## 2026-10-12 (evening, 5) - A/B RESULT (10:59 launch, upscaling off + Picta 1.0.1): "brightness better, blurriness [gone] now, grass is fixed"

- Log confirms the state: 'Upscaling' disabled at boot, E11 loaded 107 weathers (= the 1.0.1 set). User report: brightness better,
  the blur gone, grass "fixed" (sharp, dense - the DLSS 4.5 path had been mushing thin grass, which is why it "looked vanilla"),
  "maybe too many flowers" (the July cache's flower-field grass type in that area; the planned cache rebuild replaces it with
  Witchy Wilderness' own mix; WW's installer has a lower-flower tundra option).
- Conclusions: BRIGHTNESS = the Picta 1.1.1/1.1.2 rework (1.0.1 restores the look). BLUR / mushy grass = Bottled 1.0.11's upscaling
  path (Streamline 2.14.1 + DLSS 310.9.1 "4.5" model); no DLSS = sharp. Decisions pending: keep upscaling off (native 4K, check fps)
  vs retry DLSS with another preset / FSR4; stay on Picta 1.0.1 vs tune 1.1.x darker.
- Parallel session (7b213a74, 11:02) replaced the carriage fix with `Authoria - Skyking Carriages - Over Outputs` and updated
  Animated Carriage 1.2.1 + routes (its own ledger: CARRIAGE-UPDATE-PLAN-20261012.md). `Authoria - Carriage PBR Wood Fix` is
  disabled in all 8 profiles (folder kept). Riften PBR 2K (P17) stays a user pick for Riften itself.

## 2026-10-12 (late) - UI SMEAR SOLVED: ReShade (the user's call from the start)

ReShade off for one launch -> "crisp ui - as I said, I fucking knew it was reshade". Cause inside the Picta-lane preset
(`Authoria - ReShade - Picta lane preset\Root\Northman II.ini`): FOUR depth-of-field techniques enabled at once (MagicDOF, MatsoDOF,
RingDOF, GP65CJ042DOF from DOF.fx; autofocus, 6 samples) plus GaussianBlur - the original Northman II preset in the other mod has NO
DOF at all. The HUD writes no depth, so autofocus DOF blurs it whenever the focus is near, and the stacked low-sample DOF draws
doubled copies; static text looked sharp only when the focus sat far. Fix: those entries removed from Techniques/TechniqueSorting
(backup `Northman II.ini.bak-noblur-20261012`); ReShade DLL mod back on in both lanes. "A tiny bit too dark" without ReShade =
the preset's grade missing; it returns with ReShade. Upscaling stays OFF and Picta stays 1.0.1 until the next steps.
Built in advance: `Authoria - Picta 1.1.2 - Darkened to 1.0.1` (scratchpad s15_picta_darken.py; 30 brightness keys scaled to the
1.0.1 average, see its README; registered DISABLED in all 8 modlists directly above the 1.1.2 Data mod). Next launches: (2) Picta
1.1.2 + the darkened override (`s15_picta_ab.py to111` then `s15_picta_darken.py --write --enable`), (3) DLSS 5 NR via the parked
dlss-unlocked proxy (config A), each with its own launch.

## 2026-10-12 (late, 2)

Lane on Picta 1.1.1/1.1.2 again + `Authoria - Picta 1.1.2 - Darkened to 1.0.1` enabled (line 3332). ReShade on without the DOF/blur
passes (UI smear solved). Upscaling still off. Details in the PICTA plan doc.

## 2026-10-12 (late, 3)

`Authoria - Picta 1.1.2 - Darkened to 1.0.1` rebuilt as v2 (the 1.0.1 grade per weather; see the PICTA plan doc). Twin re-synced.

## 2026-10-12 (late, 4) - user: "still bright wtf go back" -> both lanes BACK ON PICTA 1.0.1

v2 (the 1.0.1 grade copied onto 1.1.2) was still too bright, so the remaining brightness is not in the ENB grade at all; most likely
the 1.1.1 weather RECORDS themselves (the game's own light colours in the rebuilt esm), which no ini can undo. Done: darkened override
disabled (PICTA + Studio, line 3332, kept built), `picta_ab_switch.py to101`: 1.0.1 weathers + 1.0.1 ENB data on, 1.1.1/1.1.2 off,
Nordic Winds patch MOD kept enabled with its esp UNCHECKED (line kept, no slot loss), fair patch + clouds.nif at 1.0.1, Root twin
synced to 1.0.1 (5 files). Upscaling still off, ReShade on without DOF/blur. Backups `modlist.txt.bak-goback-20261012`.

## 2026-10-12 (late, 5) - user: "nooooo I want the new picta you are not trying hard enough" -> full sweep + v3 + record patch

6-lane workflow (wf_43f22efe-fcd, 12 agents, each lane re-verified by a skeptic; digest scratchpad s17_digest.py / s17_bright.txt) found
the 1.1.x brightness in ~15 places, not 2. Confirmed causes: E11 [TIMEOFDAY] (dawn 2 h earlier, Day peak 12h: up to +1.5 EV mornings);
climate PIC_CLMT_Skyrim full day 08-18 instead of 09-17; VOLI PhaseFunctionScattering lowered (daytime god-ray veil off-sun x5);
[GAMEVOLUMETRICRAYS] x1.25-1.67; E11 [VOLUMETRICRAYS] x5 (sky/far terrain); [RAYS] sun shafts x10; DLI/ALI dawn/dusk + storm ambient;
fog colour multipliers/curves; mist weathers 10x fog + 3x bloom + 3x denser record fog + new density VOLIs; interior bloom thresholds;
[WATER] brightness x2; night sky gradient/scattering; WTHR FogFar, haze-band cloud layers 27/28 (+ layer 27 alpha), night sky colours,
DALC +22-45% in cloudy/overcast/storm/snow; dropped fVolumetricLightingIntensity=0.0 (engine fallback 2.0 for any weather/slot without
a VOLI: Bruma, Wyrmstooth, Olenveld, MQ scenes incl. the Helgen intro whose VOLI links point at missing records).
BUILT: (1) override v3 (`\_tools\picta-bridge\picta_darken_v3_full.py`): 25652 values, every non-colour number = 1.0.1 (category
medians per weather, 1.0.1 root/base values, [TIMEOFDAY] 3.5/9/10/17/3.5/20.5), colours stay 1.1.2; + the 1.0.1 'Picta - Weathers of
Aurbis.ini'. Backups `_backups\2026-10-12 - Picta darkened v1 (before v2)` and `... v2 (before v3)`. (2) ESL record patch
`Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp` (`picta_darken_records_patch.py`): CLMT 000812 TNAM 06/09/17/20, 21 VOLI = 1.0.1
bodies, 23 MASTER WTHR (FogFar, night sky 75, cloud 27/28 colours + 27 alpha 0, DALC x k, mist fog distances + VOLI relink). Masters
Skyrim/Dragonborn/Update/Dawnguard/Picta esm. Placed: plugins.txt after `Authoria - Picta over NAT.esp` (PICTA 1258, Studio 1256),
loadorder 1318/1316, plugingroups after the same line; mod line above the override in 5 modlists (+ PICTA/Studio, - elsewhere).
houseCARL: 0 errors, patch wins every record, values read back (CLMT 06/09/17/20, VOLI g 0.999, C03 fog 150000/0.9, DALC scaled).
Lanes switched back to 1.1.x (`picta_ab_switch.py to111`) with the override ON; Root twin synced from the override (4 files).
Not done on purpose (content, not scene brightness): region weather frequencies (1.1.1 has clear 2x as often), climate fallback WLST.

## 2026-10-12 (late, 6) - v3 + record patch CONFIRMED ("THERE WE GO ... still a tiny bit too DARK but so much better")

- Exposure trim: picta_darken_v3_full.py TRIM_EV = 0.2 adds +0.2 EV to every Adaptation Exposure Compensation (1134 values; e.g. Day 2.5 -> 2.7)
  in the override weather inis + root enbadaptation.fx.ini (adaptation-side, so the eye adaptation does not normalise it away). Change
  TRIM_EV and rerun the builder + sync_root_twin.py to nudge. [TIMEOFDAY] lines now written without a space before '='.
- ReShade: what the user misses = the removed MagicDOF/Matso/Ring/GP65 DOF + GaussianBlur. Picta 1.1.2 ships enbdepthoffield.fx.ini, but
  Silent Horizons 2 (1.10 installed, 1.15 on Nexus) has NO depth-of-field shader, so E11 logs 'Effect file not found, skipping
  enbdepthoffield.fx'. Option: an E11 DOF (draws before the UI) from an installed plain-HLSL ENB DOF (Cabbage / Berserkyr ship one).
- Brynjolf (GAB's Brynjolf Replacer, Nexus 170105): hair renders auburn, but the beard (FacialHair HDPT BrynBeards, HairTint + Decal flags)
  and brows render untinted: beardshort01.dds is pale brown (mean 100,81,67) -> reads blond/white. Facegen tint in the nif is dark
  (0.289,0.219,0.211); TSOS's Brynjolf facegen uses (0.51,0.235,0.188) red. Fix options: recolour the beard/brow textures auburn (texconv
  available in tools\xEdit\Edit Scripts) or use TSOS. User decision pending.

## 2026-10-13 - ReShade effects back without UI smear + Brynjolf beard (user picks: beard 1a; ReShade "you can figure it out")

- WHY the UI was crisp before: PureDark ran ReShade before the UI (mRenderReShadeBeforeUpscaling), and in the Picta lane until
  10-11 ReShade sat on a frame-gen D3D12 swap chain with no depth (MagicDOF inert). Bottled 1.0.11 has no frame gen, so ReShade got
  real depth on the D3D11 chain and its DOF ran AFTER the UI. The extra Matso/Ring/GP65 DOFs also drew the distant double vision.
- BUILT: `_tools/reshade-before-ui` -> mod `Authoria - ReShade Before UI` (+ PICTA / Studio, - in the 4 other profiles with the
  Picta-lane preset) = SKSE + ReShade add-on DLL; wraps ID 82084 +0x17A (1.6.1170, bytes verified on a SteamStub-decrypted copy)
  and calls render_effects there, the SSE ReShade Helper method (the original is on CS's incompatible-DLL list by file name).
  Picta-lane `Northman II.ini` Techniques back to the 10-06 set: + GaussianBlur + MagicDOF (no Matso/Ring/GP65); backup
  `.bak-beforeui-20261013`. Modlist backups `.bak-beforeui-20261013`.
- Brynjolf: hair is tinted in game, beard and brows render their raw textures; brows are dark already, beard texture pale ->
  mod `Authoria - Brynjolf Auburn Beard` above GAB (+ PICTA / Studio, - elsewhere) with beardshort01.dds scaled to mean 49,34,21.
- Next launch checks (mine): `SKSE/AuthoriaReShadeBeforeUI.log` (hook installed / registered / first pass), ReShade.log add-on line.

## 2026-10-13 (later) - original Northman II restored in the Picta lane (user: "restore the original settings from northman but keep our UI fix")

- First test launch 04:28: AuthoriaReShadeBeforeUI log = hook installed, registered (ReShade.log "Registered add-on ... API 18"),
  first pre-UI pass done. The user then edited DOF in the overlay (Matso/Ring/GP65 back on, blur radius 2.0) - saved as
  `Northman II.ini.bak-useredits-20261013-0443`.
- Lane preset = byte copy of the Nexus 159125 v1.0 file (md5 1fd04722...; pristine copy `Northman II.ini.original-159125-1.0`):
  Pirate_Bloom, LUT pack, CAS, Curves, Clarity, AmbientLight, Vibrance (-0.10), GloomAO SSDO_Plus, RadiantGI PCGI_One, Vignette,
  Technicolor, GaussianBlur, Colourfulness; MagicDOF OFF at start (Scroll Lock toggles it), Ctrl+Delete toggles GloomAO + RadiantGI.
  Lane ReShade.ini KeyEffects back to none (the 10-12 test toggle sat on Scroll Lock too). Archive copied to D:\1. MOD STUFF\1. SKYRIM FILES\CS.
- Note: with the pre-UI plugin ReShade has real scene depth, so GloomAO + RadiantGI now actually run in this lane (before 10-12 they
  had no depth here) - fps and the look (AO darkening, GI bounce, bloom) can shift. Script: `_tools/reshade-before-ui/restore_northman_original.py`.

## 2026-10-13 (later, 2) - "the July look" = Northman + the automatic DOF -> AMON ENB's ADOF in the Picta lane

- Finding: July profile DEEEZ NUTTZZZ ran AMON ENB REBORN (EnableDepthOfField=true, ADOF Kitsuune Edition, autofocus) under the
  stock Northman II (MagicDOF off). User 08-31: DOF "was automatic" in July; MagicDOF on = "overblown and just wrong".
- Built: mod `Authoria - Picta - July Depth of Field (AMON ADOF)` above the darkening override (+ PICTA / Studio, - DEEZ CS NUTZ / PBR /
  PICTA EXPERIMENT; backups modlist.txt.bak-julydof-20261013): AMON's enbdepthoffield.fx with includes inlined, its July
  enbdepthoffield.fx.ini, white Textures/BokehMaskAtlas.png placeholder. Override rebuilt with EnableDepthOfField=true +
  [DEPTHOFFIELD] FocusingTime 0.5 / ApertureTime 5.0 (forced in picta_darken_v3_full.py); Root twin re-synced. Installer:
  _tools/picta-bridge/install_july_dof.py. MO2's process hung windowless after exit (files written 05:18) and was ended at ~05:24.
- Verification 10-13 (workflow wf_3c3bb9f6-c46, 9 agents, 0 confirmed defects): see memory july-look-was-amon-enb-dof. Side note (older,
  display only, not from this change): PICTA plugingroups split 3 group headers ('Essential - BugFixes', 'Lighting - Lux Patches',
  'Visuals - Seasons and Landscape') around the Helios_Astralite* plugins; tidy later by regrouping those 3 lines if the user wants.
