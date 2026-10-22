ScriptName REQ_FoodPoisoning Extends REQ_CoreScript

Keyword Property ContaminatedFood Auto

Spell Property FoodPoisoning Auto

Message Property MessageFoodPoisoning Auto

; --- Authoria: raw-food racial exemption ------------------------------------
; Requiem's stock food-poisoning roll ignores race, so beast races were poisoned
; by the very raw foods Food & Beverages Redone lets them eat (its paralysis
; effect exempts them, but this separate poisoning script never did). This aligns
; the two: Carnivore races (Orc / Bosmer / Argonian) tolerate any raw meat or
; fish; the Khajiit tolerate raw fish only (foods tagged LoreBox_REQ_FelineStomach).
; Forms are fetched lazily via GetFormFromFile, so this needs no ESP master and no
; filled script properties. A form whose plugin is absent resolves to None and is
; skipped harmlessly.
Bool _authReady = False
Keyword _felineStomach
Race[] _carnivoreRaces
Race[] _felineRaces

Function AuthInitForms()
    _felineStomach = Game.GetFormFromFile(0x000A35, "Requiem - Food and Beverages Redone.esp") as Keyword

    _carnivoreRaces = new Race[10]
    _carnivoreRaces[0] = Game.GetFormFromFile(0x013747, "Skyrim.esm") as Race       ; OrcRace
    _carnivoreRaces[1] = Game.GetFormFromFile(0x0A82B9, "Skyrim.esm") as Race       ; OrcRaceVampire
    _carnivoreRaces[2] = Game.GetFormFromFile(0x013749, "Skyrim.esm") as Race       ; WoodElfRace
    _carnivoreRaces[3] = Game.GetFormFromFile(0x088884, "Skyrim.esm") as Race       ; WoodElfRaceVampire
    _carnivoreRaces[4] = Game.GetFormFromFile(0x013740, "Skyrim.esm") as Race       ; ArgonianRace
    _carnivoreRaces[5] = Game.GetFormFromFile(0x08883A, "Skyrim.esm") as Race       ; ArgonianRaceVampire
    _carnivoreRaces[6] = Game.GetFormFromFile(0x05A1B0, "UBE_AllRace.esp") as Race   ; 00UBE_OrcRace
    _carnivoreRaces[7] = Game.GetFormFromFile(0x05A1B1, "UBE_AllRace.esp") as Race   ; 00UBE_OrcRaceVampire
    _carnivoreRaces[8] = Game.GetFormFromFile(0x05A1AC, "UBE_AllRace.esp") as Race   ; 00UBE_WoodElfRace
    _carnivoreRaces[9] = Game.GetFormFromFile(0x05A1AD, "UBE_AllRace.esp") as Race   ; 00UBE_WoodElfRaceVampire

    _felineRaces = new Race[4]
    _felineRaces[0] = Game.GetFormFromFile(0x013745, "Skyrim.esm") as Race           ; KhajiitRace
    _felineRaces[1] = Game.GetFormFromFile(0x088845, "Skyrim.esm") as Race           ; KhajiitRaceVampire
    _felineRaces[2] = Game.GetFormFromFile(0x03322B, "HalfKhajiit.esp") as Race      ; HalfKhajiitRace
    _felineRaces[3] = Game.GetFormFromFile(0x05693A, "HalfKhajiit.esp") as Race      ; HalfKhajiitRaceVampire

    _authReady = True
EndFunction

Bool Function AuthRaceInList(Race akRace, Race[] akList)
    Int i = 0
    While i < akList.Length
        If akList[i] && akRace == akList[i]
            Return True
        EndIf
        i += 1
    EndWhile
    Return False
EndFunction

Bool Function AuthIsExempt(Form akFood)
    If !_authReady
        AuthInitForms()
    EndIf
    Race playerRace = Player.GetRace()
    If AuthRaceInList(playerRace, _carnivoreRaces)
        Return True
    EndIf
    If akFood.HasKeyword(_felineStomach) && AuthRaceInList(playerRace, _felineRaces)
        Return True
    EndIf
    Return False
EndFunction
; ---------------------------------------------------------------------------

Function initScript(Int currentVersion, Int nevVersion)
EndFunction

Function shutdownScript(Int currentVersion, Int nevVersion)
EndFunction

Event OnObjectEquipped(Form akBaseObject, ObjectReference akReference)
    If akBaseObject As Potion
        If akBaseObject.HasKeyword(ContaminatedFood)
            If !AuthIsExempt(akBaseObject)
                Float DiseaseResist = Player.GetActorValue("DiseaseResist")
                If DiseaseResist < Utility.RandomFloat(0.0, 100.0)
                    Player.AddSpell(FoodPoisoning, False)
                    MessageFoodPoisoning.Show()
                EndIf
            EndIf
        EndIf
    EndIf
EndEvent
