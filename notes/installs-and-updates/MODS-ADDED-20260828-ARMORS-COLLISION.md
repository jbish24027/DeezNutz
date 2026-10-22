# Armors, collision, CRDW plugin — 2026-08-28

Twelve archives handed over. MO2 was closed the whole time.

Backups: `_backups\2026-08-28 - armors-collision-crdw\` (profile files before and after the UBE
run, both Sera mod folders, the old SkyPatcher INIs). Mesh backups sit beside each mesh as
`*.bak-neckcut-20260828`. The Katari UBE patch ESP has `*.bak-preghostfix-20260828` beside it.

---

## 1. CRDW Automatic Mode (MO2 plugin)

Extracted to `plugins\crdw_auto_mode\`. This is an MO2 application plug-in, not a mod, so it does
not appear in the left pane.

What it does: it decides CRDW's cache mode for you. It watches for mod installs, enable/disable,
priority moves and load-order changes, and it also marks the profile dirty whenever you launch
anything through MO2 that isn't Skyrim or SKSE (Pandora, BodySlide, DynDOLOD, and so on). If
nothing changed it runs CRDW in LOAD mode with the pop-up suppressed; if something did, it runs
one CACHE rebuild and then goes quiet again. Caches are kept per profile.

It writes its own `CRDW.ini` into Overwrite and never touches CRDW's installed ini. The first
launch of each profile is treated as dirty on purpose, so the first start after this session will
rebuild the cache by itself — you do not need to answer a pop-up.

This supersedes the old rule about always answering Yes to CRDW's question. The pop-up is off
because the companion is now making that decision from real change events instead of asking you.

## 2. Dynamic Combat Collision 1.4.3

Mod folder `Dynamic Combat Collision`, sitting next to Dynamic Collision Adjustment in all six
profiles. SKSE DLL + PDB + English translation. No plugin, no records, no asset conflicts.

I checked the file hash against Nexus: it is the **SE/AE** main file, not the VR one (both are
v1.4.3 and dated the same day, so this was worth confirming).

The optional **MCM file was not installed**, and I would leave it that way. You are near SkyUI's
128-menu ceiling, and SKSE Menu Framework is installed, so the mod's settings are reachable in
game without spending an MCM slot or a plugin slot.

Everything it can use is already here: Address Library, MCM Helper, SKSE Menu Framework,
SkyParkour v3, True Directional Movement, TrueHUD, Precision, Combat Pathing Revolution.

**One thing to know.** You already run **Dynamic Collision Adjustment** (Ersh). The two overlap
only in a narrow way: Ersh's mod resizes the collision capsule for *sneaking and swimming* and
fixes actor-scale collision, while this one resizes it *in combat only* and reverts outside
combat. The shared case is sneaking while in combat, which 1.4.0 added. DCC 1.4.2 specifically
fixed "a crash when putting collision back after another mod rebuilds the hull", so the author has
handled this. I left both enabled — Ersh's also does the actor-scale fix, which DCC doesn't. If
combat ever feels like the hull is fighting itself, Dynamic Collision Adjustment is the one to try
disabling.

## 3. Katari Armor

Five mod folders, in this priority order (top wins):

| Mod | What it provides |
|---|---|
| `LM's Fuse Katari Armor Retex` | the winning textures — see below |
| `Katari Armor - Xtudo Tweaks` | the ESP + his optimised ground/inventory models |
| `Fuse00 - Katari Armor UBE` | `!UBE` meshes, BodySlide sets, the UBE patch ESP |
| `Fuse00 - Katari Armor 3BA` | 3BA worn meshes + BodySlide sets |
| `Fuse00 - Katari Armor - CBBE` | base textures and the fallback meshes |

**The retex is ON** (turned on at your request after the first pass; it was installed off because
your screenshot showed the plain tan suede, which is the base texture). LM repaints the vest as a
dark olive floral, so the armour will not look like that screenshot any more — the neck cut is
geometry and is unaffected either way.

