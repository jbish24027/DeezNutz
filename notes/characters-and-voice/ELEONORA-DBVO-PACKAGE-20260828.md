# Eleonora DBVO — the 2026-08-28 run, checked and split by mod

You were right that every line came from a mod. Chasing that found a mistake in how I
was building the filename, and correcting it changes almost every number I gave you
earlier. This file supersedes what I said before.

## The mistake

DBVO drops the trailing parenthetical tag before it looks a file up.
`Please don't leave, Xelzaz. (Persuade)` is voiced as
`Please_don't_leave,_Xelzaz..fuz`, not `..._(Persuade).fuz`.

Your pack proves it: of 2,239 topics that end in a tag, it holds the stripped name for
2,080 and the full name for 13.

I had been building the full name. Everything downstream was wrong because of it.

The rule, as it actually is:

1. Drop a trailing ` (…)` tag — only when a space precedes the `(`, so
   `you... (Persuade)` loses it and `you...(<BribeCost> gold)` keeps it.
2. Trim.
3. Space and `\ / : * ? " < > |` become `_`.
4. Append `.fuz`.

Everything else stays verbatim, curly quotes and ellipses included. Codified in
`_tools\eleonora-dbvo\dbvoname.py`.

## What actually happened

| | |
|---|---:|
| Live player topics in the load order | 47,512 |
| Covered before this run | 34,147 — 71.9% |
| **Covered after this run** | **46,736 — 98.4%** |
| New coverage from the run | 12,589 |
| Still missing | **776** |

12,589 of the 12,648 files you generated landed on a real topic that had nothing
before. Zero duplicates of files the pack already had. The run was close to a clean
sweep, not the two-thirds job I described.

### The 59 that did not land

- **27 mangled names.** The TTS pipeline turns non-ASCII into `_` and then drops a
  trailing `_`, so `I think it's good…` came out as `I_think_it_s_good.fuz`. DBVO
  matches the verbatim text, so those are silent. They are back under their correct
  names in the package. List in `_tools\eleonora-dbvo\renamed_nonascii.txt`.
- **31 with no home.** Editor leftovers — `AMQ06a`, `Enable_People`,
  `GetOwningQuest().SetStage(100)` — or lines the run truncated. In `_UNATTRIBUTED`.

### The 776 still missing

Topic files to re-run them, in your format, are in
`z. DBVO crap\topic files still missing 20260828-run2\` — 103 per-plugin files plus
`_ALL STILL MISSING deduplicated.txt`.

| Lines | Mod |
|---:|---|
| 223 | Sanguine's Trade - An Economy Mod |
| 70 | Skyrim.esm |
| 51 | Improved Follower Dialogue - Lydia |
| 45 | Beyond Skyrim - Bruma SE - Main |
| 30 | Serana Dialogue Add-On |
| 27 | Immersive Kaidan AIO |
| 24 | Unofficial Skyrim Special Edition Patch |
| 23 | Interesting NPCs 3DNPC |
| 23 | Val Serano |
| 22 | Ashe - Crystal Heart |

Those 70 Skyrim.esm lines are the only ones that are not from a mod. They are vanilla
topics no plugin overrides. They go in a folder called `Skyrim - Base Game`.

## The DBVO Fix plugins

**Yes, the existing 25 were honoured** — by resolving the load-order winner for every
dialogue string, so a topic a fix plugin rewrites is filed under the fix, with the text
the menu really shows. Running the `.pas` straight in xEdit would have written the
pre-fix wording.

**No new fix plugin was made, and the case for one is much weaker than I said.**

A fix plugin only ever rewrites topic text — move a leading `...` to the end, strip a
trailing space, fix a typo, split a semicolon, move a tag from the front to the back,
move an `<Alias=…>` token into a trailing parenthetical. That last move now makes
sense: putting the token in a trailing tag means the tag gets stripped and the filename
comes out clean.

With the tag stripped, only **368** topics still carry runtime markup, not the 889 I
quoted. The tag was the markup in most cases. Those 368 are **84% covered**, against
98% for ordinary lines — so there is a gap, but a small one. 58 of them are among the
776 still missing.

The `0x<FormID>___Broken___` naming is real — the Voice Pack Maker writes a
`BrokenTopicList<Plugin>.txt` (archive in `topic files\done\`) and there are 70 such
files in the pack. But it is a much smaller problem than I made it, and the FormID form
in the pack is inconsistent (masked local `0x3356` in some, load-order-stamped
`0x500591C` in others), so it is not something to generate blind.

## The packages

Both rebuilt on the corrected rule.

**Use this one.** `z. DBVO crap\Eleonora-DBVO-20260828-per-mod.zip` — 294 MB.

201 mod zips inside. Extract the outer zip anywhere — it holds single files, no
folders. Then extract whichever mod zip you want; each contains only:

```
Sound/DBVO/elnordvoice/*.fuz
```

Split this way because of path length. The longest filename is 176 characters, and
with a mod-name folder in the path too the total hit 245 — Explorer refuses at 260 and
throws `0x80010135: Path too long`. Moving the mod name into the zip's filename takes
the longest path to 199, so any destination up to 60 characters extracts with plain
Explorer.

Loose mod zips also on disk at `z. DBVO crap\Eleonora-DBVO-20260828-per-mod\`.

**The flat one.** `z. DBVO crap\Eleonora-DBVO-20260828-by-mod.zip` — 293 MB, the same
files as `<Mod Name>/Sound/DBVO/elnordvoice/*.fuz` in one tree. Needs 7-Zip.

Both contain:

- 200 mod folders, 13,130 placements. Biggest: Flint 52.3 MB, Amorous Adventures
  Rewritten 36.4 MB, Glenmoril 18.9 MB, M'rissi 18.1 MB, SDA 16.5 MB.
- Lines shared word-for-word between two mods appear in both, so every folder stands
  alone.
- `Skyrim - Base Game` — the vanilla Skyrim.esm topics.
- `_UNATTRIBUTED` — 31 files.
- `_MANIFEST.csv` and `_READ ME.txt`.

One thing to pass on: filenames must survive verbatim, curly apostrophes included.
Anything that straightens a quote makes that line silent.

## Scripts

`C:\1. AUTHORIA\_tools\eleonora-dbvo\`

- `dbvoname.py` — the filename rule. Everything else imports it.
- `attribute.py` — every winning player topic to its mod
- `attribute_fallback.py` — same over every plugin on disk, active or not
- `package_by_mod.py` — the flat zip
- `package_per_mod_zips.py` — the per-mod zips
- `gen_rerun.py` — the still-missing topic files
