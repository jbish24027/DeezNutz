Authoria - Lydia Face Tint Fix   (folder/plugin still named "Weight Runtime" for history - do not rename;
the SPID ini and MGEF/SPEL FormIDs reference this plugin basename.)

WHAT IT FIXES: UBE Lydia (0A2C8E:Skyrim.esm) loaded with a dark/brown face on every new game.
ROOT CAUSE (measured 2026-08-16): her head shape's face-tint shader ShaderTintColor (NiOverride key 7)
was 0,0,0 at first load and stayed 0. RaceMenu (skee64, SKEEHooks.cpp UpdateModelSkin_Hooked) writes
the actor's skin tint into that field ONLY on a model update (e.g. console setnpcweight); its first-load
path (ActorUpdateManager.cpp) never does. Her authored skin preset is HumanFemaleSkinWhite02
(206,205,204) so her baked FaceTint carries almost no colour and her whole face tone depended on that
runtime value -> black -> brown face. Serana's baked tint already carries her colour, so she was fine.
WEIGHT WAS NEVER THE CAUSE (actor weight measured 79 = record, and she was still brown).

THE FIX: SPID ability -> Authoria_LydiaWeightFix.pex writes 206,205,204 as a PERSISTENT NiOverride
node override (key 7) on shape 00UBE_FemaleHead. RaceMenu re-applies persistent node overrides at every
load. No weight/race/rebuild/console. Touches no record -> survives Reqtificator. Prints proof to console:
  [LydiaTint] fix: before=0,0,0 wrote=206,205,204 after=206,205,204 persisted=True
Requires: RaceMenu (NiOverride), ConsoleUtilSSE (print only), SPID.

PARKED 2026-08-17 14:35: the SPID ini is renamed to *.PARKED-... so this ability no longer runs.
Reason: the real cause of Lydia's dark face was found (see Authoria - Patch - Serana UBE Face /
SERANA-FACE-FIX-NOTES.md round 3): her baked head was never loading. Now that it does load, writing
ShaderTintColor (NiOverride key 7) onto a BAKED head converts its material and crashes the renderer
(two CTDs on Serana 2026-08-17 11:48 + 14:24 with the same write). A baked head needs no tint write.
Do NOT re-enable unless her head is proven to be a runtime rebuild again (Authoria_FaceProbe.txt shows
"head tex0 = Textures\!UBE\Head\FemaleHead_d.dds" instead of her !UBE\Lydia\Head diffuse).
