Scriptname AuthKBS_QuestScript extends Quest
{Authoria: Kaidan holds Luna's Beeing Female baby in a sling, and a portable crib.
Holders (Kaidan, placed cribs) go in the StorageUtil list "Authoria.BabyHolders",
which the patched BF scripts count as still the player's, so the baby keeps
growing and hatches on time wherever it is.}

Actor Property PlayerRef Auto
Actor Property KaidanRef Auto
FormList Property AuthKBS_BabyItems Auto
GlobalVariable Property AuthKBS_CanHand Auto

string Property HolderList = "Authoria.BabyHolders" AutoReadOnly

Event OnInit()
	Setup()
EndEvent

Function Setup()
	RegisterHolder(KaidanRef)
	UpdateCanHand()
EndFunction

Function RegisterHolder(ObjectReference akRef)
	if akRef
		StorageUtil.FormListAdd(none, HolderList, akRef, false)
	endif
EndFunction

Function UnregisterHolder(ObjectReference akRef)
	if akRef
		StorageUtil.FormListRemove(none, HolderList, akRef, true)
	endif
EndFunction

; First baby item this reference carries, or none.
Armor Function FirstBabyOn(ObjectReference akRef)
	if !akRef
		return none
	endif
	int i = AuthKBS_BabyItems.GetSize()
	while i > 0
		i -= 1
		Armor a = AuthKBS_BabyItems.GetAt(i) as Armor
		if a && akRef.GetItemCount(a) > 0
			return a
		endif
	endwhile
	return none
EndFunction

; A baby item Luna carries whose father BF recorded as Kaidan, or none.
Armor Function FindKaidanBaby()
	int i = AuthKBS_BabyItems.GetSize()
	while i > 0
		i -= 1
		Armor a = AuthKBS_BabyItems.GetAt(i) as Armor
		if a && PlayerRef.GetItemCount(a) > 0
			int n = StorageUtil.FormListCount(PlayerRef, "FW.BabyItemArmor")
			int j = 0
			while j < n
				if StorageUtil.FormListGet(PlayerRef, "FW.BabyItemArmor", j) == a && StorageUtil.FormListGet(PlayerRef, "FW.BabyItemFather", j) == KaidanRef
					return a
				endif
				j += 1
			endwhile
		endif
	endwhile
	return none
EndFunction

Function UpdateCanHand()
	if FindKaidanBaby()
		AuthKBS_CanHand.SetValue(1)
	else
		AuthKBS_CanHand.SetValue(0)
	endif
EndFunction

Function GiveToKaidan()
	Armor a = FindKaidanBaby()
	if a
		RegisterHolder(KaidanRef)
		PlayerRef.UnequipItem(a, false, true)
		PlayerRef.RemoveItem(a, 1, true, KaidanRef)
		KaidanRef.EquipItem(a, true, true)
	endif
	UpdateCanHand()
EndFunction

Function TakeFromKaidan()
	Armor a = FirstBabyOn(KaidanRef)
	if a
		KaidanRef.UnequipItem(a, false, true)
		KaidanRef.RemoveItem(a, 1, true, PlayerRef)
		PlayerRef.EquipItem(a, false, true)
	endif
	UpdateCanHand()
EndFunction

; Keep the sling on Kaidan if his outfit handling takes it off.
Function ReequipOnKaidan()
	Armor a = FirstBabyOn(KaidanRef)
	if a && !KaidanRef.IsEquipped(a)
		KaidanRef.EquipItem(a, true, true)
	endif
EndFunction
