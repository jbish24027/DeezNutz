Authoria - Papyrus - Misc - Requiem Optimizations
REQ_ConditionalSubEffect : when the parent magic effect starts, each configured SubSpells entry is added to the effect target, and when the effect ends, those subspells are removed from the same actor when possible.

The override keeps Requiem's SubSpells.Length loop behavior and per-spell None guards. It also caches the OnEffectStart target in a local actor before adding subspells, so cell unload or effect cleanup cannot clear the stored fallback target mid-loop and turn the call into None.AddSpell().

REQ_OutfitUpdater_MQ101 preserves Requiem's NPC-only Helgen behavior: when the Helgen tower Stormcloak (dunCGStormcloakTowerA) is killed by Alduin, Ralof's and Hadvar's outfits are updated to their faction gear. It never touches the player's outfit. OnDeath now returns early unless the player is on a genuine Helgen prisoner start (still carries PrisonerClothes), so an Alternate Perspective alt-start cannot trigger it, and the Hadvar/Ralof outfit calls are guarded with "If actor && actor.Is3DLoaded()" so unloaded companions cannot log native-object errors.
