# Lewis's Authoria changes - what to take (2026-10-12)

Source: his GitHub repository (cloned to `C:\Users\User\Downloads\skywim\Lewis-ARR-Shared`). Full survey: session
scratchpad `s11_friend\FRIEND-CHANGES.md`. His own page "Rule 11 Changes for Authoria" lists 234 additions, 12 updates,
7 switch-offs and 9 list bugs with fixes, up to 11 October. Same base as you (1.6.1170, Requiem 6.0.2, UBE 2.0, Pandora).

What the repository is NOT: a profile export. It holds his patches, fixes, notes and skills. Binaries (meshes, textures,
archives) are not in it; those are on his Nexus pages or the Discord customizations channel. About 56 of his 300 items
are already on your side; about 244 are new.

## A. The three things you asked about

### A1. Animations (his are mostly idle / dialogue / follower animations, not combat packs)

| Item | What it does | On your side | Take? |
|---|---|---|---|
| OAR stack update (OAR 3.2.1, Math 1.0.5, Detection 2.1.5, Animation Queue Fix 1.0.2, Paired Animation Improvements 1.0.3) | His reason: 3.2.0 fixed keywords added by KID not being recognised on load, and variant settings not loading | one step behind on each | **Yes** - the foundation of everything below |
| NPC Idle Animations - Guards and Bandits Fidgets | guards and bandits fidget instead of standing still | no | Yes |
| Arcanyx Animation Asset Collection | animation resources used by his Lyra follower lane | no | Only with Lyra |
| Animated Poisons Redone 1.3 | poison-apply animation | in your download folder | Yes (already in the batch plan) |
| Ride Along 1.2.1 | follower rides behind you on the horse | 1.1.0 in your folder, newer on Nexus | Yes (batch plan) |
| Grab And Throw | grab and throw objects and bodies | no | Your call |
| Animated Mounted Casting | cast from horseback with animations | no | Your call |
| FP Inertia | first-person camera inertia | no (you have third-person Inertia) | Your call |
| Harvest Feedback Animations | animations when harvesting | no, but you run Dynamic Looting and Harvesting Animations | Skip (overlap) |
| Conditional Expressions base | face animations | you have the Extended version | Skip (redundant) |
| Vampire Feed Proxy | feeding animation and gameplay | no | Your call (unpatched for Requiem) |
| Player gestures tied to a player voice (DBReV bridge) | gestures while your character speaks | you run the Eleonora voice, he runs Dragonborn ReVoiced | Skip (different voice lane) |
| His follower-drunk-animation fix, Ashe idle-config comma fixes | NPCs and followers can use the drunk pack; two Ashe idle files had broken commas | described only, files NOT in the repo | Ask him for the files |

### A2. Conversation camera

| Item | On your side | Take? |
|---|---|---|
| Cinematic Conversation Camera 1.5.0 | in your download folder | **Yes** (batch plan). He switched Alternate Conversation Camera off; yours is already off |
| BG3-style preset pack for it | in your download folder ("Cinematic Preset For CCC") | Yes |
| His own camera settings file | NOT in the repo | Ask him for it, so yours looks like his |
| Smart Talk + its MCM | no | Your call (dialogue tweak; overlap with your dialogue mods unknown) |
| Floating Subtitles | he turned it OFF ("subtitles sit too high in first person"); yours is ON | Your call |

Needed on your side either way: "Switch Camera During Dialogue" goes off when the cinematic camera goes on.

### A3. Environment (thin - he added almost nothing to trees, grass, weather, lighting or water)

| Item | On your side | Take? |
|---|---|---|
| Dynamic Underwater Fish | in your download folder | Yes (batch plan) |
| Dynamic Terrain Deformation 1.2 | installed 1.0, disabled | Batch plan pick P6 |
| Region Weather - Engine Fix | no | Your call |
| Followers Ride Horses | no | Your call |
| House Cats Sandbox (all 28 house cats get an AI package; Winterhold and Morthal cats moved onto the rebuilt floors) | you have the same frozen cats | Ask him for the file (not in the repo) |
| Housecarls Pre-Thaneship placement fix (Winterhold and Morthal housecarls moved onto the rebuilt floor) | you have the same mod | Ask him for the file (not in the repo) |

