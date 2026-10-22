# Testing: offline checks, the in-game loop, reading feedback

## Contents
1. What offline checks can and cannot see
2. Bundled checks (run after every build)
3. Extra checks worth writing for a new garment type
4. Pre-install checklist
5. The in-game test loop
6. Turning user feedback into a change

## 1. What offline checks can and cannot see
Every offline check poses bones by hand and measures the skinned result. None of them simulates physics, so none can see **lag, inertia or momentum**. A tabard that passed every static check clipped "a ton more" in game because its inertia was copied from a rig with longer bones. Always say this when you report check results; the user's in-game test is the real verdict.

The most honest offline metric: **legs posed, cloth NOT reacting** (physics bones held at rest). Whatever ends up inside the legs there is what the cloth must actively get out of.

## 2. Bundled checks (run after every build)
`scripts/rebuild.py <design.py> [--install]` runs all of them and prints one table; `<work>/STATE.md` keeps each design's
last verdict, its numbers at the last install and what differs from the installed mod. Read that, not the logs.
| Script | What it proves | Pass |
|---|---|---|
| `verify_rig.py <design>` | Every source triangle present once (or split exactly into 4); visible pieces keep shader/textures/alpha/flags; <= 4 influences summing to 1; <= 80 bones per shape; HDT string -> the XML; every XML shape / bone / constraint body exists; **0 rest contacts** for every collider pair the XML allows; BodySlide targets: every point's simulated build (small + big, set defaults + optional preset) = the original set's, colliders move with their source points; skirt smoothness (share of points on 2 chains) | `ALL OK` |
| `stride_check.py <design> [target]` | The skirt lining vs the one-sided leg colliders while the legs sprint/walk (each side leading) and the chains are at rest / curled in to the limit / swung back, forward, sideways: caught (pushed out correctly), **hooked** (pushed out the wrong way = stuck behind the leg), sunk (deeper than the catch) | compare versions of YOUR rig (it reads the builder's collider names, so it cannot score a different author's rig); hooked is what reads as "stuck". A confirmed-good mail skirt: 1002 / 15 / 666 summed over all rows; the version that stuck had 44 hooked in the sprint-at-rest row alone |
| `pose_render.py <design> [target]` | Source at rest, build at rest (must look identical), build with a right-front kick: panels bend smoothly, slits open, layers stay together | look at the PNG |

Also diff the new XML against the previously installed one when you change a value: builder edits that silently did not apply have shipped the old version before.

**Reading the numbers** (values from designs users confirmed in game):
| Number (where) | Meaning | Typical / lever |
|---|---|---|
| lining to the trousers at rest, p10 / median (build log) | how far the skirt's inner side hangs off the trousers; negative = the trousers poke through the cloth at rest (puffy trousers - fine, the cloth follows them there) | mail skirts 2.6-4.1 median; hide / quilted skirts ~1.6-3.1 |
| free share p10 / median (build log) | how much of the skirt swings free of the legs (the rest follows the trousers) | **0.75-0.9 median** on confirmed designs. Below ~0.5 = very subtle. Raise with `gap=(0.0, 1.5)` (skirts resting within ~2 units of the trousers) or `free_max`; lower with a wider `gap` |
| points with physics / on 2 chains (verify_rig.py) | share of skirt points carrying chain bones; of those, how many blend two neighbouring chains | informational: 76-77% with physics, 54-69% on two chains on confirmed designs; far lower on two chains = points sitting on one chain (creases) |
| caught / hooked / sunk (stride_check.py) | see above | hooked ~0; sunk rises when more of the skirt swings free (normal - the collider lets go and the leg passes through); judge sunk only between versions with the same gap |
| bones per shape (build log) | the 80 cap | a 12 x 5 skirt piece lands at 60-70 |

## 3. Extra checks worth writing for a new garment type
These caught real problems in earlier projects; write them when the bundled ones don't cover the garment.
- **Edge stretch in posed legs**: |l1/l0 - 1| per edge in idle / stance / walk / stride / run / knee-up. Catches tearing and helper bugs (a 4-cap drop at a slit = 260-415% stretch). A finished tabard: idle max ~0.5, stance ~0.85. Benchmark against the author's mesh and a reference rig - all-joints-at-limit poses are meaningless.
- **Layer crossings**: inner layer points outside the posed outer layer, legs posed, cloth not reacting.
- **Rigid-swing clearance** for a flap: the smallest rotation about its hinge that clears the posed leg (walk ~0.4 rad, stride ~0.58, run ~0.86) - sets the out-limit and shows when a hinge can never clear.
- **Tail / plate sink**: a belt tail or plate with its own bone held at rest while the skirt under it swings within its limits; >= 1.5 units sunk -> let it ride the surface more.
- **Quasi-static pose solve** (damped least squares over the joint angles within the XML limits, legs moved in small steps): an approximation that ignores momentum - it passed a version that was worse in game. Use it to compare, never to promise.
- Leg poses that worked (thigh L, thigh R, knee L, knee R in rad, + = forward): idle (.22, -.06, .12, .05) - the default idle has the LEFT leg forward; stance (.35, -.15, .2, .1); walk (.38, -.25, 0, .35); stride (.55, -.3, 0, .6); run (.75, -.45, .25, .9); knee-up (1.1, -.1, 1.2, .1). Thighs rotate about the hip bind position round world x, calves about the knee.

