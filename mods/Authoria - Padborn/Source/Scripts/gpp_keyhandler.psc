ScriptName gpp_keyhandler extends ReferenceAlias
{Gamepad++ key handler - Authoria build 3.5.
Stock Gamepad++ 2.5 (the Complete Controller Setup repack) plus three changes:
 1. Menu guard fixed. Stock `if !MenuName == "FavoritesMenu"` parses as (!MenuName) == "..." and is
    always false, so GPP never disabled itself in menus. Now `if !(MenuName == "FavoritesMenu")`.
 2. QuickLoot guard fixed. Stock checked the old QuickLoot RE window ("Loot Menu"); QuickLoot IE
    registers "LootMenu". D-pad Up/Down gestures are inert while either is open - see isLootWindowOpen.
 3. All 16 non-combo D-pad slots are set explicitly - see ApplyAuthoriaBindings.
getVersion() is pinned at 3.5 on purpose: a bump makes checkVersion() reset the hold slots and combo
keys in every existing save. Properties and script variables are identical to stock, so this script
is save-safe over stock 2.5.}

bool bIsC4Held
int iMultiTap
bool bIsC2Held
int iWaitingKeyCode = -1
int[] aiActionKeys
float fCurrentVersion
bool bIsC3Held
bool bIsC1Held

int Property GPP_KEYCODE_A4 = 267 Auto Hidden
int[] Property aiC3Actions Auto Hidden
bool Property bAllowKeyPress = true Auto Hidden
int Property GPP_KEYCODE_A2 = 269 Auto Hidden
int[] Property aiC1Actions Auto Hidden
bool Property bConsoleUtilLoaded Auto Hidden
int[] Property aiiEquipKeys Auto Hidden
globalvariable Property GPP_COMBO3 Auto
int[] Property aiNonComboActions Auto Hidden
int Property GPP_KEYCODE_A1 = 268 Auto Hidden
int Property GPP_KEYCODE_C1 = 276 Auto Hidden
bool Property bFourthComboEnabled Auto Hidden
globalvariable Property GPP_COMBO1 Auto
bool Property biEquipLoaded Auto Hidden
int Property GPP_HOTKEY_TIM Auto Hidden
int Property GPP_KEYCODE_C3 = -1 Auto Hidden
bool Property bMultiTapEnabled = true Auto Hidden
bool Property bLongPressEnabled = true Auto Hidden
bool[] Property abConsoleCommand Auto Hidden
globalvariable Property GPP_COMBO2 Auto
int[] Property aiC4Actions Auto Hidden
int[] Property aiC2Actions Auto Hidden
float Property fLongPressDelay = 0.6 Auto Hidden
float Property fMultiTapDelay = 0.3 Auto Hidden
string[] Property asConsoleCommands Auto Hidden
int Property GPP_KEYCODE_C4 = -1 Auto Hidden
globalvariable Property GPP_COMBO4 Auto
int Property GPP_KEYCODE_A3 = 266 Auto Hidden
int Property GPP_KEYCODE_C2 = -1 Auto Hidden
bool Property bExtControlsEnabled Auto Hidden

; ---------------------------------------------------------------------------------------------
; Lifecycle
; ---------------------------------------------------------------------------------------------

Event OnInit()
    int i
    aiNonComboActions = new int[16]
    aiC1Actions = new int[16]
    aiC2Actions = new int[16]
    aiC3Actions = new int[16]
    aiC4Actions = new int[16]
    while i < 16
        aiNonComboActions[i] = -1
        aiC1Actions[i] = -1
        aiC2Actions[i] = -1
        aiC3Actions[i] = -1
        aiC4Actions[i] = -1
        i = i + 1
    endwhile
    ApplyAuthoriaBindings()
    aiActionKeys = new int[4]
    aiiEquipKeys = new int[5]
    ClearEquipKeys()
    abConsoleCommand = new bool[16]
    asConsoleCommands = new string[16]
    fCurrentVersion = getVersion()
    OnPlayerLoadGame()
EndEvent

