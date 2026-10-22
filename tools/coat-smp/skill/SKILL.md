---
name: authoring-smp-armor-physics
description: USE WHENEVER the user mentions SMP, HDT-SMP, FSMP, cloth / armour physics, a skirt / cape / plume / belt / bag that should move, or any Sons of Skyrim, Realistic Armor, New Legion, Elite Wolf or Nordwar SMP work - load it before touching the builders. Author, port or tune HDT-SMP / FSMP cloth physics on Skyrim SE armour by script (Python + PyNifly) - skirts, gowns, coats with welded skirts, mail, tabards, cloaks, hip plates, belt tails, sashes and bags - covering piece cutting, bone rigs, weights, the SMP XML, hidden colliders, BodySlide project patching, offline checks, a one-command build/verify/install round and the in-game tuning loop. Use when asked to add physics to an armour that has none, to port or rebuild an existing SMP rig, or when SMP cloth is stuck on the legs, twitches, clips, or feels too stiff or too light.
compatibility: Windows x64; Python 3.10+ with numpy (opencv-python for renders); PyNifly V29 (headless); Skyrim SE/AE with FSMP 4.x. Claude Code skill.
---

# Authoring SMP armour physics

You build cloth physics the way a careful modder would in Outfit Studio + NifSkope, but by script: read the armour's
mesh with PyNifly, cut the moving cloth into pieces, hang a bone rig on it, weight it, add hidden colliders, write the
mesh and its SMP XML, prove it offline, then tune it with the user over a few in-game rounds. The user tests in game;
you never can.

