Scriptname AuthHtH_KnockoutEffect extends ActiveMagicEffect
{Hand to Hand (Authoria) - Knockout. Applied (via the Knockout perk's ApplyCombatHitSpell) only when the
 player power-attacks an unarmed strike into a target below half Health. Rolls a chance to knock the
 target down (ragdoll in place via a zero-force PushActorAway).}

float Property fKnockoutChance = 0.25 Auto  ; chance to knock down on a qualifying hit (Requiem-tuned)

Event OnEffectStart(Actor akTarget, Actor akCaster)
    if akTarget == None
        return
    endif
    if Utility.RandomFloat(0.0, 1.0) <= fKnockoutChance
        akTarget.PushActorAway(akTarget, 0.0)   ; 0 force = knockdown in place
    endif
EndEvent
