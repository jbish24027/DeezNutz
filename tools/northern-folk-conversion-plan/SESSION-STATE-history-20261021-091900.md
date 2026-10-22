# Handoff — 2026-10-19

## Fair logger INSTALLED — 20 October, user authorized “go”
Temporary mod `Authoria - Fair Barter Trace - TEMP` installed and enabled in PICTA, immediately after The Wanderer's Fair in effective file priority. MO2 and Skyrim verified closed before writes. houseCARL confirms its SkyrimFairStallCounter.pex wins. Papyrus logging and tracing both enabled. No plugin/loadorder changes or generator runs. Profile backup: `_backups/20261020-142742 - Fair barter trace/modlist.txt`. Next: user launches, tries any fair Browse counter once, waits a few seconds, quits; inspect newest Papyrus.0.log for AuthoriaFairTrade. This supersedes prior NOT installed notes. Remove/disable temporary logger after diagnosis.

## Current scope — user update
Second fair-only pass approved and completed: 59 NPC factions/template flags, 33 vendor factions and 33 populated persistent chests verified. No shared data defect proven. Temporary logging-only counter override compiled under `_staging/fair-barter-trace-trial/`; NOT installed. README describes one-counter runtime test. This is the next concrete step, not another broad audit. No installed files changed; no generator reruns. Stamina remains deferred.
User explicitly deferred the stamina issue. Do not request further stamina tests or investigate it unless they reopen it. Preserve findings; do not mark fixed. User tried multiple fair stalls and does not recall names; treat the failure as affecting several stalls, and do not keep asking for a stall name. Belethor barter works. Fair shops and instrumental music remain active pending work.

## Latest runtime results — 20 October
User confirms Belethor barter opens normally on the tested save. Focus shop investigation on fair actors/counters/vendor state, not a blanket barter-menu replacement. Screenshot shows player Stamina 120.00 and HUD 120/120, StaminaRate 0.84, StaminaRateMult 125.30. Positive configured values and full current stamina do not prove recovery after depletion; no depleted-to-recovered comparison supplied yet. Next minimal test: sprint to drain some stamina, stop out of combat, compare numeric stamina before/after ten seconds with console closed. Ask which fair stall fails; do not repeat completed static checks.

## Added plan item — starting-area lanterns, 20 October
Unresolved issue added to MASTER-PLAN.md and OTHER-ISSUES-PLAN.md from `_tools/start-room-lighting-investigation.md`. Actual room is Sev Cut CELL 000002, not replaced APStartCell. User reports failure with RaceMenu light on/off. Mesh self-glow missing; separate lights exist; red Lux placement/falloff changes are a lead, blue cause unproven. No implementation or repeated investigation. Existing priorities retained. Completion requires visible lantern glow and surrounding illumination in both RaceMenu-light states.

## User playtest — 2026-10-20
- Approved fair/stamina diagnostic pass completed: see FAIR-STAMINA-DIAGNOSIS.md. Music preference clarified: instrumental, no vocals. Stamina bar did not refill. 59 counter->keeper links valid, voice fix still wins (201/214); runtime shop cause unresolved. Current log shows script backlog but causality unproven. Optional built-in stage-music silence switch identified, not executed. Need ordinary-merchant comparison and live stamina values before targeted fix. No game changes installed.
- Arghus's robe SMP confirmed working. No robe repair needed for him.
- Stamina wheel confirmed gone. User says stamina was not regenerating the way they were used to seeing; do not assume this is only a hidden bar or actual regeneration failure. Clarify observed behavior before changing settings.
- Wanderer's Fair song described as "crazy" (exact audio problem not yet clarified).
- Both "Browse" and "What have you got for sale" reported not working at the fair. Treat both as confirmed user-reported failures; investigate vendor dialogue/barter routing and music separately. Earlier fair keeper/dialogue work is not passed in game.
- Save these observations without repeating the completed outfit audit. Substantial new diagnosis needs an estimate and user OK.

## Latest completed step
User approved the bounded audit after its estimate. Completed and saved `DISTRIBUTION-AUDIT.md`; read this report before repeating any queries. 126 NPCs / 49 outfits / 74 ARMO / 103 ARMA checked at SkyPatcher POST; 234 required VFS mesh paths present. Ysolda only explicit race/model failure, 125 static passes; runtime inventory still unverified. Found ten named overlapping recipients including Ysolda; report has preservation recommendations. Bell targets Hulda/Valga, but source author requires FSMP <=2.5.1 for skirt while local prior runtime is3.5.0. Cultural Bards 3BA documents body physics, not cloth SMP. No game mods changed. Audit approval did not authorize an unestimated large build. Older progress sections below are historical; do not redo completed export checks.

