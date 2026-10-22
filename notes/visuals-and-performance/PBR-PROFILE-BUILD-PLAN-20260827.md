# PBR Profile Build Plan — 2026-08-27 (rev 2)

Supersedes the phasing in `PBR-SURVEY-AND-PLAN-20260827.md`. That file stays valid as the survey.

Decisions locked: trimmed Vanilla PBR AIO. SMIM PBR dropped. Armours and weapons in scope. Dwemer gear stays non-PBR. Ore veins and Stony AF Markarth added. Mines and Caves at 4k. Dwarven Trio More Shiny. Golden Dwemer update as downloaded. No flora. No LOD rerun.

**BUILT 2026-08-28.** Everything below is done except the patcher run, which has to be launched from inside MO2. Sections 1 to 13 are the plan as agreed; section 14 is what actually happened, including four places where the build differed from it.

---

## 1. Answering the LOD question first, because it changes the plan

**No, you would not have to rerun. And the textures were never going to show up in LOD either way.**

Object LOD and terrain LOD are separate baked assets with their own simple shader. PBR is a near-mesh feature only. The patcher is already told to skip every LOD path, so it never touches them. That is true today and stays true after this work.

So LOD is never PBR, rerun or not.

What a TexGen and DynDOLOD rerun would actually do is re-bake the LOD atlas colours from the new diffuse maps. That only matters if a mod changes the colour of something you can see from a distance. A PBR conversion mostly keeps the original albedo and re-authors the surface properties instead, so the colour barely moves.

Nothing breaks without a rerun. No purple, no missing LOD, no crash. The worst case is a slight near-versus-far colour difference on one or two exterior sets.

**This resolves the fourth decision I asked you for.** Nordic Stonewalls and the Imperial Forts Remake both stay in. The LOD exposure I flagged in rev 1 was overstated.

---

## 2. Armours and weapons — it takes two changes, not one

I found something while checking this. The armour block is not doing what it looks like it does.

The blocklist entry is written for a folder name that vanilla Skyrim does not use — armour meshes sit in the singular form, and the pattern is plural. So it never matched. What is actually keeping armour and weapon meshes out is the second gate: the list of record types the patcher is allowed to walk. Armour, armour addon and weapon records are all absent from it, so those meshes have no reachable use and get skipped.

I confirmed the patcher does support all three record types. They were simply never switched on.

So enabling this needs **both**:

1. Drop the two dead blocklist patterns for armours and weapons
2. Add armour, armour addon and weapon to the allowed record types

**Your hand-tuned work is protected by a boundary that already exists.** Every piece of UBE work — the converter output, the Ninirim converter output, the BodySlide output, and the Corsican Raider fix — lives under one folder, and that folder has its own blocklist entry that is not being touched. Bodies and facegen stay excluded by the character actor entry.

Two more things reduce the risk I flagged in rev 1:

- The patcher never modifies source meshes. It writes patched copies into its own output mod. Turning that mod off reverts everything.
- The bug that would have threatened the Corsican alternate-texture fix — shapes being deleted and 3D indices shifting out from under a plugin — was fixed in 1.1.4. Another reason the update comes first.

Real costs that remain: every armour and weapon mesh in the build now gets considered, so the run takes longer and the output grows. The Complex Material pig iron set, currently inert, goes live. Any armour carrying an environment mask picks up a dynamic cubemap, which changes how it looks. There is a switch to suppress that if you dislike it.

---

## 3. The shared-output trap

"Authoria - PG Output" is one folder, enabled in **all five** profiles.

A PBR run pointed at it would rewrite meshes for the Main profile, the NSFW profile, DEEEZ NUTTZZZ and PICTA. None have PBR textures. Two are ENB profiles where PBR does not function. All four would break from a run that looked successful.

The new profile gets its own output mod, **Authoria - PG Output - PBR**, at the exact position the old one sits today. The old folder is never written to.

---

## 4. Patcher update

1.2.0 restructures the install and now bundles its own runtime, so it is not a safe overwrite. Clean install to a new folder; 1.0.0 stays as the rollback.

Facegen meshes were pulled into the pipeline in 1.1.0. This build has a lot of hand-baked facegen. 1.2.0 added a switch to skip facegen and I will be using it, on top of the blocklist entry that already covers that folder.

---

## 5. Settings — the exact delta

