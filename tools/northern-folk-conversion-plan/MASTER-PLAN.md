# Authoria — consolidated repair and completion plan

Updated 19 October 2026. **This is a plan, not a claim that the fixes are installed.** It consolidates the reported in-game problems, requested outfit work and unfinished items from the reviewed Claude chats.

## Current baseline

**20 October status update:** Arghus's SMP and stamina-wheel removal are confirmed working. Stamina refill and both fair shopping options remain unresolved; see [FAIR-STAMINA-DIAGNOSIS.md](FAIR-STAMINA-DIAGNOSIS.md). These observations supersede the older test requests below.

**Latest clothing decisions and completed static audit:** see [DISTRIBUTION-AUDIT.md](DISTRIBUTION-AUDIT.md). It supersedes the earlier generic Hulda selection proposal: Bell Wild West is requested for Hulda and Valga Vinicia, pending current-FSMP compatibility. Protect existing Kreiste/professional/unique outfits, retain Northern Folk variety, add compatible accessories, provide Cultural Bards cloth SMP, and replace only the identified pointed-collar male looks in the specified holds.

- You have run BodySlide, NPC Plugin Chooser 2, Reqtificator and Synthesis. Do not repeat them without a specific reason.
- **Muiri and Olfina's faces are good.** Preserve their current selections.
- The stamina wheel, its reskin and the override hiding the normal stamina bar have already been disabled in **DEEZ CS NUTZ - PICTA**. The wheel DLL is absent from the active virtual filesystem; the game still needs a visual check.
- **Arghus is untested, not confirmed broken.** You did not see him moving.
- Other repairs below are not yet installed. Earlier checks identified causes or leads, not completed fixes.
- Reconfirm the active profile before implementation: the inspected profile was PICTA, whereas the workspace reference names DEEEZ NUTTZZZ.

## Non-negotiable outfit standard

**Every 3BA refit must use the SMP version in our outputs.** Select the SMP BodySlide project, preserve its physics during rebuilding, and verify that its built mesh is the final MO2 winner. A static alternative must not overwrite it. If no SMP version exists, author and validate the missing physics before calling the requested refit complete.

- Use the installed 3BA reference, zeroed base shapes and **Build Morphs** for OBody. Preserve matching weight meshes, TRI morphs and physics links.
- Hanging skirts and robes should have **freer movement like Helga**, with a stable waist and controlled settling. Body physics alone does not satisfy the cloth requirement.
- Keep 3BA, UBE and HIMBO projects and outputs clearly identified. UBE NPCs need their own compatible meshes and race support; a 3BA build cannot substitute for that.
- Preserve original clothing colours, coverage and texture variants. New rigs or shape splits must not break alternate textures.

## Prioritized repairs

| Priority | Issue | Planned work | Completion check |
|---|---|---|---|
| 1 | **Ysolda naked** | Confirm her actually equipped outfit and reconcile the competing Northern Folk and Helga distribution rules. Prepare a reversible interim Helga repair using the already installed UBE addons and meshes. Complete Northern Folk UBE coverage before switching her back to it. | Clothed after reload; matching body seams; working cloth physics; one effective outfit assignment. |
| 1 | **Stamina wheel removal** | Confirm the installed removal in PICTA. Investigate saved HUD settings only if the normal stamina bar remains hidden. | No wheel; normal stamina display works when stamina changes. |
| 2 | **Fralia / Northern Folk clothing** | Start with Fralia's complete Black Hardanger outfit. Make a 3BA/OBody/SMP prototype, validate Helga-style movement, then expand by distinct geometry family. Include applicable HIMBO and UBE coverage. | Fralia's skirt moves freely; clothing follows OBody changes; colours and seams remain correct. |
| 2 | **Eldawyn has no robe movement** | Her winning female monk robe has no SMP rig. Create the missing 3BA/OBody/SMP version, with suitable collision and preserved robe variants. | Visible movement while walking, turning and sitting, without instability or persistent clipping. |
| 2 | **Arghus robe** | Observe him moving before changing anything. His winning male monk robe already has a rig and XML. If it fails, investigate that specific mesh/configuration and simulation state. | Motion verified in game; only make a repair if a failure is reproduced. |
| 2 | **Robes appear black** | Check actual worn items and intended colours. Audit alternate-texture mappings where builders split robe shapes. Record names saying green/gray do not override what you saw. | Intended colours survive the final mesh and texture winners. |
| 3 | **Hulda barkeeper outfit** | Preview an existing practical dress/apron option with suitable body and physics support. Resolve any materially different style choice with you, then assign the complete outfit to Hulda alone. | Suitable appearance, complete clothing, working movement and unchanged inn services. |
| 3 | **Olfrid hair/beard mismatch** | Inspect textures and tint/shader differences; make a narrow authored-asset correction, normally matching his beard to his current hair. | Consistent colour indoors and in daylight; chosen face preserved. |
| 4 | **Gray skin at distance** | Compare the same NPC near/far in fixed lighting. Check skin texture mipmaps, face/body differences and relevant renderer settings. Test one supported hypothesis at a time. | Skin colour remains appropriate at distance without spoiling the close-up appearance. |
| 4 | **Lydia's pre-thanedom voice** | Trace a specific spoken line to its dialogue record and winning audio. Her configured voice type is already IFD's unique Lydia voice; inspect coverage/conflicts before changing quest conditions. | The affected line uses the intended voice and recruitment/thane progression still works. |

