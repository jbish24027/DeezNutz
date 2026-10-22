# Immersive World Encounters — dragon content audit (2026-08-21)

Scope: Immersive Encounters.esp (IWE 3.6.1), read-only audit. No files changed.

## Summary

IWE has exactly **three** events that put a live dragon in the world. It defines no
dragon actor, no dragon leveled list, and no dragon spawn of its own — every dragon
is pulled into a quest alias from vanilla forms. Nothing else in the mod spawns one.

| # | In-game event | Starts how | Off-switch today |
|---|---------------|-----------|------------------|
| 1 | A dragon attacks a capital city when you arrive | Automatic | MCM toggle exists |
| 2 | Blades on the road, heading out to hunt a dragon | You volunteer | none (Blades toggle only) |
| 3 | Legion / Stormcloak patrol marching to a dragon's nest | You volunteer | none |

## 1. Dragon Attack in a capital city

- Quest `WI_SetteCL03` "Dragon Attack", story node `WI_SetteCLNodeDragon` (919DA8).
- Node conditions: `SetteToggle_WIAll` = 1, `SetteToggle_WIDragon` = 1, CWSiege not
  running, new location has LocTypeHabitationHasInn **and** LocTypeCity, **not**
  LocTypeSettlement, **not** LocTypeDwelling. So: capitals only.
- Timer: the quest calls the vanilla `WIs.updateWIDragonTimer()` / `RegisterDragonAttack()`.
  It rides vanilla's settlement-dragon timer, not IWE's own "min days between events" slider.
- MCM: "WI: Dragon Events" — *"ON/OFF a dragon occasionally attacking major cities."*
  Global `SetteToggle_WIDragon` (CC2A30).
- This is the only one of the three that is **not** opt-in.

## 2. Blades Dragon Hunt

- Roadside encounter `WE_SetteBlades02` "Blades On Their Way To Dragon Hunt" (0F8A8C),
  in story node `WE_SetteRoads` (84535E).
- Encounter gates: Rebuilding the Blades stage 40 done, `SetteToggle_WECVQuestInt`,
  `SetteToggle_GlobalFaction`, `SetteToggle_WEFactionBlades`.
- The encounter itself is just three Blades walking. **No dragon spawns here.**
- The dragon lives in the follow-up `SetteBladesDragonHunt` "Dragon Hunters" (9333F8),
  started only from the player topics "You have a Dragon to slay? May I come with you?"
  and "[Dragon Hunt] Lead me to the Dragon's Lair" (branches 3C8912 / 3C8915).
- Turning off the Blades faction toggle also kills `WE_SetteBlades01` "Blade vs Thalmor",
  which has no dragon in it.

## 3. Soldiers marching to a dragon's nest

- Intro encounters `WE_SetteQuestIntSoldiers01Imp` (C3004E) and `...Sons` (C3004F),
  in story node `WE_SetteQuestIntros` (8A055E), 50% random gate.
- Each intro has two follow-up quests: ObjA (bandit / animal mission) and ObjB (dragon
  nest). Imp: F6E6A8 / F788D9. Sons: 0A3649 / 0A876E.
- The pick is made in `TIF__05F737C9` on the player topic "I am happy to help.":
  `If GetOwningQuest().GetStageDone(15) == 1 → QuestB.Start() Else QuestA.Start()`.
  Same shape on the Sons side. Intro stage 15 = the dragon variant.
- The declining topic "I can't help you." (F737C5 / Sons equivalent) is always available.
- The encounter itself is just soldiers on the road. **No dragon spawns until you accept.**
- Note: `SetteSoldiersBossAnimal` / `SetteSoldiersBossBandit` are the ObjA/ObjB script
  properties on the intro — they pick the *boss type* of the non-dragon mission, not the
  dragon branch. Don't confuse them with QuestA/QuestB.

## Not dragon events (checked, no dragon involved)

- "Farmer refugees after dragon attack" — an aftermath camp, scenery only.
- "Collect 10 Dragon Bones / Dragon Scales" fetch objectives — inventory checks.
- Bard songs about the Dragonborn, ghost combat taunts mentioning dragons — audio only.
- `SetteBlades02DragonHuntReward` (3BE70F) — a leveled reward item list.

## Surgical patch — BUILT 2026-08-21

Mod folder `houseCARL - Authoria - Patch - IWE No Dragon Events`, plugin
`Authoria - Patch - IWE No Dragon Events.esp`. ESL-flagged, form version 44, **6** override
records (not 4 — the soldier fix needs 4 dialogue responses, two per faction), 5886 bytes.
Inserted in all 4 profiles in the "Authoria - Custom Patches" group, directly after
`Authoria - Patch - IHSS - Horsepower.esp`. Per-record ledger in the mod folder's
PATCH-NOTES.md. Error sweep clean; all 6 records verified as the live load-order winner.
In-game test pending.

What it does:

1. **City attack** — add an always-false condition to node `WI_SetteCLNodeDragon` so it
   can never fire regardless of the MCM switch. Makes the fix permanent and
   save-independent instead of relying on an MCM setting per playthrough.
2. **Blades hunt** — add an always-false event condition to `WE_SetteBlades02` so the
   dragon-hunt roadside encounter never rolls. `WE_SetteBlades01` "Blade vs Thalmor"
   is untouched and still fires under the same Blades toggle.
3. **Soldiers** — add `GetStageDone(15) == 0` to the two "I am happy to help." responses
   (F737C9 / F737CA and the Sons equivalents). When the patrol's target is a dragon nest
   the join option simply doesn't appear; the decline line still does. The bandit and
   animal missions are unaffected.

Risk class: conditions-only, additive, no records deleted, no NPCs touched, no leveled
lists touched. No Reqtificator re-run needed (no NPC, no item, no spell records).
Reversible by disabling the plugin.

## Alternative with zero file changes

MCM only:
- "WI: Dragon Events" OFF — kills event 1.
- Blades faction encounters OFF — kills event 2, and also loses "Blade vs Thalmor".
- Soldier quest intros OFF — kills event 3, and also loses the bandit/animal missions.

Or: leave events 2 and 3 on and just decline them in dialogue. They never spawn a dragon
unless you say yes.
