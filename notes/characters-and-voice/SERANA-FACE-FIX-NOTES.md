# Serana bald / dark face — investigation and fix (2026-08-17)

## What you saw
Serana in Dimhollow: no hair, face darker than her body, glowing pale eyes.

## What is actually on disk / in the load order (all measured with houseCARL)
| Item | Finding |
|---|---|
| Her NPC record (winner) | `Requiem for the Indifferent.esp` — plain vanilla Serana: NordRace, vanilla brows / vampire eyes / face marks / `DLC1HairFemaleSerana`, weight 20. Only 6 plugins touch her, none is a replacer. |
| Her facegen keyed to her own FormID | Vanilla only (`Skyrim - Meshes0.bsa` / `Textures0.bsa`). No mod overrides `FaceGeom\Dawnguard.esm\00002B6C.nif`. |
| The UBE look | `UBE Serana - NPC Replacer` (Nexus 184078), **Multiform** variant: no override of her record. It ships facegen keyed to `SeranaMultiformNG.esp\00000801` (vampire) and `\00000802` (cured), a SkyPatcher ini that sets her race to `00UBE_NordRace`, and an outfit ini. |
| Serana Multiform NG (DLL, v1.1.1 dated 2026-05-05) | Disassembled `ApplyPresetToActor`: sets her `faceNPC` to the form (0x801/0x802), copies race, height/weight, body tint, tint layers, hair colour, face texture — then `TESNPC::ChangeHeadPart(hair)` on **her own** record and `Actor::DoReset3D`. It does **not** copy the other head parts (brows/eyes/lashes) or face morphs. |
| Vampire form 0x801 (winner RftI, carries the UBE look correctly) | race UBE Nord; head parts `_OriSeranaUBE_Lashes/_Brows/_Eyes/_Hair`; hair colour 01; skin `_OriSeranaUBE_Skin`; tint skin tone 160,177,177; weight 50. Cured form 0x802: same four parts, tone 166,160,152, hair colour 02. |
| Baked facegen 00000801.nif | Has hair baked in (`_OriSeranaUBE_Hair`, `_HL`, `_Hairline`), head shape `00UBE_FemaleHead`, OriSerana head diffuse + facetint 00000801.dds. Fine. |
| Hair head part model | `_OriSeranaUBE_Hair` (and its two extra parts) point at `meshes\!UBE\OriSerana\Hair.nif` — **ABSENT from the whole VFS**, and absent from the mod's archive (checked the .rar). The mod relies on the baked head only. |
| Hair texture | DXT3, fine. Not the cause. |
| INI | `bUseFaceGenPreprocessedHeads` untouched (default). No RaceMenu NPC preset for her. |

## Reading
After Multiform NG runs, her own record has vanilla brows/eyes/marks + the OriSerana hair, and the engine
rebuilt her head from head parts instead of loading the baked one:
- rebuilt hair → needs `!UBE\OriSerana\Hair.nif` → missing → **bald**
- rebuilt face → no baked face tint → **dark**
- rebuilt eyes → the OriSerana eye part has no texture set → **wrong glowing eyes**
- the visible brows are thin (vanilla `FemaleBrowsHuman07`), consistent with a rebuild from her own parts.

