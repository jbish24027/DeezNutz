# Fair and stamina diagnostic pass — 20 October 2026

Approved bounded diagnostic pass, PICTA profile. No installed game files changed. User dislikes the song and vocals; this is a music preference, not reported audio corruption. Arghus SMP and wheel removal are confirmed working.

## Fair shops
- Second approved pass: all 59 NPC winners retain vendor and JobMerchant factions, with Traits-only inheritance. All 33 vendor factions have Vendor enabled, hours 0–24 and no extra conditions. All 33 merchant chests resolve, are persistent (raw flag 1024), have no enable parent and contain 2–20 entries; exported stock links show no unresolved references. No shared broken record established.
- Logging-only counter trial prepared and compiled at `_staging/fair-barter-trace-trial/`, NOT installed. It preserves original behavior and records runtime keeper lookup, dead/3D state, native barter invocation and a delayed BarterMenu check. See its README for one-counter test and rollback. No plugin or generator reruns needed. Do not claim this is a repair.
- User tried multiple stalls and cannot recall their names. Proceed on that evidence; no specific stall name is required to investigate shared fair behavior.
- Runtime follow-up: user confirms Belethor's shop opens normally. Shared barter UI works in that test; focus remaining investigation on the fair. User tried several stalls; no stall name required.
- Confirmed all 59 counter references have KeeperRefId and KeeperPlugin properties, and all 59 addressed forms resolve to PlacedNpc records.
- Winning SkyrimFairStallCounter.pex decompiled cleanly. OnActivate looks up that specific keeper and calls ShowBarterMenu only if the actor is not dead and is 3D-loaded. The latter failure branches are silent. It does not use generic trade dialogue, so a voice-list fix cannot repair this path.
- The previously patched face lists still win from Holidays and Fair Requiem: 201 female and 214 male entries. Reqtificator has not restored the removed entries. A previously rolled actor's saved voice still cannot be established from these records.
- Today's Papyrus log (last write 06:13) contains suspended-stack warnings at 05:59:44 and 06:00:45, mainly crosshair event scripts plus several background updates. This is evidence of script backlog, not proof it caused the shop failure. No counter failure trace establishes the runtime branch reached.
- Ordinary-merchant comparison is complete. Next test uses the prepared counter trace to establish runtime execution. Do not repeat that comparison, rebuild voices or reset inventory blindly.

## Music
- Six stage tracks live under Sound/SkyrimFair/Music/Stage, with separate inside/outside sound descriptors. Audio quest uses parallel song lengths and performance timing, so simply swapping an arbitrary-length WAV risks mismatched timing.
- Source script exposes MusicEnabled. Its winning GlobalFloat is SkyrimFairAudioMusicEnabled (0014AF:SkyrimFair.esp), default 1. The update code stops playing song/cheer when the value falls below 0.5.
- Optional temporary in-game command: `set SkyrimFairAudioMusicEnabled to 0`. Restore with value 1. This silences stage playback, not an installed instrumental replacement. No console command has been executed by the assistant.
- Final replacement should use instrumental selections with adjusted/coordinated song timing and singer behavior, including outside playback. Fiddle.wav is a candidate to audition, not yet verified vocal-free. Do not claim it is an instrumental on filename alone.

## Stamina
- **Deferred at the user's request.** Retain findings below, but do not pursue the suggested tests or changes unless the user reopens this issue. Not confirmed fixed.
- Runtime screenshot: stamina 120.00 (HUD 120/120), StaminaRate 0.84, StaminaRateMult 125.30. These are positive rates at full stamina, not a timed recovery test. Need a depleted sample followed by ten seconds stationary, out of combat, with console closed.
- Active custom Run Stamina Drain quest: threshold 300 units/sec, 1.25 stamina/sec, 0.5-second updates. Its source drains current stamina while moving fast enough; it does not set regeneration actor values, and stationary samples do not drain. It excludes sprinting, swimming, sneaking and mounted movement by default. Could affect recovery while running; does not establish a cause for no stationary recovery.
- Winning REQ_AttackStaminaDrain is Authoria's exhaustion optimization. Source contains cleanup for attacking-drain/helper abilities. Source alone cannot prove cleanup happened in this save.
- No confirmed causal link between wheel removal and lost regeneration. Do not change regeneration values, remove Requiem effects or alter global balance without a runtime check.
- Next observation: stand still out of combat, then read `player.getav stamina`, `player.getav staminarate`, `player.getav staminaratemult`. Close console for ~10 seconds and read stamina again (console pauses the game). If numeric stamina rises but bar does not, pursue HUD; if it does not, inspect active effects/regen values. These are read-only commands.

## Evidence
Targeted exports `_staging/fair-counterrefs-20261020.jsonl`, `fair-keeperrefs-20261020.jsonl`, `fair-audioquest-20261020.jsonl`; decompiled scripts in `_staging/fair-counter-20261020/` and `_staging/fair-diagnostics-20261020/`. Initial ACTI export has no VMAD: scripts belong to placed counter references, not those base activators. Do not repeat the base-only search.

No definitive repair for shops/stamina can be claimed from this pass. Gather the small runtime comparison above before expanding investigation. No Synthesis/Reqtificator run needed for these diagnostic steps.
