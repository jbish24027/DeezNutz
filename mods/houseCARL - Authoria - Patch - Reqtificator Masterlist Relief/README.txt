Authoria - Patch - Reqtificator Masterlist Relief   (2026-08-21)

THE PROBLEM
The Reqtificator's output may name at most 254 plugins as masters. Installing Improved Follower
Dialogue - Lydia pushed the build to 255 (its plugin defines NPCs and a weapon the patcher rebalances),
so the export failed. Nothing was wrong with the load order; it simply crossed a hard cap.

WHAT THIS PATCH DOES
It carries, verbatim, the Reqtificator's own 07:15 result for 893 records - 844 armour, 38 weapons,
8 containers, 3 doors - belonging to 39 plugins that nothing else in that output points at. With those
records already in their finished state, the patcher's passes decline to touch them, writes nothing for
those plugins, and stops naming them as masters. Expected: 255 -> 212.

Nothing changes in game. Every value in here is the value the patcher already produced and that the
build already uses.

*** HOW IT ACTUALLY WORKS - READ THIS BEFORE REBUILDING ***
It is NOT true that the Reqtificator compares before and after and skips unchanged records. It has no
such comparison. Its transformers call Modify() unconditionally, and the exporter writes every record
a transformer touched. (Proof: WeaponCriticalDamageScaling always sets Critical.Damage = base damage;
feed it its own output and all 1695 weapons are rewritten unchanged.)

This patch works for a narrower, verified reason - each relevant pass has a PRECONDITION that the
finished values fail:
  * armour rating   - ArmorRatingScaling only fires when the rating is at or below Requiem's threshold
                      for that armour type and slot. The stored ratings are already above it.
  * armour keywords - the keyword rules are guarded by "none of these keywords present". They are.
  * containers/doors- CustomLockpicking only fires when a script named REQ_LockpickControl is absent.
                      The copied records already carry it.
  * weapons         - value matching does NOT protect weapons. They are protected by an explicit skip:
                      all 38 carry RFTI_Exclusions_NoDamageRescale + NoWeaponReachRescale +
                      NoBowSpeedRescale, and the Reqtificator build this list uses (the Authoria tweak
                      build, NOT stock Bugfix Pack 2) skips a weapon carrying all three.
  * 16 armours      - listed in relief-manifest.json under keyword_applied. Their ratings sit at or under
                      the threshold, so they were additionally given RFTI_Exclusions_NoArmorRatingRescale.
                      Five of them (hair ribbons) were a live bug: the next run would have taken them
                      from 21.3 to 88.29.

So: NEVER build the next relief patch on "the values already match". Build it on preconditions and
explicit skip keywords, and re-verify per record type.

LOAD ORDER - LOAD-BEARING
Last plugin before Requiem for the Indifferent.esp. The patcher reads only what loads before its own
output, so below it this patch is completely inert; above the other pre-output overrides, or the patcher
sees someone else's values and writes anyway. Currently registered exactly there in the CS profile.

DELIBERATELY EXCLUDED
Vindictor Armor and the DDV Arcane Fencer (their Authoria Requiem patch was edited after the 07:15 run,
so the stored values could be stale), RB's Scout (its arrow has no no-rescale keyword and would be
scaled twice), DynDOLOD (tool output), and every plugin the output merely references.

UPKEEP - when this goes stale it FAILS SAFE (the plugin just reappears as a master; nothing breaks)
  * After any Requiem or Bugfix-Pack update: the armour keyword rules live in
    ArmorKeywordAssignments_Requiem.esp.conf. If an update edits it, all 844 armours can silently become
    writes again. Re-check.
  * The weapon half depends on the Authoria Reqtificator tweak build winning the file conflict against
    Requiem 6.0.2 - Unbroken Road Bugfix Pack 2. If the tweak mod is disabled or loses that fight, the
    stock binary has no weapon skip and 10 plugins return as masters (worst case ~224, still under 254).
  * If one of the 39 source mods is updated or reinstalled, rebuild its share from the fresh output.
  * Rebuild recipe: houseCARL forward_record from Requiem for the Indifferent.esp using the record list
    in relief-manifest.json, then re-add the exclusion keywords listed there.

NOT VERIFIED BY A RUN
Every number above comes from reading the 07:15 output, the failure log, the shipped configs and the
Reqtificator's own source. The patcher was not run. The master count is only settled by the next export.


AMENDED 2026-08-27 - SACRILEGE REMOVED
Sacrilege was swapped out for Everdamned. This patch carried one Sacrilege record (CONT 1A81F1
SQL_CheatChest_Container, a debug chest) purely to keep Sacrilege off the Reqtificator's master
list. With Sacrilege gone the declared master became a hard game-start blocker ("masters for some
plugins are not enabled"). The record was removed IN PLACE and the orphaned master pruned:
masters 50 -> 49, records 893 -> 892. relief-manifest.json updated to match; rebuilds must NOT
re-add that record. Backup of the pre-edit file: *.esp.bak-everdamned-20260827.
NOTE (pre-existing, unchanged by that edit): three plugins now sit between this patch and
Requiem for the Indifferent.esp - Authoria - Patch - New Weapons - Requiem.esp, Authoria -
Vibrant Weapons - New Blades.esp, Authoria - Starting Kit.esp. If any of them overrides a weapon
or armour this patch carries, the patcher sees their values instead and that plugin returns as a
master. Worth a check before the next export.
