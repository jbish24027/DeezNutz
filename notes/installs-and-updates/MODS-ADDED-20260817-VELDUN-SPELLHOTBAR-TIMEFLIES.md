# Mods added / updated on 2026-08-17

Profile in use: DEEZ CS NUTZ. Every change was also written into the other three profiles at the same neighbours (details at the bottom).
Backups: `C:\1. AUTHORIA\backups\veldun-preupdate-20260817\` (the three old Vel'dun folders + all four profiles' modlist/plugins/loadorder/plugingroups).

## 1. Vel'dun UI 1.0.5 -> 1.0.6 (three folders updated in place)

The current FOMOD choices were reconstructed from the installed files (every installed file hash-matched against the option folders of the OLD archives), then the same choices were applied to the 1.0.6 archives. The reconstruction reproduced all three old folders byte-for-byte before the update was applied, so the choices below are proven, not guessed.

### Choices used (Vel'dun UI main FOMOD -> folder "Vel'dun UI")
- Main Files: Main Bulk
- Main Menu: Skip (default)
- General Patches: BTPS, CoMAP, Experience, ImGUI Icons, Oblivion Interaction Icons, STB Active Effects, STB Widgets, TrueHUD. NOT: Scribes of Skyrim, Inventory Bars, Music, Flick (new in 1.0.6)
- Dialogue: was "DBVO" in 1.0.5 - option REMOVED in 1.0.6, see the DBVO note below. Now: Skip/Default + carry-over folder.
- Patches page 1: COCKS = Skip; Compass Navigation Overhaul = Knotwork patch; Favorites Menu = Skip; Local Map Upgrade = Skip; moreHUD Inventory Edition = patch; moreHUD = patch; QuickLoot = Skip
- Patches page 2: Quest Journal = Skip; Detection Meter = patch; Floating Subtitles = Skip; Sorting Mod = Aura's Inventory Tweaks; Static Skill Leveling = Skip; TDM Target Lock = Vel'dun themed; Tween Menu = Custom Skills patch; Weapon Stats = Skip
- Resolution: 16 by 9
- Configs: Inventory placement = Slimventory; UI placement = BOTTOM (default); SkyUI 3D item = UI default
- Three options are indistinguishable from the files (COCKS crafting-categories patch, Inventory Bars, Local Map Upgrade): Slimventory overrides the same files, so ticked or not the result is identical, in 1.0.5 and in 1.0.6. Left unticked.

### Choices used (Vel'dun UI Patches FOMOD -> folder "Vel'dun UI Overhauls - Patches")
- Alternative Perspective (regular), Biggie Traits/Sky Signs, Casting Bar, Frostfall/Last Seed bars, UIExtensions (regular), Follower Stats, Legendary Map (CoMAP support, regular), Werewolf Transformation Timer, Oxygen Meter, Photo Mode, SkyParkour, Why I Came to Skyrim, Easy Console Commands, Sunhelm, Swiftly Order Squad (regular), LoreBox
- ADDED this time: Spell Hotbar (Nexus) - two icon files
- Everything else Skip, including the 1.0.6 newcomers (SKSE Menu, Apparel Preview, A Matter of Time, Kill Feed, QUI, Everdamned, Skills of the Wild). Note: you DO run A Matter of Time and SKSE Menu Framework - those two new looks-only patches are available if you want them.

### Choices used (Vel'dun UI Overhauls FOMOD -> folder "Vel'dun UI - More Patches")
- Character Menu = Character Menu Patch (regular); Dragonborn Bestiary = Bestiary Patch (regular, not KYE2); Favorites Menu = Effects Description Extended; Wait/Sleep Menu = Modern Wait Menu. Everything else Skip.
- This folder was still on 0.9.6 before today. Its wait-menu file now targets Modern Wait Menu 2.1.1; you run Modern Wait Menu 2.0.5. Harmless: "Dragonborn Reskin - Modern Wait Menu" sits above and wins the wait menu anyway (it also wins the character sheet, bestiary and favorites menu from this folder). If you ever disable that reskin, update Modern Wait Menu to 2.1.1.
- New in 1.0.6 here: Character Menu SE - Simonrim patch (not for you, Requiem) and Character Menu SE - Biggie Traits Show in UI (available if you want it).

### What actually changed on disk
- "Vel'dun UI": 620 files before, 620 after. Only 3 files changed content: hudmenu (survival stamina penalty on SkyHUD bars), tutorialmenu (button art/keybind fix), truehud_widgets (masked anyway by "Dragonborn Reskin - TrueHUD"). Plus dialoguemenu, see DBVO.
- "Vel'dun UI Overhauls - Patches": 47 -> 49 files. Only the 2 Spell Hotbar icon files are new; nothing else changed.
- "Vel'dun UI - More Patches": 6 -> 7 files. sleepwaitmenu updated (masked), PlatformButtons added (unused by MWM 2.0.5).
- "Vel'dun UI - Racemenu DIP" and "Vel'dun UI Overhauls - Quickloot": untouched (no new files on Nexus).
- "Vel'dun UI - 21x9": untouched, still disabled in all four profiles (leftover experiment).

### DBVO note (important)
- Vel'dun 1.0.6 removed the DBVO dialogue-menu option ("not needed with DBVO 2 or Dragonborn ReVoiced").
- You run Dragonborn Voice Over 1.1.1, which still needs a DBVO-patched dialogue menu file. Without it Vel'dun's plain dialogue menu would win over DBVO's, and your player voice lines can stop playing.
- Vel'dun's base dialogue menu is byte-identical between 1.0.5 and 1.0.6, so the 1.0.5 DBVO variant is still current. It was carried over as its own small mod: "Vel'dun UI - DBVO Dialogue Patch (1.0.5 carry-over)", placed directly above "Vel'dun UI". Disable/delete it if you ever move to DBVO 2 or Dragonborn ReVoiced.

## 2. Spell Hotbar 0.1.2 + "Option 7 - White" reskin
- Folders: "Spell Hotbar" and "Spell Hotbar - Option 7 - White (Reskins and Presets)", placed at the top of the Wheeler block (above "Wheeler Icon Embellishment"), Option 7 above Spell Hotbar so its font wins.
- Plugin SpellHotbar.esp (light) after "Wheeler - UI.esp", group Interface - User Interface. No record conflicts, all requirements present (JContainers, PapyrusUtil, po3 Extender/Tweaks, I4, OAR, SkyUI). No DAR folder-number collisions.
- Spell Hotbar 0.1.2 is the current main file on Nexus. Spell Hotbar 2 exists as a separate rewrite; Vel'dun ships a patch for that too if you ever switch.
- The Vel'dun Spell Hotbar patch and Option 7 White both replace the same two hotbar frame graphics (empty slot + overlay); Spell Hotbar loads every icon CSV in its images folder and the last one wins (alphabetical: "veldun" after "nordic"). USER DECISION 2026-08-17: "full Vel'dun" - "Spell Hotbar - Option 7 - White (Reskins and Presets)" is now DISABLED in all four profiles (folder kept on disk). Result: Vel'dun frames, Spell Hotbar's own font, no competing files. Re-enable Option 7 only if you want the white frames back (then its font also returns).
- Set your hotbar keys in the Spell Hotbar MCM before playing (defaults are the number keys, which Skyrim's favorites hotkeys also use).

## 3. Time Flies SE 8.2.2 + AE Fishing patch, spell tomes take no time
- Folders: "Time Flies SE", "Time Flies - AE Fishing Patch", "Authoria - Time Flies - No Spell Tome Time", placed at the top of the Gameplay - Survival block (above "Immersive Carcass Carrying - Simple Hunting Overhaul").
- Time Flies' four bundled FISS scripts were not installed - byte-identical copies already come from FISSES.
- Spell tomes: Time Flies has one setting for it, "spell learning" (default 2 hours). The MCM script was byte-patched so the default is 0 hours; 0 means no time passes at all. The slider is still there (0-8 h) if you ever want it back. This lives in its own folder "Authoria - Time Flies - No Spell Tome Time" (patched MCM script + source), above Time Flies. Re-apply after any Time Flies update.
- Time Flies starts DISABLED by design - open its MCM and turn on "Enable Time Flies" on your test session. Its other defaults (crafting, reading, eating, training, etc.) are the mod's own.
- Plugins: TimeFlies.esp (full, 1 slot) then TF-AEFishing Patch.esp (light), both right after "Wounds Overlays Applied.esp" in Gameplay - Early Loaders. They must stay BEFORE Requiem: TimeFlies.esp carries a vanilla copy of the Slaughterfish Egg ingredient and the AE patch a vanilla-ish copy of the CC Slaughterfish food; loaded there they are overridden by Requiem/Alchemy Redone/Food Redone/Authoria CC Fishing patches, which is correct.
- The AE Fishing patch is redundant in this list: its only change (raw-food keyword on the CC Slaughterfish) is already in your Authoria CC Fishing patch. It is installed as asked and does no harm where it sits.
- Plugin count DEEZ CS NUTZ: 251/254 full slots before, 252/254 now (TimeFlies.esp is the only new full plugin). Headroom candidates from the 08-14 vetting list are still available if you need slots.

## 4. Kaidan Wig Slot 44 Patch (your houseCARL patch from 2026-08-15)
- Folder "Kaidan Wig Slot 44 Patch" placed directly above "houseCARL - Authoria - Vorstag Headpart Races" (the mod whose wig record it builds on). Plugin right after "Authoria - Vorstag Headpart Races.esp", group Authoria - Master Patches.
- What it does: moves the Yasha wig (used by Kaidan/Vorstag) from the hair slot to slot 44 and marks it non-playable; also lets the Akaviri race wear the elven helmet.
- It shipped as a full plugin although it is override-only. Flagged light (header bit only, no renumbering) so it costs no slot; original kept beside it as `Kaidan Wig Slot 44 Patch.esp.bak-pre-eslflag-20260817`.
- Verified: it is now the winner for the wig record; no missing masters, no dangling references.
- Other profiles: DEEEZ NUTTZZZ enabled (same anchor). Main and NSFW: inserted DISABLED next to "Authoria - Kaidan Visual Replacer" because "houseCARL - Authoria - Vorstag Headpart Races" is parked/disabled there.

## Other profiles (DEEEZ NUTTZZZ, Main, NSFW)
- All seven mod lines inserted at the same neighbours, enabled where the neighbour is enabled. Plugins added to their plugins/loadorder/plugingroups (Kaidan wig plugin only where the mod is enabled). Full-slot counts after: DEEEZ 244/254, Main 197/254, NSFW 207/254.

## Housekeeping
- MO2 was opened at 4:24 PM while I was working; it auto-parked the DBVO folder at the very bottom, disabled. Fixed. If MO2 is open while I write, it overwrites the profile files - please keep it closed until I say done.
- All eight archives were copied into `C:\1. AUTHORIA\downloads` with .meta files (installed = true, Nexus mod/file ids filled in). Your "Downloads\to add" folder was left untouched.
- Verified: nothing new sits in the FWMF / LOD-output blocks or after "Authoria - Output - Synthesis Gameplay.esp" in any profile.
- No Reqtificator/Synthesis rerun is needed for these additions (none of the new plugins touch records those tools patch; the wig record is not in RFTI).
