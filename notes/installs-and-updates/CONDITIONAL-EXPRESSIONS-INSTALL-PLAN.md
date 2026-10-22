# Conditional Expressions — inspection and install plan

Date: 2026-08-28. **Status: INSTALLED** — see section 8 for what actually shipped.
Profile inspected: `DEEZ CS NUTZ - PBR`. Deployed to all six profiles with MO2 closed.

Two archives were handed over:

- `Conditional Expressions-45148-1-29-1755293339.rar` — the **original** mod by JaySerpa, v1.29.
- `Conditional Expressions Extended 91438 2.2.1 ... .zip` — **CEE** by crajj, v2.2.1.

---

## 1. Short answer

Install **CEE 2.2.1 only**. Skip the 1.29 rar.

CEE ships a complete replacement: its own plugin, its own scripts, its own MCM art,
translations and sounds. The only two files the old rar has that CEE does not are
`Condiexp_RandomFrostbite.pex` and `CondiExp_RandomVanilla.pex`. I checked every CEE
script and every compiled CEE .pex — **nothing references either one**. They are dead
code from the old random-expression system that CEE replaced with JSON presets.

Nexus lists the original as a requirement, and the author's own install note says
"alongside **or instead of**". Instead of is the clean read here. If anything ever acts
up, dropping the old mod in underneath CEE costs nothing and breaks nothing.

For UBE and followers specifically: **this works, with three real things to settle.**
They are in sections 4, 5 and 6.

---

## 2. What it costs the list

| Thing | Cost | Headroom |
|---|---|---|
| Full plugin slot | **none** | plugin is already ESL-flagged (form 44, flag 0x200) |
| Light plugin slot | 1 | ~236 free |
| **MCM slot** | **1** | **~125 of 128 used** — this is the tight one |
| Mod entry | 1 | — |

The plugin declares Skyrim, Update, Dawnguard. It defines 94 records and **overrides
nothing** — 46 globals, 15 magic effects, 14 sound descriptors, 14 sound markers,
2 quests, 2 form lists, 1 spell. No conflicts with anything in the list are possible.

The MCM slot is the only real cost. The 08-19 census put you at about 125 of SkyUI's
hard 128. CEE's menu script extends `SKI_ConfigBase`, so it takes one. That still fits,
but it is one closer to the wall.

---

## 3. Requirements — all met except one optional

| Requirement | Status |
|---|---|
| **Mfg Fix NG 1.0.7+** | ✅ you have 1.0.9, and it wins over the old Mfg Fix |
| **PapyrusUtil SE/AE** | ✅ installed |
| **SkyUI** | ✅ `SkyUI_SE.esp` active |
| **BEES** | ✅ not needed — you are on 1.6.1170, ESL is native |
| po3 Papyrus Extender | ✅ installed (optional, gives better random timing) |
| Original CE 1.28+ | see section 1 |
| **Audio Util** | ❌ **not installed** (optional) |

On Mfg Fix: you have both `Mfg Fix NG` and the old `Mfg Fix` enabled. NG sits at higher
priority, so NG's DLL wins. That is what CEE needs — it calls `MfgConsoleFuncExt`
functions that only NG provides. The old Mfg Fix is fully shadowed and harmless.

On AudioUtil: CEE's own notes say the AudioUtil path is player-only in practice, and
every call is guarded. Without it, breathing and sobbing fall back to the sound
descriptors inside CEE's own plugin. Nothing is lost but per-actor voice packs. Followers
use a silent breathing path either way. **Treat it as genuinely optional.**

---

## 4. UBE

### The population is smaller than you'd think

I asked the load order which actors actually sit on a `00UBE_*` race. The answer:

- **The player** (via the `00DZ*_...DZFemale01 / DZMale01` "Prisoner" race templates)
- **Lydia** — `HousecarlWhiterun`, on `00UBE_NordRace`
- **Serana** — `DLC1Serana` and both `SeranaMultiformNG` variants, on `00UBE_NordRace`

