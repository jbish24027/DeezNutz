# Authoria - Patch - IWE No Dragon Events

Built 2026-08-21 by Claude via houseCARL. ESL-flagged, form version 44, 6 override records,
5886 bytes. Masters: Skyrim.esm, Update.esm, Immersive Encounters.esp.

Purpose: remove every event in Immersive World Encounters that puts a live dragon in the
world, without removing the non-dragon content that shares the same encounters.

Load position: "Authoria - Custom Patches" group, directly after
`Authoria - Patch - IHSS - Horsepower.esp`, all 4 profiles. Anything after
`Immersive Encounters.esp` works — nothing else in the load order touches these 6 records
(every one was override_depth 1 before this patch).

## The three dragon events and what was done

### 1. Dragon Attack in a capital city — hard off
`WI_SetteCLNodeDragon` (919DA8), the story node that starts `WI_SetteCL03` "Dragon Attack".
Appended an eighth condition: `GetRandomPercent >= 200`. GetRandomPercent returns 0-99, so
the node can never pass. All 7 original conditions kept verbatim, including IWE's own
`SetteToggle_WIDragon` MCM gate — the MCM switch still exists, it just no longer matters.
Node `Parent`, `PreviousSibling` and `Quests` list preserved.

This event was the only one of the three that was not opt-in. It fired on entering a
location with LocTypeCity + LocTypeHabitationHasInn, riding vanilla's own settlement-dragon
timer via `WIs.updateWIDragonTimer()`.

### 2. Blades Dragon Hunt — encounter never rolls
`WE_SetteBlades02` "Blades On Their Way To Dragon Hunt" (0F8A8C). Appended a fifth
EventCondition: `GetRandomPercent >= 200`. The roadside encounter no longer spawns, so the
follow-up `SetteBladesDragonHunt` "Dragon Hunters" (9333F8) can never be offered.

`WE_SetteBlades01` "Blade vs Thalmor" is deliberately untouched and still fires under the
same `SetteToggle_WEFactionBlades` toggle. That is the whole point of patching the quest
rather than flipping the MCM.

### 3. Soldiers marching to a dragon's nest — join option hidden
Four DialogResponses under the two "I am happy to help." topics:
- Imperial: F737C9, F737CA (topic F737C8, quest C3004E)
- Stormcloak: 0A876C, 0A876D (topic 0A876B, quest C3004F)

Each got one appended condition: `GetStageDone(<owning intro quest>, 15) == 0`.

Why stage 15: both `TIF__05F737C9` / `TIF__05F737CA` / `TIF__050A876C` / `TIF__050A876D`
branch on exactly this — `If GetOwningQuest().GetStageDone(15) == 1 → QuestB.Start()
Else QuestA.Start()`. QuestB is the dragon-nest follow-up (F788D9 Imp / 0A876E Sons);
QuestA is the bandit/animal mission (F6E6A8 / 0A3649). Intro stage 15 is set only on the
dragon path; the non-dragon path uses stages 10 and 12.

Result: the patrol still spawns, still talks, and still offers its bandit and animal
missions. When its target is a dragon nest the "I am happy to help." line simply does not
appear. The decline line "I can't help you." (F737C5 and the Sons equivalent) is untouched
and always available, so the conversation never dead-ends.

## Safety notes

- Conditions-only and purely additive. No record deleted, no field overwritten, no list
  entry removed. Every original condition survives byte-for-byte.
- Every existing condition on all 6 records had Flags = 0 (ANDed, no OR chains), verified
  before writing — so an appended condition ANDs cleanly and cannot accidentally widen a
  group.
- No NPC, item, spell, leveled-list or container records touched. **No Reqtificator re-run
  needed.** Does not interact with `Authoria - Reqtificated - Immersive World Encounters.esp`.
- houseCARL error sweep: 0 dangling references, 0 missing masters, 0 unparseable records.
- Reversible: disable the plugin and all three events come back.

## What this does NOT do

- Does not touch vanilla dragon attacks on minor settlements, vanilla dragon lairs, or the
  main quest. Only IWE's own three events.
- Does not remove IWE's dragon-flavoured dialogue, bard songs, ghost combat taunts, the
  "farmer refugees after a dragon attack" camp, or the "collect 10 dragon bones/scales"
  fetch objectives. None of those spawn a dragon.
- Does not change the IWE MCM. "WI: Dragon Events" is still there and still toggles the
  global; it just has no effect now that the node can never pass.

Full pre-build audit: `IWE-DRAGON-EVENTS-20260821.md` in the instance root.
