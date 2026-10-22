Papyrus Log Fix - Immersive Dialogue Expansion - Thalmor
Fixes the aaThalmor Papyrus log cluster from optional quest aliases that may not fill before the scripts run.
guard optional actor aliases before calling IsDead(), GetActorBase(), MoveTo(), Disable(), package, faction, and actor-value functions. Estormo's startup Assistance actor value is changed from invalid 3 to valid 2, preserving his intended ally/protector behavior around Ancano.