That is it. Kaidan, Lucien, Inigo, Auri, Xelzaz, Remiel, Eleonora and every vanilla NPC
are on ordinary races and use the vanilla head meshes. So everything below about UBE
applies to you, Lydia and Serana. Everyone else is on the normal path.

### CEE will find UBE actors correctly

CEE's NPC quest picks actors with a `HasKeyword ActorTypeNPC` condition. I checked every
UBE race record — **all of them carry `ActorTypeNPC`**. Lydia and Serana will be picked up
like any other NPC. No patch needed.

### The expressions come from UBE's own morph files, not from EFA

This is the part worth knowing. UBE's head parts point at its own tri files:

```
!UBE\Head\femaleHead.tri
!UBE\Brows\femaleheadbrows.tri
!UBE\Lashes\EyeFemaleLashes.tri
!UBE\Mouth\mouthhumanf_tangent.tri
!UBE\Eyes\eyesfemale.tri
```

**Expressive Facial Animation only ships vanilla paths** (`actors\character\character
assets\FemaleHead.tri` and friends). It does not touch any UBE actor. Same for MFEE's
stock mapping list. So the face quality you get on you, Lydia and Serana is whatever UBE
baked, not EFA's improved set. This is already true today — CEE does not change it. It
just means the three UBE faces will read slightly differently from the rest of the cast.

**Can EFA be ported to UBE?** Investigated 2026-08-28. Short answer: not by installing
anything, and no port exists on Nexus under any search phrasing. EFA is authored for the
996-vertex vanilla head; UBE's is 11,498 vertices and a different sculpt. EFA's own page
says non-vanilla meshes need a third-party patch the author does not supply. MFEE cannot
bridge it either — it is add-only, in a namespace no game event can reach, by its author's
own statement.

But measuring every morph on both, **UBE is not weak.** Median UBE/EFA ratio is about 0.9,
and UBE is *stronger* on anger (1.9–2.2x), puzzled (1.8–2.7x), squint (2.2x), brow-in
(1.9x), disgusted and fear. A straight EFA port would make several expressions worse. The
real gaps are narrow: eyelid gaze-follow (0.17–0.23x), surprise (0.23–0.45x), happiness
(0.39–0.65x), brow-raise, and a few phonemes.

Those gaps are now fixed by **`Authoria - Fix - UBE Expression Strength`** (built
2026-08-28), which raises only those morphs' multipliers. See that mod's README. Three
things it cannot fix, because they have no delta data to scale at all: brows on blink,
brows on look up/down, and 43 of the 49 morphs on UBE's eye mesh.

MFEE does have full UBE coverage in your list, via two ini files that map UBE's tri paths
to extension morphs — one in `Authoria - Ostim tweaks and Patches`, one in `PPA`. Those
extensions **append** morphs past the base set, so CEE's indices 0–31 are untouched. CEE
behaves identically whether MFEE is on or off. Worth noting because MFEE is disabled in
the Main Profile and enabled in the other five — that difference does not matter here.

UBE is female-only. Male actors on a UBE race fall back to vanilla head parts, so they get
EFA normally.

### UBE No Combat Expressions — the one real interaction

You have `Ultimate Body Enhancer - No Combat Expressions` enabled in all six profiles. Its
own Nexus page warns about Conditional Expressions by name.

I diffed its tri files against stock UBE. It is doing exactly what it claims — one large
zeroed block near the end of the morph table, which is the combat-anger morph, plus
re-quantisation noise elsewhere. It covers all four face parts, and because every one of
UBE's ~17 lash variants shares the same `EyeFemaleLashes.tri`, the lash coverage is
complete too.

Here is the collision:

- CEE's NPC loop calls `SmoothSetExpression(act, 15, 35–80)` when an actor is in combat.
  **15 is Combat Anger** — the exact morph NCE deleted.
