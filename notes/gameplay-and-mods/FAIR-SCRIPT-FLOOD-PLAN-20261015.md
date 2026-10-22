# Wanderer's Fair: arrival script flood - plan (2026-10-15)

Follow-up to `FAIR-FPS-20261014.md`, section "In-game check 2026-10-14 16:05".
Status: **INSTALLED 2026-10-15 04:06** (all three, on your OK), MO2 and the game closed at every write. Verified after
install: SkyPatcher reads the INI (gated on the fair plugin), a live pre/post replay strips exactly the one ability from
fair NPCs, the SOS patch carries the new condition at index 0 as an AND with its ESL flag kept, the OBody config parses
with the two new entries. No load-order change was needed (the SOS patch already loads after the fair plugin in every
profile). Originals: `_backups\2026-10-15 - Fair script flood\`. In-game after-check still owed (new game).

## What the logs say (before)

Measured with `_tools\fair-script-flood\measure.py` on the 16:05 session logs. Arrival = the first Walk With Me
scan with 120+ actors in high process (16:05:40, 213 actors). Window = the next 70 seconds.

| measure | before |
|---|---|
| Papyrus stack dumps in the window | 565 |
| top of those stacks: Requiem spell rescaling / OBody / fair keeper / SOS | 212 / 151 / 63 / 41 |
| `REQ_PersistentSpellRescaling.OnEffectStart` instances | 213 |
| `obodyngscript.OnActorGenerated` instances | 156 |
| `SOS_ActorMagicEffect_Script.OnEffectStart` instances | 53 |
| OBody "apply preset to Fair ..." calls | 126 |
| SOS per-actor lines for fair actors | 31 |
| crowd cull "switched" line | 70 s after arrival |

## What each burst member is, and the lever for it

**1. Requiem's persistent spell rescaling (213 instances, the biggest).**
The Reqtificator stamps the ability `RFTI_NPC_PersistentSpellRescaling` on every NPC; it is a fixed entry in the
Reqtificator's rules file with no condition, so the Reqtificator cannot be told to skip the fair. The script removes
and re-adds up to 7 perk-scaled spells (ranged combat training x3, Agility, armor padding x3) on load.
Checked against the live load order: **none of the 225 fair NPCs carries any of those 7 spells.** On them the ability
does nothing except queue 213 script instances on arrival. Every fair NPC carries exactly four Reqtificator abilities
(this one, Crossbow Stagger, Exhaustion Controller, Base Attack Speed); the other three never appear in the dumps.
Lever: a SkyPatcher NPC line that removes that one ability from every NPC carrying the `SkyrimFairNPC` keyword.
All 225 carry the keyword on the record itself, none inherits spells from a template, and the removal is applied to
the winning record at runtime, so it survives every Reqtificator rerun and never touches the RFTI output.
Replayed through houseCARL's SkyPatcher overlay on a female and a male fair NPC: exactly one spell removed, the
other three abilities and all 45 perks untouched.

**2. OBody (156 instances + 126 native body passes).**
OBody runs a morph pass per fair actor on load and fires a Papyrus event per actor. Lever: add `SkyrimFair.esp` to
both plugin blacklists in the Authoria OBody distribution config. OBody's source matches that list against the
actor's first source file, which for every fair actor is the fair plugin, so the Requiem override does not get in the
way. Consequence: fair NPCs keep the body their outfits were built on (your zeroed builds), with no preset applied.
Lighter alternative if you want to keep presets on them: turn off OBody's legacy StorageUtil writes in the settings
loader. That removes only the Papyrus half for every NPC in the game and is a global change, so it is not staged.

**3. Schlongs of Skyrim (53 + 31 instances).**
SOS reaches NPCs through a cloak on the player; the cloak's per-NPC effect is already overridden by the Authoria
patch `Authoria - SOS Custom Races.esp` (52 OR-ed race conditions). Lever: insert one more condition at the front of
that list, `HasKeyword SkyrimFairNPC == 0` on the subject, as an AND. Fair NPCs then never receive the SOS actor
spell. Consequence: the 143 male fair NPCs get no schlong; they are never undressed at the fair. The patch loads
after the fair plugin in every profile that has it, so taking the fair plugin as a new master needs no reordering.
Dry run passed (53 conditions, one master added). The SFW main profile has no SOS and is unaffected.

**Left alone.** `REQ_MassEffectArmor` (7 instances, 35 "on None" errors) is carried by the race records, not the
fair NPCs, so a per-NPC removal cannot reach it; its errors come from actors the cull disables mid-effect and
should shrink once the cull fires on time. The fair's own keeper script (63) is the fair working as designed.
The Reqtificator fork's "already reqtified" skip keyword would strip every Requiem trait from the fair NPCs, not
just this one ability, and needs a rerun; rejected.

## Exact edits (staged under `_tools\fair-script-flood\staging\`)

1. **New file** `mods\houseCARL - Authoria - Patch - Holidays and Fair - Requiem\SKSE\Plugins\SkyPatcher\npc\Authoria - Wanderers Fair\SkyrimFair.esp.ini`
   (that mod is enabled in all 8 profiles; the file name gates it on the fair plugin being active)
   ```
   filterByKeywords=SkyrimFair.esp|00171E:spellsToRemove=Requiem.esp|AD3977
   ```
2. **Edit** `mods\Authoria - OBODY Distro\skse\plugins\OBody_presetDistributionConfig.json`
   add `"SkyrimFair.esp"` to `blacklistedNpcsPluginFemale` and `blacklistedNpcsPluginMale` (2 lines; staged copy parses).
3. **Edit in place** `mods\Authoria - Ostim tweaks and Patches\Authoria - SOS Custom Races.esp`
   magic effect `SOS_SetupNPCMagicEffect` (0012DD:Schlongs of Skyrim.esp): insert condition 0 = HasKeyword
   `SkyrimFairNPC` (00171E:SkyrimFair.esp) == 0, run on subject, no OR flag. Adds master `SkyrimFair.esp`.
   The op is in `staging\SOS\sos_fair_exclusion_ops.json`; applied with houseCARL in place, after a backup.

Backups go to `_backups\2026-10-15 - Fair script flood\` (the original JSON and the original SOS patch).
Rollback = delete the INI, copy the two backups back.

## After-check (new game, visit the fair once)

Run `measure.py --label after` on the fresh logs. Pass =
- `REQ_PersistentSpellRescaling.OnEffectStart` absent from the window (was 213),
- OBody "apply preset to Fair ..." = 0 (was 126) and no `obodyngscript` stacks on fair actors,
- SOS per-actor lines for fair actors = 0 (was 31),
- stack dumps in the window well under 565 and the cull's "switched" line well under 70 s after arrival.
The remaining cost after this is the actor load itself (game thread 114-194 ms frames) and the crowd; that is the
crowd-cap lever, not scripts.
