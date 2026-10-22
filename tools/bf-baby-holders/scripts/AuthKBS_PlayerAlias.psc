Scriptname AuthKBS_PlayerAlias extends ReferenceAlias
{Authoria: keeps the "can hand Kaidan the baby" flag current and re-registers holders on load.}

AuthKBS_QuestScript Property QuestScript Auto
FormList Property AuthKBS_BabyItems Auto

Event OnInit()
	AddInventoryEventFilter(AuthKBS_BabyItems)
EndEvent

Event OnPlayerLoadGame()
	AddInventoryEventFilter(AuthKBS_BabyItems)
	QuestScript.Setup()
EndEvent

Event OnItemAdded(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akSourceContainer)
	QuestScript.UpdateCanHand()
EndEvent

Event OnItemRemoved(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akDestContainer)
	QuestScript.UpdateCanHand()
EndEvent