- On Lydia and Serana that morph is gone, so nothing renders. The script still runs,
  including a hard `Utility.Wait(5)` per actor per cycle, for no visual result.
- On every **vanilla-race** NPC — guards, bandits, Kaidan, Lucien — the morph is present,
  so CEE's combat anger **will** show. NCE does not cover them.

So you end up with an asymmetry: your UBE trio stays neutral in combat while everyone
else gets angry faces.

**Recommendation: turn CEE's combat expression off** (MCM → *Less Dramatic Combat
Expression*). It costs you nothing you are currently getting, it makes the whole cast
consistent with the choice you already made by installing NCE, and it removes a 5-second
blocking wait per NPC per combat tick.

If you'd rather keep angry faces on the general population, leave it on and accept that
Lydia and Serana won't participate. Both are valid; the toggle is one click either way.

---

## 5. Followers

### "Followers" is a misnomer — it means the 16 nearest NPCs

CEE's follower quest has 16 optional reference aliases plus one for the player. Each alias
fills on: *closest matching ref in loaded area*, not swimming, not dead, not talking, not
disabled, not a child, within **2000 units**, and has `ActorTypeNPC`.

There is **no follower faction check and no whitelist**. It grabs whoever is nearest. In
Whiterun market that means sixteen townsfolk. Out on the road with two followers it means
your two followers and fourteen empty slots.

Consequences:

- **Every custom follower works with zero setup.** Kaidan, Lucien, Inigo, Auri, Xelzaz,
  Remiel, Eleonora, Val Serano, IFD Lydia, SDA Serana — all covered automatically.
- **Cities are the load spike, not follower count.** Sixteen actors each running a poll
  loop plus `Utility.Wait` calls.
- The *Register followers* hotkey just resets the quest so aliases re-fill. Use it after
  swapping companions. It also re-fills on game load, and automatically whenever you move
  more than 300 units.

Given the size of your list, **start `Update interval NPCs` at 6–8 seconds rather than the
default.** You can walk it down later if it feels sluggish.

### Your follower stack is otherwise clean

`Simple Follower Framework` and `marth Follower Overhaul` handle AI and outfits. Neither
touches facial morphs. No interaction.

DBVO is a genuine plus here. CEE 2.2.1 uses `MfgConsoleFuncExt.GetPlayerSpeechTarget()`
and `IsInDialogue()` — SKSE-level checks that work whether or not a dialogue menu is open.
That is exactly the case DBVO creates. Older Conditional Expressions could not see DBVO
conversations and would animate over them. CEE can.

---

## 6. Four conflicts to settle before install

### 6a. CEE ships its own `mfgfix.ini` — decide who wins

CEE includes `SKSE\Plugins\mfgfix.ini`. So do Mfg Fix and Mfg Fix NG. I diffed CEE's
against NG's. **Exactly one line differs:**

```
Mfg Fix NG:   fTrackEyeZ = 40.000000     (stock — the whole NG ini is stock)
CEE:          fTrackEyeZ = 50.000000     (comment claims default 20.0; it's stale)
```

That is how high NPCs aim their eyes when tracking. It is global — every MFG eye track in
the game, not just CEE's.

**Recommendation: delete `SKSE\Plugins\mfgfix.ini` out of the installed CEE mod** and let
Mfg Fix NG keep owning it. Your stack is tuned around NG's stock values. This also frees
CEE's mod position from mattering at all.

If you'd rather try the author's value, keep the file and put CEE at higher priority than
Mfg Fix NG. It's a one-line revert either way.

### 6b. Blinking Player Eyes vs CEE's blink modifiers

You have `Blinking Player Eyes` (SKSE DLL, player only). CEE's own docs warn that writing
modifiers 16/17 (BlinkLeft/BlinkRight) **stops the eye blinking** for as long as they're
held.

I read all five JSON presets. Blink modifiers appear in:

