# Outfit Studio Automation

The Automation dialog lets you define, save, and execute sequences of operations (called **steps**) on your project — either one at a time or in batch across many files or slider sets.

Open it from the **File** menu in Outfit Studio (**Open Automation...**, or press **Ctrl+Shift+A**).

---

## Running an Automation

### Loading a Script

Use the dropdown at the top of the dialog to select a previously saved automation script. Scripts are stored as `.xml` files in the `Automations` folder next to Outfit Studio.

### Placeholder Variables

Expand the **Placeholder Variables** panel to define key/value pairs. Any text field in your steps can reference these using `{{KEY}}` syntax — when the automation runs, every occurrence of `{{KEY}}` is replaced with the corresponding value.

For example, if you define `BODY` = `CBBE`, then a step with target meshes set to `{{BODY}}Body` would resolve to `CBBEBody` at execution time.

Up to 10 variables can be defined. Variables are saved with the script.

### Executing

- **Execute**: Runs every active (checked) step in order on the current project. If a batch mode is enabled, it repeats the steps for each batch item.
- **Execute Selected** (right-click a step): Runs only that single step on the current project. This does not use batch mode.

If a step fails, you are prompted whether to continue with the remaining steps or abort.

### Headless Execution

Saved scripts can also be run without opening the dialog by using the command-line automation flag:

```text
OutfitStudio --automation "Script Name" [batch inputs...]
```

Use the saved script name without the `.xml` extension. For batch scripts, positional arguments become batch inputs:

- **Folder Scan**: files or directories to process.
- **Slider Sets**: slider set or project names to process.

Non-batch scripts ignore positional arguments.

### Batch Operations

Expand the **Batch Operation** panel to process multiple files or slider sets automatically. Choose a mode:

#### None
Steps run once on the currently loaded project.

#### Folder Scan
Repeats the automation for every matching file in a folder.

| Setting | Description |
|---|---|
| **Folder** | The folder to scan for files. |
| **Extension** | File extension filter (e.g. `.nif`). Only files with this extension are processed. |
| **Include subdirectories** | Also scan subfolders recursively. |
| **File name filter** | Only process files whose name contains this text (case-insensitive substring match). |
| **Regex** | Treat the file name filter as a regular expression instead of a substring. |

For each file, the project is cleared, the file is imported, the automation steps run, and the project is cleared again. The following variables are automatically available in addition to your custom ones:

| Variable | Value |
|---|---|
| `{{BATCH_FILE}}` | Full path to the current file |
| `{{BATCH_NAME}}` | Filename without extension |
| `{{BATCH_FULLNAME}}` | Filename with extension |
| `{{BATCH_DIR}}` | Directory containing the file |

#### Slider Sets
Repeats the automation for every matching installed slider set (from BodySlide projects).

| Setting | Description |
|---|---|
| **Slider set filter** | Only process slider sets whose name contains this text. |
| **Regex** | Treat the filter as a regular expression. |

After applying the filter, a checklist dialog appears letting you select which slider sets to process. For each selected set, the project is loaded from the slider set file, the automation steps run, and the project is cleared.

| Variable | Value |
|---|---|
| `{{BATCH_FILE}}` | Path to the slider set project file |
| `{{BATCH_NAME}}` | Display name of the slider set |
| `{{BATCH_SET}}` | Same as `{{BATCH_NAME}}` |
| `{{BATCH_DIR}}` | Directory containing the slider set file |

---

## Creating an Automation

Type a new name into the script dropdown and click **Save** to create a new script. The dialog starts with an empty step list.

### Managing Steps

Right-click the step list to open the context menu:

- **Add Step**: Inserts a new step below the currently selected step. If no step is selected, adds to the end of the list.
- **Remove Step**: Deletes the selected step.
- **Move Up / Move Down**: Reorders the selected step. You can also press **Ctrl+Up** / **Ctrl+Down** in the step list.
- **Execute Selected**: Runs only the selected step (without batch mode).

Each step has an **Active** checkbox. Inactive steps are skipped during execution.