Event OnPlayerLoadGame()
    checkVersion()
    GotoState("")
    UnregisterForUpdate()
    RegisterForMenus()
    bIsC1Held = false
    bIsC2Held = false
    bIsC3Held = false
    bIsC4Held = false
    iWaitingKeyCode = -1
    iMultiTap = 0
    bAllowKeyPress = true
    biEquipLoaded = !(game.GetModByName("iEquip.esp") == 255)
    bConsoleUtilLoaded = skse.GetPluginVersion("ConsoleUtilSSE") > 0
    if biEquipLoaded
        RegisterForModEvent("iEquip_KeysUpdated", "OniEquipKeysUpdated")
        SendModEvent("iEquip_KeysUpdated", "", 0.0)
    else
        ClearEquipKeys()
        UnregisterForModEvent("iEquip_KeysUpdated")
    endif
    RegisterKeys()
EndEvent

float Function getVersion()
    return 3.5
EndFunction

; Runs once per version change. Same reset stock GPP performs: combo keys back to default, the
; D-pad map written, multi-tap and long-press forced on. The C1-C4 action arrays are never reset.
Function checkVersion()
    float fThisVersion = getVersion()
    if fThisVersion == fCurrentVersion
        return
    endif
    bExtControlsEnabled = false
    if !abConsoleCommand
        abConsoleCommand = new bool[16]
        asConsoleCommands = new string[16]
    endif
    GPP_KEYCODE_C1 = 276
    GPP_KEYCODE_C2 = -1
    GPP_KEYCODE_C3 = -1
    GPP_KEYCODE_C4 = -1
    ApplyAuthoriaBindings()
    bMultiTapEnabled = true
    bLongPressEnabled = true
    fCurrentVersion = fThisVersion
EndFunction

; Index = actionKey * 4 + tap, tap: 0 = hold, 1 = single, 2 = double, 3 = triple.
; A1 = D-pad Left, A2 = D-pad Right, A3 = D-pad Up, A4 = D-pad Down. Values are DirectInput
; scancodes of the KEYBOARD key the target mod listens on. Singles stay -1: the controlmap already
; binds single D-pad presses to vanilla favorites Hotkey5-8.
Function ApplyAuthoriaBindings()
    aiNonComboActions[0]  = 27 ; Left  hold   -> ]          pitch tent (tent_pitcher)
    aiNonComboActions[1]  = -1 ; Left  single -> vanilla Hotkey6
    aiNonComboActions[2]  = 38 ; Left  double -> L          Lights On
    aiNonComboActions[3]  = 12 ; Left  triple -> -          stamina potion (Optimal Potion Hotkey)
    aiNonComboActions[4]  = 43 ; Right hold   -> \          build campfire (Campfire)
    aiNonComboActions[5]  = -1 ; Right single -> vanilla Hotkey5
    aiNonComboActions[6]  = 35 ; Right double -> H          follower command wheel (Swiftly Order Squad)
    aiNonComboActions[7]  = 13 ; Right triple -> =          magicka potion
    aiNonComboActions[8]  = 70 ; Up    hold   -> ScrollLock Campfire instincts / harvest / create, Frostfall weather sense
    aiNonComboActions[9]  = -1 ; Up    single -> vanilla Hotkey7
    aiNonComboActions[10] = 45 ; Up    double -> x          Stances NG cycle
    aiNonComboActions[11] = 21 ; Up    triple -> Y          helmet toggle (Helmet Toggle 2)
    aiNonComboActions[12] = 48 ; Down  hold   -> B          horse whistle (Horse Whistle Key)
    aiNonComboActions[13] = -1 ; Down  single -> vanilla Hotkey8
    aiNonComboActions[14] = 52 ; Down  double -> .          Stances NG neutral
    aiNonComboActions[15] = 11 ; Down  triple -> 0          health potion
EndFunction

Function ClearEquipKeys()
    int i = 0
    while i < 5
        aiiEquipKeys[i] = -1
        i = i + 1
    endwhile
EndFunction

; ---------------------------------------------------------------------------------------------
; Registration
; ---------------------------------------------------------------------------------------------

