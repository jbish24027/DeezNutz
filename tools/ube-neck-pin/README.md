# UBE neck pin — recovery kit

The UBE neck seam fix is a **skin-weight edit baked into the body meshes**: on every UBE body /
body-copy / neck-adjacent shape, the Head bone's weight is forced to 0 at Z <= 112.5 (the seam ring)
and ramps back to full by Z 116.25; the removed weight goes to Spine2. The head mesh carries the
mirror-image profile (Authoria - Fix - UBE Neck Seam). Head and body therefore agree at the ring.

**Any BodySlide rebuild of a UBE body or outfit writes raw weights and strips the pin.**
Symptom: a thin gap / step around the whole neck at neutral pose.

## What happened 2026-08-21
- 07:03 BodySlide rebuilt `UBE SE 2.0 Release Body` (zeroed sliders) into
  `mods\Authoria - Bodyslide Output - UBE\Meshes\!UBE\Body\femalebody_tangent_0/1.nif`.
- Measured: 483 ring verts carried Head weight up to 0.21 (raw). Male body pinned 07-31: 0. -> pin gone.
- Re-pinned both files with `pin_files.py`. Verified: ring Head = 0, ramp band identical to the
  pinned male body (same mesh), byte-diff vs backup = weights only. Backup of the raw rebuild:
  `backups\bodypin4-rebuild-20260821\`.
- Still UNPINNED (never were, installed after the 07-31 pass): Vindicator `VA_Leotard_0/1.nif`
  (own body copy + shell, Head up to 0.19/0.21) and `VA_Cuirass` (negligible, max 0.03).
  Other outfits installed after 2026-08-01 were never swept either.

## Scripts (rescued from the Recycle Bin 2026-08-21 — the scratchpad copies were gone)
| file | use |
|---|---|
| `measure_pin.py <nif>...` | READ-ONLY. Prints Head weight on the ring per shape; VERDICT PINNED/UNPINNED. Run this first. |
| `pin_files.py <backup-dir> <nif>...` | Pins the listed files (same algorithm as `pin_fixed.py`, idempotent; copies originals to `<backup-dir>` first). |
| `verify_pin.py <backup-dir>` | Byte-diff every file in `<backup-dir>` vs live; `flagged: 0` = only weight fields changed. |
| `from-bodypin3/pin_fixed.py` | The original universal pass (walks all UBE mod trees). Hard-coded scratchpad path — use `pin_files.py` instead. |
| `from-bodypin2/clearance_pass.py`, `weight_copy.py` | Outfit-shell fixes (cosplay/socks/dresses). Only needed if THOSE outfits are rebuilt. |
| `from-neckbib5/free_jaw.py` | Head-side profile (distance-gated). Only if the head mesh is regenerated. |
| `from-neckfix-final/freeze_skirt.py`, `headtri.py` | Expression-tri skirt freeze. Only after a UBE update replaces the head tris. |

Scripts under `from-*` still import from a dead scratchpad path; `pin_files.py` / `verify_pin.py`
/ `measure_pin.py` import from `from-bodypin3` and work as-is.

## After ANY zeroed BodySlide rebuild of UBE content
1. Close MO2.
2. `python measure_pin.py <the rebuilt nifs>` — confirm UNPINNED.
3. `python pin_files.py "C:/1. AUTHORIA/backups/bodypin-<date>" <the rebuilt nifs>`
4. `python measure_pin.py ...` -> PINNED, and `python verify_pin.py "<backup-dir>"` -> `flagged: 0`.
5. If the rebuilt outfit is one of the cosplay/socks/dresses that had clearance or weight-copy
   fixes, run those first (order: clearance_pass -> weight_copy -> pin).
