Scriptname REQ_AttackStaminaDrain extends ActiveMagicEffect

; Host: REQ_Effect_Mechanics_Stress_Attacking_ (6AD103:Requiem.esp), Requiem's
; "Exhaustion from weapon usage" — a ConstantEffect ability put on the attacking
; actor. While alive this polls every 0.1s, toggling BlockRemover
; (REQ_Stress_Attacking_End, 6B203A) to make Requiem re-evaluate whether the attack
; stamina drain should end; on shutdown it strips BlockRemover plus the drain ability
; Drainspell (REQ_Stress_Attacking, 6AA964) so the actor isn't left stuck in an
; exhaustion state with no stamina recovery.
;
; The attack-stress effect is added/removed rapidly in combat, so OnEffectStart and
; OnUpdate can run AFTER this ActiveMagicEffect has already been disposed. Once that
; happens the script object has no bound native object (the stack frame owner shows
; as [None]), and ANY native call on Self throws
; "no native object bound to the script object" — that includes RegisterForSingleUpdate,
; UnregisterForUpdate and Dispel, so none of those can be used to "stop" the loop.
; The only safe test is (Self == None): a handle compare, not a native call. We gate
; every native Self-call behind it. Cleanup()/RefreshBlockRemover() touch only Target
; (a live Actor), never Self, so they are safe to run even on a disposed instance.

Spell Property BlockRemover Auto
Spell Property Drainspell Auto

Actor Target
Bool Shutdown

Event OnEffectStart(Actor akTarget, Actor akCaster)
    if akTarget == None || !akTarget.Is3DLoaded()
        if Self != None
            Dispel()
        endif
        return
    endif

    Target = akTarget
    Shutdown = false

    RefreshBlockRemover()

    ; Skip registration if the effect was disposed during start (Self unbound).
    if Self != None
        RegisterForSingleUpdate(0.1)
    endif
EndEvent

Event OnUpdate()
    ; Self == None => the effect was disposed while this update was queued. Don't make
    ; any native Self-call; strip the abilities defensively so exhaustion can't get
    ; stuck, then stop the loop.
    if Self == None || Shutdown
        Cleanup()
        return
    endif

    if Target == None || !Target.Is3DLoaded()
        Cleanup()
        return
    endif

    RefreshBlockRemover()

    RegisterForSingleUpdate(0.1)
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
    Cleanup()
EndEvent

Event OnCellDetach()
    Cleanup()
EndEvent

; Add+remove the helper ability to force Requiem to re-check the drain. Acts only on
; Target (a live Actor), so it is safe even when Self is unbound.
Function RefreshBlockRemover()
    if Target != None && BlockRemover != None
        Target.AddSpell(BlockRemover, false)
        Target.RemoveSpell(BlockRemover)
    endif
EndFunction

Function Cleanup()
    if Shutdown
        return
    endif

    Shutdown = true

    if Target != None
        if BlockRemover != None
            Target.RemoveSpell(BlockRemover)
        endif
        if Drainspell != None
            Target.RemoveSpell(Drainspell)
        endif
    endif

    Target = None
EndFunction
