Scriptname Authoria_LydiaWeightFix extends ActiveMagicEffect
{THE FIX, from evidence. Diagnostic read her head shape's ShaderTintColor
 (NiOverride key 7) = 0,0,0 at first load and it stays 0 -> face composites
 diffuse*facetint*BLACK = dark. RaceMenu (SKEEHooks.cpp UpdateModelSkin_Hooked)
 writes the actor's skin tint there ONLY on a model update (setnpcweight); the
 first-load path (ActorUpdateManager) never does. So: write her record's skin
 tint (HumanFemaleSkinWhite02 = 206,205,204) as a PERSISTENT node override on the
 head shape. Persistent node overrides ARE re-applied by RaceMenu at every load.
 No weight, no race, no rebuild, no console. Then read it back and print proof.}

Int Property TintRGB = 0xCECDCC Auto   ; 206,205,204 = her record tint (HumanFemaleSkinWhite02)
Actor kTarget
Int   iTries = 0

String Function Col(Int c)
    Int r = Math.LogicalAnd(Math.RightShift(c, 16), 255)
    Int g = Math.LogicalAnd(Math.RightShift(c, 8), 255)
    Int b = Math.LogicalAnd(c, 255)
    Return r + "," + g + "," + b
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
    kTarget = akTarget
    RegisterForSingleUpdate(1.0)
EndEvent

Event OnUpdate()
    If kTarget == None || kTarget.IsDead()
        Return
    EndIf
    iTries += 1
    If !kTarget.Is3DLoaded()
        If iTries < 30
            RegisterForSingleUpdate(1.0)
        EndIf
        Return
    EndIf
    Int before = NiOverride.GetNodePropertyInt(kTarget, false, "00UBE_FemaleHead", 7, -1)
    ; write the missing skin tint onto the head shape, persist so RaceMenu re-applies on every load
    NiOverride.AddNodeOverrideInt(kTarget, true, "00UBE_FemaleHead", 7, -1, TintRGB, true)
    NiOverride.ApplyNodeOverrides(kTarget)
    Utility.Wait(0.5)
    Int after = NiOverride.GetNodePropertyInt(kTarget, false, "00UBE_FemaleHead", 7, -1)
    ConsoleUtil.PrintMessage("[LydiaTint] fix: before=" + Col(before) + " wrote=" + Col(TintRGB) + " after=" + Col(after) + " persisted=" + NiOverride.HasNodeOverride(kTarget, true, "00UBE_FemaleHead", 7, -1))
EndEvent

Event OnCellLoad()
    ; belt-and-braces: re-assert if she reloads before RaceMenu's flush lands
    iTries = 0
    RegisterForSingleUpdate(1.0)
EndEvent