So this is **not** the Lydia mechanism (Lydia's head *was* the baked one; only its runtime tint value was black).
The Lydia-style tint override alone would leave Serana bald. Where exactly the engine decides "rebuild vs load"
could not be read from the exe (Steam-encrypted .text), so the fix removes every trigger at once.

## The fix — mod `houseCARL - Authoria - Patch - Serana UBE Face` (built, NOT yet enabled)
1. **SkyPatcher** `SKSE\Plugins\SkyPatcher\npc\OriSeranaUBE - Authoria Fix\OriSeranaUBE.esp.ini`
   `filterByNpcs=Dawnguard.esm|2B6C:race=UBE_AllRace.esp|5A184:copyVisualStyle=SeranaMultiformNG.esp|801:skin=OriSeranaUBE.esp|83A:weight=50`
   Her own record gets the full vampire look at data load → matches the baked head → Multiform finds the same
   hair, swaps nothing, and the engine loads the baked facegen. Folder name sorts after the mod's own
   `OriSeranaUBE` folder so the race is already UBE when the copy runs. Gated on `OriSeranaUBE.esp`.
   The vampire↔cured switch keeps working (both forms use the same four head parts).
2. **Own-FormID facegen**: byte copies of the installed (neck-pinned) `00000801.nif/.dds` as
   `FaceGeom\Dawnguard.esm\00002B6C.nif` / `FaceTint\Dawnguard.esm\00002B6C.dds` — correct even before Multiform
   runs, or if it is ever disabled.
3. **SPID ability** (`Authoria - Patch - Serana UBE Face.esp`, ESL, MGEF 0x800 + SPEL 0x801, script
   `Authoria_SeranaFaceFix`): prints a `[SeranaFace]` probe to the console + Papyrus log (which head is on her,
   head diffuse + facetint texture paths, whether the OriSerana hair shapes exist, her base head parts, race,
   weight, the head shape's ShaderTintColor) and, only if that tint reads 0,0,0 (Lydia gap), writes the form's
   skin tone as a persistent NiOverride (vampire 160,177,177 / cured 166,160,152). This is the visible test of
   the "same as Lydia" hypothesis.

Verified so far: script compiles; plugin passes `housecarl_check_errors` (0 dangling, 0 missing masters).
Wired 2026-08-17 10:30 into all four profiles (enabled in DEEZ CS NUTZ and DEEEZ NUTTZZZ, listed disabled in the two
legacy Requiem Reforged profiles): mod right after the Lydia runtime patch, plugin right before `PG_1.esp`, group
`Authoria - Outputs`. Backups: `backups\serana-face-wire-20260817-102956`. `housecarl_skypatcher_read` on Serana
confirms race / skin / weight applied and the copyVisualStyle directive recognized. The SkyPatcher ini was split
into two lines (race on its own line first) so the copy never runs before the race change.

## How to read the probe in game (console, after she loads)
- `head facetint = ...FaceTint\SeranaMultiformNG.esp\00000801.dds` → baked head loaded (good)
- `_OriSeranaUBE_Hair=True` → hair present
- `base headparts(4): [5]OriSeranaUBE_Lashes [2]OriSeranaUBE_Brows [3]OriSeranaUBE_Eyes [4]OriSeranaUBE_Hair` → SkyPatcher copy applied
- `tint fix: before=0,0,0 wrote=160,177,177 after=160,177,177` → Lydia gap was present too, fixed
- `tint ok: key7=160,177,177` → nothing needed
- `no '00UBE_FemaleHead' shape` or `head facetint = ` (empty) → head still rebuilt at runtime → report back

## Side notes
- `Universal Cured Serana Eye Fix` (SeranaEyeFix.esp) will slap a vanilla human eye texture on the OriSerana eye
  mesh when she is cured; the cured form already has cured eyes baked. Consider disabling it when/if she is cured.
- The Reqtificator patch (`Requiem for the Indifferent.esp`) already carries the OriSerana look on the two
  Multiform forms — a Reqtificator rerun will keep it (it copies the winner).
- Old memory said "Serana was fine" on 2026-08-16 — that was an in-game impression, never measured; her head
  was probably rebuilt then too.

## Round 2 (2026-08-17 ~11:30) — after the first in-game test
Test result: not dark any more, still bald, face generic. Lydia is the same class of problem (her "fixed" face is a
runtime-rebuilt generic UBE head, not her sculpted bake).

Five-agent investigation results (full data in the session transcript):
1. No INI or RaceMenu setting disables baked heads (bUseFaceGenPreprocessedHeads absent everywhere = ON; skee64.ini clean; only RaceMenu's stock bDisableFaceGenCache=1).
2. Lydia record vs bake: aligned 1:1 by part EditorID; all models present; no ValidRaces exclusions. A rebuilt head explains "wrong face, right hair" exactly: her unique face diffuse lives only inside the bake; the record's head part carries the generic UBE head texture set.
3. Serana: ValidRaces excludes NOTHING (a patch plugin already injected all UBE races into the vanilla hair list). The bake is internally correct. The ONLY hard fault: !UBE\OriSerana\Hair.nif is the model of ALL THREE hair parts and exists nowhere -> any rebuild is bald.
4. The 10:36-10:51 test was a NEW GAME; Serana Multiform NG never logged applying an appearance; both SkyPatcher inis processed clean; skee64 logged nothing per-NPC.
5. Engine research: documented rebuild triggers are (a) missing facegen file, (b) bake vs record head-part mismatch. No race-vs-bake check is documented. Regenerated heads drop tint layers (dark face) - Face Discoloration Fix exists to patch exactly that.

Fixes landed this round (all in the same mod):
- Extracted the three baked hair shapes into standalone HDPT models (structure mirrored from Lydia's WORKING Soledad F.nif): meshes\!UBE\OriSerana\Hair.nif / HairHL.nif / Hairline.nif. Verified by two independent parsers (shapes, skin, partitions SBP_131, alpha 0x12ED/0x12EE, textures, bones all intact). The ESL now also overrides _OriSeranaUBE_HL and _OriSeranaUBE_Hairline to point at their own models (masters now include OriSeranaUBE.esp). Even a runtime rebuild can no longer be bald.
- Fixed the cross-keyed embedded facetint in my copied Dawnguard.esm 02B6C.nif (slot 6 now points at Dawnguard.esm 02B6C.dds; was pointing at SeranaMultiformNG.esp 00801.dds) - the one bake anomaly that could reject or mistint the baked head.
- Probe v2: now covers Lydia too, and writes to Data\Authoria_FaceProbe.txt (lands in MO2 overwrite) - the next session's file tells us per-NPC whether the rendered head is the BAKE (head tex0 = the NPC-specific diffuse, tex6 = a FaceGenData\FaceTint path) or a REBUILD (generic !UBE\Head diffuse).
- Removed a stale SkyPatcher backup ini that was double-applying pre-natsplit UBE Converter 3 armor values since 08-13 (moved to mods\Authoria - UBE Converter Output\_removed-from-skypatcher\).

Open question for the probe: does Serana's head now load the bake (record parts aligned by SkyPatcher copyVisualStyle + fixed slot 6 + own-FormID facegen), and does Lydia's? If Lydia still rebuilds despite full alignment, the next suspect is the custom RacemenuHeadpartsExcluder.dll (it repoints 21k+ head parts' race lists at load; its ini has enabled=0 as a safe A/B switch).

## Round 3 (2026-08-17 ~12:00) — ROOT CAUSE FOUND
The probe file from the second test session is conclusive:
- Lydia's rendered head uses the GENERIC UBE head diffuse -> runtime rebuild, ground truth.
- Both NPCs' runtime head-part lists contain `00UBE_HumanFemaleLashes` with **Type = 160** — an invalid
  pseudo-type. Source: **my own `Authoria - Fix - Lashivious Lash Meshes.esp`** (2026-08 lash fix) retypes
  ALL 85 lash parts to 160 so the 25 Lashivious variants can coexist in RaceMenu. Side effect never seen:
  that part is ALSO the UBE races' default female head part — with type 160 nothing supersedes it, so EVERY
  female UBE NPC carries a part that exists in NO baked head -> permanent parts-vs-bake mismatch -> the
  engine rebuilds every baked UBE NPC head (the documented dark-face trigger). This broke Lydia (and made
  the 08-16 "weight/tint" diagnosis a band-aid on the rebuild) and Serana alike. Bonus symptom: both NPCs
  were wearing DOUBLE lashes on the rebuilt heads.
- Serana additionally kept her vanilla face-marks part (SkyPatcher copyVisualStyle merges by type; the
  donor has no marks-type part, so the vanilla one survived) — a second bake-mismatching part.

Fixes landed (all in `Authoria - Patch - Serana UBE Face.esp`):
1. Race override `00UBE_NordRace`: removed `00UBE_HumanFemaleLashes` from the female default head-part
   list (now head/eyes/brows/mouth, renumbered). Scope: ONLY the UBE Nord race — the player (UBE Breton)
   and the whole Lashivious lash system are untouched. Blast radius checked: the only NPCs on this race
   are Lydia, Serana, the two Multiform forms (all carry their own lashes) and two chargen dummies.
2. Serana record override (wins over RFTI): full OriSerana vampire look at the record level — the four
   OriSerana head parts, UBE Nord race, hair colour 01, OriSerana skin, weight 50, skin-tone tint layers,
   vanilla face morphs removed (the bake was made without them). Body fields carried from the current
   RFTI version (Requiem torch etc.). NOTE: re-verify this override after every Reqtificator rerun —
   it freezes RFTI's current gameplay fields for her.
3. Vampire-variant race checked: its female list is head+mouth only — no edit needed.

Expected next probe: `record headparts(12)` for both, `head tex0` = the NPC-specific face diffuse
(!UBE\Lydia\Head\... / !UBE\OriSerana\Head\...), `head tex6` = a FaceGenData\FaceTint path, and the
sculpted faces + hair in game. If STILL rebuilt: next suspect is RacemenuHeadpartsExcluder.dll (A/B via
its ini `enabled=0`).

## Round 4 (2026-08-17 14:40) — the crashes, and CONFIRMATION the fix works
Two CTDs near Serana (11:48, 14:24). Both crash logs: render thread, `BSLightingShader` on Serana's
`00UBE_FemaleHead`, material already `BSLightingShaderMaterialFacegenTint` (RGB-tint type), fault reading a
texture pointer whose bytes were two floats (0.627 / 0.651 = 160/255 and 166/255 - my tint values).
The 14:2x probe file shows the sequence exactly:
  pass 1: head tex0 = OriSerana face diffuse, tex6 = FaceGenData\FaceTint\...\00000801.dds  <- BAKED HEAD LOADED
          record headparts(12), lashes/marks gone                                            <- round-3 fix WORKED
          "tint fix: before=0,0,0 wrote=166,160,152 persisted=TRUE"                          <- my band-aid fired
  pass 2: tex6 = ...\Femalehead_wet.dds                                                     <- material CONVERTED
  next load -> CTD.
Mechanism: NiOverride ShaderTintColor (key 7) on a BAKED FaceGen head converts the material to the RGB-tint
type; the renderer keeps the FaceGen path and reads the colour as a texture pointer. Only ever safe on
runtime-rebuilt heads (that is why the Lydia fix "worked" on 08-16 - her head was a rebuild then).
And the override was PERSISTENT: RaceMenu re-applies it from the save on every load, so the crash recurs.

Fixes:
- Probe script is now read-only, and REMOVES the stale persistent key-7 override from both actors
  (Serana + Lydia) then queues a 3D refresh, so existing saves heal themselves on next load.
- Lydia's own tint fix ("Lydia Weight Runtime") is PARKED: its SPID ini renamed *.PARKED-20260817-...
  (README explains). Her head is now baked too and must not be written to.
Expected: no crash near either NPC; probe shows "REMOVED stale persistent key-7 tint override" once per
actor, then "tint key7=... (read-only; no override present)" afterwards, tex6 = FaceGenData\FaceTint path.

## RESOLVED 2026-08-17 ~15:00 — user confirmed "lydia and serana are fixed!"
Final probe (last session): Lydia head tex0 = !UBE\Lydia\Head\FemaleHead_D.dds, tex6 = FaceGenData\FaceTint\
Skyrim.esm\000A2C8E.dds (her BAKE), record headparts(12), no override present. Serana head tex0 = OriSerana
diffuse, hair/HL/eyes/brows shapes present, headparts(12), no override. No crash logs after 14:24.
(Serana's tex6 shows a "_wet" texture: Community Shaders' skin feature rewrites that slot at runtime on her
head — cosmetic to the probe only; the face is the bake.)

Final state of the fix — mod `houseCARL - Authoria - Patch - Serana UBE Face` (ESL, enabled in CS + non-CS
profiles, listed disabled in the two legacy profiles):
- Race override 00UBE_NordRace: default female lashes entry removed  <- THE ROOT-CAUSE FIX (both NPCs)
- Serana record override: full OriSerana vampire look at record level (re-verify after Reqtificator reruns)
- SkyPatcher ini (race + copyVisualStyle + skin + weight): now redundant with the record override, harmless;
  keeps her right if the ESL ever loses to a later override
- Own-FormID facegen copies (Dawnguard.esm\00002B6C.nif/.dds, slot-6 fixed)
- Standalone hair models Hair/HairHL/Hairline.nif + HL/Hairline HDPT repoints (safety net for any rebuild)
- Probe ability (read-only; strips stale key-7 overrides): SAFE TO LEAVE ON; disable by renaming
  `Authoria - Serana UBE Face_DISTR.ini` if the console spam bothers you.
- Lydia Weight Runtime mod: SPID ini PARKED (must stay parked)
Left in place / not undone: `Authoria - Fix - Lashivious Lash Meshes.esp` type-160 retype (still needed for
RaceMenu); other UBE races still list the type-160 default lashes part — remove it from any UBE race that
gets a baked NPC replacer in future (Breton = the player, no baked NPCs on it today).
