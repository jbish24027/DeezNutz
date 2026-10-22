Authoria - Patch - Player Dirt Overlays   (built 2026-08-21)

*** READ THE 'ROUND 5' SECTION AT THE BOTTOM FIRST. It supersedes the record/script layout
*** described immediately below: the visuals now run from a QUEST, the GetIsID conditions are
*** gone, and the MGEFs no longer carry a script.

What it does
  Dirt and Blood keeps tracking the player's dirt exactly as before (four stages, washing,
  rain, swimming, soap, the NPC comments, the "Filthy" penalties). What changes is only how
  the PLAYER's dirt is drawn: instead of Dirt and Blood's baked UBE effect shader, the four
  stages put Zaki's UBE dirt (mod "BISR - Zaki Renewed - UBE Set A") on the player's skin as
  RaceMenu overlays - body, hands, feet and face - with rising opacity:
      stage 1 "Slightly Dirty"   0.50
      stage 2 "Somewhat Dirty"   0.65
      stage 3 "Quite Dirty"      0.80
      stage 4 "Covered in Dirt"  1.00
  The overlay is removed when the stage ends (washed, rained clean, swam, or a blood stage
  took over - Dirt and Blood replaces a dirt stage with a blood stage while you are bloody).
  NPCs are not touched: vanilla-race NPCs keep the HD Retexture, UBE NPCs keep the UBE bake.
  Blood on the player is unchanged (still the UBE bake).
  Because these are skin overlays, clothes and armour do not get dirty any more on the player;
  the skin under them does. That is the Bathing-in-Skyrim look the set was made for.

Records (ESL-flagged plugin, loads right after "Ultimate Body Enhancer - Dirt and Blood.esp")
  NEW  GLOB  Authoria_PlayerDirtStage            which stage currently owns the overlay (0 = none)
  NEW  MGEF  Authoria_Dirty_Effect_Dirt1..4_PlayerOvl
             copies of Dirty_Effect_Dirt1..4_UBE (name, description, flags, Dirty_Blood_Keyword
             on 2-4, perk Dirty_Perk_VeryDirty on 4) WITHOUT the hit shader, plus the script.
             Conditions: HasKeyword UBE_BodyRace == 1 AND GetIsID Player == 1.
  OVR  MGEF  Dirty_Effect_Dirt1..4_UBE           + condition GetIsID Player == 0
             (so the baked shader no longer draws on the player; UBE NPCs unchanged)
  OVR  SPEL  Dirty_Spell_Dirt1..4                + the matching _PlayerOvl effect as a third entry

Script  Scripts\Authoria_PlayerDirtOverlay.pex   (source in Source\Scripts)
  OnEffectStart : finds a slot per part, sets the texture + the shader keys, records the stage.
  OnEffectFinish: restores the slot to RaceMenu's blank default unless a newer stage already
                  owns the overlay (Dirt and Blood adds the next stage BEFORE removing the old).
  Abilities re-fire OnEffectStart on every game load; the apply is idempotent (a slot already
  carrying one of our textures is reused rather than a second one taken).

  THE THREE THINGS THAT MADE v1 DO NOTHING (fixed 2026-08-21 17:15) - keep them in mind if this
  is ever rewritten. Both working overlay mods already in this load order (UBE Wounds,
  OCum Ascended) do it the way described here; v1 did not, and applied nothing at all:
    1. Overlay node names are LOWERCASE - "Body [ovl0]", not "Body [Ovl0]". skee64.ini's own
       comment spells it "Body [Ovl#]", which is misleading. A wrong node name is a SILENT
       no-op: nioverride.psc warns "THESE DO NOT SELF CLEANUP IF THE NODE IS NOT FOUND".
    2. On the PLAYER every overlay slot already exists and carries
       actors\character\overlays\default.dds. So a slot is free when its texture is EMPTY OR
       THAT DEFAULT - testing HasNodeOverride() finds every slot "taken" and the script gives up.
    3. Texture (key 9) + alpha (key 8) alone is not enough. Set the whole stack the way the
       working mods do: 9/0 texture, 7/-1 tint (white = 16777215), 0/-1 emissive colour 0,
       1/-1 emissive multiple 1.0, 8/-1 alpha, 2/-1 glossiness 0.0, 3/-1 specular 0.0.
  Needs RaceMenu (NiOverride) - already in the list; skee64.ini has 28 body / 18 hand /
  18 feet / 26 face slots and bPlayerOnly=1, which is all this needs.

Tuning
  Opacity per stage = property OverlayAlpha on each _PlayerOvl effect (xEdit / houseCARL);
  it is Properties[1] on the record's script, a ScriptFloatProperty.
  Texture paths = properties BodyTextureFemale / BodyTextureMale / FaceTexture. They are NOT
  bound in the plugin - the defaults compiled into the .pex are used. Another Zaki set
  installed to the same paths needs no edit at all.