## Usage stop
User introduced estimate-before-large-work rules, now in root AGENTS.md. Paused deeper audit at natural break pending scoped estimate/OK. Usage snapshot: 20% weekly used, 17% five-hour used; this is NOT today's consumption. No daily cap supplied. Compaction reminder delivered at this break; do not repeat in this session.

## Latest clothing preferences (supersede earlier generic selection proposals)
- Preserve Northern Folk's detailed cultural distribution and existing varied NPC resources; do not replace everyone with one outfit pack.
- Add appropriate accessories/capes to NPCs lacking them, checking occupied slots and clipping, not stripping existing unique outfits.
- Favor Kreiste Publican for barkeepers/merchants and existing merchant outfits, with complementary accessories.
- Bell Wild West specifically for Hulda and the woman running the Falkreath inn; verify the latter's identity in this modlist before assignment.
- Cultural bards outfits for bards, with SMP required.
- Replace disliked Northern Folk male pointed-collar suit-jacket styles in Rift/Falkreath/Reach. Identify exact meshes before changing regional assignments.
- All 3BA refits/output winners must use SMP; retain OBody morphs. Applicable HIMBO/UBE/integration requirements remain.

## Nexus decision evidence
User URL https://www.nexusmods.com/skyrimspecialedition/mods/195244?tab=files is UBE YI GMS, a 57-NPC face overhaul, separate from Kreiste screenshot.
Read actual file descriptions via mcp__nexusmods__list_mod_files:
- Regular MAIN file 819700, 525.76 MiB, UBE 2.0/LRO Eidolon.
- ALTER MAIN file 822450, 820.99 MiB; description specifies uncompressed textures for Anwen, Carlotta, Danica, Delphine, Elenwen, Margret, Maven, Idgrod, Ingjard, Ingun, Rayya, Saadia, Sylgja, Temba, Tonilia, Uthgerd.
- ARCHIVED ALTER file 822371 additionally mentions DD2 hair, but current main description does NOT: do not claim current hair differences verified.
- Regular IFD Lydia optional 819693; ALTER IFD 822372. Matching JK Dibella / Nether Karliah / Nether Vex patches also exist; only apply for installed corresponding mods and selected affected appearances. Only ImprovedCompanionsBoogaloo.esp matched the installed plugin search for those names.
- Recommend regular as conservative default unless previews demonstrate preferred ALTER appearance. Do not replace all chosen faces indiscriminately; Muiri/Olfina confirmed good. New UBE selections require re-audit of clothing.
- Browser page adult-content gated in guest session; no preference changes/login performed. Connector supplied file metadata successfully.

## Audit progress and limits
Active profile confirmed DEEZ CS NUTZ - PICTA. Northern Folk INI explicitly targets 126 unique NPCs. All were read in one call with SkyPatcher POST overlay: `_staging/cnf-npc-audit.jsonl`. Only Ysolda has non-Skyrim race (05A184:UBE_AllRace.esp); all others vanilla Skyrim races. This is a race-risk screen, NOT proof nobody else is naked. SPID/save state and actual equipped inventory remain separate.
Bulk counts: 54 OTFT, 387 ARMO, 596 ARMA across CNFDistribution.esp and Clothes_of_the_Northern_Folk.esp. Exports `_staging/cnf-outfits.jsonl`, `cnf-armor.jsonl`, `cnf-addons.jsonl` are COMPLETE but SCOPED SOURCE VALUES, NOT winner/POST values. Use them as ID lists; reread needed records with formids and source overlay post (scan+to_file+overlay refused). Do not claim those source exports establish final compatibility.
Next approved audit: follow only assigned outfits -> items -> addons; check recipient sex/race support, model paths and VFS presence, slots, external links and competing distributors. Save report with accounting and explicit runtime limitations. Do not dump exports inline.
Installed/enabled: Publican base/CBBE/Normal Male Belly; Merchantress Main/SMP/3BA/HIMBO/CID distro. Bell/Cultural Bards not yet reliably located. Broad meta.ini search was noisy because descriptions cross-link unrelated mods; avoid repeating it.

## Actual changes
This turn only notes/AGENTS were written; no outfit mods/distribution installed. Earlier stamina wheel removal remains the only installed repair from the issue list. Master plan and detailed plans exist in this folder. Needs latest clothing preferences integrated after resume; this handoff is authoritative for those preferences.

## 2026-10-20 latest fair test (17:30)
- User completed counter test and reported Gore appearing at fair; shop visibility/usability not yet confirmed.
- Papyrus.0.log 17:30:33: counter 7B000D4C resolved live, loaded keeper 7B0013CF; ShowBarterMenu called/returned; BarterMenu open after 0.5s=True. Logging-only trial is not a confirmed repair.
- At 17:30:23 fair audio logged bringing 3 companions. Existing decompiled BringCompanions resolves CompanionFinder aliases and MoveTo(player) on entry/exit; log does not name Gore. Ask whether Gore was recruited/following before changing selection.
- TEMP Fair Barter Trace remains enabled pending outcome clarification. Stamina remains deferred.

