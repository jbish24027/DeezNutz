# In-game fix list 22 Oct 2026 - state

Source: user's test session 22 Oct (list also in Desktop\WHAT TO TEST.txt section I). Profiles: PICTA + HPH.

## Done
- 2. Guard helmet idle: `05-settle-helmet.hkx` (male+female) moved out to
  `mods\NPC Idle Animations (OAR)\_removed (helmet idle)\`.
- 3. Malignis mix: `user.json` beside both NPC Idle Animations OAR submod configs = full config + OAR `Random`
  < 0.5 (Local, reset on loop) -> new guard/bandit idles play ~half the time. Malignis replaces mt_idle,
  the new pack replaces mt_idlelookingb, so they never overrode each other.

## Findings, not fixed
- 1. Ride Along (mod `Ride Along - Horse Riding Companion`, RideAlong.esp ESL FE:1604, DLL internal v0.4.0):
  RideAlong.log: topics found, but "Ride: 0 of 0 lines pass (offset 424 ...)" for all 4 topics at runtime,
  while the plugin has 16 INFOs per topic and nothing overrides them (houseCARL info_order: single plugin).
  Only one copy of the DLL/esp exists. Cause unknown - something in the setup leaves the topics with 0 INFOs
  at runtime. Workaround told to user: K key while mounted. Next: test with a minimal setting (DialogueEnabled),
  check other SKSE dialogue hookers (DBReV, Fuz Ro D-oh, Liita, Dynamic String Distributor), ask on the mod page.
- 4. Faces: Ria / Carlotta / Taarie = GMS (UBE YI GMS) faces from NPC2 output `Authoria - Output - NPC Appearances.esp`
  (mod `Authoria - NPC Merge`). The GMS pack's own skins: Ria's skin uses `CarlottaValentia_SkinTexture`
  (Eidolon\Carlotta Valentia\!UBE\Body\femalebody_1_d.dds) - authored that way in GMS. Facegen provenance clean.
  So the seam is face-vs-body skin tone inside the GMS look. Options for the user: pick another look in NPC2 for
  these three (user runs NPC2), or a patch giving them default UBE skin (test).
- Naked: Taarie's outfit FineClothesOutfit02Variant -> armor `REQ_Cloth_Fine_Body_4` 0F8715 (winner Requiem.esp,
  only Skyrim+Requiem touch it) uses ARMA `FineClothes02VariantAA` with no UBE race -> UBE women naked in it.
  Probably a wider UBE vanilla-outfit coverage gap: sweep every outfit worn by UBE-race women for armors without
  a UBE-race ARMA. Sybille (also naked) not checked yet.

## Still to do (user asked: small fixes 1-9)
5. Balgruuf hair/beard colour mismatch. 6. Static carriage outside Whiterun stables wrong textures.
7. Female priest robes no SMP (vanilla coats SMP was men only). 8. Fair: hated song still plays outside and inside;
stalls don't work; browse via dialogue doesn't work. 9. Marcurio's needs HUD (SunHelm Follower Needs widget?) move left.
Then 10 (big): Clothes of the Northern Folk 3BA + HIMBO + SMP + bard outfits (Lisette).

## Session 2 (22 Oct, afternoon) - results
- 5 Balgruuf: FIXED offline. Mod `Authoria - Balgruuf Beard Fix` (README inside) above TSOS; + PICTA / PICTA x Astralite / HPH,
  - elsewhere; modlist backups `*.bak-pre-balgruuf-20261022`. Cause: beard shape HumanBeardMedium04 baked near-white tint +
  Hvergelmir vanilla-path texture; 0BalgruufBeardHL pointed at a missing beardshort05_hd. Note: TSOS beard textures are
  pre-coloured brown, hair is pale+tinted platinum, so some tone gap is TSOS's authored look.
- 6 Carriage: Whiterun stable cart = ref 0DDDA4 swapped by Snazzy BOS to GM_cartfurnstatic01A_Covered01; the 10-18 Skyking
  fix (`Authoria - Skyking Carriages - Over Outputs`) wins all 22 Snazzy cart meshes, all 81 textures present. Need the
  user's screenshot / words for what still looks wrong. Side find: Snazzy Seasonal Patch inis sit in the mod ROOT, not a
  Seasons\ folder (its own page says MO2 drops the folder) - may not load. Not changed.
- 7 Female priest robes: female priests do NOT wear monk robes at runtime: Senna/Orla -> 000805:ksssl_dbgc.esp outfit,
  Danica -> Younglings patch outfit (SkyPatcher). UBE robe SMP = new rigs on UBE BodySlide meshes with the coat-smp toolkit.
  Sized for the user, not started.
- 8 Fair: barter trace 22 Oct 06:01 again BarterMenu open = TRUE (cheese stall). Topic/vendor data fine. Vanilla
  "What have you got for sale?" = JobMerchant + GetOffersServicesNow + voice; the 10-17 voice fix needs a NEW game. Song:
  per SESSION-STATE the user dislikes sung songs, wants instrumental. Asked user which song + what the stall menu does.
  Side find: Papyrus log floods with `Unbound native function "NSR_IsOn" / NSR_GlobalValue / NSR_DirectorHeartbeat`
  several times a second - some script's DLL is missing. Not investigated.
- 9 Needs HUD: SunHelmFollowerNeeds.json hudAnchorX 0.16 -> 0.02 (backup .bak-pre-hudleft-20261022). Shared by all profiles.
- 1 Ride Along: plugin data fine (TIFC 16/4/16/16, IDs 0x810+, QNAM ok, single provider). Log "offset 424/1655/1AD6/2D0F"
  = the topics' FILE offsets in RideAlong.esp, not IDs. INFO conditions: DialogueEnabled 803==1, teammate OR
  CurrentFollowerFaction, not in RideAlong faction, BackSeatEnabled 809==1, GetIsVoiceType per-voice list (16 lists).
  Cause still unknown; next = report to the author (Clyde, GPL source on Nexus/GitHub) with RideAlong.log.
- 4 Naked UBE women: FOUND. Records are clean (80 vanilla outfit armors all have UBE ARMAs incl. SkyPatcher
  armorAddonsToAdd; 146 UBE meshes present). The CNF Immersive Distribution SkyPatcher layer swaps 6 UBE women into
  CNF outfits with NO UBE ARMA: Taarie (CNFBunadSigdalPurple), Sybille + Alva (CNFValdresSanguine), Endarie
  (CNFVikingSigdalPurple), Viola (CNFVikingTelemarkBurgandy), Illia (CNFVikingNordlandGreyPurple). 8 armors, 5 body.
  Quick fix offered: drop these 6 from zzzClothesOfTheNorthernFolk.ini like the 10 protected NPCs. Scratch data in this
  session's scratchpad (ube_*.jsonl).
- 10 CNF: 387 ARMO / 596 ARMA; 210 female body meshes (139 bunad, 71 viking) + ~385 accessories; no 3BA/HIMBO/UBE
  conversion exists on Nexus (search 22 Oct). Plan + estimate given to user, waiting.
- 4 DONE (user OK): the 6 UBE women removed from CNF zzzClothesOfTheNorthernFolk.ini (5 list entries trimmed, 1 line
  commented). Backup `_backups\2026-10-22 - CNF UBE women out\`. SkyPatcher post-state verified: vanilla/Illia-mod outfits,
  all UBE-covered. Put them back once CNF has UBE versions.
- 8 Fair song DONE: user named it = "The Wanderer's Fair" (sung, about the fair). Stage + outside-show scripts now skip it
  (see mods\Authoria - Fair Companion Guard\README.md). Mod also added to HPH (above The Wanderer's Fair, backup
  modlist.txt.bak-pre-fairsong-20261022). Takes effect on load; no new game needed.
- 1 Ride Along FIXED (22 Oct): RideAlong_DialogueQuest is Start-Game-Enabled but the mod ships NO .seq, so the engine never
  loads its topics' INFOs (= the DLL's "0 of 0 lines"). houseCARL write_seq -> mods\Ride Along - Horse Riding Companion\SEQ\
  RideAlong.seq (0x01000800). Dialogue check now 0 findings. Voice types (Marcurio MaleEvenToned, Aela FemaleCommander)
  are covered by the INFO lists. Best tested on a new game. If the mod updates, re-run write_seq.
- 10 CNF prototype BUILT (Fralia's Hardanger black): see _tools\northern-folk-conversion-plan\SESSION-STATE.md.