It wins all six of its texture files over the base. Resolution delta: the two diffuse maps stay
4K, the two normals drop 4K → 2K, and the two metallic masks go 1K → 2K. So colour detail is
unchanged, surface relief is a little softer, metal masks are sharper. The `mushroom04_e` cubemap
still comes from the base mod because the retex does not ship one.

**I dropped three of Xtudo's meshes.** He ships first-person, boots and glove meshes built on
plain CBBE; the 3BA versions have to win those or the body shape is wrong. His ground models and
his ESP are what you actually want from that mod, and those are in. The cost is that his
"removed HDT-SMP bones from the first-person models" tweak doesn't apply — the 3BA first-person
mesh keeps its 46 dress bones. Harmless, just not optimised.

**The plugin clash, and how it was fixed.** Xtudo's ESP renumbers every record (000801+ instead of
000D63/000001) so the plugin is properly ESL-safe. That broke the author's UBE patch, which was
built against the 3BA plugin's FormIDs — three of its records pointed at armors Xtudo doesn't
define, which showed up as three dangling references and meant Katari would have been **invisible
on a UBE character**. Fixed by deleting those three ghost records from the UBE patch and adding
the three UBE ArmorAddons onto Xtudo's six armors instead (in the Reqtificated patch). The UBE
patch now carries only its three ArmorAddons; check_errors is clean.

Xtudo's clothing (unarmored) variants got UBE coverage too, so both the armored and the mage
version work on a UBE body.

### The neck

You asked for the collar gone, then for the V-yoke and the shirt bodice too. All three are cut:

- the jacket's **standing collar** (its own triangle island, 661 verts)
- the jacket's **V-shaped yoke straps** (543 verts)
- the **cream shirt bodice trimmed at z=110** — your body's shoulders top out at 110.5 and the
  neck at 114, so the shoulder yoke survives and only the part that climbs the neck is gone

The sleeves and shoulder caps are untouched, exactly as your second screenshot shows them.

Done on eight meshes: both weights of the world mesh in **both** the 3BA and UBE lanes, plus the
four BodySlide reference meshes so a rebuild keeps the change. The base-CBBE worn meshes and both
ground/inventory models got the same cut so nothing looks different when dropped on the floor.

The method matters if you ever want to undo it: I removed **triangles only** and left every vertex
in place. That means the BodySlide slider data still lines up perfectly, `_0` and `_1` share an
identical triangle list (they have to, or the weight morph breaks), and restoring any
`.bak-neckcut-20260828` puts it back exactly. All 40 Katari meshes re-parse clean.

## 4. LDD - Lili Collection

Three folders: `LDD - Lili Collection` (CBBE CS-PBR 4K base), `- 3BA`, `- UBE`. Two outfits,
Lilac and Gooseberries and Toussaint Meadow, 33 pieces. The author's own UBE patch already covers
every piece, so the UBE lane needed nothing from me.

It ships `PBRNIFPatcher\LDDs_LiliCollection_SMP.json`, which is a config for the PBR pass. It is
inert until a generator run picks it up, so on the PBR profile the collection renders non-PBR for
now. Nothing is broken by that.

## 5. Sera's Armor 1.4 + 3BA 1.5.2

Straight update in place. The 1.4 plugin is a **clean superset**: all 980 existing records keep
their exact FormID, EditorID and type, and 334 are new. So nothing that pointed at Sera broke.

What changed underneath: 34 existing meshes were rebuilt (the author remade the sleeves and
reweighted the chestguard pieces), 24 meshes are new, and 90 new armors were added — thighguards,
chainmail and buckled pauldrons, a simple chestguard, two new kneepads, Isabela's choker, plus
"repaired" variants of the dresses.

The 3BA update touched 14 files, all of them the SMP dress and sweater slider data.

## 6. Requiem

All 123 new armors went into the existing `Authoria - Reqtificated - Armor Folder.esp`, which grew
from 520 to 643 records. I derived the numbers from what that patch already does rather than
inventing any — across its 234 existing Sera records the convention is completely uniform, and it
matches Requiem's own light leather/hide ladder exactly.

