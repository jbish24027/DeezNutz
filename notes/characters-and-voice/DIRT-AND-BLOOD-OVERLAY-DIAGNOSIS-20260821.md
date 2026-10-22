# Dirt and Blood overlay — why it looks worse than it used to (2026-08-21)

Read-only diagnosis. Nothing was changed. MO2 was open the whole time.

## One-paragraph answer

Nothing in this instance drifted. Every dirt/blood texture, every shader record and the whole
mod/plugin order are byte-identical to the shipped list. The overlay the PLAYER sees is simply a
different set of textures from the one vanilla-race bodies use: because Enora is a UBE race
(00UBE_BretonRace since save #1 on 2026-08-02), Dirt and Blood draws her dirt and blood from the
"Ultimate Body Enhancer - Dirt and Blood" pack (textures\!UBE\filthyfx1-4.dds, bloody1-5.dds).
That pack was baked on 2026-07-02 by re-projecting the HD Retexture (dirt) and Keep It Clean
"Splat" (blood) onto UBE's UV layout, and the bake darkened the colour toward black wherever the
texture is semi-transparent (premultiplied-alpha style). Dirt and Blood's membrane shader
multiplies skin by (colour + 1 - alpha), so faint fringes that are invisible on the HD set become
a visible dark halo on the UBE set; fine speckle reads as black soot; blood edges go black-red.
The bake also softened alpha edges ~15%. Vanilla-race NPCs still get the good set, so a dirty NPC
next to the player looks better than the player.

## What was checked and found unchanged

| Layer | Result |
|---|---|
| Texture files on disk | Only three sources exist for the overlay textures (HD Retexture 2K dirt, Keep It Clean 4K "Splat" blood, UBE pack). No duplicates anywhere else in mods/, overwrite/ or Stock Game. No .mohidden files. |
| CRC vs original archives | HD filthyfx1-4 = archive "2k" option (CEA89B22 / 6BDEC832 / 47418B07 / 6EAF9B60). Keep It Clean bloody1-5 = archive "splat" set. UBE pack textures = archive. Base D&B esp = archive 2.38. Shader Tweak esp = archive. |
| FOMOD choices (FOMOD Plus record in meta.ini) | HD Retexture: 2k, Blood Brightness Default, optional plugin Yes. Keep It Clean: Splat. |
| Mod order | The D&B block (Authoria tweak → Settings Loader → Seamless Soap → Keep It Clean → HD Retexture → ... → base mod; UBE pack lower) is in the same relative order in every modlist backup from 2026-08-02 to today, all four profiles. |
| Plugin order | Dirt and Blood - Dynamic Visuals.esp → Seamless soap patch → Shader Tweak ... → Requiem - Dirt and Blood.esp ... → Authoria - Patch - Dirt and Blood Tweaks.esp → Ultimate Body Enhancer - Dirt and Blood.esp. Same relative order in every loadorder backup (earliest 2026-08-02). |
| Effect shader records (vanilla lane) | Dirty_Shader_Dirt1-4 winner = Dirt and Blood - Shader Tweak.esp (fill alpha 0.5 / 0.6 / 0.7 / 0.8, textures filthyfx1-4.dds). Dirty_Shader_Blood1-5 winner = base mod (alpha 1.0, Bloody1-5.dds). Dirty_SoapFX winner = Seamless soap patch. No Reqtificator / Synthesis / PG touch. |
| Effect shader records (UBE lane) | Dirty_Shader_Dirt1-4_UBE / Blood1-5_UBE defined only in the UBE esp; same alphas and blend modes as the vanilla lane; textures !UBE\filthyfx*.dds / !UBE\Bloody*.dds. |
| Gating | Base dirt/blood MGEFs (overridden by the UBE esp) carry HasKeyword UBE_BodyRace == 0; the _UBE MGEFs carry == 1. Each D&B spell has both effects. No stacking. |
| Player race keyword | 00UBE_BretonRace winner = UBE D&B esp, keyword UBE_BodyRace present. 00UBE_NordRace winner = Authoria - Patch - Serana UBE Face.esp and it keeps the keyword too. |
| Installed UBE esp vs archived esp | 20 bytes smaller: the two Wood Elf UBE races each lost one racial spell (AE3B67:Requiem.esp) from ActorEffect. Wabbajack-time patch, part of the shipped list, unrelated to dirt. |
| Skyrim INIs | No mip skipping, same decal settings in all profiles. CS profile differs only in bUseTAA=0 (CS upscaling handles AA). |
| Community Shaders | Skin feature on, DLSS quality + frame generation on, sharpening off. Not changed for this check; no evidence it is involved. |

## The measurement (stage-4 dirt and stage-5 blood, 1024-sample NEAREST downsample for the bins)

"solid" = alpha > 200, "soft" = 16 < alpha < 96. Colour is mean RGB.

| Texture | covered | RGB > alpha (frac) | solid colour | soft colour | alpha edge std |
|---|---|---|---|---|---|
| HD filthyfx4 (vanilla lane) | 0.302 | 0.089 | (58.6, 49.4, 40.0) | (55.9, 47.0, 38.3) | 39.6 |
| UBE filthyfx4 (player) | 0.306 | 0.000 | (56.1, 47.1, 38.0) | (16.6, 13.3, 10.2) | 33.0 |
| HD filthyfx2 | 0.123 | 0.117 | (58.2, 49.1, 39.9) | (56.8, 47.8, 39.0) | 42.0 |
| UBE filthyfx2 | 0.126 | 0.000 | (55.3, 46.6, 37.7) | (16.1, 13.0, 10.0) | 35.1 |
| Keep It Clean bloody5 (vanilla lane) | 0.377 | 0.321 | (72.4, 2.5, 1.9) | (73.7, 2.5, 2.3) | 21.7 |
| UBE bloody5 (player) | 0.354 | 0.000 | (68.3, 1.7, 0.9) | (24.1, 0.2, 0.2) | 20.3 |

Reading: straight-alpha art keeps the same colour at any alpha (HD/KIC rows). The UBE rows have
the right colour on solid pixels but ~3.4x darker colour on faint pixels, and RGB never exceeds
alpha — premultiplied-alpha behaviour. The edge std drop (~15%) is resampling blur from the bake.

In-game blend simulation (membrane shader: skin * (colour + 1 - alpha)), stage-4 dirt, mean
multiplier on skin:

| | all covered pixels | soft fringe only |
|---|---|---|
| HD (vanilla lane) | 0.44 | 1.02 (invisible fade-out) |
| UBE (player) | 0.45 | 0.87 (visible dark halo) |

A naive un-premultiply (RGB / alpha) overshoots to 1.16 on the fringe (a light halo), so the fix
must rebuild the colour, not just divide it out.

Images: scratchpad\tex\DnB_dirt_stage4_skin_simulation.png, DnB_blood_stage5_skin_simulation.png,
DnB_dirt_stage4_full_textures.png (copies sent in chat).

## Timeline

- 2026-07-02 20:40 — UBE pack textures baked (file dates); esp 21:08. Uploaded to Wabbajack
  authored-files (meta: directURL authored-files.wabbajack.org/...). Version tag d2026.7.3.0.
- 2026-07-27 — this instance installed from the list (all meta.ini 13:26-14:31).
- 2026-08-02 — save #1 of Enora, already 00UBE_BretonRace. Every later save is UBE Breton.
- So the player has never seen the HD set in this playthrough; "what we shipped with originally"
  is the pre-UBE list where everyone used HD Retexture + Keep It Clean on vanilla UVs.

## Fix recipe (not applied)

Goal: keep the UBE pack's alpha (that is the UV layout) and replace its colour with straight-alpha
colour, then re-encode BC7 with mips.

1. Decode the nine !UBE textures (PIL 12.2 reads BC7; numpy 2.4 present).
2. For every pixel with alpha > 0 set RGB = local solid colour: take pixels with alpha > 200,
   blur/dilate their colour across the island (or simply use the per-texture solid mean —
   dirt (56,47,38), blood (68,2,1) — the HD art is almost flat-coloured anyway), keep alpha as is.
   Leave alpha-0 pixels black.
3. Encode: tools\xEdit\Edit Scripts\Texconv.exe -f BC7_UNORM -m 0 (also at
   tools\xLODGen\Edit Scripts\Texconv.exe). 2K dirt, 4K blood, same as now.
4. Ship as a new mod folder "Authoria - Fix - UBE Dirt and Blood Textures" placed above
   "Ultimate Body Enhancer - Dirt and Blood" in all four profiles (MO2 closed for the modlist
   edit; plugingroups untouched because no plugin). Or overwrite in place with a .bak copy.
5. Optional: the HD Retexture archive also has a 4K dirt option (CRCs AB4D0E2F / 9D69F30E /
   4C07EC4C / A6A24484) if the vanilla lane should be bumped to 4K too.
6. Better long-term: redo the bake from the 4K HD source with straight alpha in the converter
   (tools\CBBE to UBE) — sharper than fixing the 2K bake.

## Follow-up: "I thought we had Zaki's overlays for Dirt and Blood" (Nexus 106332)

- The archive in Downloads (Zaki Dirt and Blood Overlays for Racemenu-106332-1-0-1701891773.7z)
  was downloaded 2026-08-21 08:37 — today, after the first report.
- It has never been in this list: not in downloads\, no mod folder, no meta.ini with modid 106332,
  no mention in any modlist backup here, in the v2 export snapshot (08-20), or in any archived
  list state on D: back to the 2.0 pre-hotfix snapshot of 2026-07-21. Every one of those states
  has the same Dirt and Blood block (HD Retexture + Keep It Clean + UBE pack).
- What the mod is: RaceMenu paint overlays only (Body/Hand/Face paint, 4 dirt + 5 blood levels,
  female on CBBE UV, male on SOS UV, 4K or 8K, BC7, NO mipmaps). The esp is an empty script
  carrier; ZakiDirtAndBloodRacemenu.psc just registers the paints. The author's own page says:
  "These textures are Racemenu overlays only. If you wish to use these with Dirt & Blood, then use
  ... Zaki Dirt and Blood Textures for Dirt & Blood & Cum" (LoversLab, NSFW, manual download).
  So the Nexus file cannot drive Dirt and Blood's dynamic dirt at all.
- The art is different: Zaki's dirt is an all-over grime shading on the body layout; the HD
  Retexture is splatter strokes. The UBE bake visibly reuses the HD strokes, so Zaki's was not
  the source of the bake either (sheets: DnB_zaki_vs_HD_vs_UBE_dirt4.png,
  DnB_zaki_vs_KIC_vs_UBE_blood5.png).
- If the Zaki look is wanted for Dirt and Blood: vanilla lane needs the LoversLab D&B version
  (user download), installed above HD Retexture + Keep It Clean; the UBE lane would need that
  texture re-baked onto UBE's layout with straight alpha (tools\CBBE to UBE is a MESH/record
  converter — it does not convert textures; whatever baked the 07-02 pack is not in tools\).
  Zaki's overlays as RaceMenu paint are static and would not wash off.
