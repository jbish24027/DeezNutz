# Picta x Astralite "baby" (built 2026-10-17)

Profile **DEEZ CS NUTZ - PICTA x ASTRALITE** = byte copy of DEEZ CS NUTZ - PICTA plus four baby-only mods.
User picks: colour mix Medium (MIX 0.50 / 0.30 / 0.50 dawn / day / dusk), fog air half strength, rain/fog/snow mixed too,
mists at all hours. Night, interiors, brightness keys, fog distances, seasons, summer weathers, fair, Helios exits = Picta.

## What is installed

| Mod | What it holds | Baby modlist slot |
|---|---|---|
| `Authoria - Picta x Astralite - E11` | full fork of the Darkened E11 override (+ shipped postpass/lens/overlays ini, July DOF ini, PictaPure B01 copy); 931 whitelisted Dawn..Dusk colour/GVR lines in 24 routed files | above `Authoria - Picta - Bottled raindrop` |
| `Authoria - Picta x Astralite - Root twin` | copy of the Picta Root twin with the fork's enbseries.ini + 4 fx ini | above `-Authoria - Picta ENB - Root twin` (Picta twin OFF in the baby) |
| `houseCARL - Authoria - Patch - Picta x Astralite` | ESL: 28 WTHR (DALC, VOLI links, Distant_Mounts rings on 15, MoT banks on 12) + 11 VOLI + 3 RFCT + 3 ARTO | above `houseCARL - Authoria - Patch - Picta Seasonal`; plugin right after Picta Seasonal.esp |
| `Authoria - Picta x Astralite - Mist assets` | Soul Core distant_mounts nif/dds + Astralite MistsVolumetric reskin + volmist/mist1.dds | above `[NoDelete] Mists of Tamriel` |

## Folders

- `design_final.json` - the verified design spec. `map_*.json`, `map/` - the evidence.
- `design/finalize/` - `final2_model.py` (solver; dials in `dials()`), `build_stage2.py <branch>` (stage + VERIFY), `indep_check.py`.
- `build/` - `install_e11.py <branch> [--update]`, `make_voli_spec.py`, `make_ops.py`, `verify_records.py`, `make_profile.py`,
  `baby_snapshot.py` (Picta-lane fingerprint), `build_mist_assets.py`.

## Branches (E11 fork only; the ESL is the same in all four)

`alive` (installed) = VL already renders. `newly_on` = plugin ini fVolumetricLightingIntensity=1.0 + GVR zeroed elsewhere (use only if the
in-game VL probe shows no change). `alive_full` / `newly_on_full` = fog air at Astralite's full strength.
Switch: MO2 + game closed -> `python -I -B build/install_e11.py <branch> --update`. The installer refuses if the installed fork/twin
changed since the last install (`build/fork_state.py check` - e.g. in-game Effects 11 saves): capture those first, or pass `--discard-edits`.
It then mirrors the twin (`build/baby_sync_twin.py --write`) and re-records the state (`build/fork_state.py record`).
After an in-game E11 Save in the baby: run `build/baby_sync_twin.py --write` (MO2 closed) so the Root twin matches the fork.

## Verification 2026-10-17 (3 independent checkers, read-only) - PASS
Records exact (45, all 609 ops, VOLI = PBR-winner sources), colours within 0.71% luminance, night identical, hue to 0.1 deg, VFS/plumbing
correct, Picta lane 0 changes. Known, by design / disclosed: (1) the fog air uses Astralite's phase + density, so storms (E01/E03/E04)
and snow are much hazier than Picta (off-sun haze ~ Picta's god-ray peak at noon) - per-weather VOL 0 is the off switch; (2) VL up to
1.32x target on the fair clock; (3) 47 interiors with UseSkyLighting (Kaidan tent, Magpie attic, Labyrinthian maze, fair sandbox) take
the new ambient (luminance up to -3.9%); (4) cloud silver-lining rim -7.4% next to the sun; (5) ReShade ini sync-back still lands in the
shared Picta-lane ReShade preset - do not retune ReShade in the baby. Reports: `verify/`.

## Refresh after any Picta change (Darkened rebuild, E11 editor save in PICTA, records/seasonal patch rebuild)

1. MO2 + game closed. 2. Re-dump the map JSONs if records changed (see design_final.json build_steps 2).
3. `design/finalize/final2_model.py` -> `build_stage2.py alive` (all four) -> `indep_check.py`.
4. Records changed? Rebuild the ESL: forward the 28 from Darkened/Seasonal again, `make_voli_spec.py`, `make_ops.py`, apply, `verify_records.py`.
5. `build/install_e11.py <branch> --update`. In-game E11 editor saves made in the BABY land in the fork: copy them out before step 5.

## Rules in the baby

- Effects 11 editor Save is fine (lands in the baby fork). Never press Bottled "Save Settings" (shared SettingsUser.json), never retune ReShade
  (shared Picta-lane preset), never run generators from the baby (shared output mods).

## Rollback

Switch MO2 back to DEEZ CS NUTZ - PICTA. To remove completely: delete the profile folder and the four mod folders (nothing else was touched;
`build/manifest_before.json` vs `manifest_after.json` = 0 changes across 2,392 Picta-lane files).