Function RegisterKeys()
    UnregisterForAllKeys()
    RegisterForKey(GPP_KEYCODE_A1)
    RegisterForKey(GPP_KEYCODE_A2)
    RegisterForKey(GPP_KEYCODE_A3)
    RegisterForKey(GPP_KEYCODE_A4)
    aiActionKeys[0] = GPP_KEYCODE_A1
    aiActionKeys[1] = GPP_KEYCODE_A2
    aiActionKeys[2] = GPP_KEYCODE_A3
    aiActionKeys[3] = GPP_KEYCODE_A4
    RegisterForKey(GPP_KEYCODE_C1)
    RegisterForKey(GPP_KEYCODE_C2)
    RegisterForKey(GPP_KEYCODE_C3)
    if bFourthComboEnabled
        RegisterForKey(GPP_KEYCODE_C4)
    endif
    GPP_COMBO1.SetValueInt(GPP_KEYCODE_C1)
    GPP_COMBO2.SetValueInt(GPP_KEYCODE_C2)
    GPP_COMBO3.SetValueInt(GPP_KEYCODE_C3)
    GPP_COMBO4.SetValueInt(GPP_KEYCODE_C4)
    SendModEvent("GPP_ComboKeysUpdated", "", 0.0)
EndFunction

; Every menu GPP disables itself in. FavoritesMenu is registered but exempted in OnMenuOpen so
; the D-pad favorites hotkeys keep working inside it.
Function RegisterForMenus()
    RegisterForMenu("BarterMenu")
    RegisterForMenu("Book Menu")
    RegisterForMenu("Console")
    RegisterForMenu("Console Native UI Menu")
    RegisterForMenu("ContainerMenu")
    RegisterForMenu("Crafting Menu")
    RegisterForMenu("CustomMenu")
    RegisterForMenu("Dialogue Menu")
    RegisterForMenu("FavoritesMenu")
    RegisterForMenu("GiftMenu")
    RegisterForMenu("InventoryMenu")
    RegisterForMenu("Journal Menu")
    RegisterForMenu("LevelUp Menu")
    RegisterForMenu("Loading Menu")
    RegisterForMenu("Lockpicking Menu")
    RegisterForMenu("MagicMenu")
    RegisterForMenu("Main Menu")
    RegisterForMenu("MapMenu")
    RegisterForMenu("MessageBoxMenu")
    RegisterForMenu("Quantity Menu")
    RegisterForMenu("RaceSex Menu")
    RegisterForMenu("Sleep/Wait Menu")
    RegisterForMenu("StatsMenu")
    RegisterForMenu("Training Menu")
    RegisterForMenu("Tutorial Menu")
    RegisterForMenu("TweenMenu")
EndFunction

Event OniEquipKeysUpdated(string sEventName, string sStringArg, float fNumArg, Form kSender)
    int i
    int hexBase = 1129375
    if !game.GetFormFromFile(hexBase, "iEquip.esp")
        hexBase = 2122
    endif
    while i < 5
        int tmpKey = (game.GetFormFromFile(hexBase + i, "iEquip.esp") as globalvariable).GetValueInt()
        if !(tmpKey == -1)
            aiiEquipKeys[i] = tmpKey
        endif
        i = i + 1
    endwhile
EndEvent

; ---------------------------------------------------------------------------------------------
; Menu guards
; ---------------------------------------------------------------------------------------------

Event OnMenuOpen(string MenuName)
    if !(MenuName == "FavoritesMenu")
        GotoState("DISABLED")
    endif
EndEvent

Event OnMenuClose(string MenuName)
    if !utility.IsInMenuMode()
        GotoState("")
    endif
EndEvent

; QuickLoot IE registers "LootMenu" and opens a fresh instance per window, so IsMenuOpen tracks it
; exactly. The second line is the stock check for the old QuickLoot RE window, kept as a fallback.
bool Function isLootWindowOpen()
    if ui.IsMenuOpen("LootMenu")
        return true
    endif
    return ui.IsMenuOpen("Loot Menu") && ui.GetBool("Loot Menu", "_root.Menu_mc._visible")
EndFunction

; ---------------------------------------------------------------------------------------------
; Gesture resolution
; ---------------------------------------------------------------------------------------------

