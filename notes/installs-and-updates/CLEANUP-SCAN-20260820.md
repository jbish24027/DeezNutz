# Project cleanup scan — 2026-08-20

Scan of `C:\1. AUTHORIA` for stale files. MO2 confirmed closed during scan.
Disk at scan time: C: 227.7 GB free, D: 202.2 GB free.

## SAFETY FINDING — junction landmine (defuse before any delete)

`C:\1. AUTHORIA\_codex_temp\mo2_dragonknight\mods` is an NTFS **junction → `C:\1. AUTHORIA\mods`** (the live mod build).
A naive `Remove-Item -Recurse` on `_codex_temp` could follow it and delete the real mods folder.
The folder's apparent 626 GB size is this double-count; real content is ~1.07 GB.

**Safe removal order:**
1. `cmd /c rmdir "C:\1. AUTHORIA\_codex_temp\mo2_dragonknight\mods"`  (removes link only)
2. Verify `C:\1. AUTHORIA\mods` still intact (spot-check count)
3. Then and only then delete the rest of `_codex_temp`

## Bucket 1 — junk, no unique data (~1.98 GB)

| Item | Size | Why safe |
|---|---|---|
| `Authoria-Astralite-CS-Build-Export.zip` (v1, 08-13) | 1340 MB | Superseded by v2 zip built 2026-08-20 (kept) |
| `backups\_superseded-uniques-20260801` | 390 MB | Resolved investigation |
| `backups\neckbib5-20260801` | 164 MB | Neck seam saga — rolled back, closed |
| `backups\jenny-weights-20260801` | 33 MB | Resolved |
| `backups\jenny-mid-20260801` | 20 MB | Resolved |
| `backups\devotion-preupdate-20260813` | 15 MB | Superseded by devotion-preupdate-20260818 (kept) |
| `backups\neckseam-femalehead-tri-removed-20260815` | 4 MB | Rollback source; rollback completed |
| `backups\full-state-2026-08-15` | 1 MB | Snapshot of superseded state |
| `backups\profile-backup-2026-08-14-shadowcasting-lights` | 0.7 MB | Experiment failed + fully reverted |
| `backups\profile-backup-2026-08-14-shadowcasting-REVERT-pre` | 0.7 MB | Same saga |
| `backups\clearance-20260731` | 0 MB | Empty |
| `backups\SkyrimPrefs.ini.bak-pre-focusshadow-20260814` | 0 MB | iNumFocusShadow resolved |
| `crashDumps\*` (5 MO2 dumps, 08-15…08-18) | 12 MB | Crashes past |
| `__temp__` | 0 (empty) | Nothing in it |

## Bucket 2 — stale but ONLY COPY anywhere (~4.26 GB)

| Item | Size | What it is |
|---|---|---|
| `_codex_temp` (after junction defused) | ~1.07 GB | Abandoned 08-02 houseCARL staging: KittyClass Dragonknight source ESP + 2 BSAs, a scratch MO2, and a **finished "Requiem - Dragonknights Tale Direct Patch.esp"**. Mod never installed — nothing dragonknight-named in mods/ or downloads/. Source re-downloadable from Nexus; the hand-built patch ESP is unique. |
| `profile-backup-pre-astralite-cs-20260809` | 3.19 GB | Only pre-CS-swap profile snapshot. CS build live since 08-09 with ~12 days of work on top; rollback via this is no longer coherent. |

Recommended: archive both to `D:\` then delete from C:.

## Bucket 3 — deliberately NOT touched

- `overwrite\` (2.9 GB) — backup blind spot, contains un-backed-up generated files
- `_backups\` (0.96 GB) — active hotfix-delta runbook target, written today
- `backups\` entries 08-16 → 08-18 (~111 MB kept): lydia-weight x2, serana-face-wire (confirm pending), veldun-preupdate, devotion-preupdate-20260818, willow-dynamicwind (test pending)
- All root `*.md` notes — live paper trail, referenced by session memory
- `downloads\` (247 GB, 7293 files) — the real space hog, but it's the restore source for installed mods. Needs a separate curation pass (superseded file versions only) if wanted.
- `mods`, `profiles`, `Stock Game`, `logs`, `webcache`, MO2 program files — live instance

## Execution log — completed 2026-08-20 ~12:54, all steps verified

1. **Junction defused**: `rmdir` on the link only. Live `mods\` entry count 4165 before = 4165 after. ✅
2. **Dragonknight staging → D:** `robocopy /MOVE` to `D:\AUTHORIA-Dragonknight-Staging-Backup-20260820`, 199/199 files, 1.071 GB, source removed. ✅
3. **Pre-CS profile backup → D:** `robocopy /MOVE` to `D:\AUTHORIA-Profile-Backup-pre-astralite-cs-20260809`, 550/550 files, 3.188 GB, source removed. ✅
4. **Junk bucket → Recycle Bin** (recoverable, not hard-deleted): 18/18 items OK — v1 export zip, 11 backups/ entries, 5 crash dumps, empty `__temp__`. `backups\` now holds exactly the six kept 08-16→08-18 entries. ✅
   - ⚠️ Note: `_superseded-uniques-20260801` was the vault of unique files saved out of the Aug-1 cleanup (163 files, superseded UBE-era outputs). Judged dead ends, but restorable from the bin if wanted.
5. **Space**: C: 227.7 → 232.3 GB free (+4.6). Emptying the Recycle Bin frees ~2 GB more. D: 202.2 → 197.9 (archives landed).

MO2 verified closed before and during all writes.
