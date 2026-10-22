# Authoria - Fix - UBE Expression Strength

Built 2026-08-28.

## What this is

UBE's faces use their own expression morph files, so Expressive Facial Animation never
touches them. EFA is authored for the 996-vertex vanilla head; UBE's is 11,498 vertices
and a different sculpt, so EFA cannot be ported by any file swap, and no port exists.

Measured morph-for-morph, UBE is not actually weak — it beats EFA on anger, puzzled,
squint, brow-in, disgusted and fear. It is weaker on a short list: eyelid gaze-follow,
surprise, happiness, brow-raise and a few phonemes.

This mod raises **only those** morphs, by editing the single float multiplier each morph
carries in the .tri file. Nothing else changes.

## Who it affects

Only actors on a UBE race. In this load order that is the player, **Lydia** and **Serana**.
Everyone else uses vanilla head parts and already gets EFA.

## How it was made

Source files are the copies from `Ultimate Body Enhancer - No Combat Expressions`, which is
the current load-order winner for all four. That preserves NCE's deliberate settings:
`CombatAnger` multiplier 0.0 and `CombatShout` 0.35x. Both are frozen and never touched here.

Only per-morph multiplier floats were rewritten. Vertices, triangles, UVs, morph names,
morph order and every int16 delta are copied byte-for-byte. Byte counts changed per file:
head 40, brows 30, lashes 45, mouth 37 — all inside multiplier floats. (The mouth's 37 includes
4 bytes for the extra `CombatAnger` zeroing described below.)

Each boost is capped so the result never exceeds EFA's own reach for that morph by more
than 10%. Seven morphs hit that ceiling and were clamped automatically, and one more
(head `DialogueHappy`) was already above it in UBE and so was left alone entirely.

The cap is measured as `multiplier x max |int16 delta component| / part's largest bounding-box
dimension`. Measured instead as peak vertex *displacement magnitude*, three head morphs
(`MoodSurprise`, `BrowUpLeft`, `BrowUpRight`) land 0.7–3.6% over the ceiling rather than exactly
on it. That is a choice of yardstick, not a miscalculation — all three are still under 4% of the
head's bounding box.

## Boost table

One factor per morph, applied to every part that carries it, so the face stays in sync.

| Morph | Factor | Was (vs EFA) |
|---|---|---|
| LookUp, LookDown | 2.5x | 0.17-0.23x — eyelids barely followed the gaze |
| DialogueSurprise | 1.7x | 0.23-0.45x |
| MoodSurprise | 1.4x (mouth clamped 1.33x) | 0.65x |
| MoodHappy | 1.5x (mouth clamped 1.32x) | 0.39-0.65x |
| DialogueHappy | 1.2x lashes, 1.03x mouth (clamped); head/brows already at EFA, untouched | 0.60-0.69x |
| BrowUpLeft, BrowUpRight | 1.35x (head clamped 1.30x) | 0.58-0.85x |
| Aah | 1.3x (mouth clamped 1.24x) | 0.59-0.77x |
| BigAah | 1.2x | 0.68-0.80x |
| DST, BMP | 1.4x | 0.43-0.72x |
| Th, N | 1.25x (mouth Th clamped 1.15x) | 0.69-0.71x |

## What this does NOT fix

Scaling a zero is still zero. These have no delta data in UBE at all and need real
geometry work, not a multiplier:

- **Brows on blink** — 8% of EFA, essentially noise
- **Brows on look up/down** — literally all-zero
- **UBE's eye mesh** — 43 of its 49 morphs are all-zero; only the Look directions carry
  data. This may well be deliberate, since UBE's eyelids live on the head mesh.

## Load order

Must sit **above** `Ultimate Body Enhancer - No Combat Expressions`, which must stay above
`Ultimate Body Enhancer`. If NCE wins over this mod, these boosts are silently undone.

Files touched (4):

    meshes\!UBE\Head\FemaleHead.tri
    meshes\!UBE\Brows\femaleheadbrows.tri
    meshes\!UBE\Lashes\EyeFemaleLashes.tri
    meshes\!UBE\Mouth\mouthhumanf_tangent.tri

`meshes\!UBE\Eyes\eyesfemale.tri` is deliberately not included — boosting the eye mesh's
Look morphs moves the eyeball itself, which changes where characters appear to be looking.

## Reverting

Disable the mod. Nothing else is affected — no plugin, no script, no save data.

## Tuning

Every value is a single float in the .tri. If the eyelid follow still reads too subtle,
LookUp/LookDown have room to go to about 4x before they reach EFA's level. If anything
looks overdone, the factor can be dialled back or set to 1.0 for that morph alone.
