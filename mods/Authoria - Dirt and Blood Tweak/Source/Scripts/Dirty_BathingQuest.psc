Scriptname Dirty_BathingQuest extends Quest

; ============================================================================
; ARR MERGE PATCH - Dirty_BathingQuest
; Base   : "Authoria - Dirt and Blood Tweak" version (adds free-camera during
;          bathing, gated by global 0x805 in Authoria - Patch - Dirt and Blood
;          Tweaks.esp).
; Merged : "Malignis Animations - BiSR - Dirt and Blood Patch" version
;          (WashCustom -> Debug.SendAnimationEvent "mzinBatheA5_T4", the FNIS
;          custom Bathing-in-Skyrim animation, + DryCustom).
;
; WHY: In ARR's load order "Authoria - Dirt and Blood Tweak" overrides this
;      loose script and WON the conflict over the Malignis patch, so the game
;      ran Authoria's version which sent the vanilla IdleWarmArms/IdleWipeBrow
;      idles and NEVER sent "mzinBatheA5_T4" -> the immersive Malignis tub
;      animation never fired. This merged copy keeps Authoria's free-cam AND
;      restores Malignis's custom animation. Load it ABOVE the Authoria tweak.
; ============================================================================

GlobalVariable Property Dirty_WashingAutomaticClothes auto
Spell Property Dirty_SoapEffectSpell Auto
Spell Property Dirty_NPCisWashingNow Auto
Formlist property Dirty_ListofSoaps Auto
Formlist property Dirty_ListofIgnoredItems Auto
GlobalVariable Property Dirty_SoundEffect Auto
Sound Property Dirty_WashingMarkerSound auto
Spell Property Dirty_Spell_Dirt1 Auto
Spell Property Dirty_Spell_Dirt2 Auto
Spell Property Dirty_Spell_Dirt3 Auto
Spell Property Dirty_Spell_Dirt4 Auto
Spell Property Dirty_Spell_Blood1 Auto
Spell Property Dirty_Spell_Blood2 Auto
Spell Property Dirty_Spell_Blood3 Auto
Spell Property Dirty_Spell_Blood4 Auto
Spell Property Dirty_Spell_Clean Auto
Formlist Property Dirty_BathingActors Auto
GlobalVariable Property Dirty_PlayerBathingAnimation Auto
GlobalVariable Property Dirty_NPCBathingAnimation Auto

import PO3_SKSEFunctions

