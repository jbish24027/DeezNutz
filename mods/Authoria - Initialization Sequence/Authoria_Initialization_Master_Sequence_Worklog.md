# Authoria Initialization Master Sequence Worklog

## Goal
Create a clean, reversible initialization sequence for new games. The master sequence starts after RaceMenu closes, keeps the player locked in place, runs Requiem initialization silently, then runs Starting Choices, Biggie Traits, SkySigns, difficulty selection, MCM Recorder, and final unlock in order.

## Current Implementation Rules
- Do not remove or disable plugins automatically. Legacy autopop plugins may remain enabled for reference.
- Use `Authoria - Initialization - Master Sequence.esp` for new records and quest/script overrides.
- Prefix new scripts and records with `_Authoria`.
- Prefer ESP/Papyrus coordination for the current sequence; no SKSE DLL exists in this working mod yet. The `no SKSE DLL` rule is superseded only for the future PRISMA UI prompt bridge, because clickable PRISMA UI requires native SKSE integration. No RaceMenu edits, no hooks.
- Keep all runtime changes inside `D:\Wabbajack\Authoria-dev\mods\Authoria - Initialization Sequence`.

## Known Legacy Starters
- `McmRecorder.esp` / `McmRecorder.psc`: listens for `RaceSex Menu` close and autoruns recordings marked `autorun`.
- `Requiem.esp` / `REQ_Installation.psc`: waits for inventory or magic menu close, then calls Requiem setup.
- `Starting Choices.esp` and `AP & SC Patch.esp`: compatibility quest can auto-start `SC_Main`.
- `Traits Autopop.esp`: start-game quest listens for `RaceSex Menu` close and casts `Traits_SelectionSpell`.
- `Sky Signs Autopop.esp`: start-game quest listens for `RaceSex Menu` close and casts `SkySigns_Ab`.

## Planned Sequence
1. RaceMenu closes (`RaceSex Menu`).
2. Master quest locks player controls.
3. Requiem initializes silently.
4. Placeholder welcome message appears.
5. Starting Choices runs; master waits for completion.
6. Biggie Traits runs through `Traits_SelectionSpell`; master waits for completion.
7. SkySigns runs through `SkySigns_Ab`; master waits for completion.
8. Difficulty message appears: Easy / Normal / Hard.
9. MCM Recorder plays `Authoria_Easy`, `Authoria_Base`, or `Authoria_Hard`.
10. Placeholder finish message appears and controls are restored.

## Implementation Notes
- This file was created before implementation changes, per request.
- Added and compiled `_Authoria_Init_MasterSequence.psc`.
- Added compiled overrides for Requiem install scripts so new-game install is driven by `_Authoria_Init_RunRequiemInstall`, not inventory/magic menu close, and the new-game install/start/done prompts are suppressed.
- Added compiled completion events to `SC_MainSCRIPT`, `Traits_QuestScript`, and `SkySigns_Script`.
- Added a compiled inert `SC_CompatibilitySCRIPT` override as a fallback guard against the old Starting Choices compatibility quest auto-starting outside the master sequence.
- Added compiled inert overrides for `Traits_AutopopScript` and `SkySigns_AutopopScript` so the legacy starter quests do not fire their old RaceMenu behavior while kept for reference.
- Set `McmRecorder/Authoria_Base.json` autorun to `False`; difficulty playback is now selected by the master sequence.
- Created `Authoria - Initialization - Master Sequence.esp` with:
  - `_Authoria_Init_Running` global.
  - Welcome, difficulty, and finish message boxes.
  - `_Authoria_Init_MasterSequenceQuest` as a start-game, run-once quest.
  - An `SC_Main` override wiring `_Authoria_Init_Running` into `SC_MainSCRIPT`.
  - Quest-flag overrides that clear Start Game Enabled / Run Once from `SC_Compatibility`, `Traits_AutopopQuest`, and `SkySigns_AutopopQuest`.

