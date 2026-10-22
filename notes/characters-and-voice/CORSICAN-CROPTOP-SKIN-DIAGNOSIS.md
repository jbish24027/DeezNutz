# Corsican Raider Crop Top — torso/neck skin: diagnosis + FIXES (2026-08-21)

Two real defects found and fixed the same day. Both live in the minted `*_UBE` crop-top ArmorAddons
(`000B89:Authoria - Output - UBE Converter 2.esp` base + `000BAE/BB4/BBC/BC0:Authoria - Output -
UBE Converter.esp` variants 2–5). Architecture context: see "UBE outfit lane" notes below.

## Defect 1 (the sighting) — variant texture swap painted the BODY
**Symptom:** wearing Crop Top **2–5**, the whole torso + arms + neck skin render with the variant's
woven fabric texture (burlap/ruffle patterns smeared by body UVs). Face and hands clean (different
meshes). Base "Corsican Raider Crop Top" was never affected. Third person.

**Cause — a July regression:** variant color = an AlternateTextures entry targeting a shape **by
3D index**. Original ARMAs: Index=0 (raw mesh order: fabric shape first). The converter correctly
re-authored Index=**1** for its own July mesh (`!UBE\...Top_1.nif`, body shape first). Then the
07-31 15:21 hand-remake of that mesh (in `houseCARL - Authoria - Fix - Corsican Raider UBE Meshes`,
which WINS the path) put the fabric shape back at index 0 / body at index 1 — nobody re-pointed the
minted records. Since July 31, Index=1 = **BaseShape**, so the fabric TXST
(`00_TexCorsicanCropTop2..5`) replaced the body's skin texture set at runtime.

**Fix applied:** `WorldModel[0].AlternateTextures[0].Index` and `WorldModel[1].AlternateTextures[0].Index`
set 1 → 0 on all four variant ARMAs (`000BAE/BB4/BBC/BC0`), in place, each verified; check_errors clean.
(First-person models carry no alternate textures — variants show base fabric color in 1st person,
matching the original author's own setup.)

## Defect 2 (real, secondary) — first-person models on the raw mesh
All 5 minted ARMAs' `FirstPersonModel[1].File` still pointed at the RAW 3BA mesh (the converter
tool never repaths MOD4/MOD5). In first person the torso/arms rendered the 3BA body with BnP CBBE
skin. Fixed earlier the same day: repointed to `!UBE\[Ashtoreth] Corsican Raider Top\..._1.nif` on
all 5. This was NOT the user's sighting (theirs was third person) but was broken all the same.

## Verified-good (checked before the fixes, all still true)
Converted mesh (fix-mod copy, wins): fabric `SeaPirateTop1` 6820 verts + `BaseShape` = exact UBE
body (29298 verts, same as naked `femalebody_tangent_1.nif`), `!UBE` textures, Skin Tint shader
byte-identical to the naked body's. TRIP morphs match both shapes. SkyPatcher attach lines present
for all 5 ARMOs and loaded clean in-session. UBE races have ArmorRace=null → raw-lane ARMAs never
render on UBE actors; no double-render.

## Standing risks
1. **Re-running Authoria-DaysTool regenerates the converter ESPs and regresses BOTH fixes**
   (5 first-person paths + 8 alternate-texture indices). Re-apply after any re-run, or teach the
   tool: (a) repath MOD4/MOD5, (b) recompute AlternateTextures indices against the WINNING mesh.
