# Rite of Arcana - Install Plan (Authoria, CS profile "DEEZ CS NUTZ")

Date: 2026-08-19
Mod: Rite of Arcana 4.5.7 (Nexus 168649, Thingamajig)
Requirement: Don't Eat Spell Tomes (API) 1.2.2 (Nexus 43095, Parapets)
Archives on disk: C:\Users\User\Downloads\ (both 7z files, downloaded 2026-08-19)
Extracted and inspected in the session scratchpad.

STATUS 2026-08-19: APPLIED (MO2 was closed). See section 0.

## 0. What was applied

- New mod "Don't Eat Spell Tomes (API)": DLL + 7 pex, no ESP. Left pane: next to Scrambled Bugs
  (SKSE fixes block). meta.ini points at Nexus 43095 / file 320336 for update checks.
- New mod "Rite of Arcana": esp + 16 pex (the archive holds 16, not 18). Left pane: the slot
  Immersive Spell Learning - DESTified held. meta.ini points at Nexus 168649 / file 782480.
- Disabled (not deleted): "Immersive Spell Learning - DESTified", "I Just Want to Sit Down and
  Read" (its animation only fires from the ISL study script, so it is inert without ISL).
- Plugin swap: Rite of Arcana.esp took DEST_ISL.esp's line in plugins.txt (line 434, between
  SkyrimOutfitEquipmentSystemNG.esp and SkySigns.esp), loadorder.txt (line 491) and
  plugingroups.txt (line 1403, group "Gameplay - Early Loaders").
- Backups: profiles\DEEZ CS NUTZ\{modlist,plugins,loadorder,plugingroups}.txt.bak-roa-20260819.
  Diffs against them show only the intended lines. Line endings and BOM state preserved.
- Verified through houseCARL after the write: Rite of Arcana.esp ACTIVE and resolving; ISL mod
  DISABLED and DEST_ISL.esp gone from the order; the DLL and every DEST/ROA script has exactly
  one enabled source; the music-trigger activator now carries the ROA script; Dragonsreach,
  Blue Palace and Tamriel winners unchanged. Enabled mod count and checked plugin count are
  identical to before (net zero).
- Cleanup DONE 2026-08-19 (houseCARL in-place, no xEdit needed): 8 stray fog/mist/static ref
  overrides removed from the ESP (193 -> 185 records). Two of the planned ten turned out to be
  Arcane Confluence music-trigger hooks (106D1C/106D1B carry ROA_AddMusicTriggerSCRIPT) and were
  KEPT. Update.esm dropped from the masters (the first removed ref held its only link). Backup:
  Rite of Arcana.esp.bak-fogcleanup-20260819 in the mod folder. Verified after: error sweep
  clean (0 dangling, 0 missing masters), all 8 refs reverted to their pre-RoA winners (Lux x2,
  Lux Master x1, vanilla x5), all 4 script-carrier refs + 3 activators + spells + quest intact.
- Difficulty eased 2026-08-19 at the user's request: ROA_cost_mult default set 1.0 -> 0.85 in
  the ESP (in place, verified). This is the mod's own MCM dial ("Learning cost multiplier"):
  ~15% gentler drain model, and per the author's changelog it proportionally lowers ritual XP
  payout. Adjustable in game via MCM any time; the quest script re-reads it on every load.
  The MCM's "Learning cost exponent" slider has no backing global in the ESP - record-level
  tuning happens through cost_mult only. Ritual times (15-40s), Anchor duration (3-6s),
  randomness and penalty toggle left at author defaults.
- Friend export built 2026-08-20: _export-for-friend-roa\ (both tuned mod folders + INSTALL-GUIDE.md, zipped as Authoria-RiteOfArcana-Export.zip, 28 files). ESP in the bundle md5-matches the live tuned one; the .bak was excluded.
- Not done: any save-side step (your call).

---

## 1. Verdict

Install it. No Requiem patch is needed. No Reqtificator re-run is needed.
The whole job is: two mods in, one mod out, one plugin slot swap, and a save decision.