- Related Nexus files, for the record:
  - 139311 "Zaki 8K-4K Textures for Bathing in Skyrim - Renewed" (Oozaki) — for BiSR 2.30+,
    which applies per-part overlays (Body/Hands/Feet/Head files), a different system from
    Dirt and Blood's single fill texture.
  - 139868 "UBE Conversion for Zaki 8K-4K Textures for Bathing in Skyrim - Renewed" (Ondine,
    2025-01-25) — the only UBE-native Zaki set that exists. Sets A–D, head 4K, body/hands/feet 8K,
    file names DirtFXBody.dds etc. It needs Bathing in Skyrim - Renewed installed and its
    "Player Texture Override" — it is NOT loadable by Dirt and Blood as-is.
  - 130075 — BHUNP variant of the RaceMenu overlays. Not relevant (UBE).
  - Bathing in Skyrim - Renewed itself has never been in any list state (2026-07-21 → today);
    only the Malignis animation pack and its D&B patch are. Switching Enora's dirt to BiSR +
    139868 would be a system swap (MCM slot, Requiem, scripts, save), not a texture swap.
- Converters on this machine: tools\CBBE to UBE (Authoria-DaysTool fork) and
  D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\UBE-Converter (v3.6) both convert ARMOR MESHES and
  records. Neither converts textures. The 07-02 D&B bake was made with something else.