## 2026-10-20 Gore at fair: fresh-save clarification
- User started a NEW save, left start room and went straight to fair; no companions recruited. Gore speaks as if in Coldharbour.
- Read-only houseCARL: SkyrimFairCompanions 070000:SkyrimFair.esp has six aliases, each (GetPlayerTeammate == 1 OR GetInFaction CurrentFollowerFaction == 1) AND WaitingForPlayer == 0 AND GetDead == 0. No quest-stage/location gate. Script teleports filled aliases on fair arrival/departure.
- Gore - Vigilant.esp defines HD1GoreCH1/CH2/CH3 (0316AE/0316AF/0316B0), all named Gore. POST SkyPatcher faction reads confirm each has CurrentFollowerFaction rank -1. This suggests quest-specific Gore may be selected; runtime identity and actual condition evaluation not yet verified. Do not claim a confirmed cause or remove Vigilant patch.
- Evidence exports: _staging/fair-companion-aliases-20261020.jsonl and fair-gore-factions-20261020.jsonl.
- Next minimal evidence: click the Gore who appears at fair in console and obtain reference ID/screenshot. No installed changes made in this check.

## 2026-10-20 screenshot confirms fair Gore identity
- User screenshot identifies EditorID HD1GoreCH1, base runtime 260316AE (0316AE:Gore - Vigilant.esp), placed reference 260316B1 (0316B1:Gore - Vigilant.esp).
- This is the Vigilant quest-specific Gore, appearing on a fresh save after going directly from start room to fair, with Coldharbour dialogue. Not normal recruited Gore.
- Fair companion selection remains leading transport cause (logged 3 companions); exact runtime predicate responsible not proven. Target companion eligibility fix, preserve Gore/Vigilant content. Check GetInFaction vs rank semantics and actual teammate state before selecting replacement condition. No installed edits this turn; screenshot shows game running.

## 2026-10-20 three Gore variants: selection conflict identified
- User reports THREE Gores, two older, and asks investigation without console work while game runs.
- houseCARL places CH1/CH2/CH3 at 0316B1/0316B2/0316B3:Gore - Vigilant.esp. CH1 confirmed directly by screenshot; other two fit reported count/appearance, not individually runtime-selected.
- Crucial: winning HD1GoreVigilant quest 00704E:Gore - Vigilant.esp Aliases[2,3,4] (GoreCH1/2/3) EACH adds CurrentFollowerFaction 05C84E:Skyrim.esm plus 084D1B. Thus base NPC rank -1 does NOT describe runtime quest-added faction membership. Fair's OR CurrentFollowerFaction branch can select all three without actual recruitment.
- Do not propose rank>=0 alone as a sufficient fix. Prepare fair-side actual-recruitment gate for these story variants, retaining legitimate follower travel and leaving Vigilant quest/factions intact. No installed changes while game runs. Existing aliases evidence in _staging/gore-vigilant-aliases-20261020.jsonl.

## 2026-10-20 installed Fair Companion Guard
- SkyrimSE and ModOrganizer confirmed closed; checked immediately before mods/profile writes.
- Enabled Authoria - Fair Companion Guard immediately above The Wanderer's Fair in reverse-priority PICTA modlist. No plugins/loadorder changes, no generators run.
- Compiled staged decompiled SkyrimFairAudioScript with added AuthoriaFairTravelAllowed: three Vigilant original refs 0316B1/B2/B3 require IsPlayerTeammate before BringCompanions moves them. Applies on entry and exit. Other actors unchanged. Original source equality checked after removing guard/helper additions.
- Compile successful after decompiling SkyrimFairPassport import. Only AudioScript PEX installed. houseCARL confirms Guard wins over original.
- Manual fresh-test-save recovery: cqf SkyrimFairAudioQuest AuthoriaRestoreGores. Returns the three original actors with MoveToMyEditorLocation only if alive and not player teammates. Never automatic; no stages/factions/inventory/enable edits. User must execute in game; not yet tested.
- Staging source/readme: _staging/fair-companion-fix. Backup: _backups/20261020-174810 - Fair companion guard. PEX SHA256 1A305E6DDE42572B472540E7D0F928FD4960719002476ADA60E580801B8B375D.
- Limitation: excluded Gores can still occupy companion finder alias slots. Targeted movement fix only; no six-slot finder redesign.
- Next: load pre-fair save OR use manual recovery on fresh Solitude test save; enter and exit fair, confirm no unrecruited Gore arrivals. No claim of runtime verification yet.
- Fair Barter Trace TEMP retained pending user report on shop usability. Stamina remains deferred.