## 4. Pre-install checklist
1. Every collider pair: 0 contacts at rest (and in the idle stance).
2. Legs posed, cloth not reacting: visible cloth inside the legs, layer crossings.
3. Edge stretch in those poses.
4. No colliding point skinned to the dynamic bones of the surface it collides with.
5. Shared helpers keyed on this armour's bone prefix (or a parameter), not a previous one.
6. `_0` and `_1`: same topology, same collider point counts.
7. Renders of rest + poses.
8. Tell the user: static checks cannot judge feel or fast motion.
9. New mesh code (a cut, a weld, a re-weight) was tested on its output: 0 edges joining two panels when neighbouring panels are swung apart; each layer rendered alone and swung; the posed-check numbers compared with the last installed round and given to the user.
10. The report says what the checks covered (rest pose only, or which poses / clips) and never implies movement was tested when it was not; it says plainly what is installed and what is only staged.
11. Collider COVERAGE after any topology change (a cut, a split, a weld, a new layer): print every hidden collider shape's point count and z range and compare with the last installed round. A selection rule can silently shrink a collider to the edges of a sheet (Realistic Armor v16: cutting the outer into panels turned 10% of its triangles sideways, the "inward side" rule took the cut edges + hem lip as the lining, and the panel faces had no leg collider for three rounds - the user saw the skirt "sitting in the thigh"; verify's ALL OK never looked at coverage).
12. When the user says a piece of geometry belongs to the wrong layer, render that layer ALONE (textured, four sides) and ray-cast through its openings before answering, and show them the render. Never argue from an aggregate statistic: a per-vertex texel-luminance test "proved" twice that a Realistic Armor scale skirt carried no cloth, while a brown gusset strip bridging its front and back openings sat on the scale shape the whole time (the author's filler behind the panel edges, cut in half by the panel cuts). The user's screenshot was right on the first try.

## 5. The in-game test loop
- Install as a NEW mod (stage folder copied in), back up the previously installed version OUTSIDE the mod manager's mods folder first, and tell the user exactly which mod it must outrank (see pipeline-and-packaging.md).
- Give the user a table of `player.additem <FormID> 1` lines for every armour / variant using the mesh (including vanilla items that share it).
- Ask them to: walk, run, sprint, turn, jump, stop and stand still (twitch-after-stop is a separate symptom), crouch, sit.
- Console: `smp reset` reloads every equipped item's XML (XML-only changes: no restart). `smp report gear` lists what loaded. **Mesh changes need a full game restart** (and a re-run of any downstream mesh patcher). Say which kind each change is.
- `Documents/My Games/Skyrim Special Edition/SKSE/hdtSMP64.log` reports XML parse errors with line numbers (search for the XML's file name).
- Expect 1-3 rounds for a design built from the bundled presets, up to 10 for a first-of-its-kind garment. Ask for screenshots plus what the character was doing.

## 6. Turning user feedback into a change
- Change one thing family at a time and say what you changed in their words ("springs 20% softer so it swings more").
- Translate feel words with the table in xml-and-physics.md section 5; diagnose clipping/sticking/twitching with troubleshooting.md before touching values.
- Before rebuilding, run a targeted check that reproduces the complaint offline (stride for "stuck", rest contacts for "twitch", stretch for "uneven spot"), fix, re-run it, then rebuild.
- Record each round (version, what changed, why, the user's verdict) so the next session does not re-learn it.

**`smp reset` caution (2026-10-10):** an XML change that showed no effect after `smp reset` did take effect after a full relaunch (FSMP's log level was off, so the reload could not be confirmed). When a change seems not to apply, relaunch before concluding the values are wrong.
**Chain swing budget:** the SUM of a chain's outward limits (hinge + every lower joint) must stay under 90 deg. A thigh at a sprint pushes a tassel to its limit; past the horizontal gravity holds it folded on the stomach and no mass, damping or spring brings it back (confirmed in game: hinge 1.3 + 3 x 0.1 fixed it).
