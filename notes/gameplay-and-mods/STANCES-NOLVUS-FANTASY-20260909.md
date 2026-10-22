# Stances - Nolvus Awakening v6 Fantasy movesets into Bear / Wolf / Hawk

**2026-09-09.** Goal: make Authoria's stance animations match the acrobatic/fantasy
movesets Nolvus Awakening v6 uses, without needing a new save.

## What Bear / Wolf / Hawk actually are

Settled from Stances NG's own EditorIDs, not guessed:

| Authoria | Stances NG effect | Nolvus stance | Role |
|---|---|---|---|
| Bear | `APO_HighStanceEffect` | High | Aggression. Normal attacks +30%, movement and attack speed -20% |
| Wolf | `APO_MidStanceEffect` | Mid | Defence. Block +10%, damage reduction +5%, attack power -10% |
| Hawk | `APO_LowStanceEffect` | Low | Speed. Attack speed +20%, movement +10%, attack power -20% |

Authoria and Nolvus run the same three stances under the same animal names -
Stances NG ships bear/wolf/hawk icons and Nolvus ships the matching icon mod.

**This reverses the pairing given earlier in the session** (low->bear, high->hawk).
Bear is the High stance. Putting Nolvus's fast Low movesets on Bear would have run
them at -20% attack speed while the heavy ones played at +20%.

## What could NOT be verified

Nolvus's own per-stance moveset assignment was not recoverable. Checked and ruled out:
the Awakening guide pages (no equivalent of the v5 animation page exists), the public
animation appendix (gives folder numbers per weapon/stance, never mod names), the Nolvus
dashboard source (the mapping lives in `InstallPackage.xml`, fetched from an authenticated
endpoint that returns 401), and a real Awakening v6 modlist from Load Order Library
(the framework mod names carry no stance labels). No Nolvus install survives on C: or D:.

The three framework archives are empty folder scaffolds - `meta.ini` and `config.json`
only, zero animations. The installer copies movesets into them at install time.

So placement below is **Authoria's own, decided by measurement**, not a reproduction of
Nolvus's assignments.

## How placement was decided

Animation duration was read directly out of each `.hkx`. The parser was validated against
the annotation sidecars already in the stance folders (`# duration:` lines) and reproduced
them exactly (2.000000 and 2.166667 on the first two Bear greatsword attacks).

Mean normal-attack duration across the 11 packs, fastest first:

| Pack | Mean | Placed |
|---|---|---|
| Nioh Spear | 1.37s | Hawk |
| Swords of Legends (Jinyun) | 1.38s | Hawk |
| WoLong Spear | 1.58s | Wolf |
| WoLong Dual Wield | 1.64s | Hawk |
| WoLong LongSword | 1.91s | Hawk |
| Jedi Survivor Dual Wield | 2.10s | Wolf |
| HollowSlayer | 2.12s | Wolf |
| BDM Berserker Greatsword | 3.00s | Bear |
| Tower of Fantasy XIAZUO | 3.38s | Bear |
| Axe of Leviathan (God of War) | 3.55s | Bear |
| Naraka Bladepoint Dual Wield | 3.76s | Bear |

The three slowest packs plus XIAZUO went to Bear, the middle band to Wolf, the fast band
to Hawk. Two calls changed from the first draft once measured: **Tower of Fantasy moved
Hawk -> Bear** (3.38s is Bear-tier, not fast), and **the two spears swapped** (Nioh at
1.37s is the faster of the pair, so it took Hawk and WoLong Spear took Wolf).

Naraka on Bear was the least certain call in the draft and the measurement confirmed it -
at 3.76s it is the slowest pack of all eleven.

## Final placement - 11 folders

**Bear (High)**

| Weapon folder | Moveset | Chain |
|---|---|---|
| Greatsword | BDM Berserker Greatsword | 4 normal, 3 power |
| War Axe | Axe of Leviathan (God of War) | 7 normal, 6 power |
| Dual Sword | Naraka Bladepoint Dual Wield | 3 normal, 4 power |
| DaiKatana | Tower of Fantasy XIAZUO | 6 normal, 4 power |

**Wolf (Mid)**

| Weapon folder | Moveset | Chain |
|---|---|---|
| Greatsword | HollowSlayer | 4 normal, 10 power |
| Polearm | WoLong Spear | 4 normal, 2 power |
| Dual Sword | Jedi Survivor Dual Wield | 4 normal, 3 power |