2. **Any future hand-remake of a multi-shape `!UBE` mesh must preserve shape order** — minted
   AlternateTextures indices bake the order in. (Corset/Jacket/Top 2 are single-shape: immune.
   Skirt is multi-shape but its mesh is the converter's own copy: consistent.)
3. Same two defect classes may exist on other converted outfits — audit chip queued
   (first-person raw paths with baked bodies; alt-texture indices vs winning-mesh shape order).

## Rollback
`mods\Authoria - UBE Converter Output\*.bak-croptop1stperson-20260821` — both ESPs as of before
today's edits (taken before the first-person fix; restoring reverts BOTH fixes).

## Test
1. Equip Crop Top 2, 3, 4, 5 in third person: torso/arms/neck skin must match naked UBE skin; the
   fabric color must sit on the TOP only.
2. Base Crop Top: unchanged (was always fine).
3. First person, any variant: look down / raise fists — skin matches UBE; fabric shows base color.

## Round 3 (2026-08-21, after both fixes): skin CONFIRMED FIXED; residual neck object
User confirms torso/arm skin is normal. Remaining: a pale, folded, skin/cream-colored band at the
base of the neck / upper chest that appears IFF the crop top is equipped (pants irrelevant) and
moves around with animation.

**Exhaustively ruled out on disk (all verified this session):**
- The winning `!UBE` mesh contains NOTHING near the neck: fabric tops out at Z=111; body Z
  histogram is bucket-identical to the naked body (max 114.5, the neck seam). Stored bounds honest.
- Fabric AND body skinning byte-equivalent to naked (46/16 bones, bind transforms sane, 0 weight-sum
  errors — conversion even fixed 106 slightly-bad sums the raw build had).
- TRIP morphs: crop tri vs naked tri = same 196 body morphs; 17 differ only in minor detail sliders;
  max morph offset above chest height 2.4 units — cannot build a band.
- Exactly ONE minted ARMA attaches (single SkyPatcher line per ARMO); "my UBE output" duplicate
  converter run exists but is DISABLED; original ARMA can't render (ArmorRace null).
- No Corsican rules in Dynamic Armor Variants, IED, Dynamic Fur Morph (Khajiit-only), KID/ORF inis.
- W&C hoods ruled out (hair visible; their minted ARMAs use vanilla meshes).
- UBE skin has no underwear/neck addon.

**Conclusion (SUPERSEDED by Round 4 below — it WAS in the file, in the one block Round 3 never read):**
Prime suspect: RaceMenu body-paint overlays being re-cloned onto the armor's body shape on equip —
OverlayFix.log fires bursts of "geometry doesn't match source pointer, skipping" exactly at load
and equip moments, and UBE-race overlay fragility is a documented prior issue in this setup
(skee64.log has overlay logging off, so no direct confirmation). Secondary suspect: OBody
clothed-state slider application.

**Decisive in-game tests (30s each):**
A. Equip any OTHER body-slot top (e.g. a Ninirim one). Band present too → not Corsican-specific;
   it's the body-armor overlay/morph lane shared by all slot-32 gear.
B. With the band visible: RaceMenu → Body Paint → zero/remove all overlays. Band gone → overlay
   clone on the armor body is the cause (OverlayFix "skipping" path).
C. OBody menu → re-apply / switch preset while wearing the top → tests the clothed-morph lane.

## Skirt SMP verification (2026-08-21) — CONFIRMED GOOD, one fix applied
The active UBE conversion of the skirt (`!UBE\...Skirt_0/_1.nif` + its xml, converter output mod,
sole provider) is the best available copy:
- Geometry byte-equal to the author's build (bbox deltas 0.00–0.03 across all 4 shapes, both
  weights) — unlike the disabled July-21 attempt, which warped shapes up to ~0.8 units.
- Full SMP rig intact: 11 nested Ash_B cloth chains (5–6 links each), 95 nodes — NOT flattened.
- Physics link correctly re-pathed to the `!UBE` xml; raw lane keeps its own shipped xml.
- Minted ARMAs (base `000837` + 4 variants) point at the `!UBE` mesh; variant AlternateTextures
  indices all match the shape order (skirt=0, belt=1, '2'=3) — no crop-top-style index bug.
- The xml's references to 46 nonexistent bones (chain link-7s, breast/hand/genital bones) are the
  AUTHOR's template slop, identical in the original — FSMP skips them with warnings. Harmless.

**Fix applied:** the converter had stripped the `VirtualGround` per-triangle-shape from the
converted xml (its dangling-name cleanup — but VirtualGround is an FSMP magic name needing no mesh
shape). Restored verbatim from the author's xml; converted xml now differs from the original ONLY
by two dead typo-bone lines. Backup: `...Skirt.xml.bak-virtualground-20260821` beside it.
**Tool gap #3:** the converter strips VirtualGround from SMP xmls — re-apply after any re-run.
(Minted skirt ARMAs also carry raw-path first-person models — tool gap #1; irrelevant to SMP since
FSMP first-person physics is disabled, and covered by the queued audit chip.)

