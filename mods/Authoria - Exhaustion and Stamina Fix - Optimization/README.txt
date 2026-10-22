Authoria - Exhaustion and Stamina Fix - Optimization
=== What it overrides ===
REQ_AttackStaminaDrain.pex  ->  attached to REQ_Effect_Mechanics_Stress_Attacking_
(6AD103:Requiem.esp), Requiem's "Exhaustion from weapon usage". That magic effect is
a ConstantEffect ability placed on the attacking actor; while it is alive the script
polls every 0.1s and toggles the helper ability BlockRemover
(REQ_Stress_Attacking_End, 6B203A:Requiem.esp) to make Requiem re-evaluate whether the
attack stamina drain should end. On shutdown it strips BlockRemover and the drain
ability Drainspell (REQ_Stress_Attacking, 6AA964:Requiem.esp) from the actor so it is
not left stuck in an exhaustion state.

=== The bug ===
The attack-stress effect is added/removed rapidly during combat, so OnEffectStart and
OnUpdate can run AFTER this ActiveMagicEffect has already been disposed. A disposed
effect has no bound native object (the Papyrus stack shows the owner as [None]), and
any NATIVE call on Self then fails with:

    Error: Unable to call RegisterForSingleUpdate - no native object bound to the
    script object, or object is of incorrect type

In heavy combat this spammed the Papyrus log (e.g. ~28 of these per dungeon clear).
RegisterForSingleUpdate, UnregisterForUpdate and Dispel are all native, so none of
them can be used to "stop" the loop from inside a disposed instance — calling
UnregisterForUpdate just moves the same error to a different line.

=== The fix ===
Gate every native Self-call behind a (Self == None) check. That comparison is a handle
test, not a native call, so it is always safe and it is exactly when the engine reports
the owner as [None]. This restores the guard Requiem's own original script used
(`If !Shutdown && self != None`) which the upstream "Exhaustion and Stamina Fix"
rewrite had dropped while also adding the offending UnregisterForUpdate call.

  - OnEffectStart : only RegisterForSingleUpdate / Dispel if Self != None.
  - OnUpdate      : if Self == None (or Shutdown), strip the abilities defensively and
                    return WITHOUT re-registering; otherwise refresh and re-register.
  - OnEffectFinish / OnCellDetach : Cleanup() only (no native Self-calls).
  - Cleanup() and the BlockRemover refresh act only on Target (a live Actor), never on
    Self, so they remain safe even on a disposed instance.

Gameplay is unchanged: the 0.1s refresh and the on-shutdown spell removal behave exactly
as before. The defensive strip in the disposed OnUpdate path also hardens against the
original "stuck exhaustion / no stamina recovery" bug this mod family was made to fix.
