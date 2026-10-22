;/* OstimScaling
* * native bridge into OstimScaling.dll (Authoria height-aware scene scaling)
* * called by this mod's OSKSE.psc override -- not meant for other addons
*/;
ScriptName OstimScaling Hidden

;/* GetRmScale
* * returns the anchor-corrected rmHeight for an actor in a managed OStim
* * scene, so OStim's own scaling formula anchors the scene to the reference
* * actor's true size instead of the animation baseline.
* *
* * @return: the corrected factor, or 0.0 when the actor isn't managed
* *          (creature / solo scene) -- callers must fall back to the vanilla
* *          RaceMenu read on 0.0
*/;
float Function GetRmScale(Actor akActor, bool isFemale) Global Native
