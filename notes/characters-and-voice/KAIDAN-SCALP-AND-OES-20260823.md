# Kaidan — missing scalp + OES in the prison (2026-08-23)

Profile: `DEEZ CS NUTZ`. MO2 was closed for this scan. Nothing was written.

---

## 1. The missing scalp — incomplete re-slot of the Yasha wig

### Cause

`Kaidan Wig Slot 44 Patch.esp` (built 2026-08-17) moved the wig off the hair slot:

| Record | Before (`_Fuse00HairPack01.esp` / `HSFVorstag.esp`) | After (patch, current winner) |
|---|---|---|
| `_Fuse00_Yasha_WIG_Armo` `000852:_Fuse00HairPack01.esp` | `Hair` (31) | `16384` = slot 44 |
| `_Fuse00_Yasha_WIG_Arma` `000851:_Fuse00HairPack01.esp` | `Hair, LongHair, Ears` (31/41/43) | `16384` = slot 44 |

The **mesh was never re-partitioned to match.**

`meshes\Fuse00\HairPack01\Yasha\Yasha WIG Male.nif`
(VFS winner: `Authoria - Kaidan Visual Replacer`, loose; also in `Valkyr HDT-SMP Hairstyles`, `Fuse00 HairPack 01`)

13 shapes. Block census: `NiSkinInstance x12`, **`BSDismemberSkinInstance x1`**.

- 12 shapes carry a plain `NiSkinInstance` — **no dismember partition, so they can never be culled.** These are the hair strands, braids, bun, front, low_1..low_6, and the two collision shapes. They render.
- **`_Fuse00_Yasha_ScalpMale` is the only partitioned shape — partition `31 (SBP_31_HAIR)`, flags 257.**

An armor shape is only drawn when its dismember partition corresponds to a biped slot the item
actually occupies. The wig now occupies slot 44; its scalp cap still claims slot 31. Mismatch →
**that one shape is culled.** Hair renders, scalp does not.

This is the standard incomplete-re-slot failure: ARMO slots + ARMA slots + NIF partition must all agree.

### Timeline

- **before 2026-08-17** — wig on slot 31, mesh partition 31 → match → scalp rendered.
- **2026-08-17 16:38** — `Kaidan Wig Slot 44 Patch.esp` re-slots ARMO + ARMA to 44. Mesh untouched.
- **from then on** — scalp culled.

### Why the head's own baked scalp does not cover it

Kaidan's facegen — `meshes\actors\character\facegendata\facegeom\0Kaidan.esp\00002F9A.nif`
(winner: `Authoria - Kaidan Visual Replacer`, loose; also in `0Kaidan.bsa`) — has 9 baked shapes:

| shape | NiAVObject flags | state |
|---|---|---|
| `karlach_hair` | `0x8000F` (**+0x1 = Hidden**) | hidden |
| `karlach_hair_2` | `0x8000F` (**+0x1 = Hidden**) | hidden |
| `karlach_scalp` | `0x8000E` (default) | visible, partition 31 |
| `VorstagHead` / `Scar` / `Eyes` / `Lashes` / `Brows` / `Mouth` | — | visible |

The two baked Karlach hair shapes were deliberately flagged Hidden so the Yasha wig could be the
only hair. `karlach_scalp` is still visible, but it is Karlach's scalp cap shaped to the Karlach
hairline — it does not fill the Yasha wig's parting.

### Confirmed NOT the cause

- Scalp mesh + both scalp textures are present and win cleanly from `Authoria - Kaidan Visual Replacer`.
- `karlach_scalp` head part `00000C:HSFVorstag.esp` is intact, valid races `VorstagList`, uncontested (1 plugin).
- Nothing in any Kaidan outfit occupies slot 31 — resolved all 13 armors across the 10 Kaidan OES
  outfits: cuirass, gauntlets, boots, backpack, tunics, gloves, wig. No helmet, hood or circlet.
- `BanditHelmetAAA` `0F13CF:Skyrim.esm`, still listed in the wig's Armature, is Argonian-only —
  it never matches `VorstagRace`, so it is inert (harmless leftover).
- Pre-Thalmor Kaidan `000800:Kaidan pre Thalmor.esp` has **no facegen file of its own**, but that is
  correct — it templates `002F9A:0Kaidan.esp` with `Traits` set, so it uses the main facegen.

### Fix A (recommended) — keep slot 44, re-partition the mesh

Set `_Fuse00_Yasha_ScalpMale`'s dismember partition from `31` → `44`.

```
housecarl_nif_set
  mesh_path = meshes\Fuse00\HairPack01\Yasha\Yasha WIG Male.nif
  op        = set_partition
  target    = _Fuse00_Yasha_ScalpMale
  body_part_id = 44
```

Default lane writes a new houseCARL mod folder — must be enabled and sorted **above**
`Authoria - Kaidan Visual Replacer`. Keeps the whole point of the 08-17 patch: a helmet no longer
evicts the wig.

### Fix B — revert the wig to slot 31

Undo the 08-17 patch. Scalp returns with no mesh edit, and the baked `karlach_scalp` gets hidden
again as a bonus. Cost: any helmet evicts the wig again — the exact problem the patch was built for.

---

## 2. OES is dressing him in the prison

`overwrite\SKSE\Plugins\OutfitEquipmentSystemNGData.json` (mtime 2026-08-02 05:00) now holds:

```
"0x2f9c|0Kaidan.esp": {
  "currentOutfitName": "Kaidan - base",
  "locationBasedOutfits": { 28 entries }
}
```

