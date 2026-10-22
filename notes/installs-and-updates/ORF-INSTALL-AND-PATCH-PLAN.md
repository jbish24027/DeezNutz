# Outfit Recognition Framework — install plan and patch plan

Written 2026-08-19. Profile audited: **DEEZ CS NUTZ**. MO2 was closed when the counts were taken.

---

## 1. What this mod does

NPCs comment out loud on what you are wearing. They also comment on what they are wearing.

It works by putting 33 marker keywords on clothing and armour. A keyword says a thing about the
item: it is red, it is a dress, it shows cleavage, it is scruffy, it is from another game. The
dialogue then reads those keywords and picks a line.

The mod ships nearly 2000 new voiced lines across 52 voice types. Mod-added NPCs who use a vanilla
voice get the lines for free.

The keywords are applied at game launch by Keyword Item Distributor. Nothing is written to your
save. Adding or removing any of this is clean.

---

## 2. What you downloaded

Seven archives. Here is what each one actually is.

1. **Outfit Recognition Framework 1.2** — the mod itself. Plugin, scripts, MCM, 78 MB of voice
   files, and the keyword file for vanilla clothing.
2. **Skypatcher for Vanilla Outfits 1.01** — an alternative to a file the main mod already ships.
   **Do not install this.** See section 4.
3. **Cosplay Pack ORF 1.0** — official patch for the Cosplay Pack.
4. **FIBBI patches 2.0.6** — 203 patch files covering 150+ armour mods.
5. **ORF more keywords 2.1.1** — 54 patch files, mostly Aokili, ELLE, Obi and SaltLemon outfits.
6. **MEG ORF 1.1** — one file covering about 20 miscellaneous armour mods.
7. **Ninirim ORF patch 1.1** — one file for the Ninirim Collection.

Your setup already has everything these need. Keyword Item Distributor is live and healthy. Its
last log loaded 153 keyword files and ran 630 separate armour rules without an error. Spell Perk
Item Distributor, SkyUI and MCM Helper are all installed and enabled.

The mod's plugin is light-flagged, so it costs you no full plugin slot. You have 17 free.

---

## 3. OUTCOME — the patches are built (2026-08-19)

The plan below was written before the work. It is superseded on one point: the
patch packs are no longer needed at all.

**Built:** a mod called `Authoria - ORF Patches`, holding 162 keyword files,
6,210 keyword assignments across 2,821 wearable records, covering every
armour-adding mod in the profile. It validates clean: no syntax errors, no
unknown keywords, no malformed references.

**Install just two things:** Outfit Recognition Framework 1.2, and
`Authoria - ORF Patches`. Skip all five patch packs and the Skypatcher file.
Of the packs' 264 files only 34 touch a mod present here, and 23 percent of
their colour lines sit on helmets, boots and capes, which muddies the outfit
reading. Everything they would have done is now done properly.

Colours were read off the textures this load order actually loads, so they
reflect your retextures rather than the mod authors' originals.

---

## 4. Install order

Install these as **seven separate mods** in Mod Organizer. No two archives contain a file with the
same name, so nothing overwrites anything.

Put the whole block under the **Gameplay - Line Expansions** separator, next to Brawl Lines
Expansion. That separator already holds this kind of mod.

Install in this order.

1. **Outfit Recognition Framework 1.2.** Installs clean, no choices. You can delete the `Source`
   folder afterwards if you like; it is script source, not needed to play.
2. **Cosplay Pack ORF.**
3. **MEG ORF.** The archive has a `Data` wrapper folder. Mod Organizer normally strips this by
   itself. Check the install window shows the keyword file at the top level before you click OK.
4. **Ninirim ORF patch.** **This one needs a manual fix.** The archive puts its keyword file inside
   a folder called `Ninirim - ORF`. Keyword Item Distributor only reads files sitting flat in the
   Data folder, so installed as-is this patch does nothing at all and gives you no error. In the
   install window, right-click the `Ninirim - ORF` folder and choose "Set as data directory".
5. **FIBBI patches.** 203 files, all at the top level, installs clean.
6. **ORF more keywords.** 54 files, all at the top level, installs clean.
7. **Skypatcher for Vanilla Outfits — skip it.** Reason in section 4.

