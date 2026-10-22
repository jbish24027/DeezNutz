# MCM cut list — verification pass

Date: 2026-08-19
Profile: `DEEZ CS NUTZ`. MO2 closed. Nothing changed. Proposal only.
Companion file: `MCM-CENSUS-AND-CUT-CANDIDATES-20260819.md` (the census and the 128-slot finding).

You asked for bucket 1 and bucket 2, keeping Wounds. That was 16 menus.
I checked every one. **Six survive. Nine would break something. One I could not verify.**

---

## 1. Direct answer on the initialization sequence

The init sequence is not at risk from any of this.

1. I read every step file in all five recordings — `Authoria_Base`, `Authoria_Easy`,
   `Authoria_Hard`, `jbish base`, `AUTHORIA_OSTIM`. Between them they drive 31 menus.
   **None of the 16 cut candidates is one of them.**
2. None of the init sequence's own scripts names any of the 16.
3. The recordings do not touch Requiem's menu, Legacy of the Dragonborn's menus, or any
   of the settings-loader mods.

One thing worth knowing while I was in there. The recording step that shows as
`$MODNAME` is **CBBE 3BA**. Its menu registers under an untranslated token because no
translation file defines that key. It works today. It will break the moment 3BA ships a
translation for that key, because MCM Recorder looks menus up by display name. Same
shape as the `$FrostfallSeasons` and Outfit Equipment System steps. Not on any cut list,
just a landmine to know about.

---

## 2. What survives — safe to cut

Six menus. All verified: dedicated menu-only quest, nothing else on the load order calls
into the script, and no work done at game load.

| Menu | Why it is safe | What you lose |
|---|---|---|
| At Your Own Pace — Thane Overhaul | Menu-only quest. Writes its globals only when you click. Nothing references it. | The in-game toggles. Globals keep their plugin defaults. |
| OBody NG | Its menu sits on a separate quest from OBody's logic. Settings still load from your settings file via OBody's own script. | In-game toggles and remapping the preset key. The key itself still loads from the file. |
| VioLens | Menu-only quest. Writes globals only when you click. Nothing references it. | In-game killmove tuning. Globals keep their plugin defaults. |
| Bow Rapid Combo | Menu-only quest. It is two keybinds and nothing else. | Rebinding those two keys in game. |
| Legacy of the Dragonborn — debug menu | Menu-only quest, no aliases, nothing references it. | Legacy's debug/troubleshooting tools. |
| At Your Own Pace — College of Winterhold *(conditional)* | Menu-only script, nothing references it. **But** its quest is also the mod's objective tracker. | The toggles, and the "objectives shown between quests" display. Take this one only if you do not want that display. |

Note on the two Legacy menus. Legacy does not start its menu quests at game start — a
Legacy script starts them. So the flag lever I described does not reach them. For the
debug menu I would instead detach the menu script from its quest, which leaves the quest
running and harmless. That is slightly more invasive and it changes a record Legacy owns.

That is **5 clean slots, 6 if you take the College one**. Roughly 125 down to 119-120.

---

## 3. What does not survive — and why

Nine menus. Each of these would break something.

**Their menu script is the thing that applies the settings on every game load.**
Stop the quest and the mod silently drops back to its plugin defaults. The settings file
you ship is read *by that script*, so killing the menu throws the settings away too.

- **Trade and Barter** — reloads roughly forty values into globals and game settings every load.
- **Honed Metal** — same pattern.
- **DynDOLOD** — same pattern, and it writes engine INI values and calls into the DLL.

**Another script calls into the menu, so removing it leaves a dangling reference.**

- **Requiem — skills menu.** Requiem's own data-storage script uses it.
- **Legacy of the Dragonborn — display checklist.** Legacy's SKSE support script uses it.
- **Atlas Map Markers.** Its player alias script uses it, and that alias runs at load.
- **Sanguine Symphony.** Its maintenance script uses it.
- **Dismembering Framework.** Its maintenance script uses it.

**I had it mislabelled.**

