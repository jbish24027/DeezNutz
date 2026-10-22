ScriptName RMS_ControllerScript extends Quest
{Authoria Requiem patch 2026-09-06 for Rovan's Market Stall 1.4.1 - the shipped 1.4.1 controller,
 decompiled and recompiled with ONE kind of change: the Market Stall Bag (an Ingestible defined in
 the patch "Authoria - Patch - Rovan Market Stall - Requiem.esp" as 0x801) stands in for the author's
 craftable "Market Stall Deployment Kit" (RMS_StallKit). Using the bag from the inventory starts
 placement mode exactly like dropping the kit does (see Authoria_RMS_BagEffectScript); the bag is
 consumed by the use, and every place the shipped script hands a kit back now hands a bag back:
   - StartPlacementFromItemDrop(): the 5-stall limit refund
   - CancelPlacement(): the cancelled placement
   - ExecuteStallBuild(): the four failed-build paths
   - DisassembleSlot() / EmergencyRecallSlot(): the packed-up or recalled stall (one bag per stall)
 New helpers GetStallBag() / GiveStallBag(). Nothing is handed out automatically - the player adds
 the first bag themselves (SearchUI / console: Authoria_RMS_StallBag, 0x801 in the patch). The kit
 recipe is suppressed by the patch; a kit added by console still works through the shipped drop path
 and its stall also returns a bag. Everything else is the shipped 1.4.1 logic, unchanged. Property list
 unchanged (the quest's script data in RovanMarketStall.esp binds the same properties).}

bool[] SlotOccupied
float DeploymentY
float DeploymentX
ObjectReference[] SlotVendorMarkerRefs
ObjectReference[] SlotCustomerMarker2Refs
Actor RecentCustomer4
Actor RecentCustomer3
Actor RecentCustomer2
Actor RecentCustomer1
bool CustomerSchedulerRunning = false
int KeyShout
ObjectReference[] SlotNavCutterRefs
int KeyActivate
int KeyReadyWeapon
int iTargetingSlot = -1
ObjectReference[] SlotMerchandiseRefs
float DeploymentAngle
ObjectReference[] SlotCustomerMarker3Refs
float[] SlotSimTimestamps
Actor[] SlotFollowerRefs
ObjectReference[] SlotClutterRightRefs
ObjectReference[] SlotStallRefs
ObjectReference[] SlotLedgerRefs
ObjectReference[] SlotCashBoxRefs
ObjectReference[] SlotFoundationRefs
ObjectReference[] SlotClutterLeftRefs
ObjectReference[] SlotCustomerMarker1Refs
float DeploymentZ
string[] SlotLocationNames
bool bTrackingPaused = false
ObjectReference DeploymentMarkerRef

message Property RMS_MSG_ReputationMenu Auto

static Property VendorMarkerBase Auto

topic Property BarkBrowsing Auto

sound Property SoundBook Auto

activator Property DeploymentMarkerBase Auto

sound Property SoundDisassemble Auto

referencealias Property Customer2Alias Auto

globalvariable Property rms_MaxStallLimit Auto

message Property RMS_MSG_PlacementMenu Auto

activator Property LedgerBase Auto

bool Property IsInFollowerTargetMode = false Auto Hidden

referencealias Property LedgerAlias Auto

activator Property StallBase Auto

static Property ApproachMarkerBase Auto

globalvariable Property rms_FollowerWagePercent Auto

message Property MsgDisassembled Auto

globalvariable Property rms_StallReputation Auto

message Property RMS_MSG_LedgerMenu Auto

globalvariable Property MinBrowseTime Auto

container Property MerchandiseBase Auto

sound Property SoundDeploy Auto

message Property MsgDeploymentFailed Auto

message Property MsgAlreadyDeployed Auto

message Property RMS_MSG_LedgerCash Auto

message Property MsgEmergencyRecall Auto

referencealias Property StallAlias Auto

globalvariable Property TodayTransactions Auto

message Property RMS_MSG_RecallSelectMenu Auto

globalvariable Property TotalRevenue Auto

message Property RMS_MSG_LedgerInventory Auto

message Property MsgInvalidLocation Auto

referencealias Property MerchandiseAlias Auto

message Property MsgNoActiveStall Auto

sound Property SoundGoldTake Auto

message Property RMS_MSG_LedgerSales Auto

globalvariable Property TotalItemsSold Auto

globalvariable Property CustomerSearchRadius Auto

topic Property BarkPurchased Auto

faction Property PlayerFaction Auto

static Property TableClutterRightBase Auto

globalvariable Property MaxCustomerInterval Auto

globalvariable Property LastBusinessDay Auto

referencealias Property CashBoxAlias Auto

globalvariable Property rms_ActiveStallCount Auto

static Property TableClutterLeftBase Auto

referencealias Property CustomerMarker3Alias Auto

message Property MsgInventoryNotEmpty Auto

bool Property IsInPlacementMode Auto Hidden

rms_cashboxscript Property CashBoxSystem Auto

message Property RMS_MSG_LedgerStatistics Auto

rms_inventoryscript Property InventorySystem Auto

container Property CashBoxBase Auto

effectshader Property PlacementGhostShader Auto

topic Property BarkRejected Auto

referencealias Property Customer3Alias Auto

message Property MsgCashNotEmpty Auto

globalvariable Property MaxBrowseTime Auto

referencealias Property Customer1Alias Auto

referencealias Property CustomerMarker2Alias Auto

message Property RMS_MSG_RecallConfirm Auto

referencealias Property CustomerMarker1Alias Auto

referencealias Property FollowerVendorAlias Auto

globalvariable Property TotalTransactions Auto

activator Property StallNavCutterHelperBase Auto

miscobject Property RMS_StallKit Auto

globalvariable Property rms_AllowIllicitGoods Auto

globalvariable Property rms_FollowerSalesPerHour Auto

sound Property SoundCoin Auto

message Property MsgImprisoned Auto

message Property MsgInterior Auto

globalvariable Property PurchaseChance Auto

globalvariable Property TodayRevenue Auto

message Property RMS_MSG_MaxStallsReached Auto

globalvariable Property MinCustomerInterval Auto

static Property FoundationBase Auto

referencealias Property VendorMarkerAlias Auto

message Property MsgDeploySuccess Auto

message Property RMS_MSG_MasterVaultMenu Auto

message Property MsgInCombat Auto

Event OnInit()
    InitializeRegistry()
EndEvent

Function InitializeRegistry()
    SlotOccupied = new bool[5]
    SlotStallRefs = new ObjectReference[5]
    SlotFoundationRefs = new ObjectReference[5]
    SlotMerchandiseRefs = new ObjectReference[5]
    SlotCashBoxRefs = new ObjectReference[5]
    SlotLedgerRefs = new ObjectReference[5]
    SlotClutterLeftRefs = new ObjectReference[5]
    SlotClutterRightRefs = new ObjectReference[5]
    SlotVendorMarkerRefs = new ObjectReference[5]
    SlotNavCutterRefs = new ObjectReference[5]
    SlotFollowerRefs = new Actor[5]
    SlotSimTimestamps = new float[5]
    SlotLocationNames = new string[5]
    SlotCustomerMarker1Refs = new ObjectReference[5]
    SlotCustomerMarker2Refs = new ObjectReference[5]
    SlotCustomerMarker3Refs = new ObjectReference[5]
    int i = 0
    while i < 5
        SlotOccupied[i] = false
        SlotStallRefs[i] = None
        SlotFoundationRefs[i] = None
        SlotMerchandiseRefs[i] = None
        SlotCashBoxRefs[i] = None
        SlotLedgerRefs[i] = None
        SlotClutterLeftRefs[i] = None
        SlotClutterRightRefs[i] = None
        SlotVendorMarkerRefs[i] = None
        SlotNavCutterRefs[i] = None
        SlotFollowerRefs[i] = None
        SlotSimTimestamps[i] = 0.0
        SlotLocationNames[i] = ""
        SlotCustomerMarker1Refs[i] = None
        SlotCustomerMarker2Refs[i] = None
        SlotCustomerMarker3Refs[i] = None
        i = i + 1
    endwhile
    if !(rms_ActiveStallCount == None)
        rms_ActiveStallCount.SetValue(0.0)
    endif
    if !(rms_MaxStallLimit == None)
        rms_MaxStallLimit.SetValue(5.0)
    endif
    if !(rms_StallReputation == None)
        rms_StallReputation.SetValue(0.0)
    endif
    CustomerSchedulerRunning = false
    IsInPlacementMode = false
    IsInFollowerTargetMode = false
    iTargetingSlot = -1
    bTrackingPaused = false
    RecentCustomer1 = None
    RecentCustomer2 = None
    RecentCustomer3 = None
    RecentCustomer4 = None
EndFunction

Function RunMaintenanceUpdate()
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None
        return
    endif
    if !SlotOccupied || SlotOccupied.Length < 5
        InitializeRegistry()
    endif
    CheckBusinessDayRollover()
EndFunction

int Function GetActiveStallCount()
    int count = 0
    int i = 0
    while i < 5
        if SlotOccupied[i]
            count = count + 1
        endif
        i = i + 1
    endwhile
    return count
EndFunction

bool Function IsStallDeployed()
    return GetActiveStallCount() > 0
EndFunction

; Authoria: the Market Stall Bag lives in the Requiem patch (light plugin, local FormID 0x801).
Potion Function GetStallBag()
    return game.GetFormFromFile(0x000801, "Authoria - Patch - Rovan Market Stall - Requiem.esp") as Potion
EndFunction

; Authoria: hand the player ONE bag - every place the shipped script hands a deployment kit back.
; One bag per stall: a pack-up, a recall, a cancelled or a refused placement each return exactly one.
bool Function GiveStallBag(bool abSilent = true)
    Actor PlayerRef = game.GetPlayer()
    Potion Bag = GetStallBag()
    if PlayerRef == None || Bag == None
        return false
    endif
    PlayerRef.AddItem(Bag, 1, abSilent)
    return true
EndFunction

ObjectReference Function GetActiveStallRef()
    int nearSlot = GetNearestActiveSlot()
    if !(nearSlot == -1)
        return SlotStallRefs[nearSlot]
    endif
    return None
EndFunction

ObjectReference Function GetActiveMerchandiseRef()
    int nearSlot = GetNearestActiveSlot()
    if !(nearSlot == -1)
        return SlotMerchandiseRefs[nearSlot]
    endif
    return None
EndFunction

ObjectReference Function GetActiveCashBoxRef()
    int nearSlot = GetNearestActiveSlot()
    if !(nearSlot == -1)
        return SlotCashBoxRefs[nearSlot]
    endif
    return None
EndFunction

int Function FindAvailableSlot()
    int i = 0
    while i < 5
        if !SlotOccupied[i]
            return i
        endif
        i = i + 1
    endwhile
    return -1
EndFunction

int Function GetSlotForReference(ObjectReference akRef)
    if akRef == None
        return -1
    endif
    int i = 0
    while i < 5
        if SlotOccupied[i]
            if akRef == SlotLedgerRefs[i] || akRef == SlotStallRefs[i] || akRef == SlotMerchandiseRefs[i] || akRef == SlotCashBoxRefs[i]
                return i
            endif
        endif
        i = i + 1
    endwhile
    return -1
EndFunction

int Function GetNearestActiveSlot()
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None
        return -1
    endif
    int nearestSlot = -1
    float minDistance = 999999.0
    int i = 0
    while i < 5
        if SlotOccupied[i] && !(SlotStallRefs[i] == None)
            float dist = PlayerRef.GetDistance(SlotStallRefs[i])
            if dist < minDistance
                minDistance = dist
                nearestSlot = i
            endif
        endif
        i = i + 1
    endwhile
    if minDistance <= 3500.0
        return nearestSlot
    endif
    return -1
EndFunction

float Function GetStallReputation()
    if !(rms_StallReputation == None)
        return rms_StallReputation.GetValue()
    endif
    return 0.0
EndFunction

Function AddStallReputation(float Amount)
    if rms_StallReputation == None || Amount == 0.0
        return
    endif
    float cur = rms_StallReputation.GetValue()
    float updated = cur + Amount
    if updated > 100.0
        updated = 100.0
    elseif updated < 0.0
        updated = 0.0
    endif
    rms_StallReputation.SetValue(updated)
EndFunction

float Function GetReputationPriceMultiplier()
    float rep = GetStallReputation()
    if rep >= 100.0
        return 1.2
    elseif rep >= 75.0
        return 1.15
    elseif rep >= 50.0
        return 1.1
    elseif rep >= 25.0
        return 1.05
    endif
    return 1.0
EndFunction

float Function GetFollowerCommissionRate()
    float rep = GetStallReputation()
    float baseRate = 20.0
    if !(rms_FollowerWagePercent == None)
        baseRate = rms_FollowerWagePercent.GetValue()
    endif
    if rep >= 100.0
        baseRate = baseRate - 10.0
    elseif rep >= 50.0
        baseRate = baseRate - 5.0
    endif
    if baseRate < 5.0
        baseRate = 5.0
    endif
    return baseRate
EndFunction

Function AwardSpeechcraftXP(int SaleGoldValue, float Multiplier)
    if SaleGoldValue <= 0 || Multiplier <= 0.0
        return
    endif
    float BaseXP = 3.0 + math.Sqrt(SaleGoldValue) * 0.75
    float EarnedXP = BaseXP * Multiplier
    if EarnedXP < 3.0
        EarnedXP = 3.0
    elseif EarnedXP > 45.0
        EarnedXP = 45.0
    endif
    game.AdvanceSkill("Speechcraft", EarnedXP)
EndFunction

Function CheckBusinessDayRollover()
    float CurrentGameDay = utility.GetCurrentGameTime()
    if !(LastBusinessDay == None)
        if CurrentGameDay - LastBusinessDay.GetValue() >= 1.0
            float SoldToday = 0.0
            float RevToday = 0.0
            if !(TodayTransactions == None)
                SoldToday = TodayTransactions.GetValue()
            endif
            if !(TodayRevenue == None)
                RevToday = TodayRevenue.GetValue()
            endif
            if SoldToday > 0.0 || RevToday > 0.0
                debug.Notification("Market day closed. " + (SoldToday as int) + " sales for " + (RevToday as int) + " gold.")
                AddStallReputation(1.0)
            endif
            if !(TodayTransactions == None)
                TodayTransactions.SetValue(0.0)
            endif
            if !(TodayRevenue == None)
                TodayRevenue.SetValue(0.0)
            endif
            LastBusinessDay.SetValue(CurrentGameDay)
        endif
    endif
EndFunction

Function StartPlacementFromItemDrop()
    if GetActiveStallCount() >= 5 || FindAvailableSlot() == -1
        if !(RMS_MSG_MaxStallsReached == None)
            RMS_MSG_MaxStallsReached.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            debug.Notification("You have reached the maximum active stall limit (5/5).")
        endif
        GiveStallBag()   ; Authoria: the bag comes back instead of the kit
        return
    endif
    StartPlacementMode()
EndFunction

bool Function ValidateDeployment()
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None
        return false
    endif
    if PlayerRef.IsInCombat()
        if !(MsgInCombat == None)
            MsgInCombat.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            debug.Notification("You cannot deploy a market stall while in combat.")
        endif
        return false
    endif
    if PlayerRef.IsInInterior()
        if !(MsgInterior == None)
            MsgInterior.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            debug.Notification("You cannot deploy a market stall indoors.")
        endif
        return false
    endif
    if PlayerRef.IsArrested()
        if !(MsgImprisoned == None)
            MsgImprisoned.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            debug.Notification("You cannot deploy a market stall while in prison.")
        endif
        return false
    endif
    return true
EndFunction

Function StartPlacementMode()
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None
        return
    endif
    float pAngle = PlayerRef.GetAngleZ()
    float Distance = 185.0
    DeploymentX = PlayerRef.GetPositionX() + math.Sin(pAngle) * Distance
    DeploymentY = PlayerRef.GetPositionY() + math.Cos(pAngle) * Distance
    DeploymentZ = PlayerRef.GetPositionZ()
    DeploymentAngle = pAngle
    if DeploymentMarkerBase == None
        ExecuteStallBuild()
        return
    endif
    DeploymentMarkerRef = PlayerRef.PlaceAtMe(DeploymentMarkerBase, 1, false, true)
    if DeploymentMarkerRef == None
        ExecuteStallBuild()
        return
    endif
    DeploymentMarkerRef.SetPosition(DeploymentX, DeploymentY, DeploymentZ)
    DeploymentMarkerRef.SetAngle(0.0, 0.0, DeploymentAngle)
    DeploymentMarkerRef.Enable(false)
    if !(PlacementGhostShader == None)
        PlacementGhostShader.Play(DeploymentMarkerRef, -1.0)
    endif
    rms_placementmarkerscript MarkerScript = (DeploymentMarkerRef as rms_placementmarkerscript)
    if !(MarkerScript == None)
        MarkerScript.Controller = Self
    endif
    IsInPlacementMode = true
    bTrackingPaused = false
    KeyReadyWeapon = input.GetMappedKey("Ready Weapon", 255)
    KeyActivate = input.GetMappedKey("Activate", 255)
    KeyShout = input.GetMappedKey("Shout", 255)
    if KeyReadyWeapon > 0
        RegisterForKey(KeyReadyWeapon)
    endif
    if KeyActivate > 0
        RegisterForKey(KeyActivate)
    endif
    if KeyShout > 0
        RegisterForKey(KeyShout)
    endif
    debug.Notification("Aim your stall. Press [R] or [E] to lock in position.")
    RegisterForSingleUpdate(0.05)
EndFunction

Event OnKeyDown(int KeyCode)
    if IsInPlacementMode && !(DeploymentMarkerRef == None)
        if KeyCode == KeyReadyWeapon || KeyCode == KeyActivate || KeyCode == KeyShout
            LockInPlacement()
            return
        endif
    endif
    if IsInFollowerTargetMode
        if KeyCode == KeyActivate
            ProcessCrosshairFollowerTarget()
        elseif KeyCode == KeyReadyWeapon
            CancelFollowerTargeting()
        endif
    endif
EndEvent

Event OnUpdate()
    if !IsInPlacementMode || DeploymentMarkerRef == None
        return
    endif
    if !bTrackingPaused
        Actor PlayerRef = game.GetPlayer()
        if !(PlayerRef == None)
            float pAngle = PlayerRef.GetAngleZ()
            float Distance = 185.0
            float TargetX = PlayerRef.GetPositionX() + math.Sin(pAngle) * Distance
            float TargetY = PlayerRef.GetPositionY() + math.Cos(pAngle) * Distance
            float TargetZ = PlayerRef.GetPositionZ()
            float TargetAngleZ = pAngle
            DeploymentMarkerRef.TranslateTo(TargetX, TargetY, TargetZ, 0.0, 0.0, TargetAngleZ, 1200.0, 500.0)
        endif
    endif
    RegisterForSingleUpdate(0.05)
EndEvent

Function LockInPlacement()
    if !IsInPlacementMode || DeploymentMarkerRef == None
        return
    endif
    bTrackingPaused = true
    DeploymentMarkerRef.StopTranslation()
    int Choice = 0
    if !(RMS_MSG_PlacementMenu == None)
        Choice = RMS_MSG_PlacementMenu.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    else
        Choice = 0
    endif
    if Choice == 0
        ConfirmPlacement()
    else
        CancelPlacement()
    endif
EndFunction

Function CancelPlacement()
    UnregisterForUpdate()
    UnregisterForAllKeys()
    IsInPlacementMode = false
    bTrackingPaused = false
    if !(DeploymentMarkerRef == None)
        if !(PlacementGhostShader == None)
            PlacementGhostShader.Stop(DeploymentMarkerRef)
        endif
        DeploymentMarkerRef.StopTranslation()
        DeploymentMarkerRef.Disable(false)
        DeploymentMarkerRef.Delete()
        DeploymentMarkerRef = None
    endif
    GiveStallBag()   ; Authoria: the bag comes back instead of the kit
    debug.Notification("Market stall placement cancelled. Bag returned.")
EndFunction

Function ConfirmPlacement()
    UnregisterForUpdate()
    UnregisterForAllKeys()
    IsInPlacementMode = false
    bTrackingPaused = false
    if DeploymentMarkerRef == None
        return
    endif
    DeploymentMarkerRef.StopTranslation()
    DeploymentX = DeploymentMarkerRef.GetPositionX()
    DeploymentY = DeploymentMarkerRef.GetPositionY()
    DeploymentZ = DeploymentMarkerRef.GetPositionZ()
    DeploymentAngle = DeploymentMarkerRef.GetAngleZ()
    if !(PlacementGhostShader == None)
        PlacementGhostShader.Stop(DeploymentMarkerRef)
    endif
    DeploymentMarkerRef.Disable(false)
    DeploymentMarkerRef.Delete()
    DeploymentMarkerRef = None
    ExecuteStallBuild()
EndFunction

float Function GetOffsetWorldX(float fOriginX, float fAngle, float fSideOffset, float fFwdOffset)
    return fOriginX + fSideOffset * math.Cos(fAngle) + fFwdOffset * math.Sin(fAngle)
EndFunction

float Function GetOffsetWorldY(float fOriginY, float fAngle, float fSideOffset, float fFwdOffset)
    return fOriginY - fSideOffset * math.Sin(fAngle) + fFwdOffset * math.Cos(fAngle)
EndFunction

form Function GetInvisibleMarkerForm()
    if !(ApproachMarkerBase == None)
        return ApproachMarkerBase
    endif
    form FallbackMarker = game.GetFormFromFile(52, "Skyrim.esm")
    if !(FallbackMarker == None)
        return FallbackMarker
    endif
    return game.GetFormFromFile(59, "Skyrim.esm")
EndFunction

Function ExecuteStallBuild()
    int slotIndex = FindAvailableSlot()
    if slotIndex == -1
        if !(RMS_MSG_MaxStallsReached == None)
            RMS_MSG_MaxStallsReached.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
        GiveStallBag()   ; Authoria: the bag comes back instead of the kit
        return
    endif
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None || StallBase == None
        GiveStallBag()   ; Authoria: the bag comes back instead of the kit
        return
    endif
    ObjectReference stallObj = PlayerRef.PlaceAtMe(StallBase, 1, false, true)
    if stallObj == None
        GiveStallBag()   ; Authoria: the bag comes back instead of the kit
        return
    endif
    stallObj.SetPosition(DeploymentX, DeploymentY, DeploymentZ)
    stallObj.SetAngle(0.0, 0.0, DeploymentAngle)
    ObjectReference foundObj = None
    if !(FoundationBase == None)
        foundObj = PlayerRef.PlaceAtMe(FoundationBase, 1, false, true)
        if !(foundObj == None)
            foundObj.SetPosition(DeploymentX, DeploymentY, DeploymentZ - 4.0)
            foundObj.SetAngle(0.0, 0.0, DeploymentAngle)
        endif
    endif
    ObjectReference merchObj = stallObj.PlaceAtMe(MerchandiseBase, 1, false, true)
    ObjectReference cashObj = stallObj.PlaceAtMe(CashBoxBase, 1, false, true)
    ObjectReference ledgerObj = stallObj.PlaceAtMe(LedgerBase, 1, false, true)
    if merchObj == None || cashObj == None || ledgerObj == None
        if !(stallObj == None)
            stallObj.Disable(false)
            stallObj.Delete()
        endif
        GiveStallBag()   ; Authoria: the bag comes back instead of the kit
        return
    endif
    ObjectReference clutLeft = None
    ObjectReference clutRight = None
    ObjectReference vendMark = None
    ObjectReference navCut = None
    if !(TableClutterLeftBase == None)
        clutLeft = stallObj.PlaceAtMe(TableClutterLeftBase, 1, false, true)
    endif
    if !(TableClutterRightBase == None)
        clutRight = stallObj.PlaceAtMe(TableClutterRightBase, 1, false, true)
    endif
    if !(VendorMarkerBase == None)
        vendMark = stallObj.PlaceAtMe(VendorMarkerBase, 1, false, true)
    endif
    if !(StallNavCutterHelperBase == None)
        navCut = stallObj.PlaceAtMe(StallNavCutterHelperBase, 1, false, true)
        if !(navCut == None)
            navCut.SetPosition(DeploymentX, DeploymentY, DeploymentZ)
            navCut.SetAngle(0.0, 0.0, DeploymentAngle)
        endif
    endif
    form MarkerForm = GetInvisibleMarkerForm()
    ObjectReference cust1 = None
    ObjectReference cust2 = None
    ObjectReference cust3 = None
    if !(MarkerForm == None)
        cust1 = stallObj.PlaceAtMe(MarkerForm, 1, false, true)
        cust2 = stallObj.PlaceAtMe(MarkerForm, 1, false, true)
        cust3 = stallObj.PlaceAtMe(MarkerForm, 1, false, true)
    endif
    float sX = DeploymentX
    float sY = DeploymentY
    float sZ = DeploymentZ
    float sAngle = DeploymentAngle
    merchObj.SetPosition(sX, sY, sZ)
    merchObj.SetAngle(0.0, 0.0, sAngle + 180.0)
    cashObj.SetPosition(GetOffsetWorldX(sX, sAngle, 68.0, 4.0), GetOffsetWorldY(sY, sAngle, 68.0, 4.0), sZ + 75.0)
    cashObj.SetAngle(0.0, 0.0, sAngle + 180.0)
    ledgerObj.SetPosition(GetOffsetWorldX(sX, sAngle, -68.0, 4.0), GetOffsetWorldY(sY, sAngle, -68.0, 4.0), sZ + 79.0)
    ledgerObj.SetAngle(0.0, 0.0, sAngle - 30.0)
    if !(clutLeft == None)
        clutLeft.SetPosition(GetOffsetWorldX(sX, sAngle, -24.0, 18.0), GetOffsetWorldY(sY, sAngle, -24.0, 18.0), sZ + 75.0)
        clutLeft.SetAngle(0.0, 0.0, sAngle - 70.0)
    endif
    if !(clutRight == None)
        clutRight.SetPosition(GetOffsetWorldX(sX, sAngle, 24.0, 18.0), GetOffsetWorldY(sY, sAngle, 24.0, 18.0), sZ + 75.0)
        clutRight.SetAngle(0.0, 0.0, sAngle - 110.0)
    endif
    if !(vendMark == None)
        vendMark.SetPosition(GetOffsetWorldX(sX, sAngle, 0.0, -105.0), GetOffsetWorldY(sY, sAngle, 0.0, -105.0), sZ)
        vendMark.SetAngle(0.0, 0.0, sAngle)
    endif
    if !(cust1 == None)
        cust1.SetPosition(GetOffsetWorldX(sX, sAngle, 0.0, 90.0), GetOffsetWorldY(sY, sAngle, 0.0, 90.0), sZ)
        cust1.SetAngle(0.0, 0.0, sAngle + 180.0)
    endif
    if !(cust2 == None)
        cust2.SetPosition(GetOffsetWorldX(sX, sAngle, -35.0, 90.0), GetOffsetWorldY(sY, sAngle, -35.0, 90.0), sZ)
        cust2.SetAngle(0.0, 0.0, sAngle + 180.0)
    endif
    if !(cust3 == None)
        cust3.SetPosition(GetOffsetWorldX(sX, sAngle, 35.0, 90.0), GetOffsetWorldY(sY, sAngle, 35.0, 90.0), sZ)
        cust3.SetAngle(0.0, 0.0, sAngle + 180.0)
    endif
    stallObj.Enable(false)
    if !(foundObj == None)
        foundObj.Enable(false)
    endif
    merchObj.Enable(false)
    cashObj.Enable(false)
    ledgerObj.Enable(false)
    if !(clutLeft == None)
        clutLeft.Enable(false)
    endif
    if !(clutRight == None)
        clutRight.Enable(false)
    endif
    if !(vendMark == None)
        vendMark.Enable(false)
    endif
    if !(navCut == None)
        navCut.Enable(false)
    endif
    if !(cust1 == None)
        cust1.Enable(false)
    endif
    if !(cust2 == None)
        cust2.Enable(false)
    endif
    if !(cust3 == None)
        cust3.Enable(false)
    endif
    if !(PlayerFaction == None)
        cashObj.SetFactionOwner(PlayerFaction)
    endif
    SlotOccupied[slotIndex] = true
    SlotStallRefs[slotIndex] = stallObj
    SlotFoundationRefs[slotIndex] = foundObj
    SlotMerchandiseRefs[slotIndex] = merchObj
    SlotCashBoxRefs[slotIndex] = cashObj
    SlotLedgerRefs[slotIndex] = ledgerObj
    SlotClutterLeftRefs[slotIndex] = clutLeft
    SlotClutterRightRefs[slotIndex] = clutRight
    SlotVendorMarkerRefs[slotIndex] = vendMark
    SlotNavCutterRefs[slotIndex] = navCut
    SlotFollowerRefs[slotIndex] = None
    SlotSimTimestamps[slotIndex] = utility.GetCurrentGameTime()
    SlotCustomerMarker1Refs[slotIndex] = cust1
    SlotCustomerMarker2Refs[slotIndex] = cust2
    SlotCustomerMarker3Refs[slotIndex] = cust3
    string locName = "Skyrim"
    location curLoc = PlayerRef.GetCurrentLocation()
    if !(curLoc == None) && !(curLoc.GetName() == "")
        locName = curLoc.GetName()
    endif
    SlotLocationNames[slotIndex] = locName
    if !(rms_ActiveStallCount == None)
        rms_ActiveStallCount.SetValue(GetActiveStallCount())
    endif
    BindCustomerAliasesToSlot(slotIndex)
    if !(SoundDeploy == None)
        SoundDeploy.Play(stallObj)
    endif
    if !(MsgDeploySuccess == None)
        MsgDeploySuccess.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    else
        debug.Notification("Market Stall deployed in " + locName + " (Slot " + (slotIndex + 1) + "/5).")
    endif
    UpdateCustomerScheduler()
EndFunction

Function DisassembleSlot(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    ObjectReference merch = SlotMerchandiseRefs[aiSlot]
    ObjectReference cash = SlotCashBoxRefs[aiSlot]
    if !(merch == None) && merch.GetNumItems() > 0
        if !(MsgInventoryNotEmpty == None)
            MsgInventoryNotEmpty.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            debug.Notification("Cannot pack up stall while merchandise remains in the chest.")
        endif
        return
    endif
    if !(cash == None) && !(CashBoxSystem == None)
        CashBoxSystem.SetCashBoxReference(cash)
        if CashBoxSystem.GetCash() > 0
            if !(MsgCashNotEmpty == None)
                MsgCashNotEmpty.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            else
                debug.Notification("Cannot pack up stall while uncollected gold remains in the strongbox.")
            endif
            return
        endif
    endif
    if GetNearestActiveSlot() == aiSlot
        ClearCustomerSlots()
    endif
    StopSlotFollower(aiSlot)
    if !(SoundDisassemble == None) && !(SlotStallRefs[aiSlot] == None)
        SoundDisassemble.Play(SlotStallRefs[aiSlot])
    endif
    if !(SlotFoundationRefs[aiSlot] == None)
        SlotFoundationRefs[aiSlot].Disable(false)
        SlotFoundationRefs[aiSlot].Delete()
    endif
    if !(SlotClutterLeftRefs[aiSlot] == None)
        SlotClutterLeftRefs[aiSlot].Disable(false)
        SlotClutterLeftRefs[aiSlot].Delete()
    endif
    if !(SlotClutterRightRefs[aiSlot] == None)
        SlotClutterRightRefs[aiSlot].Disable(false)
        SlotClutterRightRefs[aiSlot].Delete()
    endif
    if !(SlotVendorMarkerRefs[aiSlot] == None)
        SlotVendorMarkerRefs[aiSlot].Disable(false)
        SlotVendorMarkerRefs[aiSlot].Delete()
    endif
    if !(SlotNavCutterRefs[aiSlot] == None)
        SlotNavCutterRefs[aiSlot].Disable(false)
        SlotNavCutterRefs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker1Refs[aiSlot] == None)
        SlotCustomerMarker1Refs[aiSlot].Disable(false)
        SlotCustomerMarker1Refs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker2Refs[aiSlot] == None)
        SlotCustomerMarker2Refs[aiSlot].Disable(false)
        SlotCustomerMarker2Refs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker3Refs[aiSlot] == None)
        SlotCustomerMarker3Refs[aiSlot].Disable(false)
        SlotCustomerMarker3Refs[aiSlot].Delete()
    endif
    if !(SlotMerchandiseRefs[aiSlot] == None)
        SlotMerchandiseRefs[aiSlot].Disable(false)
        SlotMerchandiseRefs[aiSlot].Delete()
    endif
    if !(SlotCashBoxRefs[aiSlot] == None)
        SlotCashBoxRefs[aiSlot].Disable(false)
        SlotCashBoxRefs[aiSlot].Delete()
    endif
    if !(SlotLedgerRefs[aiSlot] == None)
        SlotLedgerRefs[aiSlot].Disable(false)
        SlotLedgerRefs[aiSlot].Delete()
    endif
    if !(SlotStallRefs[aiSlot] == None)
        SlotStallRefs[aiSlot].Disable(false)
        SlotStallRefs[aiSlot].Delete()
    endif
    SlotOccupied[aiSlot] = false
    SlotStallRefs[aiSlot] = None
    SlotFoundationRefs[aiSlot] = None
    SlotMerchandiseRefs[aiSlot] = None
    SlotCashBoxRefs[aiSlot] = None
    SlotLedgerRefs[aiSlot] = None
    SlotClutterLeftRefs[aiSlot] = None
    SlotClutterRightRefs[aiSlot] = None
    SlotVendorMarkerRefs[aiSlot] = None
    SlotNavCutterRefs[aiSlot] = None
    SlotFollowerRefs[aiSlot] = None
    SlotSimTimestamps[aiSlot] = 0.0
    SlotLocationNames[aiSlot] = ""
    if !(rms_ActiveStallCount == None)
        rms_ActiveStallCount.SetValue(GetActiveStallCount())
    endif
    GiveStallBag(false)   ; Authoria: the packed stall goes back into the player's bag
    if !(MsgDisassembled == None)
        MsgDisassembled.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    else
        debug.Notification("Market Stall packed up. Bag returned to inventory.")
    endif
    UpdateCustomerScheduler()
