# SMP XML and FSMP physics: what the numbers actually do

## Contents
1. How FSMP reads the XML (verified rules)
2. XML layout (order matters)
3. Joint limits, springs and the sign convention
4. Collision shapes, tags, margin, penetration
5. Feel levers: what to change for "heavier", "stiffer", "more oomph"
6. Proven parameter sets (by garment and material)
7. Reference rigs worth measuring

All rules below were checked against the FSMP source (DaymareOn/hdtSMP64, tag v4.0.1) or confirmed in game.

## 1. How FSMP reads the XML (verified rules)
- `gravity-factor` is **clamped to 0..1**. XMLs that say 1.5 or 10 do nothing extra. You cannot make cloth heavier with gravity.
- Wind is a **force**: its push scales with 1/mass. At mass 0.1 a breeze shoves cloth at 1-2x gravity ("air blowing up the legs"). Per-bone `<wind-factor>`.
- `linearDamping` is world-space velocity decay = air drag. Running trail angle ~ atan(-ln(1-d) x speed / g): d 0.9 trails ~50 deg, d 0.6 ~30 deg. High linear damping = cloth "blown back" into the thighs at a run.
- `inertia` is **absolute** (not multiplied by mass). It only means something against the bone length. **Never copy another rig's mass/inertia onto bones of a different length**: copying a reference's inertia 20-25 onto bones half as long made a tabard lag so badly the thighs passed through it at a run - while every static check passed.
- `restitution` multiplies with the collider bone's own value; skeleton bones declared before any `<bone-default>` have 0, so bounce settings usually do nothing.
- `friction` multiplies with the kinematic body's default 0.5. A light skirt resting close to bulky trousers that touches them every step **sticks** with friction 0.5-1; use 0 there (and a little more spring).
- COM sits at each bone's origin; `frameInA`/`frameInB` identity = the joint at the child bone's origin in the parent's bind frame.
- FSMP auto-adds skeleton bones the XML forgets (pinned), but **undeclared custom bones do not simulate** (they hang stiff).
- **FSMP reads the XML top to bottom and creates a bone the first time a shape uses it** ("Created bone X added to body Y,
  created without default values"); a later `<bone name="X"/>` is "already exists, skipped" (hdtSMP64.log, FSMP 4.0.1,
  2026-10-13). Harmless for plain kinematic leg bones, but any per-bone setting on a collider bone (a margin-multiplier on
  calves / feet) must be declared BEFORE the first shape that uses that bone, or it never applies.
- Constraints must chain consecutively (bone 1 to anchor, 2 to 1, ...). A missing link = the cloth melts / falls through the floor from that bone.
- The same mesh shape may be declared twice (per-vertex AND per-triangle) with different tags; FSMP builds one body per declaration. Pair filter is two-way: `canCollideWith(a,b) && canCollideWith(b,a)`.
- `smp reset` (console) re-reads every equipped item's XML from disk - XML edits need no restart. **Mesh edits need a full game restart.**
- FSMP simulates only the few actors nearest the camera (configurable); budget bones accordingly.

## 2. XML layout (order matters)
A `<bone-default>` applies to every bone declared after it, until the next default. Shapes come after bones.
**The root element must be `<system>`.** FSMP (`hdtSkyrimSystem.cpp`) returns no system at all for any other root - the
old hdtSMP `<skinned-mesh-physics>` name included - and the only trace is an error-level log line, invisible at the
default log level. The symptom is "no physics, no collision, nothing in the log" (shield collider, 2026-10-11).
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- plain-language description + "Tuning: edit, save, type smp reset in the console" -->
<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">
  <per-triangle-shape name="VirtualGround"> ... tag ground ... </per-triangle-shape>
  <per-triangle-shape name="PFX Legs Front"> ... </per-triangle-shape>          <!-- colliders the cloth hits -->
  <bone name="NPC Pelvis [Pelv]"/> ...                                            <!-- kinematic: skeleton bones the
                                                                                       collision shapes are skinned to -->
  <bone name="PFX Skirt00 0"/> ...                                                <!-- pinned chain anchors (no default
                                                                                       yet = mass 0 = kinematic) -->
  <bone-default> mass, inertia x=y=z, centerOfMassTransform identity, linearDamping, angularDamping,
                 friction, rollingFriction, restitution 0, gravity-factor, wind-factor </bone-default>
  <bone name="PFX Skirt00 1"/> ... all swinging bones of this material
  (repeat bone-default + bones for every other material: plates, tail, bag)
  <generic-constraint-default> frameInB identity, useLinearReferenceFrameA false, linear limits,
                 angularLowerLimit, angularUpperLimit, linearStiffness 0, angularStiffness (x y z), ... </...>
  <constraint-group> <generic-constraint bodyA="PFX Skirt00 1" bodyB="PFX Skirt00 0"/> ... </constraint-group>
  (a second default for the lower joints; one constraint-group per chain: bodyA = row r, bodyB = row r-1)
  <!-- links round the body: frameInLerp 0.5 (translation + rotation), symmetric small limits -->
  <constraint-group> bodyA = chain k+1 row r, bodyB = chain k row r </constraint-group>   <!-- skip across open slits -->
  <per-vertex-shape name="PFX Skirt Front"> margin, tag, can-collide-with-tag ... </per-vertex-shape>
  <per-triangle-shape name="PFX Skirt Outer"> margin, penetration, tag, can-collide-with-tag ... </per-triangle-shape>
