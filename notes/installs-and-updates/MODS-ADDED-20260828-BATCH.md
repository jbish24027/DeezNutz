# Batch add/update — 2026-08-28

15 archives handed over. Four were already installed. Seven were updates. Four were new mods.
MO2 was closed the whole time, so the plugin census below is trustworthy.

Backups: `_backups\2026-08-28 - batch add-update\` (whole mod folders, plus the stale PG sign
meshes I removed). Profile files: `*.bak-batch-20260828` in all six profiles.

---

## Nothing to do (4)

| Archive | Why |
|---|---|
| CRDW AE 1.1.5 | Byte-identical to what's installed. Already the current file on the page. |
| Nirn Necessities PBR 1.0 | Byte-identical. |
| Sonders Raysense Wall Leaning 1.0 | Byte-identical. |
| Kaidan Wig Slot 44 Patch | **Do not install this one.** It is a re-packaged copy of the houseCARL patch as it was generated on 08-15, before I ESL-flagged it on 08-17. The ESP in the archive matches `Kaidan Wig Slot 44 Patch.esp.bak-pre-eslflag-20260817` byte for byte. Installing it would flip the plugin back to a full slot. |

## Updated in place (7)

| Mod | From → to | What actually changed |
|---|---|---|
| SkyPatcher | 6.4.2 → 7.0.3 | DLL + PDB only. The shipped `SkyPatcher.ini` is unchanged, so no settings were lost. 7.0.0 was a big rewrite (much faster load), 7.0.2 fixed `filterByArmorTypes=light` never matching light armour, plus crash safeguards. |
| OAR - RaySense | 1.1 → 1.2.0 | New `RaySense_Ledge` condition + Skyrim 1.7.99 support. The INI gains a `[Ledge]` block and changes nothing else — your old values were all stock defaults. ESP is still ESL. |
| Smooth Terrain | 0.2.0 → 0.6.0 | Four releases at once. New micro-LOD system (`iSmoothedQuads=3`, `iGradientStep=2`), `fSmoothness` removed (always 1.0 now), VR support, 1.7.99 support, and 0.5.0's collision update reverted in 0.6.0. Your INI was stock, so nothing custom was lost. |
| DynamicShader Core | 1 → 2 | DLL only. No changelog published. |
| DynamicShader-DynamicSnow | 1 → 2 | DLL, plus a new `DynamicSnow.ini` that v1 didn't ship. It sets `MaxFootprints=100` (author's comment says the default is 400 and that above ~400 the per-stamp rebuild goes from ~5 ms to ~10 ms). Raise it if the trail is too short. |
| Asherana banter patch | 1.0.8 → 1.0.10 | You were actually on 1.0.8 despite the folder saying 1.0.7 — the author mislabelled that upload. 1.0.9 added a per-conversation seven-day cooldown to every repeatable radiant banter; 1.0.10 added the one it missed ("A Moment's Rest"). The author also **pulled** the Slower / Much Slower Cooldown optional patches as incompatible — neither was installed here, so nothing to remove. |
| IDE Jorrvaskr | 1.0.1 → 1.0.3 | Fixes toasts that could not start after a previous one ended badly. One new script (`IDJO_Player0101Script`). `Authoria - Reqtificated - IDE Jorrvaskr.esp` still lines up: its single override, `000BD0 aaJorBackupToast`, exists unchanged in 1.0.3. |

## New (4)

**Immersive Dialogue Expansion - Dawnguard and Vigilants** (ESL, 581 records)
Sits right below IDE Jorrvaskr in both the mod list and the load order. All 14 NPCs are new, so
no facegen fight with any NPC replacer. It does override 10 vanilla cells and carries lighting
data with them — but it loads at ~897 and Lux.esp is at ~3000, so Lux still wins the lighting.
One vanilla placed object (`0F9626`) gets disabled; nothing later touches it, so that sticks.
BUVARP isn't installed, so the one documented incompatibility doesn't apply. Ships its own SEQ.

**Beam Walking Assist 1.3** (ESL + `BeamWalking.dll`)
With the RaySense animation cluster. Needs OAR 3.0.2+ (you're on 3.2.0) and RaySense, which is
why it pairs with that update. OAR priorities 2110000080–2110000090 — nothing else in the list
uses that band. `Beam Walk.esp` defines two globals and masters Skyrim.esm only.

**iLluminous Elementals 1.1.4** (Light Placer configs, no plugin)
All 16 base options installed: four atronachs, four spriggans, ash spawn, bone horse, chaurus,
magic anomaly, ice wraith, wisp, wispmother, flame familiar. The Mod Support step was skipped
entirely — none of the mods it supports (Arclight, Atronach Matriarchs, EDMR, Flamekin, the 15
Mihail creatures, Natura Spriggans, Spriggan/Wispmother Variance) is installed.

Two things I had to fix:
- Its `Wispmother.json` ships with 16 ideographic spaces (U+3000) used as indentation. That is
  not legal JSON whitespace, so Light Placer would have thrown the whole file out and wispmothers
  would have stayed dark. Replaced with ordinary spaces. **This will come back on the next update.**
- Per your call, iLluminous now owns the three vanilla atronachs. `Authoria_Glow_Atronachs.json`
  was cut back to the two creatures iLluminous does not cover: the Bruma cold-flame atronach and
  the Dawnguard Ancient Frost Atronach. Old version kept beside it as
  `.bak-pre-illuminous-20260828`.

**WiZkiD Diverse Blacksmith Signs 1.2** (4K main, no plugin)
Above Skyking Signs so it wins the four meshes. Your picks: Riverwood bellows, Whiterun horseshoe,
Riften bellows, Windhelm key. You named both the key and the anvil-and-hammer for "the others" but
Windhelm was the only town left, so I took the key — the author's own screenshot for that model is
shot in Windhelm. Swapping it to the anvil is a one-file copy if you'd rather.

Two conflicts handled:
- The archive ships three cubemap stubs (4 KB each) at paths already served by Custom Cubemaps by
  fadingsignal (1 MB) and Forgotten Retex Project (8.5 KB). I dropped WiZkiD's copies. The signs
  still get their reflections from the better files, and every other iron object keeps its.
- Both PG Output folders held ParallaxGen'd copies of the Riverwood and Windhelm signs, built from
  the old Skyking meshes, and PG Output sits at priority 40. Those two would have kept showing the
  old sign. Removed the four stale files (backed up). All four signs now resolve to WiZkiD in both
  CS profiles.

**State of the signs as installed — no generator run involved, none needed.** Everything WiZkiD
authored is complete in the mesh: the metal carries env maps in slots 4/5, Riften already has
`RiftenCanalWood01_p` in slot 3, Windhelm already has `pole01_p`. Two shapes sit without parallax —
the Riverwood beam (`WoodPost02`) and the Whiterun beam (`WRWoodBeam01`) — and on the PBR profile
the `metalwork01_brown` chains render non-PBR. That is the whole delta. Nothing is missing or
broken, and it is not worth acting on.

---

## Where things landed

Deployed to all six profiles. iLluminous is listed **disabled** in the three profiles that have no
Light Placer at all (Requiem Reforged Main, Requiem Reforged NSFW, DEEEZ NUTTZZZ) — listed rather
than omitted so MO2 can't drop it in at a random priority on next launch.

Plugin cap: **230 full plugins**, unchanged. Both new plugins are ESL-flagged.
Active plugins went 4099 → 4101; enabled mods 3960 → 3964.

`housecarl_check_errors` on the two new plugins plus the four touched ones: 0 dangling refs,
0 missing masters. (The two DBVO Fix plugins Mutagen can't parse were already excluded before
this batch — unrelated.)

All eleven archives were copied into MO2's own downloads folder with `.meta` files carrying the
right mod/file IDs, so `installationFile` resolves and the next update sweep can read them.
Every one verified CURRENT against Nexus at file level.

---

## Left for you

- **Smooth Terrain 0.6.0 is a real behaviour change**, not a bugfix bump. `iSmoothedQuads=3` limits
  full smoothing to a 3-quad radius with a gradient beyond it; 0.2.0 smoothed everything loaded.
  Worth a look at terrain in the distance on the first run.
- **DynamicSnow footprint trail** is capped at 100 by the new INI. Bump it in
  `mods\DynamicShader-DynamicSnow\SKSE\Plugins\DynamicSnow.ini` if the trail feels short.
- **WiZkiD also has a 2K optional file** on the page if the 4K textures are more than you want.
