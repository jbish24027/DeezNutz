Scriptname AuthoriaGreenPactWipe extends ActiveMagicEffect
{Green Pact violation extension (attached to REQ_Apo_BosmerExclusionNegEffect):
 when the punishment applies, wipe the player's active food buffs - including
 the violating food's own effects. A delayed second pass catches effects that
 apply after the first sweep. FoodEffects lists dispellable food-benefit MGEFs
 only (curated: no detrimental effects, no shared potion effects).}

FormList Property FoodEffects Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
    WipeFoodEffects(akTarget)
    Utility.Wait(1.0)
    if Self == None
        return
    endif
    WipeFoodEffects(akTarget)
EndEvent

Function WipeFoodEffects(Actor akTarget)
    if akTarget == None
        return
    endif
    MagicEffect[] active = PO3_SKSEFunctions.GetActiveEffects(akTarget, false)
    int i = active.Length
    while i > 0
        i -= 1
        MagicEffect m = active[i]
        if m && FoodEffects.HasForm(m)
            DbSkseFunctions.DispelMagicEffectOnRef(akTarget, m, None)
        endif
    endwhile
EndFunction