| Preset | Entries using 16/17 |
|---|---|
| `Expression_Random.json` | female2, male2 |
| `Expression_aroused.json` | female2/4/6/7, male2/4/6/7 |
| `Expression_pain.json` | female3/4, male3/4 |
| `Expression_trauma.json` | female6/7, male6/7 |

`Random` is the one that matters — it's the idle expression that fires constantly. Two of
its seven entries hold your eyes shut and fight the blink DLL.

**Fix: zero indices 16 and 17 in `female2` and `male2` inside
`SKSE\Plugins\CondiExp\Expression_Random.json`.** Two numbers. The rest of that entry
(the brow-down squint) still plays. I can do this edit as part of the install.

Pain and trauma are short and rare, so leave those.

### 6c. Everdamned already drives facial expressions

`Everdamned` ships `ED_FacialExpression_Utils.pex` and `ED_FeedDialogue_SmileSpell.pex` —
it sets expressions during vampire feeding. CEE polls the same actors. Both write the same
MFG channels.

CEE registers for `dhlp-Suspend`/`dhlp-Resume` and for `ostim_start`/`ostim_end`, so OStim
scenes correctly pause it. **Everdamned's feed scenes are not covered by either.** If you
see the feeding smile flicker or get cut short, that is this. Not a blocker — something to
watch on the first vampire feed.

### 6d. PC Head Tracking uses the eye-look modifiers

`PC Head Tracking - MCM` drives modifiers 24–27 (LookDown/Left/Right/Up). CEE's trauma and
aroused presets use index 27. Both are features you'd want to keep, and both are off by
default in the plan below (section 7), so this is dormant unless you enable trauma. Noted
for completeness.

Also on the list and harmless: `Immersive Interactions` and the Skyrim's Got Talent bard
scripts both set expressions transiently. Both are short scenes CEE's dialogue guard
handles.

---

## 7. MCM settings — what to set and why

Based on what's actually installed in your list.

| Setting | Set to | Why |
|---|---|---|
| **Cold Detection** | **Frostfall** | You run Frostfall *and* SunHelm cold together. CEE can only read one. Frostfall's exposure global is a smooth 0–100 signal; SunHelm's is three coarse spell stages. "Automatic" would pick Frostfall anyway — set it explicitly so it can't drift. |
| **Less Dramatic Combat Expression** | **Off** | Section 4. Consistency with UBE No Combat Expressions, and drops a 5s blocking wait per NPC. |
| **NPCs Support** | On | The whole point — and it **defaults to off**. The follower quest is not start-game-enabled, so nothing runs until you flip this. |
| **Update interval NPCs** | **6–8s** | Sixteen concurrent actors in a 4,000-mod list. Start conservative. |
| **Update interval** (player) | leave default | Player-only, cheap. |
| **Dirty Expression** | **On** | Dirt & Blood is active and CEE reads its dirtiness/bloodiness effects directly. This one genuinely works. |
| **Trauma Expression** | **Off** | Needs Apropos2 or ZaZ. Neither is installed on any profile. It would poll for nothing. |
| **Aroused Expression** | **Off** | Needs SexLabAroused or OSL Aroused. You run OStim SA with no arousal framework. Dead feature. |
| **Aroused Modifiers** | Off | Same reason. |
| **Breathing Sounds** | your call | Works via CEE's own sound descriptors. AudioUtil not needed. |
| Eating Expression | Quick or Slow | Depends on your eating animation mod — try both. |
| Verbose Notifications | On for the first hour, then off | Tells you which emotion is firing while you tune. |

Gags and mouth wearables: CEE's check looks only for Devious Devices, ZaZ, Toys and
SL Survival keywords. None installed, so it never fires. Helmets and masks are not
detected — a full-face helmet may hide expressions, which is fine.

---

## 8. Install steps — DONE 2026-08-28

All of it executed. MO2 was closed throughout.

1. `Conditional Expressions Extended 2.2.1` installed as **Conditional Expressions Extended**.
   The 1.29 rar was NOT installed. Archive-vs-installed diff: 90/90, zero gaps.