Why no patch: every record in the plugin is runtime plumbing for the ritual.
None of it is a learnable school spell, an NPC, a leveled list, armour, a weapon or a race.
The author already flagged every spell the way Requiem needs (see section 5).

---

## 2. What changes in play

Requiem 6.0.2 in this build has NO spell-tome gate of its own.
I checked: the tome records carry no script, the spells carry no perk condition, and Requiem
has no tome quest or tome perk. Reading a tome today teaches the spell instantly.

Your "Requiem - Improved Spell Learning" mod hands you TOMES (a gift menu) when you take a
magic perk. Those tomes are read like any other.

So with Rite of Arcana:
- Every tome, bought, found, or perk-granted, must survive the ritual before you get the spell.
- Requiem's higher spell costs and smaller magicka pools mean more tomes will read as
  "Impossible" early on. That is the mod working as designed. The cost multiplier in its MCM
  is the lever if it feels too harsh.
- Failure penalties cut magicka regen 40% for 11 minutes and stack. Requiem regen is already
  slow. There is an MCM toggle for the penalty.
- Backlash cloaks and bolts hit bystanders. Requiem NPCs will treat that as assault. Do rites
  alone, which is also the mod's own advice.

---

## 3. Install steps (MO2 closed for every file write)

### 3a. Mod: "Don't Eat Spell Tomes (API)" 1.2.2
From the 7z install ONLY:
- SkyrimSE\SKSE\Plugins\DontEatSpellTomes.dll  (the 1.2.2 build; it is the same DLL your
  current ISL mod bundles, and your SKSE log shows it loading correctly on 1.6.1170)
- Scripts\*.pex (7 files: DEST, DEST_ActiveMagicEffectExt, DEST_AliasExt, DEST_FormExt,
  DEST_PlayerSpellLearningScript, DEST_ReferenceAliasExt, DEST_UIExt)
Do NOT install DontEatSpellTomes.esp. Rite of Arcana says it is not required. It would cost a
plugin slot for nothing.
Skip the SkyrimVR folder and the pdb.

Left-pane position: anywhere in your SKSE-plugin block. No asset conflicts once ISL is off.

### 3b. Mod: "Rite of Arcana" 4.5.7
Install: Rite of Arcana.esp + scripts\ (18 pex). Skip the README and png.
Left-pane position: where "Immersive Spell Learning - DESTified" sits now (modlist line ~1185).
No asset conflicts: all script names are ROA_*.

### 3c. Remove the old spell-learning mod
- Disable "Immersive Spell Learning - DESTified" (mod and DEST_ISL.esp). Both it and Rite of
  Arcana listen for the same tome-read event. If both are on, every tome fires BOTH systems.
- "I Just Want to Sit Down and Read" is, in this install, only the ISL patch script plus a
  sit-and-read animation. Its tome script goes inert once DEST_ISL.esp is gone. Keep or
  disable, your call. Nothing in it touches Rite of Arcana.

### 3d. Plugin order
Put Rite of Arcana.esp in DEST_ISL.esp's exact slot:
  after  SkyrimOutfitEquipmentSystemNG.esp
  before SkySigns.esp
  group  "Gameplay - Early Loaders"  (plugingroups.txt line 1403: replace DEST_ISL.esp with
  Rite of Arcana.esp, or MO2 shows a duplicate group header)

Why this slot is safe (verified against the live load order):
- The plugin overrides 30 vanilla cells and 6 worldspaces as carriers for its teleport markers.
  Those overrides are identical-to-vanilla. Every one of those cells and worldspaces has its
  real winner far below this slot (Lux, Occlusion, DynDOLOD, Synthesis Worldspace, FWMF, your
  Authoria patches). An early slot means Rite of Arcana changes none of them.
- The 3 activator overrides it needs (music trigger, Eye of Magnus orb, Eye barrier) are
  uncontested. Its Arcane Confluence feature works.
- It also carried 8 accidental nudges to fog/mist/static refs. REMOVED 2026-08-19 (section 6).
- It must NOT go below Lux or any output/FWMF plugin. That would revert interior lighting in
  Dragonsreach, Blue Palace, Temple of Kynareth, both Halls of the Dead, Septimus' outpost,
  Tower of Mzark, Alftand and more.