### Common Step Settings

Every step has these fields:

| Field | Description |
|---|---|
| **Type** | The operation to perform (see below). |
| **Active** | Whether this step runs during execution. |

| **Target Meshes** | Comma-separated list of shape names this step applies to. If empty, the step applies to all non-reference shapes. |
| **Regex** | If checked, the target meshes field is treated as a regular expression matched against shape names. |
| **Note** | A free-text note for your reference. Shown in error messages if the step fails. |

For **Set Extra Data** and **Delete Extra Data**, leaving **Target Meshes** empty targets the NIF root node instead of all non-reference shapes.

#### Choosing a step type

The **Type** field opens a popup listing the step types grouped by category. The categories start collapsed, so all of them fit on screen at once; expand one to see its types, or type into the **Filter** box at the top to narrow the list to matching names. Filtering expands the remaining groups automatically, and pressing **Enter** picks the first match. Arrow keys move through the tree and **Down** from the filter box jumps into it.

### Step Types

The dialog currently exposes **63** step types.

Many of the geometry, slider and mask steps work off the current vertex mask. The mask is a per-shape state of the loaded project, not part of a step, so it survives from one step to the next — build it with the **Masks** steps first and then run the step that consumes it.

#### Project & Reference

##### Clear Project
Resets the entire project to a blank state, removing all shapes, sliders, and data.

##### Load Reference
Loads a reference (base) shape from a file.

| Option | Description |
|---|---|
| **Source File** | Path to a `.nif` file or a slider set project file (`.osp`, `.xml`). |
| **Slider Set** | If loading from a project file, the name of the slider set to load. Leave empty to use template matching. |
| **Shape** | The specific shape name to use as the reference. Leave empty to use the default. |
| **Load All** | When using template matching (no set specified), load all shapes from the template. |
| **Merge Sliders** | Merge incoming slider data with existing sliders of the same name. |
| **Merge Zaps** | Merge incoming zap sliders with existing ones. |
| **Append New Sliders** | Add sliders from the reference that don't already exist in the project. |

##### Add Project
Adds shapes and sliders from another slider set project file into the current project.

| Option | Description |
|---|---|
| **Source File** | Path to the project file. |
| **Slider Set** | The slider set to add. |
| **Append New Sliders** | Add new sliders that aren't already in the project. |

##### Set Reference Shape
Designates an existing shape in the project as the reference (base) shape, or clears the current reference when **Unset Reference** is enabled.

| Option | Description |
|---|---|
| **Shape Name** | Name of the shape to set as reference. Ignored if **Unset Reference** is enabled. |
| **Unset Reference** | Clears the current reference instead of selecting a shape. |

##### Clear Reference
Removes the current reference shape from the project, keeping all other shapes and slider data intact.

##### Make Conversion Reference
Turns the currently applied slider values into a single conversion slider, the automation counterpart of *Slider ▸ Conversion ▸ Make Conversion Reference*. The deformed reference becomes the new base geometry and the new slider undoes that deformation, so a project built on the old body can be retargeted to the new one.

| Option | Description |
|---|---|
| **Slider Name** | Name of the conversion slider to create. It must not exist yet. |

Requires at least one non-zero slider value. **All other sliders of the project are deleted**, so put this step after the ones that set up the slider values and before anything that creates sliders you want to keep.

#### Shapes

##### Delete Shape
Deletes shapes from the project. Uses the **Target Meshes** filter to select which shapes to delete.

##### Rename Shape
Renames a single shape.

| Option | Description |
|---|---|
| **Old Name** | Current name of the shape. |
| **New Name** | New name for the shape. |

##### Duplicate Shape
Creates a copy of target shapes with a new name.

| Option | Description |
|---|---|
| **New Name** | Name for the duplicated shape. If duplicating multiple shapes, the original name is appended to avoid conflicts. |

##### Change Partitions
Changes target shape triangle assignments from one body partition to another.

| Option | Description |
|---|---|
| **Source Partition** | Existing partition/body part to change from. |
| **Destination Partition** | Partition/body part to change to. |