Test: wear the skirt, walk/run/sneak — cloth sways and collides with legs; sit/crouch — skirt no
longer passes through the floor.


## Round 4 (2026-08-21) — ROOT CAUSE FOUND AND FIXED: render-side bone bindings
User's decisive description: "the upper neck area of the shirt/torso moves with my head in a way
other outfits don't." That is a skinning defect, not geometry or texture.

**What Round 3 missed:** every skinning check read the legacy `NiSkinData` block (per-bone vertex
weight lists). On SE the renderer ignores that block — it skins from the bone indices + weights
PACKED INTO EACH VERTEX inside `NiSkinPartition`. The July 31 rebuild of this mesh wrote the legacy
block correctly (identical to the naked body) but botched the packed data for two regions.

**Evidence (packed skinning decoded for every vertex; naked body used as the oracle — its decoding
yields a clean, systematic pattern: neck ring Spine2=1.0 / Head=0 — that is the UBE NECK PIN from
`_tools/ube-neck-pin`, re-applied to the base body this morning, NOT engine design):**
- fix-mod crop-top body, BEFORE fix: 650 vertices (exactly the Head-region neck ring, idx 14303+)
  rendered bound 100% to `NPC R UpperArm [RUar]`; 169 groin verts to `NPC L Butt`/`NPC LT Anus2`;
  22 to `NPC Anus Deep2`. The other ~28,450 vertices were correct — hence "body looks fine, only
  the neck swings" (it rode the right arm / torso sway, at neck height).
- Packed bone indices in these files are GLOBAL skin-bone indices; the bone table gained 10
  genital bones in the July merge and the neck/groin entries were written against a stale table.

**Fix applied:** copied the naked body's packed per-vertex skinning (12 bytes/vertex: 4 half
weights + 4 bone indices) onto the crop-top body, both `_0` and `_1`, after proving identical bone
table (46, same order), identical vertex order (positions equal for `_1`; legacy weights equal by
index for `_0`, whose low-weight shape differs ≤0.67 units), identical partition maps. Re-verified:
render skinning now decodes IDENTICAL to the naked body at both weights; files parse clean
(67 blocks, partitions 32+53 intact). Backups beside the files:
`[Ashtoreth] Corsican Raider Top_0/_1.nif.bak-neckskin-20260821`.

**Neck-pin linkage:** the transplant carries the base body's current neck pin onto the crop-top body.
After ANY future base-body rebuild + re-pin, re-pin (or re-transplant) the crop-top body as well;
`measure_pin.py` gives the verdict. The memory notes every body-included UBE outfit installed after
2026-08-01 is still UNPINNED (Ninirim etc.) — a separate sweep.

**Kit verdict after fix:** `measure_pin.py` → crop-top `_1` PINNED with a profile identical to the
base body (62 ramp verts, max Head 0.163, mean 0.007); `_0` PINNED. CAUTION: the PRE-fix backup also
read PINNED (Head 0 everywhere) — the kit measures Head weight only and cannot see a ring bound to
the wrong bone. For rebuilt/converted bodies, the packed-index diff against the base body
(`partition_check2.py` pattern) is the stronger check; run both.

**Why the fabric never swung:** `SeaPirateTop1` packed skinning was self-consistent (0 mismatches).
Corset/Top2/Jacket: garment-only shapes, not rebuilt with a merged bone table (corset checked).

**Lesson (toolkit):** `housecarl_nif_inspect`, NiSkinData weight dumps, bind transforms, and
morph checks can ALL pass while the render skinning is wrong. For any hand-rebuilt or converted
skinned mesh, decode the packed partition skinning and diff it against a known-good twin.
Scripts: scratchpad `partition_check2.py` (decoder + naked-oracle) and `skin_transplant.py`
(gated vertex-for-vertex transplant) — worth promoting into `tools\nifcheck`.