Mid-save install
  Safe. The current stage's ability re-fires OnEffectStart on load, so the overlay appears on
  the next load; otherwise at the next stage change.

If it still does not show
  Papyrus logging was turned on for this test (profile Skyrim.ini, backup
  Skyrim.ini.bak-playerdirt-log-20260821). The script traces every decision, so
  Documents\My Games\Skyrim Special Edition\Logs\Script\Papyrus.0.log will contain either
    Authoria_PlayerDirtOverlay: Body [ovl27] <- mzin\Bathe\Set1\F\DirtFXBody.DDS   (it applied)
  or
    Authoria_PlayerDirtOverlay: NO FREE OVERLAY SLOT for Body (28 slots)           (it could not)
  or nothing at all (the effect never started). That tells us which half is wrong without guessing.

Removal
  Wash to clean first (so no overlay is left in the co-save), then disable the plugin.


================================================================================
ROUND 5 (2026-08-21 18:30) - THE VISUALS NOW RUN FROM A QUEST, NOT A MAGIC EFFECT
================================================================================
Four in-game rounds produced ZERO Papyrus traces from the magic-effect script, including a
full 15-minute session (18:11-18:26) on the build where the archetype was already correct.
Evidence gathered along the way, none of it assumed:
  * the plugin IS loaded - it is in the save's own LIGHT PLUGIN list (parsed from the .ess)
  * the patch IS the load-order winner for all four dirt spells (conflict tree)
  * the RaceMenu .skse co-save holds default.dds + SFO freckles + RX tattoos + Bitchcraft
    body paint, and ZERO occurrences of "mzin" / "DirtFX" - the texture had never been applied
  * the marks in the user's screenshot are NOT the Bitchcraft overlays (rendered them: tiny
    gem/herb and moon motifs, ~0.2% coverage, not the large smudges)
CONCLUSION FROM THE ABSENCE OF TRACES: with the archetype fixed, the script runs the instant the
effect applies. It never traced, so the player was NOT holding a dirt stage in any measured
session - Dirt and Blood swaps the dirt stage for a BLOOD stage while bloody, and blood is
untouched here (Zaki Set A ships dirt textures only - no blood exists to swap).

So the visuals were moved OFF the magic effect entirely, onto a polling quest that cannot be
blocked by condition semantics, effect-list propagation, or effect application:

  QUST Authoria_PlayerDirtQuest (000805) - Flags 17 (start-game-enabled), one Reference alias
       forced to PlayerRef 000014, alias script Authoria_PlayerDirtDriver. Structurally
       IDENTICAL to Authoria_WashQuest in "Authoria - Patch - Dirt and Blood Tweaks.esp",
       which works in this same load order.
  Scripts\Authoria_PlayerDirtDriver.pex - polls every 6 s: reads which of Dirty_Spell_Dirt1..4
       the player has via Game.GetFormFromFile + HasSpell, checks the race carries UBE_BodyRace
       (Race.HasKeyword, not a condition), and applies/clears the overlay. Traces every decision,
       including a FIRST POLL line naming the race, the UBE check and the dirt stage.
  The four _PlayerOvl MGEFs KEEP the gameplay payload (name, description, Dirty_Blood_Keyword,
       the Filthy perk on stage 4) but their script was REMOVED - only the quest touches overlays
       now, so two code paths can never fight over the same slot.
  Scripts\Authoria_PlayerDirtOverlay.pex is left on disk but is referenced by NOTHING. Harmless.

WHAT THE LOG WILL SAY NEXT RUN (Documents\My Games\Skyrim Special Edition\Logs\Script):
  Authoria_PlayerDirtDriver: STARTUP - polling every 6.0s          <- plugin + script are live
  Authoria_PlayerDirtDriver: FIRST POLL - race=... isUBE=... dirtStage=N
  Authoria_PlayerDirtDriver: Body [ovl27] <- mzin\...\DirtFXBody.DDS @0.5
If dirtStage reads 0, the character simply is not dirty (bloody or clean) and there is nothing
for this mod to draw - which is the single most likely explanation for every round so far.

================================================================================
ROUND 6 (2026-08-22 05:15) - IT WORKS; KILLING THE LEFTOVER OLD VISUAL
================================================================================
CONFIRMED WORKING, from two sides:
  Papyrus  Authoria_PlayerDirtDriver: FIRST POLL - race=Breton isUBE=TRUE dirtStage=1
           Body [Ovl27] / Hands [Ovl17] / Feet [Ovl17] <- mzin\Bathe\Set1\F\DirtFXBody.DDS @0.5
           Face [Ovl25] <- mzin\Bathe\Set1\F\DirtFXFace.DDS @0.5
  co-save  now lists mzin\Bathe\Set1\F\DirtFXBody.DDS and DirtFXFace.DDS on the character.