EndFunction

Function EmergencyRecallSlot(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None
        return
    endif
    if GetNearestActiveSlot() == aiSlot
        ClearCustomerSlots()
    endif
    StopSlotFollower(aiSlot)
    if !(SlotMerchandiseRefs[aiSlot] == None)
        SlotMerchandiseRefs[aiSlot].RemoveAllItems(PlayerRef, true, false)
    endif
    if !(SlotCashBoxRefs[aiSlot] == None)
        SlotCashBoxRefs[aiSlot].RemoveAllItems(PlayerRef, true, false)
    endif
    if !(SlotFoundationRefs[aiSlot] == None)
        SlotFoundationRefs[aiSlot].Disable(false)
        SlotFoundationRefs[aiSlot].Delete()
    endif
    if !(SlotClutterLeftRefs[aiSlot] == None)
        SlotClutterLeftRefs[aiSlot].Disable(false)
        SlotClutterLeftRefs[aiSlot].Delete()
    endif
    if !(SlotClutterRightRefs[aiSlot] == None)
        SlotClutterRightRefs[aiSlot].Disable(false)
        SlotClutterRightRefs[aiSlot].Delete()
    endif
    if !(SlotVendorMarkerRefs[aiSlot] == None)
        SlotVendorMarkerRefs[aiSlot].Disable(false)
        SlotVendorMarkerRefs[aiSlot].Delete()
    endif
    if !(SlotNavCutterRefs[aiSlot] == None)
        SlotNavCutterRefs[aiSlot].Disable(false)
        SlotNavCutterRefs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker1Refs[aiSlot] == None)
        SlotCustomerMarker1Refs[aiSlot].Disable(false)
        SlotCustomerMarker1Refs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker2Refs[aiSlot] == None)
        SlotCustomerMarker2Refs[aiSlot].Disable(false)
        SlotCustomerMarker2Refs[aiSlot].Delete()
    endif
    if !(SlotCustomerMarker3Refs[aiSlot] == None)
        SlotCustomerMarker3Refs[aiSlot].Disable(false)
        SlotCustomerMarker3Refs[aiSlot].Delete()
    endif
    if !(SlotMerchandiseRefs[aiSlot] == None)
        SlotMerchandiseRefs[aiSlot].Disable(false)
        SlotMerchandiseRefs[aiSlot].Delete()
    endif
    if !(SlotCashBoxRefs[aiSlot] == None)
        SlotCashBoxRefs[aiSlot].Disable(false)
        SlotCashBoxRefs[aiSlot].Delete()
    endif
    if !(SlotLedgerRefs[aiSlot] == None)
        SlotLedgerRefs[aiSlot].Disable(false)
        SlotLedgerRefs[aiSlot].Delete()
    endif
    if !(SlotStallRefs[aiSlot] == None)
        SlotStallRefs[aiSlot].Disable(false)
        SlotStallRefs[aiSlot].Delete()
    endif
    string recLoc = SlotLocationNames[aiSlot]
    SlotOccupied[aiSlot] = false
    SlotStallRefs[aiSlot] = None
    SlotFoundationRefs[aiSlot] = None
    SlotMerchandiseRefs[aiSlot] = None
    SlotCashBoxRefs[aiSlot] = None
    SlotLedgerRefs[aiSlot] = None
    SlotClutterLeftRefs[aiSlot] = None
    SlotClutterRightRefs[aiSlot] = None
    SlotVendorMarkerRefs[aiSlot] = None
    SlotNavCutterRefs[aiSlot] = None
    SlotFollowerRefs[aiSlot] = None
    SlotSimTimestamps[aiSlot] = 0.0
    SlotLocationNames[aiSlot] = ""
    if !(rms_ActiveStallCount == None)
        rms_ActiveStallCount.SetValue(GetActiveStallCount())
    endif
    GiveStallBag(false)   ; Authoria: the recalled stall goes back into the player's bag
    debug.Notification("Emergency Recall: Stall in " + recLoc + " recalled. Remaining stock and bag returned.")
    UpdateCustomerScheduler()
