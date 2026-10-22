Authoria - Papyrus - Quest Fragment Patches

This output collects small quest-fragment fixes where several quest mods touch the same vanilla scripts. The ESPs keep the record-side properties lined up with the winning scripts, and the loose scripts keep the compiled fragment code matched to those merged records.

ESPs included:
- Authoria - Papyrus - AYOP Thane - Immersive Interactions.esp
  Merges the AYOP Thane and Immersive Interactions dialogue/quest fragment setup so the shared Thane quest fragment keeps the properties both sides expect.

- Authoria - Papyrus - Bards Reborn - USSEP - AYOP Misc.esp
  Merges overlapping Bards Reborn, USSEP, and AYOP misc quest fragment edits instead of letting one patch leave the other scripts with stale or missing properties.

- Authoria - Papyrus - Ebony Bade Curse - Requiem.esp
  Keeps the Ebony Blade Curse and Requiem changes together so the Ebony Blade tracking script has the properties it needs at runtime.

- Authoria - Papyrus - Infiltration QE - AYOP Thane.esp
  Carries forward the Infiltration Quest Expansion reward update while preserving the AYOP Thane edits to the same quest area.

- Authoria - Papyrus - USSEP - Dibella Quest Expansion.esp.esp
  Merges the USSEP and Dibella Quest Expansion quest-fragment/property changes so the repaired Dibella quest scripts bind cleanly.

Scripts included:
- DA08EbonyBladeTrackingScript.pex
  Source-backed Ebony Blade tracking script used with the Ebony Blade Curse/Requiem merge. It keeps the friend-kill and blade-state tracking code matched to the patched VMAD data.

- Infiltration_Reward_Final.pex
  Source-backed Infiltration reward script. It keeps the final reward/global update intact after the quest-fragment merge.

- QF_MS05DUPLICATE000_00053511.pex
  Source-backed quest fragment for the Bards Reborn/USSEP/AYOP misc merge, compiled against the repaired property layout.

- QF_T01_00023B6C.pex
  Source-backed Dibella quest fragment compiled against the merged USSEP/Dibella Quest Expansion properties.

- TIF__00060022.pex
  Source-backed topic fragment for the AYOP Thane/Immersive Interactions merge, keeping the dialogue properties from both patches available.