Everything carries across verbatim: game paths, mod manager mode, output language and zip setting, all four pre and post patcher switches, the empty allowlist, logging and threading flags, the texture map table, the 19-entry vanilla archive list, Complex Material on, parallax on, parallax-to-CM off.

**Four values change:**

1. TruePBR: off becomes **on**
2. Output folder: points at the new output mod
3. Blocklist: the two dead armour and weapon patterns come out. **The other eight stay, including the UBE folder and character actors**
4. Allowed record types: armour, armour addon and weapon are added to the existing 30

One value disappears on its own because the feature was removed from the tool. It was already off.

Plus one runtime flag, not a setting: skip facegen.

---

## 6. The mod list — 26 mods

All texture-only. Nothing touches the plugin count.

**Dungeons, interiors, clutter, creatures, effects — 16**

1. Praedy's Apocrypha PBR
2. Praedy's Fort Dawnguard PBR
3. Praedy's Castle Volkihar PBR
4. Praedy's Staves AIO PBR
5. Praedy's Skeleton Replacer HD PBR
6. Improved Dwemer Glass PBR
7. Dwemer Pipework Reworked PBR
8. Golden Dwemer Pipeworks PBR
9. **Dwarven Trio PBR** — new this round. The dwarven constructs in PBR. No base mod needed, and you have no dwarven creature retexture for it to fight. This is dwemer metal walking around in the world, which is the most literal reading of what you asked for
10. Detailed Rugs PBR
11. Thrones Expanded PBR
12. Ruins Clutter Improved PBR
13. Draugrs PBR
14. Sanguine Symphony PBR
15. Realistic PBR Footprints
16. Embers XD PBR

**Exterior statics — 2**

17. Nordic Stonewalls Complex Material and PBR
18. Tomato's Imperial Forts Remake, PBR option — replaces the Complex Material forts currently installed

**Armour and weapons, unlocked by the settings change — 4**

19. Sons of Skyrim Complex Material and PBR
20. NordwarUA's Legion Complex Material and PBR
21. Creation Club Alternative Armors Complex Material and PBR
22. Dawnguard Arsenal PBR

All four are add-ons for armour mods you already run. Your existing retextures are untouched, and no art direction changes.

**Tier 1 swaps you asked for — 3**

23. Vanaheimr Ore Veins, PBR 4.0 — replaces the 3.1 Complex Material install
24. **Vanaheimr Mines and Caves, PBR** — not optional if 23 goes in, see section 6a
25. Stony AF Markarth PBR — replaces the Complex Material layer

**Base layer — 1**

26. Vanilla PBR AIO, **trimmed to dungeons, clutter and furniture**. Cities and actors dropped before install. It must also sit below ERM, because it ships mountain textures and ERM should keep winning those. I will do the trim once the archive is downloaded and I can see the folder tree.

**One prerequisite to check:** Golden Dwemer Pipeworks PBR lists the Golden Dwemer Pipeworks unofficial update as a requirement. That is not installed here as its own mod — the hotfix folder you have is a file from the base page, not the update. Worth grabbing alongside it.

---

## 6a. The two swaps you added, and what they drag with them

I checked what actually wins in both chains before agreeing to these. Neither is quite a drop-in.

**Ore veins pulls Mines and Caves with it.**

Ore veins are overlays on cave rock. Vanaheimr builds both with a shared blending system, and they are designed as a set. If the vein goes PBR and the rock around it stays Complex Material, the blend at the edges will not match. Mines and Caves is already installed at exactly the version whose page carries the PBR file, so this costs you one more download and no version change at all. Ore veins on its own is the version I would not do.

Also worth knowing: the ore veins jump is 3.1 to 4.0, and 4.0 reworks the meshes and some textures on top of adding PBR. It is a real update, not a PBR file bolted onto what you have.

**The dwarven ingot is a loose end.**

Vanaheimr ships a diffuse for every ingot except dwarven. For dwarven it ships only the material maps, and the diffuse comes from your Ancient Dwemer Metal ore patch. That pairing is deliberate — it is how your dwarven ingot matches the rest of your dwemer metal.

Go PBR and that patch's diffuse gets read as PBR albedo, which is a mismatch on that one item. Disabling the patch is worse, because then nothing supplies a dwarven diffuse at all.

4.0 reworked textures, so it may now ship the dwarven diffuse itself and make the patch redundant. I will check that after download and tell you which way it landed. No action needed from you now.

**Stony AF Markarth strands two dwemer patches.**