EndFunction

bool Function IsFollowerAlreadyAssigned(Actor akActor)
    if akActor == None
        return false
    endif
    int i = 0
    while i < 5
        if SlotOccupied[i] && SlotFollowerRefs[i] == akActor
            return true
        endif
        i = i + 1
    endwhile
    return false
EndFunction

Function ManageSlotFollower(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    if !(SlotFollowerRefs[aiSlot] == None)
        StopSlotFollower(aiSlot)
        return
    endif
    StartFollowerTargeting(aiSlot)
EndFunction

Function StartFollowerTargeting(int aiSlot)
    if IsInPlacementMode
        return
    endif
    IsInFollowerTargetMode = true
    iTargetingSlot = aiSlot
    KeyActivate = input.GetMappedKey("Activate", 255)
    KeyReadyWeapon = input.GetMappedKey("Ready Weapon", 255)
    if KeyActivate > 0
        RegisterForKey(KeyActivate)
    endif
    if KeyReadyWeapon > 0
        RegisterForKey(KeyReadyWeapon)
    endif
    debug.Notification("Target Mode: Aim at your companion and press [E] / Activate. Press [R] to cancel.")
EndFunction

Function CancelFollowerTargeting()
    if !IsInFollowerTargetMode
        return
    endif
    UnregisterForAllKeys()
    IsInFollowerTargetMode = false
    iTargetingSlot = -1
    debug.Notification("Stall attendant assignment cancelled.")
EndFunction

Function ProcessCrosshairFollowerTarget()
    if !IsInFollowerTargetMode || iTargetingSlot < 0 || iTargetingSlot >= 5
        return
    endif
    ObjectReference crosshairRef = game.GetCurrentCrosshairRef()
    Actor targetActor = (crosshairRef as Actor)
    if targetActor == None
        return
    endif
    if targetActor == game.GetPlayer()
        return
    endif
    if targetActor.IsDead()
        debug.Notification("You cannot assign a deceased companion.")
        return
    endif
    if !targetActor.IsPlayerTeammate()
        debug.Notification(targetActor.GetActorBase().GetName() + " is not an active companion.")
        return
    endif
    if IsFollowerAlreadyAssigned(targetActor)
        debug.Notification(targetActor.GetActorBase().GetName() + " is already tending another market stall.")
        return
    endif
    int targetSlot = iTargetingSlot
    UnregisterForAllKeys()
    IsInFollowerTargetMode = false
    iTargetingSlot = -1
    AssignSlotFollower(targetSlot, targetActor)
EndFunction

Function AssignSlotFollower(int aiSlot, Actor akFollower)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot] || akFollower == None
        return
    endif
    SlotFollowerRefs[aiSlot] = akFollower
    SlotSimTimestamps[aiSlot] = utility.GetCurrentGameTime()
    if !(FollowerVendorAlias == None)
        FollowerVendorAlias.ForceRefTo(akFollower)
    endif
    akFollower.EvaluatePackage()
    debug.Notification(akFollower.GetActorBase().GetName() + " is now tending stall #" + (aiSlot + 1) + " (" + SlotLocationNames[aiSlot] + ").")
