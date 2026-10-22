# PBR Survey and Adoption Plan — 2026-08-27

Scope: find PBR texture options for mods Authoria already runs. Survey and plan only. Nothing was changed.

---

## 1. Where Authoria stands today

The engine side is ready. The content side is empty.

- The active profile is DEEZ CS NUTZ. It runs Community Shaders with no ENB. There are no ENB binaries in the game folder.
- Community Shaders AIO ships the TruePBR feature. It is present and unused.
- PGPatcher is installed and is what generates "Authoria - PG Output". That output is currently 3.4 GB and 15,553 patched meshes.
- PGPatcher has PBR switched **off** in its settings. Complex Material and parallax are switched on.
- Zero PBR texture mods are installed. I searched the whole mod tree for PBR config folders and found none.
- About 30 Complex Material and parallax mods are installed instead.

So the build is a Complex Material build. Every piece of plumbing needed for PBR is already there. It has just never been fed any PBR content.

One maintenance item found along the way: the local PGPatcher is version 1.0.0.0. The current release is 1.2.0. Most of the TruePBR maturity landed after 1.0.

---

## 2. How PBR and Complex Material coexist

This matters for planning, because it decides whether this is one big swap or many small ones.

- PGPatcher decides shader type **per mesh**. If a PBR config matches a mesh, that mesh becomes PBR. If not, it falls back to Complex Material or parallax.
- That means PBR can be adopted one mod at a time. There is no all-or-nothing cutover.
- Landscape is the one exception. Terrain textures blend across cell boundaries. A PBR terrain texture next to a Complex Material one shows a visible seam. So the landscape set has to move together.

---

## 3. Tier 1 — drop-in swaps

These are mods Authoria already has where the **same Nexus page** offers a PBR file. No new mod, no new conflict, no plugin cost. Just a different file from a page already in the download history.

| Installed now | Swap to | Also a version bump? |
|---|---|---|
| Vanaheimr Landscapes AIO — Complex Parallax 2k, v5.5 | Vanaheimr Landscapes AIO — PBR 2k, v5.5 | no |
| ERM Enhanced Rocks and Mountains v1.1.1 | v1.1.2 main installer, choose the PBR option | yes, 1.1.1 to 1.1.2 |
| Vanaheimr Northern Roads — Complex Material v2.7 | same page, PBR option | no |
| Vanaheimr Ore Veins v3.1 | same page, PBR option | yes, 3.1 to 4.0 |
| Vanaheimr Farmhouses v2.0 | same page, PBR option | yes, 2.0 to 3.0 |
| Vanaheimr Mines and Caves v5.0 | same page, PBR option | no |
| Stony AF Markarth — Complex Material | Stony AF Markarth PBR | no |
| Tomato's Riften and Ratway — Complex Parallax 2K v1.0 | Tomato's Riften PBR 2k v1.2 | yes, 1.0 to 1.2 |

Note on the Vanaheimr set: the PBR versions do not need Terrain Helper, which the Complex Material versions do. Terrain Helper is currently active in the build, so this changes nothing immediately, but it is one fewer dependency long term.

---

## 4. Tier 2 — PBR add-ons for mods already installed

These keep the installed mod as the base and layer a PBR conversion on top. I verified each base mod is actually present in Authoria by mod ID, not by name guess.

**From PBR Hub and Leo's standalone pages**

| Base mod (installed) | PBR add-on |
|---|---|
| Embers XD | Embers XD - PBR (standalone page, current) |
| Golden Dwemer Pipeworks Redone | Golden Dwemer Pipeworks - PBR (standalone page, current) |
| Improved Dwemer Glass | Improved Dwemer Glass PBR |
| Dwemer Pipework Reworked | Dwemer Pipework Reworked PBR |
| Detailed Rugs SE | Detailed Rugs PBR |
| Thrones Expanded | Thrones Expanded PBR |
| Praedy's Apocrypha | Praedy's Apocrypha PBR |
| Praedy's Fort Dawnguard | Praedy's Fort Dawnguard PBR |
| Praedy's Castle Volkihar | Praedy's Castle Volkihar PBR |
| Praedy's Staves AIO | Praedy's Staves AIO PBR |
| Skeleton Replacer HD | Praedy's Skeleton Replacer HD PBR |
| Nordic Stonewalls + Terraces | Nordic Stonewalls Complex Material and PBR |

**Standalone PBR add-ons for other installed mods**