- **The "spare Campfire menu" is not Campfire's.** It ships inside the Campfire script
  optimisation mod but it belongs to **Equipping Overhaul** — geared-up display, drop-torch
  and item-recovery hotkeys. It registers those hotkeys itself. Killing it kills them.
  It is a real control panel, not a duplicate.

**Not counted.**

- **Legacy of the Dragonborn — fossil menu.** I could not find a quest that carries it.
  It may already be inert, in which case cutting it frees nothing. Worth a look in game
  before counting it.
- **Wounds** — you excluded it.

---

## 4. Where this leaves the headroom problem

Best case here is six slots, about 125 down to 119. That buys room for new mods but it
does not change the picture much.

The reason the yield is low is structural. Most menus in this list are not decoration.
Either the menu script is the mod's settings engine, or another script holds a reference
to it. A menu is only safely removable when the mod author put it on its own quest and
kept the logic elsewhere, and most authors did not.

If you want materially more headroom, the honest options are:

1. Take the six, then re-check the count in game against the real registered list rather
   than my static census.
2. Look at whole mods you are not using rather than at menus. Removing a mod removes its
   menu for free.
3. Accept the ceiling and treat the 128 slots as a budget when adding anything new.

---

## 5. How I checked

1. Read every recording step file in all five recordings, and listed the 31 menus they drive.
2. Grepped the init sequence's own scripts for all 16 candidate names.
3. For each candidate, read its compiled script's symbol table for load-time work —
   `OnGameReload`, `OnUpdate`, `LoadSettings`, and the MCM Helper setting getters.
4. Read the actual source where the mod ships it, to confirm what `Load()` applies.
5. Swept every loose script and all 521 archives in the profile for any other script that
   names each candidate, to catch dangling references.
6. Pulled each candidate's quest record to check it is menu-only: script count, alias
   count, and whether the game starts it.

---

## 6. What was built — 2026-08-19

You confirmed VioLens, OBody and Bow Rapid Combo. Those three are done.

New mod: **houseCARL - Authoria - MCM Slot Trim**, one plugin, ESL-flagged.
It overrides three quest records and changes one field on each — the flag that tells
the game to start that quest. Nothing else in any record differs from the original.

Enabled in **DEEZ CS NUTZ only**. Present but switched off in the other three profiles.

Load order: directly after the Junk Disabler, well above the Synthesis, UBE, ParallaxGen,
DynDOLOD and flat-map blocks. Those are all still last, in every profile.

All four profile files were updated, including plugingroups. Every file touched has a
backup ending in `.bak-mcmslottrim-20260819`. The plugin has its own backup from before
the ESL flag went on.

Verified after writing: all three records now win from the new plugin, one field changed
each, no dangling references, no missing masters.

**This only takes effect on a new game.** Clearing the start flag stops the quest from
starting on a fresh save. On a save that already has those quests running, they stay
running and the menus stay visible. That suits the init sequence, which is a new-game flow.

Count goes from about 125 to about 122 of 128.

---

## 7. Never cut — the initialization recordings depend on these

Standing rule, set 2026-08-19. **Dirt & Blood is needed for initialization.** Its menu is
off-limits, and so is every other menu the recordings drive.

The recordings set two hotkeys on Dirt & Blood's Settings page — Wash Followers and Wash
Together. It appears in all four recordings: Base, Easy, Hard and jbish base.

The rule generalises. If a menu appears in any recording, it cannot be cut, because
playback looks the menu up by name and stalls when it is not registered. These are the 31
menus currently driven by the recordings:

Amorous Adventures, Apocalypse Spells, At Your Own Pace main quest, Become a Bard,
CBBE 3BA, C.O.I.N., Devotion, **Dirt & Blood**, Frostfall, Frostfall Seasons, GLENMORIL,
Immersive Interactions, Kaidan, moreHUD, OCum Ascended, OISeeYouMasturbating, OStim NPCs,
OStim Sound Overhaul, Outfit Equipment System, PC Head Tracking, Safe Save System Overhaul,
Schlongs of Skyrim, SearchUI, Seasonal Weathers, Shadow of Skyrim, Simply Knock,
Stage Flow for OStim, SunHelm, Survival Control Panel, Unslaad, Wounds.