### 3e. Plugin slot
Full slot. The ESP is not ESL-flagged and its FormIDs are outside ESL range.
Live count: 226 checked full + 12 implicit full = 238 of 254. About 16 free.
ESL compaction IS possible (no hard-coded FormIDs in any script), but this is a third-party
mod that updates often, so every update would need re-compacting. Recommend: full slot.

### 3f. Save
Best: new game. Your current character started today (Prisoner start), so that is cheap.
If continuing: disable ISL, load, save, quit, then enable Rite of Arcana. ISL has no uninstall
routine but states it is safe to remove.
For future Rite of Arcana updates use its clean-save procedure (console:
SetStage ROA_ArcanaMainQuest 200, save, remove, load, save, reinstall).

### 3g. MCM slots
Net zero. ISL's MCM leaves, Rite of Arcana's arrives. You stay at the same count under the
128 ceiling.

### 3h. In-game checks
1. MCM "Rite of Arcana" registers.
2. Read any tome: a preview message appears instead of instant learning, and Arcane Anchor is
   in your hands.
3. Cast Anchor, watch the drain, let one ritual finish (success or fail).
4. Walk into a music-sting location (for example Throat of the World path) and confirm the
   Arcane Confluence buff can appear.
5. Papyrus log: no ROA errors on tome read or on load.

---

## 4. Record enumeration (193 records, 20 types)

| Type | Count | What it is | Disposition |
|---|---|---|---|
| Spell | 19 | ritual, anchor, penalty, backlash, confluence, VFX carriers | new content, magic lane, no patch |
| MagicEffect | 30 | effects for the above | new content, magic lane, no patch |
| PlacedObject | 34->26 | 22 new teleport/VFX markers, 4 scripted vanilla refs (music triggers); 8 stray nudges removed 2026-08-19 | new + brushed |
| Cell | 31 | 1 new holding cell, 30 vanilla carriers (identical-to-vanilla) | brushed, harmless at early slot |
| Worldspace | 6 | vanilla carriers | brushed, harmless at early slot |
| Message | 19 | ritual/difficulty text | new content |
| GlobalFloat/Short/Int | 26 | MCM settings + runtime state | new content |
| FormList | 9 | failure pools, message pools, teleport list | new content |
| Activator | 4 | 1 new anchor, 3 vanilla with script added | new + brushed (uncontested) |
| Keyword | 4 | 2 new, 2 vanilla (alchemy restore health/magicka, identical) | new + brushed (uncontested) |
| Perk | 2 | activation blocker, ghost sneak (runtime only) | new content, perk lane, leave |
| Quest | 2 | main brain quest, MCM quest | new content |
| ArtObject 2, EffectShader 1, Explosion 1, ImageSpaceAdapter 1, Projectile 1, Static 1 | 7 | VFX | new content |

Reconciliation: 193 enumerated = 193 dispositioned (routed/skipped with reason). Zero unowned.
After cleanup the shipped plugin holds 185 records.

---

## 5. Requiem lane findings (requiem-patching + requiem-magic-patching)

Freshness probe: houseCARL on instance C:\1. AUTHORIA, profile DEEZ CS NUTZ, Requiem.esp
active, Magic Redone in the Flames chain. OK.

Magic lane: the five core spells I read in full (ritual drain, Arcane Anchor, penalty,
ghost-void, Arcane Confluence) are self-target, BaseCost 0, ManualCostCalc ticked, HalfCostPerk
null, IgnoreResistance + NoAbsorbOrReflect. The other 14 are backlash/VFX carriers and vanilla
copies; none is tome-taught and none sits on a school tier.
Requiem magic resistance and absorption cannot touch them. No comparable exists and none is
wanted. Disposition: skip, runtime plumbing.

Watch items (no patch, just know them):
- Arcane Anchor's two effects carry a school (Destruction / Restoration) with a 0.5 skill-use
  multiplier at magnitude 1. Each cast gives a sliver of skill XP. Negligible.