; Fires after the gesture window closes. iMultiTap: 0 = hold, 1 = single, 2 = double, 3 = triple.
; D-pad Up/Down (266/267) scroll the loot list, so their gestures are inert over the loot window.
Event OnUpdate()
    int keyToTap
    int i = aiActionKeys.Find(iWaitingKeyCode)
    bAllowKeyPress = false
    bool bGestureEnabled = iMultiTap == 1 || (iMultiTap == 0 && bLongPressEnabled) || (iMultiTap > 1 && bMultiTapEnabled)
    if bGestureEnabled && i != -1 && !((iWaitingKeyCode == 266 || iWaitingKeyCode == 267) && isLootWindowOpen())
        if bConsoleUtilLoaded && bIsC2Held && i == 0 && abConsoleCommand[0]
            consoleutil.ExecuteCommand(asConsoleCommands[0])
        elseif bIsC1Held
            keyToTap = aiC1Actions[i * 4 + iMultiTap]
        elseif bIsC2Held
            keyToTap = aiC2Actions[i * 4 + iMultiTap]
        elseif bIsC3Held
            keyToTap = aiC3Actions[i * 4 + iMultiTap]
        elseif bIsC4Held
            keyToTap = aiC4Actions[i * 4 + iMultiTap]
        elseif !biEquipLoaded || aiiEquipKeys.Find(iWaitingKeyCode) == -1
            keyToTap = aiNonComboActions[i * 4 + iMultiTap]
        endif
        if keyToTap > 0
            input.HoldKey(keyToTap)
            utility.WaitMenuMode(0.1)
            input.ReleaseKey(keyToTap)
        endif
    endif
    iMultiTap = 0
    iWaitingKeyCode = -1
    bAllowKeyPress = true
EndEvent

Event OnKeyDown(int KeyCode)
    bool bIsComboKey
    if KeyCode == GPP_KEYCODE_C1
        bIsC1Held = true
        bIsComboKey = true
    elseif KeyCode == GPP_KEYCODE_C2
        bIsC2Held = true
        bIsComboKey = true
    elseif KeyCode == GPP_KEYCODE_C3
        bIsC3Held = true
        bIsComboKey = true
    elseif KeyCode == GPP_KEYCODE_C4
        bIsC4Held = true
        bIsComboKey = true
    endif
    if bAllowKeyPress
        if !(KeyCode == iWaitingKeyCode) && !(iWaitingKeyCode == -1)
            if !bIsComboKey
                UnregisterForUpdate()
                OnUpdate()
            else
                iMultiTap = 0
            endif
        endif
        iWaitingKeyCode = KeyCode
        if iMultiTap == 0
            RegisterForSingleUpdate(fLongPressDelay)
        elseif bMultiTapEnabled
            if iMultiTap == 1
                iMultiTap = 2
                RegisterForSingleUpdate(fMultiTapDelay)
            elseif iMultiTap == 2
                iMultiTap = 3
                RegisterForSingleUpdate(0.0)
            endif
        endif
    endif
EndEvent

Event OnKeyUp(int KeyCode, float HoldTime)
    if bAllowKeyPress && KeyCode == iWaitingKeyCode && iMultiTap == 0
        iMultiTap = 1
        if bMultiTapEnabled
            RegisterForSingleUpdate(fMultiTapDelay)
            utility.WaitMenuMode(fMultiTapDelay + 0.1)
        else
            RegisterForSingleUpdate(0.0)
        endif
    endif
    if KeyCode == GPP_KEYCODE_C1
        bIsC1Held = false
    elseif KeyCode == GPP_KEYCODE_C2
        bIsC2Held = false
    elseif KeyCode == GPP_KEYCODE_C3
        bIsC3Held = false
    elseif KeyCode == GPP_KEYCODE_C4
        bIsC4Held = false
    endif
EndEvent

State DISABLED
    Event onBeginState()
        UnregisterForUpdate()
        bAllowKeyPress = false
        iWaitingKeyCode = -1
        iMultiTap = 0
    EndEvent

    Event onEndState()
        bIsC1Held = false
        bIsC2Held = false
        bIsC3Held = false
        bIsC4Held = false
        bAllowKeyPress = true
    EndEvent
EndState
