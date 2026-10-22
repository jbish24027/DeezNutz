Scriptname ImmersiveHuntingPlayerAlias extends ReferenceAlias  

Import PO3_SKSEFunctions
Import PO3_Events_Alias

ImmersiveHuntingFunctions Property ihFunctions Auto
ReferenceAlias Property ihAnimalAlias Auto

Actor Property PlayerRef Auto

FormList Property IH_FL_CookingIgnoreList Auto
FormList Property IH_FL_CookingAllowList Auto

Spell Property IH_AnimSpellCarryCarcass Auto 

ObjectReference Property IH_CarcassMarker Auto

MagicEffect ForwardMGEF 
MagicEffect LeftMGEF 
MagicEffect BackwardMGEF 
MagicEffect RightMGEF 

Bool isMGEFRegistered
Bool isHitRegistered
Bool isPickupRegistered
Bool isControlRegistered
Bool isLootMenuRegistered
Bool isDrawnRegistered
Bool wasAnimal
Bool isBusy
Bool isExtenderInstalled
Bool isItemCrafted
Bool isCampfire

GlobalVariable glCarcassEnable

ObjectReference obGrabbed

Event OnInit()
	ihFunctions.LoadSettings()
	RegisterGamepad()
	CheckPapyrusExtender()
EndEvent

Event OnPlayerLoadGame()
	ihFunctions.LoadSettings()
	RegisterGamepad()
	CheckPapyrusExtender()
EndEvent

; ---  dTry's movement Magic effect monitor for controller users
Event OnMagicEffectApplyEx(ObjectReference akCaster, MagicEffect akEffect, Form akSource, bool abApplied)
	If isMGEFRegistered && Game.UsingGamepad()
		ihFunctions.OnControlDown("Forward")
	EndIf
EndEvent