| What | Armor rating | Value | Weight |
|---|---|---|---|
| body, armored | 150 | 100 | 5.0 |
| hands / feet, armored | 45 | 30 | 1.5 |
| body, cosmetic | 0 (clothing) | 20 | 1.0 |
| accessory slots | 0 (clothing) | kept | kept |

- **Katari** (3 records): 33/11/10 → 150/45/45 on the leather ladder, values and weights to match.
  His keywords were already correct so I left them. The three clothing variants were already
  correct and were left alone.
- **Lili** (33 records): the whole collection is now **clothing frames** — armor rating 0, type
  Clothing, proper clothing/jewelry keywords. As shipped, seven dresses each carried the cuirass
  keyword and a real armor rating, and Requiem hands ranged resistance to anything with that
  keyword, so wearing several of these together would have stacked protection outside the slot
  model. Values are the author's; only weights were normalised. If you'd rather one of the dresses
  be genuine light armor, that's a three-field change.
- **Sera** (84 of the 90 new records): the 16 armored dresses onto the ladder, the 16 cosmetic
  dresses to clothing frames, and 52 accessory-slot pieces (kneepads, thighguards, pauldrons,
  belt bags, arm guards, simple tops) to clothing at 0 rating. The remaining 6 — two pairs of
  flats and the four Isabela chokers — already had the right shape and were left alone.

Why the accessory pieces matter: the Reqtificator's rating scaler **skips anything typed Clothing
outright**. Setting them that way means those pieces stay cosmetic permanently instead of being
rescaled into extra protection on top of your four real armor slots.

I did not hand-stamp any resistance-tier or tempering keyword. Those are the Reqtificator's own
output and it assigns them from the set keyword at build time.

Expect the Reqtificator's master count to go from ~212 to about 217 next time it runs — the cap is
254, so there's plenty of room.

## 7. UBE — Sera

Katari and Lili came with author-made UBE conversions, so only Sera needed a run.

Ran the converter scoped to `KW_SerasArmor.esp` into a fresh folder,
`Authoria - UBE Converter Output - Sera`, leaving the big hand-curated
`Authoria - UBE Converter Output` untouched. It produced 285 ArmorAddons, 78 meshes and a
287-line SkyPatcher ini. All 78 meshes validated: no zero-filled files, no truncation, correct
UBE topology (the body reads 29298 verts as it should). The 24 genuinely new pieces are all there.

**Why this replaced the old Sera lane rather than topping it up.** The converter deliberately
ignores its own output mods when it scans, which means it could not see the 213 existing Sera
SkyPatcher lines and would have added a *second* UBE ArmorAddon to every piece — double geometry.
So the new patch now owns Sera's whole UBE lane, and I stripped the 213 Sera lines out of
`Authoria - Output - UBE Converter.esp.ini` and `... 2.esp.ini`. Every other mod's coverage in
those two files is untouched (4029 lines kept, and no line mixed Sera with anything else, so
nothing had to be edited around). Coverage went 258 → 348 Sera armors with none lost.

The old minted Sera ArmorAddons are still in the old output plugins, now unreferenced and inert.

**One caveat, stated plainly.** The converter reads whichever mesh currently wins, and for the 34
reweighted pieces that is still your pre-1.4 BodySlide output. So those pieces are converted from
the old geometry — same as they already were, no regression — and they match what the 3BA lane is
showing. The 24 new pieces came from the mod's own meshes and are correct.

Enabled in the four profiles where Sera's Armor is enabled; installed but off in the two
Requiem Reforged profiles, matching how Sera itself is set there.

## 8. Starting Kit

129 new zero-cost exchange-station entries, taking the plugin from 1434 to 1563. Tags follow the
existing scheme: **SER** +90 (248 → 338), **KAT** +6, **LIL** +33. Highest FormID is now 0xE1C
against the ESL ceiling of 0xFFF, so there's room for roughly 480 more.

