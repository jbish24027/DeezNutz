# Setup, PyNifly, BodySlide projects, installing and sharing

## Contents
1. Prerequisites and setup
2. PyNifly: the calls that work and the traps
3. BodySlide projects (osp / ShapeData / osd)
4. Installing into a mod manager, priority, downstream patchers
5. Sharing a build publicly
6. Working efficiently

## 1. Prerequisites and setup
**Game side** (the user's): Skyrim SE/AE + SKSE64 + Address Library; **FSMP - Faster HDT-SMP** (Nexus 57339; replaces old HDT-SMP, never both); XPMSSE skeleton (bone names like `NPC Pelvis [Pelv]`, `NPC L Thigh [LThg]`, `NPC Spine2 [Spn2]`); the body the armour is made for (HIMBO men, CBBE 3BA women, ...); BodySlide and Outfit Studio when a target is a BodySlide project.

**Script side:**
- Python 3.10+ with **numpy** (all the builder needs) and **opencv-python** (only `pose_render.py`). On machines where the system Python lacks a package, any bundled Python that has them works (scripts put their own folder on `sys.path`, so embedded Pythons are fine).
- **PyNifly** (BadDog's Blender add-on, GitHub releases; tested with V29.0.0): download the release zip and extract it - no Blender needed. Point the kit at the `io_scene_nifly` folder (it contains `pyn/` and `NiflyDLL.dll`; Windows x64).
- A skeleton nif for telling body bones from physics bones: BodySlide ships `CalienteTools/BodySlide/res/skeleton_female_sse.nif`.
- Optional: **texconv** (Microsoft DirectXTex) for textured renders.

Copy `scripts/smpkit/settings.example.json` to `scripts/smpkit/settings.json` and fill `PYNIFLY_DIR`, `SKELETON_NIF` (and `TEXCONV`), or set them as environment variables.

**Never name your own scripts after a module on the path** (`osd.py` clashes with PyNifly's `osd` package; two work folders each with `survey.py` shadow each other).

## 2. PyNifly: the calls that work and the traps
Import `pyn` directly (`import io_scene_nifly` needs Blender): `from pyn.pynifly import NifFile, NiStringExtraData, SkyPartition, nifly`.

Writing a skinned shape (what `smpkit.core.Writer` does - use it rather than re-deriving):
1. `out = NifFile(); out.initialize('SKYRIMSE', path, root_type='NiNode', root_name=src.rootName)`
2. custom bone nodes first, parents before children: `out.add_node(name, xform, parent_node)` - create every chain node top-down even if no vertex uses it.
3. `props = NiShapeBuf(); props.bufType = PynBufferTypes.BSTriShapeBufType`; for hidden colliders `props.shaderPropertyID = NO_SHADER_REF` (otherwise a default shader is attached and it renders).
4. `sh = out.createShapeFromData(name, verts, tris, uvs, normals, props=props, parent=out.root)`; `sh.flags`; `sh.set_colors(...)`.
5. Shader copy: take `src.shader.properties.copy()` but keep the new block's own `textureSetID, nameID, controllerID, rootMaterialNameID, extraDataCount`; set texture slots with `nifly.setShaderTextureSlot`; `sh.save_shader_attributes()`. Alpha: `sh.has_alpha_property = True`, fill flags/threshold, `sh.save_alpha_property()` (an existing alpha block cannot be overwritten).
6. `sh.skin(); sh.set_global_to_skin(TransformBuf())`; `sh.add_bone(name, xform, parent)`; `sh.set_skin_to_bone_xform(bone, xform)`; `sh.setShapeWeights(bone, [(vertex, weight), ...])`; `sh.set_partitions([SkyPartition(part_id=p, flags=257, namedict=out.dict) ...], per_triangle_ids)`.
7. `NiStringExtraData.New(out, name='HDT Skinned Mesh Physics Object', string_value=xml_path, parent=out.root)`; `out.save()`.

Traps:
- `shape.bone_names` repeats names per partition (and older versions truncated them): read bones via `bone_ids` + `nif.read_node(id=i).name` (`core.Shape` does).
- `TransformBuf` has no usable inverse: convert with `core.tb2m` / `core.m2tb` and use numpy.
- Some BodySlide-project shapes store points around the origin with a global-to-skin translation: run `core.to_world()` before any geometry work, write identity transforms. A verifier comparing raw positions will not notice.
- Half-float UVs shift by one step on re-save: match points by position (UV tolerance 1e-3..5e-3), never by rounded UV keys.
- Skinned shapes may come back with triangles reordered by partition: compare triangle sets, not order.
- `vertexDesc` cannot be set. Double-sided: `Shader_Flags_2 |= 0x10`.
- A fresh `NifFile` drops all extra data except what you add: if the source had other root extra data, carry it over. BodySlide adds the RaceMenu morph link (BODYTRI) on the SHAPE itself.
- Shell heredocs eat backslashes in Windows paths and XML paths: write scripts and data files with a file-writing tool, use forward slashes, `glob.escape` paths with `[`.

## 3. BodySlide projects (osp / ShapeData / osd)
- `<mod>/CalienteTools/BodySlide/SliderSets/<project>.osp` holds `SliderSet` elements; each names `DataFolder` + `SourceFile` -> `ShapeData/<DataFolder>/<SourceFile>` (the zero-slider mesh, `.nif`) and the same-stem `.osd` (slider diffs: per entry `{vertex index: (dx, dy, dz)}`, <= 65535 diffs per entry).
- A `bodyslide` target rewrites three files with the SAME names into the stage: the osp (its copy keeps every other set; only this set is rebuilt), the ShapeData nif and the osd. Installed as a mod that outranks the project's mod, BodySlide then builds the physics version. Original mods stay untouched.
- New shapes get slider entries named `<shape><slider>` with `local="true"`; data elements pointing at other projects' osd files are left alone.
- One osp often holds many sets: build every design that touches it in one sequence (each run edits the staged copy set by set).
- If the user's body differs from the project's (a CBBE project on a 3BA body), fix the base first: use the project version made for their body.
- User steps after installing: refresh the mod manager, tick the patch, launch BodySlide from the mod manager, pick the group / set and the preset, build (batch build) into an enabled output mod that outranks the old meshes. If two sets write the same file, pick the physics set in the conflict prompt.
- `verify_rig.py` simulates BodySlide builds (each slider at the preset value / 100, `invert` = 1 - f) and proves the visible points match the original set's build; after the user's real build, re-check one built mesh (HDT link, all pieces, rig bone count).

## 4. Installing into a mod manager, priority, downstream patchers
- Build into the design's `stage` folder (a work folder). Ask before writing into the user's mods folder. Install by copying the stage into a NEW mod folder; never edit other mods' files.
- Before replacing an installed version, back it up OUTSIDE the mods folder (a backup inside it becomes a mod / pollutes the virtual file system).
- The SMP mod must outrank whatever else provides the same mesh path. Say "higher priority" (wins) / "lower priority" - not "above/below", which flips between mod managers' views.
- **Downstream mesh patchers** (PBR patchers such as ParallaxGen, BodySlide outputs) write their own copies of the mesh that outrank everything. They keep the HDT string, custom nodes and colliders when they copy, but they copy whatever mesh was winning WHEN THEY RAN. Two working patterns:
  1. Build from the author's original mesh, enable the SMP mod, then re-run the patcher. **Every mesh change needs another run.** XML-only changes don't.
  2. Build FROM the patcher's output (its textures baked in) and give the SMP mod higher priority than the patcher output. No re-run needed, but the result is not shareable.
  3. **Shader donor** (the coat builder's `shader_donor`, 2026-10-11): geometry from the author's original mesh, the shader block (PBR texture paths / flags) copied from a frozen copy of the patcher's output of the same mesh. The SMP mod outranks the patcher output and never needs a re-run: a PBR patcher only writes a copy of a mesh it has to patch, and these meshes already carry the PBR paths (checked: 50 of 50 men's coat meshes, no patcher copy of any of them). Shareable only with the author's shaders put back (section 5).
- A stale downstream copy was the #1 cause of "physics doesn't work" reports.
- **BodySlide outputs** sit at their own priority: if the patcher output outranks the BodySlide output folder, a rebuilt women's set is beaten by the patcher's stale copy until the patcher updates (an update run with a cache is minutes, a full run can be 10+). Decide once per project which of the two the user runs after a women's change, and say it with every install.

## 5. Sharing a build publicly
- Check every source mod's "Permissions and credits" (mesh author, conversions, any previous physics patch). A closed-permission patch must contribute NOTHING to a public build - build from the author's mesh, not from the patch.
- Ship the author's look: if you built from a PBR/patched copy, rebuild from the author's original (or copy back the author's shaders/textures/normals onto the visible shapes while keeping geometry, weights, binds, nodes, colliders and the HDT link), and check no patched texture path remains.
- Pieces with independent XMLs and shapes can ship as separate files.
- Describe honestly what changed (cut pieces, subdivided triangles, moved UVs, hidden colliders); credit the authors.

## 6. Working efficiently
- Most of the cost of an SMP project is re-reading context; start a fresh session per armour and load this skill.
- A first-of-its-kind garment took ~10 test rounds; a design on the bundled builder with a preset took 1-3. Survey carefully, write `expect=` sizes, run all checks before the user tests.
- Keep a short per-armour record (version, change, reason, verdict) - in your notes or memory - so the next round starts from facts.
