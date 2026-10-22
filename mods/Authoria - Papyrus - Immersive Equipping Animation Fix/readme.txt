Authoria - Papyrus - Immersive Equipping Animation Fix

Scripts included:
- IDA_Dress_Ref_AliasScript.pex
  Guards missing ignore-keyword lookups and only calls `GetSlotMask()` after the equipped or unequipped form successfully casts to Armor. The script remains based on Helmet Toggle 2's IEA compatibility override, so the animation-skip behavior for managed helmets and hoods is preserved