Bundled: `scripts/` (a generic skirt-rig builder, a coat builder in `coat/`, the checks, a one-command round per builder,
a mesh survey, renders) and `references/` (the physics rules and proven numbers). Every `scripts/...` path below is relative to this skill's folder, `${CLAUDE_SKILL_DIR}`; run
them with a Python that has numpy (pass the design file's own path, from any working folder).

## Rules that decide success (read before anything else)
1. **Nothing may touch at rest.** Any collider contact while standing = twitching after the character stops.
2. **Leg colliders are the real trousers surface, split into one-sided front / side / back pieces**, each colliding
   only with the matching part of the skirt lining. Never a closed tube, never pulled inside the legs - those hook
   the skirt behind the thigh.
3. **Outward swing is the NEGATIVE X limit** in the bundled chain frame; **inward limits add up down a chain** - keep
   them 0 (capes, flared cloth) or tiny (0.08, light mail).
4. **Inertia is absolute and tied to bone length** - never copy another rig's mass/inertia verbatim. "Heavier" = more
   mass, less wind and linear damping. `gravity-factor` is clamped to 1.
5. **4 influences per vertex, 80 bones per drawn shape.** Merge the smallest weight into the bone that moves most
   like it; never just drop it. Cut moving cloth into its own shape to stay under 80 bones.
6. **`_0` and `_1` must match point for point** - topology, weights, splits AND hidden collider point counts. Decide
   everything once on `_1`.
7. **Unique bone-name prefix per armour family** - SMP finds bones by name on the actor.
8. **A downstream mesh copy (PBR patcher, BodySlide output) silently replaces your mesh.** Find which file wins
   before debugging; re-run the patcher after every mesh change.
9. **Offline checks cannot see lag or momentum.** Say so every time you report them.
10. **Ask the feel question first: subtle (cloth on the legs follows them) or oomph (fully free below a short ramp)?**
    And which SMP armour they already like the movement of - measure that rig.

## Setup (once per machine)
- Install: this folder goes in `~/.claude/skills/` (or a project's `.claude/skills/`); run it with
  `/authoring-smp-armor-physics`.
- Python 3.10+ with numpy; opencv-python only for renders. PyNifly V29 release zip extracted (no Blender needed).
- `scripts/smpkit/settings.json` (copy `settings.example.json`): `PYNIFLY_DIR` = the `io_scene_nifly` folder,
  `SKELETON_NIF` = BodySlide's `res/skeleton_female_sse.nif`, optional `TEXCONV`. Environment variables override it.
- Smoke test: `python scripts/survey_mesh.py <any armour _1.nif>` prints its shapes.
- Details and the user's game-side requirements (FSMP, XPMSSE, body): references/pipeline-and-packaging.md.

## Workflow
**0. Scope.** Get: the armour (mod + mesh path), which parts move and which stay rigid, subtle vs oomph, a reference
SMP armour they like, which bodies (finished `_0/_1` meshes, BodySlide projects for HIMBO / 3BA...), permission to
create a new mod, and agreement to 2-4 in-game test rounds. Three job types share the toolkit: **author** a new rig
(this workflow), **port** an existing rig onto a converted mesh (references/rig-and-weights.md section 8), **tune** an
existing XML only (references/xml-and-physics.md section 5; `smp reset`, no rebuild).

**1. Find the file that wins in game.** Check the mod manager's conflicts for the mesh path the armour record uses.
Build from the **author's original** mesh, not a downstream copy.

**2. Survey.** `python scripts/survey_mesh.py <mesh_1.nif>` (or `--osp <project.osp> --set "<set>"`). Assign every
shape a role - skirt layers, belt (band + tail + bag), plates, trousers, rigid (cuirass), drop (old colliders, hidden
parts) - with the guide in references/rig-and-weights.md section 1. Read the **lower edge by angle** of the belt band
and cuirass: the skirt swings only below the rigid cover over its top.

**3. Write the design file.** Copy `scripts/designs/example_design.py`; every key is explained there.
- `sk_belt` = the **lowest point of the rigid cover's lower edge** over the skirt's top (belt band or cuirass hem,
  whichever hangs lower), or up to 1 unit under it; `sk_anchor` = `sk_belt` + 2. Proven: 68-73.5 on knee skirts.
- `phys` preset by material (cloth / leather / leather_lamellar / lamellar / chain - table in
  references/xml-and-physics.md section 6); component sizes you rely on in `expect=`.

**4 to 7 in one command.** `python scripts/rebuild.py <design.py> [--install]` builds, verifies, runs the stride check and
the renders, compares the stage with the installed mod (design key `install=`), installs behind a gate (ALL OK, nothing
foreign changed, every replaced file backed up) and writes `<work>/STATE.md`. Read its one table, not the logs. A tuning
round is `rebuild.py <design.py> --install --xml-only`: it refuses if any mesh changed and tells the user `smp reset`.
The steps below are what it runs, for when one of them needs a closer look.

**4. Build.** `python scripts/build_skirt_rig.py <design.py> [target ...]` -> stage folder + `<work>/<name>_report.json`
and `_build.log`. Read the log: skirt axis, slits, chains, **lining-to-trousers gap and free share** (the first build
is how you measure these), colliders, bones per shape. Free share median below ~0.5 = very subtle; confirmed designs
sit at 0.75-0.9 - a skirt resting within ~2 units of the trousers needs `gap=(0.0, 1.5)`. references/testing.md
section 2 explains every number.

**5. Verify.** `python scripts/verify_rig.py <design.py>` must print `ALL OK`. Then
`python scripts/stride_check.py <design.py> [target]` - compare hooked counts with the previous version / the author's
rig. Diff the XML against the previously installed one. references/testing.md.

**6. Look.** `python scripts/pose_render.py <design.py> [target]` -> PNG of source at rest, build at rest (identical),
build with a kick. Read the image; show it to the user.

**7. Install.** Ask first. Back up any previous version outside the mods folder, copy the stage into a NEW mod, tell
the user which mod it must outrank, whether a downstream patcher must be re-run, and (for BodySlide targets) the build
steps. references/pipeline-and-packaging.md section 4.

**8. Test in game.** Give `player.additem` lines, ask for walk / run / sprint / jump / stop-and-stand, screenshots and
words. XML-only change -> `smp reset`; mesh change -> restart (+ patcher re-run).

**9. Iterate.** Map the complaint with references/troubleshooting.md (clipping, sticking, twitching, looks) or the feel
table in references/xml-and-physics.md. Reproduce it offline, change one thing, re-verify, rebuild, reinstall. Record
version / change / reason / verdict.

**10. Share (optional).** Permissions, the author's look, credits: references/pipeline-and-packaging.md section 5.

## Scripts
| Script | Does |
|---|---|
| `survey_mesh.py` | shapes, moving bones, welded components, texture islands, HDT link, `_0/_1` topology |
| `rebuild.py` | one command per round: build -> verify -> stride -> render -> diff against the installed mod -> gated install with backups -> one table + `STATE.md`; `--xml-only` for tuning rounds |
| `build_skirt_rig.py` | the builder: skirt layers + hip plates + belt tail + bag + floor-length gowns, any number of targets (`nif` = `_0/_1` meshes, `bodyslide` = a project set) |
| `verify_rig.py` | structure, weights, bone counts, XML consistency, rest contacts, simulated BodySlide builds |
| `stride_check.py` | stuck-on-the-legs test: caught / hooked / sunk per stride and chain pose |
| `pose_render.py` | front/side renders at rest and kicked (needs opencv) |
| `smpkit/core.py`, `smpkit/checks.py` | the shared library (NIF read/write, geometry, weights, XML snippets, BodySlide osd, pose/skin/render helpers) for writing builders for other garments |

The builder's algorithms produced armours users confirmed in game; it reproduces those builds byte for byte. It covers
skirts and what hangs on them. Cloaks, separate tabard panels, tunics with a cut-out strap and rig ports need a
garment-specific builder made from `smpkit` - follow references/rig-and-weights.md section 3 + 8.

## The coat builder (`scripts/coat/`)
For a coat whose skirt is **welded into the torso shape** (NordwarUA-style gambesons, mail coats, lamellar coats): the
skirt cut out of the torso by height, component, texture island, hem band or UV split, an inward lining, a belt band with a
hanging tail, a left-hip strap, a bag, a sash end on its own chain, optional extra skirt layers on chains of their own with
colliders between the layers, and men's meshes that keep a PBR patcher's shader block (`shader_donor`) so the SMP mod can
outrank the patcher output. Designs live in a **design file** (paths + a `DESIGNS` dict, one entry per armour) - the worked
example `scripts/coat/designs/sons_of_skyrim.py` holds seven coats confirmed in game plus the three-layer Officer and the two Eastmarch guard cuirasses exactly as installed.
| Script | Does |
|---|---|
| `coat/rebuild_coat.py <designs.py> <design ...|all> [--install]` | the one-command round for coats: build -> verify -> swing / jump / idle / flap / hang / layer checks -> layer renders + slit ray-casts -> diff against the installed mods -> gated install with backups -> one table + `STATE.md` |
| `coat/build_coat_rig.py <designs.py> <design> [m] [f]` | the builder (men's `_0/_1` + the women's BodySlide set) |
| `coat/verify_coat.py`, `coat/swing_stride.py`, `jump_check.py`, `idle_check.py`, `hang_check.py`, `layer_check.py`, `lining_check.py`, `clip_check.py`, `flap_jump.py`, `render_layers.py` | its checks, each `<designs.py> <design> [m|f]` |
| `helmet/build_helmet_rig.py <designs.py> [helmet ...]`, `helmet/helmet_check.py`, `helmet/render_helmets.py`, `helmet/install_helmets.py` | helmets: a flap skirt welded into the bowl (found by the author's Head -> Spine2 fade) on chains from the rim, hinged cheek guards, colliders vs the wearer's body (a hidden copy) and vs the cuirass it is worn with (the coat builder's `torso_coll` writes a public collider into every cuirass, matched across files by tag); per-chain limits that trail backward on a walk and never cave in over the face; a tail (`crest=dict(shape=..., n=5, chains=1|3)`: a plume or horsetail that is its own shape, with or without a weight fade, hair on one chain or three side by side along its centreline after the Realistic Armor ponytail - never in, springs resting a little out, colliding with a hidden copy of the bowl it hangs against and settled clear of it); `helmet/cuirass_collider.py <designs.py>` gives ANY cuirass nif (the author's, or one carrying someone's physics) that public collider + XML, so helmets meet cuirasses the coat builder did not build; v4: the resting skirt is SETTLED clear of every cuirass collider before the rig is built (a point resting inside a collider's margin shell is pushed every frame - 'pulling forward'), the front chains barely swing out, a cheek guard's hinge follows its whole top edge (sloping where it slopes), the check fails on any resting contact and measures contact as FSMP does (a point beyond a collider's edge is free); worked examples `sos_helmets.py` (26 helmets) and `sos_hold_cuirasses.py` |
Proof (2026-10-11): all 44 installed files of those seven coats rebuild byte-identical through this copy and every check log
matches the project's line for line. Use it, not a project fork: a new coat is a design entry, not new code.

## References
- references/xml-and-physics.md - FSMP rules (verified), XML layout, limit signs, collision semantics, feel levers,
  proven parameter sets per garment/material, reference rigs.
- references/rig-and-weights.md - coordinates, survey, pieces, rig layouts per garment, the weight recipe, the
  4-influence cap, collider design, `_0/_1`, other garments.
- references/testing.md - what offline checks can't see, bundled and extra checks, pre-install checklist, in-game loop.
- references/troubleshooting.md - symptom -> cause -> fix tables.
- references/pipeline-and-packaging.md - setup, PyNifly calls and traps, BodySlide projects, installing, downstream
  patchers, sharing.

## Working efficiently (user feedback 2026-10-10: "do this more efficiently and save tokens")
Efficiency means fewer reads, rebuilds and log dumps. It never means fewer checks: a round that skipped the posed checks
to save time (Realistic Armor v16, 2026-10-10) installed a mesh-cutting bug the checks would have caught.
- **Read the state, not the history.** Keep a per-project `STATE.md` / `state.json` that the orchestration script writes (version, verify verdict, what the checks covered, installed or not, residuals per design) and start from it. Project memories hold decisions and lessons, not logs.
- **One orchestration script** (`scripts/rebuild.py <designs> [--install]`, bundled: build, verify, stride, renders, a comparison with the installed version, an install gate, one summary table, state file). The checks live INSIDE the script so no round can skip them. A round is one tool call and one table, not 25 commands and log greps. A garment-specific builder gets its own copy with its extra checks added to the job list.
- **Narrow first, then stop.** Before the first tool call, name the ONE measurement that decides the question; run it; widen only if it does not decide. At most one image per task unless the picture is the question - numbers before pictures. Never re-measure what STATE.md / REQUESTS.md already record. Trim every tool output to the lines needed; never read a listing longer than a screen. Fleet-wide (all designs) work only when the user asks, and then as one script with a one-line summary.
- **Iterate on one design, men only** (`rebuild_coat.py <designs> <design> --bodies=m --no-render`: a men's build is 10-30 s, verify 5 s). The fleet, men + women, runs ONCE at the end of a job, when the mechanism is settled - never a fleet pass per iteration (2026-10-13: four fleet passes in one job, 30-45 min each, and a women's copy-facing loop that rebuilt the variant six times to drop two triangles).
- **Scope is a list of pieces, and everything else is frozen** (2026-10-14: a hold-armour job settled every belt tip "for consistency"
  and took the sway off belts the user had just praised; the Legate fix pulled a collider copy inside its layer to zero a "behind" count
  and the plates sank in). Before the first change, the job names the pieces the user complained about; a piece the user has called good
  is never touched, whatever its numbers look like. Every build prints a REGRESSION DIFF against the last approved install - per piece:
  physics (mass, damping, wind, limits, root), bone shares, rest height over its copy, the copy's offset from the drawn surface - and a
  change on a piece outside the job's list is a FAIL, not a note.
- **A "behind" or "contact" count is cleared only by dropping the faces or settling the piece out - never by moving the copy inward**
  (a copy behind the drawn surface is the magnet's twin: the piece sinks into the layer before anything pushes).
- **One change, one relaunch, one verdict.** A feel-affecting change (physics, root, copy offset, settle) is installed on ONE design
  and waits for the user's in-game word before the next design or the next job; fleet passes are for mechanisms the user has already
  approved on one design. "ALL OK" means nothing broke offline - it says nothing about sway, lag or feel, which only the user sees.
- **A piece that should swing is never weighted onto the layer under it, and never hangs from that layer's chain.** Ride shares
  (tip_follow / hang_follow) and a skirt-chain root are glue, not a magnet cure (user 2026-10-14: "thats the wrong fix"). The reference
  rig is the one the user names as moving best - measure it (sos tools/tip_profile.py: root, physics, weight profile by height band,
  rest clearance) and match it within .05 per band; the magnet is handled by room and dropped copy faces.
- **Idle is fine.** While the user tests, wait unless asked; do not survey or prototype the next armour on your own. A genuinely new capability (a new garment type, independent layers) is named and estimated BEFORE starting, not discovered an hour in.
- **Builders print summaries, not dumps** ("max bones 77 (shape)" instead of a per-shape dict), and carry a MAP block in the docstring saying where colliders, weights and the XML are decided, so a session jumps to the lines instead of reading 1,000 of them.
- **Calibrated gates**: residuals the user accepted in game are reported, never FAIL; everything else still fails. `ALL OK` names what it covered (rest only, or which poses and clips).
- **Prototype one design end to end** (build, verify, checks) before batching the rest of a family. Rebuild only the designs a change touches and prove the untouched ones byte-identical, instead of rebuilding every design for a two-armour job.
- **XML-only changes** (limits, springs, damping): patch the installed XML by regex AND the builder constants; never rebuild meshes for a number. Tell the user `smp reset` or relaunch, no BodySlide / PG. Python is edited with the editor, never with shell regex: three heredoc patches in one session applied nothing and the builds that followed ran the old code.
- **New mesh code** (a cut, a weld, a re-weight) is tested on its OUTPUT before anything is installed: count edges joining two panels, render each layer alone and swung, compare the posed-check numbers with the last installed round, and give the user the numbers.
- Hand only the mechanical rounds (build / verify / install) to a cheaper subagent; design decisions, new mesh code and its output tests stay in the main session.
