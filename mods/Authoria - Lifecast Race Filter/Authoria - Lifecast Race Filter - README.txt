Authoria - Lifecast Race Filter
================================

What it is
  A patched copy of Lifecast's MeridianUI\Lifecast\racesex.js. It hides the
  wrong-sex race twins in Lifecast's Race list, the same way
  RacemenuSexDisabler.ini does for RaceMenu:
    - while FEMALE: the vanilla races that have a UBE twin are hidden
      (Breton, Dunmer, Altmer, Imperial, Nord, Orc, Redguard, Bosmer).
    - while MALE: the 8 UBE_AllRace.esp races and Ohmes-Raht are hidden.
  Display only. Race indices are untouched, so picking a race sends Lifecast's
  own index. It fails open: unknown sex, an unreadable id, the current race,
  or a filter that would empty the list all leave rows visible.
  Switch it off by setting AUTHORIA_RACE_FILTER = false in the file.

Built against
  Lifecast 1.4.0 (Nexus 193940), file MeridianUI\Lifecast\racesex.js
  upstream md5 = 79a0584ca26ab343e9b9677023ccaa07

ON EVERY LIFECAST UPDATE
  Check the md5 of the NEW upstream racesex.js. If it is no longer
  79a0584ca26ab343e9b9677023ccaa07, this file is stale: re-apply the
  "AUTHORIA" block onto the new file (it is a pure addition - one block before
  renderRaces() and four lines inside it) or turn this mod off. Until then
  this mod must sit ABOVE (win over) the "Lifecast" mod in MO2.

2026-10-18 FIX: MeridianUI only serves page files that physically sit inside the owning mod's folder (it canonicalises the path, and under MO2 an override from another mod folder lands outside it -> 404). Shipping racesex.js from this folder made Lifecast lose its Race list AND Sex buttons. The patched racesex.js now lives INSIDE "Lifecast\MeridianUI\Lifecast\racesex.js" (original backed up in _backups\2026-10-18 - lifecast racesex move). This folder now only holds this README. On every Lifecast update: re-apply the patch into the Lifecast folder itself (original md5 79a0584ca26ab343e9b9677023ccaa07).
