# Authoria - Reqtificated - Immersive World Encounters

Built 2026-08-20 by Claude via houseCARL. ESL-flagged, overrides only (~245 records).
Covers: Immersive World Encounters. FINAL SE v3.6.1 (mod 18330, fetched via API while hidden)
+ Immersive World Encounters - A High Poly Overhaul v1.0.0 (mod 120853)
+ the FOMOD's RS Children patch (installed; CACO/Open Cities/Great City of Solitude options skipped - targets not present).

Load position: "Authoria - Reqtificated" block, directly after Authoria - Reqtificated - Missives.esp, all 4 profiles.
IWE itself: Gameplay - Early Loaders, after Rite of Arcana.esp. Overhaul + RS patch: Visuals - NPC Visuals block.

## What the patch does

### NPC de-levelling (the core work)
IWE enumerated at 580 NPCs; every one dispositioned.
- 172 actors moved from player-scaling (or wrong tiers) to fixed Requiem levels.
- Level ladder derived from Requiem's own treatment of the exact vanilla counterparts:
  civilians/bards/porters/revelers/cooks/scholars 4 · wizards 7 (their own REQ bandit-mage template tier) ·
  wanderers/pirates/thugs/prisoners/muggers 10 · thieves/adventurers/Companions-huntress/Nord warriors 25 ·
  bounty hunters/elite adventurers/assassin-maid 30 · soldiers/Eastmarch Thane 35 · Vigilants 36 ·
  Dawnguard/Sal 50 · cult-enemy template 20 · Monica's champion 40 (Monica herself: elder civilian, 4).
- 10 actors given Stats/SpellList template inheritance instead (Karliah, her ghost, Nazir, Beatrice,
  the vampire girl, both armored huskies, both Dawnguard bases, the Vigilant base) - they now inherit
  live Requiem balance from their vanilla/Requiem primaries forever.
- 3 orc bandits re-templated off REQ_NULL_EncBandit01Melee2HOrcM (a retired Requiem husk) onto live
  REQ_Bandit_Generic_MeleeOrcM / _Melee, plus L10.
- The painted-cow giant: full Requiem giant treatment (L70, +1000 health, +1400 stamina, Requiem giant perk).
- Stat mode: AutoCalc/as-authored preserved on every record; only the level arm was written. No stat blocks,
  no flags unions disturbed, appearance fields carried from the High Poly Overhaul winners automatically.
- Deliberate keeps: Evelyna x3 + Neddvir + follower husky keep player-scaling (follower rule; huskies
  mirror Requiem's fixed-L2 armored husky via inheritance instead); hunters mirror Requiem's own
  non-treatment of EncHunter; children untouched; ~278 actors verified as inheriting through walked
  template chains; 54 authored-fixed civilians (L1-10) kept as Sette designed.

### Buried-record rescues
- WERoad01 + WE24 forwarded from IWE (their modified quest-fragment scripts ship in IWE's BSA; the records
  had been buried by Alternate Perspective / Minor Arcana, which would have run those scripts with unfilled
  properties). Alternate Perspective's two alt-start protections (Unbound complete + level >= 4) re-grafted
  onto WERoad01, so it now carries all three gates.
- City Location registrations merged: Riften 16, Windhelm 11, Solitude 12, Tolvald's Cave 2 event-marker
  rows added on top of the live winners (Lux Orbis / Grand Solitude / Requiem), so IWE's city events find
  their markers without disturbing Lux lantern parenting.

### Item fixes
- Hektor's Crossbow: 19 -> 60 damage, value 135, weight 7, + Requiem's crossbow keywords
  (breakable, heavy-crossbow class, no-rescale exclusions) - mirrors REQ_Weapon_Steel_Crossbow.
- Hooded Thalmor Robes copy: was Light Armor AR 30; now Clothing AR 0 with Requiem's full keyword set
  including the Thalmor disguise keywords and Survival warmth - mirrors REQ_Cloth_Thalmor_Body_Hooded.

## Verified no-action lanes (checked, left alone on purpose)
- Consumables (3): tea/brandy/stew already run on Requiem's own alchemy/nutrition effects via vanilla IDs.
- Bound daggers (2): byte-identical to Requiem's own bound dagger. Volendrung replica: sane prop tier,
  correct warhammer keywords (note: Sette authored it OneHanded - left as designed).
- All 151 leveled lists: flat (every entry level 1), variety pools only - no player scaling anywhere.
- 71 spells / 76 magic effects / 3 shouts: NPC event kit, nothing player-learnable (0 tomes in 17 books);
  the Reqtificator's all-actor spell rescaling covers magnitudes at build.
- Dialogue/scene/package overrides: IWE wins all that matter; keyword shells harmless.
- WIThief: Requiem's fixed version correctly beats IWE's scaling edit. Beggar charity boon: Requiem's wins
  (correct). Thief-ambush story node: Requiem's gating wins; quest lists identical, only IWE's extra
  frequency throttles lost (cosmetic). WIAddItem03: Minor Arcana wins; IWE's per-event MCM toggle for that
  one vanilla event won't bite (cosmetic).
- CELL/worldspace overrides: Lux and generated outputs win by design (lighting/terrain stay theirs).

## Addendum 2026-08-20 (later): official High Poly Uniques add-on
"Immersive World Encounters AddOn - High Poly Uniques" V1.2 (mod 50999, all-in-one + shared assets,
ESL esp) installed in all 4 profiles, deliberately BELOW the attackdr0ne overhaul: mod priority
HPO > AddOn > IWE; plugin order IWE.esp -> High Poly AIO.esp -> (later) _ImmersiveEncountersOverhaul.esp.
Coverage check: all 8 of the add-on's faces (Adderick=Adrius, Beatrice, Einvard, Evelyna, Leleanna,
Nestynia, Roxelle, Roza tint) are inside the overhaul's 14 - the add-on is FULLY SHADOWED and changes
nothing visually while the overhaul stays above it. To prefer Sette's official faces instead: move the
add-on mod BELOW the overhaul in the left pane AND its esp AFTER _ImmersiveEncountersOverhaul.esp,
then re-derive this patch's 7 overlapping NPC overrides (they currently carry the overhaul's face data)
and re-run the Reqtificator. No patch or Reqtificator work was needed for the shadowed install.
Verified: the user's Reqtificator run (between sessions) already folded this patch's levels into
Requiem for the Indifferent.esp (spot checks: Evelyna 4, prisoner-thief 25).

## Standing obligations
- Re-run the Reqtificator after enabling (new NPCs need its build pass; it also settles the visual merge).
- The patch must load after IWE, the High Poly Overhaul, Requiem, Minor Arcana, Alternate Perspective,
  Lux Orbis, and the Grand Solitude patch (its current slot satisfies all of this).
- If IWE's Location merges ever conflict with a new city mod, re-derive the four Location records.
- MCM count after IWE: ~126 of 128 SkyUI slots.
