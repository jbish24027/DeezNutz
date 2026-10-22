# Swimming Extensions (Svimex) 1.0.0 -> 1.0.1 + Pandora Cache - 2026-09-05

Nexus 189821. Two archives handed over, both now filed in `D:\1. MOD STUFF\1. SKYRIM FILES\animation` (the 1.0.0 archive
stays there too):
- `Swimming Extensions (Svimex) Swimming Overhaul 189821 1.0.1 2026-09-04T18-15Z PuQ2UKIiL.zip` (file id 800258)
- `Svimex Pandora Cache 189821 1 2026-09-04T18-15Z CmfxYjdyh.7z` (file id 800259)

MO2, the game and Pandora were closed the whole time. Previous state: section 5 of
`MODS-ADDED-20260904-APC-ACCURACY-BACKPOCKET-SDS-SVIMEX.md` (installed 1.0.0, dormant).

Backup: `_backups\2026-09-05 - Svimex 1.0.0 pre-1.0.1\` - the whole mod folder as it was (144 files, verified by count
and byte total).

## What the two files contain

| Archive | Files | Against the 1.0.0 install |
|---|---|---|
| 1.0.1 | 236 | 143 byte-identical (all 11 animations, the plugin, the 131 behaviour-patch files) + **93 new** cache files under `Nemesis_Engine\mod\svimex\animationsetdatasinglefile\<Set>\*.txt` (34 female sets, 34 male sets, 25 first-person sets). Nothing changed, nothing removed |
| Pandora Cache | 3 | `animationsetdatasinglefile\DefaultFemale.txt`, `DefaultMale.txt`, `FirstPerson.txt` - flat lists of the new animation paths, the Pandora-format twin of the 93 Nemesis-format files |

The changelog for 1.0.1 is "I forgot to upload the animation caches, added now. Please re-run Nemesis / Pandora". The
cache file has no changelog.

## What was done

Both archives were overlaid into the existing folder `Swimming Extensions (Svimex)`, 1.0.1 first, then the cache.
No path exists in more than one of the three sources, so the author's "install the cache below the mod" has nothing to
order here and a separate folder (the `HorsePower - Pandora Cache` / `SkyParkour - Pandora Patch` pattern) was not
needed. Nothing in any profile changed: same folder, same plugin, same placement.

- Folder now holds 239 files plus `meta.ini`. Every file matches its archive by hash. The 143 original files are
  unchanged. `SwimmingExtensions.esp` is byte-identical to 1.0.0.
- No other mod ships anything under `Nemesis_Engine\mod\svimex`.
- `meta.ini`: version 1.0.1, the 1.0.1 archive as the installation file, both file ids under `[installedFiles]`
  (the same two-file layout as Simple Diving), notes rewritten. CRLF preserved.

## Still dormant until Pandora runs

The behaviour patch is complete now, but it is still not in the generated output. The last Pandora run in
`Authoria - Pandora Output - NSFW` is dated 2026-08-27, before Svimex existed. Until Pandora runs with the Svimex patch
ticked, only the first-person swim idle (the one file that replaces a vanilla animation) and the breathing-line plugin
are live. Sprint swimming, swim-enter and the first-person directional swims stay unreferenced.

Pandora is launched through MO2, so it is yours to run:

1. Launch Pandora from MO2 as usual.
2. Tick **Swimming Extensions - Swimming Overhaul** (the `svimex` patch; author Tsptds). Leave everything else as it is.
3. Run, with the output going to the existing `Authoria - Pandora Output - NSFW` mod.
4. Check `Engine.log` in that output for errors mentioning `svimex`.

`Authoria - Pandora Output - NSFW` is enabled in five profiles. The Main profile has every `- NSFW` output disabled and
no other Pandora output enabled; that was already the case before this update.

Simple Diving's patches touch the same swimming nodes. Same author, recommended together; Pandora merges them.