EndFunction

Function StopSlotFollower(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    Actor fol = SlotFollowerRefs[aiSlot]
    if !(fol == None)
        SimulateSlotFollowerSales(aiSlot)
        SlotFollowerRefs[aiSlot] = None
        if !(FollowerVendorAlias == None) && FollowerVendorAlias.GetReference() == fol
            FollowerVendorAlias.Clear()
        endif
        fol.EvaluatePackage()
        debug.Notification(fol.GetActorBase().GetName() + " relieved from stall #" + (aiSlot + 1) + ".")
    endif
EndFunction

Function SimulateSlotFollowerSales(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    Actor currentTender = SlotFollowerRefs[aiSlot]
    ObjectReference merch = SlotMerchandiseRefs[aiSlot]
    ObjectReference cash = SlotCashBoxRefs[aiSlot]
    if currentTender == None || merch == None || cash == None || InventorySystem == None || CashBoxSystem == None
        return
    endif
    float curTime = utility.GetCurrentGameTime()
    float deltaDays = curTime - SlotSimTimestamps[aiSlot]
    SlotSimTimestamps[aiSlot] = curTime
    if deltaDays <= 0.0
        return
    endif
    if deltaDays > 3.0
        deltaDays = 3.0
    endif
    float ratePerHour = 0.5
    if !(rms_FollowerSalesPerHour == None)
        float val = rms_FollowerSalesPerHour.GetValue()
        if val > 0.0
            ratePerHour = val
        endif
    endif
    int salesTarget = math.Floor(deltaDays * 24.0 * ratePerHour)
    if salesTarget <= 0
        return
    endif
    int actualSold = 0
    int totalGross = 0
    int distinctCount = merch.GetNumItems()
    while distinctCount > 0 && actualSold < salesTarget
        distinctCount = distinctCount - 1
        form itemForm = merch.GetNthForm(distinctCount)
        if !(itemForm == None) && itemForm.GetGoldValue() > 0 && !(itemForm.GetFormID() == 15)
            int itemQty = merch.GetItemCount(itemForm)
            int needed = salesTarget - actualSold
            int qtyToSell = itemQty
            if qtyToSell > needed
                qtyToSell = needed
            endif
            if qtyToSell > 0
                int singleVal = InventorySystem.CalculateRetailPrice(itemForm, currentTender)
                if singleVal > 0
                    merch.RemoveItem(itemForm, qtyToSell, true)
                    actualSold = actualSold + qtyToSell
                    totalGross = totalGross + singleVal * qtyToSell
                endif
            endif
        endif
    endwhile
    if actualSold > 0
        float commRate = GetFollowerCommissionRate()
        int followerCut = math.Floor(totalGross * (commRate / 100.0))
        int netProfit = totalGross - followerCut
        CashBoxSystem.SetCashBoxReference(cash)
        CashBoxSystem.AddCash(netProfit)
        if !(TotalTransactions == None)
            TotalTransactions.SetValue(TotalTransactions.GetValue() + actualSold)
        endif
        if !(TotalRevenue == None)
            TotalRevenue.SetValue(TotalRevenue.GetValue() + netProfit)
        endif
        AwardSpeechcraftXP(netProfit, 0.15)
        AddStallReputation(actualSold * 0.2)
        debug.Notification(currentTender.GetActorBase().GetName() + " sold " + actualSold + " items (" + netProfit + "g earned, " + followerCut + "g wage).")
    endif
EndFunction

Function SimulateAllRemoteStalls()
    int i = 0
    while i < 5
        if SlotOccupied[i] && !(SlotFollowerRefs[i] == None)
            SimulateSlotFollowerSales(i)
        endif
        i = i + 1
    endwhile
    debug.Notification("Audit complete: All active franchise accounts synchronized.")
EndFunction

int Function CollectAllCentralRevenue()
    SimulateAllRemoteStalls()
    int totalCollected = 0
    Actor PlayerRef = game.GetPlayer()
    if PlayerRef == None || CashBoxSystem == None
        return 0
    endif
    int i = 0
    while i < 5
        if SlotOccupied[i] && !(SlotCashBoxRefs[i] == None)
            CashBoxSystem.SetCashBoxReference(SlotCashBoxRefs[i])
            int amt = CashBoxSystem.CollectCash()
            if amt > 0
                totalCollected = totalCollected + amt
            endif
        endif
        i = i + 1
    endwhile
    if totalCollected > 0
        if !(SoundGoldTake == None)
            SoundGoldTake.Play(PlayerRef)
        endif
        debug.Notification("Collected " + totalCollected + " Gold from all active market stalls.")
    else
        debug.Notification("No pending gold in any stall strongboxes.")
    endif
    return totalCollected
EndFunction

Function OpenLedger(ObjectReference akLedgerRef)
    int slotIndex = GetSlotForReference(akLedgerRef)
    if slotIndex == -1
        return
    endif
    if !(SlotFollowerRefs[slotIndex] == None)
        SimulateSlotFollowerSales(slotIndex)
    endif
    if !(SoundBook == None)
        SoundBook.Play(akLedgerRef)
    endif
    string locName = SlotLocationNames[slotIndex]
    if locName == ""
        locName = "Skyrim"
    endif
    bool menuOpen = true
    while menuOpen
        int Choice = -1
        if !(RMS_MSG_LedgerMenu == None)
            Choice = RMS_MSG_LedgerMenu.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
        if Choice == 0
            ShowSalesOverview()
        elseif Choice == 1
            ShowEnterpriseVaultMenu()
        elseif Choice == 2
            ShowInventoryOverview(slotIndex)
        elseif Choice == 3
            ShowLocalCash(slotIndex)
        elseif Choice == 4
            menuOpen = false
            ManageSlotFollower(slotIndex)
        elseif Choice == 5
            menuOpen = false
            DisassembleSlot(slotIndex)
        else
            menuOpen = false
        endif
    endwhile
    UpdateCustomerScheduler()
EndFunction

Function ShowSalesOverview()
    if !(RMS_MSG_LedgerSales == None)
        float sSold = 0.0
        float sRev = 0.0
        if !(TotalItemsSold == None)
            sSold = TotalItemsSold.GetValue()
        endif
        if !(TotalRevenue == None)
            sRev = TotalRevenue.GetValue()
        endif
        RMS_MSG_LedgerSales.Show(sSold, sRev, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    endif
EndFunction

Function ShowInventoryOverview(int aiSlot)
    if !(RMS_MSG_LedgerInventory == None) && !(SlotMerchandiseRefs[aiSlot] == None)
        InventorySystem.SetMerchandiseReference(SlotMerchandiseRefs[aiSlot])
        InventorySystem.ScanInventory()
        float distinct = InventorySystem.GetSellableItemCount()
        float units = InventorySystem.GetTotalItemUnits()
        RMS_MSG_LedgerInventory.Show(distinct, units, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    endif
EndFunction

Function ShowLocalCash(int aiSlot)
    if !(RMS_MSG_LedgerCash == None) && !(SlotCashBoxRefs[aiSlot] == None)
        CashBoxSystem.SetCashBoxReference(SlotCashBoxRefs[aiSlot])
        float cur = CashBoxSystem.GetCash()
        RMS_MSG_LedgerCash.Show(cur, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    endif
EndFunction

Function ShowEnterpriseVaultMenu()
    bool vaultMenuOpen = true
    while vaultMenuOpen
        int Choice = -1
        if !(RMS_MSG_MasterVaultMenu == None)
            Choice = RMS_MSG_MasterVaultMenu.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
        if Choice == 0
            CollectAllCentralRevenue()
        elseif Choice == 1
            SimulateAllRemoteStalls()
        elseif Choice == 2
            ShowReputationStanding()
        elseif Choice == 3
            PromptEmergencyRecallMenu()
        else
            vaultMenuOpen = false
        endif
    endwhile
EndFunction

Function PromptEmergencyRecallMenu()
    if RMS_MSG_RecallSelectMenu == None
        return
    endif
    int Choice = RMS_MSG_RecallSelectMenu.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    if Choice >= 0 && Choice <= 4
        if !SlotOccupied[Choice]
            debug.Notification("Franchise Slot " + (Choice + 1) + " is currently empty.")
            return
        endif
        string loc = SlotLocationNames[Choice]
        string tenderName = "Unattended"
        if !(SlotFollowerRefs[Choice] == None)
            tenderName = SlotFollowerRefs[Choice].GetActorBase().GetName()
        endif
        debug.Notification("Inspecting Slot " + (Choice + 1) + ": " + loc + " (" + tenderName + ")")
        int confirmChoice = 1
        if !(RMS_MSG_RecallConfirm == None)
            confirmChoice = RMS_MSG_RecallConfirm.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            confirmChoice = 0
        endif
        if confirmChoice == 0
            EmergencyRecallSlot(Choice)
        endif
    endif
EndFunction

Function ShowReputationStanding()
    if !(RMS_MSG_ReputationMenu == None)
        float rep = GetStallReputation()
        float priceBonus = (GetReputationPriceMultiplier() - 1.0) * 100.0
        float wageCut = GetFollowerCommissionRate()
        float sold = 0.0
        float rev = 0.0
        if !(TotalItemsSold == None)
            sold = TotalItemsSold.GetValue()
        endif
        if !(TotalRevenue == None)
            rev = TotalRevenue.GetValue()
        endif
        RMS_MSG_ReputationMenu.Show(rep, priceBonus, wageCut, sold, rev, 0.0, 0.0, 0.0, 0.0)
    endif
EndFunction

Function UpdateCustomerScheduler()
    int activeNearSlot = GetNearestActiveSlot()
    if !(activeNearSlot == -1) && !CustomerSchedulerRunning
        CustomerSchedulerRunning = true
        BindCustomerAliasesToSlot(activeNearSlot)
        CustomerSchedulerLoop()
    elseif activeNearSlot == -1 && CustomerSchedulerRunning
        CustomerSchedulerRunning = false
        ClearCustomerSlots()
    endif
EndFunction

Function BindCustomerAliasesToSlot(int aiSlot)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot]
        return
    endif
    if !(StallAlias == None) && !(SlotStallRefs[aiSlot] == None)
        StallAlias.ForceRefTo(SlotStallRefs[aiSlot])
    endif
    if !(MerchandiseAlias == None) && !(SlotMerchandiseRefs[aiSlot] == None)
        MerchandiseAlias.ForceRefTo(SlotMerchandiseRefs[aiSlot])
    endif
    if !(CashBoxAlias == None) && !(SlotCashBoxRefs[aiSlot] == None)
        CashBoxAlias.ForceRefTo(SlotCashBoxRefs[aiSlot])
    endif
    if !(LedgerAlias == None) && !(SlotLedgerRefs[aiSlot] == None)
        LedgerAlias.ForceRefTo(SlotLedgerRefs[aiSlot])
    endif
    if !(VendorMarkerAlias == None) && !(SlotVendorMarkerRefs[aiSlot] == None)
        VendorMarkerAlias.ForceRefTo(SlotVendorMarkerRefs[aiSlot])
    endif
    if !(CustomerMarker1Alias == None) && !(SlotCustomerMarker1Refs[aiSlot] == None)
        CustomerMarker1Alias.ForceRefTo(SlotCustomerMarker1Refs[aiSlot])
    endif
    if !(CustomerMarker2Alias == None) && !(SlotCustomerMarker2Refs[aiSlot] == None)
        CustomerMarker2Alias.ForceRefTo(SlotCustomerMarker2Refs[aiSlot])
    endif
    if !(CustomerMarker3Alias == None) && !(SlotCustomerMarker3Refs[aiSlot] == None)
        CustomerMarker3Alias.ForceRefTo(SlotCustomerMarker3Refs[aiSlot])
    endif
    if !(InventorySystem == None) && !(SlotMerchandiseRefs[aiSlot] == None)
        InventorySystem.SetMerchandiseReference(SlotMerchandiseRefs[aiSlot])
    endif
    if !(CashBoxSystem == None) && !(SlotCashBoxRefs[aiSlot] == None)
        CashBoxSystem.SetCashBoxReference(SlotCashBoxRefs[aiSlot])
    endif
EndFunction

Function ClearCustomerSlots()
    if !(Customer1Alias == None)
        rms_customerslotscript slot1 = (Customer1Alias as rms_customerslotscript)
        if !(slot1 == None)
            slot1.AbortCustomer()
        else
            Customer1Alias.Clear()
        endif
    endif
    if !(Customer2Alias == None)
        rms_customerslotscript slot2 = (Customer2Alias as rms_customerslotscript)
        if !(slot2 == None)
            slot2.AbortCustomer()
        else
            Customer2Alias.Clear()
        endif
    endif
    if !(Customer3Alias == None)
        rms_customerslotscript slot3 = (Customer3Alias as rms_customerslotscript)
        if !(slot3 == None)
            slot3.AbortCustomer()
        else
            Customer3Alias.Clear()
        endif
    endif
EndFunction

Function CustomerSchedulerLoop()
    while CustomerSchedulerRunning
        int nearSlot = GetNearestActiveSlot()
        if nearSlot == -1
            CustomerSchedulerRunning = false
            ClearCustomerSlots()
            return
        endif
        BindCustomerAliasesToSlot(nearSlot)
        float minInt = 10.0
        float maxInt = 20.0
        if !(MinCustomerInterval == None) && MinCustomerInterval.GetValue() > 0.0
            minInt = MinCustomerInterval.GetValue()
        endif
        if !(MaxCustomerInterval == None) && MaxCustomerInterval.GetValue() > 0.0
            maxInt = MaxCustomerInterval.GetValue()
        endif
        float interval = utility.RandomFloat(minInt, maxInt)
        if interval < 5.0
            interval = 5.0
        endif
        utility.Wait(interval)
        if !CustomerSchedulerRunning
            return
        endif
        nearSlot = GetNearestActiveSlot()
        if !(nearSlot == -1) && !(SlotMerchandiseRefs[nearSlot] == None)
            if SlotMerchandiseRefs[nearSlot].GetNumItems() > 0
                StartAvailableCustomer(nearSlot)
            endif
        endif
    endwhile
EndFunction

Function StartAvailableCustomer(int aiSlot)
    if !(Customer1Alias == None) && Customer1Alias.GetReference() == None
        StartCustomerInSlot(Customer1Alias, aiSlot)
        return
    endif
    if !(Customer2Alias == None) && Customer2Alias.GetReference() == None
        StartCustomerInSlot(Customer2Alias, aiSlot)
        return
    endif
    if !(Customer3Alias == None) && Customer3Alias.GetReference() == None
        StartCustomerInSlot(Customer3Alias, aiSlot)
        return
    endif
EndFunction

Function StartCustomerInSlot(referencealias akSlot, int aiSlot)
    if akSlot == None || SlotStallRefs[aiSlot] == None
        return
    endif
    Actor candidate = FindEligibleCustomer(SlotStallRefs[aiSlot])
    if candidate == None
        return
    endif
    RecentCustomer4 = RecentCustomer3
    RecentCustomer3 = RecentCustomer2
    RecentCustomer2 = RecentCustomer1
    RecentCustomer1 = candidate
    akSlot.ForceRefTo(candidate)
    rms_customerslotscript scriptRef = (akSlot as rms_customerslotscript)
    if !(scriptRef == None)
        scriptRef.QueueVisit()
    endif
EndFunction

Actor Function FindEligibleCustomer(ObjectReference akStall)
    if akStall == None
        return None
    endif
    float rad = 2000.0
    if !(CustomerSearchRadius == None) && CustomerSearchRadius.GetValue() > 0.0
        rad = CustomerSearchRadius.GetValue()
    endif
    Actor PlayerRef = game.GetPlayer()
    int attempts = 0
    while attempts < 35
        Actor c = game.FindRandomActorFromRef(akStall, rad)
        if !(c == None) && !(c == PlayerRef)
            if !c.IsDead() && !c.IsEssential() && !c.IsInCombat() && !c.IsChild() && !c.IsGuard()
                if !(c == RecentCustomer1) && !(c == RecentCustomer2) && !(c == RecentCustomer3) && !(c == RecentCustomer4)
                    float dx = c.GetPositionX() - akStall.GetPositionX()
                    float dy = c.GetPositionY() - akStall.GetPositionY()
                    float ang = akStall.GetAngleZ()
                    float fwd = dx * math.Sin(ang) + dy * math.Cos(ang)
                    if fwd >= 20.0
                        return c
                    endif
                endif
            endif
        endif
        if attempts == 15
            RecentCustomer4 = None
            RecentCustomer3 = None
        endif
        attempts = attempts + 1
    endwhile
    RecentCustomer4 = None
    RecentCustomer3 = None
    RecentCustomer2 = None
    return None
EndFunction

int Function ProcessSale(form akItem)
    int nearSlot = GetNearestActiveSlot()
    if !(nearSlot == -1)
        return ProcessSaleForSlot(nearSlot, akItem)
    endif
    return 0
EndFunction

int Function ProcessSaleForSlot(int aiSlot, form akItem)
    if aiSlot < 0 || aiSlot >= 5 || !SlotOccupied[aiSlot] || akItem == None
        return 0
    endif
    ObjectReference merch = SlotMerchandiseRefs[aiSlot]
    ObjectReference cash = SlotCashBoxRefs[aiSlot]
    Actor tender = SlotFollowerRefs[aiSlot]
    if tender == None
        tender = game.GetPlayer()
    endif
    if merch == None || cash == None || InventorySystem == None || CashBoxSystem == None
        return 0
    endif
    InventorySystem.SetMerchandiseReference(merch)
    int saleVal = InventorySystem.SellOneItem(akItem, tender)
    if saleVal <= 0
        return 0
    endif
    CashBoxSystem.SetCashBoxReference(cash)
    CashBoxSystem.AddCash(saleVal)
    if !(SoundCoin == None)
        SoundCoin.Play(cash)
    endif
    if !(TotalTransactions == None)
        TotalTransactions.SetValue(TotalTransactions.GetValue() + 1.0)
    endif
    if !(TotalItemsSold == None)
        TotalItemsSold.SetValue(TotalItemsSold.GetValue() + 1.0)
    endif
    if !(TotalRevenue == None)
        TotalRevenue.SetValue(TotalRevenue.GetValue() + saleVal)
    endif
    AwardSpeechcraftXP(saleVal, 1.0)
    AddStallReputation(0.2)
    CheckBusinessDayRollover()
    return saleVal
EndFunction

