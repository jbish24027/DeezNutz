Authoria - Papyrus - Horse Whistle Key Saddle Gate
Built 2026-10-17 for Authoria.

WHAT
A corrected copy of one Horse Whistle Key script: scripts\eeeHorseSpellScript.pex
(edited source in scripts\source\eeeHorseSpellScript.psc).
It must win over Horse Whistle Key's own copy, so this mod sits below Horse Whistle Key in MO2.
No plugin. Nothing else is touched.

WHY
Horse Whistle Key puts a spell on your horse. When that spell starts, a function called
CheckSaddle runs. If the horse wears a saddle outfit, it takes the outfit off (sets the
mod's naked horse outfit) and drops the saddle into the horse's inventory.
Putting the saddle back on only happens when the mod's "Enable Saddles" option is ON.
Authoria keeps that option OFF (MCM\Settings\Horse Whistle Key.ini, bSaddles = 0).
So with the option OFF, horses lost their saddles and never got them back.

THE FIX
CheckSaddle now does nothing unless "Enable Saddles" is ON. It uses exactly the same
check the re-equip code uses (Saddles.GetValue() as Bool).
- Saddles OFF: horses keep the saddle their outfit gives them.
- Saddles ON: the mod behaves exactly as before.
Every other function compiles to the same bytecode as the original. The script's
7 properties (names and types) are the same, so the esp's links still fill.

NOTE
A horse that was already stripped in an existing save keeps the naked outfit; the fix
stops new stripping, it does not undo old ones.

RE-CHECK AFTER ANY HORSE WHISTLE KEY UPDATE
This replaces the whole eeeHorseSpellScript from Horse Whistle Key 2.3 (scripts dated
2025-01-21). If Horse Whistle Key is updated, do not keep this file blindly:
compare the new eeeHorseSpellScript against this one, and either re-apply the same
Saddles gate around CheckSaddle in the new script or drop this mod if the author fixed it.