;--- Player might get hit during the animations, sends stagger event and finishes what's pending.
Event OnHitEx(ObjectReference akAggressor, Form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
	If isHitRegistered
		Debug.SendAnimationEvent(PlayerRef, "StaggerStart")
		RegisterForHit(False)
		ihFunctions.EndAnim(True)
	EndIf
EndEvent

;--- This event is responsible for the Pickup option. It tracks when an object is grabbed and is conditioned to only trigger with animals that are possible to carry (what determines this, are the models available from Carry your Carcasses).
;    This will move the carcass to a created cell and enable the displays, registering for the activate key while at it.
Event OnObjectGrab(ObjectReference akObjectRef)
	If akObjectRef as Actor && akObjectRef.HasKeywordString("ActorTypeAnimal") && isPickupRegistered && (!(akObjectRef as Actor).WornHasKeyword(Keyword.GetKeyword("HISSkinnedAnimalSkin")) && !(akObjectRef as Actor).WornHasKeyword(Keyword.GetKeyword("AnimalSkinnedModel"))) ; If using the HiS patch, skinned animals will be ignored
		If obGrabbed ; Drops current carried carcass
			OnControlDown("Activate")
		EndIf
		glCarcassEnable = ihFunctions.GetCarcass(akObjectRef as Actor)
		If glCarcassEnable
			obGrabbed = akObjectRef
			obGrabbed.MoveTo(IH_CarcassMarker)
			If obGrabbed.IsNearPlayer()
				Debug.SendAnimationEvent(PlayerRef, "IdleStop")
				obGrabbed = None
				glCarcassEnable = None
			Else
				RegisterForControl("Activate")
				isControlRegistered = True
				glCarcassEnable.SetValue(1)
				IED.Evaluate(PlayerRef)
			EndIf
		EndIf
	EndIf
EndEvent

;--- Since the OnObjectGrab is not active anymore after moving the carcass, the event OnControlDown is used instead. 
;    When the grab key, or rather the activate key, is pressed again, this event is called to move the carcass back to the player, disabling the displays.
Event OnControlDown(String control)
	If control == "Activate" && isControlRegistered
		obGrabbed.MoveTo(PlayerRef)
		obGrabbed.SetPosition(PlayerRef.X, PlayerRef.Y, PlayerRef.Z + 75)
		obGrabbed = None
		glCarcassEnable.SetValue(0)
		IED.Evaluate(PlayerRef)
		glCarcassEnable = None
		UnregisterForControl("Activate")
		isControlRegistered = False
	EndIf
EndEvent

;--- Event to track dead animals when QuickLoot menu is opened
Event OnMenuOpen(String menuName)
	If !PlayerRef.HasPerk(ihFunctions.IH_PK_ImmersiveHunting) ; Mod is disabled, do nothing
		Return
	EndIf
	
	If PlayerRef.GetAnimationVariableInt("i1stPerson") && ihFunctions.IH_ForceThirdPerson.GetValue() == 0 ; First person and force third camera is disabled, do nothing.
		Return
	EndIf

	If menuName == "LootMenu"
		If isLootMenuRegistered
			ObjectReference orTargetRef = Game.GetCurrentCrosshairRef()
			If orTargetRef
				If (orTargetRef.HasKeywordString("ActorTypeAnimal") || orTargetRef.HasKeywordString("LootingSmallAnimal") || orTargetRef.HasKeywordString("LootingLargeAnimal")) && (orTargetRef as Actor).IsDead()
					ihFunctions.isQuickLootAnim = True
					ihAnimalAlias.ForceRefTo(orTargetRef)
				EndIf
			EndIf
		EndIf
	EndIf
EndEvent

Event OnMenuClose(string menuName)
	If menuName == "LootMenu" && isLootMenuRegistered
		ihFunctions.isQuickLootAnim = False
		Utility.Wait(1.0)
		If !UI.IsMenuOpen("ContainerMenu") && !UI.IsMenuOpen("LootMenu")
			ihAnimalAlias.Clear()
		EndIf
	EndIf
EndEvent

; --- Player can draw weapon during animation
Event OnAnimationEvent(ObjectReference akSource, string asEventName)
	If asEventName == "weaponDraw" && akSource == PlayerRef && isDrawnRegistered
		ihFunctions.EndAnim(True)
		RegisterForWeaponDrawn(False)
	EndIf
	
	If asEventName == "AnimObjectUnequip"
		UnregisterForAnimationEvent(PlayerRef, "AnimObjectUnequip")
	EndIf
EndEvent

; --- Track when the campfire furniture from Campfire mod is used
Event OnSit(ObjectReference akFurniture)
	If akFurniture.HasKeywordString("_Camp_CraftingCampfire") && ihFunctions.IH_EnableCampfire.GetValue()
		CheckForCooking(True)
		isCampfire = True
		While UI.IsMenuOpen("Crafting Menu")
			Utility.Wait(0.1)
		EndWhile
		ihFunctions.EndAnim(True)
	EndIf
EndEvent

Event OnGetUp(ObjectReference akFurniture)
	If akFurniture.HasKeywordString("_Camp_CraftingCampfire")
		CheckForCooking(False)
		isCampfire = False
	EndIf
EndEvent

; --- Functions and events responsible for the Cooking animation. 
; --- In vanilla, there are no good ways (that I know of) to detect when an item is crafted
; --- Luckly, Papyrus Extender has an Event exactly for this, which makes the process more reliable
Event OnItemCrafted(ObjectReference akBench, Location akLocation, Form akCreatedItem)
	; Triggers when an item is crafted to start the animation and set up the displays for IED
	isItemCrafted = True
	ihFunctions.fCookedFood = akCreatedItem
EndEvent

State CookingAnim
	; OnItemRemoved is being used to detect the input item for the recipe
	; It's also used to play the animation if Papyrus Extender is not installed. However, this event is not very reliable since it could trigger with any item being removed from the player's inventory while the crafting menu is open
	Event OnItemRemoved(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akDestContainer)
		If !IH_FL_CookingIgnoreList.HasForm(akBaseItem) ; Ignores certain items in this FormList until I find a better way to do this.
			If isCampfire
				 If !IH_FL_CookingAllowList.HasForm(akBaseItem)
					Return
				EndIf
			EndIf
			; Checks if Papyrus Extender is installed and waits a little bit, since this event triggers before OnItemCrafted. Otherwise plays the animation with the removed item
			If isExtenderInstalled
				Utility.Wait(0.2)
				If isItemCrafted
					; Item was really crafted, set up the display and animation
					doCookingAnim(akBaseItem)
					isItemCrafted = False
				EndIf
			ElseIf akBaseItem.GetType() == 46
				; Removed food must be at least a potion type to trigger the animation
				doCookingAnim(akBaseItem)
			EndIf
		EndIf
	EndEvent

	; OnItemAdded is being used to detect the output item for the recipe, if Papyrus Extender is not installed
	Event OnItemAdded(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akDestContainer)
		If !isExtenderInstalled && akBaseItem.GetType() == 46
			ihFunctions.fCookedFood = akBaseItem
		EndIf
	EndEvent
EndState

Function doCookingAnim(Form akBaseItem)
	ihFunctions.fHuntingMaterial = akBaseItem
	ihFunctions.doAnim(7, abToggle = isCampfire)
EndFunction

Function CheckForCooking(Bool doEnable)
	If doEnable
		GoToState("CookingAnim")
		If isExtenderInstalled
			RegisterForItemCrafted(Self)
		EndIf
	Else
		If isExtenderInstalled
			UnregisterForItemCrafted(Self)
		EndIf
		GoToState("")
	EndIf
EndFunction

Function RegisterForHit(Bool doEnable)
	If isExtenderInstalled
		If doEnable
			RegisterForHitEventEx(Self)
		Else
			UnregisterForHitEventEx(Self)
		EndIf
	EndIf
	isHitRegistered = doEnable
EndFunction

Function RegisterForPickup(Bool doEnable)
	If isExtenderInstalled
		If doEnable
			RegisterForObjectGrab(Self)
		Else
			UnregisterForObjectGrab(Self)
		EndIf
	EndIf
	isPickupRegistered = doEnable
EndFunction

Function RegisterForLootMenu(Bool doEnable)
	If doEnable
		RegisterForMenu("LootMenu")
	Else
		UnregisterForMenu("LootMenu")
	EndIf
	isLootMenuRegistered = doEnable
EndFunction


Function RegisterForWeaponDrawn(Bool doEnable)
	If doEnable
		RegisterForAnimationEvent(PlayerRef, "weaponDraw")
	Else
		UnregisterForAnimationEvent(PlayerRef, "weaponDraw")
	EndIf
	isDrawnRegistered = doEnable
EndFunction

; --- SKSE OnKeyDown, OnControl etc... doesn't detect movements from gamepad's analog sticks.
; --- These functions are meant for gamepad support to exit animations by moving in any direction. It uses dTry's KeyUtil's magic effects that are applied on the player when moving to track and control when to exit the animations.
; --- It also uses PO3 Papyrus Extender to better control the magic effects applied, as it allows to register/unregister for specific magic effects.
Function RegisterGamepad()
	ForwardMGEF = Game.GetFormFromFile(0x0000801, "Keytrace.esp") as MagicEffect
	LeftMGEF = Game.GetFormFromFile(0x0000802, "Keytrace.esp") as MagicEffect
	BackwardMGEF = Game.GetFormFromFile(0x0000803, "Keytrace.esp") as MagicEffect
	RightMGEF = Game.GetFormFromFile(0x0000804, "Keytrace.esp") as MagicEffect
EndFunction

Function RegisterForMagicEffectMov(Bool doEnable)
	If ForwardMGEF && isExtenderInstalled
		If doEnable
			RegisterForMagicEffectApplyEx(Self, ForwardMGEF, True)
			RegisterForMagicEffectApplyEx(Self, LeftMGEF, True)
			RegisterForMagicEffectApplyEx(Self, BackwardMGEF, True)
			RegisterForMagicEffectApplyEx(Self, RightMGEF, True)
		Else
			UnregisterForMagicEffectApplyEx(Self, ForwardMGEF, True)
			UnregisterForMagicEffectApplyEx(Self, LeftMGEF, True)
			UnregisterForMagicEffectApplyEx(Self, BackwardMGEF, True)
			UnregisterForMagicEffectApplyEx(Self, RightMGEF, True)
		EndIf
	EndIf
	isMGEFRegistered = doEnable
EndFunction

Function CheckPapyrusExtender()
	If GetPapyrusExtenderVersion()[0] > 0
		isExtenderInstalled = True
	Else
		isExtenderInstalled = False
	EndIf
EndFunction




