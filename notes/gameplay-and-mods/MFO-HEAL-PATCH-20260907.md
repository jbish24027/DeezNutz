# MFO 1.1.4 — followers handing the player their signature weapon (2026-09-07)

**Symptom.** Kaidan's Nodachi and Ashe's Crucible's Tear kept landing in the player's
inventory; the follower was left bare-handed or re-armed with pack junk (Kaidan's War Bow,
then an Imperial Heavy Bow). Five events across three sessions, all in
`overwrite\SKSE\Plugins\MFO.log` as `[heal] <ref> excluded '<weapon>' -> <substitute>,
returned-to-player 1x`.

**Cause (source, tag v1.1.4 = the installed DLL, sha256 `286e2452…` per upstream's
`releases/v1.1.4/MANIFEST.txt`).** `native/Logistics.cpp` → `HealExcludedWeapon()`, called from
`ServiceFollower()` every 5 s per follower out of combat, **above** the `bLogistics` gate, with
no INI switch anywhere on the path (verified read-site by read-site: `bLogistics`,
`bEquipToCast`, `bEconomy`, `bDollsMode`, `iCastControl`, `bCommandTarget`, `bMagicLoadout`,
`bAutoRetreat`, `bWeaponStyleControl`, `bSeedEvaluatorRules`, `bBeastHeadFix` all sit below it
or elsewhere). Guard: `!Catalog::IsExcluded(id) && !IsCreatureWeapon(bad)` → continue. The
catalogue's `exclude` array is every quest/unique weapon in the load order = every custom
follower's signature weapon (Nodachi `0Kaidan.esp 0x00A697` why=quest; Crucible's Tear
`Ashe - Fire and Blood.esp 0x04761B` why=unique). The heal was written (commit 0b21810,
v0.8.33) for invisible *creature* weapons MFO had looted; the `IsExcluded` half is the
oversight — everywhere else in the tree (`IsStockGear`, shed, loot, economy, `KeepHeadClear`)
the same predicate means *keep*. Only `mfoEnabled=false` (the per-follower MFO checkbox on
the board) stops it. Unchanged v1.1.3 → v2.0.1 → HEAD (2026-09-06) and on upstream's
`fix/mfo-heal-slot-and-proxy` branch.

**Two wrong turns first, both undone.** `bLogistics=0` (session 1) and `bEquipToCast=0`
(session 2) were each proven irrelevant by the next session's log. Both inis were restored to
their pre-session values; `bLogistics` was then set to 0 again for the *separate* reason below.

**Fix applied.** `_tools\mfo-heal-patch\patch_heal.py --apply`: two bytes at file offset
`0x9E79F` (RVA `0x9F39F`), `75 18` (`jne heal`) → `90 90`. The heal is now creature-only —
exactly the author's stated intent. Stock backup in `_tools\mfo-heal-patch\backup\`.
(The `_backups\2026-09-03 …\MFO.dll` is an older build, sha `5b5c6943…` — not a revert source.)
Post-apply instruction diff of the whole function: exactly one `jne` removed, two `nop`s added.
Verified by three independent lenses (source semantics, binary re-derivation, every other
item-removal path in the tree) plus a completeness critic — record in
`_tools\mfo-heal-patch\derive\verification-20260907.txt`. No Authenticode, no CFG table, no
checksum, no self-hash, no shadow copy of the DLL anywhere in the instance.

**Why `bLogistics` stays 0 (independent of the heal).** With logistics on, the default
"Always → Loot Equipment" gambit scores what a follower already holds while *skipping* excluded
weapons (`Logistics_Loot.cpp:722`), so a follower whose only 2H is the signature blade reads as
unarmed and will loot any corpse 2H and equip it in place, shoving the Nodachi/Tear into the
pack. Never reached the player, never fired in the surviving log — but it is the install
ledger's original reason for logistics OFF, now with a line number.

**Still to do in game (save has no pre-bug state):** hand the Nodachi (`8300A697`) back to
Kaidan and Crucible's Tear (`9404761B`) back to Ashe; take Kaidan's War Bow (`83116448`) off
Ashe and, if she still has it, the Imperial Heavy Bow. Refs: Kaidan `83002F9C`, Ashe
`942D4A35`. Force the wield with `prid <ref>` + `equipitem <formid>` if they don't draw it.

**After any MFO update:** `python _tools\mfo-heal-patch\patch_heal.py --check` (refuses any
other build; README has the re-derivation method). Alternative per-save mitigation: board →
Followers tab → untick the **MFO** column for the follower.

Effective MFO state now: MCM layer `bLogistics=0 bEquipToCast=1 bEconomy=0 bDollsMode=1
bCommandTarget=0 iCastControl=0`; DLL patched.
