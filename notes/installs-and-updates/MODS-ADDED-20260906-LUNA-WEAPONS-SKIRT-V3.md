# 2026-09-06 - Luna's favorite weapons x3, Magic Pariah skirt tune v3

Both requests came from the save (`Save33`, 08:43, Luna, level 1, UBE Breton). The inventory was
read straight out of the .ess with the new `_tools\save-forensics\save_inventory.py`.

## 1. Weapons - `mods\Authoria - Luna Weapon Buffs` (new, no plugin)

Favorited items in the save: Silver Keyblade (equipped), Silver Great Keyblade, DD - Einar Bow,
Dwemer Quiver (armor), Sketchbook (book). The three weapons get three times their current damage
through one SkyPatcher INI (`SKSE\Plugins\SkyPatcher\weapon\Authoria - Luna Weapon Buffs\Luna favorites.ini`):

| weapon | record | before | after |
|---|---|---|---|
| Silver Keyblade (1H) | `1295D6:Unslaad.esm` | 180 | 540 |
| Silver Great Keyblade (2H) | `1295DA:Unslaad.esm` | 290 | 870 |
| DD - Einar Bow | `000D62:DD - Weapon Vergi Armoury.esp` | 360 | 1080 |

Crit damage set to the same numbers (Requiem keeps crit = base). For scale, Requiem's Daedric
Sword is 90, Daedric Greatsword 144, Daedric Heavy Bow 120 - the three were already 2-3x top tier.
No SkyPatcher weapon INI existed before this one. Verified with houseCARL's SkyPatcher reader
(all three lines APPLIED, before -> after as above) and the layer scan (no conflicts, no ITM).

Registered in all six profiles' `modlist.txt` directly below `Authoria - Requiem - Companions Giant`
(enabled in DEEEZ NUTTZZZ / DEEZ CS NUTZ / DEEZ CS NUTZ - PBR / PICTA EXPERIMENT, disabled in the two
Requiem Reforged profiles). Backups `modlist.txt.bak-lunabuffs-20260906`. No plugin, so loadorder /
plugins / plugingroups untouched and no Outfit Wheeler reindex needed. Script:
`_tools\mod-install-helpers\register_luna_buffs.py`.

To retune: edit the numbers in the INI. To remove: disable the mod. Save-safe either way.

## 2. Skirt - Magic Pariah skirt tune v3

Luna wears Magic Pariah Top + Skirt (`000800/000801:Magic Pariah.esp`), Red Jenny's boots, kneepads
and leg ropes, Vergi jewelry, the Tullius wig, the Einar backpack.

Why the butt poked through (measured on the mesh): from z 64 up the BACK of the skirt was ~50% pelvis
/ spine + ~50% row-1 anchor weight, i.e. rigid with the pelvis over the whole butt, and the only
colliders were thigh and calf shapes - nothing at the hips for the moving part to rest on.

Changes (`_tools\magic-pariah-mm-rig\build_v3.py --apply` + `make_xml.py --install`, backups `*.bak-v2-20260906`):
- weights: the physics chain takes over higher, most in the back (body weight gone below z 71 back /
  63 front; the static row-1 share handed to row 2 below z 73 back / 66 front). The flap now hinges
  at the hip line (the row-1 bones, z 70.4). Applied to Skirt Lower, Skirt Upper and the collision proxy.
- new collider `CollButt`: the body's rear hips (z 54-78) cut from the same lane's top mesh
  (~950 spheres UBE / ~850 3BA), skinned to pelvis, thighs and the two Butt bones; the skirt proxy
  now collides with it. Flat `NPC L/R Butt` nodes added to the !UBE nifs.
- xml v3 (both copies identical): joints x -0.45..0.9, y/z +-0.3..0.4 rad, springs 6/4/2 (v2 15/10/6),
  damping 0.3 -> 0.15, rings 12/9/7 with wider play, bone damping halved, gravity 1.0.
- the converter's empty-texture placeholder shaders on CollThigh / CollCalves / MMSkirtProxy in the
  !UBE nifs were stripped (the purple-square trap), flags set to 0xE.

Files: `Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah\magic pariah skirt HDT_0/_1.nif` (live for Luna),
`Authoria - Bodyslide Output - UBE\Meshes\clothes\magic pariah\Magic Pariah Skirt HDT_0/_1.nif`,
`Magic Pariah - Meadowlark Physics\CalienteTools\BodySlide\ShapeData\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif`,
and the two xmls. Caveat: CollButt has no BodySlide slider data - after a BodySlide rebuild and
converter run, re-run `build_v3.py --apply` to recut it from the built body.

In-game result: not yet tested. Next step if still too stiff: springs toward 0, wider row 2.

## 3. Skirt + sleeves v4 - Helga-style cloth (same day, follow-up request)

User: the Pariah skirt and sleeves "move as one big piece"; wants the cloth feel of the Helga dress skirt.
Measured on Helga's dress: 14 columns x 9 rows of light bones (mass 0.13), ~4 bones per vertex spread
over 2 columns x 3 rows, zero-stiffness hinges, columns tethered only within 2 units / 1 rad, bone
damping 0.75/0.85. The Pariah rig had 12 columns x 3 dynamic rows, 7x heavier bones, stiff spring
rings (that is the "one piece"), and one bone per sleeve.

Built `build_v4.py --apply` (all 5 skirt nifs + all 5 top nifs, backups `*.bak-v3-20260906`) and
`make_xml_v4.py --install` (4 xmls): skirt grid 14 x 7 (`psk_*`), sleeve grids 8 x 4 (`slvL_*`/`slvR_*`)
around each forearm, Helga's xml numbers. Cross-checked: every bone the xmls name exists in the nifs
and vice versa (112 skirt, 80 sleeve bones). NIF rotation convention verified on Helga's nested bones
(row-major as read, v' = R v + T, parent-then-child) before trusting the new bone frames.
In-game result: not yet tested.

**v4 fix (same evening):** user test: skirt and sleeves much better, but the RIGHT sleeve sank into the
ground. Cause: in the top xml the right sleeve's anchor row was emitted after the left sleeve's
`<bone-default>` (mass 0.13) blocks, so FSMP made those 8 anchors free dynamic bodies with no
constraint to the forearm and they fell. Fixed in make_xml_v4.py (both anchor rows are declared before
any bone-default); both top xmls reinstalled and verified (16 anchors before the first default).