## Build 2026-08-21: Zaki UBE dirt on the player (user's choice), NPCs unchanged

User decision: "BISR - Zaki Renewed - UBE Set A" (Nexus 139868) is the dirt that shows on the
player; NPCs keep what they have. Built as a bridge, not a system swap (no Bathing in Skyrim):

- Mod "BISR - Zaki Renewed - UBE Set A" — Textures\mzin\Bathe\Set1\F\DirtFXBody.DDS (8K),
  F\DirtFXFace.DDS (4K), M\DirtFXBody.DDS (8K). Hands/Feet/M-face files omitted (byte-identical
  duplicates, CRC-verified). Archive copied to downloads\ with a hand-written .meta.
- Mod "houseCARL - Authoria - Patch - Player Dirt Overlays" — ESL-flagged, form 44, masters
  Skyrim.esm / Dirt and Blood - Dynamic Visuals.esp / Ultimate Body Enhancer - Dirt and Blood.esp.
  - GLOB Authoria_PlayerDirtStage (0x800)
  - MGEF Authoria_Dirty_Effect_Dirt1..4_PlayerOvl (0x801-0x804): mirrors of Dirty_Effect_DirtN_UBE
    (name, description, flags, Dirty_Blood_Keyword on 2-4, perk Dirty_Perk_VeryDirty on 4,
    archetype ValueModifier/HealRateMult, ConstantEffect/Self) with NO HitShader; conditions
    HasKeyword UBE_BodyRace == 1 AND GetIsID Player == 1; script Authoria_PlayerDirtOverlay with
    Stage (1-4), OverlayAlpha (0.3 / 0.55 / 0.8 / 1.0), StageGlobal -> 0x800.
  - MGEF overrides Dirty_Effect_Dirt1..4_UBE: + condition GetIsID Player == 0 (UBE NPCs unchanged).
  - SPEL overrides Dirty_Spell_Dirt1..4: the UBE esp's version + the _PlayerOvl effect as 3rd entry.
  - Scripts\Authoria_PlayerDirtOverlay.pex (+ Source\Scripts): OnEffectStart puts the textures on
    the highest free Body/Hands/Feet/Face overlay slot (or the slot already carrying them) with
    the stage's alpha; OnEffectFinish clears them unless a newer stage already owns the overlay.
    Uses NiOverride (RaceMenu). skee64.ini: 28/18/18/26 slots, bPlayerOnly=1 — sufficient.
  - check_errors: 0 dangling, 0 missing masters. Compiled against RaceMenu's nioverride.psc,
    SKSE64 sources and the vanilla Scripts.zip (CK compiler at
    "Skyrim Special Edition 489830\Papyrus Compiler", now set in houseCARL).