## Current Load Order Note
- The new ESP was written to disk, but MO2 did not see it through VFS immediately after external creation. Refresh MO2, enable `Authoria - Initialization - Master Sequence.esp`, and place it after the AP Starting Choices patch and the two legacy autopop plugins.

## 2026-05-21 V2 Fixes
- Requiem new-game initialization keeps its audio but no longer applies or clears the black fade during `VersionSavegame == 0`; existing-save update fades remain intact.
- Master sequence lock now disables camera switching and looking, and sets `Game.GetPlayer().SetDontMove(True)` until success/failure cleanup.
- SkySigns now removes `SkySigns_Ab` after `ShowMenu()` returns so the active effect can reliably send `_Authoria_Init_SkySignsDone`.
- Added a working-mod `McmRecorder.psc` loose override that listens for `_Authoria_Init_PlayMcmRecording`, plays the named preset, then sends `_Authoria_Init_McmRecorderDone`.
- Master sequence now sends the Authoria MCM Recorder event and waits for `_Authoria_Init_McmRecorderDone` before showing the finish message and unlocking controls.
- Compiled `REQ_VersionController.pex`, `_Authoria_Init_MasterSequence.pex`, `SkySigns_Script.pex`, and `McmRecorder.pex` successfully.

## 2026-07-13 SkySigns 1.0.6 update — birthsign step re-architected
Context: SkySigns updated 1.0.5.0 -> 1.0.6.0, a ground-up script rewrite, plus a new
companion patch `Sky Signs - Birthsigns Redone` (same author, modid 147884) that ships loose
scripts overriding `Requiem - Birthsigns Redone.esp` so SkySigns' b612 grid UI now drives the
**Requiem** birthsigns. The patched `Nox_Birthsign_InitQuest` also removes the SkySigns
standing-stone power on new game, so the real selector in ARR is
`REQ_Ability_Birthsign_ChooseBirthsign` (`000813:Requiem - Birthsigns Redone.esp`, a
LesserPower/Self), not `SkySigns_Ab`.

What broke and what changed:
- The old loose `SkySigns_Script.pex` override (v1.0.5, `extends activemagiceffect`, held the
  `NotifySkySignsDone` hook) was **deleted**. In 1.0.6 `SkySigns_Script` `extends Quest` with a
  new API, so our stale copy would have won VFS and clobbered the rewritten base with a
  wrong-typed script.
- The master sequence's birthsign step no longer casts `SkySigns_Ab` or waits on the
  `_Authoria_Init_SkySignsDone` mod event. It now resolves `ChooseBirthsign` at runtime via
  `Game.GetFormFromFile(0x000813, "Requiem - Birthsigns Redone.esp")`, `AddSpell`s it
  defensively, casts it, and detects completion by polling `HasSpell(ChooseBirthsign)` — the
  patched birthsign script removes that power once a sign is picked. No ESP master or property
  fill is needed, and we no longer depend on overriding anyone's script.
- Removed now-dead plumbing from `_Authoria_Init_MasterSequence.psc`: the `SkySigns_Ab`
  property, the `SkySignsDone` flag, the `_Authoria_Init_SkySignsDone` registration + handler,
  `NotifySkySignsDone`, and `WaitForSkySigns` (replaced by `WaitForBirthsign`).
