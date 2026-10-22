# MFO — marth Follower Overhaul 1.0.66 + Synthesis patcher (2026-08-27)

Nexus 187445. FFXII-style gambit system for followers, SKSE DLL + ESL-flagged MFO.esp
(Skyrim.esm-only master, 5 new records, no overrides). Runtime only: edits no follower
records, no AI packages; acts on anyone flagged player-teammate.

## Install

- Mod folder: `mods\marth Follower Overhaul` — all 16 archive files verbatim, verified.
  No file conflicts with anything in the instance (all paths MFO-namespaced).
- Plugin: `MFO.esp` after `Quick Follower Commands.esp` (loadorder 308), group
  `Interface - User Interface`. All FOUR profile files updated in DEEZ CS NUTZ.
- Enabled in DEEZ CS NUTZ only; listed disabled in the other four profiles.
- Requirements verified: game 1.6.1170 (exactly what MFO supports), MCM Helper 1.6.2,
  po3 Papyrus Extender 6.4.2, Address Library 11. Progression Addon NOT installed.

## Deliberate settings delta (exclude-anyone-who-might-break)

MFO has NO per-NPC blacklist — eligibility is just "is a teammate", and every tracked
follower is auto-seeded with a default gambit kit that includes "Always → Loot
Equipment". Shipped 1.0.66 defaults have looting, follower economy (sell/buy), and
auto-retreat ON. That would fight SDA's Serana outfit lock, Ashe's curated gear,
Kaidan's wig/scalp, OES, and the UBE outfit lanes.

Set in BOTH `MCM\Settings\MFO.ini` (wins) and `SKSE\Plugins\MFO.ini` (seed), all
MCM-visible:

| key | shipped | ours | why |
|---|---|---|---|
| bLogistics | 1 | **0** | no looting/inventory touching at all |
| bEconomy | 1 | **0** | followers never sell/buy (log-only) |
| bAutoRetreat | 1 | **0** | no ambient combat repositioning |
| bMagicLoadout | 1 | **0** | casters never re-dress by school |
| bDollsMode | 0 | **1** | "Fashionrim": armor stays hands-off even if logistics is later enabled |
| bCommandTarget | 1 | **0** | MFO cannot steer who any follower attacks |
| iCastControl | 2 | **0** | MFO never overrides any follower's own spell choice |

## Why the exclusion is GLOBAL, not per-NPC (searched exhaustively 2026-08-27)

MFO has NO per-NPC exclusion outside the in-game board. Verified against the 1.0.68
source, not guessed:

1. **No config key.** The DLL parses exactly 84 keys; none is an actor/follower list.
   The only FormID-valued key is `xMerchantPerkID`.
2. **No data file.** It reads only `MFO.ini` (both layers) and `mfo_items.json` (the
   item catalog). No follower/exclusion file exists or is looked for.
3. **No Papyrus API.** The registered natives are the MFO_Trade economy bridge only —
   nothing that reads or writes a gambit, so no script can pre-author a board.
4. **The addon manifest is unrelated.** `MFO_AddonManifest` declares the Progression
   add-on's classes and economy globals; it cannot carry follower rules.
