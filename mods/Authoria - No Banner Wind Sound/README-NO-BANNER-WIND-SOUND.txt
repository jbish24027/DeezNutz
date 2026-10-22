Authoria - No Banner Wind Sound
================================
Created 2026-09-06 by houseCARL / Claude for the "windy sound coming from banners" complaint.

WHAT THE SOUND IS
-----------------
Every hanging banner that makes the flapping / wind noise plays the same looping ambient sound
descriptor:  AMBBannerRockCairnLP  (FormID 044EC5 in Skyrim.esm).
It is attached as the "Looping Sound" (SNAM) of 50 Movable Static (MSTT) banner objects.
No other banner-like object in the load order carries any other loop (checked all 375 MSTTs
that have a looping sound; only this descriptor appears on cloth-type objects).

The descriptor plays two files, picked at random (paths written with forward slashes):
  sound/fx/amb/amb_bannerrockcairn_lp.wav      (mono, 22050 Hz, 16-bit, 7.88 s)
  sound/fx/amb/amb_bannerrockcairn_02_lp.wav   (mono, 22050 Hz, 16-bit, 7.00 s)
In this profile the files the game actually plays are the LOOSE copies shipped by
"Regional Sounds Expansion (2.1.0)" (loose beats the copies in Audio Overhaul Skyrim.bsa and
Skyrim - Sounds.bsa).

Descriptor override chain (load order, winner last):
  Skyrim.esm > Audio Overhaul Skyrim.esp > Immersive Sounds - Compendium.esp >
  AOS_ISC_Integration.esp > Regional Sounds Expansion.esp > Malignis_Essentials.esp (WINNER)
Malignis_Essentials.esp (an animation mod) carries a stray override of this descriptor that
puts every value back to vanilla: static attenuation 3.08 dB instead of AOS's 7.93 / RSE's 9,
priority 128 instead of 255, vanilla category and output model, plus a bogus
"Alternate Sound For" link to its own MALSD_shock_draw sound. Net effect: the banner loop
plays LOUDER than any of the installed sound mods intended.

WHAT THIS MOD DOES
------------------
Ships two silent WAVs at the same two paths, same format and length as the RSE files.
Placed above Regional Sounds Expansion (2.1.0) in MO2 priority, they win the VFS, so every
banner loop plays silence. No plugin, no record edits, no save impact. The Malignis override
is left alone (it no longer matters for banners once the files are silent).

WHAT GOES QUIET
---------------
All 50 objects that carry the loop:
  Vanilla hanging banners (clutter/banners/GenericBanner*):
    GenericBannerRed03/04, GenericBannerBlue03/04, GenericBannerGreen01-04, GenericBannerYellow01-04
    (Red01/02 and Blue01/02 never had the sound)
  Rock cairn cloth strips near Nordic ruins: RockCairnBanner01, RockCairnBanner02
  Apocrypha banners (Dragonborn): ApoBanner03, ApoBanner04
  Beyond Skyrim Bruma: CYRImperialBanner03/04, CYRSecondEraImperialBanner03/04
  Vigilant: zzzCH*Banner*_03 and _04 (Alessian x3, Molag, Varla, Mara, Sithis, Vamp, Dibella,
    Drozel, Stendarr) = 22 objects
  JK's The Bannered Mare: XJKBannGenericBannerYellow01
  JK's Castle Volkihar: XJKCVbanner_YellowBorder03, _BlackBorder03, _BlackandGoldBorder03
  Legacy of the Dragonborn: DBM_StendarrBanner
  Wyrmstooth: WTMarauderBanner03
  ClefJ's Fort Dawnguard: aaaCJDBanner3
  Ivy Stendarr's Beacon Overhaul: IvyStendarrBannerWind
Many of these are currently won by PG_1.esp (ParallaxGen output), which only swaps the model
path and forwards the sound link unchanged. That is why a plugin patch on the MSTT records
was NOT used: it would have to load after PG_1.esp to win, which the load-order rules forbid.
SkyPatcher was not an option either: it has no Movable Static or Sound Descriptor support.

PLACEMENT
---------
One modlist.txt line directly BEFORE "+Regional Sounds Expansion (2.1.0)" in every profile
(earlier line = higher priority = wins). No plugin, so plugins.txt / loadorder.txt untouched.

TO REVERT
---------
Disable or delete this mod. Regional Sounds Expansion's files take over again.

TO MAKE IT QUIET INSTEAD OF SILENT
----------------------------------
Replace the two WAVs with gain-reduced copies of the RSE files (same names), or override the
descriptor's StaticAttenuation in a light patch loaded after Malignis_Essentials.esp.
