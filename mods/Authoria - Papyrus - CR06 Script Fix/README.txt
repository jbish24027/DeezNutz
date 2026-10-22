Authoria - Papyrus - CR06 Script Fix

This mod fixes the CR06 Papyrus log error where Family Heirloom can try to advance its startup stage while the engine does not consider it started by Story Manager.

It adds a small guard to CR06QuestScript.Setup(): if CR06 is not running, the setup call exits before registering the radiant quest or calling the inherited SetStage(1). Valid Story Manager starts still use the original parent setup path.