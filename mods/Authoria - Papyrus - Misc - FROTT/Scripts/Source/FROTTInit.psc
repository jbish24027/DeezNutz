Scriptname FROTTInit extends Quest  

Quest Property CW01A Auto 
Quest Property CW01B Auto
Quest Property CWResolution01 Auto 

Quest Property KmodFastTravelQuest Auto

GlobalVariable Property FROTTWarStarted Auto 
GlobalVariable Property FROTTWarEnded Auto 

Event OnInit()
    InitRouteCosts()

    RegisterForSingleUpdate(60.0)

EndEvent

int Function InitRouteCosts()
    int jRouteSettings = JValue.readFromFile("Data/settings/FROTTRouteSettings.json")
    int jSettings = JValue.readFromFile("Data/settings/FROTTSettings.json")

    JDB.setObj("frottRouteSettings", jRouteSettings)
    JDB.setObj("frottSettings", jSettings)

    string route = JMap.nextKey(jRouteSettings)
    while route
        int routeCost = SetRouteCost(route)
        route = JMap.nextKey(jRouteSettings, route)
    endwhile

    return 0
EndFunction

int Function GetWarStage()
    int warStage = 1

    If CW01A.IsCompleted()
        warStage = 2
    EndIf

    If CW01B.IsCompleted()
        warStage = 2
    EndIf 

    If CWResolution01.IsCompleted()
        warStage = 3
    EndIf 

    return warStage
EndFunction

int Function GetWarMultiplier()
    int warStage = GetWarStage()

    int warMultiplier = 1

    If warStage == 1
        warMultiplier = JDB.solveInt(".frottSettings.EarlyWarMultiplier")
    ElseIf warStage == 2
        warMultiplier = JDB.solveInt(".frottSettings.WarMultiplier")
    EndIf

    return warMultiplier
EndFunction

int Function GetFortPenalty(int fortSetting)
    int warStage = GetWarStage()

    Form fort = JMap.getForm(fortSetting, "location")
    int costMultiplier = JMap.getInt(fortSetting, "costMultiplier")
    int locationCost = JDB.solveInt(".frottSettings.FortCost")
    int warStageCleared = JMap.getInt(fortSetting, "warStageCleared")

    Bool isCleared = False 
    If warStageCleared == 0
        isCleared = (fort as Location).IsCleared()
    ElseIf warStage > warStageCleared
        isCleared = True 
    EndIf

    int fortPenalty = 0
    If isCleared == False 
        fortPenalty = locationCost * costMultiplier
    EndIf 

    return fortPenalty
EndFunction 


int Function SetRouteCost(string route)  
    int routeCost = JDB.solveInt(".frottRouteSettings." + route + ".cost")
    int jRoutePenalties = JDB.solveObj(".frottRouteSettings." + route + ".penalties")

    int baseCost = JDB.solveInt(".frottSettings.BaseCost")
    int locationCost = JDB.solveInt(".frottSettings.FortCost")
    int warMultiplier = GetWarMultiplier()
    int locationSettings = JDB.solveObj(".frottSettings.FortSettings")


    baseCost = baseCost * warMultiplier

    int totalCost = routeCost * baseCost
    int penaltyCount = JArray.count(jRoutePenalties)
    while (penaltyCount > 0)
        penaltyCount -= 1
        string penaltyName = JArray.getStr(jRoutePenalties, penaltyCount)
        int fortSetting = JMap.getObj(locationSettings, penaltyName)
        int fortPenalty = GetFortPenalty(fortSetting)

        totalCost = totalCost + fortPenalty
    EndWhile


    Form costGlobal = JDB.solveForm(".frottRouteSettings." + route + ".glob") 
    (costGlobal as GlobalVariable).SetValue(totalCost)
    
    KmodFastTravelQuest.UpdateCurrentInstanceGlobal(costGlobal as GlobalVariable)

    return totalCost
EndFunction


Event OnUpdate()
    Bool bNoWarRecalc = True
    int warStage = GetWarStage()
    If (FROTTWarStarted.GetValueInt() as Bool) == False && warStage == 2
        FROTTWarStarted.SetValue(1)
        InitRouteCosts()
        bNoWarRecalc = False
    EndIf

    If (FROTTWarEnded.GetValueInt() as Bool) == False && warStage == 3
        FROTTWarEnded.SetValue(1)    
        InitRouteCosts()
        bNoWarRecalc = False
    EndIf

    int fortSettings = JDB.solveObj(".frottSettings.FortSettings")
    string fort = JMap.nextKey(fortSettings)
    Bool bRecalc = False 
    Bool bNeedMoreUpdate = False 
    While fort
        int fortSetting = JDB.solveObj(".frottSettings.FortSettings." + fort)
        Form clearanceState = JMap.getForm(fortSetting, "clearanceState")
        If ((clearanceState as GlobalVariable).GetValueInt() as Bool) == False 
            int warStageCleared = JMap.getInt(fortSetting, "warStageCleared")
            If warStageCleared == 0
                Form loc = JMap.getForm(fortSetting, "location")
                If (loc as Location).IsCleared()
                    (clearanceState as GlobalVariable).SetValue(1)
                    bRecalc = True 
                Else 
                    bNeedMoreUpdate = True 
                EndIf
            Else 
                If warStage > warStageCleared
                    Form loc = JMap.getForm(fortSetting, "location")
                    (clearanceState as GlobalVariable).SetValue(1)
                    bRecalc = True 
                Else 
                    bNeedMoreUpdate = True 
                EndIf 
            EndIf
        EndIf
        fort = JMap.nextKey(fortSettings, fort)
    EndWhile

    If bRecalc && bNoWarRecalc
        InitRouteCosts()
    EndIf
    
    If (FROTTWarEnded.GetValueInt() as Bool) == False
        bNeedMoreUpdate = True
    EndIf

    If bNeedMoreUpdate
        RegisterForSingleUpdate(60.0)
    EndIf
EndEvent