The Complex Material layer you have is 61 material masks and nothing else. Two patches sit above it and override 11 files between them — Ancient Dwemer Metal recolours six Markarth diffuse textures, and Dwemer Pipework Reworked replaces five more. Both were authored for the current workflow.

Swap the layer to PBR and those 11 files render against a PBR config they were not made for. Markarth columns, inn windows and metal designs are where you would see it.

Two ways to go:

- **Disable both patches in the new profile.** Markarth's dwemer metal reverts to Stony AF's own look. Given world dwemer is going PBR through Golden Dwemer Pipeworks PBR and Dwemer Pipework Reworked PBR anyway, this is the more coherent result, not less.
- **Keep them and accept 11 mismatched files.**

I would disable them. It is reversible and it only affects the new profile.

Good news on the rest of that chain: Ancient City of Markarth is vines and moss, Snazzy Markarth ships no textures at all, and Metallurgy puts its ore textures on a custom path. None of them collide with either swap.

---

## 7. Dwemer gear — decided, staying non-PBR

Your dwarven armour and weapon textures come from a mod with no PBR conversion, and nothing exists to convert it. World dwemer goes PBR through items 6 to 9; dwarven gear stays as it is.

No vanilla armour pack is being added, so your Xavbio stack and your dwemer gear retexture are untouched. The four armour PBR mods in the list are all add-ons for mods you already run.

If the gear ends up looking flat next to the new dwemer architecture, Weapons and Armors Remastered PBR is the fallback — same author as most of the picks above, so the art direction would match. That is a look-at-it-in-game decision, not one to make now.

---

## 8. The new profile

Name: **DEEZ CS NUTZ - PBR**

Cloned from DEEZ CS NUTZ. Copies the mod list, plugin list, load order, locked order, plugin groups, archives, profile settings, ini tweaks, all three game inis, and the saves folder. Backup files are not copied.

Changes inside the new profile, and nothing else:

1. Old PG output off, new PG output on, same position
2. The 26 mods enabled at their correct positions
3. The Complex Material Imperial Forts turned off, since the Remake replaces it
4. The two Stony AF Markarth dwemer patches turned off, per section 6a

The plugin list, load order and plugin groups files stay byte-identical. Everything being added is textures only, and the new output ships the same two plugin names as the old one.

---

## 9. Order of work

1. Install PGPatcher 1.2.0 clean to a new folder. Leave 1.0.0 in place.
2. Write the new settings file, forwarded from the old one, with the four changes from section 5.
3. Clone the profile. Verify the copy before touching it.
4. Create the new output mod folder and register it.
5. Trim Vanilla PBR AIO, then apply all mod list changes.
6. Verify: diff the new mod list against the old and confirm only intended lines moved. Confirm the plugin files are identical. Confirm the settings file differs in exactly four keys.
7. Select the new profile, with MO2 closed.
8. Run PGPatcher with facegen skipped.
9. Report what the run produced — PBR against Complex Material against parallax counts, and how many armour and weapon meshes were newly touched — and confirm the old output folder was never written to.

Steps 1 through 9 are mine. Downloading the mods is yours.

---

## 10. Still open

Nothing blocking. Two things I will settle myself and report on:

1. Whether Vanaheimr Ore Veins 4.0 now ships its own dwarven ingot diffuse, which decides the fate of the Ancient Dwemer Metal ore patch. I check this after download.
2. The Vanilla PBR AIO trim, once I can see the folder tree.

One thing I have decided on your behalf and will reverse on request: **disabling the two Stony AF Markarth dwemer patches**, per section 6a. Say the word if you would rather keep them.

Ready to build once the downloads are in.

---

## 11. Download list

26 mods, 1 prerequisite, 1 optional. Every page is manager-download only, so use the Mod Manager Download button on each.

### One page, eight files — PBR Hub

https://www.nexusmods.com/skyrimspecialedition/mods/139889

Take these eight main files:

1. Praedy's Apocrypha - PBR
2. Praedy's Fort Dawnguard - PBR
3. Praedy's Castle Volkihar - PBR
4. Praedy's Staves AIO - PBR (v1.0.1)
5. Praedy's Skeleton Replacer HD PBR
6. Improved Dwemer Glass PBR
7. Detailed Rugs PBR
8. Thrones Expanded PBR

### Dungeons, clutter, creatures, effects

