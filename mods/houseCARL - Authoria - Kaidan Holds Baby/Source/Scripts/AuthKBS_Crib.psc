Scriptname AuthKBS_Crib extends ObjectReference
{Authoria: a placed crib. Put the baby in, take it out, or fold the crib up.
The baby item lives inside this container while it sleeps; the crib is a
registered holder, so Beeing Female still counts the baby as Luna's.}

Actor Property PlayerRef Auto
AuthKBS_QuestScript Property QuestScript Auto
Container Property AuthKBS_CribEmpty Auto
Container Property AuthKBS_CribFull Auto
MiscObject Property CribFolded Auto
Message Property AuthKBS_CribMenuEmpty Auto
Message Property AuthKBS_CribMenuFull Auto

bool busy = false

Event OnInit()
	BlockActivation(true)
EndEvent

Event OnLoad()
	BlockActivation(true)
EndEvent

Event OnActivate(ObjectReference akActionRef)
	if akActionRef != PlayerRef || busy
		return
	endif
	busy = true
	if QuestScript.FirstBabyOn(self)
		if AuthKBS_CribMenuFull.Show() == 0
			TakeBabyOut()
		endif
	else
		int choice = AuthKBS_CribMenuEmpty.Show()
		if choice == 0
			PutBabyIn()
		elseif choice == 1
			FoldUp()
		endif
	endif
	busy = false
EndEvent

; BF hatching the baby (it grows into a child) takes the item out of the crib.
Event OnItemRemoved(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akDestContainer)
	if !busy && GetBaseObject() == AuthKBS_CribFull && !QuestScript.FirstBabyOn(self)
		busy = true
		SwapTo(AuthKBS_CribEmpty)
		Retire()
	endif
EndEvent

ObjectReference Function SwapTo(Container akBase)
	ObjectReference other = PlaceAtMe(akBase, 1, true, false)
	other.SetAngle(GetAngleX(), GetAngleY(), GetAngleZ())
	QuestScript.RegisterHolder(other)
	return other
EndFunction

Function Retire()
	QuestScript.UnregisterHolder(self)
	Disable()
	Delete()
EndFunction

Function PutBabyIn()
	Armor a = QuestScript.FirstBabyOn(PlayerRef)
	if !a
		Debug.Notification("You have no baby to lay down.")
		return
	endif
	ObjectReference full = SwapTo(AuthKBS_CribFull)
	PlayerRef.UnequipItem(a, false, true)
	PlayerRef.RemoveItem(a, 1, true, full)
	Retire()
EndFunction

Function TakeBabyOut()
	Armor a = QuestScript.FirstBabyOn(self)
	if !a
		return
	endif
	ObjectReference empty = SwapTo(AuthKBS_CribEmpty)
	RemoveItem(a, 1, true, PlayerRef)
	PlayerRef.EquipItem(a, false, true)
	Retire()
EndFunction

Function FoldUp()
	PlayerRef.AddItem(CribFolded, 1)
	Retire()
EndFunction
