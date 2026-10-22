# Devotion 1.5.0 -> 1.5.0e (2026-08-18)

Applied to the active profile DEEZ CS NUTZ. Save-safe hotfix, no plugin changes, no profile edits.
Backup taken first: `C:\1. AUTHORIA\backups\devotion-preupdate-20260818\` (both Devotion mod folders +
all four profiles' modlist/plugins/loadorder/plugingroups), byte-count verified.

## What this release changes

Author's own changelog for prerelease e, all behavioural:

- Drinking water no longer counts as revelry. Survival-mod water bottles were being read as alcohol and
  awarding Sanguine devotion.
- Skinning and looting no longer builds a Hunt. Pelts, hides and leather from any kill were being read as
  Hircine trophies.
- A Daedric Prince now offers a pact rather than claiming you. Reaching a Prince's threshold presents a
  choice to accept, wait or refuse, and rising toward a Prince no longer overrides an active patron.
  Daedric devotion also keeps to the daily pace like every other path.
- The Book of Days now shows your Daedric Prince as patron once the pact is accepted.

## FOMOD choices — reconstructed and proven

The 1.5.0 archive is not on disk (downloads only had 1.0.2 and 1.0.4), so the choices were reconstructed
from the installed files against the 1.5.0e archive, exactly as was done for Vel'dun.

Result: **63 of 80 options selected.** The 17 not selected each require a quest mod that is not active in
this load order, so nothing is missing:

Heart of the Reach, Legends of Aetherium, Moon and Star, Project AHO, Sleepwalking Into A Nightmare,
The Sinister Seven, There Is No Umbra - Chapter III, Defeat the Dragon Cult, Destroy the Acolyte Priests,
Destroy The Dark Brotherhood, Return Aegisbane, Revealing Rune, Thieves Guild For Good Guys,
Khajiit Will Follow, Merlin the Corgi, Sa'chil, The Thalmor's Shadow - Taliesin.

Cross-checked every option's `fileDependency` esp against `plugins.txt` plus the implicit base/CC masters:
- options APPLICABLE but not installed: **0**
- options installed whose required esp is not active: **0**

Choice set saved to `_tools\mod-install-helpers\veldun-choices\choices_devotion.txt`.
Verification before writing anything: simulating those 63 choices against the installed folder gave
335 files vs 335 installed, **0 only-in-sim, 0 only-in-installed, 41 content differences** — i.e. a
perfect structural reconstruction where only the hotfixed files differ.

## The 41 changed files — all in the required core

Nothing under any quest-patch option changed. The hotfix touches only:

- `Devotion.esp` (657,998 -> 658,913 B, still a FULL plugin)
- `CHANGELOG.txt`
- `PDV_ItemRecognition_KID.ini` (2,500 -> 3,530 B)
- `Scripts\PDV__ManagerQuest.pex` + source
- `Scripts\PDV_DaedricPath_*.pex` — all 17 Princes — plus `PDV_DaedricPathBase`, and sources
- `Scripts\PDV_MCM.pex` + source

That maps one-to-one onto the changelog. High confidence this is exactly what it claims to be.

### The KID change is the behavioural one worth knowing

`PDV_ItemRecognition_KID.ini` diff:

- Added a name exclusion so `*Ale` / `*Mead` / `*Wine` / `*Brandy` no longer match "Bottle of Water".
  The author's comment names SunHelm's water-bottle keyword editor-IDs (`_SH_MeadWATERBottleKeyword`)
  as the cause. You run SunHelm, so this fix is live for you.
- Two whole distribution lanes are now **commented out**, described by the author as "never
  design-approved" and leaking through vendor keywords:
  - Zenithar trade goods (`*Ingot`, `*Ore`, `*Gem`, `*Circlet`, `*Necklace`, `*Ring`)
  - Hircine hunt trophies (`*Pelt`, `*Hide`, `*Claw`, `*Fang`, `*Tusk`, `*Antler`)
  Disabling the Hircine keyword also makes the paired Kyne credit inert. Both are reversible by
  uncommenting.

## Devotion - PatchHub — resolved, no action taken

`Devotion - PatchHub` is the bespoke package installed 2026-07-16 from
`PDV_QuestModPatches_FOMOD_20260716.zip` (a path under `C:/Users/Heisen/Downloads/`, so shared by the
author rather than downloaded by you). Full intersect against everything 1.5.0e can install:

- 40 files total. **38 are also provided by official 1.5.0e options you already have selected**, and the
  official copies are different (newer). Those 38 are the ten `PDV_QRM_*.json` reaction channels, the nine
  `PDV_TIF_*` dialogue-fragment scripts with sources, and ten docs.
- **Only 2 files are unique to it**: `PDV_Patch_Authoria_QuestMods.esp` and one doc.
- That merged esp carries 21 records (3 Quest, 9 DialogTopic, 9 DialogResponses) and masters
  Slays-Many-Beasts, War's Folly and Once We Were Here. The official archive ships a dedicated
  ESL-flagged patch for each of those three, plus two more (AFDI, Daedric Shrines AIO). So it is fully
  superseded and the official set covers more.

**You already migrated off it.** In DEEZ CS NUTZ the mod is disabled and `PDV_Patch_Authoria_QuestMods.esp`
is not in `plugins.txt`; the five official patches are active instead. Verified through the VFS: every one
of those 38 paths resolves to the `Devotion` folder, single provider, no contention. That matches the new
README, which says explicitly not to keep any older Devotion compatibility package alongside this one
because they overwrite Devotion's core scripts.

### Open item (reported, not changed)

In the other three profiles PatchHub is still **enabled** and `PDV_Patch_Authoria_QuestMods.esp` is still
**active**, while the five official patch plugins are not:

| profile | PatchHub mod | merged esp |
|---|---|---|
| DEEZ CS NUTZ (active) | disabled | not active |
| DEEEZ NUTTZZZ | enabled | active |
| Requiem Reforged - Main | enabled | active |
| Requiem Reforged - NSFW | enabled | active |

Because PatchHub sits one line above `Devotion` in those modlists, it would **win** those 38 paths and
serve stale reaction channels and fragment scripts over the 1.5.0e ones. Per the author's README that
breaks core scripts. Those profiles are not the one you play, so nothing was changed without asking.

## Plugins and load order

Plugin set before and after is identical, so **no modlist, plugins.txt, loadorder.txt or plugingroups.txt
edits were needed in any profile**:

`Devotion.esp` (full) + `PDV_Patch_AFDI.esp`, `PDV_Patch_DaedricShrinesAIO.esp`,
`PDV_Patch_OnceWeWereHere.esp`, `PDV_Patch_SlaysManyBeasts.esp`, `PDV_Patch_WarsFolly.esp` (all five
ESL-flagged, byte-identical between 1.5.0 and 1.5.0e).

Plugin-cap impact: **none.** Still 252/254 full slots on DEEZ CS NUTZ.

Integrity sweep on all six: **0 dangling references, 0 missing masters, 0 unreadable records.**

The README's ordering rules are all satisfied as-is:

| plugin | index | after Devotion.esp (1923) | source plugin | after source |
|---|---|---|---|---|
| PDV_Patch_AFDI.esp | 1924 | yes | Aetherium Forge Destroys Items.esp (425) | yes |
| PDV_Patch_DaedricShrinesAIO.esp | 1925 | yes | n/a | n/a |
| PDV_Patch_OnceWeWereHere.esp | 1926 | yes | Once We Were Here - Quest Mod.esp (875) | yes |
| PDV_Patch_WarsFolly.esp | 1927 | yes | War's Folly.esp (873) | yes |
| PDV_Patch_SlaysManyBeasts.esp | 1928 | yes | Slays-Many-Beasts Quest Mod.esp (870) | yes |

## Other checks

- Both `.seq` files shipped and are present: `Seq\Devotion.seq`, `Seq\PDV_Patch_AFDI.seq`. A stale seq
  would break start-enabled quests, so this matters after an esp change.
- `DevotionPrismaBridge.dll` present (433,152 B). PrismaUI is active in this profile
  (`PrismaUI 1.5.0` + `Prisma UI - Next-Gen Web UI Framework`), so the panel will work.
- No player-written Devotion state in `overwrite\` — nothing of yours was at risk of being clobbered.
  All `StorageUtilData\PlayerDevotion\` files are static data shipped by the mod.
- Archive copied into `C:\1. AUTHORIA\downloads` with a `.meta` carrying mod id 185531 and file id 791427.
- meta.ini updated to version 1.5.0e with the new installation file name.

## Unverified

Not tested in game; MO2 and Skyrim were never launched. The Daedric pact rework is the one place where an
existing save could behave oddly: the changelog says a Prince now makes a formal offer instead of claiming
you, but it does not say what happens to a pact that was already auto-entered under 1.5.0. If you had
already been claimed by a Prince, check the Book of Days shows the patron you expect.