| Base mod (installed) | PBR add-on |
|---|---|
| Nature of the Wild Lands v3.14 | Nature of the Wild Lands - PBR, plus its Snowier Spruce Trees patch (Authoria has that base too) |
| Draugrs (Mandragorasprouts) | Draugrs - PBR |
| Sanguine Symphony | Sanguine Symphony - PBR |
| Footprints | Realistic PBR Footprints |
| Waterplants | PBR Waterplants |
| High Quality Ivy | High Quality PBR Ivy |
| Ruins Clutter Improved SE | Ruins Clutter Improved PBR |
| SMIM 2.08 | SMIM PBR |
| Dawnguard Arsenal SSE | Dawnguard Arsenal - PBR |
| Sons of Skyrim v2.0 | Sons of Skyrim - Complex Material and PBR |
| New Legion (NordwarUA) | NordwarUA's Legion - Complex Material and PBR |
| Creation Club Alternative Armors | CC Alternative Armors - Complex Material and PBR |
| Rudy HQ Complex Material Silverware | Complex Silverware - PBR (this one replaces rather than layers) |
| Tomato's Imperial Forts 2.0 CM | Tomato's Imperial Forts Remake 2.0, PBR option (different page, replaces) |

Two entries in that list are blocked by a config choice, see section 6.

---

## 5. Tier 3 — base-layer options that need a decision

These are not drop-ins. Each one replaces or fights something already in the build. I am listing them so the option is on the table, not recommending them.

- **Vanilla PBR AIO.** A full PBR pack for architecture, clutter, actors and dungeons in vanilla style. It would sit against Skyland AIO, which is the current base layer at 1k.
- **Faultier's PBR Skyrim.** The other big base pack. Same overlap problem with Skyland AIO.
- **Tomato's Whiterun Remake PBR** and **Tomato's Windhelm PBR.** Both conflict hard with Authoria's city stack. Whiterun currently has Riton's Whiterun, Witcherun and Snazzy. Windhelm has Riton, Nordic Windhelm, Spaghetti's and Snazzy. I would leave these alone.
- **Weapons and Armors Remastered PBR** or **Faultier's PBR Armors and Clothes.** Both would run into the Xavbio retexture stack and into the blocklist issue in section 6.
- **Cathedral PBR Plants**, **PBR Flora Overhaul**, **Diverse PBR shrubs.** Flora is the riskiest area in this build given the colour work on record. I would keep PBR away from flora until last.

---

## 6. Two things that will silently do nothing

Worth knowing before anyone buys into an armour PBR pack.

1. PGPatcher's blocklist currently excludes armours, weapons, character actors and the UBE folder. Any PBR pack for armour or weapons will install fine and then have no effect, because the patcher never touches those meshes. Sons of Skyrim PBR, the Legion PBR, Alternative Armors PBR and Dawnguard Arsenal PBR all fall in this bucket. Lifting those exclusions is a real decision with UBE risk attached, not a checkbox.
2. PGPatcher's PBR switch is off. Until it is on, every PBR mod in sections 3 and 4 installs and does nothing.

---

## 7. Cost and risk

- **No plugin cost.** Every mod in sections 3 and 4 is textures and meshes only. The load order is near the 254 cap, and none of this adds to it.
- **LOD rerun.** Changing the landscape set means TexGen and DynDOLOD have to run again. That is the single largest time cost in this plan.
- **Seasons.** Authoria runs Seasons of Skyrim, Seasonal Landscapes and Unfrozen. A landscape texture swap needs a season-by-season look before it is called done.
- **Flora colour.** There is a settled baseline on flora colour. PBR changes how foliage reacts to light. Anything touching trees or plants should be tested on its own, not batched.
- **VRAM.** PBR ships extra maps per texture. Skyland AIO is at 1k and Vanaheimr at 2k. Keeping the PBR picks at 2k matches what is already there.
- **PG output is a tool output.** It gets regenerated, never hand-edited. Every step below ends in a fresh patcher run.

---

## 8. Suggested phasing

**Phase 0 — prerequisites, no content**
1. Update PGPatcher from 1.0.0.0 to 1.2.0.
2. Turn on PBR in its settings, leaving Complex Material and parallax on.
3. Run it once with no PBR content installed. Confirm the output is clean and the game still looks identical. This proves the toolchain before anything visual changes.

**Phase 1 — objects and dungeons, lowest risk**
Everything in section 4 that is not landscape, flora or armour. Dwemer pipeworks, Praedy's sets, rugs, thrones, ruins clutter, skeletons, draugr, blood, footprints, silverware, SMIM. No LOD impact. Interiors mostly, so easy to eyeball.

**Phase 2 — architecture**
Markarth, Riften, the Imperial forts, the stone walls. Exterior work, so worth a LOD check at the end.

**Phase 3 — landscape and trees**
Vanaheimr Landscapes, ERM, Ore Veins, Mines and Caves, Northern Roads, Farmhouses, and NOTWL PBR. These move as one group. Ends with TexGen, DynDOLOD and a four-season pass.

**Phase 4 — gated on decisions**
The base layer question (Vanilla PBR AIO or Faultier's versus Skyland), and the armour question (whether to lift the patcher blocklist).

---

## 9. What I would do first

Phase 0 and Phase 1 only. That is roughly 20 mods, all texture-only, no LOD rerun, no landscape risk, and it answers the real question — whether PBR actually looks better in this build — before committing to the expensive parts.
