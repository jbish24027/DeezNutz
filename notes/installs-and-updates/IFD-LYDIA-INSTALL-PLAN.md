# Improved Follower Dialogue - Lydia (IFD) — install plan

Written 2026-08-21. EXECUTED the same day in the CS profile ("DEEZ CS NUTZ") after the decisions below were answered — see "Status" at the end of this file for what landed and what is still yours to do.
Archives: `Downloads\Improved Follower Dialogue - Lydia-38473-4-2-2.zip` and `Downloads\UBE Lydia Replacer - IFD Patch-127221-1-0.7z`.

---

## 1. The one thing that matters

IFD gives Lydia a new voice actress and 1,100+ lines.
To do that it moves Lydia from the shared "FemaleEvenToned" voice to her own voice type, "FemaleUniqueLydia".

Every compatibility problem below comes from that one change:

- Any other mod that recorded Lydia lines stored them under the old voice folder. After IFD, the game looks in the new folder and finds nothing. The line shows a subtitle and plays silence.
- Any mod that overrides Lydia's NPC record after IFD puts the old voice back, and then IFD's own lines go silent.

So the job has three parts:
1. Install IFD and make sure the new voice survives our Lydia record chain.
2. Re-key every other mod's Lydia lines into the new voice folder.
3. Generate the player's side (Eleonora DBVO) for IFD's 394 new prompts.

---

## 2. What I checked (facts, not guesses)

**The mod itself**
- One full plugin (cannot be light: 5,707 records, 1 new worldspace — a bandit fortress canyon — plus empty overrides of Tamriel and the Dragonsreach porch, 18 NPCs, 7 voice types). Two BSAs (72 MB voice/scripts/meshes, 47 MB textures). Ships its own SEQ file. Has an MCM (moral objection toggles).
- Three content patches, all already ESL-flagged: Bruma, Wyrmstooth, Legacy of the Dragonborn. We run all three mods, so all three patches go in.
- Two "disable Amorous Adventures" patches. Ours is the OStim Standalone AA, same plugin filename, so the plain AA disabler applies in principle (see section 5 for why we will not use the shipped file as-is).
- Appearance patches: none apply (we use the UBE replacer).
- IFD re-records Lydia's vanilla lines itself (including 31 Solstheim lines) and adds "not Lydia" to 16 vanilla lines so the old ones never fire for her.

**Lydia's record in our build**
- Nine plugins touch her. The winner is our "Authoria - Patch - Lydia UBE Weight" patch (after Requiem for the Indifferent).
- Compared field by field, IFD's Lydia record is vanilla Lydia plus the new voice. Nothing else in it is worth keeping: we already carry USSEP's sandbox fix, Requiem's outfit/perks/stats, and the UBE face and body.
- Conclusion: the only IFD change that must reach the game is the voice type.

**The Nexus "UBE Lydia Replacer - IFD Patch"**
- It is just the replacer's plugin with IFD added as a master and the voice set. In our chain it sits at position 4 of 9 and would be overridden by five later plugins. It can never reach the game. Do not install it.