**Hawk (Low)**

| Weapon folder | Moveset | Chain |
|---|---|---|
| Greatsword | WoLong LongSword | 4 normal, 6 power |
| Polearm | Nioh Spear | 6 normal, 4 power |
| Dual Sword | WoLong Dual Wield | 8 normal, 2 power |
| Sword | Swords of Legends (Jinyun) | 5 normal, 3 power |

Each pack ships several condition folders; the one taken is the **player** variant in every
case - the folders gated on `NOT IsActorBase(Skyrim.esm|0x7)` are NPC-only and the
Keytrace-gated ones are directional variants. For the Leviathan axe only the base moveset
folder was taken, not its stagger library, idles, movement or hit reactions - those would
have overridden animations globally instead of inside one stance.

## What changed on disk

Three mods edited in place: `Authoria - Stances - Bear`, `- Wolf`, `- Hawk`.

- 253 animation files removed from the 11 target folders
- 126 animation files copied in (attacks, power attacks, sprint attacks, combat idles, SCAR dummies)
- 19 directional sibling folders deleted

Every `config.json` was preserved, so the stance conditions are untouched.

The **combo chain is always replaced whole**. A half-swapped chain would play the new
moveset for the first hits and the old one for the rest. Any `BFCO_`-named attack file was
removed too, because it would shadow the `MCO_` file going in - two target folders were
BFCO-driven (Hawk Polearm entirely, Wolf Dual Sword partly) and are now MCO-named like the
rest of the stance system.

**Sprint attacks, jump attacks and idles were kept where the incoming pack had no
replacement** - Bear Dual Sword and Bear DaiKatana keep their sprint attacks, Wolf Dual
Sword keeps its jump attacks. Everything else came from the new pack.

The directional folders had to go. They still held the outgoing moveset, so leaving them
would have played the old animations whenever you attacked while moving. With them gone
OAR falls through to the base folder and the whole stance is one coherent moveset.

## Coverage

Each stance covers 21 weapon types, so 63 folders exist. **11 were changed.** The other 52
keep their current Authoria movesets.

That is a limit of the source material, not caution. These 11 archives are the distinctive
Fantasy picks; Nolvus fills its remaining stances from a much larger roster shared with the
Conventional option.

Submod counts after the work: Bear 57, Wolf 31, Hawk 36.

## Verification

All 11 folders re-measured after installation. Every one reports the source pack's own
duration, a contiguous `mco_attack1..N` chain with no gaps, its `config.json` intact, and
zero leftover `BFCO_` attack files. Zero stray directional folders remain. Ten files from
the WoLong Dual Wield folder were byte-compared against the source: all identical.

## Save safety and reversal

No plugin was added, removed or touched. No load order change, no ESL index shift, no
profile file edited, nothing the Outfit Wheeler can notice. This is animation files inside
folders that already existed.

Backup: `_backups\2026-09-09 - Stances pre-Nolvus-Fantasy` - complete copies of all three
stance mods as they were, 65 MB. To revert, delete the three mods and copy these back.

Extracted sources and the three framework scaffolds are kept at
`_maintenance\nolvus-fantasy-20260909`.

## Not done

The `Nolvus Awakening OAR Stance Combat/Movement/Block Framework` archives were **not**
installed. They reference Nolvus-specific perks and plugins Authoria cannot satisfy, and
they carry no animations. They were used as reference only.

---

# Revision 2 - the sword stances, and what "acrobatic" actually meant

**2026-09-09, later.** User feedback after testing: "stances dont look like the acrobatic ones
im thinking of for sword". Two separate causes, only one of them about moveset choice.

## Cause 1 - two of the three sword stances were never touched

Revision 1 changed `Sword - Hawk` only. `Sword - Bear` and `Sword - Wolf` still held Authoria's
originals, so unless the Low stance was active nothing had changed. `Sword - Bear` also had **no
idle animation at all** and never has - it fell through to a generic pose.

## Cause 2 - Nolvus's stance "look" is the IDLE POSE, and Authoria has no such layer

Opening the Movement Framework properly settled this. It carries **662 submods**, and for every
weapon type it defines four separate idle poses - `Sword Neutral / Low / Mid / High Combat Idle
Start`, each with a Non Combat twin, plus per-stance movement, blocking, equipping and sprint
variants.

