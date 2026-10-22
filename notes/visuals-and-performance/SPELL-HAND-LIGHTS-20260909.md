# Spell hand lights - 2026-09-09

Request: "light should emit from spells in my hand".

## What was wrong

The game already puts a light on every spell held in the hand. It is just tiny.
Flames uses a light with radius 36, Frostbite and Healing 50, Sparks 30. A hand is about
30 units across, so the light never reaches a wall or the floor. The records are intact
(vanilla values, USSEP winners) and nothing suppresses them. It only looks like there is no light.

Checked and cleared: the Requiem Magic Redone effects still point at the vanilla hand lights;
Light Placer's Lux CS blacklist only disables placed light references and torches are exempt,
so it cannot touch hand lights; the CS Light Limit Fix unlocks the magic light limit at load
("[LLF] Unlocked magic light limit" in CommunityShaders.log); ISL Helper deliberately skips
every light referenced by a magic effect (magicFXSkipped=405 in SKSE_ISL.log).

## What was done

One new file, no plugin, no load-order change, save-safe:

    mods\houseCARL - Authoria - Glow Coverage\LightPlacer\Authoria\Authoria_SpellHandLights.json

Light Placer 4.2.1.1 (installed) has supported casting-art lights since Dec 2024. It hooks the
moment the game attaches the hand-casting visual (ActorMagicCaster::AttachEnchantmentVisuals)
and removes the light when the visual detaches (spell released or sheathed). The light is a
real dynamic point light parented to the casting art itself, so it rides the hand and lights
walls, floor, and actors, including the caster. It applies to every caster, so NPC mages
glow while they charge a spell too.

The JSON keys each entry by casting-art FormID ("formIDs"), so it works with the Kittytail
VFX Edit replacer meshes (same records, new nifs) and with any future mesh replacer.

Coverage: 165 of the 230 casting arts in the load order, 4075 of 4278 magic effects that carry
a casting art. The bulb for each art is the light record the game's own effects pair with it
most often (a census of all 4278 winning magic effects), so:

- fire = warm pale orange (MagicLightFireInHand)
- frost = pale ice blue (MagicLightFrostHand01)
- shock = blue-violet (MagicLightShockHand)
- restoration = gold (MagicLightHealHand01), ward = sky blue
- alteration = green (MagicLightAltPosHand01), telekinesis = amber, paralysis = pale green
- conjuration = deep violet (MagicLightSummon01), banish = dark purple, reanimate = blue
- illusion = mint (positive) / salmon (negative)
- Apocalypse, Triumvirate, Everdamned, Requiem MR, Wildwaker etc. use their own hand lights

Full per-bulb table and the two skip lists: SPELL-HAND-LIGHTS-COVERAGE-20260909.md.

Left out: 60 arts with no paired light anywhere (Requiem throwing knives, bombs, powders,
mine traps, the Dragonborn spider casting arts, spider spit, Staff of Magnus). And 5 Triumvirate
shadow-magic arts whose paired light is a NEGATIVE light (darkness in the hand is the author's
intent; a negative dynamic light under CS is untested, so they stay vanilla).

Known stack: about ten casting arts already carry a large light of their own in the game's
records (Everdamned's vampire-lord blood hands r512, Vigilant's Mary hands r768, the blue absorb
hands and Requiem MR's reanimate ritual r300, one Apocalypse atronach ward). Those spells get
the new light on top of the old one, so they read a little brighter than the rest. If one looks
blown out, delete its FormID from the JSON; the coverage table names them.

## Tuning (edit the JSON, then `ReloadLP` in the console)

Every entry uses the same three numbers:

- `fade` = brightness. 0.6 for all schools, 0.7 for fire. Lux CS's exterior lanterns are 0.8,
  its interior lanterns 0.3, iLluminous's frost atronach body glow 1.0. Halve or double to taste.
- `cutoff` = reach. 0.1 (same as Lux CS and iLluminous). Reach under CS inverse-square lighting
  is roughly sqrt(fade x 4 x 0.8 x 4904 / cutoff): fade 0.6 / cutoff 0.1 = about 300 units,
  fade 0.7 = about 330. Lower cutoff = longer soft tail (0.05 = about 1.4x reach).
- `radius` = 350. Only the culling bound for the renderer; leave it at or above the reach.

Flags: InverseSquare (CS inverse-square falloff, matching the Lux CS / ISL Helper world),
IgnoreScale (a giant or a scaled NPC does not get a bigger light), PortalStrict (culled by
room bounds, same as the vanilla hand lights). No Shadow flag on purpose: the engine has 4
shadow slots and a light that loses its slot goes black under CS 1.8 (see the lighting notes).

`ReloadLP` applies changed values immediately to lights already attached. A newly added entry
attaches the next time the spell is drawn.

Per-school changes: each entry is one bulb group, so change the fade on the fire group alone,
or give a group a `"color": [r,g,b]` override to replace the bulb's colour.

## Test in game

1. Load a save, go somewhere dark (an unlit cellar or outdoors at night), stay in third person.
2. Draw Flames in one hand, do not cast. The wall and floor near you should light orange.
3. Swap to Frostbite (blue), Healing (gold), Sparks (blue-violet). Hold Candlelight charging: pale.
4. Cast Flames continuously: the light stays while the stream runs, then goes when you stop.
5. Find an NPC mage charging a spell: their hand should light the ground.
6. Optional console check: `prid 14` then `logLP` lists the lights attached to you; the
   Light Placer log's RESULTS block should show FormIDs rising by 165 keys.

If it is too strong or too weak, say so in words (brighter / dimmer / reaches too far) and the
fade / cutoff numbers change. Nothing else needs to move.

## Removal

Delete the one JSON file. Nothing else was changed.

## Why not the alternatives

- (SJG) Lights On / Colorful Lights for Spells: they edit the vanilla LIGH records to torch size
  (radius 512-1024) with vanilla falloff. They would work, but every hand light would then be a
  flat vanilla-falloff blob in a world where every other light is inverse-square (Lux CS, ISL
  Helper), and the LIGH overrides would need a plugin slot and re-checking against USSEP.
- Editing the LIGH records myself: same falloff mismatch, and ISL Helper skips magic-effect
  lights by design, so they could not be converted at runtime either.
- ENB particle-light planes in the hand meshes: Kittytail's Healing mesh already has one, the
  fire / frost / shock meshes do not; adding planes means editing four replacer meshes that get
  overwritten on every VFX Edit update, and CS makes the light radius half the plane's bound.
- First person magic hand light fix (Nexus 142757): irrelevant here, first person is blocked.

## Facts worth keeping

- Light Placer casting lights: hook ActorMagicCaster::AttachEnchantmentVisuals -> AddCastingLights.
  Key = casting art (ARTO) FormID via "formIDs", or the art's model path via "models". Attach
  node = the attached casting art (player, 3rd person) or the actor's magic node (NPCs).
  One light per casting source (left / right / dual), removed with the art.
- The GetFormID parser accepts "0x01B211~Skyrim.esm" (plugin-relative) and EditorIDs.
- JSON data keys in 4.2.1: light, color, radius, fade, fov, cutoff, size, shadowDepthBias,
  offset, rotation, externalEmittance, conditions, conditionalNodes, flags, controllers.
  With InverseSquare set and a vanilla bulb, `cutoff` MUST be given: the default comes from the
  record's falloff exponent (1.0), which collapses the light to nothing.
- LP's IsDynamicLight is true for anything attached to an actor, so hand lights always light actors.
- Census tooling (scratch, re-runnable): casting_art_census.json/.md, build_spell_hand_lights.py.