Audited: zero entries carry conditions (the vanishing-entry bug stays fixed), and every EditorID's
hex suffix equals its item's local FormID.

## 9. Outfit Wheeler

Adding five ESL plugins shifted every light index, which invalidates every stored Wheeler rawID.
Calibrate reported all 77 entries stale. I ran the reindex; it rewrote all 77 and calibrate now
reports 77 match, 0 mismatch. Safe to launch.

---

## Verification

- `check_errors` across all eight touched plugins: **0 dangling references, 0 missing masters,
  0 unparseable records**.
- Profile files: +10 mod lines and +4/+5 plugin lines per profile, all four files in lockstep,
  every new plugin grouped (no split headers in MO2's plugin pane).
- Plugin budget: 228 of 254 full slots. All five new plugins are ESL.
- Asset resolution spot-checked: Katari 3BA and UBE meshes, Lili UBE, Sera UBE — each resolves to
  the intended mod.
- All 40 Katari meshes and all 78 new Sera UBE meshes re-parse clean.

## Known gaps

- Lili's PBR textures need a generator pass before they render as PBR.
- Sera's 34 reweighted pieces are still built from the older BodySlide output in both the 3BA and
  UBE lanes.
- Xtudo's first-person SMP-bone optimisation for Katari is not in, because the 3BA mesh has to win
  that file.

---

## Post-run verification — BodySlide, Synthesis and the Reqtificator all ran

**The neck cut survived.** BodySlide built the UBE Katari set into
`Authoria - Bodyslide Output - UBE`, and that output now WINS the `!UBE` path over the mod's own
prebuilt meshes. It carries the cut — jacket 19512 triangles, DressNew 7047, exactly the numbers
written on 08-28. That is the payoff for cutting the BodySlide *reference* meshes as well as the
built ones: a rebuild reproduces the cut instead of undoing it.

The paths BodySlide did not touch still carry it too: the 3BA world meshes (which still win the
non-UBE path from `Fuse00 - Katari Armor 3BA`), the CBBE fallback, and Xtudo's ground model.
6365 meshes re-validated across all seven Katari/Sera/BodySlide-output folders: zero zero-filled,
zero truncated, zero unparseable.

**The Reqtificator closed the tempering gap and changed nothing else.** On every armored piece it
kept the hand-set values and the UBE ArmorAddon, and added only the two keywords it owns:

| Record | AR / Value / Weight | Armature | Added by the run |
|---|---|---|---|
| Katari cuirass `000801` | 150 / 100 / 5 — unchanged | UBE addon intact | Ranged_Tier1 + Tempering_Craftsmanship |
| Katari boots `000802` | 45 / 30 / 1.5 — unchanged | UBE addon intact | Tempering_Craftsmanship (no ranged tier — cuirass-only, correct) |
| Sera new armored dress `000C65` | 150 / 100 / 5 — unchanged | intact | Ranged_Tier1 + Tempering_Craftsmanship |

The clothing frames were left alone exactly as designed — Sera's pauldron `000D75` and Lili's
boots/dress are still ArmorRating 0, type Clothing, with their UBE addons. That is the scaler
skipping `ArmorType.Clothing` outright, which is why typing them Clothing was the durable fix.

So all 19 armored pieces are now temperable at the armor workbench, and the whole batch is
Requiem-complete.

**Wheeler:** 77 match, 0 mismatch. The three tool runs regenerate full plugins, so no light index
moved and the reindex from earlier still holds.

**One unrelated finding.** `check_errors` reports a single dangling reference in the regenerated
`Requiem for the Indifferent.esp`: the patcher's own `REQ_LockpickControl` script, attached to the
Magpie Manor trap door `1F2471:MagpieManor.esp`, has a property pointing at `000028:Skyrim.esm`
which nothing defines. Not armor, not from this session — the source mod's own copy of that door
is clean, so the patcher introduced it. It is also inert: `PG_1.esp` wins that record anyway.
Noted, not fixed.