- Recompiled `_Authoria_Init_MasterSequence.pex` (import dirs: Init Sequence Source, MCM
  Recorder Fix, base MCM Recorder, JContainers AE, PapyrusUtil AE, PO3 Extender, vanilla,
  USSEP — NOT MCM Helper, whose `MCM` script collides with MCM Recorder's `mcm` local).
- Untested in-game as of this entry; needs a new-game run to confirm the birthsign grid
  appears at step 7 and the sequence advances on selection.

### Follow-up (same day): vanilla finish placeholder wrongly appeared
- First full new-game run reached the end (birthsign step now works) and the vanilla
  "Placeholder finishing message" box popped up at the end.
- What the Papyrus log proves: the fallback trace lives INSIDE the `If ShowNotice("finish")`
  branch, so `ShowNotice` returned True; and it fired 27s after MCM playback (not the 300s
  timeout), so `WaitForPrismaPromptAction()` returned a non-empty action that was NOT
  `notice|finish|continue`, tripping the brittle equality check into `FinishMessage.Show()`.
  It does NOT prove the finish notice actually RENDERED, or where the 27s action came from.
- ROOT CAUSE (confirmed via `_AuthoriaInitializationNG.log` after enabling its logging): the
  finish prompt reaches the bridge with `promptId="Finish"` (capital F) — logged envelope
  `"promptId":"Finish"` — even though the pex passes lowercase `"finish"`. Proof the pex is
  lowercase: a proper PEX string-table parse shows string [169]=`'finish'` with NO bare
  `"Finish"` literal; Champollion agrees; ripgrep finds exactly one caller (this script,
  lowercase); and the Papyrus log proves THIS pex ran (`Property SkySigns_Ab ... no longer
  contains that property`). The gap is the engine: Papyrus `String`/`BSFixedString` use a GLOBAL,
  case-insensitive intern pool that returns the FIRST-seen casing of a word across all loaded
  scripts. `"Finish"` is a very common identifier/state across ARR's ~3400 plugins, so its
  canonical interned form is `Finish`; when the VM marshals the literal to the DLL's `std::string`
  it hands over `Finish`. `welcome`/`difficulty` don't collide, so they arrive lowercase and work.
- Then the web UI `normalizePrompt` did `defaults[promptId]` (case-SENSITIVE); `defaults["Finish"]`
  missed and fell back to the WELCOME definition, whose button emits `notice|welcome|continue`,
  which failed the Papyrus `== "notice|finish|continue"` check -> vanilla fallback. The "final
  message" seen was the welcome notice re-rendered under a finish request.
- Why it only appeared now: pre-fix the birthsign step timed out -> `FailSequence`, so
  `ShowFinishPrompt` never ran. The birthsign fix made the sequence reach the finish prompt for
  the first time, exposing this latent case-fragility. No Papyrus code is wrong; the psc is
  UNCHANGED (still `ShowNotice("finish")` + exact-string check + fallback).
- FIX (the cause, not the fallback): `PrismaUI/views/AuthoriaInitializationNG/index.html`
  `normalizePrompt` now lowercases the promptId before lookup
  (`String(payload.promptId||"welcome").toLowerCase()`), so any interned casing maps to the right
  `defaults` entry (and the CSS class normalizes too). HTML/JS only — no recompile; PRISMA reloads
  it on next game load. The Papyrus action `==` check is already case-insensitive, so the returned
  `notice|finish|continue` matches regardless of casing.
- Diagnostics logging left ENABLED in `_AuthoriaInitializationNG.ini` for verification; set
  `Enabled=false` (and `LogPayloads=false`) once confirmed.

## 2026-07-20 Devotion startup popups folded into the sequence
Goal: the **Devotion** mod's race-based startup popup(s) (Argonian->Hist info box, the
Nord/Breton/Bosmer/Redguard/Orc choice+confirm flow, etc.) must appear AFTER the SkySigns
birthsign step and BEFORE the difficulty message, and the sequence must wait for ALL of them
to finish before advancing. Previously they fired on their own the instant RaceMenu closed.

How Devotion's popup actually works (source read of `Devotion\Scripts\Source`):
- `PDV__ManagerQuest` (`00C325:Devotion.esp`, Start-Game-Enabled) ticks `OnUpdate` every 1s and
  calls `EnsureUnifiedStartupChoice()`. It fires when TWO conditions hold: the PapyrusUtil
  StorageUtil int `PDV.Startup.UnifiedChoiceComplete` (namespace `None`) is not yet `1`, AND the
  origin race is resolved (`PDV_GLO_OriginRace >= 0`). It sets that flag to `1` when the player
  finishes (choice races show a choice box + a confirm box, looping until confirmed; other races
  a single `Debug.MessageBox`). So "all popups done" == "flag == 1".
