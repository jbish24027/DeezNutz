Scriptname Traits_QuestScript extends Quest

Import b612
Import PO3_SKSEFunctions
Import StringUtil
Import MCM

; Properties
FormList Property Traits_AbilityList Auto
Spell Property Traits_AuNaturelAb Auto
Message Property Traits_NoneSelectionMsg Auto

Function ShowTraitsMenu(Int iMin = -1, Int iMax = -1)
    GetSpinicon().Show("$BIGTRAIT_LOADING")
    ; display and populate the menu
    b612_TraitsMenu TraitsMenu = GetTraitsMenu()
    Int i = 0
    Int size = Traits_AbilityList.GetSize()
    If iMin == -1
        iMin = GetModSettingInt("Biggie Traits", "iRequiredTraits:Main")
    EndIf
    If iMax == -1
        iMax = GetModSettingInt("Biggie Traits", "iMaxTraits:Main")
    EndIf
    If iMin > iMax
        iMin = iMax
    EndIf
    While i < size
        Spell thisSpell = Traits_AbilityList.GetAt(i) as Spell
        TraitsMenu.AddItem(thisSpell.GetName(), FormatDescription(GetDescription(thisSpell)), "TraitPics/" + GetFormEditorID(thisSpell) + ".dds")
        i += 1
    EndWhile
    GetSpinicon().Hide()
    String[] result = TraitsMenu.Show(aiMaxSelection = iMax, aiMinSelection = iMin)

    If ! result || result.Length == 0
        If Traits_NoneSelectionMsg.Show() == 0
            ShowTraitsMenu()
            Return
        EndIf
    Else
        i = 0
        While i < result.Length
            Int selectedIndex = result[i] as Int
            Spell selectedSpell = Traits_AbilityList.GetAt(selectedIndex) as Spell

            If selectedSpell == Traits_AuNaturelAb
                ; prevent death from Au Naturel trait
                Game.GetPlayer().UnequipAll()
            EndIf

            Game.GetPlayer().AddSpell(selectedSpell)
            i += 1
        EndWhile
    EndIf
    SendModEvent("_Authoria_Init_TraitsDone")
EndFunction

; add support for CK's way of <bolding text>
; both GetNthChar and Substring mess up string's text casing
String Function FormatDescription(String desc)
    String sResult
    String[] parts1 = StringUtil.Split(desc, "<")
    Int i
    While i < parts1.Length
        If i != 0
            sResult += "<b>"
        EndIf
        String[] parts2 = StringUtil.Split(parts1[i], ">")
        String part = ""
        Int j = 0

        While j < parts2.Length
            If j != 0
                sResult += "</b>"
            EndIf
            sResult += parts2[j]
            j += 1
        EndWhile
        i += 1
    EndWhile

    Return sResult
EndFunction
