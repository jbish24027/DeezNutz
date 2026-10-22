# Everdamned Install Plan — v2 (decisions resolved)

**STATUS: EXECUTED 2026-08-27.** All stages of §4 and §8 completed by Claude in one session (MO2 closed throughout). Backups: `*.bak-everdamned-20260827` beside all 4 files in all 4 profiles. Delivered: Sacrilege chain disabled ×4 profiles; Everdamned 1.6.3 installed (FOMOD choices per plan, hash-verified, RCS script variant + CIF config path confirmed); Spells Sort installed (re-downloaded from Nexus after Downloads was cleaned; FormID-keyed, rename-immune); plugin slots at Sacrilege's exact former positions; `Authoria - Patch - Everdamned - Requiem.esp` authored (ESL, 55 records, 11 masters, integrity-clean) + SAN ini override with Serana×3 + Valerica exclusions (VFS-verified winning) in mod folder `houseCARL - Authoria - Patch - Everdamned - Requiem`, loading after the MGEF-Merge patch in all 4 profiles. All §5–§7 lanes executed incl. the MR pass (13 spells re-costed, 30+ effect keywords, 4 stagger riders, Maelstrom re-schooled), 7% infection carry-forward, RVC boss re-asserts, ISC audio grafts (ED's own drain audio kept where intentional), UBE formlist hardening, boss-tome dedup (minimal), creature-race lane (4 patched / 2 earned skips; 3 trait perks + 2 ghost keywords on NPCs; Requiem's flame-atronach resist NOT copied — wrong polarity for cold-flame; Manbeast's werewolf controller NOT copied — overhaul machinery). USSEP audit closed as superseded (2 deep-dive confirmations). Final census 240/254 FULL in the CS profile — net-zero as designed. Wheeler raw-ID reindex attempted per house rule: the wardrobe JSON no longer exists anywhere (wardrobe-ESP era) — nothing to reindex.

**HOTFIX 2026-08-27 (post-launch-attempt).** The user's first launch was blocked: "masters for some plugins are not enabled — Sacrilege … required by Authoria - Patch - Reqtificator Masterlist Relief.esp". A **fourth** Sacrilege dependent existed that the evidence sweep's dependent scan missed (it grepped the first 64KB for the master's name instead of parsing TES4 headers). A correct recursive header parse of all 4,364 plugin files confirms only 4 ever mastered Sacrilege: the 3 known departing ones plus the Relief patch. That patch's only tie was **CONT 1A81F1 `SQL_CheatChest_Container`** — Sacrilege's debug cheat chest, forwarded there purely to keep Sacrilege off the Reqtificator's master list. Removed in place; the orphaned master auto-pruned (masters 50→49, records 893→892; houseCARL had to be given the master temporarily to re-serialize, then it was re-disabled). Its `relief-manifest.json` and README were amended so the documented rebuild recipe won't re-add it, and the pre-edit file is backed up as `*.esp.bak-everdamned-20260827`. **Verified: unscoped `check_errors` over all 4,090 active plugins now reports `0 missing masters`** (the 5,060 dangling refs are pre-existing vanilla noise — `Skyrim.esm`'s own CWTestHold/Region records). RFTI's live header declares 216 masters and no Sacrilege, so the Reqtificator export is unblocked. Order re-verified: Everdamned.esp (1960) is before Lux (3053) and the navmesh block; the integration patch (3973) sits right after MGEF Merge and touches no CELL/NAVI.