Plugin order does not matter much. The plugin only adds dialogue and keywords; it overrides nothing.
Put it anywhere in your normal patch region. It must stay **above** your flat map and output blocks,
same as everything else.

Then enable the mod and launch once. Do not start a new game yet.

---

## 4. Why to skip the Skypatcher file

It is offered on the mod page as a teaching example, not as a required file.

I compared it line by line against the keyword file the main mod already ships. They are the same
work done two different ways. The main mod's file has 191 rules. The Skypatcher file has 176. Of
those, 175 are identical.

The main mod's file is the better one. It carries 16 rules the Skypatcher version lacks, including
every "this outfit is inappropriate here" rule for temples, the orphanage and cemeteries. The
Skypatcher file has exactly one rule the other lacks, for Steel Wolf Armor.

Installing both would just do the same job twice. If you want that one missing rule, add a single
line to your own patch file instead. Section 7 shows how.

---

## 5. What gets covered, and what does not

I counted every wearable chest piece in your load order and checked each one against the patches
you downloaded.

Vanilla, the DLCs and Creation Club come to 1,242 chest pieces across 41 plugins. Those are handled
by the file the main mod ships. No work needed.

Everything else is 233 mod plugins. Of those, 69 turned out to be creature hides, naked body
records, spell effects, horse gear or gore records. Keywords there would never be seen. That leaves
**164 mods that genuinely matter**, holding **2,253 wearable chest pieces**.

Against those 2,253 pieces the seven archives give you:

- **405 pieces covered exactly**, by name, from the patch packs.
- **193 more caught loosely**, by a name-fragment rule such as "anything called Leather Armor".
- **598 covered in total. 1,655 pieces with no keywords at all.**

So the downloads get you about a quarter of the way. The rest is the work below.

Forty of your mods come out fully covered with nothing left to do. Among them: both Armors of
the Velothi packs, Moon Monk's Robes, Elmlock and its colour variants, Cute Adventurer, all the
Obi outfits, all the Fuse00 armours, Gryphonknight, Asura's Guard, Girl's Travel Outfit, the three
SaltLemon outfits and the Sigrin Silver Fox armour.

Magecore is the standout. FIBBI covers 118 of its 120 pieces.

The full mod-by-mod table is at `_tools\orf\orf-coverage-report.csv`. It has one row per mod, what
the mod is called in game, how many wearable pieces it has, how many are already covered, and how
many still need work.

---

## 6. Two things to fix before you play

**First: two packs disagree with each other on 28 items.**

FIBBI and MEG both patch about 40 of the same armours. On 28 of them they hand out different colour
keywords. Keyword Item Distributor adds both, so the item ends up carrying both.

The worst case is Kaidan's Khajiit Robes. FIBBI calls the whole range "colourful". MEG calls each
one by its actual colour. So a green robe would be described as both green and colourful. One light
red robe would be called red by one pack and white by the other.

This is cosmetic, not a crash. An NPC will occasionally describe your outfit wrong. If it bothers
you, delete the eight or so Khajiit robe lines from the MEG file and keep FIBBI's, or the reverse.
The affected items are listed in the CSV.

**Second: the mod's "borrow other mods' keywords" file will do almost nothing here.**

The main mod ships a file that looks for tags from SexLab Aroused, Advanced Nudity Detection, Naked
Armor and similar, and converts them to its own. It is meant to give you free coverage.

You do not have those mods. Of the ten tags it looks for, only one exists in your load order:
Schlongs of Skyrim's "revealing" tag, which sits on the Cosplay Packs, Magecore and the H2135
pirate outfits. Everything else finds nothing.

Leave the file installed, it costs nothing. Just do not expect coverage from it.

---

## 7. How to write the missing patches

Every patch is a plain text file. No plugin, no Creation Kit, no xEdit.

### The rules

- The filename must contain `_KID` and end in `.ini`. Call them
  `ORF - <mod name>_ORF_KID.ini`.
- The file must sit flat in the Data folder, meaning the top level of a Mod Organizer mod folder.
  Not in a subfolder.
- No section headers. Comments start with a semicolon.
- One line per keyword. The form is:

```
Keyword = <keyword>|Armor|<editor id>,<editor id>,<editor id>
```

