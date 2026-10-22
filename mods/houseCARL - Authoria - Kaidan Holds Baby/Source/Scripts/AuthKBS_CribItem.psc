Scriptname AuthKBS_CribItem extends ObjectReference
{Authoria: drop the folded crib from your inventory and it is set up in front of you.}

Actor Property PlayerRef Auto
Container Property AuthKBS_CribEmpty Auto
AuthKBS_QuestScript Property QuestScript Auto

Event OnContainerChanged(ObjectReference akNewContainer, ObjectReference akOldContainer)
	if akNewContainer == none && akOldContainer == PlayerRef
		float ang = PlayerRef.GetAngleZ()
		ObjectReference crib = PlayerRef.PlaceAtMe(AuthKBS_CribEmpty, 1, true, true)
		crib.MoveTo(PlayerRef, 80.0 * Math.Sin(ang), 80.0 * Math.Cos(ang), 0.0)
		crib.SetAngle(0.0, 0.0, ang + 180.0)
		crib.Enable()
		QuestScript.RegisterHolder(crib)
		Disable()
		Delete()
	endif
EndEvent
