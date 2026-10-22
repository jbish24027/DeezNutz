Authoria - UBE Master Patch (Authoria UBE 2.9.10, archive "Authoria - UBE Master Patch 170235 2.9.10 2026-10-11T16-49Z")
Built 2026-10-18.

What is in this folder
- Authoria - UBE Master Patch.esp          byte-identical to the archive (md5 41637b43b0d62ab1d572babd41bac482)
- Authoria - UBE records only Patch.esp    byte-identical to the archive (md5 c719e1beaa23a674a80a2fc7da475031)
- SKSE\Plugins\SkyPatcher\armor\AuthoriaUBERecordsOnlyPatch\Authoria - UBE records only Patch.esp.ini   byte-identical
- SKSE\Plugins\SkyPatcher\armor\AuthoriaUBEMasterPatch\Authoria - UBE Master Patch.esp.ini            6 lines removed in total across this file and the next (see below)
- SKSE\Plugins\SkyPatcher\armor\AuthoriaUBERecordsOnlyPatch\Authoria - UBE records only Patch - Duplicates.ini

The only change: the Cimmerian lines are removed (user decision 2026-10-18).
Reason: "Obi's Cimmerian UBE patch.esp" already gives all six Cimmerian pieces their UBE armature,
so these lines would have put a second UBE armature on the same piece.
The plugins were NOT edited. Nothing else changed.

Removed from "Authoria - UBE Master Patch.esp.ini" (5 lines):
filterByArmors=Obi's Cimmerian.esp|000D68:armorAddonsToAdd=Authoria - UBE Master Patch.esp|000A7D
filterByArmors=Obi's Cimmerian.esp|000D69:armorAddonsToAdd=Authoria - UBE Master Patch.esp|000A65
filterByArmors=Obi's Cimmerian.esp|000D6A:armorAddonsToAdd=Authoria - UBE Master Patch.esp|000A79
filterByArmors=Obi's Cimmerian.esp|000D6B:armorAddonsToAdd=Authoria - UBE Master Patch.esp|000A73
filterByArmors=Obi's Cimmerian.esp|000D6D:armorAddonsToAdd=Authoria - UBE Master Patch.esp|000A75

Removed from "Authoria - UBE records only Patch - Duplicates.ini" (1 line; its comment line above was left as-is):
filterByArmors=Obi's Cimmerian.esp|000D6C:armorAddonsToAdd=Authoria - UBE records only Patch.esp|000EA7

Pieces (Obi's Cimmerian.esp): 000D68 Amulet, 000D69 Boots, 000D6A Top, 000D6B Gloves, 000D6C Waist (skirt), 000D6D Shoulder.
Each keeps its UBE armature from "Obi's Cimmerian UBE patch.esp" (000800-000805).
To undo: put the six lines back from the original archive.