`0x2f9c` is **KaidanRef**, not the NPC base — correct key, so it is live.

Tracked actors are now: Lucien, Auri, the Player, **and Kaidan**. The 2026-08-02 note
(`oes-permanent-visuals-via-skin`) recorded Kaidan as *not* tracked — that is out of date.

### Proof it is firing right now

`Documents\My Games\Skyrim Special Edition\SKSE\SkyrimOutfitEquipmentSystemNG.log`, last line,
**today 04:23:41**:

```
Updated outfit for actor Shackled Prisoner, ID: 2164273052
Armors equipped: 5
```

`2164273052` = `0x81002F9C` — low bytes `2F9C` = KaidanRef. "Shackled Prisoner" is prison Kaidan.
5 armors = exactly the `Kaidan - base` outfit (Infantry Cuirass + Gauntlets + Boots +
Adventurer's Magic Bag + Yasha WIG).

So OES is putting his full late-game kit on him while he is still chained up.

### Removing him does NOT cost him his hair

The KIF self-heal is already in place in `Authoria - Vorstag Headpart Races.esp`:

- `KaidanOutfitDefaultLL` `B43231` → single base entry = the Yasha wig
- `KaidanChanging` `B4322D` → single item = the Yasha wig

Kaidan - Immersive Features rebuilds those with `Revert()` + `AddForm()`, and `Revert()` restores
the ESP base entries. The wig reinstalls itself on every wardrobe change without OES.

### Removal options

1. **Co-save edit** — proven on 2026-08-22 (54 co-saves, player untracked). Delete Kaidan's whole
   field-3 assignment record from the `SOAA` subchunk of the `tzOc` plugin chunk, decrement both
   the subchunk and plugin chunk lengths. 64 co-saves currently in
   `profiles\DEEZ CS NUTZ\saves`. One shot, preserves the 25 outfits and the other 3 actors.
2. **MCM** — clear his assignment in game. Simpler, but it is his current outfit plus 28
   location entries to clear by hand.

### Putting him back after the prison

Never Import the on-disk JSON as it sits — Import is a whole-document replace against the
authoritative co-save. Correct order is always:

1. MCM → **Export to JSON**
2. add Kaidan's assignment block to that fresh export (preserved below)
3. MCM → **Import from JSON**

Write UTF-8 **without BOM**. A genuine export starts with byte `0x7B`.

The 10 `Kaidan - *` outfit definitions live in the `outfits` array and are untouched by removing
the assignment — only the assignment needs restoring. His assignment block is preserved verbatim in
`_tools\oes-cosave\kaidan-oes-assignment.json` (written UTF-8 no BOM, first byte `0x7B`) —
paste it into the `actorOutfitAssignments` object of a fresh MCM export. Do not rely on
`overwrite\SKSE\Plugins\OutfitEquipmentSystemNGData.json` keeping it; the DLL rewrites that file
on the next save and Kaidan will drop out of it.

---

## 3. What was actually done — 2026-08-23

MO2 and the game were closed for every write.

### Scalp — DONE

- Backed up the wig mesh to
  `Yasha WIG Male.nif.bak-pre-slot44-partition-20260823` (same folder, 7,321,366 bytes).
- `housecarl_nif_set` `set_partition` on `_Fuse00_Yasha_ScalpMale`: **`[0]=31 -> [0]=44`**.
- Written **in place** into `Authoria - Kaidan Visual Replacer` rather than as a new mod folder.
  Deliberate: it avoids inserting a mod into the load order across 4 profiles, and the file already
  wins the VFS. No load-order change of any kind was made.
- Verified by the tool's two gates: no header change, only block `[353]` touched, net size delta
  0 bytes, block census intact, value re-read after reload.

To revert: restore the `.bak-pre-slot44-partition-20260823` copy over the live file.

### OES — DONE

Tool written: `_tools\oes-cosave\oes_cosave.py` (`scan` / `remove <needle> [--apply]`).
It walks every plugin chunk to EOF and refuses any file whose walk does not land exactly on EOF.

Run against `profiles\DEEZ CS NUTZ\saves`:

| result | count |
|---|---|
| Kaidan assignment removed (727 bytes each) | **61** |
| no OES data present, untouched | 3 |
| total co-saves | 64 |

Per-file verification, run **before** anything was written:

- rewritten file re-walks to EOF
- outfit count unchanged (25)
- assignment count exactly one lower
- `enabled` and both inventory-management modes unchanged
- target string absent afterwards
- file shrank by exactly the cut size

Post-run re-scan of all 64: **25 outfits, 2 assignments (Auri + Lucien)** on the 61, and the
3 empty ones unchanged. Per-file backups written as `.bak-pre-oes-kaidan-20260823` (~73 MB total,
safe to prune once a session confirms good).

Note the player was already untracked in the co-saves from the 2026-08-22 run — only the stale
on-disk JSON still lists `0x14|Skyrim.esm`.

### Watch item — KIF wardrobe now has nothing but the wig

`KaidanOutfitDefaultLL` and the other KIF wardrobe lists hold **one entry: the wig**. That was fine
while OES was overriding his visible outfit on top. With OES no longer tracking him, if a Kaidan -
Immersive Features dialogue fragment fires a wardrobe change he will end up wearing the wig and
nothing else.

If that shows up before the prison is done, the options are to switch the KIF wardrobe off in its
MCM, or to add his base clothes alongside the wig in those leveled lists. Not done — out of scope
for today and it would need a decision on what he should be wearing.
