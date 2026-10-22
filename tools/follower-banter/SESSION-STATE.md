# Follower banter - session state (2026-10-21, evening)

Read with: MANIFEST.md, STYLE-GUIDE.md, TRIGGERS.md, research\ (bibles, content, triggers), qa_check.py, dup_scan.py.
Scripts: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\` (+ 6 original files on the Desktop). Trigger rows: `triggers\`.

## Where it stands
- WRITING DONE: **9,231 talks**, all QA-clean (only old harmless title repeats left). User OK'd going past 8.5k.
- 10-21 added: the 9 cut-off part-2 files; 60 BEEING FEMALE FAMILY (BF1-100, needs Kaidan = father);
  11c LOTD 3 (LT241-390, Lucien/Remi/Xelzaz); 54b QUEST CROSSTALK 2 (FL201-320); 61 WANDERERS FAIR (WF1-60);
  53b RIVALRY 2 (RV201-300, early stage); 62 SOLSTHEIM BEFORE THE DLC (SL1-60); 63 KAIDANS PEOPLE (KP1-60).
- Edits 10-21: NP6 ("keep a spare" removed), NP9 rewritten (Gore is NOT into Farengar). NP16/NP21 = model Luna humour.
- Invented backstory in 63 for the user to vet (listed in its trigger file): Kaidan met Farkas over a broken table at the
  Bannered Mare; Tilma's stitched blanket; old sheep "Lady Horker" in Rorikstead; Brynjar left Kaidan with Mralki a winter;
  Xelzaz has heard Aryo's name.
- Each trigger file lists its [unconfirmed] gates - resolve at build time.
- Beeing Female: installed 10-21 (see memory beeing-female-install-20261021 and Notes and Files\BEEING FEMALE PLAN.txt).

## Voice tests BUILT 10-21 (waiting on the user's picks)
- `Notes and Files\BANTER VOICE TESTS\<Speaker>\` for 11 speakers: 3 real reference wavs ("0 - real voice N"), 5 lines
  (calm/funny/emotional/combat/short) x 3 takes, manifest.json; one `READ ME.txt` at the top.
- Reference clips (3 per speaker, 4-10 s, Whisper large-v3-turbo transcripts) saved for the full run in
  `_tools\follower-banter\voice-refs\<Speaker>\ref1-3.wav` + `voice-refs\chosen_refs.json` (wav, text, source file).
  Luna = the 2 Eleonora refs in `_staging\omnivoice-test-20261017\reference`.
- Voice types: Kaidan kaivoice (0Kaidan.bsa), Gore hd1gorevoice (loose), Val ax_valvoice (AX ValSerano.bsa),
  Remiel hlioremivoice (use "Remiel - Cleaned Audio" loose), Xelzaz bpufxelzazvoice, Inigo inigofollowervoice (.xwm),
  Lucien jrlucienvoice, Redcap fa01redcapvoice (loose; enough 4-10 s clips exist), Serana SDA dlc1seranavoice,
  Ashe mm_ashevoice (Ashe - Fire and Blood.bsa).
- Generator: `_tools\follower-banter\voice-refs\scripts\` (gen_tests.py, pick_refs.py, choose.py, test_lines.json, chosen_refs.json).
- Auto-QA: no take ends rising. Remaining "words" flags are Whisper mishearing (owt->out, Ashe->Ash, for->four).
- Spoken text: leading "..." dropped, "..." -> comma, quotes stripped, ALL-CAPS words -> Capitalised.

## User's voice-test picks (22 Oct) -> `_settings` in voice-refs\chosen_refs.json
- Ashe clip 1 | Inigo clip 1 (3 also good) | Lucien mixed: clips 3+2 | Redcap clip 1 | Remiel clips 1+2 |
  Serana clip 1 | Xelzaz clip 2 | Luna: all takes good (user 22 Oct), keep current setup.
- Kaidan: tone of clip 3, pace of clip 2 (clip 2 ran ~18% slower) -> clip 3 at speed ~0.85 (OmniVoice generate(speed=)).
- Val: clip 1, slower - testing speed 0.92 / 0.85.
- Gore: only 04 take 3 (clip 3 seed 42) close - testing clip 3 seeds 42/77 + new clips 4 (cand 13) and 5 (cand 6).
  Clip 4 made 2 rising endings even after reseeding.
- Retest batch: `Notes and Files\BANTER VOICE TESTS\RETEST\` (Val, Gore, Kaidan) + READ ME; made by scripts\retest.py.
  **No full run until the user OKs the retest.**
- **Retest picks (22 Oct, settled):** Val clip 1 speed 0.92 | Kaidan clip 3 speed 0.82 (user: line 01 lost a little
  accent when slowed - check accent early in the full run) | Gore new clip 4 + clip 3 seed 77 (clip 4 alone says
  "bow" right; clip 4 tends to end rising, keep QA reroll). **Full run still needs the user's go-ahead.**

## FULL VOICE RUN STARTED 22 Oct (user: "just go for it")
- Script: `_tools\follower-banter\voice-refs\scripts\run_full.py` (settings from chosen_refs.json `_settings`).
- Output: `D:\BANTER VOICE\<Speaker>\<TALKID>_<nn>.wav` (nn = line number inside the talk), log `done.jsonl` per speaker
  (spoken text, ref, seed, QA). Run log `D:\BANTER VOICE\run.log` (+ run-errors.log, mostly harmless warnings).
- 75,405 lines across 9,231 talks (79 files incl. the 6 original Desktop scripts). Order: Kaidan, Luna, Gore, Val,
  Lucien, Remiel, Inigo, Xelzaz, Redcap, Serana, Ashe. ~1-1.5 s/line -> ~25-35 h total.
- RESUMABLE: rerun the same script; it skips ids already in done.jsonl. PAUSE: create an empty file `D:\BANTER VOICE\STOP`
  (delete it before restarting). Runs as a detached hidden process, not tied to a chat.
  Launch via WMI (Invoke-CimMethod Win32_Process Create, cmd /c ... > D:\BANTER VOICEun-<time>.log): a plain
  Start-Process child died when the app restarted (22 Oct 08:16, no error). Two python.exe = venv launcher + child, normal.
- Text handling: *Sigh* -> OmniVoice [sigh] tag; other *stage directions* and (asides) removed; 131 lines that are only
  stage directions are logged as skipped. "bow" after the/a/my/... -> phoneme [B OW1] (weapon; the Gore fix).
  Retries up to 4 (alternating preferred clips, seed +100) until QA passes; flagged lines stay in done.jsonl with flags.
- Kaidan's accent in the full run: user checked 22 Oct, "they sound fine, keep going".
- Still owed: list of flagged lines for the user to hear (when the run ends).

## Next
1. User reads/marks files.
2. User listens to BANTER VOICE TESTS and picks per speaker; swap refs where a voice is off; then full generation.
3. Plugin build (split ESLs, controller per TRIGGERS.md, resolve [unconfirmed] gates).

## Cost note
A 100-200 talk writer costs very roughly 2-3% of a week.