User reports the OLD dirt visible as well. The co-save shows only the Zaki textures plus her
freckle/tattoo/body-paint overlays - so the old visual is NOT an overlay, it is an effect SHADER.
Ruled out, with evidence, before changing anything:
  * SPID (DirtandBlood__DISTR.ini) - its two form-filtered lines target FalmerRace and
    WerewolfBeastRace, not the player.
  * Dirty_Spell_NegativeSideEffects - carries only Dirty_Persuasion and
    Dirty_ResistDiseaseNegative; it references the dirt effects in CONDITIONS, not as visuals.
  * A stale save - the character is a brand-new Enora (save #15, 05:05), not an old save.
FIX APPLIED: the four Dirty_Effect_Dirt1..4_UBE records now have HitShader nulled. Those records
are referenced ONLY by the four player-only dirt spells (verified by reverse query) and were
already removed from them, so no NPC and no other spell can be affected - this simply makes it
impossible for the old baked dirt shader to draw on the player by any route.
REMAINING CANDIDATE: BLOOD. Dirt and Blood swaps the dirt stage for a blood stage while bloody;
blood is untouched by this mod BY DESIGN and cannot be swapped - Zaki Set A ships dirt textures
only (DirtFXBody/Face/Hands/Feet), there is no blood texture in it. The driver therefore now logs
a full spell census on first poll and on every stage change:
  Authoria_PlayerDirtDriver: SPELLS dirt1=.. dirt2=.. dirt3=.. dirt4=.. | blood1=.. .. blood4=..
One line now identifies anything still on the player without another guessing round.

================================================================================
ROUND 7 (2026-08-22 05:45) - THE OLD SHADER WAS THE VANILLA LANE. CONDITIONS DO
NOT EVALUATE ON THE PLAYER IN THIS LOAD ORDER - THE DIRT LANE IS NOW CONDITIONLESS
================================================================================
Census from the 05:30 session, on a new game, after the UBE shader was nulled:
  SPELLS dirt1=TRUE dirt2=False dirt3=False dirt4=False | blood1..4=False
  Body [Ovl27]/Hands[Ovl17]/Feet[Ovl17]/Face[Ovl25] <- Zaki DirtFX @0.5
So: no blood anywhere, the Zaki overlay applied, and the old shader was STILL drawn.
The UBE effect had already been removed from the spell in round 3, so nulling its HitShader in
round 6 could not have mattered. By elimination the only remaining shader in Dirty_Spell_Dirt1
was the VANILLA-lane Dirty_Effect_Dirt1 -> Dirty_Shader_Dirt1 -> filthyfx1.dds (HD Retexture).

That effect is gated `HasKeyword UBE_BodyRace == 0`, i.e. NON-UBE actors only. It drew on a UBE
player anyway. Therefore:

  *** MAGIC-EFFECT CONDITIONS DO NOT RESOLVE ACTOR STATE ON THE PLAYER HERE. ***
  Both HasKeyword and GetIsID come back "no match" with RunOnType=Subject. The same failure
  silently blocked the _PlayerOvl effects (gated == 1) for four rounds, which is the real reason
  the script never fired - the wrong archetype was a second, independent bug on top of it.
  Papyrus is unaffected: Race.HasKeyword() returns TRUE (driver logs isUBE=TRUE every poll).
  RULE: never gate anything player-facing on a magic-effect condition in this list. Gate in
  Papyrus, or arrange the data so no gate is needed.

FIX: the player dirt lane is now CONDITIONLESS. Each of Dirty_Spell_Dirt1..4 holds exactly ONE
effect - its Authoria_..._PlayerOvl - with no conditions and a null HitShader. The vanilla-lane
effect was removed from all four spells. Nothing in the player's dirt lane can draw a shader by
any route; the quest driver alone paints the visuals. The Filthy perk (Dirty_Perk_VeryDirty) and
Dirty_Blood_Keyword still ride on the _PlayerOvl effects, so the gameplay penalties are intact.
This is safe because Dirty_Spell_Dirt1..4 are PLAYER-ONLY (every AddSpell targets PlayerRef;
NPCs use Dirty_Spell_DirtForNPCs / Dirty_BloodySpellforNPCs, untouched).

KNOWN TRADE-OFF: a NON-UBE player would now get no Dirt and Blood dirt visual, because the
vanilla shader is gone from the spells and the driver paints only UBE races (it checks
Race.HasKeyword in Papyrus). Irrelevant for this playthrough; if a vanilla-race character is ever
played, either restore Effects[0] on the four spells or extend the driver with a vanilla-UV set.
