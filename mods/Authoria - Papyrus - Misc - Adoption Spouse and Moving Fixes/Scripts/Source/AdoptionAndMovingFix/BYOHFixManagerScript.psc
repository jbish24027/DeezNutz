Scriptname BYOHFixManagerScript extends ReferenceAlias

int property Version auto hidden

Perk property BYOHFixRepairAdoptionPerk auto
ActorBase property SofieBase auto
ActorBase property SamuelBase auto ; just used for comparing essential flags

Event OnInit()
	CheckModVersion()
EndEvent

Event OnPlayerLoadGame()
	CheckModVersion()
EndEvent

Function CheckModVersion()
    Actor PlayerRef = Game.GetPlayer()

    If (PlayerRef != None && BYOHFixRepairAdoptionPerk != None && !PlayerRef.HasPerk(BYOHFixRepairAdoptionPerk))
        PlayerRef.AddPerk(BYOHFixRepairAdoptionPerk)
    EndIf

    If (Version < 1)
        Version = 1
    EndIf

    If (Version < 2)        
        TryMakeSofieNonEssential()
        Version = 2
    EndIf
EndFunction

; Sofie is the only child in the game who is flagged as essential, which can create inconsistency with mods that allow kids to be harmed
; I originally just edited the record, but I don't feel like making the unofficial patch a requirement to get around conflicts
Function TryMakeSofieNonEssential()
    ; If Samuel marked as essential, it's likely the user has a mod that makes kids essential and we should respect that
    If (SamuelBase != None && SofieBase != None && SamuelBase.IsEssential() == false && SofieBase.IsEssential() == true)
        SofieBase.SetEssential(false)
    EndIf
EndFunction