</system>
```
Write it with CRLF line endings, UTF-8. Link it from the mesh with a root `NiStringExtraData` named `HDT Skinned Mesh Physics Object` whose value is the Data-relative path (backslashes). Each body variant (plain mesh / HIMBO / 3BA) whose collider bones differ gets its own XML. `_0` and `_1` point at the same XML.

## 3. Joint limits, springs and the sign convention
FSMP uses btGeneric6DofSpring2 (RO_XYZ), bodyA = child, bodyB = parent, frames = the parent's bind frame. The bundled builder gives every chain bone the frame **X along the cloth (tangent), Y outward, Z up**. With that frame:
- **Outward swing is NEGATIVE X**: `angularLowerLimit x = -out`, `angularUpperLimit x = +in`. (A shipped `-0.1..0.7` means outward 0.1, inward 0.7.)
- Y = sideways (+-), Z = twist (+-). Lower <= 0 <= upper always.
- **Inward limits accumulate down a chain**: 0.05 rad x 8 joints let a cape sag ~15 units onto the legs; 0.05 x 5 sank a tabard into the mail under it. Use in = 0 for capes and flared cloth that must keep its drawn shape; a tiny 0.08 for light chain mail; 0.2-0.25 only for "oomph" skirts whose springs hold the shape.
- `angularStiffness` (per axis) = springs pulling back to the bind pose. Springs hold the drawn shape and calm sway, but they also read as **stiffness**: almost every first-pass skirt was "too stiff" until springs came down 20-35%.
- A side chain pushed forward by a thigh needs SIDEWAYS room (y), not only out/in.
- First joint under the belt carries most of the visible swing: give it the widest out-limit (0.8-1.2 rad) and the strongest springs; lower joints narrower (0.4-0.8) and softer.
- **A lower limit above the upper limit = a free axis** (Bullet's rule; FSMP passes the numbers through unchanged, checked in hdtSkyrimSystem.cpp). Write `<linearLowerLimit x="1" y="1" z="1"/> <linearUpperLimit x="-1" y="-1" z="-1"/>` for free translation.
- **Explicit frames**: `<frameInB><basis x y z w/><origin x y z/></frameInB>` (quaternion x y z w) places the constraint frame in bodyB's local space. FSMP derives the OTHER frame from the two bones' transforms at the moment the physics is created (equip, load, `smp reset`), so any constraint between bones that move differently (a chain bone vs a thigh) has its zero set by the pose at that moment. Chain joints are safe (parent and child are in bind relation at creation); a thigh-attached constraint is off by the thigh's swing at creation (idle ~0.2 rad) - give it slack. Each `generic-constraint-default` inherits every field it does not name from the previous one: always write every field.
- **Thigh leash** (builder key `thigh_leash=dict(slack, cos)`; confirmed in game on a light-armour skirt 2026-10-10; a floor-length gown used slack 0.15): row-1 bone of every chain within 60 deg of straight ahead / behind, bodyB = the thigh of its side (both thighs near the centre line), frameInB = inv(thigh bind) @ the chain bone's rest frame, angular X limited to [-3, +slack] (slack 0.25-0.3 - the creation-pose offset above), every other axis free, stiffness 0. Relative X = the thigh's swing seen from the chain, so it drives the chain out with a flexing thigh (front chains) or an extending thigh (back chains) and does nothing the other way. Keep the first joint's out limit >= 1.4 so a thigh on a chair (1.45 rad) can be followed; side chains (|cos| < 0.5) get none (their flexion maps to the free Y axis and would hit the Euler singularity at 90 deg). One XML can serve every body: the frames are angular-only and the orientations differ < 0.01 rad between bodies; decide the leashed set on one body.

## 4. Collision shapes, tags, margin, penetration
- `per-vertex-shape`: the mesh's points are spheres of radius `margin`. Use for the moving cloth (its lining).
- `per-triangle-shape`: the triangles are a surface. It pushes colliding points **to the side its triangles face**; points behind it within `penetration` are pushed out the front; deeper points are released. Use for legs, ground, a layer's outer surface.
- Winding matters. BodySlide bodies store normals pointing INWARD: decide facing from the triangle winding, and flip a leg collider whose triangles face in.
- `<tag>`, `<can-collide-with-tag>` (whitelist), `<no-collide-with-tag>` (blacklist). `<shared>private</shared>` keeps an armour's colliders to itself. `<shared>public</shared>` (FSMP's default when the element is MISSING) lets a shape meet shapes from other files on the same skeleton and on other skeletons: a cuirass collider for a helmet is public on both sides, each whitelisting the other's tag (`internal` = this skeleton only, `external` = other skeletons only - hdtSMP64.xsd ships with FSMP).
- **Large penetration traps cloth on the far side of a closed thigh** (sprint/jump). Closed shells: penetration ~1. One-sided pieces (only the forward-facing leg triangles) can take 3: a pass-through always comes back out in front.
- **Never skin a colliding piece to the dynamic bones of the surface it collides with** - the surface gets pushed twice and fights itself (twitching).
- **Nothing may touch at rest.** A contact active while standing = twitching after the character stops. Keep >= 0.5-1 unit clearance plus margins.
- Collide only where the cloth actually swings (physics share > 0.2-0.5): low-share collision points fling whole chains.
- An inner layer pushing an outer cloth (mail under a tabard) must hit the outer cloth's **inward-facing lining**, never its outer surface (that pushes it through).
- Proven tag set (bundled builder): ground margin 0.5 pen 10; legs front/back margin 0.4 pen 3, side margin 0.4 pen 1.5 (no-collide with each other and ground); skirt lining per-vertex 0.1 split front/side/back, each colliding only with the matching leg piece + ground; skirt outer per-triangle 0.1 pen 2 (what flaps / bag rest on); flap points 0.15; bag points 0.15.

### 4b. The magnet - one mechanism, three ways in, two non-cures (2026-10-14, after the Riften plume, the Eastmarch tips, the Legate)
FSMP tests every collision POINT of a piece against the TRIANGLES of its collider. A triangle has a front side (its normal). A point just in
front of a face, within margin_point + margin_triangle, is pushed out along the normal - the collision working. A point BEHIND the face,
within the penetration depth, is pushed along the same normal THROUGH the face: FSMP assumes it penetrated and shoves it back to the front.
If the piece cannot get through (its joints, or the drawn layer, hold it) it is shoved every frame and never arrives: it hangs there
jittering, dragged toward the face. That is "the magnet". It is a push from the wrong side of a face - not attraction, not a space problem.
A point ends up behind a face in exactly three ways:
1. the copy was placed in front of where the piece's points already sit at rest (a hanger loop wraps behind the belt; a plate's bottom row
   tucks under the mail hem; a copy pulled OUT onto a plate surface the strap passes behind) - behind from frame one, visible standing still;
2. the piece passes behind the layer in motion (the skirt flares past the belt tip; tasset plates swing past the tip) - clean at rest,
   magnet on the first step, so measure it POSED (the clips, the flare fractions), not only at rest;
3. copy faces wound the wrong way, so "behind" is the outside (infacing.py).
The cures match the three: drop every copy face a point of the piece can legitimately be behind, at rest or on the clips (1, 2 and 3),
with the piece resting well clear of the copy (the Whiterun light belt: 2.1 over the skirt; its hangers 1.15 over the plate). A RIDE share
(tip_follow / hang_follow: the piece's points weighted onto the layer under it) is NOT a cure for a piece that should swing - it is glue:
the Eastmarch tips at .55 could not swing and the hangers at .55 never lifted on a jump; the user, 2026-10-14: "who's bright idea was it
to glue the belt down to fix the magnet effect. thats the wrong fix." A ride share belongs only on a piece meant to stay put (a sash end,
a rigid hip plate). The same for the root: a swinging belt hangs from a kinematic bone on the belt (Whiterun 'BeltTip 0'), not from the
skirt chain under it (Falkreath, same physics: "the top half seems glued to the skirt"). Two more things that are NOT cures:
- moving the copy inward (deeper than the points): the behind count reads 0 and the piece now sinks that far into the drawn layer before
  anything pushes - the Legate plates inside the mail;
- thinning the catch (penetration): the deep points stop counting and the piece tunnels through on a fast swing.
The FSMP author's words for case 1 (Discord, 2026-10-13, on the Heavy crotch clip): "your collision is colliding from start, when it should
not; collision need a space from the colliding object" - that is the rest-clearance rule from the engine's side. "Play around with margin
and penetration" (another author) describes the catch; it can hide the symptom, it cannot remove the face the point is behind.
Check: a behind-faces test per pair at rest AND posed (helmet_check behind_faces, sos tools rest_pairs.py / tip_plate_ride.py): FAIL on
any point behind a copy face within the catch; a clearance number alone ("rests +0.65 off the copy") passes a magnet.

## 5. Feel levers
| User says | Change |
|---|---|
| "too light / floaty" | raise **mass** at the same inertia; cut wind-factor and linearDamping. Never borrow inertia from a rig with longer bones |
| "too heavy / sluggish" | lower mass; lower angularDamping |
| "too stiff" (most common) | springs -20-35%, first-joint out-limit +0.1-0.2, inertia down a notch, angular damping down |
| "more oomph" | more of the cloth on physics (free_max / 100% below a short ramp), wider out-limits, swing-in allowed onto a collider, small margins |
| "too much sway / keeps swinging after stopping" | raise angularDamping (not linear), sideways limits down, sideways springs |
| "blown back when running" | lower linearDamping (air drag) |
| "air blowing up the legs" | wind-factor down (0.05-0.15) or mass up |
| "sags onto the legs / stuck" | inward limits 0 (or 0.08), friction 0 for light close-fitting cloth |
| strap curves / S-shape | gravity sag with weak springs: tail springs 100-130, gravity 0.35-0.5 |

Ask before building: **subtle** (cloth on the legs follows them, ~45-80% physics) or **oomph** (100% physics below a short ramp, like most published SMP skirts).

## 6. Proven parameter sets
Notation: out/in/side/twist in radians; stiff = angularStiffness (x out-in, y, z); damp = linear/angular.

**Skirt material presets** (confirmed in game on men + women; bundled as `phys='...'`). Pick by what the skirt IS:
quilted / padded / hide cloth -> `cloth`; boiled or studded leather, a leather skirt under a lamellar coat -> `leather`;
layered leather lamellar -> `leather_lamellar`; steel lamellar / scale -> `lamellar`; any chain mail (also mail over
cloth) -> `chain`. "Leather-ish cloth" = `cloth` (lighter) or `leather` (calmer) - ask which feel, or start one and move.

| Preset | mass | inertia | damp | first joint out/in/side/twist, stiff | lower joints | friction / wind |
|---|---|---|---|---|---|---|
| chain (mail) | 0.5 | 10 | .5/.5 | 1.2/.08/.3/.1, (22,8,8) | .8/.08/.2/.08, (14,5,5) | .3 / .15 |
| cloth | 0.7 | 22 | .24/.38 | 1.05/.2/.18/.06, (75,26,26) | .62/.2/.12/.06, (44,16,16) | .1 / .14 |
| leather | 0.8 | 28 | .3/.45 | .95/.2/.15/.05, (95,32,32) | .58/.2/.1/.05, (56,19,19) | .1 / .12 |
| leather_lamellar | 0.85 | 32 | .32/.48 | .92/.25/.14/.05, (112,38,38) | .55/.25/.095/.05, (66,22,22) | .1 / .1 |
| lamellar | 0.95 | 34 | .36/.52 | .88/.2/.12/.05, (110,38,38) | .52/.2/.08/.05, (64,22,22) | .1 / .1 |
| light chain close to bulky trousers | 0.35 | 6 | .6/.55 | 1.3/.08/.3/.1, (14,5,5) | .9/.08/.2/.08, (8,3,3) | **0** / .15 |

**Other parts** (bundled defaults):
- Belt tail: mass .9, inertia 21, damp .3/.53, friction 0, wind .2, gravity .35; out .4 / in 0 / side .15 / twist .1, lin .02, stiffness 130; own 3-bone chain riding 35% on the surface under it; no collider.
- Bag: mass .6, inertia 4, damp .5/.6, friction .2, wind .05; out .7 / in .05 / side .45 / twist .3, lin .1, stiffness 25.
- Rigid hip plate: mass 1.2, inertia 20, damp .4/.6, wind 0; out .9 / in .05 / side .12 / twist .1, lin .05, stiffness 60; points follow the skirt under them 95%.
- Chain links round the skirt: lin .25, ang .3.

**Heavy-but-subtle two-layer tabard over mail** (user "all good now", 10 rounds): tabard mass 1.1, inertia 20, damp .2/.6, friction .1, wind .1; first out .9 / side .3 / twist .1, lower .38/.3/.08, in 0; panel links .35/.5. Mail mass 1.2, inertia 2.5, damp .2/.7, friction .2, wind .02; out .45 / side .35 / twist .04, in 0. Physics ramp 12 units; tabard drapes 60% onto the leg-bound mail.

**Oomph leather skirt + front flap** (user "perfect"): skirt mass 1, inertia 55, damp .5/.7, wind .1, friction .1; first lo (-.75,-.12,-.05) hi (.25,.12,.05) stiff (200,60,60); lower lo (-.45,-.08,-.05) hi (.25,.08,.05) stiff (120,40,40); links .25/.3; ramp 8. Flap (ONE chain hinged at the belt): mass 1, inertia 40, damp .6/.7, friction 0; first out 1.2 / back .05 / side .08, stiff (30,150,150); lower out .45, (20,100,100). Legs per-triangle margin .3 pen 1; flap collides only with forward-facing leg triangles, margin .3 pen 3.

**Cloak** (7 chains x anchor on `NPC Spine2` + 8; v4 2026-10-13): mass .2, inertia 4, damp .55/.7, friction 0, rolling .2, wind .9; first out .6 / side .2 / twist .1, others out .12 / side .1 / twist .06 (the chain folds < 90 deg), in 0 - v3's first out .9 + others .5 / side .45 / ang damp .45 let a cape fold 252 deg: it popped up on a sprint start and flew forward past the body on the stop; side links lin 1.5 / ang 1.0; body collider margin 1 pen 1, cape margin .5. (Cloaks & Capes values - mass .1, inertia 15, damp .97/.9 - felt "really stiff".)

**Heavy tunic, barely moving** ("extremely heavy" brief): mass 1.5, inertia 18, damp .2/.6, wind .05; first out .8, others .35, side .25/.2, twist .06, never in; 70% physics max.

## 7. Reference rigs worth measuring
When the user names an SMP armour whose movement they like, open its XML + mesh and measure it in the same terms (chains x bones, bone length, % of cloth weight on physics by height, mass/inertia/damping/limits/springs, collider kinds). Then scale to YOUR bone lengths - never copy verbatim.

| Rig | Layout | Numbers |
|---|---|---|
| Blacksted skirt | 14 strips x 6, rows ~8 units, ~45% physics everywhere, split into two shapes to stay < 80 bones | mass .1, inertia 20, damp .3/.3, +-.5 rad all axes, ring links frameInLerp .3 +-1.5 |
| The Hinterland Ranger | 6-9 unit bones, chains unlinked, 100% physics | mass 1, inertia 100, damp .6/.75, back springs 200 on the swing axis, margins .3+.1 |
| RB's Sand Snake skirt | 13 x 5 | mass .8, inertia 50, damp .9/.9, no springs, limits -.1..0.7 (= out .1, in .7) |
| Cloaks & Capes | 3 chains x 8 down the back, anchors on Spine2 | mass .1, inertia 15, damp .97/.9, friction 0, rolling .4 |
| Windcaller belt ends | 2-bone chains | mass .9, inertia 21, damp .3/.53, friction 0, gravity .5, stiffness 100, no collision |
| Northfarer chest | | mass .99, inertia 90, damp .95/.95 (barely moves) |
