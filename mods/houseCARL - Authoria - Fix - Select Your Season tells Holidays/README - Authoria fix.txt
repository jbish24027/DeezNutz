Authoria fix, 2026-10-13 (houseCARL session).

Problem: Select Your Season sets the game date when you close its MCM, but never tells Holidays.
Holidays checks the date once at game start (it sees the default Last Seed 17 date) and then only
at about 1 AM in-game, so a new game started on a holiday date shows no decorations anywhere.

Fix: selectyourseasonskyuiconfig.pex rebuilt from the shipped source with one addition at the end
of ApplySettings(): it finds Holidays' quest (Holidays.esp 0x00F059) and calls its CheckDate(),
the same refresh Holidays' own MCM does on close. Everything else is unchanged (a rebuild of the
untouched source matched the shipped .pex: same 122 strings, same code size).

Built against compile-time stand-ins for SkyUI's SKI_QuestBase / SKI_ConfigBase (SkyUI ships no
sources); the game uses SkyUI's real scripts. Must sit ABOVE (win over) the Select Your Season mod.
Remove this mod to undo.
