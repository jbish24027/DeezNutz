# MCM census and cut candidates — CS profile (DEEZ CS NUTZ)

Date: 2026-08-19
Profile scanned: `DEEZ CS NUTZ` (3868 enabled mods)
MO2 was closed during the scan. Nothing was changed. This file is a proposal only.

---

## 1. The short version

SkyUI can hold **128 MCM menus**. That is a hard cap in SkyUI's own code. When the
129th mod asks to register, SkyUI silently refuses it. The menu never appears.

MCM Recorder finds a menu by looking it up in SkyUI's registered-menu list, by name.
A menu that never registered is not in that list. Playback then stalls on
"Waiting for <mod> MCM to load", then offers Try again / Skip.

So an MCM past the cap cannot be used in a recording at all.

The usual workaround, **MCM Limit Upgraded**, is listed by MCM Recorder's own author
as incompatible with MCM Recorder. It is not installed here, and it should not be.

That leaves one option: fewer MCMs.

**Current count: about 125 of the 128 slots.**

| Menu type | Count | How it was counted |
|---|---|---|
| SkyUI-native (SKI_ConfigBase) | 85 | every loose and BSA script, conflict winners only |
| MCM Helper (JSON) | 38 | read from the last real game run's MCM Helper log |
| NL_MCM | 2 | Save System Overhaul, OComfort |
| **Total** | **~125** | |

Treat 85 as an upper bound. A menu script only takes a slot if its quest actually
runs, and a few of the 85 may be dormant. The real number is somewhere in the high
110s to 125. Either way there are only a handful of free slots, and every new mod
with a menu eats one.

---

## 2. What is NOT the problem

These were checked and ruled out.

1. **MCM Recorder losing its script to a conflict.** MCM Recorder works by replacing
   SkyUI's `SKI_ConfigBase`. Only two mods ship that file loose, and the one that wins
   is `Authoria - Papyrus - MCM Recorder Fix`, which is the correct winner. SkyUI's own
   copy is inside a BSA and loses to both.
2. **MCM Helper menus being unrecordable by design.** MCM Helper's base script does not
   override the six functions MCM Recorder hooks. Recording is not structurally blocked
   for them.
3. **NL_MCM menus being unrecordable.** Save System Overhaul is NL_MCM based and it
   recorded fine — see `jbish base`, step 0007.
4. **Settings-loader mods creating a duplicate menu.** Checked all five. Each one
   overrides the mod's own menu script and wins on priority. One menu each, not two.

---

## 3. Bucket 1 — spare menus inside a mod that already has one

Frees 7 slots. Lowest risk of the three buckets. The mod keeps its main menu.

| Mod | Keep | Drop |
|---|---|---|
| Legacy of the Dragonborn V6 | main museum menu | debug menu, dynamic-display menu, fossil menu |
| Campfire | main Campfire menu | the second unequip menu |
| At Your Own Pace | the main quest menu | College of Winterhold menu, Thane Overhaul menu |
| Requiem | main Requiem menu | the second skills menu |

Note on Requiem: confirm the skills menu is not the one you use before dropping it.

---

## 4. Bucket 2 — menus whose values already come from a settings file