- Origin capture is one-way: `IsOriginCaptureSafe` (`PDV_PlayerEvents`) needs movement+menu
  controls enabled and only gates CAPTURE. Origin captures in the brief enabled window right as
  RaceMenu closes (before our `LockPlayer` runs), and STAYS resolved. `EnsureUnifiedStartupChoice`
  does NOT re-check `IsOriginCaptureSafe`, so re-locking controls cannot re-suppress the popup —
  which is why it fired immediately on RaceMenu close, not at our old end-of-sequence unlock.
  Confirmed against the initial control-lock hypothesis, which was WRONG in practice.

Neutralization + drive (NO ESP edit, NO Devotion file touched — the suggested "clear Start Game
Enabled / Run Once" does NOT apply: the popup lives inside the always-on `PDV__ManagerQuest` that
runs ALL of Devotion, so its SGE flag can't be cleared without disabling the mod). Uses only
Devotion's public StorageUtil gate:
- `HoldDevotionStartup()` added to `_Authoria_Init_MasterSequence.OnInit` (game start, before
  origin can resolve): if `Game.GetFormFromFile(0x00C325,"Devotion.esp")` resolves, set
  `PDV.Startup.UnifiedChoiceComplete = 1`. This holds the popup from before RaceMenu even closes.
- `WaitForDevotion()` inserted between the birthsign step and the difficulty picker: sets the flag
  back to `0` (Devotion fires on its next tick), briefly enables controls with `SetDontMove(True)`
  as a safety net for the rare custom-race origin deferral, then polls the flag until it reads `1`
  (StepTimeout = 300s). The difficulty step re-locks immediately after.
- Fail-safe: `FailSequence` now calls `ReleaseDevotionStartup()` (flag -> `0`) so an init that
  aborts before the Devotion step never leaves Devotion's startup permanently muted.
- On timeout `WaitForDevotion` LOGS and PROCEEDS to difficulty (not `FailSequence`) — a Devotion
  hiccup must not brick the new game; with the flag left at `0` Devotion simply shows its popup
  later, the old fallback behavior.
- Recompiled `_Authoria_Init_MasterSequence.pex` OK (same import dirs as the 07-13 entry: Init
  Sequence Source, MCM Recorder Fix, base MCM Recorder, JContainers AE, PapyrusUtil AE, PO3
  Extender, vanilla-with-flags, USSEP — NOT MCM Helper).
- UNTESTED until a new-game run. Watch for: (1) NO Devotion popup right after RaceMenu closes;
  (2) the Devotion popup(s) appear AFTER the birthsign grid and BEFORE the difficulty message;
  (3) for a choice race, both the choice AND its confirmation resolve before difficulty shows;
  (4) the sequence advances to the difficulty picker only once the popup(s) are dismissed. A
  Papyrus trace `Devotion detected; startup popup held (UnifiedChoiceComplete=1).` at game start
  confirms the hold fired.

## 2026-05-21 PRISMA UI Feasibility Study
- PRISMA UI `1.4.1.0` is installed and enabled in Authoria.
- `SKSE/Plugins/PrismaUI.dll` resolves from `Prisma UI - Next-Gen Web UI Framework` with no conflicts.
- Authoria already has a live PRISMA consumer example: `Authoria - FrostFallWidgetsNG`.
- Passive HUD rendering is proven by `FrostFallWidgetsNG`.
- Clickable prompt UI is feasible using the `SanguineTrade-PrismaUI` pattern: `Show/Hide`, `Focus/Unfocus`, `RegisterJSListener`, queued actions, and Papyrus polling.
- The first-pass replacement scope is master-sequence prompts only: welcome, difficulty picker, and finish.
- Starting Choices, Biggie Traits, and SkySigns internal menus are explicitly out of scope for this first pass.
- Vanilla `Message.Show()` fallback remains required if PRISMA UI or the native bridge is unavailable.

## 2026-05-21 Easy/Hard Difficulty Tuning
- PRISMA/SKSE bridge is considered stable and is not part of difficulty tuning.
- Difficulty selection now tracks a mode (`easy`, `normal`, `hard`) and then maps that mode to MCM Recorder playback:
  - `easy` -> `Authoria_Easy`
  - `normal` -> `Authoria_Base`
  - `hard` -> `Authoria_Hard`
- Hard mode is recording-only. `madEngagingCombat.esp` / Engaging Combat must remain a manual pre-game user choice; the initialization sequence does not enable, disable, or configure it.
- Normal mode is baseline and restores Requiem Lite to its default disabled state.
- Easy mode enables Requiem Lite, adds `RequiemLite_Perk` from `Requiem Lite.esp:000D63`, and writes Easy runtime INI values.
- Requiem Lite enable-message suppression is done as a loose script override in `Authoria - Initialization Sequence`, not by editing `Requiem Lite 2` in place. The MCM remains usable so the user can disable Requiem Lite later.
- Future Easy INI additions must be added in two places:
  1. The source setting file under `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings`.
  2. The runtime apply list in `_Authoria_Init_MasterSequence.psc`, so Easy selection writes the same value in-game.

### Easy Runtime INI Source Files
- `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings\MCM\Settings\TKDodgeAddon.ini`
- `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings\MCM\Settings\Wounds.ini`
- `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings\MCM\Settings\Requiem.ini`
- `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings\SKSE\Plugins\Experience.ini`
- `D:\Wabbajack\Authoria-dev\mods\Authoria - Easy Mode Settings\SKSE\Plugins\SkyParkourNG.ini`

### Easy Runtime INI Values
`Data/MCM/Settings/TKDodgeAddon.ini`

```ini
[General]
iDodgeKey = 56
fDodgeCost = 10.0
bEnableSprintDodge = 0
bUseMCORecovery = 1
bUsePercentages = 0

[Perk]
bUsePerkLock = 0
```

`Data/MCM/Settings/Wounds.ini`

```ini
[GlobalOptions]
iBaseInjuryChance = 5
iBaseInfectionChance = 5
iHeadInjuryChance = 10
iRightArmInjuryChance = 30
iRightLegInjuryChance = 10
iInjurySeverity = 1
iMinimumSpeed = 40
iTorsoInjuryChance = 25
iLeftArmInjuryChance = 30
iLeftLegInjuryChance = 10
iArmorOffset = 50

[BrokenBones]
sBrokenBonesHealTime = 5.641263 days
iBrokenBonesChance = 15

[Bruises]
sBruisesHealTime = 1.880421 days
iBruisesChance = 40

[Concussions]
sConcussionsHealTime = 1.880421 days
iConcussionsChance = 20

[Cuts]
sCutsHealTime = 1.880421 days
iCutsChance = 50

[Maintenance]
bLoadSettingsonReload = 1
```

`Data/SKSE/Plugins/Experience.ini`

```ini
[General]
bEnableKilling = true
bEnableReading = true
bEnableSkillXP = false
iMaxPlayerLevel = 100
fSkillCapBase = 100.000000
fSkillCapMult = 0.000000
bUseRacialCaps = false
bShowMessages = true

[Questing]
iXPQuestNone = 10
iXPQuestMain = 175
iXPQuestCollege = 80
iXPQuestThieves = 50
iXPQuestBrotherhood = 80
iXPQuestCompanions = 80
iXPQuestMisc = 10
iXPQuestDaedric = 150
iXPQuestSide = 30
iXPQuestCivilWar = 100
iXPQuestDawnguard = 300
iXPQuestDragonborn = 300

[Exploring]
iXPDiscDefault = 0
iXPDiscCity = 0
iXPDiscTown = 0
iXPDiscSettlement = 0
iXPDiscCave = 0
iXPDiscCamp = 0
iXPDiscFort = 0
iXPDiscNordicRuin = 5
iXPDiscDwemerRuin = 15
iXPDiscShipwreck = 5
iXPDiscGrove = 0
iXPDiscLandmark = 0
iXPDiscDragonLair = 15
iXPDiscFarm = 0
iXPDiscWoodMill = 0
iXPDiscMine = 0
iXPDiscDoomstone = 10
iXPDiscWheatMill = 0
iXPDiscSmelter = 0
iXPDiscStable = 0
iXPDiscImperialTower = 0
iXPDiscClearing = 0
iXPDiscPass = 0
iXPDiscAltar = 0
iXPDiscRock = 0
iXPDiscLighthouse = 0
iXPDiscOrcStronghold = 10
iXPDiscGiantCamp = 5
iXPDiscShack = 0
iXPDiscNordicTower = 5
iXPDiscNordicDwelling = 5
iXPDiscDocks = 0
iXPDiscDaedricShrine = 15
iXPDiscCastle = 0
iXPDiscMiraakTemple = 30
iXPDiscTelvanniTower = 0
iXPDiscCastleKarstaag = 30

[Clearing]
iXPClearDefault = 20
iXPClearCity = 0
iXPClearTown = 0
iXPClearSettlement = 0
iXPClearCave = 20
iXPClearCamp = 0
iXPClearFort = 30
iXPClearNordicRuin = 40
iXPClearDwemerRuin = 60
iXPClearShipwreck = 0
iXPClearGrove = 0
iXPClearLandmark = 20
iXPClearDragonLair = 60
iXPClearFarm = 0
iXPClearWoodMill = 0
iXPClearMine = 20
iXPClearDoomstone = 40
iXPClearWheatMill = 0
iXPClearSmelter = 0
iXPClearStable = 0
iXPClearImperialTower = 25
iXPClearClearing = 0
iXPClearPass = 0
iXPClearAltar = 40
iXPClearRock = 0
iXPClearLighthouse = 0
iXPClearOrcStronghold = 0
iXPClearGiantCamp = 50
iXPClearShack = 0
iXPClearNordicTower = 25
iXPClearNordicDwelling = 0
iXPClearDocks = 0
iXPClearDaedricShrine = 0
iXPClearCastle = 0
iXPClearMiraakTemple = 80
iXPClearTelvanniTower = 0
iXPClearCastleKarstaag = 80

[Killing]
fLevelFactor = 1.000000
fGroupFactor = 0.500000
fKillingMult = 3.000000

[Reading]
fReadingMult = 3.000000
```

`Data/MCM/Settings/Requiem.ini`

```ini
[General]
fDiffMultHPByPCL = 1.100000
fDiffMultHPToPCL = 0.900000
fJumpHeightMin = 76.000000
iHoursToRespawnCell = 336
iHoursToRespawnCellCleared = 7200
fPlayerHealthHeartbeatSlow = 0.100000
bAtmosphereAllowFastTravel = 1
bCombatNoDeathHandling = 1
bCombatNoFearAndYield = 1
bCombatNoHorseTrample = 1
bCombatNoOnHitDisarm = 1
iWIWaitDragon = 12
bAtmosphereNoPoisonISM = 1
bCombatEssentialAgain = 0
bSkillsNoSmithingBooks = 0
fTimeScale = 12.000000
fAtmosphereKillmoveHealthThreshold = 0.100000
bCombatNoDragonFear = 1
```

`Data/SKSE/Plugins/SkyParkourNG.ini`

```ini
[ESP]
sEspName = SkyParkour.esp
iBlueMarkerRefID = 0x000014
iRedMarkerRefID = 0x00000C

[MCM]
bEnableMod = true
bShowIndicators = false
fPlaybackSpeed = 1.15
bUsePresetKey = true
iPresetKeyIndex = 0
iCustomKeybind = 0
fInputDelay = 0.0
bEnableStaminaSystem = false
bMustHaveStamina = true
iBaseStaminaDamage = 20
bSmartSteps = true
bSmartVault = true
bSmartClimb = true
```

## 2026-07-21 — Removed the per-step timeouts (players skipped elements when lingering)

- **Symptom reported:** if a user lingered past ~5 minutes on any character-creation step
  (starting-choices items, Biggie Traits, birthsign, etc.), later parts of the sequence were
  just skipped.
- **Cause:** every wait loop was bounded by `StepTimeout`/`PrismaPromptTimeout` (300s, a
  testing-phase safeguard). On timeout the step's `WaitFor*` returned False and `FailSequence`
  aborted the whole remaining sequence — hence the "skipped elements."
- **Fix in `_Authoria_Init_MasterSequence.psc`:** dropped the `StepTimeout` /
  `PrismaPromptTimeout` properties and `GetPrismaPromptTimeout()`; every `WaitFor*`
  (Requiem, StartingChoices, Traits, Birthsign, Devotion) and `WaitForPrismaPromptAction`
  now blocks on its completion condition only, no time bound. Removed the now-dead
  `If !WaitForX() ... FailSequence(...)` guards in `StartSequence`. `FailSequence` /
  `ReleaseDevotionStartup` kept as harmless failsafe scaffolding.
- Recompiled `_Authoria_Init_MasterSequence.pex` OK (same import dirs as prior entries),
  landed straight into `Scripts\`.
- UNTESTED until a new-game run — verify a deliberately slow run through every step no longer
  skips anything.

## 2026-07-22 — NSFW-profile OStim recording chained after the difficulty recording

Goal: in the **NSFW profile only**, after the difficulty recording (`Authoria_Easy` /
`Authoria_Base` / `Authoria_Hard`) finishes, automatically play the extra adult-stack preset
`AUTHORIA_OSTIM` that ships in `Authoria - Ostim tweaks and Patches\McmRecorder`, then show the
finish prompt. The **Main profile sequence must be unchanged**.

- New sequence (NSFW): Devotion popups -> difficulty choice -> difficulty recording ->
  `AUTHORIA_OSTIM` recording -> finish message. Main profile: unchanged (the new step returns
  immediately).
- **Gate:** `Game.IsPluginInstalled("OStim.esp")` in the new `PlayOStimRecording()` helper in
  `_Authoria_Init_MasterSequence.psc`, called between the difficulty playback and
  `ShowFinishPrompt()` (with a `LockPlayer()` on each side). `OStim.esp` is active only in the
  NSFW profile (confirmed via houseCARL load-order lookup), so the Main profile skips the whole
  step. `IsPluginInstalled` was chosen over `GetModByName` because it covers ESL-flagged plugins
  too; SKSE's plugin lookup is case-insensitive, so the Papyrus string-interning casing trap that
  bit the `finish` promptId does not apply here.
- **No new asset or manifest change needed.** `AUTHORIA_OSTIM.json` already has
  `"autorun": "False"`, so it never fired on its own, and MO2's VFS merges both mods'
  `McmRecorder\` folders into one `Data\McmRecorder`, which is exactly where
  `McmRecorder_RecordingFiles.PathToRecordingFolder` looks. The OStim tweaks mod is untouched.
- Playback uses the same call shape as the difficulty step —
  `McmRecorder_Player.PlayRecording("AUTHORIA_OSTIM", mcmLoadWaitTime = 30.0, verbose = False)`.
  `PlayRecording` is fully self-contained (it clears mods-played state and sets/clears its own
  is-playing flag), so calling it twice back-to-back is safe.
- Recompiled `_Authoria_Init_MasterSequence.pex` OK straight into `Scripts\`. **Import dirs
  corrected** — two paths in the earlier entries no longer exist; the working set is now:
  Init Sequence Source; `Authoria - Papyrus - MCM Recorder Fix\Scripts\Source`;
  `MCM Recorder\Scripts\Source`; `JContainers AE\Scripts\Source`;
  `PapyrusUtil AE - Scripting Utility Functions\Source\Scripts`;
  `PowerofThree's Papyrus Extender\Source\scripts`; vanilla-with-flags; USSEP — NOT MCM Helper.
- UNTESTED until a new-game run. Watch for: (1) in the **NSFW** profile the OStim recording runs
  right after the difficulty recording and before the finish message; (2) in the **Main** profile
  nothing changes and the Papyrus log shows no `OStim detected` trace; (3) MCM Recorder does not
  choke chaining two recordings (watch for a stuck MCM/system menu between them).
