# Claude handoff — 21 October 2026

This is the current state. Historical notes contain superseded instructions; do not repeat completed audits or treat old “not installed” statements as current.

## Immediate next step: test the installed Gore correction

User started a NEW save, left the start room, and went straight to the fair without recruiting anyone. Three Gores appeared (two looked older), one spoke about Coldharbour; all three subsequently followed the player to Solitude after leaving the fair.

Screenshot confirmed HD1GoreCH1: base 0316AE:Gore - Vigilant.esp, reference 0316B1:Gore - Vigilant.esp (runtime 260316AE/260316B1). The other two correspond to CH2/CH3 by evidence and count, but were not individually console-confirmed.

Cause identified in records and script:
- SkyrimFairCompanions (070000:SkyrimFair.esp) accepts player teammates OR CurrentFollowerFaction members, alive and not waiting.
- HD1GoreVigilant (00704E:Gore - Vigilant.esp) starts with the game. Its CH1/CH2/CH3 aliases add CurrentFollowerFaction, despite base NPC rank -1. A rank-only fix would miss this runtime addition.
- BringCompanions moves selected actors on BOTH fair entrance and exit. Log recorded bringing three companions.

INSTALLED: Authoria - Fair Companion Guard, enabled in profile DEEZ CS NUTZ - PICTA immediately above The Wanderer's Fair in reverse-priority modlist.txt. Only Scripts/SkyrimFairAudioScript.pex is overridden. Source mod intact; no plugin order changes.
- AuthoriaFairTravelAllowed requires IsPlayerTeammate for references 0316B1/B2/B3:Gore - Vigilant.esp. Gore's recruitment controller explicitly sets teammate state. Other actors retain existing behavior.
- Compilation passed; original source comparison confirmed only guard/helper additions. houseCARL confirmed override wins. Enabled entry and installed hash rechecked 21 October.
- SHA256: 1A305E6DDE42572B472540E7D0F928FD4960719002476ADA60E580801B8B375D
- Source and README: C:\1. AUTHORIA\_staging\fair-companion-fix\
- Backup: C:\1. AUTHORIA\_backups\20261020-174810 - Fair companion guard\ (profile and original PEX).
- Limitation: excluded Gores may still occupy the six companion-finder slots. This is a targeted travel fix, not a redesigned finder.

User was given this recovery command FOR THEIR FRESH TEST SAVE:
    cqf SkyrimFairAudioQuest AuthoriaRestoreGores
It manually returns the three original references to editor locations, skipping missing, dead, or recruited actors. It does NOT run automatically and does not change stages, factions, inventory, or enabled state. Save separately first; pre-fair save is preferable when available. Do not generalize this recovery to progressed Vigilant saves.

NOT YET VERIFIED IN GAME: recovery command and prevention on entry/exit. User has not reported running the command or testing the installed correction. Next ask for outcome, not more discovery. No Synthesis or Reqtificator needed.

## Fair shops and music remain unresolved

User tried several stalls; both Browse and spoken sale options failed. They do not remember stall names. Belethor barter works. Do not keep requesting stall names or repeat the completed static audit.

TEMP logger remains enabled: Authoria - Fair Barter Trace - TEMP, overriding SkyrimFairStallCounter.pex. It changes logging only. Backup: _backups/20261020-142742 - Fair barter trace/modlist.txt. Remove/disable after diagnosis with closed-process check; do not restore an old whole modlist over newer changes.

20 October 17:30:33 trace: counter 7B000D4C resolved keeper 7B0013CF, alive and loaded; ShowBarterMenu called and returned; BarterMenu open after 0.5 seconds = TRUE. User has NOT confirmed visible stock or successful trading. Ask whether menu was usable, blank, or flashed closed. This trace is not proof of a repaired shop. Saved excerpt: _staging/fair-trace-result-20261020.txt.

Completed checks: 59 counter/keeper links valid; 59 NPC vendor factions/template flags checked; 33 vendor factions and persistent stocked chests valid. Earlier generic-voice list fix still wins (female 201 / male 214). Script backlog observed, not proven cause. Details: FAIR-STAMINA-DIAGNOSIS.md and _staging/fair-*.jsonl.

Music preference: instrumental, no sung words; user dislikes the song, not reported audio corruption. No replacement installed. Optional existing console switch: set SkyrimFairAudioMusicEnabled to 0 (restore 1). No evidence user used it. SongLengths2 and stage choreography depend on timing; do not blindly replace with a differently sized audio file. Fiddle is only a candidate, not verified instrumental.

## Other work — preserve status

