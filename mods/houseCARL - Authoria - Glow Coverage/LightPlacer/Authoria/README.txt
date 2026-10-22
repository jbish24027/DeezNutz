Authoria - Glow Coverage
========================
Real light on things that look like they should emit it but do not.
Each group is its own .json - delete a file to drop that group, nothing else breaks.

ALREADY LIT BEFORE THIS MOD - deliberately NOT covered
  Glowing mushrooms (plants\glowingmushroom01 / cluster01 / single01.nif).
  Rudy HQ - More Lights for ENB already bakes a billboard named "Enb Light"
  into those meshes using textures\!_Rudy_Misc\effects\fxglowENB.dds, and
  Community Shaders registers that texture in ParticleLights\fxglowenb.ini.
  So they already cast light. ParallaxGen re-processed the meshes and kept
  the light plane intact - verified block-for-block against Rudy's copy.
  Adding Light Placer on top would double-light every one of them.

  Firefly jars are likewise already lit - see the Firefly Light mod's README.

WHAT EACH FILE COVERS
  Authoria_Glow_Plants.json
      Nirnroot (green), Crimson Nirnroot (red), Oceanroot from Beyond Skyrim
      (blue), Deathbell (purple), Gleamblossom (pale blue).
      DEATHBELL, 2026-08-15 round 2: the petal texture was taken to a near-black
      plum (see Authoria - RMF Purple Retint\LOCKED-VALUES.md - it has to be dark
      or it renders blue). The plant therefore leans on this light to read at
      all, so Authoria_Glow_Deathbell was strengthened: radius 110 -> 200,
      fade 0.4 -> 0.9, colour deepened 220,70,210 -> 200,55,190. Adjust the
      flower's brightness HERE. Do not brighten the texture instead.
      Nirnroot is an ACTIVATOR, not a Flora record - that is why it does not
      turn up in a Flora search. The meshes are Plants\FloraNirnroot01.nif and
      Plants\FloraNirnroot01Red.nif, plus the _Empty picked variants.
      Gleamblossom's mesh has vanilla glow billboards using
      textures\effects\FXGlowSpotLinearAlpha.dds, which is NOT a registered
      particle-light texture - it looks bright but emitted nothing.
  Authoria_Glow_Mushrooms.json
      Blackreach epic / small / tiny mushrooms (cyan), Solstheim mushroom
      trees and the Saints and Seducers Mania thin mushroom trees (amber).
      2026-08-16: + all five ANIMATED giant mushrooms (BlackreachGiantMushAnim01-05,
      the swaying MSTT ones - user: "i want ALL the animated ones to faintly
      glow"). Same cyan bulb, faint: fade 0.4, radius per mesh 700 / 420 / 340 /
      420 / 400 (roughly 3x each cap's bounding radius). These are attached to
      the NODE "Bone_Top" instead of a point: the meshes are skinned, Bone_Top is
      the cap bone (translation z 1096 / 438 / 306 / 426 / 542 - inside the
      cap; Bone_Roots hangs from it = the tendrils), so the light rides the sway
      and lands at the cap at ANY reference scale (placed scales run 0.44 to
      6.93, median 0.79). IgnoreScale keeps radius/fade constant so the one 6.9x
      giant does not become a floodlight. Node names verified in the winning
      High Poly Blackreach Mushrooms meshes.
      NOT covered on purpose (user scoped to the animated ones): the static
      BlackreachGiantMush01-05, GiantMushHoriz01-04. Add them the same way if
      wanted - they are NOT skinned, so use points at cap height, not Bone_Top.
  Authoria_Glow_BlackreachFlora.json  (added 2026-08-16)
      The other Blackreach plants the user highlighted, "very gentle glow &
      light matching their colors":
        BlackreachBush01/02 (TREE)   Authoria_Glow_BlackreachBush 120,225,220
                                     r200 fade 0.45, point z 70 / 80 (glowing
                                     tips are the top half; bounds -6..114 /
                                     ..130)
        TreeBlackReachFern01/02      Authoria_Glow_BlackreachFern 140,225,150
                                     (green, like the leaves) r230 fade 0.4,
                                     point z 25 (bounds -22..54, XY +-130..170)
        BlackreachVineFloor01        Authoria_Glow_BlackreachVine 130,225,205
                                     r280 fade 0.35, point z 15 (flat vines,
                                     bounds -15..10, XY +-213..259)
      BUSH CAVEAT: the winning bush meshes (Blackreach Bush - FOMOD, ENB-light
      option, carried through by ParallaxGen) already hold an ENB billboard
      "ENBLBBRD/ENBL0" textured GlowSoft01_enbl.dds, and CS registers that
      texture (ParticleLights\glowsoft01_enbl.ini). By the CS rule above (light
      radius = billboard bound radius x 0.5) that light is bound 80 x node scale
      2.4 x 0.5 = ~96 units, centred inside the bush (z ~62) - it never leaves
      the bush's own geometry (bound radius 104). The LP bulb is what reaches
      the ground and wall. So the two DO overlap inside the bush; if a bush
      looks blown out at its core, delete the two bush entries here (the
      particle light stays) or lower the bulb's fade. This is the one place in
      this mod where an LP light is stacked on a known ENB light on purpose,
      because the ENB one is too small to count and the user asked.
      Meshes checked for existing lights before adding (nifshader dump): fern
      = plain own-emit (0,0.73,1)x1.5, no glow planes; vine floor = Glow shader
      + the vanilla AzuraCrystal decal effect (not a light); giant mushrooms =
      Glow shader + the same decal, no billboards. Tiny mushrooms and crimson
      nirnroot were ALREADY in this mod (see Plants/Mushrooms) - nothing new
      needed for them beyond the crimson colour change below.
      CRIMSON NIRNROOT 2026-08-16: Authoria_Glow_NirnrootCrimson colour changed
      255,60,110 (pink-red, H~343) -> 255,45,55 (crimson, H~357) - user asked
      for a RED glow. Radius/fade unchanged (128 / 0.5).
      Sibling mod created the same day: "Authoria - Blackreach Sun Dimmer" (the
      Blackreach sun sphere's emissive x8 -> x4, mesh-only, own README). Not
      part of this mod but the same request.
  Authoria_Glow_SoulGems.json
      FILLED soul gems only - the _full meshes. An empty gem stays dark,
      which is the point. Black soul gems get their own violet light.
      Winning meshes come from Crystalline Soul Gems; none had a light.
  Authoria_Glow_Atronachs.json
      Flame (orange, flickering), Frost (icy blue), Storm (violet, fast
      flicker), plus Dawnguard's Ancient Frost and Beyond Skyrim's Cold Flame.
  Authoria_Glow_Lanterns.json
      Handheld Lanterns - HDT-SMP held meshes. CHECK THIS ONE FIRST: if the
      lantern mod already casts its own carried light, you will get two.
      Delete this file if the lantern looks blown out.
  Authoria_Glow_AzuraCrystals.json   (added 2026-08-16)
      The six vanilla Azura crystal clusters (AzurasCrystalCluster01-06, the
      Dungeons\AzurasStar\ meshes) - JK's College of Winterhold plants 42 of
      them in the halls at 0.4-0.9 scale, and they fill the Azura's Star realm.
      Their meshes have two additive "effect" shapes (cyan-green core, violet
      rim) but no light-emitting plane, so they cast nothing. Faint icy light:
      Authoria_Glow_SoulGem bulb with color 150,215,235 (H~194, outside the
      dead band), radius 320, fade 0.5, Simple|IgnoreScale|PortalStrict.
      Keyed by base FormID (formIDs), NOT by model path, on purpose: Lucien's
      red recolors (aaaLucAzurasCrystalCluster0XRed) reuse the same .nif and
      would get a cyan light. Olenveld's copies use their own meshes.
      Light points come from the actual vertex centroids of the winning (USSEP)
      meshes, not from ObjectBounds: cluster01's geometry sits at x +228 (its
      record bounds claim +-228, which is wrong), so it has its own entry at
      [228, 37, 70]; clusters 02-06 share [-8, -12, 85].
      IgnoreScale keeps radius/fade fixed on the scaled-down College clusters;
      the point itself scales with the object, so it stays inside the crystal.
      Too faint -> fade 0.7. Too strong -> 0.35. To make the crystal BODY
      brighter instead, the two effect shaders' Emissive Multiple (1.0 rim,
      2.0 core) would need a loose mesh copy - not done.
  Authoria_Glow_DunmerLanterns.json  (REWRITTEN 2026-08-16)
      All 48 meshes of Dovahnique's Diverse Dark Elf Lanterns (BOS) - six
      shapes x eight patterns, 0DV_BOSLanterns\0DVDarkElfLantern0N*.nif. Both
      the 48 STAT and the 48 MSTT records (same EditorIDs, same meshes) resolve
      to these paths.
      These DO ship an ENB particle light: a shape named EnbParticleLight01:0
      textured textures\Dark Elf Lantern ENB Light\fxglowENB.dds. The filename
      matches ParticleLights\fxglowenb.ini, and Rudy's mushrooms light fine off
      that same filename, so the registration is not the problem - yet in game
      the lantern glowed inside and spilled nothing onto the crate under it.
      Two differences from Rudy's working mesh, neither confirmed as the cause:
      this fxglowENB.dds is a different 516-byte file (Rudy's is 2872), and the
      lantern carries two BSEffectShaderPropertyColorController blocks animating
      the glow colour. Rather than keep guessing at closed shader behaviour, the
      lantern gets a real Light Placer bulb, which is fully under our control.
      2026-08-16 BUG FOUND: the 2026-08-15 version of this file never lit a
      single lantern. Dovahnique's records store the model path WITH the prefix
      - "Meshes\0DV_BOSLanterns\...nif" - and Light Placer matches the record's
      MODL string against the json string verbatim (case-insensitive, nothing
      stripped, see MODEL PATH RULE below). The json had the paths without the
      prefix, so gameModels.find() never hit. This is why the ClefJ Morthal
      lantern (ref CC033F61) still cast nothing after the "fix". BOS is not the
      cause - LP reads the swapped base's model, which is fine.
      Every group now lists each path twice, with and without "Meshes\", so a
      future override that stores the path either way still matches.
      Points are now PER SHAPE, read out of the meshes (bounding-sphere centre of
      the inner candle object + 7 units, which is where each glass centre and the
      mod's own ENB light disc sit). The old [0,0,0] was the HOOK - every one of
      these lanterns hangs DOWN from its root, by up to 280 units:
        01  triple cluster  [4.3,189.1,-225] [1.3,-0.4,-190] [-31.5,-54.1,-279]
        02  double          [0.2,-142.1,-127.5] [-0.3,0.6,-154.5]
        03  single          [0.8,-1.0,-153]
        04  single          [0.8,-1.0,-119.5]
        05  single          [0.8,-1.0,-80.5]   (ClefJ's own light sat at -89)
        06  single          [0.8,-1.0,-31]
      Bulb tuning follows Lux CS's exterior lantern entry exactly (Lux CS -
      Lanterns ISL - Exterior.json): flags InverseSquare|IgnoreScale|Linear,
      radius 425, fade 0.8, cutoff 0.1, size 2.0. Only the LIGH differs -
      Authoria_Glow_Lantern (255,110,50) instead of Lux_DefaultLanternNS
      (247,155,72), because Lux Orbis's own dunmer-lantern light is 255,108,0.
      Under CS this makes the pool the same size and falloff as every other
      lantern in the town. No Simple flag, so it gets contact shadows like Lux's.
      EXTERIORS ONLY: condition "Self IsInInterior NONE NONE == 0". Interior
      Dunmer lanterns (Raven Rock houses etc.) are Lux's job - Lux's own placed
      interior lights survive in this build, and adding a bulb there would stack.
      If an interior one turns up dark, add a second entry with the condition
      flipped to == 1 and Lux CS's interior tuning (fade 0.3, size 1.2).
      Known stack: a Lux Orbis placed light can survive AT the same lantern (the
      ClefJ Morthal one has LuxOrbis_FarmDunmerLanternsNS, radius 120, night-only
      via FXLightRegionInvertLightsWhiterun, ISL-converted by ISL Helper). It is
      small and sits inside the glass; the bulb here is the one that reaches the
      wall and ground. If a lantern looks blown out at the glass, that is why.
  Authoria_Glow_DwemerPipes.json  (added 2026-08-16)
      Golden Dwemer Pipeworks Redone - Real Dwemer Pipes vents, hubs, boilers,
      pipe ends and the Solstheim reading-room pipe groups. Bulb is
      Authoria_Glow_DwemerVent (00080C): 255,112,28 orange, radius 320, fade 1.0,
      slow flicker (period 0.7, amplitude 0.15). Boilers and ReadRmPipeGrp01 are
      overridden to radius 420 / fade 1.1, the pipe end to 130 / 0.7.
      WHY LIGHT PLACER AND NOT ParticleLights: GDPR bakes an ENB particle-light
      disc into these 7 meshes (shape ENBParticleGlow / DwePipeBoiler02:365:366,
      texture textures\effects\ENB_particle_glow.dds, orange vertex colour,
      NiBillboardNode parent). No ParticleLights\enb_particle_glow.ini exists in
      the load order, so under CS the disc draws as a glow but emits nothing.
      Registering it looked like the obvious fix but is a trap: CS makes the light
      radius = billboard bound radius x 0.5, which is 44 units on the vent (disc
      radius 80 x node scale 1.1 / 2). Not one vertex of the vent lies within 44
      units of the disc centre (the pipe wall is at ~50), and Cull=true would
      also HIDE the visible orange glow. So the vent would get darker, not lit.
      The boiler's 80-unit light only reaches its own inner vanes. Hence a real
      bulb. The GDPR discs are left in place - they are the visible "glow", the
      bulb is the "light". Do NOT add ParticleLights\enb_particle_glow.ini on top,
      that would stack a second (tiny) light and cull the discs.
      Light points are GDPR's own emitter positions read out of the meshes:
        Vent01 / Hub01        [0,0,0]        (model centre, inside the vented hub)
        Boiler01 / Boiler02   [0,0,200]      (mid-body, behind the glowing vanes)
        PipeEnd01             [20,0,0]       (the open mouth)
        DLC2DweReadRmPipeGrp01 [-367,660,820] and [367,660,820]
        DLC2DweReadRmPipeGrp02 [0,750,230]
      Vanilla falloff on purpose (no InverseSquare/Linear flags): under CS ISL a
      light without the InverseSquare bit passes radius/fade through unchanged,
      so radius and fade here mean what they say. PortalStrict is set to match
      the vanilla Dwemer lamps and stop the light leaking through walls; if a
      vent light pops off when you walk through a doorway, drop that token.
      Model matching means every STAT that uses these nifs is covered - vanilla,
      Markarth Mossy AF, the Seasons winter copies, LOTD, CC puzzle dungeon.
  Authoria_Glow_DwemerGlass.json  (added 2026-08-16, "faint lights" per user)
      Improved Dwemer Glass's ENB lights as carried by the GDPR patch meshes. Under
      CS those discs are dead: their texture is vanilla GlowSoft01, which cannot be
      registered without lighting 58 Storm Lightning bolt meshes (see the census).
      Bulb Authoria_Glow_DwemerGlass (000810): 225,235,240 pale glass, radius 200,
      fade 0.4, no flicker. Points are the disc positions read from the meshes:
        Astrolabe hub      3 points [-141,0,497] [291,-428,506] [728,-9,526]
        Astrolabe lens     [0,0,1080], radius 250
        Observatory armillary [0,2,415], radius 160
        Observatory domes 01/02/03  [-16,-955,660] [-2,-777,860] [-6,-565,990]
      These are animated machines; the points are the rest pose. If a light sits
      off the glass by a rotation, nudge the point, do not brighten it.
      Records: ACTI DweAstrolabeHub01/Lens01, DweObservatoryArmillary01, Dome01-03,
      plus LOTD's DBM_DWEAstrolabe01 and Dac0da's copies (same model strings).
  Authoria_Glow_MageStatue.json  (added 2026-08-16)
      Winterhold mage statue (Architecture\Winterhold\MageStatue.nif - also used by
      LOTD, Bruma, Vigilant, Glenmoril, Unslaad, Seasons). The mod "Winterhold
      Statue - Animated with ENB Lights" put two discs at the hands with vanilla
      FXGlowSpotLinearAlpha - unregisterable for the same reason. Two bulbs:
      Authoria_Glow_MageStatueBlue (000813) 70,160,255 at [92,-88,413] and
      Authoria_Glow_MageStatueRed (000811) 255,70,40 at [-92,-88,413], radius 180,
      fade 0.4. The mesh's own colours were deep blue (dead band) and dark red;
      the blue was moved to H~211.
  Authoria_Glow_SmallItems.json  (added 2026-08-16)
      Items whose ENB disc is too small for CS to make anything of (CS radius =
      disc radius x 0.5, and these discs are 0-9 units):
        Fire salts   Clutter\Ingredients\FireSaltPile.nif  [0,1,9]
                     Authoria_Glow_FireSalts (000812) 255,120,30 r60 fade 0.35 flicker
                     (also covers Requiem RedGemDust and Bruma ColdFireSalts, same mesh)
        Barenziah's jewelry box  Clutter\Quest\BarenziahsJewelryBox.nif  [0,0,7]
                     Authoria_Glow_BarenziahBox (000814) 255,70,50 r70 fade 0.35
        Dawnbreaker  Weapons\Dawnbreaker\Dawnbreaker.nif + 1stPersonDawnbreaker.nif
                     [0,9.4,0] (the sun guard)  Authoria_Glow_Dawnbreaker (000815)
                     255,220,150 r100 fade 0.4. LOTD's replica shares the model.
        Enchanting tables  Furniture\EnchantingWorkbench.nif [0,92,78] and
                     Furniture\EnchantingWorkStation.nif [0,64,79]
                     Authoria_Glow_EnchantingTable (000816) 110,170,255 r120 fade 0.35
                     (WeldingMans' disc was violet 241 - dead band - moved to H~215)
      All "faint" on purpose: fade 0.35-0.4. Raise fade before radius if too weak.
  Authoria_SpellHandLights.json  (added 2026-09-09)
      Spells held or cast in the hand emit a real light in their school's colour.
      The game's own hand lights are radius 30-50 (a hand's width), so they never
      reach a wall. Light Placer attaches these at the casting art itself and
      removes them when the spell is released or sheathed; NPC casters too.
      Keyed by casting-art FormID ("formIDs"), NOT model path, so mesh replacers
      (Kittytail's VFX Edits) do not matter. 83 bulb groups / 165 casting arts,
      bulb = the light the load order's own magic effects pair with that art most
      often (census of all 4278 winning effects). Tuning: fade 0.6 (fire 0.7),
      cutoff 0.1, radius 350, InverseSquare|IgnoreScale|PortalStrict. Under
      InverseSquare with a vanilla bulb the cutoff MUST be written - the default is
      the record's falloff exponent (1.0) and collapses the light. Skipped: 60 arts
      with no paired light (throwing knives, bombs, spider spit...) and 5 Triumvirate
      shadow arts whose light is Negative (darkness). Full table and how-to:
      C:\1. AUTHORIA\SPELL-HAND-LIGHTS-20260909.md and ...-COVERAGE-20260909.md.
      Rebuild: scratch build_spell_hand_lights.py from casting_art_census.json.
  ParticleLights\pp_black.ini  (added 2026-08-16, mod root, not this folder)
      Registers CC Arcane Accessories - ENB Light Addon's black disc texture with
      CS. Cull = true. The only unregistered emitter texture in the whole census
      that is mod-specific AND safe (5 emitters). Everything else unregistered is
      either vanilla-textured VFX or already lit by Embers/Lux/this mod.
      Full census: PARTICLE-LIGHT-CENSUS-2026-08-16.txt / .csv in this folder.

COLOR RULE - IMPORTANT
Every light color here deliberately avoids hue 224-295. That band is the
Effects 11 dead band documented in Authoria - RMF Purple Retint\LOCKED-VALUES.md
- painted colors inside it render green or cyan. Violet lights were pushed to
H~300 magenta and blues to H~205 for the same reason. If you retune a color,
keep it out of 224-295.

MODEL PATH RULE - IMPORTANT (learned 2026-08-16, the hard way)
Light Placer looks up gameModels.find(record->GetModel()) - the record's raw
MODL string against the json string. The map is case-insensitive and that is
ALL: no "Meshes\" stripping, no slash normalisation. Vanilla records store
"Clutter\Foo.nif"; a lot of mod records store "Meshes\Clutter\Foo.nif" (816
STATs in this load order do - LoadScreenCompendium, JK's, RedBag's, Dovahnique).
A json path that differs only by that prefix matches NOTHING and LP logs no
error - the entry count in po3_LightPlacer.log still looks fine. So: take the
model string from housecarl_read_record's Model.File, verbatim, never from the
file on disk, and when in doubt list the path both ways. Audited 2026-08-16:
across all 396 LP model keys in the enabled mods (Lux CS included) the only
casualties of this were the 48 Dunmer lantern paths, now fixed.

OFFSETS - DERIVE THEM, DO NOT GUESS
A light's "points" z is an offset from the MODEL ROOT, which is usually ground
level, so a guessed value lands at the plant's feet. Read the record's
ObjectBounds instead - housecarl_read_record with depth=2 gives First/Second as
min/max XYZ, and the z of Second is the object's height above its origin.
Measured here:
  Deathbell    z -16 .. +118   flowers occupy roughly the top half -> light at 80
  Nirnroot     z -56 ..  +58   origin sits mid-plant                -> light at 20
  Gleamblossom z -10 ..  +91   pods along the stalk                 -> light at 45
Deathbell shipped at z=25 in the first pass and the user correctly reported the
glow coming from the base rather than the flowers. The harvested and Hearthfire-
planter deathbell meshes are a SEPARATE group at z=18 with a smaller radius -
they are small potted objects, so the tall-plant offset would float above them.

TUNING
Radius and fade can be overridden per model group in the json without touching
the plugin - see the Blackreach entries, which set radius per mushroom size.
For a global change edit the LIGH record in Authoria - Glow Coverage.esp.
All lights are Dynamic (they light actors, not just terrain) and Simple
(no contact shadows - these are decorative, shadows are not worth the cost) -
except the Dunmer lanterns, which follow Lux CS's ISL lantern convention
(InverseSquare|IgnoreScale|Linear, no Simple) so they match the town's other
lanterns; see that entry.

KNOWN GAP
ParallaxGen duplicates some meshes into _pgpatcher_dups\<n>\... and repoints
records at them. Two Blackreach tiny-mushroom variants are covered by their
current dup paths, which will change on the next ParallaxGen run. If Blackreach
tiny mushrooms go dark after a PG rerun, re-read the model paths and update
Authoria_Glow_Mushrooms.json.
The bush / fern / vine / giant-mushroom entries use the vanilla record paths
(verified 2026-08-16 against Model.File of Skyrim.esm and USSEP's overrides);
PG had NOT re-pointed any of those records at dup paths at that time.
NODE ATTACHMENT (giant mushrooms) depends on the winning mesh keeping a node
called Bone_Top. Vanilla and High Poly Blackreach Mushrooms both have it. If a
future mushroom replacer drops it, LP will attach nothing - swap those entries
to points at the cap heights listed above.

VERIFY IN GAME
Console-click the object and run  logLP  - it lists the lights attached to it.
ReloadLP  re-reads these json files without a restart - BUT it only re-cycles
refs that ALREADY carry a Light Placer light. A mesh that had no light before
(a newly added or newly fixed entry) does not get one from ReloadLP alone; the
ref's 3D has to reload. Easiest is to load the save again. In-session: after
ReloadLP, console-click the object and run  disable  then  enable  - Load3D
fires again and the light attaches.

Created 2026-08-15.