Frees up to 10 slots. These mods already read their settings out of a file that
`Authoria - MCM and INI Settings` (or the mod's own settings loader) ships. The
menu is only there for manual tweaking after the fact.

- DynDOLOD
- Honed Metal
- Trade and Barter
- OBody NG
- Atlas Map Markers
- VioLens
- Sanguine Symphony
- Dismembering Framework
- Wounds
- Bow Rapid Combo

Before dropping any of these, confirm its settings file is actually live and not a
leftover. Two on this list (VioLens, Bow Rapid Combo) have a settings file but no
matching settings-loader mod installed, so their file may be orphaned.

---

## 5. Bucket 3 — set-once utility menus

Frees about 15 slots. Every one of these is a judgement call, not a free win. You
lose the ability to change these in game.

- Complete Controller Setup
- Gamepad Plus Plus
- Hot Key Skill
- Auto Move
- Hide Quest Items in Container Menu
- YEET - Store Quest Items
- Fast Travel Cost
- Wait Carriage in Inns
- Select Your Season
- Storm Lightning
- Helios
- EVG CLAMBER
- FSMP
- Custom Skills Menu
- Mists of Tamriel

---

## 6. How to actually kill a menu, CS profile only

This matters. MO2 has only one per-profile lever, which is whether a mod is enabled.
Hiding or deleting a file inside a mod folder hits every profile at once. So a
CS-only change has to live in a new mod that is enabled in CS and nothing else.

**For SkyUI-native menus — recommended.**
Author one small plugin that overrides each MCM quest and clears its
"Start Game Enabled" flag. The quest never starts, so it never registers, so the
menu never appears and the slot stays free. Nothing else about the mod changes.
Reversible by disabling the one plugin. It must be ESL-flagged at creation because
the full-plugin list is at its cap.

Caveat: this is only safe when the quest does nothing but the menu. Most are named
so that this is obvious, but each one needs a look before it goes in.

**For MCM Helper menus — not recommended yet.**
The lever is the menu's `config.json`. A higher-priority mod can replace it, but an
emptied file may still register a blank menu and still burn the slot. This needs one
in-game test before it is worth building.

**Not recommended at all.**
Replacing the menu script with a stub. The quest keeps running, its script properties
fail to fill, and anything that calls into that script breaks. This is how you get
silent Papyrus damage.

---

## 7. Full census

### SkyUI-native menus, by owning mod (85)

Mods owning more than one:

- Campfire - Script Optimization — 2
- Legacy of the Dragonborn V6 — 4

One menu each (79 mods):

A Matter Of Time - Settings Loader, Amorous Adventures - MCM, Apocalypse - Magic of
Skyrim, At Your Own Pace, At Your Own Pace - College of Winterhold, At Your Own Pace -
Thane Overhaul, Atlas Map Markers, Authoria - Bards Reborn Tweaks, Authoria - Dirt and
Blood Tweak, Authoria - No Ammo and Septim Weight (Requiem), Authoria - Ostim tweaks and
Patches, Authoria - Papyrus - Frostfall Updates and Fixes, Authoria - Papyrus - Wet and
Cold Optimized, Authoria - Sunhelm MCM Fix, Authoria - Time Flies - No Spell Tome Time,
Auto Move, Bow Rapid Combo V3, C.O.I.N, CBBE 3BA (3BBB) - Config, Complete Controller
Setup, Custom Skills Menu, Deadly Dragons, Devotion, Dismembering Framework, Dragonborn
Voice Over, DynDOLOD - Settings Loader, EVG CLAMBER - Slope Animations, Experience - MCM,
FSMP - Faster HDT-SMP, Fast Travel Cost, Fort Takeovers Framework, Frostfall - Seasons,
GLENMORIL, Gamepad Plus Plus, Hearthfire Multiple Adoptions Expanded, Helios, Hide Quest
Items in Container Menu, Honed Metal - Settings Loader, Hot Key Skill, Immersive Kaidan
AIO, LOTD - The Curator's Companion, Lucien, MCM Recorder, OBody NG - Yet Another Settings
Loader, OCum Ascended, OISeeYouMasturbating, OStim NPCs, OStim Standalone, Ostim Standalone
Sound Overhaul, PC Head Tracking - MCM, Requiem 6.0.2 Bugfix Pack (skills menu), Sacrilege,
Sanguine Symphony, Sanguine's Trade, Schlongs of Skyrim - NG, SearchUI - Remember Settings,
Seasonal Weathers Framework, Select Your Season, Shadow of Skyrim, Simple Fishing Overhaul,
Simply Knock SE, Skyrim Arrow Overhaul, Skyrim Outfit Equipment System NG, SmoothCam, Spell
Hotbar, Stage Flow for OStim, Starting Choices, Storm Lightning, Survival Control Panel, The
Tools of Kagrenac, Thieves Guild Requirements SE, Trade and Barter - Settings Loader, Unslaad
SE, VioLens, Wait Carriage in Inns, Wounds - Simplified, YEET - Store Quest Items, Mists of
Tamriel, moreHUD - AE

### MCM Helper menus (38, from the last real game run)

BetterThirdPersonSelection, Biggie Traits, Campfire Animations, DEST_ISL, Dynamic
Activation Key, DynamicCollisionAdjustment, Easy Console Commands, FirstPersonInteractions,
FloatingSubtitles, Follower Stats, Helmet Toggle 2, Horse Whistle Key, HotkeyReminder,
Immersive Equipping Animations, ImmersiveHunting, LootingAnimations, LoreBox, Missives,
OptimalPotionHotkeyMCM, PhotoMode, Precision, Quick Item Transfer, SeranaMultiformNG, Simple
Hunting Overhaul, SkyUI itself, Skyrim Got Talent UI, SkyrimWaterInertia,
StealthKillDetectionFix, Stress and Fear, TKDodgeAddon, ThirdPersonFirstPersonAiming,
TrueDirectionalMovement, TrueHUD, Vigilant, Wheeler UI, Wyrmstooth, fixLOD, tent_pitcher

### NL_MCM menus (2)

Skyrim Save System Overhaul 3, OComfort

---

## 8. What the existing recordings cover

Five recordings exist: `Authoria_Base`, `Authoria_Easy`, `Authoria_Hard`, `jbish base`,
and `AUTHORIA_OSTIM`. Between them they touch about 31 menus. Every one of those is
SkyUI-native or NL_MCM. No MCM Helper menu appears in any recording, which fits the
pattern of MCM Helper mods being configured by shipped settings files instead.

Two recorded steps are named with an untranslated key rather than a display name
(`$MODNAME`, `$FrostfallSeasons`, `$SkyOutEquSys_MCMName`). Those work, but they will
break if the owning mod ever ships a translation for that key, because the lookup is
by display name.