- Stamina wheel removal confirmed working. Stamina regeneration issue explicitly DEFERRED by user. Do not investigate or request tests unless reopened.
- Arghus robe SMP confirmed working. No repair needed.
- Northern Folk audit DONE: 126 NPCs, 49 assigned outfits, 74 ARMO, 103 ARMA, 234 required mesh paths present. Ysolda only explicit race/model compatibility failure; static passes do not prove runtime clothing. Read DISTRIBUTION-AUDIT.md before any queries.
- Ysolda UBE race lacks compatible CNF addon; competing Helga distribution also exists. Proposed existing Helga UBE fix not installed.
- Fralia/CNF: 3BA conversion with OBody morphs and loose Helga-like cloth movement requested. ALL 3BA output winners must use SMP variants. Applicable HIMBO/UBE integrations required.
- Eldawyn female monk robe lacks SMP rig/link; repair pending. Do not conflate with working male Arghus robe.
- Preserve Kreiste Publican/merchant and unique NPC outfits; enrich accessories/capes instead of replacing everything with CNF. Cultural Bards requested with actual cloth SMP.
- Bell Wild West requested for Hulda and Valga Vinicia. Local FSMP 3.5.0 versus Bell 3BA v1.1 author's <=2.5.1 requirement needs a targeted trial/repair, not global downgrade. UBE conversion exists. Not installed by this work.
- Replace disliked pointed-collar male CNF jackets in Rift/Falkreath/Reach only after exact visual identification.
- Muiri/Olfina faces good: preserve. Olfrid hair/beard mismatch, distant gray SKIN, Lydia pre-thanedom voice remain pending.
- Starting-room lanterns: _tools/start-room-lighting-investigation.md. Sev Cut CELL 000002, not APStartCell. Red/blue illumination issue unresolved; no fix installed.
- Nexus 195244 is UBE YI GMS face overhaul, not Kreiste clothing. Regular main recommended provisionally; no blanket replacement or install performed. Detailed historical evidence retained.

Master scope: MASTER-PLAN.md; outfit conversion: PLAN.md; other issues: OTHER-ISSUES-PLAN.md. These plans may contain older status wording: this handoff takes precedence. Historical state retained alongside this file for deeper evidence.

## Rules and working preferences

Read root AGENTS.md. Actual profile used by this work is DEEZ CS NUTZ - PICTA; generic workspace text naming DEEEZ NUTTZZZ is stale for these changes. Instance C:\1. AUTHORIA.

Never run Synthesis, Reqtificator, or LOOT. Verify Skyrim and MO2 closed immediately before writes to mods/, profiles/, or ModOrganizer.ini. Fixed plugin order; edit plugins/loadorder in lockstep only if needed; Authoria Outputs stays terminal. Preserve original Dint masters and generated-output separation.

Estimate substantial new work and WAIT for approval; approved scope need not be re-approved. No numeric daily cap set. Short updates, normal model for routine work, scripts for computation, no repeated broad audits. No agent delegation unless expressly authorized. Current repair is script-only: no added content requiring voice/body/Requiem/Seasons integration.

This handoff update changed documentation only. Do not claim any runtime test passed without the user's report or logs.
## Update 21 Oct (Claude, afternoon)
- User ran PGPatcher, then Reqtificator, then Synthesis on 21 Oct. PGPatcher displaced RftI/PG_1/PG_2/DynDOLOD/Occlusion to the bottom and dropped 6 plugingroups lines; both restored (backups 20261021-112926 and the plugingroups restore). After every generator run: check loadorder tail AND plugingroups.
- Muiri and Ysolda faces CONFIRMED GOOD by the user. Do not re-ask.
- New user requests pending: pick faces from UBE YI GMS (57 NPCs; 22 already have chosen faces, 35 come from the NPC merge); Lisette (Markarth bard, Breton) new Cultural Bards outfit; review friend's GitHub (needs user sign-in to fetch).
- 21 Oct (user away): removed the 10 protected NPCs (Ysolda, Kerah, Orgnar, Thoring, Dagur, Camilla, Muiri, Nenya, Aslfur, Jorleif) from mods/CNF - Immersive Distribution/.../zzzClothesOfTheNorthernFolk.ini (backup _backups/<stamp> - CNF protected outfits). SkyPatcher post-state verified: Camilla Haberdashery, Muiri LDD white, Nenya steward; Ysolda/Kerah/Orgnar fall to their SPID outfits at runtime.
- Bottled 1.0.18 still contains the Data\enbseries refusal -> still breaks Picta.
- Choices handed to the user in Desktop "WHILE YOU WERE AWAY.txt": Lisette Cultural Bards outfit (+ user must download the 3BA conversion 133265), GMS face picks (35 candidates), friend's GitHub sign-in, new-download picks.

## Update 22 Oct (Claude, evening) - PROTOTYPE BUILT (Fralia, CNFVikingHardangerBlack)
- Mod `Authoria - Northern Folk Prototype - Hardanger Black` (README inside) + `Authoria - CNF Prototype - UBE.esp` (ESL).
  Dress + knitted boots: 3BA women (with .tri morphs), UBE women (with .tri), HIMBO men (with .tri); headscarf UBE races.
  Cloth physics on the women's dress (3BA + UBE) via robe-smp recipe. Men's tunic: no SMP yet.
- Done WITHOUT BodySlide or the UBE converter (both are the user's tools): own conform pipeline in `_tools\cnf-convert`
  (BodySlide's Vanilla To CBBE / HIMBO VAL references, 3BA + HIMBO + UBE slider data written as .tri, DayOnly's
  3BA->UBE move learned from 965 existing 3BA/UBE pairs). No BodySlide projects (.osp) were written yet.
- Checks: renders (scratchpad r2/r3/r4/r5.png), deep clipping flat under big sliders, plugin 0 errors, SkyPatcher
  post-state attaches all 3 UBE addons, all meshes parse and win in PICTA.
- OWED: in-game check on Fralia (walk/run/sit/stairs, OBody presets), feel of the skirt; then decide the batch.
- NOTE: the 6 UBE women are still OUT of the CNF distribution (removed 22 Oct); only this outfit has UBE versions.
