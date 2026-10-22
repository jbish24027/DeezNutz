# Authoria: remaining reported issues

2026-10-19. Planning only. Based on the user's in-game observations and the read-only checks already performed. Active profile verified as DEEZ CS NUTZ - PICTA. Northern Folk 3BA/OBody/loose-SMP conversion is covered separately in PLAN.md.

## Status boundaries

- Completed on disk: disabled Wheel Of Stamina SKSE, its Dragonborn Reskin, and Authoria - TrueHUD Stamina Bar Off (Wheel of Stamina), in PICTA only. Backed up modlist.txt to `_backups/2026-10-19 - stamina wheel removal/`. houseCARL confirms StaminaRing.dll absent from the active virtual filesystem. The winning TrueHUD settings have uPlayerWidgetStaminaMode=4. In-game confirmation remains.
- User confirmed Muiri and Olfina faces good. Preserve these selections and face assets.
- No other fix below has been installed. Diagnoses marked provisional require the stated check before a change.

## 1. Ysolda naked — first priority

Evidence: Ysolda is on UBE race 05A184:UBE_AllRace.esp. SkyPatcher changes her outfit to CNFBunadNordlandBlue (000818:CNFDistribution.esp). The Northern Folk dress has no UBE addon. A separate SPID rule also assigns Xtudo_YsoldaOutfit, so two distribution mechanisms need reconciling. The Ysolda-specific Helga dress currently has only its original non-UBE addon. Existing Helga UBE addons and built dress/boots/gloves/choker meshes are available; their race lists include her UBE race.

Plan:
1. Confirm the actual worn outfit from SPID logs or in-game inventory before claiming which of the two rules wins in the save.
2. Prepare a small reversible compatibility fix that restores her previous Helga outfit as the immediate clothing solution: explicitly resolve the competing Northern Folk assignment and link the existing UBE Helga addons to all four Ysolda-specific clothing items. Preserve the items' authored stats and her appearance.
3. Validate the UBE mesh and texture paths, slots, race support, low/high weight pair and physics XML. Check matching body shape at seams.
4. Explain any needed outfit refresh for the current save only after the mechanism is verified; do not prescribe resetinventory blindly.
5. Later, once the separate Northern Folk UBE conversion passes, her intended Northern Folk outfit can be enabled without leaving her undressed. The interim fix is not a substitute for completing that conversion.

Pass: Ysolda is clothed after launch and reload, hands/feet/neck match, no invisible torso, and no outfit tug-of-war between distributors. Face remains the selected UBE appearance.

## 2. Eldawyn missing robe physics; Arghus awaiting movement test

User correction: Arghus was not observed moving. His physics is UNTESTED, not reported broken. Do not change his rig or global FSMP settings on that basis.

Evidence: both NPC outfit records point to monk-robe variants (Eldawyn: Hooded Green Robes; Arghus: Grey Robes), despite their reported black appearance. That record naming does not invalidate what the user saw. Eldawyn's female monk mesh is supplied by CBBE 3BA Vanilla Outfits Redone - Prebuilt and has no HDT link or moving bones. Arghus's male monk mesh is supplied by Authoria - SMP Vanilla Coats and contains a rig and a resolvable XML. The earlier black/necromancer robe work does not cover Eldawyn's female monk mesh.

Plan:
1. Check actual equipped items and runtime outfit overrides; keep their currently intended garments.
2. Eldawyn: make a 3BA/OBody-compatible monk-robe project with loose Helga-style skirt movement, stable torso/sleeves, morphing collisions and weight-pair parity. Include applicable UBE coverage in the family work; preserve HIMBO male coverage.
3. Arghus: first observe him walking/turning at close range. Only if his robe fails to move should we validate weighted bones against XML declarations and constraints, inspect targeted logs and investigate simulation budgeting. No change is currently justified.
4. Audit alternate-texture mappings. The existing men's builder split the original robe into additional shapes; shader/shape-name/index changes may explain lost colour variants. Compare against authored sources and correct mappings only if verified.
5. If simulation works but motion is too restrained, measure and tune the existing rig toward the user's freer Helga reference. Do not replace a valid rig before distinguishing stiffness from a load/configuration failure.

Pass: robes move visibly in walk/run/turn/sit/stop tests, preserve intended colour and silhouette, settle without jitter and remain correct across OBody presets. Re-check in a group to assess FSMP budget effects.

## 3. Hulda — proper barkeeper outfit

Evidence: her winning NPC record has FarmClothesOutfit02. The existing ClothesTavernWenchOutfit (0F966E:Skyrim.esm) contains vanilla tavern clothes and shoes; this is an available candidate, not an approved visual selection.

Plan:
1. Inspect the installed tavern/barkeeper outfit replacements and their current female mesh winners. Prefer an existing practical dress/apron with proper 3BA/OBody coverage and suitable cloth movement.
2. Prepare one concrete recommendation with a preview and identify whether it is a modest apron-style barkeeper outfit or the more revealing tavern dress. Ask for the user's preference if the existing choices materially differ; do not silently choose revealing clothing.
3. Assign the chosen outfit to Hulda alone with one explicit runtime rule, after checking other distributors. Leave her face, merchant behaviour, inventory and quests unchanged.
4. If a new outfit is necessary, include Requiem, applicable HIMBO/UBE, Seasons and Eleonora applicability assessment before calling the addition complete. Prefer existing content to avoid unnecessary additions.

Pass: Hulda wears the chosen complete outfit after reload, moves without obvious clipping, and still offers inn/merchant dialogue.

