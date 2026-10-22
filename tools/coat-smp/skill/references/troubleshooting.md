# Troubleshooting: symptom -> cause -> fix

Each row happened on a real armour and the fix was confirmed. Diagnose with an offline check before changing values.

## Physics does nothing / is broken
| Symptom | Cause | Fix |
|---|---|---|
| No physics at all in game | A downstream copy of the mesh wins (a PBR patcher's output, BodySlide output, another mod) and lacks the HDT string or is an older version | Find which file actually wins (mod manager conflict view / data tab). Outrank it, or re-run the patcher AFTER enabling the SMP mod. Every mesh change needs that re-run; XML-only changes don't |
| BodySlide-built armour has no physics | BodySlide was run with the patch mod unticked, or opened before ticking it, or its output went to a disabled / lower-priority mod | Tick the patch, refresh, launch BodySlide from the mod manager, build into an enabled output mod that outranks the old meshes |
| A piece "falls down" / hangs dead after an update | Mesh and XML versions mismatch (old mesh copy + new XML expecting other bones) | Re-run the downstream patcher / BodySlide; check the HDT string and bone names in the winning mesh |
| An old SMP patch does nothing | Its meshes sit at a path the armour no longer uses | Compare the armour record's model path with the patch's file paths |
| Cloth melts / falls through the floor from one bone down | A missing constraint in the chain | Every bone r must constrain to r-1 |
| Some strips hang stiff | Custom bones not declared in the XML | Declare every custom bone the mesh uses |
| Game crashes when equipping | > 80 bones in one drawn shape, or a malformed / mismatched skinned NIF | Split the moving cloth into its own shape; verify_rig.py bone counts; rebuild from the author's mesh |

## Clipping, sticking, twitching
| Symptom | Cause | Fix |
|---|---|---|
| **Twitches after stopping** / jitters while standing | A collision is active at rest (cloth or a hanging piece already touching its collider) | 0 rest contacts for every pair (verify_rig.py); drop collider triangles touching at rest; never skin a colliding piece to the dynamic bones of the surface it collides with |
| **Stuck behind the thigh** after a sprint or jump | It passed through a CLOSED leg collider and was pushed out the back wall; or a large penetration held it there | One-sided leg pieces (front/back/side by facing) paired with lining pieces by angle; never pull leg colliders inside the legs; stride_check.py hooked count |
| **Crumpled / stuck between the legs** after a jump, a wide stance or combat; a group of neighbouring tassels held splayed out | The Side piece included the INNER thigh faces: they sit 1.5 units apart at the crotch (0.2 on 3BA), inside each other's penetration, so a point that fell between the legs was pushed both ways and held; linked neighbours were dragged up with it | Leave every triangle whose normal points at the body's centre line by > 0.6 out of ALL leg pieces (keep the front-/back-inner quadrants: they only push forward / back). Real-clip check: 'pinched' went from thousands per power attack to tens |
| **Legs show through a long enclosed skirt / gown** when walking, even with working colliders (2026-10-11..13, DE Ballgown v3-v6) | No rig fully stops a stepping thigh touching an enclosed skirt (the Draft Skirt resource, Nexus 171243: "you will get clipping with the thighs... cut from the knee up"). Check what the outfit DRAWS under the skirt: the DE Red project drew the thighs to z 54, GoldBlack the whole thighs + pelvis | Cull the body drawn under the skirt from just below the knee to the waist (target key `cull={'3BA': (z_knee - 1.5, z_waist)}`, pelvis pieces in `drop`); the hidden leg colliders still push the cloth. Never show a "legs posed, cloth frozen" render to the user |
| **Skin blotches through a close-fitting bodice / top** (static cloth over the body; 2026-10-13 DE Ballgown v9) | The outfit's body sits 0-0.5 units under the cloth: a depth fight from a few metres away, and the two follow different bones in motion | Don't draw the body where the cloth covers it: target key `cull_under=dict(shape, cover=(...), depth=2, keep_edge=1.5, edge_zmin=...)`. Keep the strip along the cover's open edges (neckline, armholes) or you see through the dress there; check the cover has no alpha property and every culled triangle stays under it at both weights |
| **Feet come through the BACK hem** on a walk / run / sprint kick-up, though the leg colliders have big foot margins (DE Ballgown v9) | Leg pieces are chosen by REST facing; the leading face of a kick-up is the SOLE (faces down at rest = in no piece) and the foot top (Front). Measured with the game's clips: only 22-32% of the backward-facing foot area at the kick was in the Back piece | `back_kick_clips=('walk','run','sprint')` (needs smpkit anim settings): foot faces that face backward when the foot is behind join the Back piece; `leg_zmin` below the soles |
| **The top of the thigh clips the skirt** when walking / sprinting (the rest is fine) | The leg collider had been pulled 2-3 units INTO the thigh to clear cloth the author buried inside the trousers, so the thigh travels that far before anything pushes. The hip joint sits at pelvis height; the thigh's top sweeps 5+ units forward at a sprint | Collide only points resting >= 0.6 off the REAL trousers (buried ones follow the legs anyway); cap the pull-in at 1.0. Optionally a thigh leash (xml-and-physics.md section 3) |
| **Two layers hang apart** with a see-through gap at the line where they were cut | The author's one sheet was cut into two rigs at a seam (a mail hem over its red band) | Keep one sheet on one rig; where a separate layer is welded to it (a lining at the hem), give the welded points that layer's weights exactly, fading into their own rig over ~3 units |
| **Stacked layers twitch standing still** | Each layer may sag inward (in-limit > 0) onto the one below, touches it and is pushed out again | in-limit 0 on every layer resting on another (0.05 for the innermost on the legs); rest gaps >= 0.6 on every pair |
| Sticks to the legs on every step | Friction (multiplies with the default 0.5) on a light skirt resting close to the trousers | friction 0, springs +40% |
| Sags onto the legs / clings | Inward joint limits accumulate down the chain | in-limit 0 (capes, flared cloth) or 0.08 (light chain) |
| Outer layer clips the inner layer standing still | Inward limits let the outer layer sag through | in-limit 0; an inner-layer shell collider |
| Layers cross when walking | Inner layer follows the legs while the outer hangs free | Drape the outer layer partly onto the legs where the inner one is leg-bound, uniformly across each panel |
| Inner layer pushes the outer cloth THROUGH | It collides with the outer cloth's outer surface | Collide with its inward-facing lining |
| Plates clip into the skirt after stopping | Plate part on its own hinge settles on a different rhythm | Plate points follow the skirt under them 95%; protect that share in the 4-cap |
| Front flap stuck when sprinting | Hinged low on the upper thigh; can never clear a walking thigh | Hinge it at the belt, one chain, forward-facing leg collider only, penetration 3 |
| Belt tail sinks into the skirt / the crotch twitches | Tail rides the skirt AND collides with it (skirt pushed twice), or tail too free | No tail collider; ride 35% (90% flat only for a long tail that sinks in tests) |
| Clipping got worse after "making it heavier" | Inertia copied from a rig with longer bones: the cloth lags | Restore inertia; raise mass instead; cut wind and linear damping |

## Looks wrong
| Symptom | Cause | Fix |
|---|---|---|
| "I can see the skeleton" / creased panels | Each point on one chain / one bone; too few bones per chain | Blend every point over 2 chains x 2 rows; 12 x 5 rig |
| Torn step / uneven spot at a slit top or centre line | The 4-influence cap dropped the left thigh on one side and the right on the other | Merge, never drop; wide L/R thigh blend at the centre |
| Cloth tears where leg-follow sources meet | Borrowed weights from several leg sources (plates, straps) | One smooth source: the trousers, Gaussian-smoothed |
| Belt tail split into layers | Stacked pieces took nearest-skirt weights per vertex | Weight by height alone on its own chain |
| Strap bends sharply under the buckle / S-curve | Short belt->tail blend; gravity sag with weak springs | Blend over ~4 units; springs 100-130, gravity 0.35-0.5 |
| Tails look frozen / crooked | Riding the surface 90%; several loosely linked chains on one panel settle skewed | Own swing (35% ride); one chain per straight panel |
| Black / see-through spot on moving cloth | A single-sided cloth folding, or texture areas the author never painted (hidden while static) | Double-sided flag (SLSF2 0x10); move those UVs onto painted texture by whole pattern repeats - don't repaint |
| Seams open where a piece was cut out | Physics share not zero at the cut | SEAM_FADE (share 0 at the cut, fading in over ~4 units) |
| The mesh loads at the feet (BodySlide project) | Shape stored around the origin with a global-to-skin offset | `core.to_world()` - work and write in bind space |

## Feel
See xml-and-physics.md section 5 ("too stiff", "too light", "too much sway", "air blowing up the legs", "more oomph").

## Added 2026-10-13 (Sons of Skyrim: Riften plume v6-v8b, Officer hangers, the guard bags)

**A tail / plume that sits INSIDE a bowl or cone in game while every offline check passes.** Cause: the chain lies on an inclined
surface, so gravity loads its "never in" stop permanently - the only chain in a project that does that (skirts hang plumb and never load a
stop). A joint stop under a sustained load does not hold in FSMP; contact with a kinematic body does. Measure: the piece's rest clearance
against the surface's OUTER skin by radial crossings (a nearest-triangle distance on a thick-shell bowl reads the inner skin and lies by
the shell's thickness); the limit sense against a chain proven in game (same sign relationship); the VFS winner of the file. Fix: give
the tail the surface back as a PRIVATE collider (helmet crest_collide), not more stops, springs or lifts - six value rounds did nothing.

**'Pulled like a magnet' + jitter the moment a collider is added or enlarged.** Mechanism, the three ways a point gets behind a face and the two non-cures (never move the copy inward, never thin the catch): xml-and-physics.md section 4b. Cause: the hidden copy contains faces the piece sits
BEHIND within the catch (the far side of a thin spike, a rim's underside, any face the piece never lies on); FSMP pushes those points
through the face every frame. Measure: for every piece point, the signed height over each copy face it projects into (FSMP's own test):
count points with height in (-catch, 0) - helmet_check behind_faces does it. Fix: keep only copy faces the piece lies in front of (drop a
face with a point behind it within the catch at rest, drop down-looking faces), and a catch no deeper than the thinnest part of the
surface copied. A clearance number alone passes a magnet.

**A pouch / bag that 'stretches and bends' with every step.** Cause: a rigid piece built with the sash-end recipe - a blend of the
surface under it, the thighs and its hinge, fading over its height (hinge share 0 at the top to 0.85 at the bottom). Measure:
tools/bag_weights.py-style per-height weight breakdown; edge-length strain across the posed clips. Fix: one bone below the hang line
(tail_rigid), the strap / loops on the belt's weights, no leg share; collider, lift and limits unchanged.

**Hip hanger loops that jitter at idle.** Lead: a closed loop of hard joints (anchor -> ring -> strap -> back ring <- anchor) with zero
linear play and light bodies; and copy clearance (points within 0.6 of their copy). Decide with two XML-only tests (closure removed /
collider removed, smp reset) before changing the builder.

**Rest clearance must hold at EVERY character weight.** NPCs spawn at random weights; a piece clear at 0 and 1 sat 2.9 units inside its
copy at 0.5 and 0.75 (Heavy hip loop). Sweep 0..1 in 0.1 steps (coat_lib.weight_sweep) - it costs seconds.