**Other mods with Lydia lines (scanned file by file, condition by condition)**
| Mod | Lydia-specific lines | Where the files are | Action |
|---|---|---|---|
| Kaidan IF | 217 lines (334 files incl. variants) — Kaidan's Lydia banter quest, Erik travel quest, wedding, jail, dungeon, comments | loose files | copy into the new voice folder |
| Inigo | 79 lines (Inigo's NPC chat with Lydia) | inside Inigo.bsa | extract + copy |
| Lucien | 3 lines (Lucien–Lydia banter) | inside Lucien.bsa | extract + copy |
| Amorous Adventures (OStim) | 98 lines (her romance quest) | loose | disable her AA romance (decision D3) |
| FDE Lydia | all 300 (AI voice of the old actress) | loose | remove — its own author says it is incompatible with IFD |
| Serana Dialogue Add-On | none for Lydia (its FemaleEvenToned lines are other NPCs) | — | nothing |
| Kaidan 2 base, Auri–Kaidan banter | none | — | nothing |

None of the Kaidan IF lines are gated on voice type; they are gated on "is Lydia". So copying the audio files is the whole fix. No plugin edit is needed for Kaidan.
The copied lines keep the vanilla actress's voice. IFD's own lines are the new actress. That mismatch is the trade-off; the alternative is silence. The IFD author explicitly forbids AI-cloning her voice, so I am not proposing that.

**World edits IFD makes to vanilla records**
- 18 cells. Two interiors (Dragonsreach Dungeon, Frostfruit Inn) where IFD only adds things; Lux and Snazzy keep winning the lighting as long as IFD loads early. 16 exterior cells near Halted Stream Camp, Loreius Farm, Bilegulch Mine and Glenmoril Coven where only the Occlusion/DynDOLOD outputs win, as they should.
- 24 navmeshes. 23 are touched by nothing else. One is shared with Interesting NPCs and reads identical.
- 5 terrain (landscape) records. Our Synthesis worldspace output currently wins them, so after install that patcher has to be re-run or IFD's ground edits are lost (floating or buried objects).
- 1 placed NPC at the Ritual Stone necromancer camp that IFD makes persistent and location-bound. Our Reqtificated Ryn's Standing Stones patch wins it today, so the change has to be forwarded.
- Navmesh info map: the winning copy is our Val Serano/Ryn's navmesh patch. IFD's 78 new navmeshes need their entries merged into it, same procedure as the earlier navmesh patches.
- 2 worldspace records (Tamriel, Dragonsreach porch): effectively empty overrides; the flat-map patches keep winning.
- 2 of the 16 vanilla dialogue lines IFD overrides currently carry USSEP fixes (line ordering, response text). IFD's copy drops them. Forward both.

**Capacity**
- Full plugin slots, MO2 closed, counted from disk: CS profile 233 of 254, NUTTZZZ 223, the two legacy profiles 189 and 199. IFD costs one. Fine.
- MCM menus: about 126 of 128 before this (per the 08-19 census). IFD adds one. Still under the cap, but this is the last comfortable addition.
- FDE Lydia is light and nothing depends on it. Removing it frees nothing and breaks nothing.
- SkyPatcher is 6.4.2. The voice-type crash bug was 2.4.9–2.4.14. We are clear.

**DBVO / Eleonora**
- The pack is keyed by the prompt TEXT, not by plugin. I matched IFD's 443 player prompts against all 41,298 files.
- 49 already exist (generic lines such as "Follow me.", "Wait here.", "I need to trade some things with you.").
- 394 are missing: 358 in the core plugin, 25 in the Bruma patch, 11 in the Wyrmstooth patch, 0 in the LotD patch.
- The filename rule was verified against Kaidan IF, which the pack covers: 2,802 of 2,876 prompts matched; the 74 misses are stage directions like "(Remain silent)" that were deliberately not voiced.
- Manifest: `IFD-LYDIA-DBVO-ELEONORA-MANIFEST.txt` (filename TAB text) and `.csv` (plugin, topic, filename, text), next to this file.
- 12 prompts contain curly apostrophes; the pack already stores those characters in filenames as-is, so keep them. 12 contain double quotes; those become underscores in the filename (the rule handles it). One pair of prompts collapses to the same filename; one recording will serve both. No semicolons, so no "DBVO Fix" plugin is needed.

---

## 3. Decisions for you

ANSWERED 2026-08-21: D1 CS profile only · D2 SkyPatcher · D3 no AA Lydia · D4 re-key · D5 you generate the missing Eleonora lines (separate folder created for them) · D6 standing rule: major changes happen before a playthrough, never weigh the current save · D7 grass cache for the new worldspace (driver prepared, you run the five passes).

- **D1 — Profiles.** FDE Lydia and Kaidan IF are enabled in all 4 profiles. Default: IFD + the Kaidan/Inigo/Lucien voice patch + the Authoria patch go into all 4. Eleonora lines follow the pack (enabled in CS + NUTTZZZ, listed disabled in the two legacy profiles).
- **D2 — Voice mechanism.** Default: one SkyPatcher line in an Authoria ini (sets Lydia's voice to FemaleUniqueLydia at runtime). It survives Reqtificator re-runs, NPC merges and any future replacer swap. Alternative: edit the voice into the final Lydia patch record (visible in houseCARL/xEdit, but must be redone if that patch is ever regenerated or deleted). I recommend SkyPatcher.
- **D3 — Amorous Adventures Lydia.** IFD has its own romance. Default: disable AA's Lydia romance. Alternative: keep it and re-key its 98 lines too (they would play in the old actress's voice during AA scenes).
- **D4 — Kaidan/Inigo/Lucien lines in the old voice.** Default: re-key them (they play, old voice). Alternative: leave them silent. I recommend re-keying.
- **D5 — Where the new Eleonora files live.** Default: a separate mod folder "Authoria - Eleonora - IFD Lydia" above the pack, so pack updates never wipe them and you can upload them upstream later. Alternative: drop them into the pack folder.
- **D6 — Save.** The IFD author recommends a new game for 4.x (install mid-save works but replays a backlog of main-quest conversations). Removing FDE Lydia mid-save leaves its quests orphaned in the save. Tell me which save this is going into.
- **D7 — Polish for the 3 new worldspaces.** They ship their own terrain LOD but have no object LOD and no grass cache. Default: leave as is. Optional: partial grass-cache run for the new worldspaces using the existing regen method.

---

## 4. Execution steps (in order)

Backups first, every time: the 4 profile files (modlist, plugins, loadorder, plugingroups) × 4 profiles, plus any plugin I edit. MO2 must be closed for every write.

**Step 1 — Remove FDE Lydia.** Untick the mod and plugin in all 4 profiles. Keep the folder disabled for now (delete later with the other cleanup).

**Step 2 — Install IFD** as mod "Improved Follower Dialogue - Lydia": core files + Bruma + Wyrmstooth + LotD patches. No appearance patch. Not the shipped AA disabler (see step 6). Mod goes where FDE Lydia sat (the Follower Dialogue Expansion block). Plugin order: main plugin in FDE Lydia's old slot, the three patches directly after it. Update plugingroups in all 4 profiles.

**Step 3 — Voice fix (D2).** New mod "Authoria - Patch - IFD Lydia" containing a SkyPatcher NPC ini with one line: Lydia → voice FemaleUniqueLydia. No plugin needed for this part.

**Step 4 — Re-key the other mods' Lydia lines (D4)** into the same mod folder:
- Kaidan IF: copy all 334 files from its FemaleEvenToned folder into a FemaleUniqueLydia folder under the same plugin name (the 110 non-Lydia files in there are inert under her voice type; copying everything guarantees nothing is missed).
- Inigo: extract the 79 Lydia lines (and their lip files) from Inigo.bsa, place under Inigo's plugin folder / FemaleUniqueLydia.
- Lucien: same for the 3 lines from Lucien.bsa.
- BSArch exists on D: (the CLAUDE xedit folder); point houseCARL at it, or use the Python lz4 route.

**Step 5 — Authoria - Patch - IFD Lydia.esp (ESL)** in the same mod folder, loading in the late custom-patch group after the Reqtificated Ryn's Standing Stones patch and after the AA OStim patches:
- Forward USSEP's fields onto IFD's two overridden vanilla lines (keep IFD's "not Lydia" condition).
- Forward IFD's persistent flag + location on the Ritual Stone placed NPC on top of the Reqtificated Ryn's version.
- (D3) Disable AA's Lydia romance the way IFD's disabler does it — an always-false dialogue condition on her two AA quests — but applied on top of the current OStim winner. Do NOT load IFD's shipped disabler plugin: it was built against a different AA version and would revert the OStim script properties on those quests.

**Step 6 — Requiem pass** → "Authoria - Reqtificated - IFD Lydia.esp" (ESL), with the other Reqtificated patches. Load the requiem-patching skill at execution. New records to handle: 1 weapon (Jori the Resolute's two-handed axe, draugr material, with a custom enchantment), 1 enchantment + 3 effects, 2 Lydia self-buff spells + 1 perk, 8 named NPCs (Kolgar, Eselda, Fenrar, Eorald, Vonjar, Falcius, Maximus, Jori), an assassin, generic Imperial/Stormcloak soldiers, and a leveled bandit that already templates Requiem's bandit list. Two books and a debug apple need nothing. Then you re-run the Reqtificator.

**Step 7 — Navmesh info map.** Merge IFD's entries into the winning Authoria navmesh patch (same method as Val Serano/Ryn's).

**Step 8 — Your tool runs.** Re-run the Synthesis worldspace patcher (terrain). Re-run the Reqtificator (new NPCs). DynDOLOD stays as is (a re-run would wipe the winter-grass fix; IFD's worldspaces simply get no object LOD). Optional D7 grass cache.

**Step 9 — Eleonora lines (D5).** Generate the 394 lines from the manifest with the ElevenLabs Eleonora voice, convert to fuz exactly as the pack does, name per the manifest, place under Sound\DBVO\elnordvoice\ in the chosen folder. Spoken text = the line without any leading "(Persuade)"-style tag.

**Step 10 — In-game checks** (new game or the agreed save):
1. Talk to Lydia in Dragonsreach: her first IFD conversation plays with audio.
2. "Follow me" / "Wait here" / trade all have audio (these moved into IFD's own quest).
3. Her face is still the UBE face (no grey face; the replacer's loose facegen beats IFD's BSA, so it should be).
4. Travel with Kaidan + Lydia until a Kaidan–Lydia banter fires: Lydia's reply has audio (old voice).
5. Inigo + Lydia chat: audio.
6. Choose any IFD prompt with DBVO on: Eleonora speaks it.
7. MCM list shows "Lydia" config and nothing else dropped off the bottom.
8. No Amorous Adventures prompt on Lydia (if D3 default).
9. Long IFD prompts read fully in the Vel'dun dialogue menu (IFD recommends Dialogue Interface ReShaped, which we do not run; check for truncation).

---

## 5. Risks and known limits

- Voice mismatch on re-keyed lines (old actress) — accepted trade-off, see D4.
- Generic voice-keyed NPC-reaction mods (NPCs React To…, Brawl Lines, Sleeping Expanded, Stress and Fear, Skyrim's Got Talent, etc.) will no longer have lines for Lydia; every custom-voiced follower has this limit. Not patching.
- MCM is at the ceiling after this; the next MCM-bearing mod needs a cut first.
- The shipped AA disabler must not be used directly (script-property regression) — Authoria equivalent instead.
- Kaidan IF's Lydia banter was written for vanilla Lydia's personality; IFD rewrites her character. Tone clashes are possible and not fixable.
- If the Reqtificator or the NPC merge is regenerated later, the SkyPatcher voice line keeps working; a record-level voice edit would not.
- IFD's extra Serana scenes use 28 Serana lines of its own; Serana Dialogue Add-On is unaffected (different quests).

---

## Appendix A — Technical notes (for execution)

- Lydia record: `0A2C8E:Skyrim.esm`. Winner chain: Skyrim, USSEP, USMP, UBE Lydia.esp, Requiem, USMP-Requiem, Authoria - Master Patch - NPCs Merge, Requiem for the Indifferent, Authoria - Patch - Lydia UBE Weight (winner).
- New voice type: `005901:ImprovedCompanionsBoogaloo.esp` (FemaleUniqueLydia). Old: `013ADD:Skyrim.esm` (FemaleEvenToned).
- SkyPatcher line (npc folder): `filterByNpcs=Skyrim.esm|A2C8E:voiceType=ImprovedCompanionsBoogaloo.esp|5901`
- USSEP-carrying lines IFD overrides: `0DE50E:Skyrim.esm` (PreviousDialog differs), `0A2C6C:Skyrim.esm` (response differs). IFD adds `GetIsID Lydia == 0` to each.
- Placed NPC: `0D9651:Skyrim.esm` (dunPOISummoning script, Ritual Doomstone). IFD: Persistent flag + LocationReference `0D567A:Skyrim.esm`. Winner: Authoria - Reqtificated - Ryn's Standing Stones.esp.
- Terrain records won by Synthesis output: `00A0FF, 00AB20, 00AB21, 00AB41, 00AB42 :Skyrim.esm`.
- Shared navmesh with 3DNPC: `0FD5D5:Skyrim.esm` (identical on geometry read).
- Kaidan IF voice folder: `mods\Immersive Kaidan AIO - rerun\Sound\Voice\Kaidan - Immersive Features.esp\FemaleEvenToned\` (334 files). Per-line classification: scratchpad `kif_fet_conditions.json` (217 GetIsID Lydia; others are Arcadia 67, Ria 23, Carlotta 9, Ralof 2, Skulvar 1, 3 follower-generic).
- Inigo: winner plugin file is in mod "Inigo - cleaned esp File"; audio in `mods\INIGO\Inigo.bsa` (InigoNpcChatMain, 79 Lydia INFOs; 4 InigoShopping lines are alias Shopkeeper, skip).
- Lucien: `mods\Lucien - Immersive Fully Voiced Male Follower\Lucien.bsa`, quest JRLucienLydia (3 INFOs).
- AA quests: `49C728` (AmorousAdventuresLoverDialogueLydia, only AA touches it) and `2BBF62` (SexLabAmorousAdventuresSteel, winner AAOstimSequenceAndRewrittenPatch.esp). IFD's disabler adds DialogCondition `GetIsID(PlayerRef, 064B41:Skyrim.esm) == 1` (always false).
- BSArch: `D:\1. MOD STUFF\- ARR STUFF\CLAUDE\xedit\BSArch.exe` (not in tools\xEdit).
- IFD plugin slot anchors (CS profile, pre-install numbering): FDE Lydia.esp line 896; AA plugins 467–473; 3DNPC.esp 64; Authoria Reqtificated block ~3359–3498; late custom patches ~3675–3800.
- Plugin census method: winner file per plugin via modlist priority, ESL bit 0x200 in the header; 5 base masters added (no full CC plugins are implicit here).
- DBVO filename rule: space and `\ / : * ? " < > |` → `_`; all else verbatim (UTF-8, curly quotes included). Verified 2802/2876 on Kaidan IF.

---

## Status — 2026-08-21 (CS profile only)

Landed:
1. FDE Lydia disabled (mod + plugin). Folder kept, disabled.
2. "Improved Follower Dialogue - Lydia" installed (core + Bruma + Wyrmstooth + LotD patches; meta.ini carries the Nexus id; archive + .meta copied to the instance downloads). Plugins load right before Inigo, group "Quests and Newlands - Followers". All masters present; zero dangling references.
3. "Authoria - Patch - IFD Lydia": SkyPatcher voice line (verified applied on Lydia's record by the houseCARL replay), Kaidan IF 334 files + Inigo 79 lines (160 files) + Lucien 3 lines re-keyed under FemaleUniqueLydia, and the light plugin (Steel Angel + Lover-dialogue quests carry the always-false condition on top of the OStim winners; USSEP's capitalisation fix kept on the housecarl greeting). Plugin sits last in "Authoria - Late Custom Patches", right before Requiem for the Indifferent. Zero errors.
4. "Authoria - Eleonora - IFD Lydia": empty folder + README + manifest, enabled above the pack, waiting for your recordings.
5. Grass driver for the new worldspace: `_tools\ifd-lydia\grass_regen_ifd.py` (stage/collect per season, finish restores the inis).
6. Backups: `profiles\DEEZ CS NUTZ\*.bak-ifdlydia-20260821`.
7. The Ritual Stone necromancer forward turned out unnecessary — our Reqtificated Ryn's patch already carries IFD's persistent flag and location. The navmesh-info-map merge was NOT done: the engine rebuilds that map's connectivity from the navmeshes' own edge links at runtime, and every earlier Authoria navmesh patch in this build left it alone too.

Requiem pass (done): "Authoria - Reqtificated - IFD Lydia.esp" (light, 15 overrides, masters Skyrim/Dawnguard/IFD/Requiem/Magic Redone; zero errors), in the "Authoria - Reqtificated" block. Jori's axe = Draugr-tier unique (value 330, crit 11, 3000 charge, no re-enchanting, damage kept at 22); its enchantment rebuilt on Requiem's Frost III weapon enchant (frost + stamina + slow), and its on-kill explosion re-pointed to the mod's own frost burst (it was wired to Requiem's Dawnbreaker explosion and never fired) with the player excluded; Lydia's self-buff spell moved onto Requiem's restore-stamina effect. NPCs de-levelled: Assassin fixed 45 on Requiem's assassin template; Jori 24, Vonjar 19, Kolgar 10, Eselda 10, Fenrar 10, Eorald 10, Falcius 10 on Requiem bandit templates with matching classes, combat styles, perks and tempering traits. Skipped with reasons: Maximus (scripted prop), the utility actors, the templated soldiers and leveled bandit, Lydia's bash perk and armour buff, the debug apple/effect, books, outfit, faction, form list. Reqtificator re-run required.

Still yours: (1) Eleonora recordings into the new folder; (2) Synthesis worldspace re-run (IFD's five terrain edits); (3) Reqtificator re-run; (4) grass passes with the driver; (5) in-game checks, section 4 step 10.

---

## Reqtificator master-list overflow — 2026-08-21, resolved

Installing this mod pushed the Reqtificator over its hard limit of 254 plugins, and it refused to export
twice. Re-running Synthesis could not help: the patcher only reads plugins that load before its own file,
and Synthesis output sits after it.

Fix: mod "houseCARL - Authoria - Patch - Reqtificator Masterlist Relief" (light plugin, CS profile only,
last plugin before Requiem for the Indifferent). It hands the patcher its own finished result for 893 items
across 39 mods, so those mods stop being counted. Confirmed by a real run at 14:17 — SUCCESS, 255 down
to 212, about 40 slots spare. A whole-item-layer audit found zero armour ratings and zero weapon values
changed anywhere in the build.

It works on preconditions and Requiem's own skip markers, NOT on "the values already match" — the patcher
has no before/after check at all. The mod folder's README explains this; read it before rebuilding.

Also fixed the same day: the Requiem pass on this mod had replaced four characters' spell lists instead of
adding to them, silently deleting Flames, Healing and Firebolt from the bandit assassin, Eselda, Fenrar and
Eorald, plus a vampire-feed perk from four of them and four Requiem perks from the assassin. All restored
and verified against the mod's own records. This reaches the game on the next Reqtificator run.