9. Dwemer Pipework Reworked PBR — https://www.nexusmods.com/skyrimspecialedition/mods/175031
10. Golden Dwemer Pipeworks - PBR — https://www.nexusmods.com/skyrimspecialedition/mods/186039
11. Dwarven Trio PBR — https://www.nexusmods.com/skyrimspecialedition/mods/151925 (file: "More Shiny")
12. Ruins Clutter Improved PBR — https://www.nexusmods.com/skyrimspecialedition/mods/152196
13. Draugrs - PBR — https://www.nexusmods.com/skyrimspecialedition/mods/172664
14. Sanguine Symphony - PBR — https://www.nexusmods.com/skyrimspecialedition/mods/170736
15. Realistic PBR Footprints — https://www.nexusmods.com/skyrimspecialedition/mods/140780
16. Embers XD - PBR — https://www.nexusmods.com/skyrimspecialedition/mods/186037

### Exterior statics

17. Nordic Stonewalls Complex Material and PBR — https://www.nexusmods.com/skyrimspecialedition/mods/127188
18. Tomato's Imperial Forts Remake — https://www.nexusmods.com/skyrimspecialedition/mods/172845 (file: **Imperial Forts Remake PBR v2.0**, not the CM one)

Optional from that same page: **Imperial Forts Remake PBR LOD helper v1.1**. It exists to close the near-versus-far gap without a DynDOLOD rerun, which is exactly your constraint. Worth taking.

### Armour and weapons

19. Sons of Skyrim - Complex Material and PBR — https://www.nexusmods.com/skyrimspecialedition/mods/137807
20. NordwarUA's Legion - Complex Material and PBR — https://www.nexusmods.com/skyrimspecialedition/mods/137994
21. Creation Club Alternative Armors - Complex Material and PBR — https://www.nexusmods.com/skyrimspecialedition/mods/139065
22. Dawnguard Arsenal - PBR — https://www.nexusmods.com/skyrimspecialedition/mods/188229

Take the PBR option wherever a page offers PBR or Complex Material.

### The three swaps

23. Vanaheimr - Ore Veins — https://www.nexusmods.com/skyrimspecialedition/mods/149148 (file: **Vanaheimr - Ore Veins - PBR v4.0**, single file, no size options)
24. Vanaheimr - Mines and Caves — https://www.nexusmods.com/skyrimspecialedition/mods/137033 (file: **Mines and Caves - PBR - 2k v5.0**, to match your other Vanaheimr installs)
25. Stony AF Markarth — https://www.nexusmods.com/skyrimspecialedition/mods/127407 (file: **Stony AF Markarth PBR v1.0.0**, not the Complex Material one)

### Base layer

26. Vanilla PBR AIO — https://www.nexusmods.com/skyrimspecialedition/mods/174091 (file: Vanilla PBR v1.33. I trim it before install)

### Prerequisite

Golden Dwemer Pipeworks Redone - Unofficial Update — https://www.nexusmods.com/skyrimspecialedition/mods/94440

Golden Dwemer Pipeworks PBR lists this as required. Take:

**a) Golden Dwemer Pipework Reworked (No Parallax) — v2.16a**

The page runs two tracks. The **a** track is the full version; the **b** track is the cut-down one, which older uploads label "Light" and "Lightweight". Your Golden Dwemer install is the full 2K base, so **a** is the match.

Each track offers Parallax and No Parallax at the current version. Take **No Parallax**. You are going PBR here, the PBR add-on supplies its own surface maps, your patcher regenerates shader treatment on its own, and it is already set to discard pre-patched materials. The parallax variant's height maps would be redundant at best.

What this mod is for: it bridges the Golden Dwemer gold look onto Dwemer Pipework Reworked's newer meshes. You have both sides installed — Golden Dwemer at 2.0 and Dwemer Pipework Reworked at 5.4 — but not the bridge, which is why the PBR add-on asks for it.

I will confirm the file overlap against your existing Golden Dwemer stack before enabling it. If it turns out to duplicate what Real Dwemer Pipes or Dwemer Tech Glowmapped already provide, I will say so and place it accordingly.

### Already have, no download needed

PGPatcher 1.2.0 is in your Downloads folder. Community Shaders is installed. The base mods for every add-on above are all present and at compatible versions — I checked each one by mod ID.

---

## 12. Download audit — 2026-08-27

All 26 arrived plus the prerequisite. Five things worth knowing.