- Placement (script _tools\mod-install-helpers\insert_player_dirt_overlays.py, all 4 profiles):
  both mod folders directly above "Ultimate Body Enhancer - Dirt and Blood"; the plugin right
  after "Ultimate Body Enhancer - Dirt and Blood.esp" (group "Authoria - Master Patches").
  The script refuses to run while MO2 is open and backs up the four files (.bak-playerdirt-20260821).
- Behaviour change to know: player's clothes/armour no longer show dirt (overlays are skin-only);
  a blood stage still replaces the dirt stage (Dirt and Blood's own model); player blood is still
  the UBE bake.
- TEST PENDING (user): get dirty (or console: player.addspell <Dirty_Spell_Dirt4>), check body,
  hands, feet, face; wash; check removal; reload a save mid-stage; check a dirty UBE NPC and a
  dirty vanilla-race NPC still look as before.

### Round 1 FAILED — "it's unchanged" (user, 2026-08-21 ~17:05). Cause + fix

What was NOT wrong (checked before touching anything):
- Mods still enabled after MO2's 16:44 rewrite; plugin still starred; ESL, form 44.
- The patch IS the load-order winner for Dirty_Spell_Dirt1..4 and Dirty_Effect_Dirt1..4_UBE
  (conflict tree, live order — nothing later re-overrides them).
- Player race: the new test character ("Prisoner", forest start, saves 16:49/16:51) is
  00UBE_BretonRace, so the UBE_BodyRace gate passes.
- Compiled .pex carried the correct texture paths; check_errors and validate_scripts clean.
- Textures resolve: BISR - Zaki Renewed - UBE Set A wins all three paths (loose, uncontested).

The cause was three bugs in MY script, found by reading the two overlay mods already in this
load order that demonstrably work — Ultimate Body Enhancer - Wounds
(WoundsOverlaysAppliedScript.psc) and OCum Ascended (OCumUtils.psc). Both agree on all three:
1. Overlay nodes are LOWERCASE: "Body [ovl0]". I used "Body [Ovl0]" (skee64.ini's comment spells
   it that way). A node name that does not resolve is a SILENT no-op — nioverride.psc even warns
   "THESE DO NOT SELF CLEANUP IF THE NODE IS NOT FOUND". No error, no log, nothing drawn.
2. On the PLAYER every overlay slot already exists and carries
   actors\character\overlays\default.dds. My free-slot test was `!HasNodeOverride(...)`, which is
   FALSE for every slot on the player — so FindFreeSlot returned -1 and the script applied
   nothing at all. Correct test: texture is "" OR equals that default.
3. Texture + alpha alone does not render. The working stack is 9/0 texture, 7/-1 tint colour
   (white 16777215), 0/-1 emissive colour 0, 1/-1 emissive multiple 1.0, 8/-1 alpha,
   2/-1 glossiness 0.0, 3/-1 specular 0.0.

Fixed 17:15: script rewritten to mirror the working implementations (lowercase nodes, correct
free-slot test, full key stack, cleanup restores default.dds), recompiled, verified in the .pex
string table. Opacity ramp raised 0.3/0.55/0.8/1.0 -> 0.50/0.65/0.80/1.00, because stage 1 at
0.3 of Zaki's LEAST-coverage set would have been near-invisible even once it rendered; the UBE
shaders it replaces ran 0.5-0.8. Papyrus logging enabled in the CS profile Skyrim.ini
(backup .bak-playerdirt-log-20260821) and Debug.Trace added at every decision point, so a third
round would have evidence instead of another guess. Turn logging back off after the test.
Plugin data layer was NOT touched except the four OverlayAlpha values; ESL + form 44 re-verified.

### Round 2 FAILED too — and the log finally named the cause (2026-08-21 ~17:50)

User relaunched after the 17:15 script fix (new game 17:45, save 17:47) — old dirt still drawn.
This time there was evidence, because logging was on:
- The Papyrus log contains NOT ONE trace from Authoria_PlayerDirtOverlay, and no
  "Cannot open store for class" error for it either. So the script was never even reached:
  the magic effect never applied. The round-2 script fixes were necessary but not sufficient.
- The plugin IS loaded: it appears in the 17:47 save's own LIGHT PLUGIN LIST (parsed from the
  .ess — 241 regular + 3821 light). So "the patch isn't active" was ruled out, not assumed.