If what you saw on his game was trees, grass, weather or lighting, it is not a mod in this repository. Ask him what it
was; it may be his upscaler build or an ENB/shader setting rather than a mod.

## B. Fixes worth taking now (small, safe, no new mods)

| Fix | Confirmed on your side? | What it does | Take? |
|---|---|---|---|
| Experience settings file (his corrected copy is in the repo) | **YES** - your winning file has no reading or group keys at all; the mod's built-in defaults apply (reading 2.0 instead of 0.5, group 0.2 instead of 0.3) | books give 4x the intended XP; his file restores the list's values and renames the keys the new version reads. One difference to decide: XP for uncategorised quests is 0 in your file, 10 in his | **Yes** - placed as a small override mod above "Authoria - MCM and INI Settings" in both profiles |
| Hearthfire Multiple Adoptions - USSEP fixes (+ Lux variant) and Requiem Lover Stone patch (in repo) | you run Hearthfire Multiple Adoptions | restores the bed fix in Windstad and Heljarchen and Requiem's Lover Stone sleep bonus | Yes |
| Main Menu Video 1.4.0 | you are on 1.3.1 | 1.3.1 has a volume-key bug; two 4K AV1 videos crashed his menu until re-encoded | Your call |
| OStim quiet sleeping | not needed - your sound overhaul already silences it | - | No |

## C. His bigger lanes (each is a project of its own)

- **NPCs, followers, dialogue (105 items)**: Dynamic Follower Banter and Fight With Me (both in your folder, batch plan);
  NPC Situational Reactions (batch plan pick P15; he keeps it OFF because of the Address Library version);
  many "-ologue" and Dialogue Expansion voice add-ons; Serana Dialogue Expansion family; FDE followers you lack
  (Elisif, Camilla, Fura, Olfina, Lisette, Senna, Ysolda, Ralof, Valerica, Vex, Calder, Kharjo, Cosnach, Rayya);
  UBE looks for Ysolda, Faralda, Fura and Lydia with his Authoria patches (in repo; need the YI look mods from Nexus).
- **Outfits (39 items)**: Kestrel, Obi's Victorian, Rugged Crusader, Zerofrost Skaal Sentinel, Ivyy Cute Maid, YoRHa 2B,
  Vampy Dress, Lunar Claw - each with his Requiem patch and UBE conversion (patches in repo; UBE meshes on his Nexus pages).
- **Adult (23 OStim items)**: none on your side.
- **UI**: QuickPocket, Notification Log NG, Party Sheet HUD, Local Map Upgrade, Custom Markers, Reticle Arcs.
- **Gameplay fixes**: Crime Bounty Decay, Frozen Electrocuted Combustion, Conjuration Limit Fix, several SKSE crash fixes,
  his Dawnguard recruitment-skip quest, Engaging Combat switched ON (you have it OFF).

## D. Things NOT to take from him

- His player-voice lane (Dragonborn ReVoiced): you run Eleonora on the same base; mixing breaks both.
- Outfit lanes that start from a 3BA/CBBE main file need his UBE meshes from Nexus, not the repo.
- His Pandora output and UBE converter output: his own runs, not transferable.
- Female Cicero lane: CBBE-only body.

## E. Open asks for Lewis

1. The local fixes his page lists but the repo omits: House Cats Sandbox, Housecarls placement fix, drunk-follower
   animation file, Ashe comma fixes, No Double Staves fix, SEQ fixes, Heels Sound extra coverage, Harkon Unbound Requiem patch.
2. His Cinematic Conversation Camera settings file and preset choice.
3. Which "environmental" things you saw on his game.
