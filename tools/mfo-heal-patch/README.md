# MFO heal patch — stop MFO stripping followers' signature weapons

**Mod:** marth Follower Overhaul (Nexus 187445, github.com/marthofdoom/MFO)
**Applies to:** the byte-identical upstream **1.1.4** DLL (sha256 `286e2452…368f3`, per
`releases/v1.1.4/MANIFEST.txt` on the repo's `main` branch). Anything else is refused.

## The bug

`native/Logistics.cpp` → `HealExcludedWeapon()`, called from `ServiceFollower()` every 5 s
per follower out of combat, **above** the `bLogistics` gate. Its guard:

```cpp
if (!bad || (!Catalog::IsExcluded(bad->GetFormID()) && !IsCreatureWeapon(bad))) continue;
```

`Catalog::IsExcluded` is the Synthesis catalogue's `exclude` array — every `quest` / `unique`
weapon in the load order, which is exactly every custom follower's signature weapon. The heal
swaps the wielded weapon for the best carried playable one (or bare hands) and
`RemoveItem(..., kStoreInContainer, player)`s it — the `[heal] … returned-to-player` line in
`MFO.log`. Written for invisible *creature* weapons MFO had looted; the `IsExcluded` half is
the oversight. `IsStockGear` (#69) treats the same predicate as a reason to *protect*, but the
heal was never given that exemption. No INI switch sits above it. Unchanged v1.1.3 → HEAD
(2026-09-06).

## The patch

Two bytes, file offset `0x9E79F` (RVA `0x9F39F`): `75 18` (`jne heal`) → `90 90`. An
excluded-but-playable weapon now falls through to the `IsCreatureWeapon` test and is left
alone; creature weapons heal exactly as before. Nothing else in the function changes.

```
python patch_heal.py --check    # STOCK / PATCHED / UNKNOWN (exit 1 = stock, needs apply)
python patch_heal.py --apply    # backs up to backup\, refuses if the game or MO2 is running
python patch_heal.py --revert
```

**After every MFO update run `--check`.** A new build is refused (UNKNOWN); re-derive first.

## Re-deriving for a new build

1. `derive\locate_heal.py` — parses `.pdata`, disassembles every function with capstone,
   finds the `[heal] {:08X} excluded …` string → the `doHeal` lambda body → its
   `std::function` vftable / direct call → the constructing function (`HealExcludedWeapon`),
   and the `ServiceFollower` call site via its `"subsystem off"` / `"excursion cap"` strings.
   Prints the annotated disassembly. Update `DLL` at the top.
2. In the dump, find the hand loop: `cmp ebx,1 / sete dl / call GetEquippedObject /
   cmp byte [rsi+0x1a],0x29 / … / call IsExcluded / test al,al / jne heal / mov rcx,rsi /
   call IsCreatureWeapon / test al,al / jne heal / inc ebx / cmp ebx,2 / jl`. The patch site
   is the **first** `jne` (after the `IsExcluded` call).
3. `derive\verify_heal.py` — update the RVAs, confirm the callees (IsExcluded = FNV-1a
   `0xcbf29ce484222325` / `0x100000001b3` + set lookup; IsCreatureWeapon = `test byte
   [rcx+0x10],4` then a second lookup), that nothing lands on the patch bytes, and that
   `.reloc` is empty there.
4. Update `SIZE`, `SHA_STOCK`, `OFF`, `CTX` in `patch_heal.py`. Confirm the DLL sha against
   the repo's `releases/<ver>/MANIFEST.txt` so the source you read is the binary you patch.
5. Check the source at that tag first — if upstream ever adds `IsStockGear` to the heal
   guard, or drops the `IsExcluded` half, the patch is obsolete.

## Alternatives that also work

- **Per-follower switch (upstream-supported, per save):** Field Orders power → Followers tab →
  untick the **MFO** column for the follower. `mfoEnabled=false` returns before
  `ServiceFollower` (Scheduler.cpp ~254). Needs redoing on a new game, and a freshly recruited
  follower is hit within 5 s of first OOC service — before you can reach the board.
- **Catalogue edit** (drop the rows from `mfo_items.json`): works, but the Synthesis patcher
  regenerates the file and silently undoes it. Not used.

## Upstream report (ready to paste)

> `HealExcludedWeapon` (Logistics.cpp) strips catalogue-excluded (quest/unique) weapons out
> of followers' hands and hands them to the player — e.g. Kaidan's Nodachi (`0Kaidan.esp
> 0x00A697`, why=quest) and Ashe's Crucible's Tear (`Ashe - Fire and Blood.esp 0x04761B`,
> why=unique), logged as `[heal] … excluded '…' -> …, returned-to-player 1x`. It runs from
> `ServiceFollower` every 5 s above the `bLogistics` gate, so no INI switch stops it; only
> `mfoEnabled=false` does. `IsStockGear` (#69) already treats `Catalog::IsExcluded` as
> *signature gear to keep*; the heal treats the same predicate as a reason to strip. Suggested
> fix: guard on `IsCreatureWeapon(bad) || (Catalog::IsExcluded(id) && !IsStockGear(fol, id))`,
> or drop the `IsExcluded` half entirely (the loot filter already refuses creature weapons).
> Reproduces on 1.1.4 with every logistics/cast switch off; unchanged through v2.0.1.
