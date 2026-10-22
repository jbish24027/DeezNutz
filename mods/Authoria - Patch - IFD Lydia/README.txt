Authoria - Patch - IFD Lydia  (2026-08-21)

Why this exists: Improved Follower Dialogue - Lydia moves Lydia to her own voice type
(FemaleUniqueLydia). Every other mod's Lydia lines were recorded under FemaleEvenToned and
would play silent. This folder:

1. SKSE\Plugins\SkyPatcher\npc\Authoria - IFD Lydia\  - one SkyPatcher line that sets
   Lydia's voice to FemaleUniqueLydia at runtime, whatever plugin wins her record.
   The ini is named after IFD's plugin, so it only loads while IFD is active.
2. Sound\Voice\Kaidan - Immersive Features.esp\FemaleUniqueLydia\  - byte copies of Kaidan IF's
   334 FemaleEvenToned files (217 Lydia lines; the rest are Arcadia/Ria/Carlotta and inert here).
3. Sound\Voice\Inigo.esp\FemaleUniqueLydia\  - Inigo's 79 Lydia chat lines (xwm + lip, pulled
   from Inigo.bsa).
4. Sound\Voice\Lucien.esp\FemaleUniqueLydia\  - Lucien's 3 Lydia banter lines (from Lucien.bsa).
5. Authoria - Patch - IFD Lydia.esp (ESL) - disables Lydia's Amorous Adventures romance
   (quest-level always-false dialogue condition, on top of the OStim winners) and keeps USSEP's
   response fix on one vanilla housecarl line IFD overrides.

Re-keyed lines play in the vanilla Lydia voice (IFD's author forbids AI-cloning the new one).
If Kaidan IF / Inigo / Lucien update with new Lydia lines, redo the copy (see the plan file).
