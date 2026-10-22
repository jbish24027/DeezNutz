# Bobbing presets + Companions giant — 2026-08-30

Backups: `_backups\2026-08-30 - bobbing-presets-giant\` (all six `modlist.txt` before the edit).

## 1. Authoria - Requiem - Companions Giant

The giant Aela, Farkas and Ria fight outside Whiterun was dying too fast. It is
`C00GiantForWhiterunBattle` (`0C97D1`), placed as `C00GiantREF`, and the Reqtificator owns it.

Measured against `EncGiant02`, which is what every ordinary giant in Skyrim is:

| | Companions giant | ordinary giant |
|---|---|---|
| Level | 30 | 70 |
| One-handed / two-handed | 24 / 25 | 72 / 73 |
| Block | 18 | 50 |
| Light armor / heavy armor | 18 / 12 | 50 / 28 |
| Race base health + offset | 1000 + 3000 = 4000 | 250 + 1000 = 1250 |
| Race unarmed damage | 2 | 60 |
| Race attack damage mult | 0.1 | normal |

Requiem built it as a training dummy. Three times a real giant's health, a level-30 armour
profile, and attacks that land at a tenth damage. Health was never the weak stat.

**Nexus mod 60502 "Tougher Companions Giant" was not installed.** It is a single RACE override of
`C00GiantOutsideWhiterunRace` setting health 100 -> 1000, a number Requiem already sets. Loaded
after Requiem it strips Requiem's 2 keywords, 2 abilities and rewritten attack data; loaded before,
Requiem wins and it does nothing.

Shipped instead: one SkyPatcher line at
`SKSE/Plugins/SkyPatcher/npc/Authoria - Companions Giant/Skyrim.esm.ini`

    filterByNpcs=Skyrim.esm|0C97D1:changeStats=healthMult=2

Doubles health to 8000, changes nothing else — level, skills, the 45 Reqtificator perks and the 4
Requiem abilities are untouched. Runtime patch, so it survives a Reqtificator rerun and costs no
plugin slot. Enabled in all six profiles. Verified with `housecarl_skypatcher_layer`: applied,
0 set-conflicts, 0 dead writes, 0 duplicates, not a no-op.

**If it still dies too fast,** the next dial is the armour gap, not more health:
`changeSkills=block=50,lightarmor=50,heavyarmor=28`.

## 2. Authoria - Bobbing Framework Presets - Additions

55 configs pulled from **Bobbing Framework - My Presets** (Nexus 189894 v1.1, Blackread). Only
objects with no existing bobbing config anywhere in the load order — nothing already bobbing was
touched, and the official configs stay as they are.

| Source | New configs |
|---|---|
| Vanilla | 25 |
| Wyrmstooth | 11 |
| CFTO | 7 |
| Ivy's Riften Docks Overhaul | 4 |
| 3DNPC | 3 |
| JK's Solitude Outskirts | 2 |
| JK's Raven Rock | 1 |
| JK's Riften Outskirts | 1 |
| CFTO Tel Mithryn (not-animated variant) | 1 |

The vanilla 25: Japhet's Folly (6 barrels, 3 rowboats, 2 ships), Broken Oar Grotto x2, Castle
Volkihar, Icewater Jetty, Faldar's Tooth, Gyldenhul Barrow, Northshore Landing, EEC Warehouse,
Hela's Folly, Windhelm EEC longboat, the Katariah, Goldenglow, Riften docks rowboat 4, Solitude
docks rowboat 4.

**Dropped from the FOMOD.** Holds, Midwood Isle, Maslea, the Great Cities, Port City of Windhelm,
Better Docks, More Ferries, Redbag's, Open Cities, Raven Rock Reborn, Spaghetti's Solstheim and the
rest all gate on plugins not in this order. The JK's Skyrim branch resolves to "No" and its three
applicable configs were already covered. **Armors of the Velothi skipped deliberately** — the pack
targets `Armors of the Velothi Pt2.esl` and this order runs the `.esp`, so the FormID would not
resolve.

Two of the 55 (`RiftenDocksRowboat4`, `WindhelmEECLongboat`) are still in the 1.x config schema;
the author did not update them. 2.0 reads the old format, so they work on the older motion model.

### Profile states — read before assuming

Install position: line ~1424, Gameplay - Frameworks group, directly above
`Authoria - Bobbing Framework Configs - Modded Boats`. JSON only, no plugin.

| Profile | Bobbing Framework | New mod |
|---|---|---|
| DEEZ CS NUTZ | 2.0 | ENABLED |
| DEEZ CS NUTZ - PBR | 2.0 | ENABLED |
| PICTA EXPERIMENT | 2.0 | ENABLED |
| Authoria - Requiem Reforged - Main | 1.2, whole stack off | inserted DISABLED |
| Authoria - Requiem Reforged - NSFW | 1.2, whole stack off | inserted DISABLED |
| DEEEZ NUTTZZZ | 1.2, stack on | inserted DISABLED |

The presets require Bobbing Framework 2.0+. The three CS profiles have it because
`[NoDelete] Bobbing Framework` (2.0) sits at priority ~50 and outranks the plain 1.2 copy at ~1425.
The other three profiles have no `[NoDelete]` mods at all, so they are genuinely on 1.2 — enabling
the presets there would feed 2.0-schema configs to a 1.2 parser. To turn them on, add the two
`[NoDelete] Bobbing Framework` mods to those profiles first.

Verified: 55 files parse, 0 filename collisions with the three existing config mods, 0 FormID
overlap with anything already bobbing, all 55 target plugins active.

## Also found (not acted on)

`mods\UBE Serana - NPC Replacer\SKSE\Plugins\SkyPatcher\npc\OriSeranaUBE\OriSeranaUBE.esp.ini` has
two unparsable lines and is being skipped entirely: line 1 uses `#` as a comment marker (SkyPatcher
uses `;`), line 2 uses `filterByNPCs` instead of `filterByNpcs`. A separate
`houseCARL - Authoria - Patch - Serana UBE Face` file may already cover the intent — needs checking
before fixing.
