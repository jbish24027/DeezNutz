Scriptname _RMP_PurchaseMenuScript extends ObjectReference  
{This script handles the purchasing of the home! Buy it like Todd wants you to buy Skyrim!!}

ObjectReference Property _RMP_PurchaseHomeSign  Auto

ObjectReference Property _RMP_PurchaseSignMarker  Auto

ObjectReference Property _RMP_FrontDoor  Auto

ObjectReference Property _RMP_BackDoor  Auto

ObjectReference Property _RMP_PorchDoor  Auto

Message Property _RMP_HomePurchaseMenu  Auto

Message Property _RMP_HomePurchaseMenuFail  Auto

MiscObject Property Gold001 Auto

GlobalVariable Property _Authoria_MirelePrice Auto

Event OnActivate(ObjectReference akActionRef)
	Menu()
EndEvent

Int Function GetPrice()
	GlobalVariable priceGlobal = _Authoria_MirelePrice
	If priceGlobal == None
		priceGlobal = Game.GetFormFromFile(0x00000800, "Authoria - Patch - Mirele Price.esp") as GlobalVariable
	EndIf
	
	If priceGlobal != None
		Return priceGlobal.GetValueInt()
	EndIf
	
	Return 8000
EndFunction

Function Menu(int aiButton = 0)
	Int price = GetPrice()
	Float priceDisplay = price
	aiButton = _RMP_HomePurchaseMenu.Show(priceDisplay)
	If aiButton == 0
		
	ElseIf aiButton == 1
		If (Game.GetPlayer().GetItemCount(Gold001) >= price)
			Game.GetPlayer().RemoveItem(Gold001, price)
			_RMP_PurchaseSignMarker.disable()
			_RMP_FrontDoor.lock(false)
			_RMP_BackDoor.lock(false)
			_RMP_PorchDoor.lock(false)
			Game.IncrementStat("Houses Owned")
		Else
			_RMP_HomePurchaseMenuFail.show()
		EndIf
	EndIf
EndFunction
