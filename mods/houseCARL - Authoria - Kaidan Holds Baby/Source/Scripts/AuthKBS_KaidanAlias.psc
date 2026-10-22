Scriptname AuthKBS_KaidanAlias extends ReferenceAlias
{Authoria: puts the baby sling back on Kaidan if anything takes it off.}

AuthKBS_QuestScript Property QuestScript Auto
FormList Property AuthKBS_BabyItems Auto

Event OnLoad()
	QuestScript.ReequipOnKaidan()
EndEvent

Event OnObjectUnequipped(Form akBaseObject, ObjectReference akReference)
	if AuthKBS_BabyItems.HasForm(akBaseObject)
		RegisterForSingleUpdate(1.0)
	endif
EndEvent

Event OnUpdate()
	QuestScript.ReequipOnKaidan()
EndEvent
