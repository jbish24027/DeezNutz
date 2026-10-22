Scriptname SC_MainSCRIPT extends Quest  

GlobalVariable Property SC_AllowSMEN  Auto  
GlobalVariable Property SC_TokenAmount  Auto
Actor Property PlayerRef  Auto
MiscObject Property Token  Auto
Message[] Property MessageBox  Auto 
ImageSpaceModifier[] Property VisionFX  Auto 
GlobalVariable Property _Authoria_Init_Running Auto
FormList Property _Authoria_Init_SC_RemoveAllItemsExclusions Auto

ObjectReference ExchangeStation



Function Initialize()

	VisionFX()
	Game.DisablePlayerControls()
	Utility.Wait(1.5)
	Int iButton = MessageBox[0].Show(SC_TokenAmount.GetValueInt())

	If ( iButton == 0 )
		RegisterForMenu("Crafting Menu")
		Exchange()
	ElseIf ( iButton == 1 )
		Clean()
	EndIf

EndFunction



Function Exchange()

	ExchangeStation = PlayerRef.PlaceAtMe(Game.GetFormFromFile(0x80D, "Starting Choices.esp"))
	PreserveExcludedItems()
	PlayerRef.RemoveAllItems()
	RestoreExcludedItems()
	PlayerRef.AddItem(Token, SC_TokenAmount.GetValueInt(), True)	
	ExchangeStation.Activate(PlayerRef)

EndFunction



Function PreserveExcludedItems()

	If !_Authoria_Init_SC_RemoveAllItemsExclusions || !ExchangeStation
		Return
	EndIf

	Int index = 0
	While index < _Authoria_Init_SC_RemoveAllItemsExclusions.GetSize()
		Form excludedItem = _Authoria_Init_SC_RemoveAllItemsExclusions.GetAt(index)
		If excludedItem
			Int itemCount = PlayerRef.GetItemCount(excludedItem)
			If itemCount > 0
				PlayerRef.RemoveItem(excludedItem, itemCount, True, ExchangeStation)
			EndIf
		EndIf
		index += 1
	EndWhile

EndFunction



Function RestoreExcludedItems()

	If !_Authoria_Init_SC_RemoveAllItemsExclusions || !ExchangeStation
		Return
	EndIf

	Int index = 0
	While index < _Authoria_Init_SC_RemoveAllItemsExclusions.GetSize()
		Form excludedItem = _Authoria_Init_SC_RemoveAllItemsExclusions.GetAt(index)
		If excludedItem
			Int itemCount = ExchangeStation.GetItemCount(excludedItem)
			If itemCount > 0
				ExchangeStation.RemoveItem(excludedItem, itemCount, True, PlayerRef)
			EndIf
		EndIf
		index += 1
	EndWhile

EndFunction



Function VisionFX()

	VisionFX[0].Apply()
	VisionFX[1].ApplyCrossFade()

EndFunction



Event OnMenuClose(String MenuName)

	If ( MenuName == "Crafting Menu" )

		Int iButton = MessageBox[1].Show()
		
		If ( iButton == 0 )
			Clean()
		ElseIf ( iButton == 1 )
			Exchange()
		EndIf

	EndIf

EndEvent



Function Clean()

	SC_AllowSMEN.SetValueInt(0)
	VisionFX[1].PopTo(VisionFX[2])
	If !_Authoria_Init_Running || _Authoria_Init_Running.GetValueInt() != 1
		Game.EnablePlayerControls()
	EndIf
	If ExchangeStation
		ExchangeStation.Delete()
		ExchangeStation = None
	EndIf
	Int RemainingTokens = PlayerRef.GetItemCount(Token)

	If ( RemainingTokens > 0 )
		PlayerRef.RemoveItem(Token, RemainingTokens)
	EndIf

	UnregisterForMenu("Crafting Menu")
	SendModEvent("_Authoria_Init_StartingChoicesDone")

	Stop()

EndFunction
