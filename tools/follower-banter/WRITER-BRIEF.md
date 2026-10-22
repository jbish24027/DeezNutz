# Writer brief (shared by every banter writer job)

You write voiced party banter for a Skyrim follower-banter mod. Plain text only; you never touch the game, MO2, `profiles\`, `mods\` or `ModOrganizer.ini`.

Folder: `C:\1. AUTHORIA\_tools\follower-banter\` (call it BANTER).
Scripts: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\`. Trigger rows: `BANTER\triggers\`.

## Read first (in this order)
1. `BANTER\STYLE-GUIDE.md` in full - the rules. Obey them exactly.
2. `BANTER\TRIGGERS.md` sections 4-5 (gate names and the trigger-row format).
3. Your part-1 script in full (`<nn> <NAME>.txt`) and its trigger file `BANTER\triggers\<nn> <NAME>.md` - copy their formats exactly; do NOT repeat their topics, jokes or set-ups.
4. The bibles in `BANTER\research\bibles\` for the speakers you use, plus the research file named in your job, plus `research\triggers\vanilla_gates.md` / `kaidan_block.md` / `others_block.md` for gates.
5. A finished part-2 file for reference format, e.g. `32b THIEVES GUILD 2.txt` and `triggers\32b THIEVES GUILD 2.md`.

## Key facts (also in STYLE-GUIDE)
- Player = LUNA (she/her), a nerdy scholarly mage, dry, quick, warm underneath. She speaks in about ONE THIRD of talks. Never call her "the Dragonborn" unless gated after she learns it. Models of her humour: NP16 and NP21 in `41 FAMOUS NPCS.txt`.
- Kaidan has NO beard; his Dagon-cult past only very late; he would never say anything like "a man can keep a spare". Gore is NOT attracted to Farengar. Redcap is a riekling (never "goblin"), one word per sentence, calls Luna "Friend", no crush.
- Rivals (Kaidan, Gore, Val, Serana, Ashe): rivalry grows with romance stage.
- Never collide with any follower's scripted quest scenes; Kaidan's KaiComp (Companions content) must not be contradicted.

## Output
- Write the script to `Notes and Files\FOLLOWER BANTER SCRIPTS\<nn>b <NAME> 2.txt` and trigger rows to `BANTER\triggers\<nn>b <NAME> 2.md`, continuing the prefix numbering given in your job.
- If the file already exists, read it and continue from the last ID instead of redoing.
- Then run: `python "C:\1. AUTHORIA\_tools\follower-banter\qa_check.py" "<your script path>"` and fix every flag; then `python "C:\1. AUTHORIA\_tools\follower-banter\dup_scan.py"` and fix any repeated line that involves YOUR new IDs (change your line, not older files).
- Do NOT edit MANIFEST.md or any other file. Report back in 3 lines: file paths, talk count + ID range, Luna %, flags left (should be 0).