5. **No keyword / SPID / KID hook.** Eligibility is `IsPlayerTeammate` + a
   hard-compiled quirk table (Vilja/Tindra factions, Inigo's AV). Not extensible.
6. **The one real exclusion path is unsafe.** An actor whose `WaitingForPlayer` actor
   value is < -0.5 is invisible to MFO — but that AV *is* the vanilla wait/hold
   mechanism (MFO's own DESIGN.md calls it "the vanilla-sanctioned wait/hold"), so
   forcing it would break following itself. REJECTED.
7. **Board presets are roadmap, not shipped** (DESIGN.md §2030).
8. **Board state lives ONLY in the SKSE co-save**, so it is per-playthrough by
   construction and cannot be pre-authored on disk. Co-save surgery was considered and
   REJECTED: the .skse is shared with OES, whose outfit state is co-save-authoritative,
   so a bug there costs OES data — not worth it to save two board edits.

**Therefore the automatic new-game posture is:** every switch by which MFO could act on
a follower is off. On a new game nobody has authored gambits, so the only rules in
existence are the auto-seeded defaults — and with the above, those defaults cannot
touch anyone's gear, inventory, outfit, appearance, targeting, or casting. Serana, Ashe
and everyone else are hands-off from the first frame, with no board edits and no
per-save step. This also restores the author's own stated design ("everything ships off
or conservative"), which 1.0.66's shipped defaults contradict.

The only default-kit rule that still fires is "drink your own health potion below 30%",
which consumes a potion the follower already carries. Harmless and vanilla-like.

## Hotkeys

MFO binds very little. The board is NOT a hotkey — it opens by casting the **Field
Orders** lesser power (Powers menu, shout/power key).

| Key | What | State |
|---|---|---|
| Field Orders power | opens the gambit board | live |
| `[` | focus fire: order all followers onto what you are attacking / aiming at | inert until Commanded targeting is ON |
| `;` / `'` | dev probe / dev harness | inert (both gated off, and not in the MCM) |

**Backslash collision, found and fixed.** MFO's focus key defaults to backslash (DIK 43)
— which is exactly Campfire's `hotkey_build_campfire` in
`Authoria - MCM and INI Settings\SKSE\Plugins\CampfireData\Profile1.json`. MFO
deliberately does NOT swallow the keypress, so pressing backslash would have fired BOTH:
the focus-fire order and Campfire's build menu. Rebound to `[` (DIK 26) in
`SKSE\Plugins\MFO.ini`, verified unbound across every readable config in the load order
and the overwrite folder. `]`, `-` and `=` are taken (Dirt and Blood wash-followers /
tent pitcher, Optimal Potion Hotkey, ENB editor). `iFocusKey = 0` disables it entirely.
It is INI-only — there is no MCM entry for it.

Inside the board it is mouse + controller (A / B / R1); no extra keyboard binds.

## Turning MFO on, later (opt-in, in the MCM)

When you actually want to use gambits:
1. MCM -> Combat & Casting: set **Cast control** to "Ignore heals" and turn
   **Commanded targeting** ON (needs a game restart to arm the hook).
2. THEN, before that session, exclude the fragile ones on the board: Field Orders ->
   pick Serana / Ashe (and any other) -> replace their rules with a single
   **Always -> Wait** in BOTH the combat and logistics lists.
   Do NOT leave a board empty: a record with both tables empty is re-seeded with the
   default kit on the next load (`Serialization.cpp` backfill). One Wait rule blocks it.
3. Logistics/economy/Fashionrim can stay as set — those are the gear-breaking vectors.

Per-NPC exclusion is NOT possible outside the in-game board — see the section below
for the full search. The switches above are the exclusion, and they apply to everyone
automatically from the first frame of a new game.

## Synthesis patcher

- Git patcher added to pipeline group `Authoria - Output - Synthesis Gameplay`
  (last, nickname `MFO.Synthesis`): repo `github.com/marthofdoom/MFO`, project
  `installer\MFO.Synthesis\MFO.Synthesis.csproj`, branch main pinned at
  `5cf5f2c` (2026-08-27 tip; `MFO.sln` now exists — the README's broken-onboarding
  trap is fixed upstream).
- Versioning **Match** (its own Mutagen 0.54.2 / Synthesis 0.36.5), NOT the profile's
  manual 0.53.1/0.35.5 pins.
- It writes ONLY `SKSE\Plugins\MFO\mfo_items.json` (item catalog: potion restore
  types, ammo class, jewelry, never-loot list; schema 1 = matches the 1.0.66 DLL).
  Adds zero records to the group output. Under VFS the JSON should land back in the
  MFO mod folder (file exists there) — check after the run. Re-run Synthesis after
  load-order changes to refresh the catalog; without it the DLL uses runtime
  heuristics + shipped fallback.

## Outfit Wheeler event (found during install)

The live `overwrite\SKSE\Plugins\PrismaOutfitWheel.json` was MISSING (vanished some
time after the 08-23 recovery; not caused by this install). Rebuilt: seeded from
`_backups\...bak-20260822-113521`, then `--reindex --apply` → 77/77 rewritten,
`--calibrate` → 77 match / 0 mismatch against the new order (MFO.esp included).
Any outfit edits made in-game after 08-23 noon are not in it (none known).

## Open flags

- MCM slots: ~126 of SkyUI's 128 after MFO. If "marth's Follower Overhaul" never
  appears in MCM, the cap is the first suspect — the 08-19 cut list has 5 verified
  clean cuts ready (VioLens, OBody NG menu, Bow Rapid Combo, AYOP Thane, LotD debug).
- Reqtificator rerun still pending from the weapons batch. MFO does not add to it
  (no Requiem-facing records, masters nothing but Skyrim.esm).

Backups: `backups\mfo-install-20260827-131733` (all 4 DEEZ CS NUTZ profile files,
other profiles' modlists, PipelineSettings.json).
