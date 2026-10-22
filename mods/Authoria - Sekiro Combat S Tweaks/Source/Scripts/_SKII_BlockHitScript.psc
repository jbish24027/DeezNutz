ScriptName _SKII_BlockHitScript extends ActiveMagicEffect

Actor SelfActor
ObjectReference BlockFX
Perk ExpBlockingPerk

magiceffect Property TimedBlockSpellMGEF Auto

spell Property StaggerSpell Auto

explosion Property SparksFXPhysics Auto

explosion Property FlashShield Auto

activator Property SparksHolder Auto

explosion Property SparksFX Auto

spell Property TimedBlockSpell Auto

explosion Property Flash Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
    SelfActor = akTarget
    ExpBlockingPerk = game.GetFormFromFile(0x00079355, "Skyrim.esm") as Perk
    RegisterForAnimationEvent(SelfActor, "blockStartOut")
EndEvent

Event OnAnimationEvent(ObjectReference akSource, string asEventName)
    if asEventName == "blockStartOut" && TimedBlockAllowed()
        TimedBlockSpell.Cast(SelfActor, SelfActor)
    endif
EndEvent

; No OnUnload/OnCellDetach cleanup: animation-event registrations are destroyed
; with the effect, and unregistering during unload races teardown on an unbound
; self ("no native object bound" log spam). Re-registration below is idempotent.
Event OnCellAttach()
    RegisterForAnimationEvent(SelfActor, "blockStartOut")
EndEvent

Event OnLoad()
    RegisterForAnimationEvent(SelfActor, "blockStartOut")
EndEvent

bool Function TimedBlockAllowed()
    ; Unarmed block (both hands empty) never parries — Sekiro timed blocks
    ; require a weapon or shield.
    if SelfActor.GetEquippedItemType(1) == 0 && SelfActor.GetEquippedItemType(0) == 0
        return false
    endif
    if !ExpBlockingPerk
        ExpBlockingPerk = game.GetFormFromFile(0x00079355, "Skyrim.esm") as Perk
    endif
    if !ExpBlockingPerk
        return true
    endif
    return SelfActor.HasPerk(ExpBlockingPerk)
EndFunction

Function AwardTimedBlockXP(Actor aggressorActor)
    if !(SelfActor == game.GetPlayer())
        return
    endif
    float xp = 5.0
    if aggressorActor
        weapon aggressorWeapon = aggressorActor.GetEquippedWeapon(false)
        if aggressorWeapon
            xp = xp + aggressorWeapon.GetBaseDamage() * 0.5
        endif
    endif
    if xp > 25.0
        xp = 25.0
    endif
    game.AdvanceSkill("Block", xp)
EndFunction

Event OnHit(ObjectReference akAggressor, form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
    if !abHitBlocked
        weapon srcWeapon = akSource as weapon
        if !(akSource as spell) && !(srcWeapon && srcWeapon.IsBow())
            return
        endif
    endif
    if !TimedBlockAllowed()
        return
    endif
    Actor aggressorActor = akAggressor as Actor
    if abHitBlocked
        if SelfActor.GetEquippedItemType(0) == 10
            SelfActor.PlaceAtMe(SparksFX, 1, false, false)
            SelfActor.PlaceAtMe(SparksFXPhysics, 1, false, false)
            if SelfActor.HasMagicEffect(TimedBlockSpellMGEF)
                SelfActor.PlaceAtMe(FlashShield, 1, false, false)
                if aggressorActor
                    if aggressorActor.GetActorValuePercentage("Stamina") > 0.1
                        aggressorActor.DamageActorValue("Stamina", SelfActor.GetActorValue("Block"))
                    else
                        StaggerSpell.Cast(akAggressor, akAggressor)
                    endif
                endif
                SelfActor.RestoreActorValue("Stamina", SelfActor.GetActorValue("Block"))
                AwardTimedBlockXP(aggressorActor)
            endif
        else
            SelfActor.PlaceAtMe(SparksFX, 1, false, false)
            SelfActor.PlaceAtMe(SparksFXPhysics, 1, false, false)
            if SelfActor.HasMagicEffect(TimedBlockSpellMGEF)
                SelfActor.PlaceAtMe(Flash, 1, false, false)
                SelfActor.PlaceAtMe(FlashShield, 1, false, false)
                if aggressorActor
                    if aggressorActor.GetActorValuePercentage("Stamina") > 0.1
                        aggressorActor.DamageActorValue("Stamina", SelfActor.GetActorValue("Block"))
                    else
                        StaggerSpell.Cast(akAggressor, akAggressor)
                    endif
                endif
                SelfActor.RestoreActorValue("Stamina", SelfActor.GetActorValue("Block"))
                AwardTimedBlockXP(aggressorActor)
            endif
        endif
    else
        if SelfActor.GetEquippedItemType(0) == 10
            if SelfActor.HasMagicEffect(TimedBlockSpellMGEF)
                SelfActor.PlaceAtMe(SparksFX, 1, false, false)
                SelfActor.PlaceAtMe(FlashShield, 1, false, false)
                debug.SendAnimationEvent(SelfActor, "BlockHitStart")
                SelfActor.RestoreActorValue("Stamina", SelfActor.GetActorValue("Block"))
                SelfActor.ClearExtraArrows()
            endif
        elseif SelfActor.HasMagicEffect(TimedBlockSpellMGEF)
            SelfActor.PlaceAtMe(SparksFX, 1, false, false)
            SelfActor.PlaceAtMe(FlashShield, 1, false, false)
            debug.SendAnimationEvent(SelfActor, "BlockHitStart")
            SelfActor.RestoreActorValue("Stamina", SelfActor.GetActorValue("Block"))
            SelfActor.ClearExtraArrows()
        endif
    endif
    GotoState("HitBuffer")
EndEvent

State HitBuffer
    Event onBeginState()
        RegisterForSingleUpdate(0.5)
    EndEvent

    Event OnUpdate()
        GotoState("")
    EndEvent

    Event OnHit(ObjectReference akAggressor, form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
    EndEvent

EndState
