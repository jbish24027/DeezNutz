# Wanderer's Fair patch builders (moved out of session scratchpads 2026-10-16)

- `build_patch.py` + `espmini.py` (2026-10-14): builds `Authoria - Patch - Wanderers Fair - No Reseat.esp` from the fair's
  own 2.0.1.3 plugin: QUST 0014BD with the 3000 u capped crowd table (table json lived in the 10-14 session scratchpad `upd\table`)
  and SeatLayoutVersion 0, plus the HeightSizeFix SPEL condition. Run FIRST after any fair update.
- `build_patch_v2.py` + `fair_trim_config.json` (2026-10-16): the stage trim, applied ON TOP of the installed No Reseat patch:
  Dancers2 43 -> 5 (ring near the stage: 0C00CC..0C00D0), Singers 3 -> 2 (lead, left), Band 3 -> 2 (lute, drum), Orchestra 9 -> 0,
  the 38 dropped dancers set to crowd layer 99 in the cull's Layers array (Table indices untouched, so no table rebuild).
- `disable_ops.json`: the 49 PlacedNpc `MajorFlags += InitiallyDisabled` edits (38 dancers + flute + right singer + 9 orchestra),
  written with houseCARL apply into `Authoria - Patch - Holidays and Fair - Requiem.esp`.
- `install_trim.py`: installs the v2 output, the two shadow-free paper lantern meshes (SLSF1 Cast_Shadows cleared, into the
  Holidays and Fair Requiem mod), switches SSE FPS Stabilizer off in both ini copies, pins fade multipliers 15/12/4.5 in every
  profile, forces the CRDW rebuild. Only with MO2 and the game closed.

Order after a fair update: build_patch.py (new table from the new quest) -> install -> build_patch_v2.py -> install_trim.py
(or just the esp copy) -> re-check that the 49 disabled refs still exist in the new fair version -> Reqtificator rerun (RFTI).
Quest array changes need a NEW GAME.

## 2026-10-17 fix: build_patch_v3.py replaces build_patch_v2.py

v2 emptied the Orchestra array (0 entries). The game refuses an EMPTY array in a VMAD:
`Property Orchestra on script SkyrimFairAudioScript ... cannot be initialized because the value is the incorrect type`
(Papyrus.0.log 2026-10-17 03:54), and the property is None for the whole session.
v3 keeps the 9 orchestra refs listed (they are InitiallyDisabled by the Holidays and Fair Requiem patch, and
every Orchestra use in the stage script is guarded by Is3DLoaded(), so they still never play).

Rebuild order after a fair update is unchanged, but the v3 builder takes the SOURCE and OUTPUT as arguments:
`python -I build_patch_v3.py fair_trim_config.json <pre-trim No Reseat esp> <out esp>`
The pre-trim source is the 10-14 build (3000 u Table cap + SeatLayoutVersion 0), kept at
`_backups\2026-10-16 - Fair stage trim + stabilizer off\...No Reseat.esp.before`.
Rule: never write a 0-length array property into a VMAD; drop the property or leave one disabled entry.
