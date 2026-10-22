# Authoria - Fair Companion Guard

2026-10-20. Script-only correction for The Wanderer's Fair / Gore - Vigilant.

The fair's companion aliases accept CurrentFollowerFaction membership. Gore's
start-game Vigilant quest adds all three story variants to that faction before
recruitment. Both entrance and exit then bring the uninvited actors to the player.

BringCompanions now checks the three original Vigilant placed references against
IsPlayerTeammate before moving them. The Gore recruitment controller sets that
state explicitly. Other actors retain the existing fair selection behavior.
The three excluded actors may still occupy finder slots; this targeted correction
prevents their travel but does not redesign the six-slot companion finder.

Manual recovery for the user's fresh test save ONLY:
  cqf SkyrimFairAudioQuest AuthoriaRestoreGores
This returns the three original placed references to their editor locations,
skipping missing, dead or currently recruited actors. It is never automatic.
It does not alter quest stages, factions, inventory, or enabled state.
Prefer a pre-fair save if available. In-game recovery and travel need user testing.

Source: prior decompilation of the winning SkyrimFairAudioScript.pex.
Original PEX SHA256: 21D750E084EACA361FFD8F698CDF6C42A57CF983522FBEDE19C45271D561D19E
SkyrimFairPassport.psc is a compile dependency only; its PEX is not replaced.
No plugins or generated outputs changed. No Reqtificator/Synthesis required.
DBReV/Eleonora, body conversions, Requiem content balance, and Seasons additions
are inapplicable: this changes only an existing travel script, adding no content.

Rollback: disable Authoria - Fair Companion Guard in MO2. The original script
remains intact. Backups and installation checks are recorded in SESSION-STATE.md.

## 2026-10-22: "The Wanderer's Fair" song skipped (user's request)
Both song players now skip the sung "The Wanderer's Fair" track and go straight to the next song:
- Scripts/SkyrimFairAudioScript.pex (stage, inside the fair): new AuthoriaSkipHatedSong() called in Advance() before
  Songs2[track].Play; compares against SOUN 050002:SkyrimFair.esp (track 0, 238.88 s).
- Scripts/SkyrimFairOutsideShow.pex (outside the walls, ref 030132): same check against SOUN 050005:SkyrimFair.esp.
Song lengths, singer lines and choreography follow the track index, so they stay in step. Sources in Source/Scripts
(and _staging/fair-song-skip). Backup of the previous stage .pex: _backups/2026-10-22 - Fair song skip/.
Also enabled in Authoria - Preset Studio - HPH on 2026-10-22 (was PICTA only).