Additional unresolved visual issue, queued alongside the existing priority-4 diagnostics: **starting-area red/blue lantern glow and illumination** in Through the Woods, `000002:AlternatePerspective - Sev Cut.esp` (`SEVAPstartcell`), PICTA. Occurs with RaceMenu light **on and off**. Both winning meshes have zero emissive colour and no self-illumination flags; separate lights exist and are not disabled. The Lux Orbis patch moves the red light, removes its FadeOffset and substitutes steeper falloff. These findings do not establish the full in-game cause, especially for blue illumination. The replaced original APStartCell's conflict is not the cause established by this investigation. **Fix unimplemented; no installed files changed.** Acceptance: both lanterns visibly glow and illuminate nearby surroundings appropriately with RaceMenu light off and on. See [saved investigation](../start-room-lighting-investigation.md) and [detailed issue tracking](OTHER-ISSUES-PLAN.md#8-starting-area-lantern-lighting--unresolved); do not repeat the investigation or treat proposed steps as authorization to execute.

## Northern Folk conversion milestones

1. **Inventory:** map worn meshes, outfit records, race support, texture variants and distributors. Group genuinely identical geometry rather than counting every recolour as a new outfit.
2. **Fralia prototype:** fit the installed 3BA neutral body, preserve loose coverage, finalize topology and correct slider extremes. Save complete editable BodySlide sources.
3. **Cloth physics:** author the skirt rig and collision shapes, using the winning Helga dress as the movement reference. Ensure BodySlide rebuilds retain the rig and OBody morphs.
4. **Prototype approval in game:** test walking, turns, running, sitting, stairs and stopping; test several actual OBody shapes and actor weights. Confirm that the movement feels right before expanding.
5. **Pack coverage:** complete remaining distinct female families and matching accessories, applicable HIMBO male projects and separate UBE support, including Ysolda.
6. **Integration and delivery:** validate Requiem compatibility, applicable Seasons behaviour, source projects, reproducible build instructions and clearly separated outputs. Verify final MO2 winners after building.

Detailed implementation reference: [Northern Folk conversion plan](PLAN.md). Use the [official BodySlide and Outfit Studio project](https://github.com/ousnius/BodySlide-and-Outfit-Studio) and its project/conversion documentation; verify features against the installed tool version before relying on newer automation.

## Finish the earlier Claude work

These remain in scope, but come after the immediate clothing repairs unless an in-game test reveals a serious problem.

| Workstream | Remaining work |
|---|---|
| **Remiel hair / Researcher outfit** | Check the recolour and newly built outfit in game, including OBody and SMP where applicable. Audit and complete the outstanding Requiem integration for the 22 added Dwemer Research Squad items and required applicable body coverage. |
| **Vanilla outfit SMP** | Test the installed men's coat/robe families in motion, including texture variants and crowded scenes. Track uncovered female families separately; Eldawyn is a confirmed coverage gap. |
| **Olfina / THE PLAN** | Preserve the working Olfina and Muiri faces. Verify the clothing changes and Whiterun grass in game; wheel reskin work is superseded by removal. |
| **Dungeon fires** | Check the restored fire visuals and affected locations in game. Since you have already run Reqtificator, verify the relevant output reflects the intended inputs before requesting another run. |
| **Fair / grass** | Check fair NPC dialogue and keeper availability under the intended start conditions, and assess the installed stage/performance and grass changes in game. Avoid restarting the playthrough solely for an exploratory test; use a separate test save if required. |
| **DBReV laughs** | Listen to the 51 installed Eleonora laugh takes in context; identify only the lines needing replacement, volume adjustment or timing work. |
| **Companion banter** | Reconcile the actual draft inventory (8,241 talks plus 170 separate ask-party lines) with the manifest. Complete the identified 340 missing talks, address QA flags, then review triggers and repetition before dialogue implementation and voice production. These are drafts, not installed gameplay dialogue. |

## Practical division of work

**I can prepare:** record and asset audits, targeted compatibility fixes, conversion sources and builds, physics validation, output-winner checks, outfit previews, dialogue/audio tracing and a documented install batch.

**Your in-game checks:**

1. Confirm wheel removal and the normal stamina bar.
2. Observe Arghus walking and turning, rather than standing still.
3. Note one exact Lydia line heard before thanedom and where it occurred.
4. Capture the same affected NPC's skin close up and at a distance in unchanged lighting; note whether it affects face, exposed body, or both.
5. After the repair batch, check Ysolda, Fralia, Eldawyn, Hulda and Olfrid, then approve the prototype's cloth movement before the full conversion proceeds.

Do not rerun every generator between individual checks. I will identify which tools, if any, the final changes actually require. **You run Reqtificator and Synthesis manually.**

## Installation and acceptance rules

- Before every write to mods, profiles or ModOrganizer.ini, verify MO2 and Skyrim are closed. Back up touched files and record rollback steps.
- Preserve the fixed mod/plugin order, edit plugins.txt and loadorder.txt together when necessary, and leave nothing below the terminal Authoria - Outputs block. Never run LOOT.
- Fix authored inputs; do not copy generated output into hand-authored patches. Keep original Dint hair base/master mods enabled.
- For additions, include applicable Requiem, HIMBO, UBE and Seasons integration. Assess Eleonora DBReV coverage whenever dialogue is introduced; mesh-only work has no new spoken lines. Document any inapplicable or blocked integration explicitly.
- Keep installed assets, authored sources and recovery materials. Clean only clearly obsolete project scratch files; ask about uncertain files.
- Record each issue as **planned → prepared → installed → passed in game**. Offline validation alone does not prove the visual or physics result.

**Recommended first batch:** Ysolda's clothing repair, Hulda's outfit proposal and Olfrid's colour diagnosis, alongside the Fralia/Eldawyn SMP prototypes. Collect the Arghus, Lydia and gray-skin observations while those are prepared.

Detailed diagnostic reference: [Other issues plan](OTHER-ISSUES-PLAN.md). This consolidated plan takes precedence if an older note differs, especially on mandatory SMP output selection and Arghus's untested status.
