ScriptName REQ_ConditionalSubEffect extends ActiveMagicEffect
{This script can be applied to a magic effect which is conditionalized at the spell level (and thus temporarily dispelled when the conditions are not satisfied) to apply another spell (ability type) only when the condition is currently fulfilled. Use this to deliver spells that require rescaling at runtime, like mass-dependent blocking costs.}

Spell[] Property SubSpells Auto
Actor target

Event OnEffectStart(Actor akTarget, Actor akCaster)
    If akTarget == None
        Return
    EndIf

    target = akTarget
    Actor effectTarget = akTarget

    Int idx = 0
    Int n = SubSpells.Length
    While idx < n
        Spell s = SubSpells[idx]
        If s != None
            effectTarget.AddSpell(s, False)
        EndIf
        idx += 1
    EndWhile
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
    Actor cleanupTarget = akTarget
    If cleanupTarget == None
        cleanupTarget = target
    EndIf

    If cleanupTarget == None
        target = None
        Return
    EndIf

    Int idx = 0
    Int n = SubSpells.Length
    While idx < n
        Spell s = SubSpells[idx]
        If s != None
            cleanupTarget.RemoveSpell(s)
        EndIf
        idx += 1
    EndWhile

    target = None
EndEvent