Function PlayBatheAnimation(Actor bathingActor, bool isPlayer, bool removeSoap = false)
    If (Dirty_BathingActors.HasForm(bathingActor))
        If isPlayer
            Debug.Notification("You are already bathing!")
        Else
            Debug.Notification(bathingActor.GetDisplayName() + " is already bathing!")
        EndIF
        return
    EndIf

    Dirty_BathingActors.AddForm(bathingActor)
    Form[] Clothing
    weapon weapon1
    weapon weapon2
	Light Torch
	Armor Shield

    If removeSoap
        bathingActor.RemoveItem(FindFirstItemInList(bathingActor, Dirty_ListofSoaps))
    EndIf
    If isPlayer && ShouldAnimateBathing(bathingActor, isPlayer)
        ; force 3rd person
        Game.ForceThirdPerson()
        Game.DisablePlayerControls(True, True, True, False, True, False, True)
        ; Authoria: free camera during bathing
        GlobalVariable freeCam = Game.GetFormFromFile(0x00000805, "Authoria - Patch - Dirt and Blood Tweaks.esp") as GlobalVariable
        if freeCam && freeCam.GetValue() == 1 && Game.GetCameraState() != 3
            MiscUtil.SetFreeCameraState(true, 5.0)
        endIf
    EndIF



    If Dirty_WashingAutomaticClothes.GetValue() == 1
        If Game.IsPluginInstalled("All Geared Up Derivative.esp")
            If isPlayer
                Spell Display = Game.GetFormFromFile(0x02003000, "All Geared Up Derivative.esp") As Spell
                bathingActor.RemoveSpell(Display)
            Else
                GlobalVariable ItemsNPC = Game.GetFormFromFile(0x0200A100, "All Geared Up Derivative.esp") As GlobalVariable
                ItemsNPC.SetValue(0)
            EndIf
        endif

        ; --- Combat gear FIRST, with abPreventEquip=True. Weapons and shields carry
        ;     engine auto-equip memory that a plain (non-preventing) unequip does NOT
        ;     clear, so across the long bathing animation the engine re-draws them onto
        ;     the naked body (the reported bug: weapon/shield stay on). Prevent-equip
        ;     holds them off; the forced EquipItemEx re-dress below clears the flag.
        ;     Body armor has no such memory, so the armor loop stays non-preventing.
        ;     Capturing BEFORE the armor loop also fixes the shield reading as None
        ;     (the loop had already stripped slot 39, leaving the old Shield var dead).
        Weapon1 = bathingActor.GetEquippedWeapon()
        Weapon2 = bathingActor.GetEquippedWeapon(True)
        Torch = bathingActor.GetEquippedObject(0) as Light
        Shield = bathingActor.GetEquippedShield()
        If Weapon1
            bathingActor.UnequipItem(Weapon1, True, True)
        EndIf
        If Weapon2
            bathingActor.UnequipItem(Weapon2, True, True)
        EndIf
        If Torch
            bathingActor.UnequipItem(Torch, True, True)
        EndIf
        If Shield
            bathingActor.UnequipItem(Shield, True, True)
        EndIf

        Clothing = new Form[33]
        Int Index = Clothing.Length

        While Index
            Index -= 1
            Int ArmorSlotMask = Armor.GetMaskForSlot(Index + 30)
            Clothing[Index] = bathingActor.GetWornForm(ArmorSlotMask)
            If Clothing[Index]
                If !Dirty_ListofIgnoredItems.HasForm(Clothing[Index])
					bathingActor.UnequipItem(Clothing[Index], False, True)
				Else
					Clothing[Index] = None
				EndIf
			EndIf
        EndWhile
    endif

    Utility.Wait(0.1)
    if isPlayer && Dirty_SoundEffect.GetValue() == 1
        int instanceID = Dirty_WashingMarkerSound.play(bathingActor)
        Sound.SetInstanceVolume(instanceID, 1.0)
    endif
    ; --- Wash phase — animation set chosen in the MCM via Authoria_BathAnimStyle
    ;     (0 = Default Bathing-in-Skyrim idles, 1 = Malignis immersive tub). Resolved
    ;     at runtime, matching how the free-cam global is read; applies to whoever is
    ;     animating (player or NPC). Defaults to Malignis if the global is missing. ---
    GlobalVariable animStyle = Game.GetFormFromFile(0x00000808, "Authoria - Patch - Dirt and Blood Tweaks.esp") as GlobalVariable
    bool useDefaultAnim = animStyle && animStyle.GetValue() == 0
    if useDefaultAnim
        Lather(bathingActor, isPlayer)
        Wash(bathingActor, isPlayer)
        Rinse(bathingActor, isPlayer)
    else
        WashCustom(bathingActor, isPlayer)
    endif

    if isPlayer
        bathingActor.RemoveSpell(Dirty_SoapEffectSpell)
        bathingActor.RemoveSpell(Dirty_Spell_Dirt1)
        bathingActor.RemoveSpell(Dirty_Spell_Dirt2)
        bathingActor.RemoveSpell(Dirty_Spell_Dirt3)
        bathingActor.RemoveSpell(Dirty_Spell_Dirt4)
        bathingActor.RemoveSpell(Dirty_Spell_Blood1)
        bathingActor.RemoveSpell(Dirty_Spell_Blood2)
        bathingActor.RemoveSpell(Dirty_Spell_Blood3)
        bathingActor.RemoveSpell(Dirty_Spell_Blood4)
        bathingActor.AddSpell(Dirty_Spell_Clean, False)
    else
        bathingActor.RemoveSpell(Dirty_SoapEffectSpell)
        bathingActor.AddSpell(Dirty_NPCisWashingNow)
    endIf

    ; --- Dry phase — same style split as the wash phase above. ---
    if useDefaultAnim
        Dry(bathingActor, isPlayer)
    else
        DryCustom(bathingActor, isPlayer)
    endif

    if isPlayer
        if ShouldAnimateBathing(bathingActor, isPlayer)
            ; Authoria: exit free camera
            if Game.GetCameraState() == 3
                MiscUtil.SetFreeCameraState(false)
            endIf
            Game.EnablePlayerControls()
        endIf
    else
        bathingActor.RemoveSpell(Dirty_NPCisWashingNow)
    endIf


    ;re-equip
    If Dirty_WashingAutomaticClothes.GetValue() == 1
        If Game.IsPluginInstalled("All Geared Up Derivative.esp")
            If isPlayer
                Spell Display = Game.GetFormFromFile(0x02003000, "All Geared Up Derivative.esp") As Spell
                bathingActor.AddSpell(Display, false)
            Else
                GlobalVariable ItemsNPC = Game.GetFormFromFile(0x0200A100, "All Geared Up Derivative.esp") As GlobalVariable
                ItemsNPC.SetValue(1)
            EndIf
        endif

        Int ClothingIndex = Clothing.Length
        While ClothingIndex
            ClothingIndex -= 1
            If Clothing[ClothingIndex]
                bathingActor.EquipItem(Clothing[ClothingIndex], False, True)
            EndIf
        EndWhile
        If Weapon1
			bathingActor.EquipItemEx(Weapon1, 1, false, true)
		EndIf
		If Weapon2
			bathingActor.EquipItemEx(Weapon2, 2, false, true)
		EndIf
		If Torch
			bathingActor.EquipItemEx(Torch, 0, false, true)
		EndIf
		If Shield
			bathingActor.EquipItemEx(Shield, 0, false, true)
		EndIf
    Endif
    Dirty_BathingActors.RemoveAddedForm(bathingActor)