Authoria's Bear/Wolf/Hawk system changes **attacks**. A stance only gets a posture of its own if
its attack folder happens to carry an idle. That is why switching stance in Authoria changed how
you swung but not how you stood.

## Cause 3 - the source list was incomplete

Revision 1 worked from 11 archives. Nolvus's real Fantasy roster, read from the `6.2.1 ATTACK
ANIMATIONS` section of a genuine Awakening v6 modlist, is **76 mods**, and section `6.2.2 MOVEMENT
ANIMATIONS` is another 39. For one-handed sword alone Nolvus ships Swords of Legends, Geralt MCO
Animations, Witcher's Combat, Elder Creed - Blade, For Honor Centurion, the Imperium and Nordic
complete packs and more - it fills each stance from a *different* pack, which is exactly why its
four stances look nothing alike.

The user's description - "a lot of spinning, pirouetting, even some jumps" - is the Witcher style.
Nolvus ships **two** Witcher packs.

## What was installed

Three archives: Witcher's Combat in both its Geralt (male) and Ciri (female) variants, and
The Witcher MCO (Geralt in the skyrim, MCO build - not the SKYSA one).

| Stance | Moveset | Chain | Mean | Idle |
|---|---|---|---|---|
| Bear (High) | Witcher's Combat - Geralt (male) | 10 atk / 10 pwr | 1.65s | 3.33s |
| Wolf (Mid) | The Witcher MCO | 4 atk / 5 pwr | 1.46s | 3.33s |
| Hawk (Low) | Witcher's Combat - Ciri (female) | 10 atk / 10 pwr | 1.62s | **28.25s dynamic flourish** |

**Every stance now has its own idle**, verified by fingerprint as three genuinely different
animations - so the three stances differ in posture, not just in swing. Bear's long-standing
missing idle is fixed. Blockidles came along for Bear and Hawk, so the block pose is
stance-specific too.

Ciri's 28.25-second idle (source folder `9000021`, gated on `NOT IsAttacking`) is the showpiece -
a long flourish loop rather than a 3-second hold. It sits on Hawk, where the Low stance's +20%
attack speed also flatters the 10-hit chain.

The male Geralt set went on Bear deliberately. The author states the male and female variants
share the same moves and differ only in "movement details and idle", so using both buys a clearly
distinct posture for the heavy stance on a female character.

The pace band here is narrow - 1.46s to 1.65s - because Witcher swordplay is uniformly fast. Bear
still takes the slowest of the three, but this is not the wide spread the other weapon types got.

Sprint attacks came from the packs in their own vanilla naming (`1hm_attackforwardsprint`), and the
outgoing MCO-named ones were removed so there is no ambiguity about which plays.

Swords of Legends is displaced from Hawk and no longer used on the Sword stances.

## Requirements checked

Payload Interpreter, Precision - Accurate Melee Collisions, Animation Motion Revolution,
Attack - MCO-DXP and Elden Rim are all installed and active. Elden Counter is not, which only
affects the counter-attack folders (`2147483640`+), none of which were installed.

## Caveat from the author

Witcher's Combat is tuned for **long swords** and, in the author's own words, does not sit well on
one-handed swords that are too short. If it looks wrong on a specific blade, that is the reason.

## Not taken

The packs' directional Keytrace folders (`9000010`-`9000017` - WD, WA, AS, AD, SD, ASD, Shift
attacks) map cleanly onto Authoria's `dir*` sibling pattern and are a natural next step. The Sword
stances currently have no directional siblings, so these would be new folders rather than
replacements. Also not taken: equip/unequip animations, block-hit reactions, TK dodge, and the
counter-attack sets.

## Backups

`_backups\2026-09-09b - Sword stances pre-Witcher` - the three Sword folders as they stood after
revision 1 (Hawk on Swords of Legends). The full pre-Nolvus state is still in
`_backups\2026-09-09 - Stances pre-Nolvus-Fantasy`.

## Verification

All three folders: contiguous `mco_attack1..N` chain, expected attack and power counts, measured
mean matching the source pack, `config.json` intact, zero `BFCO_` files left to shadow the MCO
names, and three distinct idle fingerprints. Zero failures.
