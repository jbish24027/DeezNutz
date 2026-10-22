> **SUPERSEDED 2026-08-28.** The filename rule used here was wrong - it did not strip the
> trailing `(Persuade)`-style tag, so the gap count is roughly 4x too high. See
> ELEONORA-DBVO-PACKAGE-20260828.md for the corrected audit.

# Eleonora (DBVO) — mods still missing player lines

Audited 2026-08-28 against the **DEEZ CS NUTZ - PBR** profile.

## Numbers

- 4102 plugins scanned (4042 you can see in MO2 plus the 60 always-on ones). 56,888 live
  player-menu strings across the load order.
- 41,616 Eleonora `.fuz` files already on disk.
- **13,148 lines still have no recording, across 191 mods / 242 plugins. 13,048 of them unique.**

## Deliverables

**Topic files to feed the generator** —
`D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\z. DBVO crap\topic files missing 20260828\`
- 242 × `topic files<Plugin>.txt`, same format as the ones you made by hand: CP1252, CRLF,
  sorted and de-duplicated under Windows collation, one line per topic. Only the lines with
  no `.fuz` yet.
- `_ALL MISSING deduplicated.txt` — every line once, 13,048 lines. A filename only ever
  needs recording once, so use this if you are paying per character.
- `_INDEX.txt` — per-plugin counts, plus the plugins that are already fully covered.

**Line-by-line CSV** — `ELEONORA-DBVO-MISSING-LINES-20260828.csv`
(`mod, plugin, target_filename, text`).

**Scripts** — `_tools\eleonora-dbvo\`. Re-run `winners.py` then `gen2.py` after any mod update.

## How the lines were pulled

I reimplemented your `DBVO-SSEEdit-Topic-Extract.pas` in Python and checked it against your five
hand-made topic files. All five reproduce line for line, sort order included —
ImprovedCompanionsBoogaloo 409, BSCyrodiil 25, LOTD 0, Wyrmstooth 11, Sanguine's Trade 234.

Four things the plain script does not do, which I added:

**Plugin text is CP1252, not UTF-8.** Ellipses and curly quotes are single bytes in the record.
Reading them as UTF-8 corrupts the filename.

**Lines are filed under the plugin that wins the record.** A topic rewritten by a
`DBVO Fix - *.esp` is listed under the fix, not the original mod, because the fix's text is what
the menu actually shows. 239 SDA topics go to `DBVO Fix - SDA.esp`, 1985 Amorous Adventures
topics to `AmorousPlayerDialogueRewritten.esp`, and Vigilant, Moonpath and Olenveld all lose
blocks to their patches. Recording the original text would produce files DBVO never asks for.

**Lines are trimmed before the filename is built.** Checked rather than assumed: of 235 topics
carrying leading or trailing whitespace, 78 have a `.fuz` under the trimmed name and **zero**
under the raw name. So `"Begone.\r\n"` is `Begone..fuz`. Ten topics carry a stray `\r\n` or tab
that would otherwise have split your file into bogus extra lines.

**The always-on plugins are included.** MO2 leaves Skyrim.esm, the DLC, all 55 Creation Club
plugins and `_ResourcePack.esl` out of plugins.txt entirely, so a naive read of that file drops
60 plugins. Their strings live inside BSAs rather than a loose `Strings\` folder, so the reader
pulls them out of the archive. That is where 336 of the lines below come from: Skyrim.esm 181,
Dragonborn 35, Dawnguard 28, HearthFires 26, HearthfireMultiKid 23, Update 3, and 190 across
15 Creation Club plugins.

One SDA topic has a line break in the middle of it. No legal Windows filename exists for it, so
it cannot be voiced at all. It is named at the bottom of `_INDEX.txt` rather than dropped quietly.

## Two different kinds of gap

A mod at **0-20% covered** was never in the pack — that is real new work.
A mod at **90%+** is one the pack supports but that has updated since; only the new lines are left.

## About FDE

You were half right. The base FDE followers are mostly covered, because the pack lists them.
What leaked through is update drift, not missing support: Brelyna 34, Aranea 32, Aela 18 across
both plugins, Mjoll 12, Jenassa 10, then single digits on Sapphire, Marcurio, Saadia, Illia,
Erik, Borgakh, Uthgerd. Eola, Faralda, Roggi and Jordis are clean. Every FDE cross-patch
(Aela × Auri/Lucien/Remiel/Xelzaz, Mjoll × Auri/Remiel, Brelyna × Lucien/Auri, the four Inigo
ones) adds banter only — no player lines, nothing to do.

The bigger fish is **Improved Follower Dialogue - Lydia**: 357 lines, still the job from
2026-08-21. The folder you made for it (`Authoria - Eleonora - IFD Lydia`) ended up holding
217 Sanguine's Trade recordings and only 36 of the IFD manifest.

## Big jobs (100+ lines)

| Missing | Live topics | Covered | Mod |
|---:|---:|---:|---|
| 1741 | 1985 | 12% | Amorous Adventures - Player Dialogue Rewritten |
| 1703 | 1853 | 8% | Flint the Minotaur |
| 1026 | 1605 | 36% | Glenmoril - English Translation SE |
| 680 | 772 | 11% | M'rissi's Tails of Troubles SE |
| 595 | 1493 | 60% | Beyond Skyrim - Bruma SE - Main |
| 537 | 2346 | 77% | Serana Dialogue Add-On |
| 467 | 592 | 21% | Immersive World Encounters SE |
| 445 | 539 | 17% | Amorous Adventures for OStim Standalone - Patch and Fixes |
| 357 | 458 | 22% | Improved Follower Dialogue - Lydia |
| 314 | 838 | 62% | Eleonora Female Nord Dbvo Pack With Patches |
| 301 | 442 | 31% | The Forgotten City |
| 288 | 415 | 30% | Ostim Resolutions (Solutions 2.0) Standalone |
| 262 | 626 | 58% | Heart of Ice - Astrid. Custom Voiced Follower |
| 242 | 253 | 4% | Fair Rebalancing Of Transit Tariffs - Active Graph Evaluation |
| 223 | 302 | 26% | Bards Reborn Student of Song |
| 223 | 351 | 36% | Unslaad Voiced - English Addon SE |
| 181 | 4178 | 95% | <Stock Game> |
| 169 | 414 | 59% | Thogra gra-Mugur - Orc Follower and Quest |
| 165 | 254 | 35% | Authoria - xEdit Output - NSFW |
| 164 | 1870 | 91% | Unofficial Skyrim Special Edition Patch |
| 147 | 355 | 58% | FAMILY LIFE - Immersive Dialogue Expansion - Hearthfire |
| 131 | 325 | 59% | Creation Club - Cleaned Masters |
| 121 | 132 | 8% | Immersive Dialogue Expansion - Thalmor |
| 104 | 118 | 11% | Olenveld |

## Medium (20-99 lines)

| Missing | Live topics | Covered | Mod |
|---:|---:|---:|---|
| 92 | 1686 | 94% | Cleaned Base Game Masters |
| 87 | 123 | 29% | Skyrim Realistic Conquering - All In One |
| 84 | 105 | 20% | The Rot Below |
| 80 | 109 | 26% | The Frozen Heart - Quest Mod |
| 78 | 154 | 49% | CFTO - Fixes and Winterhold |
| 77 | 97 | 20% | Immersive Dialogue Expansion - Dawnguard and Vigilants |
| 68 | 839 | 91% | Gore |
| 62 | 74 | 16% | A Friend in Mead - Quest Mod |
| 62 | 94 | 34% | Moonpath to Elsweyr - Unofficial Patch |
| 57 | 68 | 16% | The Tools of Kagrenac |
| 56 | 3943 | 98% | Immersive Kaidan AIO - rerun |
| 55 | 61 | 9% | Olenveld - Tweaks and Fixes |
| 51 | 783 | 93% | Ashe - Crystal Heart |
| 51 | 86 | 40% | Moonpath to Elsweyr SSE |
| 45 | 55 | 18% | Seeking The Cure - A Rising At Dawn Quest Overhaul |
| 45 | 100 | 55% | Simple Hunting Overhaul |
| 44 | 61 | 27% | CC Farming - Tweaks and Enhancements |
| 44 | 73 | 39% | Thieves Guild Alternative Endings |
| 43 | 654 | 93% | VIGILANT - English Translation SE (Voiced) |
| 42 | 51 | 17% | Fists of Fury |
| 40 | 51 | 21% | The Heart of Dibella - Quest Expansion |
| 37 | 43 | 13% | An Evening With Angi |
| 37 | 116 | 68% | College of Winterhold - Quest Expansion |
| 37 | 103 | 64% | Horses Are Your Friends |
| 36 | 121 | 70% | Everdamned |
| 34 | 61 | 44% | Follower Dialogue Expansion - Brelyna Maryon |
| 33 | 434 | 92% | Favor Quests Separated |
| 33 | 200 | 83% | Hearthfire Multiple Adoptions Expanded |
| 32 | 88 | 63% | Follower Dialogue Expansion - Aranea Ienith |
| 29 | 40 | 27% | Yoana - Custom Voiced Follower |
| 27 | 30 | 10% | Above all Else - Lovecraft Inspired Quest |
| 27 | 416 | 93% | Redcap |
| 27 | 35 | 22% | The Taste of Death - Quest Addon |
| 27 | 1911 | 98% | Val Serano - Pirate Follower and Quest Adventure |
| 26 | 195 | 86% | SIRENROOT - Deluge of Deceit 1.3 |
| 26 | 170 | 84% | Skyrim Extended Cut - Saints and Seducers |
| 25 | 28 | 10% | Immersive Dialogue Expansion - Jorrvaskr (Companions) |
| 25 | 66 | 62% | Simple Fishing Overhaul - Improved Quest Dialogue |
| 23 | 148 | 84% | Hearthfire Multiple Adoptions |
| 22 | 440 | 95% | DAC0DA - English Translation SE |
| 22 | 10450 | 99% | Interesting NPCs 3DNPC - 4.54 Update |
| 22 | 1193 | 98% | Xelzaz - Custom Fully Voiced Argonian Telvanni Follower |
| 21 | 23 | 8% | Wait Carriage in Inns - Fast Travel Improvement |

## Small (3-19 lines)

| Missing | Live topics | Covered | Mod |
|---:|---:|---:|---|
| 19 | 769 | 97% | Remiel-Custom Voiced Dwemer Specialist and Companion |
| 19 | 66 | 71% | Song of the Green (Auri Follower) - Vigilant |
| 19 | 115 | 83% | The Gift of Saturalia - A Quest for the Holidays |
| 18 | 20 | 10% | Caught Red Handed - Quest Expansion |
| 18 | 478 | 96% | Follower Dialogue Expansion - Aela the Huntress |
| 18 | 21 | 14% | It Came from Akavir - Quest Mod |
| 18 | 374 | 95% | Wyrmstooth |
| 17 | 66 | 74% | DiegeticTravel |
| 16 | 20 | 20% | Before the End - Quest Mod |
| 16 | 27 | 40% | Thieves Guild Requirements SE |
| 15 | 36 | 58% | Immersive Dialogue Expansion - Stormcloaks |
| 14 | 15 | 6% | Banters with Flint |
| 14 | 14 | 0% | Morskom Estate |
| 14 | 31 | 54% | Paarthurnax - Quest Expansion |
| 13 | 863 | 98% | Legacy of the Dragonborn V6 |
| 12 | 50 | 76% | Follower Dialogue Expansion - Mjoll the Lioness |
| 12 | 18 | 33% | Ill Met by Moonlight - Dialogue Expansion |
| 12 | 25 | 52% | The Cursed Tribe - Quest Expansion (TCTQE) |
| 12 | 162 | 92% | The Gray Cowl of Nocturnal - 10th anniversary |
| 11 | 12 | 8% | Carriages and Stables Dialogue Bundle - Voiced Addon |
| 11 | 158 | 93% | Immersive Rejections |
| 10 | 22 | 54% | At Your Own Pace - Thane Overhaul |
| 10 | 12 | 16% | Face Sculptor Expanded |
| 10 | 507 | 98% | Follower Dialogue Expansion - Jenassa |
| 10 | 87 | 88% | Headhunter - Bounties Redone |
| 9 | 11 | 18% | Become a Bard |
| 9 | 11 | 18% | Gravewind |
| 9 | 9 | 0% | Snazzy Misc Locations |
| 8 | 8 | 0% | A Friend in Mead - Whispers of the Depths |
| 8 | 47 | 82% | Penitus Oculatus |
| 8 | 8 | 0% | Why I Came to Skyrim - Origin Stories |
| 7 | 15 | 53% | A Lovely Letter Alternate Routes |
| 7 | 8 | 12% | Carriages and Stables Dialogue Bundle |
| 7 | 17 | 58% | House of Horrors - Quest Expansion |
| 7 | 17 | 58% | Talos' Tease |
| 7 | 109 | 93% | The Forsworn Conspiracy - Quest Expansion |
| 6 | 15 | 60% | Blood on the Ice Redux SE |
| 6 | 9 | 33% | Devotion |
| 6 | 6 | 0% | Imperial Mail - Post and Banking Service |
| 6 | 35 | 82% | Infiltration - Quest Expansion |
| 6 | 8 | 25% | Requiem - Minor Arcana |
| 6 | 27 | 77% | Save the Icerunner - Lights Out Alternate Routes |
| 6 | 61 | 90% | The City of Crossed Daggers - Riften Expansion |
| 6 | 20 | 70% | The Only Cure - Quest Expansion |
| 5 | 5 | 0% | Amorous Adventures - MCM |
| 5 | 5 | 0% | Auri - 3DNPC Patch |
| 5 | 24 | 79% | Authoria - xEdit Output |
| 5 | 6 | 16% | CC Tundra Homestead - Tweaks and Enhancements (THTE) |
| 5 | 8 | 37% | Creation Club - Alternative Armors - Ebony Plate |
| 5 | 8 | 37% | Creation Club - Alternative Armors - Orcish Scaled |
| 5 | 5 | 0% | Extended Hireling Dialogue - Belrand |
| 5 | 30 | 83% | Innocence Lost - Quest Expansion |
| 5 | 7 | 28% | OStim Community Resource |
| 5 | 5 | 0% | Schlongs of Skyrim - NG |
| 4 | 6 | 33% | A new Debt Alternate Routes |
| 4 | 14 | 71% | Authoria - Basic Wenches OStim |
| 4 | 51 | 92% | Follower Dialogue Expansion - Sapphire (FDE) |
| 4 | 9 | 55% | Jimothy Follower SE |
| 4 | 312 | 98% | Sanguine's Trade - An Economy Mod |
| 4 | 9 | 55% | Simply Knock SE |
| 3 | 3 | 0% | Amorous Adventures OStim Standalone - Player Dialogue Rewritten Patch |
| 3 | 3 | 0% | Civil War Champions - Reduced Cut |
| 3 | 3 | 0% | Drengin's Blue Palace Terrace |
| 3 | 35 | 91% | Follower Dialogue Expansion - Marcurio |
| 3 | 3 | 0% | Homes Under the Warhammer - Shadowfoot Sanctum |
| 3 | 8 | 62% | Legacy of the Dragonborn Creation Club Patches - rerun |
| 3 | 12 | 75% | Miscellaneous Quests are Favors |
| 3 | 139 | 97% | Missives - Worldspace Additions |
| 3 | 10 | 70% | Nilheim - Misc Quest Expansion |
| 3 | 15 | 80% | NPCs React To Necromancy |
| 3 | 12 | 75% | Skyrim's Got Talent - Improve As a Bard |
| 3 | 21 | 85% | The Whispering Door - Quest Expansion |

## One or two lines each

Auri - VIGILANT commentary patch tweaks, Authoria - Requiem Patches, Buyable Golden Claw, Carriage Ferry Travel Overhaul (CFTO) Bittercup Fix, Follower Dialogue Expansion - Erik the Slayer, Follower Dialogue Expansion - Illia, Follower Dialogue Expansion - Saadia, Kaidan 2, Legacy of the Dragonborn Patches (Official) - rerun, Love Is In The Air - Dynamic NPC Marriages, Quest - Baba Yaga and the Labyrinth, Quest Fixes, Radiance, Skybound Underhang Camp, Spooky Philter of the Phantom, Talos' Tease - Ostim, Unmasking Sybille, Adventurer's Start - An Alternate Perspective Addon, Adventurer's Start - An Alternate Perspective Addon - Bruma, Alternate Perspective - Voiced Addon, Amorous Adventures OStim Standalone - OStim Sequences, Ashe - Crystal Heart - SDA, At Your Own Pace - College of Winterhold, Authoria - Papyrus - A New Debt Alternate Routes Fix, Authoria - Papyrus - Quest Fragment Patches, Authoria - Reqtificator and Requiem Tweak, Beyond Skyrim - Bruma SE - LOTD, Bittercup - Tweaks and Enhancements, Calling the Watchmaker - Lovecraftian Inspired Quest, Caught Red Handed - Quest Expansion - OStim Patch, Follower Dialogue Expansion - Borgakh the Steel Heart, Follower Dialogue Expansion - Uthgerd the Unbroken, Harvest Your Blood for Septimus, Heart of Ice - Astrid - OStim Integration, Honed Metal - Isobel Patch, houseCARL - Authoria - Patch - IWE No Dragon Events, Interesting Follower Requirements for 3DNPCs, Kidmer - Adoptable Elf Children, Missives - Voice and Quest Expansion, NPCs React To Invisibility, OISeeYouMasturbating, Race Compatibility Dialogue - Gore, Riverwood Trader Is A Mess, Rob's Bug Fixes - TGC Kynesgrove, Silence is Golden, Simply Order Summons, Skyforge Immersion Addon, The Forgotten City - Good Ending Tweaks, The Hunt for the Spectre - Elden Ring Inspired Quest, Triumvirate - Mage Archetypes, Unofficial Skyrim Modder's Patch, Whispers of the Depths - Quest Mod