EndFunction

Function Lather(Actor bathingActor, bool isPlayer)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
        Debug.SendAnimationEvent(bathingActor, "IdleForceDefaultState")
        Utility.Wait(0.1)
        Debug.SendAnimationEvent(bathingActor, "IdleSearchingChest")
        Utility.Wait(3.0)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
    endIf
    bathingActor.AddSpell(Dirty_SoapEffectSpell, False)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
        Utility.Wait(0.3)
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(1.0)
        Debug.SendAnimationEvent(bathingActor, "IdleWipeBrow")
        Utility.Wait(3.0)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
    endIf
EndFunction

Function Wash(Actor bathingActor, bool isPlayer)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
        ; wash
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
        Debug.SendAnimationEvent(bathingActor, "IdleWarmArms")
        Utility.Wait(1.5)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(1.0)
    endIf
EndFunction

Function Rinse(Actor bathingActor, bool isPlayer)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
        ; rinse off
        Debug.SendAnimationEvent(bathingActor, "IdleWarmHandsCrouched")
        Utility.Wait(3.0)
    endIf
EndFunction

Function Dry(Actor bathingActor, bool isPlayer)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
        Utility.Wait(1.0)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(1.0)
        Debug.SendAnimationEvent(bathingActor, "IdleWipeBrow")
        Utility.Wait(3.0)
        Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.3)
    endIf
EndFunction

Function WashCustom(Actor bathingActor, bool isPlayer)
	bathingActor.AddSpell(Dirty_SoapEffectSpell, False)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
		Debug.SendAnimationEvent(bathingActor, "mzinBatheA5_T4")
		Utility.Wait(58.0)
    endIf
EndFunction

Function DryCustom(Actor bathingActor, bool isPlayer)
    if (ShouldAnimateBathing(bathingActor, isPlayer))
		Utility.Wait(6.2)
		; Authoria: drop the soap AnimObject (Authoria_AnimObjectSoap, attached by the
		; Malignis FNIS definitions) before the animation is torn down. The ANIO's own
		; UnloadEvent is AnimObjectUnequip; sending it here means a bath that ends early
		; can't leave the bar stuck in the actor's hand.
		Debug.SendAnimationEvent(bathingActor, "AnimObjectUnequip")
		Debug.SendAnimationEvent(bathingActor, "IdleForceDefaultState")
        Utility.Wait(0.1)
		Debug.SendAnimationEvent(bathingActor, "IdleStop")
        Utility.Wait(0.1)
    endIf
EndFunction

bool Function ShouldAnimateBathing(Actor bathingActor, bool isPlayer)
    return (Dirty_PlayerBathingAnimation.GetValue() == 1 && isPlayer) || (Dirty_NPCBathingAnimation.GetValue() == 1 && !isPlayer)
EndFunction