**1. Golden Dwemer update — RESOLVED, the file you have works.** The archive self-identifies as the Light edition, so that is what goes in the record. It does not matter here, and I checked properly rather than assuming.

Golden Dwemer PBR carries 21 config files, and they are named after **textures**, not meshes — dwemer metal, pipes, bricks, doors, stone floors, the Markarth column. That is how this patcher system works: configs match the texture paths inside a mesh, not mesh filenames. Every one of those textures is supplied by Golden Dwemer Pipeworks Redone itself, which you already have installed.

So the update's job here is the mesh fixes and the bridge onto Dwemer Pipework Reworked, and the edition you have carries 83 meshes and 25 textures covering exactly that. No re-download. Proceeding with it.

Its installer has two parts: **GDPR - main**, which is required, and an optional **new collisions and fix materials** that corrects two facade meshes so metal roofs sound like metal underfoot. The author warns it may slightly affect performance. It is two meshes, so I am taking it.

**2. Mines and Caves — 4k confirmed.** 1.47 GB against your 2k Landscapes and Farmhouses. Ore Veins has no size option so the pairing is unaffected. Purely a VRAM cost, and it is your call to spend it on the places you stand around in.

**3. Dwarven Trio — More Shiny confirmed.** The other download gets ignored, not installed.

**4. Sons of Skyrim HDT-SMP Cloaks is already installed.** Same mod ID, same archive filename, already in the list as "Sons of Skyrim - HDT Physics for Cloaks Patch". Skip.

**5. The Dwemer Metals Retexture patch is a good catch.** Not on my list, but Dwemer Metals Retexture SE is installed, so it applies. Six configs and 22 textures for dwemer ruins. Adding it. Downloaded twice; one copy is enough.

**Correction:** I said everything was texture-only. Vanilla PBR ships a plugin. It is ESL-flagged, so it costs no full slot and you stay at 240 of 254 — but the claim as I made it was wrong.

**Disk:** 201 GB free. Downloads are about 19 GB, installed will be roughly double that, plus a fresh patcher output. Comfortable, not unlimited.

---

## 12a. Vanilla PBR trim — measured

15.90 GiB uncompressed, 9,416 files. The size is not the real problem. It overlaps eight of the mods you just downloaded, including in the dungeon coverage I told you to keep.

**Dropping 9.32 GiB across 4,192 files:**

| Size | Why |
|---|---|
| 4672 MiB | Architecture. The city stack owns Whiterun, Windhelm, Markarth, Solitude, Riften, farmhouses, High Hrothgar, Sky Haven, Sovngarde |
| 2414 MiB | Actors. Your creature and NPC retexture stack owns these, and its draugr collides with Draugrs PBR |
| 774 MiB | Imperial dungeons — Tomato's Imperial Forts Remake PBR owns these |
| 530 MiB | Mines and caves — Vanaheimr Mines and Caves PBR owns these |
| 366 MiB | Dwemer ruins — Stony AF Markarth PBR and the two Dwemer PBR mods own these |
| 217 MiB | Ruins clutter — Ruins Clutter Improved PBR owns these |
| 207 MiB | Vanilla armour, weapons and clothes — gear stays as it is |
| 149 MiB | More creature textures |
| 101 MiB | The Ratway — Tomato's Riften owns it |
| 67 MiB | Landscape |
| 26 MiB | Flora |
| 16 MiB | Interface |
| 7 MiB | Blood — Sanguine Symphony PBR owns it |

**Keeping 6.57 GiB across 5,224 files:** clutter, the dungeon types nothing else covers, Creation Club, Dawnguard and Dragonborn clutter and dungeons, SMIM clutter and furniture, Hearthfire, furniture, traps, effects, and the support files.

That is the trim. It is a fair bit more aggressive than "drop cities and actors", because five of the cuts exist purely to stop it fighting mods you deliberately chose.

---

## 13. Watch list for the first run

- Embers XD PBR against the Community Shaders flame setup and the Light Placer work on it. Fire is the most likely thing to look wrong.
- Praedy's Staves PBR now that weapons are unblocked. It should work where it previously could not.
- The pig iron Complex Material set going live for the first time.
- Any armour picking up a dynamic cubemap it did not have before.
- Vanilla PBR AIO's dungeon coverage against Ruins Clutter Improved PBR and the Forgotten Retex Project.
- The dwarven ingot, per section 6a.
- Where ore veins meet cave rock, to confirm the blending holds with both Vanaheimr mods on PBR.
- Markarth columns and inn windows, after the two dwemer patches come off.
- VRAM. Armour and weapon patching plus Vanilla PBR AIO both add load.