2. Deleted `SKSE\Plugins\mfgfix.ini` — Mfg Fix NG keeps ownership of that file.
3. Deleted `Interface\Translations\CEE_rename.bat`.
4. `Expression_Random.json`: indices 16 and 17 zeroed in `female2` and `male2`. No other entry in
   the file still writes a blink modifier.
5. Mod placed at the top of the **Gameplay - Immersion** block in all six profiles.
6. `Conditional Expressions.esp` placed immediately after `Simple Follower Framework.esp`, at the
   end of the **Gameplay - Late Loaders** group. It overrides nothing, so position is free.
7. All four profile files written in all six profiles, with `.bak-cee-20260828` backups.
   22 checks passed per profile: one line added per file, entry present exactly once, every other
   line byte-identical, CRLF preserved, no lone LF, plugins.txt is a subset of loadorder.txt, and
   the esp is active.
8. MCM Recorder step added as the LAST step of all four recordings — `Authoria_Base`,
   `Authoria_Easy`, `Authoria_Hard` (0019) and `jbish base` (0010). Last, so a failure there
   cannot block anything earlier.

Slots after: FULL 230/254 (unchanged — the plugin is ESPFE), LIGHT 3818/4096.
All 4,108 active plugins resolve to real files.

### What the MCM Recorder step sets

Only the five options whose ESP default differs from the target, so it is correct whether the
recorder applies a toggle as an absolute set or as a flip:

| Page | Option | Action | Default |
|---|---|---|---|
| Expressions | Cold Detection | choose `Frostfall` | `Vanilla - Snowing` |
| Expressions | Less Dramatic Combat Expression | off | on |
| Expressions | Trauma Expression | off | on |
| Expressions | Aroused Expression | off | on |
| Settings | NPCs Support | on | **off** |
| Settings | Update interval NPCs | 7 | 3 |

Ordered so NPCs Support is switched on before its interval slider is set.

Deliberately omitted, because its default is already right: **Dirty Expression** (on).

**Correction, caught in the post-install audit.** My first draft of this step omitted
*NPCs Support* on the belief that the follower quest was start-game-enabled. It is not —
`QUST 000846 CondiExp_Followers` carries flags `0x1000`, with the Start Game Enabled bit
clear, and nothing in CEE's scripts starts it at load. It is only ever started by that MCM
toggle. **Follower and NPC expressions default to OFF**, so without this step the entire NPC
feature would never have run. Fixed.

That draft also spelled the pages and options in English. MCM Recorder matches the RAW string
a mod passes to `AddXOption()`/`Pages[]`, and CEE passes `$CEE_*` keys — SkyUI translates in
Flash at render time, not in Papyrus. English strings could never have matched; the page lookup
would have failed first and each step would have burned a 30-second timeout and a modal prompt.
The step now uses raw keys, matching the convention already used by the Frostfall and moreHUD
steps in these same recordings.

The menu registers as **`Conditional Expressions`**, not "…Extended" — that is the `ModName`
string property on quest `000D64`.

---

## 9. Decisions taken

All five open questions were resolved on the recommendations in this document:

1. **CEE 2.2.1 only**, not layered over 1.29.
2. **Combat expression off**, for consistency with UBE No Combat Expressions.
3. **Mfg Fix NG's `mfgfix.ini` wins** — CEE's copy deleted. `fTrackEyeZ` stays at the stock 40.
4. **Plugin position**: end of Gameplay - Late Loaders.
5. **All six profiles.**

---

## 10. Left undone, on purpose

- **AudioUtil is not installed.** Optional; CEE falls back to its own sound descriptors, and the
  AudioUtil path is player-only anyway.
- **Route 3 (cherry-picking EFA's brow-blink and gaze morphs onto UBE)** needs Blender 3.2 plus
  Blender TRI Tools, neither of which is on this machine.
- **UBE's eye tri** is untouched — boosting its Look morphs moves the eyeball and changes where
  characters appear to be looking.