Matching triangle assignments are updated and any empty partitions are removed afterward.

##### Fix Bad Bones
Runs Outfit Studio's bad-bones fixer and applies the recommended corrections automatically to bones with inconsistent NIF transforms.

##### Fix Clipping
Pushes target geometry or slider morphs outward to reduce clipping against the current reference shape.

| Option | Description |
|---|---|
| **Mode** | **Shapes** fixes the current base geometry of target shapes. **Sliders** fixes each slider's morph data individually. |
| **Strength** | Clipping-fix strength (0% to 100%). |
| **Slider Names** | In **Sliders** mode, optional comma-separated list of sliders to process. Leave empty to process all non-zap/non-UV sliders. |

Requires a reference shape.

##### Mirror Shape
Mirrors target shapes along one or more axes.

| Option | Description |
|---|---|
| **Mirror X / Y / Z** | Which axes to mirror along. |
| **Swap Bones L↔R** | Swap left/right bone names (e.g. `NPC L Hand` ↔ `NPC R Hand`). |

##### Import File
Imports a mesh file into the project as a new shape.

| Option | Description |
|---|---|
| **File Path** | Path to a `.nif`, `.obj`, or `.fbx` file. |
| **From Folder** | If checked, imports all supported files from the specified folder. |
| **Load before batch file (step #1 only)** | In **Folder Scan** batch mode, if this is the first step, imports this file before each batch file so its root node and blocks become the base. |

##### Set Geometry Properties
Toggles geometry flags on target shapes.

| Option | Description |
|---|---|
| **Properties** | Add one or more property rows. Supported properties are `Skinned`, `Dynamic`, `Full Precision`, and `Sub Index`. |

`Skinned` adds or removes skinning data. `Dynamic` only applies to stream 100 NIFs. `Sub Index` requires stream 130 or newer. `Full Precision` only works on editable `BSTriShape` geometry.

##### Set Extra Data
Sets or creates named extra data blocks on target shapes, or on the NIF root node when **Target Meshes** is empty.

| Option | Description |
|---|---|
| **Block Type** | `NiStringExtraData`, `NiIntegerExtraData`, `NiFloatExtraData`, or `NiBooleanExtraData`. |
| **Name** | Extra data name. |
| **Value** | Value text. Boolean values accept `true/false`, `yes/no`, `on/off`, or `1/0`. |

If a block with the same name and type already exists, its value is updated. If the name already exists with a different type, automation logs a warning and does not create a duplicate block.

##### Delete Extra Data
Deletes named extra data blocks from target shapes, or from the NIF root node when **Target Meshes** is empty.

| Option | Description |
|---|---|
| **Name** | Extra data name to remove. |

##### Refine Mesh
Subdivides all shape meshes by splitting every triangle edge, increasing vertex and triangle density. Useful before conforming for better detail.

##### Recalculate Normals
Recalculates smooth vertex normals and tangents for the target shapes and writes them into the project right away. Unlike the *Shape ▸ Recalculate Normals* menu item, which only affects the viewport until the project is saved, this step modifies the loaded NIF data directly.

Leaving **Target Meshes** empty includes the reference shape, which a plain **Save Project** never touches. Vertices locked through a `LOCKEDNORM` extra data block are never changed.

| Option | Description |
|---|---|
| **Force** | Recalculate even if the shape's normals are locked. Also recalculates model space normals of Skyrim shapes, which are skipped otherwise. |
| **Seam Smoothing** | Sets the shape's *smooth seam normals* flag in the project before recalculating. Leave at *No change* to use each shape's current setting. |
| **Seam Angle** | Seam smoothing angle in degrees (default 60). Leave empty to keep the value of each shape. |
| **Lock Normals** | Sets the shape's *lock normals* flag in the project after recalculating, so later steps and the running application leave the normals alone. |

Setting any of the three options writes a `<Shape>` entry for the target shapes into the slider set, so the setting is saved with the project.

Run this step with all sliders at 0. **Save Project** rewrites the normals of non-reference shapes from the currently displayed meshes, so recalculating while a slider is applied causes the deformed normals to be saved.

##### Delete Vertices
Deletes vertices and the triangles that use them from the target shapes, the automation counterpart of *Shape ▸ Delete Vertices*.

| Option | Description |
|---|---|
| **Delete the masked vertices instead of the unmasked ones** | Off by default, matching the menu item: the mask protects vertices and everything else is deleted. |
| **Delete shapes that lose all of their triangles** | On by default. Turn it off to leave such shapes untouched instead of removing them. |

Without a mask every vertex counts as unmasked, so a step with the default settings and no preceding **Masks** step deletes the whole shape. Bones that no longer have any weights are cleaned up afterwards.

##### Separate Vertices
Moves the masked vertices of one shape into a new shape, the automation counterpart of *Shape ▸ Separate Vertices*.

| Option | Description |
|---|---|
| **New Shape Name** | Name of the new shape. It must not exist yet. |

Needs exactly one target mesh and a non-empty mask.

##### Merge Geometry
Merges the geometry of one shape into another one, the automation counterpart of *Shape ▸ Merge Geometry*. This step names both shapes itself and ignores **Target Meshes**.

| Option | Description |
|---|---|
| **Source Shape** | Name of the shape whose geometry is copied. |
| **Target Shape** | Name of the shape the geometry is merged into. |
| **Delete the source shape afterwards** | Removes the source shape once the merge succeeded. |

The step fails if the shaders or alpha properties of the two shapes do not match, if they are the same shape, or if the result would exceed the vertex or triangle limit of the NIF version. Mismatching partitions, segments, textures and transforms only produce a warning: matching slots and IDs are reconciled, missing ones are created, the texture paths of the target shape are kept, and mismatching transforms are applied to the geometry of both shapes and cleared, without moving the meshes.

##### Copy Segments/Partitions
Assigns every triangle of the target shapes to the segment or partition of the nearest reference triangle, clearing the existing ones. Requires a reference shape; leaving **Target Meshes** empty excludes it. Triangles that could not be matched are reported as a warning.

##### Symmetrize Vertices
Mirrors the selected kinds of data across the X axis for the unmasked vertices of the target shapes, the automation counterpart of *Shape ▸ Symmetry ▸ Symmetrize Vertices*. Masked vertices are left alone, just like in the vertex asymmetry dialog.

| Option | Description |
|---|---|
| **Vertex positions** | Mirror the rest positions of asymmetric vertex pairs. |
| **Unmatched vertices** | Also move vertices that have no mirrored counterpart onto the mirror plane. |
| **Slider data (all sliders)** | Mirror the morph data of every slider. |
| **Bone weights (all bones)** | Mirror the weights of every bone pair. |

Unlike the dialog, which lets you pick individual sliders and bones, the step applies its choice to all of them.

#### Transforms

##### Transform Shape
Applies movement, rotation, scaling, and/or inflation to target shapes.

| Option | Description |
|---|---|
| **Move X / Y / Z** | Translate by these amounts. |
| **Rotate X / Y / Z** | Rotate by these angles (degrees). |
| **Scale X / Y / Z** | Scale factors (1.0 = no change). |
| **Inflate X / Y / Z** | Move each vertex along its normal by this amount per axis. Useful for making shapes slightly larger/smaller while preserving form. |

##### Invert UVs
Flips UV coordinates for target shapes.

| Option | Description |
|---|---|
| **Invert U** | Flip the U (horizontal) texture coordinate. |
| **Invert V** | Flip the V (vertical) texture coordinate. |

##### Apply Transforms
Applies the shape-to-global transform of each target shape to its geometry and clears it afterwards, so the meshes don't effectively move. This is the same as setting the origin/rotation to 0,0,0 and the scale to 1.0 in the "Coordinates" tab of [[Shape Properties]] with the option to recalculate the geometry's coordinates enabled. Shapes without a transform are left alone.

##### Reset Transforms
Resets all shape transforms in the project back to identity (zero translation, zero rotation, unit scale).

##### Set Base Shape
Bakes the current slider values into the base shape geometry. After this, the shape's rest position reflects the currently applied slider values, and slider values are reset.

#### Sliders

##### Set Slider Values
Sets slider values without baking them into geometry.

| Option | Description |
|---|---|
| **Slider Names** | Comma-separated list of slider names to set. Leave empty to set all sliders. |
| **Value** | The value to set (0% to 100%). |

##### Conform Sliders
Generates slider data for target shapes by conforming them to the reference shape's slider deformations.

| Option | Description |
|---|---|
| **Proximity Radius** | Search radius for finding nearby reference vertices. |
| **Max Results** | Maximum number of nearby vertices to consider. |
| **Smooth Results** | Smooth the generated result deltas after conforming. |
| **Smoothing Iterations** | Number of smoothing passes to run when **Smooth Results** is enabled. |
| **Smoothing Strength** | Strength used for smoothing result deltas. |
| **No Squeeze** | Prevent vertices from being pushed inward. |
| **Solid Mode** | Treat the reference as a solid volume instead of a surface. |
| **Axis X / Y / Z** | Which axes to conform along. |
| **Fix Clipping** | Run clipping fix immediately after conforming each shape/slider delta. |
| **Clipping Strength** | Strength percentage used by the conform-time clipping fix. |
| **Slider Names** | Comma-separated list of specific sliders to conform. Leave empty for all non-zap/non-UV sliders. |

##### Set Slider Properties
Sets metadata and default values on existing sliders.

| Option | Description |
|---|---|
| **Slider Names** | Comma-separated list of sliders to update. Leave empty to apply to all sliders. |
| **Zap** | Mark matching sliders as zap sliders, or leave unchanged. |
| **Hidden** | Mark matching sliders as hidden, or leave unchanged. |
| **Default (Small) / Default (Big)** | Default values for regular sliders. Leave blank for no change. |
| **Default Zapped** | Shown when **Zap** is set to **Yes**. Controls whether matching zap sliders are zapped by default. |

##### Delete Slider
Removes a slider from the project.

| Option | Description |
|---|---|
| **Slider Names** | Comma-separated list of slider names to delete. |
| **Regex** | If checked, treats the name as a regular expression and deletes all matching sliders. |

##### Import Slider Data
Imports slider data from files.

Supported formats for single-file mode:
- **`.osd`** — Imports all slider diffs from the OSD file, auto-mapping to shapes by target name.
- **`.tri`** — Imports all morphs from the TRI file, auto-mapping to shapes by name. UV morphs are preserved.
- **`.nif`** / **`.obj`** / **`.fbx`** — Computes a slider diff by comparing the file's mesh geometry against the current shape. Requires a slider name (first entry of **Slider Names**, or the filename is used). Applied to all shapes that have a matching mesh in the file.
- **`.bsd`** — Imports binary slider data. Requires a slider name (same as above).

| Option | Description |
|---|---|
| **File/Folder** | Path to a slider data file (`.osd`, `.bsd`, `.nif`, `.obj`, `.fbx`, `.tri`), or a folder containing them. |
| **From Folder** | If checked, scans the folder for slider data files. For `.osd` and `.tri` files, all sliders/morphs are imported automatically (shape mapping is built into the file format). For `.nif`, `.obj`, `.fbx`, and `.bsd` files, filenames must follow the `ShapeName#SliderName.ext` naming pattern. |
| **Merge Only** | Only import data for sliders that already exist (don't create new ones). |
| **Slider Names** | Comma-separated list of specific sliders to import. For `.osd`/`.tri`, filters which sliders to import. For `.nif`/`.obj`/`.fbx`/`.bsd`, the first entry is used as the slider name. Leave empty to import all (`.osd`/`.tri`) or use the filename as slider name (others). |

##### New Zap Slider
Creates a zap slider that removes the **unmasked** vertices of the target shapes, so the mask marks what to keep. The automation counterpart of *Slider ▸ New Zap*.

| Option | Description |
|---|---|
| **Slider Name** | Name of the new zap. It must not exist yet. |

Shapes without any unmasked vertices are skipped.

##### New Combined Slider
Creates a new slider from the combined result of the currently applied slider values, the automation counterpart of *Slider ▸ New Combined Slider*.

| Option | Description |
|---|---|
| **Slider Name** | Name of the new slider. It must not exist yet. |

##### Clone Slider
Creates a copy of a slider, including its data for all shapes.

| Option | Description |
|---|---|
| **Source Slider** | Name of the slider to clone. |
| **New Slider** | Name of the copy. It must not exist yet. |

##### Negate Slider
Inverts the morph data of the given sliders for the target shapes.

| Option | Description |
|---|---|
| **Slider Names** | Comma-separated list of sliders to negate. |

##### Clear Slider Data
Removes the slider morph data of the target shapes without deleting the sliders themselves.

| Option | Description |
|---|---|
| **Slider Names** | Comma-separated list of sliders to clear. Leave empty to clear every slider of the project. |
| **Keep the slider data of masked vertices** | On by default. With a mask set, only the unmasked vertices lose their data; without one, the whole slider is cleared for the shape. |

#### Bones

##### Copy Bone Weights
Copies bone weights from the reference shape to target shapes.

| Option | Description |
|---|---|
| **Proximity Radius** | Search radius for finding nearby reference vertices. |
| **Max Results** | Maximum number of nearby vertices to consider. |
| **Bone List** | Comma-separated list of specific bones to copy. Leave empty for all bones. |

##### Delete Bones
Removes bones or bone weights.

| Option | Description |
|---|---|
| **Bone Names** | Comma-separated list of bone names to delete. |
| **From Entire Project** | If checked, deletes the bone entirely. If unchecked, only removes weights from target shapes. |

##### Add Custom Bone
Adds a new custom bone to the project.

| Option | Description |
|---|---|
| **Bone Name** | Name of the new bone. |
| **Parent** | Name of the parent bone. |
| **Translation X / Y / Z** | Position of the bone. |
| **Rotation X / Y / Z** | Rotation of the bone. |

##### Edit Custom Bone
Modifies an existing custom bone's transform and parent.

| Option | Description |
|---|---|
| **Bone Name** | Name of the bone to edit (must not be a standard skeleton bone). |
| **Parent** | New parent bone name. |
| **Translation X / Y / Z** | New position. |
| **Rotation X / Y / Z** | New rotation. |

##### Remove Skinning
Removes all bone weight data from target shapes. If no target shapes are specified, removes skinning from all shapes.

##### Apply Pose
Applies a loaded pose to the mesh geometry, permanently deforming it.

| Option | Description |
|---|---|
| **Pose Name** | Name of the pose (must be loaded in Outfit Studio's pose list). |

##### Add Bone
Adds bone references from the loaded skeleton to every shape of the project, the automation counterpart of *Bones ▸ Add Bone*. Unlike **Add Custom Bone**, this only references bones that already exist in the skeleton.

| Option | Description |
|---|---|
| **Bone Names** | Comma-separated list of bone names. Names that are not in the loaded skeleton are skipped with a warning. |

##### Transfer Selected Weights
Copies bone weights vertex by vertex from the reference shape, the automation counterpart of *Bones ▸ Transfer Selected Weights*. Unlike **Copy Bone Weights**, which searches for nearby reference vertices, this needs the target shape to have the same vertex count as the reference.

| Option | Description |
|---|---|
| **Bone Names** | Comma-separated list of bones to transfer. Leave empty to transfer every bone of the reference. |
| **Keep the weights of masked vertices** | On by default. The mask acts as a per-vertex blend factor: fully masked vertices keep the weights they already have. |

Leaving **Target Meshes** empty excludes the reference shape. Shapes with a different vertex count are skipped with a warning.

##### Set Bone Transform
Recalculates one of a bone's two transforms from the other one, the automation counterpart of *Bones ▸ Set Bone as Skin / Set Bone as Node*.

| Option | Description |
|---|---|
| **Bone Names** | Comma-separated list of bones to recalculate. |
| **Mode** | *Set bone as skin* derives the skin-to-bone transform from the node transform, *set bone as node* does the opposite. |

#### Shaders

##### Set Shader Properties
Sets one or more shader values on target shapes.

| Option | Description |
|---|---|
| **Properties** | Add one or more property rows. Supported properties are `Shader Type`, `Specular Color`, `Specular Strength`, `Specular Power`, `Emissive Color`, `Emissive Multiple`, `Alpha`, `Env Map Scale`, `Eye Cubemap Scale`, `UV Offset`, `UV Scale`, `Lighting Effect 1`, `Lighting Effect 2`, `Skin Tint Color`, `Hair Tint Color`, and `Refraction Strength`. |

Properties that do not apply to the current shader or NIF version are skipped.

##### Set Texture Paths
Sets one or more texture slots on target shapes.

| Option | Description |
|---|---|
| **Paths** | Add one or more texture rows, each with a texture slot and path. |
| **Texture Slots** | Named slots include `Diffuse`, `Normal`, `Glow/Skin`, `Parallax`, `Environment`, `Env Mask`, and `Specular`. Raw slots `6` and `8` through `12` are also available for version-specific shaders. |

Only shapes with a `BSShaderTextureSet`-capable shader, and only slots valid for the current NIF version, are updated.

#### Saving & Exporting

##### Save Project
Saves the current project as a BodySlide slider set.

| Option | Description |
|---|---|
| **Display Name** | Name shown in BodySlide. |
| **Slider Set File** | Path to the `.osp` project file. |
| **Output File** | The game output `.nif` filename. |
| **Output Data Path** | The game data path for the output. |
| **Shape Data Folder** | Folder for shape data files (`.osd` and base `.nif`). |
| **Shape Data File** | The base shape data filename. |
| **Generate Weights** | Create `_0.nif` and `_1.nif` weight variants. |
| **Copy Reference** | Include the reference shape in the output. |

**Batch-specific options** (only relevant in Slider Sets batch mode):

| Option | Description |
|---|---|
| **Use original project** | Instead of using manual settings, reads the save fields from the original slider set being processed. |
| **Replace From / To** | After loading original settings, replace all occurrences of one string with another in the output fields. Useful for redirecting output paths. |
| **Suffix** | Append a suffix to the display name, shape data folder, and slider set filename. |
| **Copy reference from project** | Only copy the reference shape if the loaded project had one. Automatically enabled when "Use original project" is checked. |
| **Ref shape names** | Comma-separated list of shape names. Only copy the reference if its name matches one of these. Leave empty to match any reference shape. |

##### Export File
Exports the project to a file.

| Option | Description |
|---|---|
| **File Path** | Output path. Supported formats: `.nif`, `.obj`, `.fbx`, `.osd`, `.tri`. For `.osd` and `.tri`, the slider data (morphs) is exported rather than mesh geometry. In batch mode with a folder-type path, the original filename is used. |
| **Include Reference** | Include the reference shape in the export (NIF only). |
| **Prefix** | Prepend this text to the output filename. |
| **Suffix** | Append this text to the output filename (before extension). |

**Batch-specific option:**

| Option | Description |
|---|---|
| **Use original file path** | Export directly to the path of the file that was loaded by the batch, overwriting it. |

#### Masks

##### Clear Mask
Clears the current vertex mask on target shapes. Uses **Target Meshes** to choose which shapes to clear.

##### Load Mask
Loads a vertex mask from a mask file and applies it to target shapes.

| Option | Description |
|---|---|
| **Mask File** | Path to the mask file. |
| **Mask Name** | Name of the mask within the file. Must match the file's stored mask name. |

##### Save Mask
Writes the current mask of the target shapes into a named entry of an XML mask file, ready to be read back by **Load Mask**.

| Option | Description |
|---|---|
| **Mask File** | Path of the file to write. Relative paths are resolved against the project folder; missing folders are created. |
| **Mask Name** | Name of the entry inside the file. An entry of the same name is replaced. |
| **Keep the other entries of an existing file** | On by default. Turn it off to overwrite the file with just this entry. |

##### Invert Mask
Inverts the mask of the target shapes: fully masked vertices become unmasked and the other way around.

##### Grow/Shrink Mask
Moves the mask border of the target shapes outwards or inwards, like the *Mask ▸ Grow/Shrink Mask* menu items.

| Option | Description |
|---|---|
| **Mode** | *Grow* extends the mask, *Shrink* pulls it back. |
| **Iterations** | How many times the border is moved by one ring of vertices. |

Each iteration first masks or unmasks the welded duplicates of the border vertices and only moves a full ring when there are none left, so the first iteration on a fresh mask usually only closes UV seams.

##### Mask Weighted Vertices
Replaces the mask of the target shapes with the vertices that have a weight greater than zero for any of their bones. Everything else becomes unmasked.

##### Mask Bone-Weighted Vertices
Same as above, but only for the given bones.

| Option | Description |
|---|---|
| **Bone Names** | Comma-separated list of bones whose weighted vertices are masked. |

##### Mask Slider-Affected Vertices
Replaces the mask of the target shapes with the vertices that the given slider has morph data for.

| Option | Description |
|---|---|
| **Slider Name** | Name of the slider to read the affected vertices from. |

##### Mask Asymmetric
Masks everything **except** the asymmetric parts of the target shapes, so the steps that follow only work on those. This matches *Shape ▸ Symmetry ▸ Mask Asymmetric Vertices/Triangles*, where the mask protects the symmetric part of the mesh.

| Option | Description |
|---|---|
| **Mode** | *Asymmetric triangles* looks at the triangle layout only and ignores the checkboxes. *Asymmetric vertices* compares the selected kinds of data between mirrored vertex pairs. |
| **Vertex positions** | Vertex pairs whose rest positions do not mirror each other. |
| **Unmatched vertices** | Vertices that have no mirrored counterpart at all. |
| **Slider data (all sliders)** | Vertex pairs whose morph data does not mirror, for any slider. |
| **Bone weights (all bones)** | Vertex pairs whose weights do not mirror, for any bone pair. |

Like the menu items, this step only ever adds to the mask — it never unmasks anything, so it narrows an existing mask instead of replacing it.

#### Nodes

##### Remove Unused Nodes
Deletes unreferenced NIF nodes from the current project.

#### Script

These two step types have no menu equivalent; they exist to make longer scripts easier to follow and to parameterize.

##### Set Variable
Defines a `{{KEY}}` placeholder for the steps that follow.

| Option | Description |
|---|---|
| **Name** | Name of the variable, without the curly braces. |
| **Value** | Value to substitute. Placeholders of variables that are already known are resolved first, so variables can be built from other variables. |

The placeholder variables from the collapsible section at the bottom of the dialog are substituted once before the run, so a name that is already defined there has been replaced everywhere by the time the step executes and cannot be overridden — the step logs a warning in that case. In batch mode the runtime variables are reset for every file or slider set.

##### Log Message
Writes a message to the automation log.

| Option | Description |
|---|---|
| **Message** | Text to write. Placeholders are substituted, which makes this the simplest way to check what a variable resolved to. |
| **Level** | *Message*, *Warning* or *Error*. Warnings and errors are shown in a dialog outside of headless runs, but the step itself never fails. |

---

## Tips

- Use **placeholder variables** to make scripts reusable. For example, define `{{OUTPUT}}` as your output folder and reference it in export paths.
- In batch mode, combine `{{BATCH_NAME}}` with custom variables to build dynamic paths: `{{OUTPUT}}/{{BATCH_NAME}}_modified.nif`.
- Use the **Regex** option on target meshes to apply a step to shapes matching a pattern, e.g. `Body|Hands|Feet`.
- Steps that fail show the step's **Note** in the error dialog — use notes to remind yourself what each step does.
- The **Execute Selected** right-click option is useful for testing individual steps before running the full script.