---

## 14. Build record — 2026-08-28

Everything is in place. One step is left and it is yours, explained at the end.

### Done

1. **PGPatcher 1.2.0** installed clean to `tools/PGPatcher-1.2.0`. The 1.0.0.0 folder is untouched and still serves the other four profiles.
2. **Settings forwarded** with exactly the four intended changes: PBR on, output redirected, the two dead armour and weapon blocklist patterns dropped, and armour, armour-addon and weapon added to the record types. The blocklist keeps character actors and the UBE folder. The patcher's cached conflict state for your 72 texture-supplying mods carried across byte-identical.
3. **Profile cloned** as `DEEZ CS NUTZ - PBR`, all eleven files byte-identical, saves copied so a character can be loaded.
4. **28 mods installed**, 15.29 GB on disk.
5. **New output mod** `Authoria - PG Output - PBR` created and registered. The old output was never written to and still holds its 15,559 files.
6. **Load order applied**: 29 mods added, 0 removed, 7 disabled. Three new ESL plugins placed with masters verified.
7. **A tool entry** was added to MO2 called **PGPatcher 1.2.0 - PBR**, pre-set with the right arguments.

### Changed from the plan during the build

**Realistic PBR Footprints was dropped.** Its texture sets key on records that live in `Footprints.esp`, and its own plugin masters that file. You run the DLL-only Footprints 1.6.1, which has no plugin at all. The mod would have installed cleanly and done nothing, or thrown a missing master. Nothing replaces it; footprints stay as they are.

**Vanilla PBR AIO lost its sky and impact decals.** The trim revealed a complete sky replacer inside it — both moons in every phase, aurora, constellations, galaxy, stars, sun, Sovngarde nebulas — plus flame and frost impact decals. Those would have fought Praedys Sky and Parallax Spell Impacts. 36 files removed on top of the planned trim. Seven vanilla-path files remain, all in scope: two falmer glow maps, two nordic ruin dragon glows, and a puddle decal.

**The dwarven ingot question is settled.** Vanaheimr Ore Veins 4.0 ships its own dwarven ingot albedo, normal, parallax and roughness set plus a config for it. The Ancient Dwemer Metal ore patch stays enabled but is now redundant for that item, and harmless.

**Nordic Stonewalls style choices.** The installer offers two terrace styles and two stonewall styles. Nothing in your install reveals which you originally picked, so I took Nordic and Style 1. Purely a look preference, and a one-mod reinstall to change.

**CC Alternative Armors includes Dwarven Plate and Dwarven Mail.** Those went in. Your decision was that vanilla dwarven gear stays flat because nothing exists to convert it — this is different gear that does have a conversion. Worth an eye in game: CC dwarven will read as PBR while vanilla dwarven does not.

### Disabled in the new profile only

- `Authoria - PG Output` — replaced by the PBR output
- `Vanaheimr - Ore Veins` — replaced by PBR 4.0
- `Vanaheimr - Mines and Caves` — replaced by the PBR 4k build
- `Stony AF Markarth Complex Material` — replaced by Stony AF PBR
- `Tomato's Imperial Forts 2.0 - Complex Material` — replaced by the Remake PBR
- `Ancient Dwemer Metal - Stony AF Markarth` — stranded by the PBR swap
- `Dwemer Pipework Reworked - Stony AF Markarth` — stranded by the PBR swap

### New plugins and where they went

All three are ESL-flagged, so no full slot is used and you stay at 240 of 254.

- `Sanguine Symphony - PBR.esp` after `Sanguine Symphony.esp`
- `Vanilla PBR.esp` and `Vanaheimr - Mines and Caves - PBR.esp` after `Vanaheimr Landscapes.esp`

Your plugin order is hand-curated, so these are conservative placements, not judgements about where they belong. Masters load earlier in all three cases. Move them if you would rather they sat elsewhere.

### The last step is yours

The patcher refuses to run outside MO2's virtual file system. I tried it directly and it stopped at "VFS not detected" before touching anything. It needs the merged data tree to load a 4,000-plugin order, and there is an override flag but using it would mean the patcher reads a partial file tree and produces a wrong result.

MO2 is already pointed at the new profile. Launch **PGPatcher 1.2.0 - PBR** from the MO2 tool dropdown. It will start on its own and skip facegen.