- The four "DUPLICATE" spells (shock bolt, fire/frost/shock cloak) are vanilla-value copies
  used only as backlash. They are not learnable and no NPC casts them. Leave.
- Penalty: -40% magicka regen, 660 s, stacking. Harsher under Requiem regen. MCM toggle.
- Failure pools I read (generic, destruction) hold only "nothing" and "hysterics". The severe
  outcomes (death, launch, levitate, ghost-void teleport) are chosen by the script for the
  worst failures, not drawn from those lists.
- Ghost-void calm effect is magnitude 255, area 512: covers Requiem's fixed-level enemies.

Reqtificator: nothing for it to process (no NPC, LVLI, ARMO, WEAP, RACE). No re-run needed.
REQ_NULL: the plugin references no Requiem forms. None possible.
Perk lane: 2 runtime perks, player-only via script, not in any tree. Leave.
Gap mechanics: none implied.

---

## 6. Stray-ref cleanup - DONE 2026-08-19

Done with houseCARL in-place removal (MO2 closed), not xEdit. ESP backup first:
mods\Rite of Arcana\Rite of Arcana.esp.bak-fogcleanup-20260819 (md5-verified copy).

REMOVED (8) - each confirmed script-free in RoA's version before removal:
  Skyrim.esm:    108B86 (mist)  0FA03F (fog beam)  100843 (dust beam)  0925A7 (fog)
                 0EAF20 (Sovngarde rock terrace)  0D8FB8 (smoke wisps)
  Dawnguard.esm: 015075 (kit room)  004D5F (mist)

KEPT - the plan's original list of 10 was wrong by two:
  106D1C and 106D1B (FXcameraAttachEffectsACT near High Hrothgar) carry
  ROA_AddMusicTriggerSCRIPT in RoA's version. They are Arcane Confluence hooks, same as
  0F25DC (Throat of the World trigger) and 0C28ED (MQ105 trigger). All four stay.

Result: 185 records, masters now Skyrim.esm + Dawnguard.esm + Dragonborn.esm (Update.esm
pruned - its only link was in a removed ref). Error sweep clean. All 8 refs revert to their
pre-RoA winners. Cell/Worldspace carriers untouched.

NOTE for updates: a Nexus update re-ships the uncleaned ESP. Re-do this cleanup (or accept the
8 strays - they are cosmetic) after any Rite of Arcana update.

---

## 7. Tunables (MCM-backed globals)

ROA_cost_mult, ROA_GrantedXP_Mult, ROA_RitualMinTime, ROA_RitualMaxTime,
ROA_AssistSpellDur_Min/Max, ROA_DisableRandomness, ROA_PenaltySpell_toggle,
ROA_force_3rd_person_toggle, ROA_ArcaneConfluence_ProbMult, ROA_LearningSpellVFXForceOn.

---

## 8. Facts verified this session

- DontEatSpellTomes.dll 1.2.2 is what ISL-DESTified already ships; skse64.log: "loaded correctly".
- Only two mods in the whole mods folder register for the tome-read event: ISL-DESTified and its
  "I Just Want to Sit Down and Read" patch script.
- DEST_ISL.esp current slot: after SkyrimOutfitEquipmentSystemNG.esp, before SkySigns.esp.
- 30 cell winners (all below slot): Lux.esp, Lux - USSEP patch, Lux - Water for ENB patch,
  Helios_Lux_ JK's Dragonsreach, Authoria - Master Patch - Lux, Authoria - Patch - Requiem -
  USSEP, Authoria - Patch - Requiem - Lock Chests Have Keys, Authoria - Reqtificated - Xelzaz,
  Authoria - Output - Synthesis Worldspace, DynDOLOD.esp, Occlusion.esp, DLC1MapMarkerEnabler,
  HLIORemi, Kaidan - Survival, BB02YoanaFollower, Dawnguard.esm (uncontested).
- 6 worldspace winners: FWMF for Fantasy Paper Maps, Water for ENB - Patch - FWMF, Soul Cairn
  Paper Map for FWMF, Authoria - Master Patch - FWMF.