Re-derive this list before proposing any future cut. It changes whenever a recording does.

Confirmed on 2026-08-19: the MCM Slot Trim plugin carries exactly three records — VioLens,
OBody and Bow Rapid Combo. Dirt & Blood's plugin is not even one of its masters.

---

## 8. REVERTED — 2026-08-19

The user reported the Dirt & Blood MCM missing on three new games in a row and
identified this change as the cause. It has been removed in full.

Removed from all four profiles: the mod entry, the plugin entry, the load order entry
and the plugin group entry. The mod folder was moved out of `mods` to
`C:\1. AUTHORIA\_REVERTED - houseCARL - Authoria - MCM Slot Trim`.

The old profile backups were NOT restored, because they predate the ten mods installed
later that day and restoring them would have wiped those. The four lines were removed
surgically instead. Fresh backups from just before the revert end in
`.bak-pre-revert-20260819`.

Verified after: enabled mods 3876, active plugins 3979, load order 4048 lines — each
exactly one less than with the trim in. Everything installed that day is still present.
The flat map block is still last.

**Do not re-add this without being asked.** Whether it was actually responsible for the
missing menu is unresolved.

---

## 9. RESOLVED — 2026-08-20

The missing Dirt & Blood MCM had nothing to do with the trim, the mod, or the recordings.

SkyUI's registration is lossy. Its RegisterMod locks itself while it works and rejects
every menu that calls during that window. Rejected menus retry, but only until one attempt
succeeds — after that a menu stops listening for good. SkyUI's cleanup pass then blanks any
slot whose menu momentarily reads as an invalid form. A menu that registers and is later
blanked is gone for the session and never retries. With ~125 menus answering the same
broadcast that is a lottery with a stable loser.

Fix: the master sequence now forces a full SkyUI registration rebuild before the recording
plays, and waits for the count to settle. Confirmed working by the user on a new game.

The three menus cut earlier (VioLens, OBody, Bow Rapid Combo) remain reverted and were
never the cause.

---

## CORRECTION — 2026-08-28

Two things in this document are now known to be wrong, and the slot situation has changed.

**Bow Rapid Combo is NOT safe to cut.** This document listed it as one of the six survivors.
Re-verification found criterion 2 fails: `BowBBConfigScript` is not just a menu, it is the mod's
keybind store. `BCKey1` and `BCKey2` are properties on that script, they ship UNBOUND (888), and
`BowRapidCQCScript` reads them at runtime. Cut the quest and the close-quarters combo system —
kick, dagger and melee attack directions, sprint attacks, backspin triggers — silently never
fires. Do not cut it.

**The count is no longer ~125.** Measured from a live Papyrus log on 2026-08-28: **128 of 128,
zero free**, with 134 distinct menus competing for the list. See [[mcm-128-slot-ceiling]].

**What was actually cut, 2026-08-28:** `houseCARL - Authoria - MCM Slot Trim` clears Start Game
Enabled on three menu-only quests — Better Third Person Selection (`000D62`), OBody NG
(`000D6B`) and VioLens (`005901`). Takes effect on a new game only.

Outfit Recognition was verified SAFE but deliberately left alone: cutting it locks ORF to
"everything on, maximum chattiness", which would undo the ORF patch work.

At Your Own Pace is excluded by user instruction, as is anything an MCM Recorder recording
drives. The live protected set is 32 menus across the four recordings plus AUTHORIA_OSTIM.

**Still worth checking:** LOTD Debug Menu registered in the live list even though its Start Game
Enabled flag is already clear, it is absent from `legacyofthedragonborn.seq`, and LOTD's own
`SKSESetup()` never initialises it. It is probably a stale registration carried in the save. If
it does not appear on a new game, that is a fourth slot for free.