- To catch items by name fragment instead, prefix with a star: `|*Robes`.
- To catch every armour in one plugin: `|SomeMod.esp`.
- A wrong keyword name does not error. Keyword Item Distributor silently invents a new empty
  keyword instead. So spelling matters, and the log is the only place it shows.

### The 33 keywords

Colours: `ORF_Red` `ORF_Blue` `ORF_Green` `ORF_Black` `ORF_White` `ORF_Brown` `ORF_Grey`
`ORF_Gold` `ORF_Silver` `ORF_Yellow` `ORF_Pink` `ORF_Purple` `ORF_Colourful`

Shape and cut: `ORF_Dress` `ORF_Robes` `ORF_Hooded` `ORF_ShortSkirt` `ORF_Cleavage` `ORF_Tight`
`ORF_Revealing` `ORF_Transparent` `ORF_NearlyNaked` `ORF_Bra` `ORF_Underwear`

Character: `ORF_Classy` `ORF_Scruffy` `ORF_Flimsy` `ORF_Sturdy` `ORF_Intimidating` `ORF_Leather`

Situational: `ORF_FromOtherGame` `ORF_OutOfPlace` `ORF_Inappropriate`

There is a 34th, `ORF_Ignore`. That one goes on an NPC, not an item, through the separate file the
main mod ships. Add a name to it to shut that NPC up.

### Worked example

This is the real patch for the Elmlock armour, from the FIBBI pack. It is a good model because it
handles a set that ships in eleven colours.

```ini
Keyword = ORF_Hooded|Armor|ksmc_elmlock_armo_BW_hood1,ksmc_elmlock_armo_BB_hood1
Keyword = ORF_Blue|Armor|ksmc_elmlock_armo_body,ksmc_elmlock_armo_SB_body
Keyword = ORF_Green|Armor|ksmc_elmlock_armo_UT_body,ksmc_elmlock_armo_MG_body
Keyword = ORF_Black|Armor|ksmc_elmlock_armo_BB_body,ksmc_elmlock_armo_VB_body
Keyword = ORF_Leather|Armor|ksmc_elmlock_armo_body,ksmc_elmlock_armo_BW_body
```

One line per colour, listing every variant of that colour. Then one line for the material.

### Which slots to tag, and why it is not a free choice

I read the mod's own dialogue conditions. Of its 2,416 keyword checks, 2,374 use a function that
asks "is this person wearing **anything** carrying this tag". There is no chest slot in the logic.
Every worn piece is pooled together.

Two things follow.

**Tagging only chest pieces kills five keywords outright.** Hooded, short skirt, underwear, bra and
transparent nearly always live on a separate garment on another slot. Those five carry 306 dialogue
conditions between them, 13 percent of everything the mod checks. Tag chest only and no NPC ever
remarks on your hood, your hemline, your underwear showing, or see-through clothing.

**Tagging everything pollutes colour.** Because all worn pieces pool, a black boot and a red dress
make you register as both black and red. The mod's author avoided this: in his own vanilla file,
colour goes on cuirasses and full outfits only.

The patch packs you downloaded do not follow that rule. Of their 3,006 colour assignments, 691 sit
on helmets, boots, gloves and capes. That is 23 percent. The Imperial Guard Centurion helmet is the
clearest case: FIBBI gives one helmet silver, gold **and** red at the same time.

So the rule for this build is per keyword, not per slot:

- **Shape and coverage** — hooded, short skirt, underwear, bra, transparent, revealing, cleavage,
  nearly naked, dress, robes. Tag whichever piece actually is that thing, on whatever slot it uses.
- **Colour and character** — the 13 colours plus classy, scruffy, flimsy, sturdy, intimidating,
  leather. Outer garment only. Never boots, gloves, helmets, circlets or capes.

That reaches every line of dialogue the mod has, and keeps colour honest.

### The method, per mod

1. Ask houseCARL for every armour piece the mod defines, with its in-game name and which body slot
   it uses.
2. Keep the chest pieces. Add hoods, skirts and boots only if the mod has ones worth remarking on.
3. Read the names. Most colours are in the name already, as with Elmlock above.
4. For anything the name does not settle, look at the mod's Nexus images or the texture.
5. Write one line per keyword, grouping every item that shares it.
6. Save into a single mod folder called `Authoria - ORF Patches`.

