# Horse switch plan: Witcher Horse Expansion -> SC Horses + Equestrian (with the DBReV voice switch)

Written 2026-10-14. Replaces the 2026-10-12 investigation (its findings are folded in below).
Status: HORSE SWITCH BUILT 2026-10-17 (see section 0). Sections 6, 8 and 10 and the voice switch (section 4) are not done yet.
Applies to `DEEZ CS NUTZ - PICTA` and `Authoria - Preset Studio - HPH` (same change in both); the other six profiles get the new lines written DISABLED at the same neighbours.

Source files: `C:\Users\User\Downloads\sc horses\` (13 archives). Plugins extracted and scanned in the session scratchpad (`sc_plugins\`, `espscan.json`).

---

## 0. BUILT 2026-10-17 (the horse switch only)

Done in both live profiles (PICTA and Preset Studio). The other seven profiles carry every new line switched off and keep their Witcher setup. MO2 and the game were closed for every write. Backups of all four profile files in all nine profiles: `_backups\2026-10-17 - sc horses switch - pre-placement` and `... - placement 2`. Plugin backups: `... - plugins`, `... - skyking`.

What went in:
- SC Horses (meshes converted, plugin flagged light), Equestrian, Let Horses be Horses patch, Realistic Eyes, Glowing fix, Mane Fix, Low Effort Harness Refit, the SC patches for Animated Carriage, Kiai, Gore and the CC wild horses, Followers Ride Horses, Animated Mounted Casting.
- Switched off: the Witcher block and pick 6 (plus the small Shadowmere retexture plugin folder).
- Authoria builds: the horse race patch (SC skeleton on HorseRace, CYRHorseRace, CartHorseRace, both sexes), the Requiem input patch for Equestrian (vendor chests, stable hands, the three saddles, the eleven Bruma horses), the post-output Equestrian patch (Katla, Thogull's skin, the follower saddle), the SC carriage x ACTYE patch, the packsaddle SC refit, the Whistle Key saddle gate, the Followers Ride Horses exclusion list, and the Skyking carriages rebuilt on the SC carriage meshes.
- Cleaned in place: the HAYF patch, the Requiem Kaidan and CC wild horse patches, the Reqtificator output, the Synthesis gameplay output and the PBR output (each lost only its Witcher links).

Two changes from the plan:
- The Requiem input patch sits directly before the Reqtificator output, not in the old Witcher Requiem slot. The records it feeds are won further down (Legacy chest patch, container merge, TSOS, MOS, the Bruma master patch), so the old slot would have lost.
- Katla and Thogull are handled in the post-output Equestrian patch, because the NPC appearance output and HAYF win them after the Reqtificator.

Verified: full plugins PICTA 245 of 254, Preset Studio 242 of 254. No missing master and no master loading late in either profile. All four new patches win their records except the Requiem input, which waits for the Reqtificator rerun. Every SC horse file, the gate script, the packsaddles and the exclusion file win. No active plugin names any of the 300 files that only Witcher provided.

Still owed by the user: Pandora (Animated Mounted Casting), the Reqtificator, then Synthesis (its outputs load after the Reqtificator output and read it), then the in-game checks in section 9 step 5. Worst case for the Reqtificator output's masters after this switch: 245 of 254. Still owed by me after the Reqtificator and NPC appearance reruns: re-check the post-output Equestrian patch against the new outputs. Sections 6, 8 and 10 (MCM Bridge, the batch archives) are not done yet.

---

## 1. Your picks (everything else is routine and I do it)

| # | Question | Recommended | Why / the other way |
|---|---|---|---|
| P1 | The 9 SC horse meshes (body, saddles, skeleton) are in the OLD Skyrim LE file format (2020 files). Convert them? | **Yes - SSE NIF Optimizer 3.2.1 (DOWNLOADED 10-14, in your Downloads folder)**; I run it on the 9 files, nothing else. | Leaving them as-is works for many people but the old format is a known crash and shader risk in SE. |
| P2 | CC Wild Horses: today they wear Witcher skins. After the switch they go back to their CC look and lose their mane (the mane fix empties the vanilla mane). | **The optional "Wild Horses CC Patch" (DOWNLOADED 10-14, twice; one copy is enough)** - wild horses use the SC body, no bald horses. I rebuild our CC Wild Horses Requiem patch on it. | Skip it and accept vanilla-looking, mane-less wild horses. |
| P3 | Follower horses: **Followers Ride Horses 1.1.2 (DOWNLOADED 10-14) goes in - your call** - with your rule: it must never touch a follower who brings their own horse. | **Yes, with the exclusion in 3.11.** Ride Along (batch) stays for the rest. | - |
| P4 | Animated Mounted Casting (your friend's pick: cast one-handed spells from horseback, summon-horse spell). | **Yes (DOWNLOADED 10-14)** - ESL, no scripts, HorsePower's author lists it as compatible. It needs the Pandora run you already owe for Animated Poisons Redone. | Skip; no Pandora dependency from the horse switch at all. |
| P5 | DBReV lane downloads (manager-only files): Dragonborn ReVoiced 1.5.2, Audio Util 0.9.29 (optional - only matters with Conditional Expressions Extended 2.3.0, you are on 2.2.1), CEE 2.3.0 update. Gestures are already in your skywim folder. | **PARKED (your call, 2026-10-15): the voice switch waits until you have made the Eleonora pack for DBReV.** The three files (DBReV 1.5.2, Audio Util 0.9.29, CEE 2.3.0) stay downloaded and untouched; Dragonborn Voice Over and its Vel'dun dialogue patch stay exactly as they are. SKSE Menu Framework 3.18 still goes in (MCM Bridge). | - |
| P6 | Horse retextures that stop doing anything after the switch (Fluffworks horse fur, both Yee Haaaa saddle packs, both Shadowmere saddle packs, Shoulder Harness retexture). | **YES (2026-10-15): disable the six horse-only folders.** HAYF is NOT one of them: Horses Are Your Friends stays whole, its packsaddles are refit to the SC body and its patch is rebuilt against Equestrian (3.5) - your words: "keep HAYF saddlepacks, or we patch HAYF and Equestrian". | - |

Defaults I will apply unless you say otherwise: Let Horses be Horses = yes (needed for a sane vanilla start), Realistic Eyes = yes, Glowing Horse Fix = yes, Tight harness refit = yes, Immersive Horses esp replacer = NOT used (we run HAYF, not Immersive Horses), HorsePower's own "SC Horses skeleton patch" = NOT used (see 3.2 - it would wipe Requiem's horse stats), Sigils of Skyrim = skipped (banner saddles still work, just not colour-matched).

---

## 2. What is in the folder and what each file does

| Archive | What it is | Plugin | Verdict |
|---|---|---|---|
| SC_HorseReplacer.7z | The base: 5 horse bodies, Shadowmere, 2 saddles, a skeleton, textures (Patreon, 2020) | SC_HorseReplacer.esp - override only (9 skins, 2 races), ships FULL | Install. Flag the plugin light (no own records). Meshes are LE format -> P1. |
| Equestrian - An SC Horses Overhaul | 11 new breeds, 120+ saddles, faction barding, saddle bags, bannered saddles, named stable horses, saddle vendors at the 5 stables | Equestrian.esp - 525 records, 401 new, FULL and cannot be flagged (ids past the light range) | Install. Needs the Authoria patch in 3.4 before it is enabled. |
| Let Horses be Horses (LHBH) | Fixes Equestrian's broken horse speeds, the vanilla intro and 6 of its 10 "fox race" horses | 28 NPC overrides, light | Install above Equestrian. |
| Equestrian - Realistic Eyes Replacer | 3 1024px eye textures | none | Install. |
| SC Horses - Glowing Horse Fix | Black skin maps so SC horses stop glowing at dawn/dusk | none | Install above SC. |
| SC Horses Mane Fix | Empties the vanilla mane mesh (kills the double-mane bug) | none | Install above SC. The CC Wild Horses side is P2. |
| LowEffortHarnessRefit (Tight harness) | Vanilla harness mesh refit to the SC shape | none | Install above SC. |
| Animated Carriage - SC Horses Patch | 24 carriage meshes with SC horses + fitted harness, 4 cart-horse meshes | 16 carriage activator overrides, light | Install in the slot "Animated Carriage - Witcher Horses" holds now. Our Witcher x ACTYE patch is rebuilt on it (3.6). |
| Kaidan - Kiai - SC Horses Recolor | Kaidan's horse in black with red eyes | 1 NPC override + new skin, light | Install in the slot "Kaidan 2 Kiai Horse Replacer" holds now. Our Kaidan Requiem patch is re-pointed (3.7). |
| Gore - SC Horses Overhaul Patch (Equestrian version) | Gore's horse Count Fleet gets the black SC body and a hunter's saddle | 1 NPC override + 1 outfit, light | Install after Gore and Equestrian. Nothing of ours touches Count Fleet (only the Reqtificator output, which regenerates). |
| SC Horse - Beyond Bruma patch | Bruma's 11 horses on SC bodies + its horse race on the SC skeleton | 11 NPC + 1 race overrides, light | Do NOT enable as-is: its race record would wipe our Bruma master patch's Requiem stats, and its 11 horses sit under our Bruma master patch. I fold its changes into the Authoria patch (3.2, 3.4). |
| Horsepower Ragdoll - SC Horses Skeleton Patch | HorsePower's own merge of the horse race with the SC skeleton | 1 race override, light | Do NOT use: it loses to our Races Merge master patch, and if put above it, it wipes Requiem's horse stats. Our race patch (3.2) does the same job correctly. |
| Immersive Horses .esp Replacer | Only for people running Immersive Horses | full | Not used (we run Horses Are Your Friends). |

Player dialogue: **none of these plugins adds a single player line.** Equestrian sells saddles through vendor chests, not dialogue. Nothing to record for Eleonora from the horse switch.

---

## 3. The build (mine)

### 3.1 What goes out
Mod folders (disabled, kept on disk): Witcher Horse Expansion - rerun, Animated Carriage - Witcher Horses, CFTO - Witcher Horses Patch, Kaidan 2 Kiai Horse Replacer, Authoria - HAYF Packsaddle WHE Fit, houseCARL - Authoria - Patch - Animated Carriage - Witcher x ACTYE.
Plugins that go inactive (all light, so no slot change): Witcher Horses 2.0, Black Unicorn - CC Wild Horses, Witcher Horses - Animated Carriage Patch, Witcher Horse Expansion - CFTO patch, Markarth Outskirts - Witcher Horses patch (inside Markarth Outskirts), CT_70_BabyHorses_WitcherHorses_PATCH (inside City Trees), Kaidan - Forest Wedding Renewal - Witcher Horses Patch (inside Kaidan FWR), BWB - Kaidan 2 Kiai Witcher Horses Replacer, Authoria - Reqtificated - Witcher Horses, Authoria - Patch - Animated Carriage - Witcher x ACTYE.
CFTO's carriage horses are vanilla records, so they pick up the SC body with no patch at all.
Dependents found by TES4-header parse (17 plugins on disk master Witcher Horses 2.0, Kiai or HAYF); after the writes a whole-order missing-master check must read 0.

### 3.2 The horse race records (the one place the official patches get it wrong)
- Horse race: 7 plugins touch it; the winner is `Authoria - Master Patch - Races Merge.esp` (Requiem stats + HorsePower's ragdoll flags). SC's plugin only changes the male skeleton path.
- Bruma horse race: winner is `Authoria - Master Patch - Bruma.esp` (Requiem stats).
- Cart horse race: only vanilla touches it; SC's plugin wins cleanly.
- New light plugin **`Authoria - Patch - SC Horses - Races.esp`**, placed after the two master patches: Horse race = Races Merge copy + SC skeleton; Bruma horse race = Bruma master copy + SC skeleton; cart horse race = SC's version. The SC skeleton has the vanilla bone names (minus XPMSSE's extras), so every horse animation, HorsePower's directional set, the petting idles and the pose-correction DLL keep working. HorsePower's author ships an SC race patch himself, so SC skeleton + HorsePower ragdoll is a supported pair.

### 3.3 Mesh conversion (P1)
SSE NIF Optimizer on the 9 SC meshes only (Equestrian's 126, the carriage patch's 28, the Kiai/harness/mane meshes are already SE format - verified by header). I run it outside MO2; it is a standalone tool. Then the packsaddle measurement in 3.5 reads the converted body.

### 3.4 `Authoria - Patch - Equestrian.esp` (light) - what Equestrian breaks if enabled raw
1. It carries a 46 KB copy of the **Tamriel worldspace record** and one cell record from 2022. Enabled raw it would clobber our winning Tamriel record (climate = Picta weather, LOD, water, map). Fix: forward both headers from the last non-output winner (same method as the carriage Terrain Fit patch); its 5 placed objects stay.
2. Vendor chests: it overrides the Riverwood Trader chest (10 other plugins touch it, incl. Requiem vendor tweaks and LotD), the Solitude stables chest and Gunmar's chest. Fix: merged by hand - winner's items + Equestrian's saddle lists. Its override of a CK test container is dropped.
3. Fox race bug: Equestrian puts 10 vanilla horses on the fox race; LHBH fixes 6. The three caravan horses and the smuggler's horse stay foxes. Fix: race back to the horse race for those 4.
4. Bruma: the 11 Bruma horses get SC skins by forwarding only the skin field from the Bruma SC patch onto our Bruma master patch's records (the master patch keeps everything else).
5. The six stable factions Equestrian edits are touched by nobody else - clean. Its two horse leveled lists were only touched by Witcher Horses - clean; the Reqtificator merges leveled lists anyway.
6. Four stable hands (Geimund, Horm, Katla, Cedran): Equestrian's overrides add merchant factions; the Authoria patch forwards each live winner and adds only those factions (3.12 point 5).
7. The three vanilla saddles and the harness: winner's Requiem / Whistle Key fields kept, Equestrian's SC-fitted model and armature added (3.12 point 2).
8. Whistle Key's saddle stripper is gated (3.12 point 1) so Equestrian's one-part saddle outfits survive.

### 3.5 Horses Are Your Friends
- `Authoria - Patch - Horses Are Your Friends.esp` rebuilt without Witcher Horses: its 3 worn saddles already point at the vanilla saddle add-ons (which SC now re-points to SC meshes) - unchanged; its override of the horse saddle outfit collides with Equestrian's override of the same outfit - one merged outfit (Equestrian's random-saddle, bags and plate lists plus HAYF's worn saddle, four parts, which also keeps it out of the Whistle Key stripper). Arivanya, her packages and the stables quest unchanged. NEW (3.12): Thogull's skin becomes the vanilla brown skin (SC body + mane); his follower saddle add-on is re-pointed to the vanilla saddle add-on.
- `Authoria - HAYF Packsaddle WHE Fit` (packsaddles shrunk to 0.915 for the Witcher barrel) is retired. Measured 10-17: SC's barrel is about 9% slimmer than the Witcher body again and 2 units taller at the back (3.12 point 4), so the three saddle meshes get a new fit (`Authoria - HAYF Packsaddle SC Fit`), calibrated against Equestrian's own SC-fitted saddle.

### 3.6 Carriages
- The SC carriage patch overrides exactly the same 16 carts as our Witcher x ACTYE patch. New light plugin `Authoria - Patch - Animated Carriage - SC x ACTYE.esp` = SC's model paths + the go-anywhere script property. Old patch retired.
- `Authoria - Skyking Carriages - Over Outputs` holds 11 carriage meshes built from the Witcher versions with Skyking wood. Rebuilt from the SC patch's 24 carriage meshes with the existing script (`_tools\carriages\skyking_ac.py`). Carriage Stops, the Terrain Fit patch and the routes are untouched.

### 3.7 Kaidan, Gore, CC Wild Horses, Requiem
- `Authoria - Reqtificated - Kaidan.esp`: Kiai's skin field re-pointed from the BWB Witcher skin to the recolor's black skin; master swapped. One field.
- Gore patch: loads after Gore and Equestrian, before the Reqtificator output. No Authoria record touches Count Fleet.
- `Authoria - CC Wild Horses Reqtificated.esp`: rebuilt on the Mane Fix's CC patch (P2) instead of the Witcher Black Unicorn patch.
- New `Authoria - Reqtificated - Equestrian Horses.esp` (light) replaces `Authoria - Reqtificated - Witcher Horses.esp`: the 38 new breed NPCs and the 39 vanilla horse overrides get what the Witcher patch gave (stealth-meter flag, template flags, Requiem creature class), built with the requiem-npc-patching skill. Equestrian's 139 saddles and bardings are horse-worn armour (ratings 7-80); the Reqtificator leaves them alone (no Requiem material keywords) - shipped values stay.

### 3.8 Generated outputs (so the game launches before your tool runs)
- PG_1.esp (PBR output, the one PICTA uses): overrides 1 Witcher record -> removed in place, master pruned. No PG run.
- Synthesis Gameplay output: 20 Witcher spell-tome overrides -> stripped in place, master pruned (interim; your Synthesis run rebuilds it).
- Requiem for the Indifferent: masters Witcher Horses and HAYF (0 Witcher-defined records, references only) -> Witcher references stripped in place (interim; your Reqtificator run rebuilds it).

### 3.11 Followers Ride Horses - who it must leave alone (your rule, 2026-10-14)
"No Lucien, Inigo, Kaidan, or any of the followers with their own horses." The mod has the switch for this built in: its manager script skips any follower carrying the keyword `FRH_FollowerExclude` (it ships that keyword and distributes it to Meeko and Vigilance through SPID). So the rule becomes one Authoria SPID file that hands the same keyword to:
- Lucien (JRLucien) - own horse in Lucien.esp
- Inigo (Inigounique) - spawns his horse by script, no horse record of his own; excluded by your word
- Kaidan (00Kaidan) - Kiai
- Gore (HD1Gore, HD1CampGore and the Vigilant quest copies) - Count Fleet
- Val Serano (AX_ValSerano) - Windward, plus his summoned Bronze Equus
- Serana (DLC1Serana and the two Multiform copies) - Phoenix and Nightshade from Serana Dialogue Add-On; the mod would otherwise target her on purpose
- Remiel (HLIORemi) - Dumac
- Auri (018Auri) - Thistlefoot, her deer
Everyone else (Lydia, the FDE followers, hirelings, housecarls) stays eligible. Checked at build time: the two dialogue lines the mod adds carry the same exclusion, otherwise the script still refuses the assignment. Not installed: the mod's optional "Named Horses" SkyPatcher file - it renames the vanilla horses at runtime and would overwrite Equestrian's names (Queen Alfsigr, Pelelana, Caster, Nurnhilde, Basalta) and flip sex flags. The mod itself is light, one MCM Helper menu, two player lines for Eleonora.

### 3.12 HAYF and the horse systems - compatibility check (2026-10-17, from the records and scripts, not from memory)

**What HAYF is, as installed.** Horses Are Your Friends Lite: 752 records - mostly its own dialogue (flute, feeding, packsaddles, "teach me the skills", Thogull), 76 placed objects (the stables workbenches, barrels, chests), its own horse Thogull, Glonjar, two "saddle dog" chest actors, 5 quests (incl. an override of the vanilla `stables` quest), 1 keyword, 6 armour add-ons, 5 armours (two packsaddles, a flower saddle, Thogull's skin, a follower saddle). It overrides 8 vanilla exterior cells (headers only, already settled in the live order) and the Tamriel persistent cell. Our `Authoria - Patch - Horses Are Your Friends.esp` (loads last, after the Reqtificator and appearance outputs) carries Arivanya, three Hearthfire horses, the stables quest, Arivanya's packages, three NonPlayable saddle clones and the three vanilla saddle outfits.

**1. The saddle-stripping trap is real, and it would hit Equestrian.** The stripper is Horse Whistle Key, not HAYF: its horse effect runs `CheckSaddle()` the moment it lands on a horse: if the horse's outfit is NOT the naked outfit, has exactly ONE part, and that part carries the `ArmorHorseSaddle` keyword, the horse is switched to the naked outfit and the saddle dropped into its inventory. Re-equipping happens only in `OnItemAdded`, and that path is gated by the mod's "Saddles" toggle. **Your setting is `bSaddles = 0`** (Authoria - MCM and INI Settings), so the first half runs and the second never does: a bare horse with a saddle in its pockets. That is the August bug, now explained - and the August fix (keyword-less, NonPlayable clones in the outfits) worked because the clones never match the keyword test. Whistle Key's KID file tags every armour that carries the `ArmorHorseSaddle` keyword - which is Equestrian's own keyword on 126 of its 139 saddles. Equestrian dresses the five named hold horses, Frost, Cicero's Smiles, the courier horse, the Penitus Oculatus horse and the Dawnguard horse with ONE-part outfits holding keyworded saddles: all eleven would go naked the first time you ride them. The random three-part outfit (saddle + bags + plate lists) is safe: the one-part test fails on it; Karliah's two-part outfit is safe too.
Fix, two ways; I take the first unless you say otherwise:
- (a) **Gate the stripper.** A one-line Papyrus fix in a small `Authoria - Papyrus - Horse Whistle Key Saddle Gate` mod: `CheckSaddle()` only runs when the Saddles toggle is on - the behaviour the author clearly intended. Compiled with the known toolchain; covers vanilla, Equestrian and any future saddle in one go; the August clones stay and keep working. Re-check after any Whistle Key update (installed 1.x, last Nexus update 2025).
- (b) The August recipe again: eleven keyword-less NonPlayable twins of the eleven one-part outfit saddles, the eleven outfits re-pointed at the twins. No script change, more records, and every new saddle mod needs the same treatment.

**2. The three vanilla saddles are a five-way merge.** `HorseSaddle`, `HorseSaddleImperial`, `HorseSaddleShadowmere` are touched by Whistle Key (playable + crafting keywords), Requiem (names, value, weight, its keywords), our Reqtificated Whistle Key patch, the Reqtificator output - and now Equestrian (SC-fitted model and armature). Equestrian loads in the horse block and would lose every one of those fields to the later plugins; or, put above them, it would strip Requiem's values. The Authoria Equestrian patch (3.4) therefore carries all three: winner's name / value / weight / keywords / playable flag + Equestrian's model and armature. `HorseHarness` likewise (harness refit model + winner's fields).

**3. Thogull would come out vanilla-shaped and bald.** HAYF's own skin for Thogull points at the vanilla horse body file and the vanilla mane file with HAYF's own brown textures painted for the vanilla body. After the switch the vanilla body path is the plain game mesh again (Witcher Horses provided it), the mane file is the Mane Fix's empty mesh, and HAYF's textures do not fit the SC body's layout. Fix in the HAYF patch: Thogull wears the vanilla brown skin record (which SC now re-points to the SC brown body, mane included) - one field on his record, forwarded over the Reqtificator's version. Same for his follower saddle add-on: it names the vanilla saddle file by path with a HAYF recolour; re-pointed to the vanilla saddle add-on (now SC's saddle), recolour dropped.

**4. Packsaddles: refit confirmed necessary, numbers measured.** Barrel half-width at the saddle seat (bind pose, same measuring band): vanilla 29.2, Witcher Horses 25.1, SC 22.8; back height 121.4 / 122.4 / 124.1; belly under the girth 71.6 / 80.5 / 77.6. SC and Witcher Horses are the same Witcher 3 body (3,421 vertices each) but SC is about 9% slimmer again and 2 units taller at the back. The August 0.915 fit therefore sits proud again on SC; the new fit scales the saddle shape by roughly 0.91 of the current fit (about 0.83 of HAYF's original) in width, with the seat raised about 2 units, calibrated at build time against Equestrian's own SC-fitted saddle exactly the way the Witcher saddle was used in August. Both HAYF packsaddles and the flower saddle get the same transform. Still untouched, as in August: the HAYF bridle sinking into the head and the flower clusters sinking into the rump.

**5. Equestrian also rewrites four stable hands.** It overrides Geimund, Horm, Katla and Cedran to make them saddle sellers (Horm and Katla gain the merchant faction; Katla the Solitude stables service faction). Their live winners are the Reqtificator output (Geimund, Horm, Cedran) and the appearance merge (Katla); Equestrian's 2022 copies would wipe Requiem and appearance data if they won, and lose the merchant factions if they lost. The Authoria Equestrian patch forwards each winner and adds only the factions, placed after the appearance output like the HAYF patch.

**6. Followers Ride Horses, Ride Along 2.0, HAYF, Whistle Key - how they share the field.**
- Whistle Key's own script already knows Followers Ride Horses (it leaves a horse's confidence alone when FRH's spell is on it), so those two were written to coexist.
- FRH assigns an owned horse to a follower (never Lucien, Inigo, Kaidan, Gore, Val Serano, Serana, Remiel, Auri - 3.11); Ride Along seats followers on YOUR horse or lets one drive you; HAYF's Thogull is a purchasable horse with its own "let's travel on horseback" line. Three systems, no shared records: the only clash is giving the same follower two instructions at once (riding Thogull and being seated by the Ride Along key). Rule for play: one system per follower per ride; the in-game check tries each pair once.
- Call-your-horse: Whistle Key (last ridden horse), HAYF's flute (last dismounted), FRH's summon distance - all script-level, all already live together except FRH; FRH's horse protection flag duplicates HAYF's immortal-horse SkyPatcher lines harmlessly.
- Ride Along 2.0 on SC bodies: passengers sit by animation on the rider bones with configurable offsets; SC's back is 2 units higher than vanilla, inside the ini offsets' range. Its road-travel feature drives the horse by package along the navmesh, so Northern Roads and the Terrain Fit have nothing to do with it. Its climb clips are rider-only and HorsePower's directional set is horse-side, so no clip collides; mounted casting adds a rider state that passengers never enter. All three are in-game checks, not patch work.
- HAYF packsaddle (slot 45) versus Equestrian saddle bags (slot 46) and plate barding (46/47): a HAYF packsaddle replaces the saddle, not the bags, so a horse can carry Equestrian bags and a HAYF packsaddle at once - visually crowded, not broken; your choice per horse.

### 3.9 Placement (both profiles, MO2 closed, backups first, four profile files in lockstep)
Mod folders take the Witcher block's slots (PICTA modlist lines 2862-2865 and 1019, 3229, 3471): SC Horses in the Witcher slot; Mane Fix, Glowing fix, Tight harness, Realistic Eyes, Equestrian, LHBH above it (higher priority); AC SC patch in the "Animated Carriage - Witcher Horses" slot; Kiai recolor in the Kiai slot; Gore and Bruma patches beside Gore / Bruma; the new Authoria patches in `Authoria - Requiem Patches` / the houseCARL patch folders.
Plugins take the Witcher plugin slots (PICTA plugins.txt 1215-1219, 1248-1249): SC_HorseReplacer, Equestrian, LHBH, AC SC patch, Kiai recolor, Gore patch; the Authoria race/Equestrian/HAYF/carriage patches at their patch-block positions (after the master patches at 3950-3980, before the Reqtificator output at 4055). Nothing below the outputs. plugingroups.txt updated (the Witcher plugins carry the group "Visuals - Animals and Creatures").
Slot census after: PICTA 245/254 full (was 244: Equestrian +1, Witcher was light), Preset Studio 242/254. The DBVO slot comes back only when the parked voice switch happens (DBVO.esp is full, DBReV's plugin is light).

### 3.10 Verification (mine, before I say done)
Added 10-17: Thogull's and the follower saddle's asset chain resolves to SC meshes; the Whistle Key gate compiles and its toggle reads your 0; the eleven one-part Equestrian outfits keep their saddles on a fresh game (your in-game check: buy a hold horse, ride, dismount, look).
Whole-order missing-master check = 0; conflict tree on every record the new Authoria patches win; asset winners for the horse body, saddles, skeleton, mane, carriage meshes and the dialogue menu file; plugin census with MO2 closed; mod lines present in all 8 modlists.

---

## 4. The voice switch: Dragonborn Voice Over -> Dragonborn ReVoiced (DBReV 1.5.2) - PARKED 2026-10-15

**Your call 2026-10-15: not yet.** DBReV goes in only after you have made the Eleonora pack for it. Until then nothing in this section is executed: Dragonborn Voice Over, its Vel'dun dialogue patch and the Eleonora pack stay as they are today; the DBReV gesture pair, Audio Util and the CEE 2.3.0 update wait with it (CEE 2.3.0 is a plain update and could go in earlier if you ever want it on its own). The text below is kept as the ready-to-run recipe for that day.

**The only voice work inside this switch (your words, 2026-10-15): topic files for the new player lines, in the DBVO pipeline's format**, so you can record them with the usual tools. The lines are the same for DBReV: it plays DBVO 1.0 packs unchanged, so every recording made now carries over, and a DBReV-format pack later is built from the same dialogue text. After the installs I run the Eleonora pipeline once over the whole order (`winners.py` then `gen2.py`); it writes one topic file per plugin for every player line that has no recording yet (CP1252, CRLF, sorted, de-duped - the Voice Pack Maker's own format) into a dated `topic files` folder next to the earlier runs, plus the names-lines list. Expected sources in this batch: Followers Ride Horses (2 lines), Word Travels (a handful), the Ashe / SDA / banter-patch updates (only lines new since the installed versions); the horse mods add none.

What DBReV is: a rewrite of the player-voice framework. It plays DBVO 1.0 packs unchanged, drives lip-sync itself, works with any UI without patches, Cinematic Conversation Camera and SmartTalk, and since 1.4.6 matches edited lines to their files (that is exactly what our 26 "DBVO Fix" plugins rely on). Needs Address Library (have v11, fine for 1.6.1170), JContainers (have), SkyUI 5.2+ (have). Tested by its author on 1.6.1170.

Out: `Dragonborn Voice Over` (mod + DBVO.esp, a FULL plugin - frees a slot; DBReV's own plugin is light) and `Vel'dun UI - DBVO Dialogue Patch (1.0.5 carry-over)` (DBReV forbids every DBVO dialogue-menu patch). After that the dialogue menu file is Vel'dun UI's own unpatched one - verified as the next provider in the file stack.
Stays: `Eleonora Female Nord Dbvo Pack With Patches` (the 41,616-file pack + its 26 light DBVO Fix plugins), `Authoria - Eleonora - IFD Lydia`, `Eleonora - PC Head Tracking Voice Type`, `PC Head Tracking - MCM`. The pack's registration file keeps its place; checked against DBReV's readme on install.
In: DBReV 1.5.2; `DBReV Player Character Gestures (OAR)` + `DBReV Gesture Bridge` (both in the skywim folder); optional Audio Util + CEE 2.3.0 (P5); Cinematic Conversation Camera from the batch plan (DBReV's recommended camera; Switch Camera During Dialogue goes off with it, as the batch plan already says).
MCM: DBVO's menu out, DBReV's menu in; under MCM Bridge the DBReV menu shows raw label keys instead of words (cosmetic, see section 6).
New game: no mid-save migration steps needed (the mod page's StopQuest routine is only for continuing a save).

Eleonora lines (the "DBVO lines" prep): the horse switch adds none. After the batch and friend installs, I re-run the Eleonora pipeline (`_tools\eleonora-dbvo\winners.py` then `gen2.py`) to produce the topic files for every new player line; you record them with your usual pipeline; DBReV reads the result as a DBVO 1.0 pack. Which new mods carry player lines comes from the catalogue in section 7.

---

## 5. Animations - styles and blends (the user's explicit ask)

| Lane | What changes | Risk | Call |
|---|---|---|---|
| Horse body animations (HorsePower directional set, jump/land, petting idles, Horse Behaviour Improvements pose DLL) | Only the body mesh and skeleton file change; bone names match vanilla | none expected | keep as is; no Pandora run for the switch |
| Rider animations (Skyrim Mounted Movesets, TDM mounted archery, mount/dismount sound fix) | nothing | none | keep |
| Animated Mounted Casting (P4) | adds the mounted cast animation via a behaviour patch | Pandora run (same run as Animated Poisons Redone) | yes if P4 |
| Player gestures during voiced lines (DBReV gestures pack + bridge) vs Gesture Animation Remix vs Walk With Me command gestures | Remix is NPC-only (its base rule excludes the player; its named-actor rules list NPCs); WWM gestures fire on command keys outside dialogue; DBReV gestures fire while your line plays | no overlap; priorities checked at install | take |
| Fluffworks fur on horses | the SC body ignores the fur shells | horses lose the fur-shell look the other animals keep | accept (P6 disables the dead folders) |
| CC Horse Armor (Steel, Elven) | fitted to the vanilla body | may clip on the SC body | in-game check; Equestrian's own barding is the replacement if it clips |

---

## 6. MCM: MCM Bridge lifts the 128 cap (your call, 2026-10-14)

You keep **MCM Bridge** in the skywim folder, and it goes in with this batch. It replaces SkyUI's menu host with a native one: no 128-menu limit, menus register in seconds, and every MCM shows up inside FLICK (or SKSE Menu Framework). The MCM counting in this plan is therefore moot; the budget lines below are kept only as history.

What it needs and what it breaks (read from the mod page, 1.2.0 released today, and from the scripts in your 1.1.0 copy):
- **Get 1.2.0, not the 1.1.0 in the folder, plus its optional "MCMRecorder Patch (beta)".** The stable Bridge is listed as INCOMPATIBLE with MCM Recorder, and your whole init sequence runs on MCM Recorder (four recordings plus the OStim one). 1.2.0 adds the beta compatibility patch; "make sure nothing overwrites this patch" is the author's own instruction. Both files sit on Nexus's new storage, so you click Mod Manager Download.
- **Frontend:** FLICK 1.6.0 or newer, or SKSE Menu Framework 3.18 or newer. You run FLICK (`Fuzz's Legally Intelligible Core Kit`) and the 1.6.0 update is in the folder and in the batch, so FLICK is the frontend; SKSE Menu Framework stays at 3.8 for the mods that use it. If Bridge still objects to 3.8, SMF 3.18 is the fallback download.
- MCM Helper 1.6.2 (installed) is a supported build. SkyUI and Address Library are fine.
- **Script winners:** Bridge ships its own `SKI_ConfigManager` and `SKI_ConfigBase`. Today MCM Recorder wins the first and `Authoria - Papyrus - MCM Recorder Fix` wins the second. Bridge (and its Recorder patch) must win both, so Bridge goes above MCM Recorder, and the Authoria fix's `SKI_ConfigBase` is retired (its job, the registration race, no longer exists). Its other file, the recorder player script, is compared against the beta patch on install and kept only if the patch does not replace it.
- **The init sequence:** its "MCM rebuild" step reads SkyUI's 128-entry name table and calls the SkyUI reset. Bridge's manager has no name table, so that step would log errors and wait on a count of zero. I rebuild the init script with that step removed (the 08-20 race it worked around is gone with Bridge) using the known compile setup, and verify on your first new-game log.
- **MCM Slot Trim** (the three menus cut on 08-28: Better Third Person Selection, OBody NG, VioLens) is no longer needed: retired, so those menus come back on a new game.
- **DBReV under Bridge** (for the day the voice switch happens): works, but its menu shows raw label keys instead of words (the Bridge author cannot fix it without DBReV's source). Cosmetic; the options still work. Dragonborn Voice Over's own menu is an ordinary SkyUI menu and is fine under Bridge.
- The one unknown is the beta Recorder patch itself ("worked for me, not broadly tested"). The test is your first new-game init run: if a recording stalls on "waiting for X MCM", the fallback is Bridge off, Recorder stack back as today, until the patch matures.

History (for the record): cap 128, last measured 128/128 on 08-28, three menus trimmed since; this plan would have added DBReV (+1, DBVO -1), FEC (+1), Word Travels (+1), Followers Ride Horses (+1 if taken). With Bridge none of that counts.

## 7. The friend's repo and the 47 new skywim downloads
Friend items that belong to this plan: Followers Ride Horses (P3 = yes with the exclusion rule in 3.11), Animated Mounted Casting (P4), the DBReV gesture pair (section 4), the OAR stack update (OAR 3.2.1 + Math 1.0.5 + Detection 2.1.5 + Animation Queue Fix 1.0.2 + Paired Animation Improvements 1.0.3 - take, foundation for every animation add), Guards-and-Bandits Fidgets (needs its Nexus file; not in any folder yet). His "Horse Whistle Key - named horses" SkyPatcher is redundant: Equestrian names the stable horses itself. Everything else from his list stays as decided in `FRIEND-CHANGES-PICKS-20261012.md`. MCM Bridge (skywim folder, 1.1.0; 1.2.0 needed) is now IN by your call - section 6.
The 47 archives added to the skywim folder since the 10-12 plan are decided in section 8; the full catalogue is `SKYWIM-CATALOG-NEW-20261014.md`.

## 8. The 47 new skywim archives (added since the 10-12 plan) - decisions

Full catalogue (per archive: contents, plugins and flags, OAR submods and what they gate on, DLLs, MCMs, voice counts, overlaps): `SKYWIM-CATALOG-NEW-20261014.md`. Headline facts: only four full plugins and three of those are updates of plugins already active (Ashe, the Ashe/Serana banter patch, SDA); ROPE's full plugin has a light twin. Everything else is light or plugin-free.

### 8a. Goes in with this batch - no Requiem patching, no body work
| Mod | Notes |
|---|---|
| Arm Movement Animations 3.0.2, NPC Animation Remix 2.4.2, Female Merchant Counter Animations, Dynamic Relaxed Sneak, UNDERDOG injured-leg guards, Sonders Raysense Wall Leaning 1.2 (update) | OAR idle packs. They layer by priority (the catalogue lists every priority); before enabling I check each against the installed idle packs (EVG, the Dynamic Female set, Goetia / Vanargand walk-run) and add a user.json where two packs claim the same idle. No Pandora run. |
| Dynamic Feminine Female Modesty Animations 4.30 + its KID patch | 108 OAR submods, one light plugin. Same priority check; UBE women use the vanilla female skeleton, so it applies. |
| DBReV Player Character Gestures + DBReV Gesture Bridge | PARKED with DBReV (section 4). Player-side gestures while your line plays; no clash with Gesture Animation Remix (NPC-only) or Walk With Me command gestures. |
| CCC Customized Close Preset | Only with Cinematic Conversation Camera (batch plan). |
| Dear Dragonborn 1.1, Fight With Me **0.3.0**, IHarvestNG 1.0.8, Ride Along **V2.0**, FLICK NG 1.6.0 | Newer files for batch-plan items; every older copy in the folder is superseded (Dear Dragonborn 1.0, Fight With Me 0.1.0 / 0.1.5 / 0.2.0, IHarvestNG 1.0.7, Ride Along 1.1.0 / 1.2.1, both FLICK 1.5.0 copies, Khajiit Fur 1.1 / 1.2). IHarvestNG still needs the magic patching the batch plan lists. Ride Along 2.0 and Fight With Me 0.3.0 details in 10a. |
| Frostwalker 2.2 | Frost spells freeze water (and lava) into walkable floes. SKSE + light plugin, needs KID / SPID / po3 Tweaks (all installed). SKSE Menu Framework settings, no MCM slot. |
| ROPE (use the ESL twin) + ROPE SMIM Ropes Patch | Swaps 82 vanilla rope objects through Base Object Swapper for physics ropes. SMIM's ropes stop applying there, and any existing BOS lines on those objects collide - I diff against `Authoria - Base Object Swapper Patches` first. |
| Hearthfire Multiple Adoptions - Assorted Patches (your friend's) | USSEP bed fixes + Lux variant go in as-is. The Requiem one overrides the same sleep quest as our houseCARL HMA Expanded Requiem patch - merged into ours, not stacked. |
| Hitch Hunter And Fixes 1.2.0 (1.1.1 superseded) | A hitch-finding tool (your friend keeps it OFF). Installed disabled; switched on only while hunting a stutter. |
| MCM Bridge 1.2.0 + MCMRecorder Patch (beta) | Your call of 10-14: goes in. Needs the two downloads (section 6); the 1.1.0 copy in the folder is superseded. |

### 8b. Updates of installed mods (folder swap, settings carried over)
| Mod | What to carry / re-check |
|---|---|
| Ashe - Crystal Heart 1.3.7 (from 1.3.6a) | Full plugin already active (no slot change). Ships a FNIS behaviour -> Pandora run. 795 player lines - only the lines new since 1.3.6a need Eleonora recordings (the pipeline reports the delta). Re-check your friend's two Ashe OAR comma fixes against the new files. |
| Ashe and Serana Banter Patch 1.0.12 (from 1.0.10) | Full plugin already active. 51 player lines, delta only. |
| Serana Dialogue Add-On 4.4.1 (from 4.3.2) | Full plugin already active. 2,698 scripts: the two Authoria SDA script fixes (`Authoria - Papyrus - Misc - SDA`, `- Base Mismatch - SDA`) must be re-validated against the new scripts before they stay enabled. FNIS behaviour -> Pandora run. 2,694 player lines, delta only. |
| Bobbing Framework 3.2 (from 2.0) | Keep the `[NoDelete] Bobbing Framework Configs` folder above it; re-check its config keys against 3.2. |
| Dynamic Bloodpool Framework 1.1.1 (from 1.0.1) | ini carry-over. |
| FollowerParkour 3.2 (from 2.0) | The installed copy is DISABLED in PICTA. Folder updated, stays disabled unless you say otherwise. |
| ISL Helper 1.0.6, ParticleWind NG 4.1.1 (from 3.5), Skyrim Water Inertia 1.4.1 (from 1.0.0) | DLL swaps; Water Inertia's MCM slot is already held. |
| Swimming Extensions (Svimex) 1.1.1 (from 1.0.1) | Ships a Nemesis/Pandora patch -> Pandora run. |
| Walk With Me 0.3.0 - Command Gestures (from 0.2.2) | Pandora patch; its files must win over Offset Movement Animation (placement, not a patch). Goes with the Walk With Me 0.3.0 main update from the batch plan. |

### 8c. Your picks from this group
| # | Question | Recommended |
|---|---|---|
| P7 | Frozen Electrocuted Combustion 6.1.3 + Extra Crispy retexture (burn / freeze / shock death visuals; your friend runs it). One MCM menu (free under MCM Bridge); three DLL builds inside, I take the 1.6.1170 one. | **YES (2026-10-15).** |
| P8 | Word Travels 1.3.1 (NPCs comment on your deeds; 1.2.0 superseded). One MCM menu (free under MCM Bridge); a few new player lines. | **YES (2026-10-15).** |
| P9 | Mage Towers of Skyrim 1.7 (new mage towers in the world; 13 light plugins). | **YES (2026-10-15).** Your plan: a full LOD run after ALL the file changes (this batch plus your friend's GitHub items) - the towers' distant meshes get picked up then. Install detail in 8e. |
| P10 | NPC Situational Reactions voice packs (7 archives, 1.9 GB + 6 x 0.2 GB). Dead weight until NSR itself is installed (batch pick P15, needs Address Library v13). Pack 1 already contains the Child, Commoner, EvenToned and Nord packs that sit in the folder as separate files; the six newer per-voice packs are not in Pack 1. | **PARKED (my call on your "whatever is smartest", 10-15).** The main NPC Situational Reactions page is gone from Nexus right now (the lookup returns "mod not found"; only the voice-pack page is still up and updating). No page = no updates, no support, and it would also force the Address Library change that every SKSE mod shares. The files stay in the folder untouched; revisit when the page is back. |
| P11 | Wargenie's Lazy Snow Cover Config - overrides the snow-cover settings Bottled Shaders ships. Your visuals stack is locked. | **Stays out (10-15).** What it changes, in plain words: it rewrites all six snow-cover settings files (Tamriel and the five city worlds). Bottled's own files keep the snow weather-driven only, with the default snow look, no tinting, and the altitude snow line switched off. Wargenie's turn on a seasonal snow line by height (winter month 3, summer month 9, the line moving 20,000 units up and down), tint grass and trees white under snow, swap in the PBR snow and frozen-marsh textures, let snow sit on steeper slopes, double the blend distance, and add object and weather fades. Your seasons already come from Seasonal Landscapes and the Picta weather patch, so this would stack a second winter on top of them - a visuals change, and your visuals are locked. |
| P12 | Dark Watchtowers - Dark Version: plugin only; its 17 tower pieces point at meshes that live in the MAIN Dark Watchtowers file, which is not downloaded. | **YES (10-15) - you were right.** Dark and Grim are the one-or-the-other choice; both need Yuril's resource pack (YAR), which you already have installed, and every tower mesh resolves to it (checked). The plugin is light: 921 placed objects, 17 statics, no navmesh records, no scripts. It overrides the Tamriel worldspace record and 37 exterior cells - headers forwarded from our winners, same as Equestrian. Every one of those 37 cells is also touched by Northern Roads (and most by Lux Via), so each tower site gets a placement check against the new roads before it is enabled; a tower standing on a road is nudged or dropped. The author's suggested LOD rerun is covered by your planned full LOD run. |
| - | Dynamic Khajiit Fur Shaders 1.2 | Stays batch pick P13 (deferred: needs a shell-fur shader host; unverified under Bottled). |

### 8e. Mage Towers of Skyrim - install detail (P9 = yes)
- Core: one light plugin, 1,117 records - almost all placed objects and statics, 14 new navmeshes and 7 navmesh overrides, one interior, no NPC records, no scripts, no menu. So: no Requiem patching.
- It overrides the Tamriel worldspace record and 10 exterior cells (the five tower exteriors and one tundra point of interest). Same treatment as Equestrian: world and cell headers forwarded from our winners; its placed objects stay. The five tower exteriors get a conflict tree against Northern Roads, the landscape and seasonal plugins, and their navmeshes are checked for a clean join (navmesh overrides carve, they never delete - see the navcut rule).
- Patches to take from its FOMOD: Nature of the Wild Lands (one of the two variants - matched to the installed NOTWL at build time), Water for ENB / Shades of Skyrim (loads after every other Mage Towers patch), The Cause (its Creation Club master is one of the always-loaded plugins, so it is present). Skipped: the Witcher Horse Expansion patch (Witcher Horses leaves), and the Happy Little Trees, Fabled Forests, Marshlands, Snow Throat, Tirashan and Ulvenwald patches (those mods are not installed).
- Its distant meshes come alive in the full LOD run you plan after all the file changes; until then the towers show at close range only.

### 8d. What this group adds to your follow-up steps
- Pandora: Ashe 1.3.7, SDA 4.4.1, Svimex 1.1.1, Walk With Me gestures 0.3.0 (plus Animated Mounted Casting if P4, plus Animated Poisons Redone from the batch) - one run covers all of them.
- MCM: FEC and Word Travels each add a menu; with MCM Bridge (section 6) that costs nothing. Everything else here uses SKSE Menu Framework or ini files.
- Eleonora lines: Ashe, SDA and the banter patch bring new player lines (deltas only), Ride Along 2.0 brings 46, Word Travels a handful, Followers Ride Horses 2 (AJO 67 if P14). Topic files come from the pipeline after the installs (section 4).
- BodySlide: nothing in this group.

---

## 10. Downloads added 2026-10-15 to 10-17 (refamiliarised 10-17) - decisions

Full catalogue: `SKYWIM-CATALOG-NEW2-20261017.md` (34 entries). Instance changes since the plan was written: plugin slots unchanged (PICTA 244/254, Preset Studio 241/254); the horse block sits four mod-list lines lower (other sessions added mods above it - placements in 3.9 are by neighbour, so nothing moves); the carriage Terrain Fit patch was rebuilt on 10-15 (bridge crowns) by another session - re-read before 3.6, not touched by this plan; Skyrim Upscaler Build 20 is live; Bottled Shaders stays 1.0.11 (1.0.14 and 1.0.15 are downloaded - the visuals lane, outside this plan). MO2 and the game were closed at 10-17 check time.

### 10a. Newer versions of things already in this plan (the newer file is used, the older copies are ignored)
| Mod | Now | What changed, and what it means here |
|---|---|---|
| Ride Along | V2.0 (file 2.3) replaces 1.2.1 | Major: up to four passengers on your horse (behind, in front, on your shoulders), and a follower can drive your horse by road to 31 places ("Take me somewhere on my horse", no fast travel - needs PapyrusUtil, installed). Plugin grows from 45 to 640 records, still light; a new OAR seats pack; 46 player lines for Eleonora. Pairs with Followers Ride Horses exactly as planned (yours seats them, FRH gives them their own). The Princess Seat add-on is not in the folder; not needed. |
| Fight With Me | 0.3.0 replaces 0.1.5 / 0.2.0 | Adds an auto-battle "Sight" mode and path bonuses; follower potion use was REMOVED; its spell effects now come from Triumvirate, Elemental Destruction Magic Redux (not installed) or Vibrant Weapons - checked at install so nothing points at a missing effect. SKSE Menu Framework, no MCM slot. |
| Word Travels | 1.3.1 replaces 1.2.0 | Story-group settings page added; voice files unchanged. MCM Helper menu (free under Bridge). |
| Hitch Hunter and Fixes | 1.2.0 replaces 1.1.1 | DLL only; plugin pre-warm now off by default. Still installed disabled, diagnostic use only. |
| Dynamic Underwater Fish | 1.1 replaces 1.01 | Settings file format changed (fish groups) - the batch plan's "spawn logging off, fish cap" settings get re-applied on the new file. |
| Dynamic Khajiit Fur Shaders | 1.3 | Stays deferred (batch P13) and is effectively blocked: it needs the Fur Shells shader, which Bottled has disabled at boot since 1.0.7. |
| Zodd's female bleedout | 1.1 | Stays skipped (batch P11): competes with the enabled Crawling Bleedout. |
| NPC Situational Reactions packs 2, 3, 4 + MaleDrunk + MaleOldKindly | - | Parked with NSR (P10). Pack 2 duplicates six of the single-voice archives already in the folder - cleanup when NSR comes back. |
| Bottled Shaders 1.0.14 / 1.0.15 | downloaded, 1.0.11 installed | Not this plan. Note for whoever updates it: the six hand-edited snow-cover files and the snow map are unchanged upstream, so the live edits must be carried over; a new rain-refraction feature overlaps the Picta raindrop patch; the 20 upscaling files are the parked set. |
| FasterNGIO | 1.6 (tool, 10-17) | Tool update for the offline grass-cache baker installed on 10-15 (new D3D12 runtime folder, radius/cell and inspect options; no changelog published). I update the tool folder; the bake stays yours. |
| LDD RFAOS Goam ears add-on | 2.0 | Deferred with batch P14 (RFAOS itself deferred; Goam ears are disabled). |

### 10b. New mods - routine, no pick needed
| Mod | Verdict |
|---|---|
| Dog Bleedout Animation (OAR) | In. One OAR rule, dogs only, nothing else claims it. |
| Global Particle Normaliser (+ Source) | OUT - cannot load. The DLL is the old 1.5.97-only kind (query export only); the author says 1.5.97 / old SKSE. The source archive is code only. |
| Piggyback 1.2.1 | In only if P18 (FollowerParaglide needs it); otherwise not installed. Nexus has 1.2.2 - fetched with your OK if P18 is yes. |

### 10c. Your picks from this group
| # | Question | Recommended |
|---|---|---|
| P14 | **AJO - Andrealletius Jobs Overhaul 1.7.2** + Configurable Chances/Pay + First Person Messages + Experience-AJO (you take jobs from NPCs: deliveries, chores, shifts; pay tunable; Experience gets XP from jobs). Big: 3,355 records, overrides 21 cells, 6 worldspace records and 24 placed actors (city overhauls to check), one facegen NPC, 69 voice files, 867 player lines (67 unique - Eleonora recordings). Three menus (one SkyUI, two MCM Helper) - free under Bridge. Its page calls SPID a hard requirement but ships no SPID file. Pay sits in Requiem's economy. | **Yes, as its own step after the horse batch**: cell and worldspace headers forwarded, the 24 placed actors checked against the city overhauls, pay ranges set with the Configurable add-on to Requiem's scale, the 67 lines into the Eleonora topic files. |
| P15 | **Atmospheric Sheet Eradicator** - a Base Object Swapper file that sinks and disables the eight vanilla mist and slow-fog sheet objects (the flat fog planes in marshes and valleys). | **Your call - it is a visuals change.** Default: out, test as its own A/B when you want it. |
| P16 | **Cat Carry 2.0** - pick up and carry the house cats (Mihail's cats, installed); seven animal profiles; SKSE Menu Framework settings. Its hold-to-activate overlaps Immersive Interactions' pet-the-cats. | Yes; the activation key is settled in its menu so petting and carrying do not fight. |
| P17 | **Disease Widget** - an on-screen widget for diseases (vanilla + CC Survival list). | Yes; I check its disease list against Requiem's disease spells and add the missing ones to its file. |
| P18 | **FollowerParaglide 1.1** - followers paraglide with you. Needs Piggyback (in the folder) and the Paraglider; you run the ONE(Plus) build, which the DLL has not been proven against. | Your call. If yes: Piggyback + FollowerParaglide together, tested on a new game; if the glide never triggers with ONE(Plus), both come out. |
| P19 | **Pet Everything** + patches - pet any animal through an activation perk, no animation. Three of its four plugins are FULL (slots); the Pet the Dog patch has no master here. You already have animated petting for cats and horses. | **No.** If you want it anyway: the two usable patches get flagged light first, the Pet the Dog patch is skipped. |
| P20 | **The public Authoria list files** (Bodyslide outputs 3BA/HIMBO/UBE 2.9.10, Bodyslide Projects UBE, UBE Converter Output 1.9.10, UBE Master Patch 2.9.10, Seasons Patches 1.0.3, Mirelle bridge, mushroom and Windhelm fixes, 8 GB). Your instance runs its OWN converter outputs and body builds (different plugin names), your installed outputs read 2.1 / 2.5, and the three small fixes are already installed under Authoria names. | **Not installed by this plan.** Tell me what you downloaded them for: compare against your own lane, update your lane to 2.9.10, or ignore. Installing them blind would collide with your converter outputs. |
| P21 | **Requiem - Foods and Ingestibles Matter 1.0.1** (from the public list: 31 light plugins, FOMOD, 52 KID files, a Requiem food/drink overhaul you do not have). | Your call. If yes: its own step (Requiem consumable patching rules apply; 31 plugins placed by hand). |

### 10d. What this group adds to your follow-up steps
- Eleonora lines: Ride Along 2.0 (46), AJO (67 unique) if P14, Word Travels, Followers Ride Horses (2) - all into the one topic-file run after the installs.
- MCM menus: AJO 3, Word Travels 1 - no cost under MCM Bridge.
- Pandora: nothing new here (Ride Along's seats are OAR, no behaviour patch).
- Slots: none unless P19 (Pet Everything).

## 9. Order of work
1. You: P1-P5 are settled by what you downloaded on 10-14 (all in `C:\Users\User\Downloads`, I move them to the MO2 downloads folder at build time). Still open: P6 and P7-P12.
2. Me: convert the SC meshes; stage every mod folder from the archives (archive-vs-folder diff on each); flag the SC plugin light; build the Authoria patches (3.2, 3.4, 3.5, 3.6, 3.7); strip the three outputs (3.8); measure and refit the packsaddles.
3. Me, MO2 closed, backups first: the placement in both profiles + disabled lines in the other six (3.9); MCM Bridge above MCM Recorder with the Authoria recorder fix retired and the init script rebuilt without its MCM rebuild step (section 6); verification (3.10). The voice switch (section 4) is parked until your Eleonora pack for DBReV exists. The batch load-order write is shown to you before it runs, per the standing rule.
4. You, in this order: BodySlide (nothing for horses - only the batch's Pelts / Dwemer Research Squad sets), Pandora (only if P4 or the batch animations go in), Reqtificator, then Synthesis (corrected 10-17: the Synthesis outputs load after the Reqtificator output and read it).
5. You, in game: the five stables (named horses, saddle vendors), Shadowmere, Frost, a carriage ride (horses + harness), the Whiterun carriage line, Bruma horses, Kaidan's horse, Gore's horse, a CC wild horse, HAYF's Thogull with a packsaddle, Steel/Elven horse armour for clipping, a follower assigned a horse through Followers Ride Horses, a Ride Along passenger on an SC horse, a HAYF packsaddle on Thogull, a bought hold horse keeping its Equestrian saddle after a ride, and every init recording playing under MCM Bridge.
6. Me, after the batch: Eleonora topic files for every new player line (your pack-making input); first new-game Papyrus log read to confirm every recording played under MCM Bridge.
7. Me, between 3 and 4 if P14 / P17 / P18 / P21 are yes: those as their own steps (section 10c).
8. You, after ALL the file changes are in (this batch, section 10, and the items you take from your friend's GitHub, which still need their own picks from `FRIEND-CHANGES-PICKS-20261012.md`): the full LOD run you planned on 10-15. I prepare its inputs and check the outputs; the run is yours.
