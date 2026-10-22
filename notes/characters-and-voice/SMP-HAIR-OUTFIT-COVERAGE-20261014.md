# SMP hair and outfit coverage - 2026-10-14

Profile scanned: DEEZ CS NUTZ - PICTA (the one MO2 runs). Every NPC record, every hair head part, every
baked face file and every default outfit was read. The per-NPC spreadsheet is
`SMP-HAIR-OUTFIT-COVERAGE-20261014.csv` next to this file (8,436 rows; named NPCs first, sorted by group).
The scripts live in `_tools\smp-coverage\` so the census can be rerun after changes.

## The one rule that decides everything

An NPC's hair only moves if the **baked face file** (the facegen mesh) carries the physics link.
It is not enough that the hair style's own mesh is an SMP mesh. The game draws a baked NPC from the
face file, not from the hair mesh, so the hair in the face file has to be the SMP hair.

That is why the numbers below look the way they do.

## Where it stands (named NPCs that have hair: 5,054)

| Group | Named NPCs | What it means |
|---|---|---|
| A. Hair physics works now | 161 | Face file has the link. Mostly True Sons / Men of Skyrim Refined males, Nimwraith quest NPCs, Inigo. |
| B. Remake style, old face bake | 2,697 | They wear a vanilla style that Vanilla Hair Remake SMP already replaced. The hair mesh moves, their face file was baked with the old static hair. Only the face file needs doing. |
| B2. Remake style, no face file | 293 | Head is built at runtime, so the live SMP mesh is used. These probably already move in game. |
| C. Static style, SMP twin installed | 119 | A KS / Modular / saLa SMP version of the same style is installed. Needs a head-part swap plus a new face bake. |
| D. Static style, no SMP twin | 1,784 | 801 are vanilla styles the Remake never made (the common short male cut, Redguard male cuts, the old-man cuts). 836 are replacer looks (NPC Merge, Bruma, 3DNPC, Vigilant, kids) whose hair is baked only. 99 KS, 37 HG Hairdos. |

Unnamed NPCs (guards, bandits, soldiers): 22 work, 2,614 are group B, 673 group D.

Followers and well-known faces: Lydia D (Soledad hair, no twin), Serana C (twin installed), Inigo A,
Auri D, Lucien B2, Remiel B, Jenassa B, Ysolda D, Carlotta D, Elisif D, Ulfric D, Tullius B, Rikke B,
Delphine B, Farkas and Vilkas B, Ralof and Hadvar B, Brynjolf D, Vex D, Karliah D, Mjoll D, Astrid D,
Cicero D, Tolfdir B, Brelyna B, J'zargo D, Valerica D, Frea D, Rumarin D, Danica D, Hulda D, Irileth C,
Maven D, Sapphire D, Jordis D, Argis C, Iona D, Rayya D, Calder B, Gregor B.

## What group B needs (the big win, 2,697 named + 2,614 unnamed)

Two kinds of face files are involved:

1. **Original bakes** - the face file still comes from the base game or the mod's own archive
   (Skyrim 444, Interesting NPCs 332, Bruma 207, Immersive Encounters 98, Legacy 70, Realistic
   Conquering 54, Grand Solitude 32, Olenveld 49, Apocalypse 29, Gray Cowl 27, Forgotten City 25,
   Mrissi 21, Remi 14, Creation Club ~57, and smaller ones). These NPCs keep their original head parts,
   so a **ready-made SMP face pack drops straight in**:
   - "Vanilla hair remake SMP - NPCs" (optional file on the Remake's own page) for the base game.
   - "Faithful Faces - Vanilla Hair Remake SMP - Consistency Patches" (Nexus 143247) for Interesting NPCs,
     Bruma, Legacy, Immersive World Encounters, Wyrmstooth, Forgotten City, Vigilant, Gray Cowl, Realistic
     Conquering, Olenveld, Carriage and Ferry Travel, Alternate Perspective, Inigo, Lucien and many more.
   - "Faithful Faces - Creation Club" (Nexus 114437) for the Creation Club NPCs.
   Roughly 1,400 named NPCs. Each pack must sit above the mod it patches, and I check every file against
   the winning record before it goes live, so no purple or dark faces.

2. **Overhaul bakes** - the face file comes from a look overhaul that kept the vanilla hairstyle
   (True Sons of Skyrim Refined 291, Men of Skyrim Refined 223, Wanderer's Fair 60, Vigilant overhaul 34,
   Bruma replacer 31, Children of the Pariah 27, Younglings 27, Legacy visual overhaul 24, 3DNPC Merge 24,
   Carriage overhaul 22, NPC Merge 22, Glenmoril 19, others). No ready pack exists. Options:
   - Re-bake those faces in the Creation Kit with the Remake meshes active, then run the Remake author's
     fix tool, SMP FaceGen (github.com/jgernandt/smp-facegen). The tool only repairs Creation Kit output;
     it cannot graft SMP hair into an old bake. The Creation Kit is not installed in this instance.
     Keeps the chosen looks exactly.
   - Or give them an SMP **wig** of the same style by SPID (the Remake has an optional wig file; Hair Colour
     Sync is already installed and matches the colour). No face work, switchable off any time, but the wig
     is an item in their inventory and clashes with helmets on the hair slot.
   Roughly 900 named NPCs.

## What groups C and D need

- C (119): head-part swap to the installed SMP twin plus a fresh bake. Needs the Creation Kit, or the
  wig route for the styles that have wigs (KS SMP wigs are not installed; KS SMP 1.5.0 ships them).
- D vanilla (801): no SMP mesh exists for these cuts in any installed pack. The Remake does not make them.
  A different style would have to be chosen for them, which changes their look.
- D replacer looks (836): the hair is baked only (the replacer ships no hair mesh), and the styles are
  mostly male KS cuts, which no SMP pack covers. Changing them means changing the look.
- D KS / HG (136): the KS female styles not in KS SMP, and HG Hairdos (no SMP version exists).

## Must-have before any NPC gets SMP head-part hair

- **SMP-NPC crash fix** (Nexus 91616, by the Remake author) is NOT installed. The Remake page requires it
  for its NPC files, and FSMP builds since 1.50.4 can crash on NPCs with SMP hair without it. It is a
  one-DLL SKSE plugin, works on 1.6.1170 with Address Library.

## Outfits (named NPCs with a default outfit: 4,488)

| State | Named NPCs |
|---|---|
| Outfit has at least one cloth-physics piece | 1,171 |
| Outfit is all static | 3,317 |

What is static, and why:

- **Male vanilla clothes** (farm clothes, merchant, miner, fine clothes, warlock and necromancer robes,
  roughspun, Redguard clothes, Bruma common clothes): about 2,000 of the 3,317. The copies that win come
  from the HIMBO Vanilla Armors prebuilt set and Common Clothing. **No SMP version of these exists in the
  instance, and I found none on Nexus.** Nothing to do here short of someone making one.
- **Vanilla armours** (Imperial light/heavy/studded, Stormcloak sets, hold guard, iron, steel plate, elven,
  glass, ebony, daedric, Dawnguard, Nightingale, vampire): several hundred NPCs. Static copies win from
  `Authoria - PG Output - PBR` and the HIMBO prebuilt, **but SMP BodySlide projects for all of them are
  installed and unbuilt** ("HDT-SMP Vanilla V2 HIMBO" and "HDT-SMP Vanilla V2 3BA"). Building those in
  BodySlide and then re-running PG Patcher would put physics on every guard and soldier.
- **Female vanilla clothes** from the 3BA output already carry cloth physics (farm dresses, hide, fur,
  leather, bandit). The few static female pieces (tavern clothes, Common Clothing dress) have no SMP project.

## Picks for you (see the chat message)

1. Group B original bakes: install the ready-made face packs (my recommendation to start).
2. Group B overhaul bakes: wigs by SPID now, or wait for a Creation Kit re-bake.
3. Armours: build the two SMP vanilla armour projects in BodySlide, then PG Patcher.
