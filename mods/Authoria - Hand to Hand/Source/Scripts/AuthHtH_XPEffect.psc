Scriptname AuthHtH_XPEffect extends ActiveMagicEffect
{Hand to Hand (Authoria) - grants skill XP on each unarmed hit, drives the CSF Level/Ratio globals, and
 scales UnarmedDamage with the skill via a legendary-safe reconciliation. Perks are unlocked with the
 VANILLA perk-point pool (CSF vanilla-menu integration), so this script no longer manages a dedicated
 perk-point pool. Player-only (only the player carries the XP-driver perk that applies this effect).
 Forms fetched via GetFormFromFile so no VMAD properties are needed. Tunable constants below.}

; --- Tunable balance (Requiem) ---
float Property fBaseXPPerHit         = 3.0   Auto  ; base skill-usage per unarmed hit
float Property fBonusXPPerLevel       = 0.15  Auto  ; extra per current level
float Property fUnarmedDamagePerLevel = 0.75  Auto  ; +UnarmedDamage per skill level above base (Requiem-tuned)
int   Property iSkillBase             = 10    Auto  ; starting skill level (matches AuthHtH_Level default)
int   Property iSkillCap              = 100   Auto

; --- XP-to-next-level curve: returns skill-usage needed to advance FROM aLevel to aLevel+1 ---
float Function XPNeeded(int aLevel)
    return 30.0 + 12.0 * aLevel
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
    ; Touch delivery -> akTarget is the struck reference. No XP from corpses or non-actor hits.
    if akTarget == None || akTarget.IsDead()
        return
    endif
    string f = "Authoria - Hand to Hand.esp"
    GlobalVariable LevelGlob = Game.GetFormFromFile(0x800, f) as GlobalVariable
    GlobalVariable RatioGlob = Game.GetFormFromFile(0x801, f) as GlobalVariable
    if LevelGlob == None || RatioGlob == None
        return
    endif
    Actor pl = Game.GetPlayer()

    int curLevel = LevelGlob.GetValue() as int
    if curLevel < iSkillCap
        float xpGain   = fBaseXPPerHit + fBonusXPPerLevel * curLevel
        float newRatio = RatioGlob.GetValue() + (xpGain / XPNeeded(curLevel))
        while newRatio >= 1.0 && curLevel < iSkillCap
            newRatio -= 1.0
            curLevel += 1
            LevelGlob.SetValue(curLevel as float)
            ; Styled CSF HUD "Hand to Hand increased to X" via the native v3 API.
            CustomSkills.ShowSkillIncreaseMessage("AuthoriaHandToHand", curLevel)
        endwhile
        if curLevel >= iSkillCap
            RatioGlob.SetValue(1.0)
        else
            RatioGlob.SetValue(newRatio)
        endif
    endif

    ; Keep the flat UnarmedDamage scaling in sync with the current level (legendary-safe).
    ReconcileUnarmedDamage(pl, curLevel, f)
EndEvent

; Target flat bonus = fUnarmedDamagePerLevel * (level - base). Reconcile against what we have already
; applied (tracked in AuthHtH_DmgApplied 0x825) so a Legendary reset (level -> base) REMOVES the bonus
; instead of leaving it stacked, and an existing save (sentinel < 0) adopts its current contribution
; once without double-applying. New games seed the tracker to 0 in the init quest.
Function ReconcileUnarmedDamage(Actor pl, int curLevel, string f)
    GlobalVariable AppliedGlob = Game.GetFormFromFile(0x825, f) as GlobalVariable
    if AppliedGlob == None || pl == None
        return
    endif
    float target = fUnarmedDamagePerLevel * ((curLevel - iSkillBase) as float)
    if target < 0.0
        target = 0.0
    endif
    float applied = AppliedGlob.GetValue()
    if applied < 0.0
        ; migration sentinel: adopt the old script's existing contribution without re-applying it.
        AppliedGlob.SetValue(target)
        return
    endif
    float delta = target - applied
    if delta != 0.0
        pl.ModActorValue("UnarmedDamage", delta)
        AppliedGlob.SetValue(target)
    endif
EndFunction