Expect it to take longer than your previous runs and produce a larger output, because armour and weapon meshes are now in scope for the first time.

When it finishes, tell me and I will read the log and report what came out PBR against Complex Material and parallax, how many armour and weapon meshes were touched, and anything it complained about.

### Rollback

Everything is reversible and nothing the other four profiles use was modified.

- Switch back to the `DEEZ CS NUTZ` profile and the build is exactly as it was.
- Backups written: `modlist.txt.bak-prepbr-20260828`, `plugins.txt.bak-prepbr-20260828`, `loadorder.txt.bak-prepbr-20260828`, `plugingroups.txt.bak-prepbr-20260828` in the new profile, plus `ModOrganizer.ini.bak-prepbr-20260828` and `ModOrganizer.ini.bak-preexe-20260828`.

---

## 15. Patcher run result — 2026-08-28

### It worked

348 seconds. 116,106 meshes read, **88,576 patched**, 227,649 textures processed. Output is 25,767 files and 6.1 GB, against 15,553 meshes before — roughly ten thousand more, which is armour and weapons entering the pipeline for the first time.

**PBR is live.** Sampling 2,100 output meshes across the fourteen largest areas, 59% now point at PBR textures:

| Area | PBR |
|---|---|
| NordwarUA armour | 100% |
| Clutter | 93% |
| Creation Club | 91% |
| EEK's Whiterun interiors | 84% |
| Praedy's sets | 84% |
| Dawnguard | 81% |
| Dungeons | 77% |
| Dragonborn | 61% |
| Actors | 61% |
| Architecture | 31% |
| Armour | 22% |
| Landscape | 6% |

Architecture sits low because the trim removed Vanilla PBR's city coverage — what remains is Stony AF Markarth, Nordic Stonewalls and the Imperial Forts. Landscape is low by design, since no landscape PBR was installed. Armour at 22% is the four add-ons covering their specific sets, not all gear.

**Both exclusions held exactly.** Zero UBE meshes patched. Zero facegen meshes patched.

### Errors: seven, all minor

- Three weight-slider variants skipped because the `_0` and `_1` meshes do not match: a gore amulet and two Val Serano pieces. Those items lose slider-aware patching, nothing else.
- Two Inigo weapon material maps could not be processed, so his thunder sword and lightning bow keep their old surface.
- One unresolved model record in the Einar Wardrobe plugin.
- One missing-masters complaint about the Reqtificator output. **This is pre-existing** — it appears in the old patcher's logs too, and is unrelated to this work.

### One thing broke, and it needs a rerun

**`Authoria - PG Output` is empty.** It held 15,559 files.

The aborted run did this, not the successful one. The old patcher deletes its output folder early in startup, *before* it shows the mod priority dialog. So by the time that dialog appeared and got cancelled, the shared output was already gone.

All four non-PBR profiles have that mod enabled and reference `PGPatcher.esp` and `PG_1.esp`, which no longer exist. Those profiles will run without their parallax and complex material meshes and with two missing plugins until it is regenerated.

**The fix:** switch to the `DEEZ CS NUTZ` profile and run the old tool once. It writes to `Authoria - PG Output` and restores the status quo. Takes about six minutes.

To make the two impossible to confuse again, the old MO2 tool entry is now named **ParallaxGen 1.0 (NON-PBR profiles only)** against **PGPatcher 1.2.0 - PBR**. Say the word if you would rather have the plain name back.

### Standing rule this exposes

One output mod shared by five profiles was always fragile — any patcher run wipes it before it knows which profile it is serving. The PBR profile now has its own. The other four still share one, so a run under any of them regenerates it for all four.

### Restore confirmed — 2026-08-28 05:03

The shared output is back: **15,570 files, 3.4 GB, 15,564 meshes**, with `PGPatcher.esp` and `PG_1.esp` present again, so the four non-PBR profiles resolve their plugins. 243 seconds, 4 errors, all the same pre-existing ones.

Slightly larger than the 15,553 meshes it held before, because it regenerated against the current state of `DEEZ CS NUTZ` rather than the 2026-08-19 snapshot it was carrying. It is now up to date rather than four batches stale.

Verified it read the non-PBR profile: **0 of 400 sampled meshes reference PBR textures.** Clean separation.

The PBR output was untouched by that run — still 25,767 files and 6.1 GB.

**Both profiles are now correct and independent. The work is complete.**