Do not use item ID numbers unless you must. Use editor IDs, the way every pack you downloaded does.
Your existing keyword files already prove editor IDs resolve correctly in this setup.

One caution. Your Requiem rebuild renames editor IDs on some items. If a line refuses to apply,
check the current editor ID rather than the mod author's original, and fall back to the ID number
for that item. Your Dynamic Fur Morph files already do exactly this and are a good reference.

### Order of work

**Group A — 19 mods, 1,294 pieces.** These are the ones worth doing. Biggest first, showing what
is left after the downloaded packs have done their part:

Ninirim Collection (154), Cosplay Gala (120), Glenmoril (112), Beyond Skyrim Bruma (108), Modular
Mage (102), Saints and Seducers (97), Vigilant (83), Sera's Armor (81), Cosplay Casual (69),
Unslaad (58), Legacy of the Dragonborn (53), Requiem's own cuirasses (51), Val Serano (40), Hal's
Casual Outfit (35), Adventurer's Tunic (30), DAc0da (29), Twilight Princess (28), Sons of Skyrim
(23), Cosplay Pack remainder (21).

Three notes on this group.

The Ninirim patch you downloaded only reaches 41 of its 195 pieces. That mod alone is a quarter of
your outfit wardrobe. It deserves its own pass.

Requiem's 51 cuirasses are worth more than the number suggests. Those are what guards, bandits and
soldiers wear, so every NPC in the world is wearing one. Same for Sons of Skyrim's 23.

Bruma, Vigilant, Glenmoril and Saints and Seducers are big but repetitive. Their armour comes in
material families, so a handful of name-fragment rules will cover most of each. Budget less time
than the raw counts imply.

**Group B — 30 mods, 231 pieces.** Small outfit mods, five to nineteen pieces each. Towels, Apex
Khajiit, the Cosplay Casual addon, Gilded Doublet, Olenveld, M'rissi, Interesting NPCs, Astrid,
Einar Wardrobe, Requiem's unique enemy armour, the pirate tops, the Ferrymen outfits, Mage's Daily
Outfit, Kaidan, the Sons of Skyrim Requiem patch, the three Kozakowy town outfits, Nibenean,
Riften Expansion, Threads of the North, Girl's Travel recolors, Bruma assets, Wyrmstooth, Ashe,
Novice Witch, Roaming Girl's Attire, Heavy Legion and Corsican Raider. These go fast, roughly one
file each.

**Group C — 75 mods, 130 pieces.** One to four pieces each. Mostly NPC replacers and quest mods.
Low value. Do these last or not at all.

---

## 8. Checking it worked

1. Launch the game and get to the main menu, then quit.
2. Open `Documents\My Games\Skyrim Special Edition\SKSE\po3_KeywordItemDistributor.log`.
3. Near the top it lists every keyword file it found. Confirm yours are there. If a file is missing
   it is in a subfolder, or the filename is missing `_KID`.
4. Search the log for `ORF_`. Each keyword shows as `added to N/17483`. A zero means the rule
   matched nothing, usually a mistyped editor ID.
5. In game, open the MCM and set the relationship threshold. Default is 1. Higher means you hear
   friendly comments only from people who actually like you.
6. Stand in a market and listen. Then change into something revealing and listen again.

The mod page also offers a Greeting Patch, a set of rings carrying every keyword for testing, and
an all-in-one bundle of 24 official outfit patches. The rings are genuinely useful for checking
that dialogue fires before you write 19 patch files. Worth grabbing.

---

## 9. Risks

Low overall. This mod adds dialogue and keywords and touches nothing else.

- It adds roughly 1,800 dialogue responses. Anything that suppresses NPC greetings will suppress
  some of these. You do not run such a mod today.
- Safe to add mid-game. The author says removal mid-game is probably safe but will not promise it.
- Both Dragonborn Voice Over fix plugins are broken in a way houseCARL cannot read. That is
  pre-existing and unrelated, but it means those two plugins were excluded from this audit. Neither
  adds armour, so the counts here stand.
- The 78 MB of voice files are loose. That is fine. Pack them into an archive later if you care
  about file count.
