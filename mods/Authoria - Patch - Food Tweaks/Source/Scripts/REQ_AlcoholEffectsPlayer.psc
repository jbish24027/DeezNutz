ScriptName REQ_AlcoholEffectsPlayer extends REQ_CoreScript
{manages player-specific alcohol effects (blur removed)}

globalvariable Property AlcoholLevelStorage Auto

Function initScript(int currentVersion, int newVersion)
    UpdatePlayerAlcoholPenalties()
EndFunction

Function shutdownScript(int currentVersion, int newVersion)
    UnregisterForUpdate()
EndFunction

Function UpdatePlayerAlcoholPenalties()
    if AlcoholLevelStorage.GetValue() > 0.0
        RegisterForUpdate(5.0)
    else
        UnregisterForUpdate()
    endif
EndFunction

Event OnUpdate()
    float Health
    float AlcoholLevel = AlcoholLevelStorage.GetValue()
    if AlcoholLevel <= 0.0
        UnregisterForUpdate()
        return
    endif
    Health = Player.GetBaseActorValue("Health")
    float Chance = (AlcoholLevel / Health - 2.0) / 2.0 ; tolerance tuned: no risk below 2x base Health, guaranteed above 4x
    if Chance >= 1.0 || Chance > 0.0 && utility.RandomFloat(0.0, 1.0) < Chance
        Player.PushActorAway(Player, 1.0)
    endif
EndEvent

