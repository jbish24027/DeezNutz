ScriptName REQ_AddItemsOnEffectStart Extends ActiveMagicEffect

Form[] Property ItemsToAdd Auto

Int[] Property Amount Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
	If !akTarget || !ItemsToAdd
		Return
	EndIf

	Int i = 0
	While i < ItemsToAdd.Length
		If Amount && i < Amount.Length
			akTarget.AddItem(ItemsToAdd[i], Amount[i])
		Else
			akTarget.AddItem(ItemsToAdd[i])
		EndIf
		i += 1
	EndWhile
EndEvent
