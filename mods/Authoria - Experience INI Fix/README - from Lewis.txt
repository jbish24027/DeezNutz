Experience.ini in "Authoria - MCM and INI Settings" uses old key names that Experience 3.7.3 no longer reads

The file uses setting names from an older Experience version. The 3.7.3 DLL doesn't contain those names (checked against the DLL's strings), so these settings are silently ignored and Experience's built-in defaults apply instead:

  Old key (ignored)          New key (3.7.3)          List value   Default actually used
  fXPReadingMult             fReadingMult             0.50         2.0  (books give 4x the intended XP)
  fXPGroupFactor             fGroupFactor             0.3          0.2
  fXPKillingMult             fKillingMult             1.00         1.0  (same)
  iXPObjectives              iXPQuestObjectives       10           10   (same)
  iXPClearStandingStones     iXPClearStandingStone    40           (none)
  iXPDiscStandingStones      iXPDiscStandingStone     10           (none)
  iXPClear/DiscImperialCamp  iXPClear/DiscMilitaryCamp  0          (none)

These have no 3.7.3 equivalent and do nothing: bForceLvlMeter, bLocClearingFix, iXPLevelRange (replaced by fLevelFactor / fMaxLevelMult), StormcloakCamp, RavenRock, Capitol.

Also, saving Experience's MCM in game rewrites the file, keeps only the keys the DLL knows, and drops the old ones.

Fix: the attached SKSE\Plugins\Experience.ini is the 2.9.9 list file with those keys renamed and the dead ones removed. All values are otherwise unchanged.
