Authoria - Firefly Light
========================
Makes flying torchbugs/fireflies emit real light.

WHAT IT DOES
Light Placer attaches a light to every reference that uses the mesh
Critters\Firefly\Firefly.nif. That is the mesh used by:
  - CritterFirefly            (0C2D3F:Skyrim.esm)  "Torchbug"  - the vanilla bug
  - CritterFirefly001         (001876:ForgottenCity.esp)
  - CritterFireflyDUPLICATE001 (001875:ForgottenCity.esp)
  - _Camp_PerkNextBug / _Camp_PerkPrevBug (Campfire.esm) - the Campfire
    perk-menu navigation bugs. They share the mesh, so they glow too.

FILES
  Authoria - Firefly Light.esp   ESL-flagged. One record: the LIGH
                                 Authoria_FireflyLight (000800).
  LightPlacer\Authoria\Authoria_Fireflies_LP.json   the attachment config.

TUNING
Edit the LIGH record (Authoria_FireflyLight) for the look:
  Radius 160                     size of the lit pool. 250 = Lux torch.
  FadeValue 0.6                  brightness. Raise for a stronger glow.
  Color 205,255,130              yellow-green. Warmer = raise R, lower G.
  Flags Dynamic, Flicker         Dynamic makes it light actors, not just
                                 terrain. Drop Flicker for a steady glow.
  FlickerPeriod 1.5              slow pulse.
  FlickerMovementAmplitude 0     kept at 0; the bug already moves.
Edit the JSON for placement:
  flags "Simple|IgnoreScale"     Simple = no contact shadows (these are tiny
                                 moving lights, shadows are not worth it).
                                 IgnoreScale keeps radius off critter scale.
  points [0,0,0]                 offset from the bug's root.

NOT COVERED ON PURPOSE
Firefly-in-a-jar (Critters\Firefly\FireflyInJar.nif) is NOT in this config.
Rally's All The Things wins that mesh and it already carries ENB Light
particle-light planes (shapes EnbParticleLight01:0 and
EnbParticleLighGlowt01:0). Community Shaders' Light Limit Fix already
registers those glow textures in ParticleLights\. Adding a Light Placer
light on top would double-light every jar.

REQUIRES
Light Placer (installed, 4.2.1) and Community Shaders Light Limit Fix, both
already in this load order. Torchbug counts are small - the vanilla spawner
property iMaxCritterCount is 2 per marker - so this is not a light-budget
concern.

Created 2026-08-15.