- 000007:Skyrim.esm IS the Player NPC record (verified — its Name is even "Prisoner",
  the test character). So the condition's parameter was correct.

CAUSE: the `GetIsID Player` condition never matches. Proof from this session, not theory —
the UBE baked effect carried BOTH `HasKeyword UBE_BodyRace == 1` AND my added
`GetIsID Player == 0`, and it still rendered on the player. So HasKeyword evaluates correctly
and GetIsID(Player) returns 0 for the player. Symmetrically my effect's `GetIsID Player == 1`
was false, so it was skipped and the script never ran. **Do not use GetIsID to test for the
player in a magic-effect condition in this load order.**

THE REDESIGN (17:55) removes the need for any player test at all. Established first, by reading
Dirt and Blood's own scripts: `Dirty_Spell_Dirt1..4` are PLAYER-ONLY — every AddSpell for them
in Dirty_Script / Dirty_Raining / Dirty_Quest_MCM targets PlayerRef, and NPC dirt uses entirely
separate spells (`Dirty_Spell_DirtForNPCs`, `Dirty_BloodySpellforNPCs`). A reverse-reference
query confirmed `Dirty_Effect_Dirt1..4_UBE` are referenced by those four player spells and
NOTHING else. Therefore:
- The four overrides of `Dirty_Effect_Dirt1..4_UBE` were REMOVED from the patch entirely
  (the shared UBE records are now untouched — smaller conflict footprint).
