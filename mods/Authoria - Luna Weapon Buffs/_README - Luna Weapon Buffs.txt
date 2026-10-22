Authoria - Luna Weapon Buffs (2026-09-06)
=========================================
Makes Luna's favorited weapons hit three times harder. No plugin: one SkyPatcher INI, applied at
game load after every plugin (including Requiem for the Indifferent), so nothing needs re-running.

  weapon                      before   after
  Silver Keyblade (1H)          180  ->  540
  Silver Great Keyblade (2H)    290  ->  870
  DD - Einar Bow                360  -> 1080
  (crit damage follows base damage, Requiem style)

For scale: Requiem's Daedric Sword is 90, Daedric Greatsword 144, Daedric Heavy Bow 120.

Which weapons: read out of the save (Save33, 2026-09-06 08:43) - the three weapons carrying the
favorite flag in Luna's inventory. Other favorites (Dwemer Quiver, Sketchbook) are not weapons.

To retune: edit the numbers in
  SKSE\Plugins\SkyPatcher\weapon\Authoria - Luna Weapon Buffs\Luna favorites.ini
To remove: disable this mod in MO2. Save-safe either way.