**Pre-existing observation, NOT changed (user's call):** the Relief patch's README requires it to be the last plugin before RFTI, but three plugins now follow it — `Authoria - Patch - New Weapons - Requiem.esp`, `Authoria - Vibrant Weapons - New Blades.esp`, `Authoria - Starting Kit.esp`. Unrelated to this swap; if any overrides a weapon/armour the Relief patch carries, that plugin returns as a master on the next export (worst case still well under the cap).

**Remaining: user runs Pandora (tick "Everdamned"), then the Reqtificator, then the §10 test protocol on a fresh save. Do not launch the game before both tool runs.**

**Date:** 2026-08-20 (v2, supersedes v1 same day) · original status: PLAN ONLY.
Evidence: two read-only workflow sweeps (8 lanes + 4 lanes, 632 tool calls) over the extracted 1.6.3 archive and the live load order (profile `DEEZ CS NUTZ`). **All live winners provisional — MO2 may have been open. Re-verify contested winners with MO2 closed on execution day.**
User decisions D1–D12 received 2026-08-20 and folded in below. Remaining user inputs: the two small items in §9.

---

## 1. Verdict (unchanged from v1)

Everdamned 1.6.3 fits. It is a **Sacrilege→Everdamned swap** plus one Authoria integration patch stack. UBE player is safe (§3). All 15 requirements installed; slot-neutral; behavior engine is **Pandora** (re-run with the Everdamned patch manually ticked); Reqtificator re-run mandatory (its output masters Sacrilege).

Key numbers: Everdamned.esp = 2,923 records, 148 vanilla overrides (zero races/NPCs/dialogue), Reqtificator output contests none of them. Known open ED bug: possible CTD loading with summoned actors. Author on hiatus.

---

## 2. Resolved decisions (D1–D12)

| # | Decision | Resolution |
|---|---|---|
| D1 | Scope | **All 4 profiles** |
| D2 | Harkon/NPC-vampire drains | **Requiem/RVC balance** — integration patch re-asserts RVC/Requiem on the 12 Harkon drain spells + gargoyle summon effect + NPC drain effect; ED keeps all player-side records |
| D3 | Blood potion | **ED wins** (Vitae economy item; Requiem's hunger effect consciously dropped) |
| D4 | ISC audio | **Forward** ISC sounds onto ED's two drain effects + merged Slow Time wear-off descriptor |
| D5 | Healing-block gate | **Leave stock.** The perk slot ED checks = Magic Redone "Mystic Turning" (Resto 75) — the intended escape hatch. FOMOD Necromage patches are never installed |
| D6 | Player-vampire combat penalties | **No patch needed — see §5.** The old patch was NOT a softener; the live tweak-suite version survives the swap on its own. Combat-strong is served by adopting ED's stock numbers and NOT re-creating the old drain nerf |
| D7 | Holy-ground damage | **Keep** (race-granted Requiem trait, fits ED lore) |
| D8 | NPC sun systems | **Keep both + Serana exclusion — see §6.** Evidence shows they complement rather than stack: ED's NPC part only suppresses regeneration (its effects resolve to Requiem's regen-suppression records here); SAN does the actual burning, combat-only, bare-headed, daylight-only |
| D9 | UBE hardening | **Yes** — 8 UBE race pairs appended index-matched to ED's two race formlists. UBE is the only played race |
| D10 | Old balance intent | **Explained plainly in §5**; nothing re-created except the two carry-forwards listed there |
| D11 | Spells: Requiem-patch + sort + dedup | **Committed — see §7.** 23-spell Magic Redone worklist ready; ABM II overlap census done (3 true duplicates, dedup = pull the 2 free power tomes); Spells Sort ini installs last (SkyPatcher v6 confirmed present; archive still needs downloading) |
| D12 | Save | **Always fresh save** — removes the mid-save-removal risk class entirely |

---

## 3. UBE safety (unchanged, confirmed)

Safe under three enforced conditions: (1) FOMOD race-compat = **"Race Compatibility SKSE (RCS)"**; (2) Everdamned's loose scripts win over RCS + RCS PatchHub (PatchHub stays enabled — it carries the live RaceCompatibility.esm; the departing `Authoria - Sacrilege RCS Updated Patch` is the current script winner and must be disabled); (3) `Authoria - UBE Patches` keeps providing the UBE→vampire race mapping json, RCS DLL stays. Every failure path = loud "RaceBroken" + Nord fallback. Record-side: UBE Breton vampire race carries the Vampire keyword + full Requiem parity + identical head/skeleton/skin to the base race. §8 hardening makes the primary lookup hit without the native call. First-transform test on a protected save (tint-count mismatch + known UBE slider trap). One-time VL transform/revert race check.

**Guardrail for all patch work:** never add the Vampire keyword to Serana's three actors or to UBE races' base forms, and never add sun/searing spells to their spell lists — Serana's protection-by-absence (§6) depends on it.

---

## 4. The swap (execution day, unchanged from v1 §2/§4 with D-resolutions applied)

0. **Pre-flight (MO2 closed):** hotfix-delta backup; full-slot re-census (provisional 240/254; swap net-zero); re-verify §5–§7 winners; AVG toml alias-collision diff (ED claims Variable01–08, five SkillAdvance AVs, Fame — must be clean vs the 7 existing ActorValueData configs); grep runtime inis for `SQL_` and for old vanilla EditorIDs of ED's 148 override targets; download Spells Sort 168803 (manager-only — user, or via the Nexus MCP session).
1. **Disable the Sacrilege chain** in all 4 profiles (modlist + plugins + plugingroups): Sacrilege mod, `Authoria - Sacrilege RCS Updated Patch` mod, `Authoria - Master Patch - Sacrilege.esp` (plugin only — its host mod folder stays), `Authoria - Sacrilege Rebalance.esp`.
2. **Install ED 1.6.3** (fomod_tool.py): Main ✓, Perk Overhauls = None, Race Compat = RCS, Assorted = Survival Mode ✓ + Vampire Feed Tweaks ✓, rest skipped. Post-install: archive-vs-installed diff; confirm the installed vampire quest script is the RCS variant (byte-compare); confirm the CIF config landed at `SKSE\CoreImpactFramework\` (above SKSE\Plugins).
3. **MO2 priority:** Everdamned above RCS, RCS PatchHub, Vampire Feeding Tweaks.
4. **Plugin order:** Everdamned.esp after Requiem.esp/USSEP/USMP/ISC/Requiem-ISC/RVC; before Lux.esp, the `Authoria - Navmesh - *` block, and outputs. Hard: ED never wins the worldspace NAVI (324 touchers) or the Lux Apocrypha cell. Never compact/ESL-flag Everdamned.esp.
5. **Build the patch stack** (§8), ESL-flagged, late in the patch block, before outputs.
6. **User re-runs:** Pandora (tick "Everdamned" manually + keep Precision/Precision Creatures/Payload Interpreter), then Reqtificator. Wheeler raw-ID snapshot check per house rule if any light plugin count changed.
7. Install Spells Sort ini (no esp) last.

---

## 5. D10 — what your old tuning actually did (plain), and what carries forward

Evidence: full diff of both departing patches against Sacrilege/Requiem (lane `old-balance-deltas`).

**Layer 1 — "Master Patch - Sacrilege" (built 2026-07-27, 89 records).** Mostly *restoration*, not invention: it re-imposed Requiem's and Requiem VampireCollection's numbers over Sacrilege (fire weakness back to 75%, disease immunity, Harkon boss drains, NPC vampire claws/traits). On top of that, four deliberate choices of yours:
1. **Hood-blocks-sun**: sun damage only ticks bare-headed (conditions wired to Helmet Toggle 2's global) on the mortal sun stages.
2. **Sanguinare infection proc raised 3% → 7%** (plus Recover flag removed, custom flavor text).
3. Cost bumps on Sacrilege's blood spells and tweaks to its VL scaling (die with Sacrilege — irrelevant under ED).
4. The **craftable become-a-vampire potion recipe disabled** (Sacrilege record — dies with it).

**Layer 2 — "Sacrilege Rebalance" (final edit 2026-08-18, 11 spells).** A drain nerf: it kept Requiem's expensive manual costs (75 magicka on the main drain) but reverted the magnitudes to Sacrilege's weak values — final live drain was **5/5/5 per second for 75 magicka**. VL Raze was similarly pulled from 50 back to 10.

**The player-penalty perk (D6):** Requiem stock puts silver/Dawnguard-weapon vulnerabilities + a strong arrow resist + bottled-blood drops on the vampire player. Your patch did **not** soften this — it forwarded the *harsher* MR WAR tweak-suite rework (silver ×1.5 damage and spell magnitude, Dawnguard gear ×1.25, the Ancient Dawnguard Warhammer ×2, arrow resist removed), deleting only the bottled-blood drop entry. After the swap the tweak-suite's own version wins again — identical to what you played with, plus bottled blood returns on vampire kills (harmless; ED has its own blood economy).

**What this means under "vampires should be combat-strong":** ED's stock drain is **6/6/6 per second at trivial cost with a 0.2s charge, plus execute/Vitae/XP riders** — already stronger than your final tuning. We adopt ED stock and deliberately do **not** re-create the drain nerf or the cost stamp. Only two things carry forward:
- **Hood-blocks-sun** → ED ships this natively as an MCM option (headwear sun protection). Zero records; set it in the MCM at first launch.
- **7% infection chance** → one small MGEF override in the integration patch re-expressing the proc bump on the live Requiem/RMA disease chain (which ED watches for infection).

---

## 6. D8 — Serana and the two NPC sun systems (evidence-settled)

**Serana takes no sun damage today and none after the swap by default.** All three of her actor bases (base, Multiform vampire, Multiform cured) lack the Vampire keyword on actor and race, none has ever carried the NPC sun ability in any override (so no Reqtificator merge can resurrect it), SAN's distribution can't match her, and SAN's effects additionally hard-require the Vampire keyword. Protection is by absence — fragile, so we harden:

- **One single-record ESPFE** (`Authoria - Patch - Everdamned - Serana Sun Exclusion`, or folded into the main patch): ED's NPC sun ability copied verbatim + three `GetIsID == 0` conditions per effect (her three actor bases; GetIsID is reliable on NPCs — the house trap is player-only). Masters: Skyrim, Dawnguard, Everdamned, SeranaMultiformNG. Survives Reqtificator re-runs (RFTI never touches this spell). Must be the LAST override of that record.
- **A VFS-overriding copy of SAN's distribution ini** in the patch mod folder with three form-exclusion filters (house precedent exists: the Wet-and-Cold SPID patch already excludes Serana this way). Original mod untouched. Re-diff on any SAN update.

Why "keep both" systems is sound: under this load order ED's NPC sun ability resolves to **regen suppression only** (its three effect records are Requiem's functional regen-suppression forms), while SAN does the actual health drain — combat-only, daylight hours, bare-headed. Complementary, not double-burn. WSSHV is proven player-only.

**Valerica included (user decision 2026-08-20):** one actor base only — `DLC1Valerica 003B8B:Dawnguard.esm` (verified: the sole Valerica NPC record in the order; live winner is the Reqtificator output at depth 6 — note-only). She gets the same treatment as Serana's three bases: a fourth `GetIsID == 0` condition on the ED NPC sun ability override, and a fourth form-exclusion filter on the SAN distribution ini line. No new masters (Dawnguard already present). Verify at execution she carries no other sun path (same absence checks run for Serana).

---

## 7. D11 — spells: Requiem patching, dedup, sorting

**7a. Magic Redone worklist (committed, 23 player spells).** Full row-by-row table with proposed costs/keywords/classifiers in the evidence lane (`mr-pass-scope`); execution walks it mechanically. The doctrine it enforces:
- **Mortal Hemomancy line** (Blood Seed/Bloom/Garden/Scourge/Ankh/Boil/Vortex/Borrowed Time/Ward/Profaned Sun + main drain): normalize costs to MR ladders (manual-calc flag as a UNION with existing flags), add Requiem behavioral keywords (absorb/concentration/no-duration-scaling; stagger riders on fire-and-forget bolts), set the Novice/Adept classifiers where empty. Two are already Requiem-classified out of the box (Blood Ankh, Profaned Sun).
- **Hard constraints:** never repoint the 8+ Vitae cost-shim perk links; never strip ED keywords; no effect-list surgery on script-driven spells (scalars/riders only); no duration normalization on ED summons (fights ED's own scaling); **no poison keyword on blood DoTs** (would misroute into poison rescaling); Poison Talons deliberately left un-keyworded (VL innate).
- **Three dual-cost collisions flagged** (Blood Vortex, Shambling Hordes, Maelstrom): MR ritual pricing would double-charge on top of ED's Vitae price — keep ED pricing, document.
- **VL spells keep VL economy** (quest-granted, not tome-learned); keywords only. Double-dip of ED's own scaling with newly-enabled Requiem perk boosts is accepted per combat-strong and flagged per row.
- NPC-only spells, 111 internal sub-spells, and 23 dev-cruft TEST/old records: excluded, itemized in the lane data.

**7b. Overlap census (done).** The only player-facing blood/vampire spell pack besides ED is **Ancient Blood Magic II** (14 tome-gated spells; 5 injected into draugr/warlock tome loot at runtime, 9 boss-drop only; its SPID also gives 4 spells to enemy vampires — a reason to KEEP it installed). Sanguine's Trade is an escort-economy skill — zero overlap. Findings:
- 3 true duplicates, all boss-gated: Conjure Stone Gargoyle, Bats Form (free power), Blood-Flame Whirlwind.
- **The one real economy clash:** the two FREE lesser powers (Bats Form, Harvest of Bats) from the Night Matron drop — free bat-escape bypasses ED's Vitae-priced travel powers.
- **Dedup (recommended, minimal):** remove the two Power Tomes from the boss death-item list in the integration patch. The duplicate *spell* tomes stay (magicka-priced Destruction/Conjuration vs ED's Vitae powers — mechanically distinct; both boss-gated). Strict variant (also pull the gargoyle + whirlwind tomes) available if you'd rather ED own those fantasies outright. Check at execution that nothing else overrides that death-item list so the removal survives the Reqtificator's list merging.

**7c. Sorting.** Spells Sort (168803) = SkyPatcher name-prefix ini, no esp, safe anytime, installs last. SkyPatcher v6.0.0 confirmed present. Archive not yet downloaded (manager-only). Prefix format gets a quick sanity read post-download (FormID-keyed expected — immune to the EditorID-rename trap).

---

## 8. The integration patch stack (final composition)

`Authoria - Patch - Everdamned - Requiem.esp` (ESPFE, houseCARL-authored, loads after MGEF-Merge/ISC patches, before outputs):
1. ISC audio forwards: player drain effect, VL drain effect, Slow Time wear-off descriptor (ED conditions + ISC sound merged) [D4].
2. RVC/Requiem re-asserts: 12 Harkon drains, Harkon gargoyle summon effect, NPC drain effect [D2].
3. UBE hardening: ED's two race formlists + 8 UBE pairs index-matched [D9].
4. Sanguinare 7% proc re-expression on the live disease chain [D10].
5. ABM II dedup: boss death-item override minus the two Power Tomes [D11].
6. MR worklist application: the 23-spell pass per §7a [D11].
7. Creature-race lane: ED's 4 real creature races classified per Requiem race doctrine (Fleder→VL beast race analogue, Cold Flame Atronach→Flame Atronach, Fogling→wisp-class, Ghost Spider→frostbite spider + ghost keyword), their NPCs balanced via the NPC lane; utility races skipped with reason; vanilla-race summons verified to inherit traits.
8. USSEP audit of the 22 residual-toucher records (expectation: nearly all superseded by ED's rework; forward only surviving data fixes).
9. Fallback sweep: no Sacrilege-shaped hole left as winner on slots ED doesn't override (e.g. Supernatural Reflexes perk).

Plus the Serana exclusion pair from §6 (ESPFE record + SAN ini override copy — possibly folded into the same mod folder, exclusion record loading last among 0F5B5D touchers).

Deliberate no-actions: Necromage gate stock [D5]; holy ground stays [D7]; blood potion ED-wins [D3]; player-penalty perk untouched [D6]; sleep-feed stays ED-disabled; load screens stay LSC's; ED drains bypassing Requiem absorb counterplay accepted (player-favoring, aligns with combat-strong).

---

## 9. Remaining user inputs — ALL RESOLVED 2026-08-20

1. **ABM II dedup depth: MINIMAL** — remove only the two free Power Tomes (Bats Form, Harvest of Bats) from the boss death item; the duplicate spell tomes stay.
2. **Sun exclusion: Serana + Valerica** (four actor bases total — §6).

**The plan is fully closed. Execution can start on request (MO2 closed).**

Play-notes (unchanged): keep ED's Vitae powers off Spell Hotbar; don't open wheels during ED slow-time; MCM lands ~127/128 — verify ED's menu registers, add nothing MCM-bearing afterwards; potion/food healing bypasses ED's healing block by engine design.

## 10. Test protocol — unchanged from v1 §7 (fresh save, protected saves at each step), plus: set ED's headwear-sun-protection MCM option at first launch [D10 carry-forward].

## 11. Evidence index

- Sweep 1 (8 lanes): `...\scratchpad\lanes\lane-*.json` — override census (all 148 rows), Sacrilege footprint (704 records + profile matrix), script/VFS providers + race-swap sources, UBE race parity, Requiem vampirism map, requirements/slots, Nexus doctrine/ecosystem, magic economy triage.
- Sweep 2 (4 lanes): `...\scratchpad\lanes2\lane-*.json` — old-balance deltas (D10/D6 evidence), Serana sun exclusion design (D8), ABM II overlap census (D11), MR 23-spell worklist (D11) + per-spell dumps (`ed_spells_detail.txt`, `ed_buckets.json`).
- Base: extracted archive at `...\scratchpad\everdamned-main\` (session-temporary; re-extract from Downloads zip if cleaned).
