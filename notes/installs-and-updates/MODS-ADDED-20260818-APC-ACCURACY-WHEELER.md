# Mods added / updated 2026-08-18

Profile worked on: **DEEZ CS NUTZ** (the active one). MO2 was closed for every write.

Backups taken first:

- All four profiles: `modlist.txt`, `plugins.txt`, `loadorder.txt`, `plugingroups.txt` → suffix `.bak-apc-20260818`. Sizes verified.
- Outfit Wheeler 2.6 mod folder → `_backups\Outfit Wheeler - Dynamic Equipment Manager.bak-2.6-20260818`. 7 files, byte count verified.

---

## 1. Outfit Wheeler — Dynamic Equipment Manager 2.6 → 2.7

**Installed and enabled.**

The author published no changelog, so the update was derived by diffing the build against 2.6.

- All five interface files are **byte-identical** to 2.6. Nothing changed in the UI.
- Only the native plugin changed, and one new small ESP was added.

New in 2.7 (from the build's own symbols):

- `StashAllOutfitsToWardrobe` / `RetrieveAllOutfitsToPlayer`
- `StashSlotOutfit` / `RetrieveSlotOutfit`
- `StashWheelOutfits` / `RetrieveWheelOutfits`
- Deleting a slot or a wheel now returns its items to your inventory instead of dropping the data.

So 2.7 adds a wardrobe: stored outfits can physically leave your inventory and live in a hidden chest.

### The new plugin

`OutfitWheeler.esp` — required by everything in that list above. Without it the wardrobe calls fail
with "make sure OutfitWheeler.esp is enabled"; the wheel itself still works.

Verified contents — it defines exactly two records and overrides nothing:

| Record | What it is |
| --- | --- |
| `OutfitWheeler_HoldingCell` | a new interior cell, not an override |
| `OutfitWheeler_WardrobeChestRef` | one `PlayerHouseChest` container placed in that cell |

Integrity sweep: 0 dangling references, 0 missing masters. Its masters are all base game plus the
Survival Mode CC file, which all load first anyway.

Placement:

- modlist, all 4 profiles: above `Prisma UI - Next-Gen Web UI Framework`
- plugins/loadorder (CS profile): directly after `SpellHotbar.esp`
- plugingroups: group `Interface - User Interface`, alongside `Wheeler - UI.esp` and `SpellHotbar.esp`

### Plugin slot cost

The ESP is a **full** plugin — its records sit outside the light-plugin ID range, so it cannot be
ESL-flagged without compacting it.

- Before: 252 / 254 full slots.
- After: **253 / 254 full slots. One free.**

Compaction looks feasible if the slot is needed later: the build has **no hard-coded form ID** for
the chest (searched the binary for the immediate — zero hits); it looks the chest up by its editor ID
string, and editor IDs survive compaction. Not done today, because it is an edit to someone else's
plugin to save one slot while a slot was still free.

### Interaction worth watching

`Skyrim Outfit Equipment System NG` is enabled. Outfit Wheeler's new wardrobe **physically moves
items** out of the player inventory. If it stashes a piece that OES is using for a permanent visual,
that visual can drop. Worth one look on the first test session.

---

## 2. Accurate Projectile Collision 2.0.0

**Installed and enabled.** New mod. DLL + INI + PDB, no plugin, so no load order change.

Placement: modlist, above `Precision - Accurate Melee Collisions`, in the
`Gameplay - Frameworks` block. Enabled in CS only; present but disabled in the other three profiles
so activating them never appends it above the flat maps.

Settings left at defaults: arrows on, spells on, normal logging.

### Requirement check

- Requires Precision. Installed Precision is **2.0.4**, which is the newest there is (Jan 2023).
- The build asks Precision for **API version 4**. The Precision log already shows version 4 being
  served to another mod, so that interface is live and correct.
- Address Library has the file for the installed game build. Fine.

### Conflict check across the archery stack

Every SKSE plugin in the mod folder was scanned for Precision API use — 351 DLLs.

| Finding | Result |
| --- | --- |
| Mods using Precision's API | Parrying RPG, SCAR V2 |
| Mods registering a Precision **collision-layer** callback | **none** — this is what APC uses, so it has that surface to itself |
| Core Impact Framework's hooks | it hooks arrow and missile collision at the vtable level; APC does **not** hook there at all, it works through Precision's filter instead — different stage, they chain |
| Smooth Arrow Trails and Fixes | fixes the arrow's *own* collision box after it lands. Different thing. Same author. No overlap |

No conflict found.

### The two locational damage mods

Both are enabled and both are set to act on arrows.

- **Archery Locational Damage 2.1.5**, driven by the big config that Skyrim Arrow Overhaul ships.
  That config resolves the body part by matching skeleton node names against regular expressions,
  and then branches on arrow type and on what armour covers that spot.
- **Locational Damage AE 1.2.1** — its log confirms projectile damage is on, with head, magicka,
  stagger and interrupt effects live.

Both work off *where the arrow actually landed*. APC improves that input. Neither is broken by it.

### Arrow keywords survived the Requiem patching

The Arrow Overhaul config is entirely keyword-driven, so if Requiem's overrides had stripped the
arrow-type keywords the whole config would silently do nothing. Checked the load-order winners:

- 101 arrow records carry Arrow Overhaul's arrow-type keywords. The Authoria Arrow Overhaul/Requiem
  patch wins 95 of them, the Reqtificator output 5, Arrow Overhaul itself 1.
- Spot-checked iron, steel and daedric arrows. Each winner carries **both** the Requiem
  armour-piercing tier and ammo weight keywords **and** the Arrow Overhaul arrow type.

So the config still fires. Nothing to fix.

### Expect this gameplay change

This is the honest consequence, not a bug.

1. Arrows will now hit arms and legs that they used to pass straight through.
2. The Arrow Overhaul config sets most arrow types to **zero damage and a bounce** against heavy
   armour on limbs, and against heavy helmets and cuirasses.
3. So archery against heavily armoured enemies will feel weaker than before. Shot placement starts
   to matter.
4. Shields should deflect more reliably, since the config has a shield rule that also keys off the
   hit location.

If that lands too harsh, the lever is the Arrow Overhaul config's limb multipliers, not APC.

---

## 3. Accuracy (Localized Combat Damage) 1.0.0

**Installed but left DISABLED in all four profiles.** Nothing about it is live.

### Why it is off

It hard-requires **Core Impact Framework 2.0.3 or newer**. The installed framework is **1.2.8**.

This is a real gate, not a warning. The build carries the message
"Core Impact Framework API not found or version insufficient" and refuses to run. It needs a method
that the framework only started exposing publicly in 2.0.3.

The newest framework is 2.0.4. It is not in the downloads folder, so this cannot be finished without
the user fetching it.

### Updating the framework looks safe

Sanguine Symphony 1.2.1 is the only mod here that feeds the framework its own instructions, and it
was built against the 1.x interface. Two things say the update will not break it:

- The 2.0.0 notes state that mods built for previous versions stay fully compatible with no changes.
- 2.0.1 specifically fixed how the filter types are read, to resolve compatibility with mods built
  against 1.x.

So: framework 1.2.8 → 2.0.4 should leave Sanguine Symphony working. Sanguine Symphony also has its
own update available (1.3.3), which *requires* framework 2.x — that pairing is the cleanest end state
but it is a second download and a bigger change.

### The bigger question is not technical

Accuracy is a localized damage system. Two are already running (Archery Locational Damage and
Locational Damage AE), on top of Requiem's own armour maths. Turning Accuracy on makes three.

Its defaults are deliberately mild — 1.5x ranged damage to the head, 0.8x to limbs, and the player is
excluded by default — but it also adds its own armour-effectiveness and combat-context layers that
overlap what Requiem already models.

Also: the author strongly recommends the optional MCM menu file, which is a separate download and is
not in the downloads folder either. Without it every setting has to be edited by hand in the INI.

Recommendation: decide whether Accuracy is replacing one of the two existing systems or stacking on
them, before enabling anything.