- The baked UBE effect was instead REMOVED from the four player dirt spells' effect lists.
  Each spell is now [vanilla-lane Dirty_Effect_DirtN, Authoria_..._PlayerOvl].
- The `GetIsID Player` condition was removed from the four _PlayerOvl effects; the only gate
  left is `HasKeyword UBE_BodyRace == 1`, which this session PROVED works.
Net effect per case — UBE player: vanilla effect skipped by its own `UBE_BodyRace == 0` gate,
mine applies, script runs, Zaki overlay. Non-UBE player: vanilla HD dirt, mine skipped.
UBE or vanilla NPC: nothing changed at all (different spells).
Final plugin: 9 records (GLOB + 4 MGEF + 4 SPEL overrides), ESL, form 44, 0 dangling refs.

TEST: load the save, then MCM > Dirt & Blood > "Restart Player Effects" — that removes and
re-adds the dirt spells so the new effect list takes hold on an existing save. A new game needs
nothing. If it still fails, the log now distinguishes every branch.

### ROUND 4 — ROOT CAUSE PROVEN (2026-08-21 18:06)

Round 3 was tested (session 17:58, new game, save 18:01) and STILL produced zero script traces.
That ruled out the effect list, the conditions, and the save state — the effect was applying and
the script was simply never running. Two independent local proofs found it:

1. `Authoria_WashRadiusEffect` (000800:Authoria - Patch - Dirt and Blood Tweaks.esp) — the Wash
   Followers power, a scripted magic effect that demonstrably WORKS in this same load order —
   has `Archetype.Type = Script`. Mine had `ValueModifier`.
   **A MagicEffect runs its attached Papyrus script only when its archetype is Script.** With any
   other archetype the effect applies, the script loads, and OnEffectStart never fires — with no
   error of any kind in the Papyrus log. Silent.
2. The RaceMenu `.skse` co-save is a direct oracle: it contains
   `actors\character\overlays\default.dds` plus the SFO-freckle and RX overlay paths (so the
   overlay system was live and writing), while `mzin` and `DirtFX` occur ZERO times — proving the
   texture had never been applied even once, in any round.

FIX: all four _PlayerOvl effects set to `Archetype.Type = Script`, ActorValue None, and flags
matched to the working effect (`Recover[, Detrimental], NoHitEvent, NoDuration, NoMagnitude,
NoArea, FXPersist`). A Debug.Trace was added at the TOP of OnEffectStart, before the player
guard, so the log now proves whether the event fires at all. Plugin re-verified: ESL, form 44,
9 records, 0 dangling refs, 0 unbound properties.

Everything fixed in rounds 2-3 was real and necessary — lowercase `[ovl` node names, the
default.dds free-slot test, the 7-key shader stack, dropping the non-matching GetIsID condition,
and removing the baked UBE effect from the four player-only dirt spells — but none of it could
ever have shown up while the archetype was wrong.

## Side notes found on the way

- The base "Dirt and Blood - Dynamic Visual Effects" folder has had its own Bloody1-5, filthyfx1-4,
  soapfx and soapparticlefx deleted. Harmless now (HD Retexture / Keep It Clean / Seamless Soap
  cover every path) but disabling any of those three leaves vanilla-race actors with missing
  textures.
- HD Retexture's own blood textures and soap particle were never installed (FOMOD says Blood
  Brightness Default, but the files are absent) — Keep It Clean "Splat" blood is the deliberate
  choice.
- Your own MCM recording (McmRecorder\jbish base\0002_Dirt & Blood.json, 2026-07-28) sets
  "Dirt on Player" to "Rarely - 2 to 4 days"; the shipped Authoria_Base recording leaves it at
  default. That changes how fast dirt builds, not how it looks.
- Requiem - Dirt and Blood.esp only touches 13 MGEF + 9 SPEL (no shaders); the UBE esp forwards it.