## 4. Olfrid Battle-Born — hair/beard colour mismatch

Evidence: face mesh and face tint both resolve to True Sons of Skyrim Refined. Hair shapes use HairTint shaders; two beard shapes use Default shaders, so they are not necessarily driven by the same tint. This is a lead, not proof of the final visual cause.

Plan:
1. Read his authored hair colour, all hair/beard texture paths, baked tint values and vertex colours. Inspect the texture images and compare them with the reported appearance.
2. Preserve his existing hair colour and bring the beard into agreement unless the user prefers another colour. Adjust only the verified source of mismatch: texture, baked tint or shader setup.
3. Make a backed-up, narrow override from the authored face asset. Preserve geometry, bone structure, partitions and unrelated face features. Do not copy NPC Chooser output into a hand-authored patch.
4. Verify the override wins and test in neutral daylight and indoors before declaring a match.

Pass: beard and hair read as the same intended colour family without changing his chosen face or creating a face/body seam.

## 5. Gray skin at distance — isolate before changing visuals

User clarified that the affected part is skin. It is not yet established whether normal colour returns close up, which NPCs are affected, or whether it occurs indoors too. Advanced Skin and subsurface-scattering settings are present, but no setting has been established as the cause.

Plan:
1. Obtain matched near/far screenshots of the same NPC under the same lighting, and names of two affected NPCs if possible. Compare exposed body skin and face separately.
2. Trace their winning skin textures, face assets and shader settings; check texture mip levels for colour loss. Distinguish a texture/face mismatch from a distance-dependent lighting or rendering effect.
3. Check the relevant renderer configuration and current logs. Prepare a reversible, one-setting-at-a-time comparison only after identifying a plausible mechanism. Do not change the overall weather, colour grading or skin setup speculatively.
4. Compare at the same location/time/camera distance and restore unsuccessful trials.

Pass: skin retains appropriate colour at normal viewing distances while the preferred close-up appearance and performance are preserved.

## 6. Lydia pre-thanedom voice — trace the exact line

Evidence: after SkyPatcher, Lydia's voice type resolves to FemaleUniqueLydia (005901:ImprovedCompanionsBoogaloo.esp), the installed IFD Lydia voice. That proves the configured voice assignment, not which dialogue line or sound was heard before thanedom.

Plan:
1. Identify an exact line spoken before thanedom and the quest stage/context. Check whether it comes from IFD Lydia, Alternate Perspective, vanilla dialogue, another dialogue mod or a scene.
2. Inspect the winning INFO/topic/quest conditions, speaker/alias selection and voice asset winner for that line. Check IFD's intended pre-thanedom coverage and any shipped original-voice audio.
3. Fix a verified conflicting dialogue condition or wrong audio provider narrowly. If IFD simply supplies no replacement for that line, report that limitation and prepare a specific coverage proposal rather than globally forcing dialogue to run early.
4. Preserve recruitment/thane gates and scripted scenes. Lydia's NPC voice and Luna's Eleonora player voice are separate systems. Include Eleonora DBReV coverage only if new player dialogue is introduced.

Pass: the tested pre-thanedom line uses the intended voice, while becoming thane and recruiting Lydia still follow the intended quest sequence.

## 7. Stamina wheel removal — confirm in game

No further removal work is currently needed on disk for PICTA. Launch and verify that the wheel is absent and the usual TrueHUD stamina bar appears when stamina changes. Check saved MCM behaviour only if the bar remains hidden. Original files stay available for rollback; other profiles were not changed.

## 8. Starting-area lantern lighting — unresolved

Added 20 October 2026. User confirms this concerns the area itself and occurs with RaceMenu light **both on and off**.

- Actual area: Through the Woods / `AlternatePerspective - Sev Cut.esp`, CELL `000002` (`SEVAPstartcell`), active profile PICTA.
- Both winning red/blue lantern meshes have zero emissive colour and no self-illumination flags. Separate placed lights exist and are not disabled.
- Lux Orbis moves the red light away from its lantern, removes its FadeOffset and changes its base to a light with steeper falloff.
- These are verified data findings, **not a proven complete cause**. Missing blue illumination remains unexplained in game. Do not attribute this to the Lux conflict in the replaced original APStartCell.
- **No fix implemented and no installed files changed.** Carry forward the existing investigation rather than repeating it. Any proposed patch trial remains future work, subject to the user's scope/estimate rules.

Pass: both lanterns visibly glow appropriately and light nearby surroundings, with RaceMenu light off and on.

Evidence: [starting-area investigation](../start-room-lighting-investigation.md). Keep existing priorities intact; queue this with the other visual diagnostics.

## Existing work order (unchanged)

1. Ysolda clothing repair and stamina-bar confirmation.
2. Hulda outfit selection/assignment and Olfrid colour fix.
3. Eldawyn missing physics and Arghus movement test, coordinated with the separate Northern Folk prototype.
4. Lydia exact-line investigation and controlled gray-skin comparison as the needed observations arrive.
5. One documented install batch where practical, then a short Whiterun/inn test route plus Arghus at his location. Retest Muiri/Olfina only if a shared dependency changes.

Every installed write requires an immediate MO2/game process check and backups. Preserve original mods, authored sources and recovery files. Never sort with LOOT or put plugins below Authoria's terminal Outputs block. Any necessary plugin edits stay in lockstep in plugins.txt and loadorder.txt. Fix authored inputs rather than generated outputs. The user alone runs Synthesis and Reqtificator; request reruns only when the actual changes require them, grouped after relevant record work.
