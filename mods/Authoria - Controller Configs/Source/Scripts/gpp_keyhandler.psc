ScriptName gpp_keyhandler extends ReferenceAlias

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

Event OnInit()
    int i
    aiNonComboActions = new int[16]
    aiC1Actions = new int[16]
    aiC2Actions = new int[16]
    aiC3Actions = new int[16]
    aiC4Actions = new int[16]
    while i < 16
        aiNonComboActions[i] = -1
        aiNonComboActions[2] = 38
        aiNonComboActions[6] = 35
        aiNonComboActions[10] = 26 ; ARR: D-pad Up dbl-tap -> [ (Stances NG cycle)
        aiNonComboActions[14] = 52 ; ARR: D-pad Down dbl-tap -> . (Stances NG neutral)
        aiC1Actions[i] = -1
        aiC2Actions[i] = -1
        aiC3Actions[i] = -1
        aiC4Actions[i] = -1
        i = i + 1
    endwhile
    aiActionKeys = new int[4]
    aiiEquipKeys = new int[5]
    i = 0
    while i < 5
        aiiEquipKeys[i] = -1
        i = i + 1
    endwhile
    abConsoleCommand = new bool[16]
    asConsoleCommands = new string[16]
    OnPlayerLoadGame()
EndEvent

Function checkVersion()
    float fThisVersion = getVersion()
    if fThisVersion == fCurrentVersion
    else
        if fCurrentVersion < 1.1 && bExtControlsEnabled
            bExtControlsEnabled = false
            bMultiTapEnabled = true
            bLongPressEnabled = true
        endif
        if fCurrentVersion < 1.2
            abConsoleCommand = new bool[16]
            asConsoleCommands = new string[16]
        endif
        if !(fThisVersion == fCurrentVersion)
            GPP_KEYCODE_C1 = 276
            GPP_KEYCODE_C2 = -1
            GPP_KEYCODE_C3 = -1
            GPP_KEYCODE_C4 = -1
            aiNonComboActions[0] = -1
            aiNonComboActions[4] = -1
            aiNonComboActions[8] = -1
            aiNonComboActions[12] = -1
            aiNonComboActions[2] = 38
            aiNonComboActions[6] = 35
            aiNonComboActions[10] = 26 ; ARR: D-pad Up dbl-tap -> [ (Stances NG cycle)
            aiNonComboActions[14] = 52 ; ARR: D-pad Down dbl-tap -> . (Stances NG neutral)
            bMultiTapEnabled = true
            bLongPressEnabled = true
        endif
        fCurrentVersion = fThisVersion
    endif
EndFunction

float Function getVersion()
    return 2.7
EndFunction

Event OnPlayerLoadGame()
    int i
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
        while i < 5
            aiiEquipKeys[i] = -1
            i = i + 1
        endwhile
        UnregisterForModEvent("iEquip_KeysUpdated")
    endif
    RegisterKeys()
EndEvent

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

Event OnMenuOpen(string MenuName)
    if !MenuName == "FavoritesMenu"
        GotoState("DISABLED")
    endif
EndEvent

Event OnMenuClose(string MenuName)
    if !utility.IsInMenuMode()
        GotoState("")
    endif
EndEvent

Event OnUpdate()
    int keyToTap
    int i = aiActionKeys.Find(iWaitingKeyCode)
    bAllowKeyPress = false
    if (iMultiTap == 1 || iMultiTap == 0 && bLongPressEnabled || iMultiTap > 1 && bMultiTapEnabled) && !((iWaitingKeyCode == 266 || iWaitingKeyCode == 267) && ui.IsMenuOpen("Loot Menu") && ui.GetBool("Loot Menu", "_root.Menu_mc._visible") == true)
        if !(i == -1)
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

