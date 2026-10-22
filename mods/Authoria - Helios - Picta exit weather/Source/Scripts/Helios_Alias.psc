Scriptname Helios_Alias extends ReferenceAlias
import Weather
import Debug
import Utility
import CLUtil

; Authoria Picta-lane edit (2026-10-13, summer variants 2026-10-15): on leaving a Helios interior, a generic Tamriel / Forgotten Vale twin
; (Helios_Skyrim*, Helios_DLC1_Skyrim*) is pushed outdoors as the matching Picta MASTER weather instead of the
; vanilla weather of the stripped name, which Picta does not route (it rendered too bright). Unique weathers and
; lanes without Picta keep Helios's original lookup. Everything else is the shipped script unchanged.

;----------------------------------------- Variables ---------------------------------------------------
Actor Property PlayerRef Auto
Bool Property Helios_Weather = false Auto
Bool Property Helios_ToggleDebug = false Auto

;------------------------------------------ Events -----------------------------------------------------
Event OnInit()
    Utility.Wait(0.1)
    RegisterForCellloadRef(self)
    UpdateWeatherState()
EndEvent

Event OnPlayerLoadGame()
    Utility.Wait(0.1)
    UpdateWeatherState()
EndEvent

Event OnUpdateGameTime()
    Weather.ReleaseOverride()
    If Helios_ToggleDebug
        Debug.Notification("Helios: Released weather override")
    EndIf
EndEvent

Event OnCellChange(Cell cl)
    If PlayerRef.IsInInterior()
	    String region = GetRegion(cl)

		If StringUtil.Find(region, "Helios_") == 0
			Helios_Weather = true
				If Helios_ToggleDebug
					Debug.Notification("Helios_Interior : " + Helios_Weather)
					Debug.Notification("Helios: Weather Region: " + region)
				EndIf
			ChangeWeather()
		Else
			If Helios_Weather
				Helios_Weather = false
					If Helios_ToggleDebug
						Debug.Notification("Helios_Interior : " + Helios_Weather)
						Debug.Notification("Helios: Weather Region: " + region)
					EndIf
				ChangeWeather()
			EndIf
        EndIf
    Else
        If Helios_Weather
			Helios_Weather = false
				If Helios_ToggleDebug
					String region = GetRegion(cl)
					Debug.Notification("Helios_Interior : " + Helios_Weather)
					Debug.Notification("Helios: Weather Region: " + region)
				EndIf
			ChangeWeather()
		EndIf
    EndIf
EndEvent

;----------------------------------------- Functions ---------------------------------------------------

Function UpdateWeatherState()
		If PlayerRef.IsInInterior()
			Cell currentCell = PlayerRef.GetParentCell()
			String region = GetRegion(currentCell)

			If StringUtil.Find(region, "Helios_") == 0
				Helios_Weather = true
				ChangeWeather()
			Else
				If Helios_Weather
					Helios_Weather = false
				EndIf
			EndIf
		Else
			If Helios_Weather
				Helios_Weather = false
			EndIf
		EndIf
EndFunction

; Picta MASTER weather that matches a generic vanilla weather name, or "" when there is no generic match.
String Function PictaEquivalent(String n)
    If StringUtil.Find(n, "Skyrim") != 0 && StringUtil.Find(n, "DLC1_Skyrim") != 0
        Return ""
    EndIf
    If StringUtil.Find(n, "War") >= 0
        Return ""
    EndIf
    Int len = StringUtil.GetLength(n)
    Bool aurora = len > 2 && StringUtil.Substring(n, len - 2, 2) == "_A"
    If StringUtil.Find(n, "Snow") >= 0
        If StringUtil.Find(n, "Storm") >= 0
            Return "PIC_WTHR_MASTER_E05_Storm_Snow_Heavy"
        EndIf
        Return "PIC_WTHR_MASTER_D05_Overcast_Snow_Light"
    ElseIf StringUtil.Find(n, "Storm") >= 0
        Return "PIC_WTHR_MASTER_E03_Storm_Rain_Heavy_Thunder"
    ElseIf StringUtil.Find(n, "Rain") >= 0
        Return "PIC_WTHR_MASTER_D03_Overcast_Rain_Light"
    ElseIf StringUtil.Find(n, "Fog") >= 0
        Return "PIC_WTHR_MASTER_D02_Overcast_Heavy_Fog"
    ElseIf StringUtil.Find(n, "Cloudy") >= 0
        If aurora
            Return "PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora"
        EndIf
        Return "PIC_WTHR_MASTER_C01_Cloudy"
    ElseIf StringUtil.Find(n, "Clear") >= 0
        If aurora
            Return "PIC_WTHR_MASTER_A02_Clear_Aurora"
        EndIf
        Return "PIC_WTHR_MASTER_A01_Clear"
    ElseIf StringUtil.Find(n, "Overcast") >= 0
        Return "PIC_WTHR_MASTER_D01_Overcast"
    EndIf
    Return ""
EndFunction

; Authoria 2026-10-15: in summer (GameMonth 5..7, the months the Seasonal Weathers Framework scores as summer) the sunny
; MASTER weathers have warm SUMMER variants (PIC_WTHR_SUMMER_*, injected into the Picta esm by Authoria - Patch - Picta
; Seasonal.esp). Return the variant's editor id when it exists, else the master id unchanged.
String Function SummerVariant(String pictaID)
    GlobalVariable gameMonth = Game.GetForm(0x36) as GlobalVariable
    If gameMonth == None
        Return pictaID
    EndIf
    Int m = gameMonth.GetValue() as Int
    If m < 5 || m > 7
        Return pictaID
    EndIf
    String summerID = ""
    If pictaID == "PIC_WTHR_MASTER_A01_Clear"
        summerID = "PIC_WTHR_SUMMER_A01_Clear"
    ElseIf pictaID == "PIC_WTHR_MASTER_A02_Clear_Aurora"
        summerID = "PIC_WTHR_SUMMER_A02_Clear_Aurora"
    ElseIf pictaID == "PIC_WTHR_MASTER_A03_Clear_Mist"
        summerID = "PIC_WTHR_SUMMER_A03_Clear_Mist"
    ElseIf pictaID == "PIC_WTHR_MASTER_B01_Lightly_Cloudy"
        summerID = "PIC_WTHR_SUMMER_B01_Lightly_Cloudy"
    ElseIf pictaID == "PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora"
        summerID = "PIC_WTHR_SUMMER_B02_Lightly_Cloudy_Aurora"
    EndIf
    If summerID != "" && (MMSF.GetByEditorID(summerID) as Weather)
        Return summerID
    EndIf
    Return pictaID
EndFunction

Function ChangeWeather()
    Utility.Wait(0.1)
    Weather.ReleaseOverride()

    Weather outgoing = Weather.GetOutgoingWeather()

    If outgoing == None
        outgoing = Weather.GetCurrentWeather()
        If Helios_ToggleDebug
            Debug.Notification("Helios: No Outgoing Weather")
        EndIf
			If outgoing == None
				If Helios_ToggleDebug
					Debug.Notification("Helios: No Current Weather")
				EndIf
				Return
			EndIf
    EndIf

    String outgoingEDID = MMSF.GetEditorID(outgoing)

    If Helios_ToggleDebug
        Debug.Notification("Helios: Outgoing: " + outgoingEDID)
    EndIf

    String targetEditorID = outgoingEDID

    If Helios_Weather
        If StringUtil.Find(outgoingEDID, "Helios_") != 0
            targetEditorID = "Helios_" + outgoingEDID
        EndIf
    Else
        If StringUtil.Find(outgoingEDID, "Helios_") == 0
            targetEditorID = StringUtil.Substring(outgoingEDID, 7, -1)
            String pictaID = PictaEquivalent(targetEditorID)
            If pictaID != ""
                If MMSF.GetByEditorID(pictaID) as Weather
                    targetEditorID = SummerVariant(pictaID)
                EndIf
            EndIf
        EndIf
    EndIf

    If Helios_ToggleDebug
        Debug.Notification("Helios: Target: " + targetEditorID)
    EndIf

    Weather targetWeather = MMSF.GetByEditorID(targetEditorID) as Weather

    If targetWeather
        If Helios_Weather
            EmittanceUtil.SetWeatherInstant(targetWeather, true)
            RegisterForSingleUpdateGameTime(3.0)
		Else
            EmittanceUtil.SetWeatherInstant(targetWeather, false)
        EndIf

        If Helios_ToggleDebug
            String currEditorID = MMSF.GetEditorID(Weather.GetCurrentWeather())
            Debug.Notification("Helios: Current: " + currEditorID)
        EndIf
    Else
        If Helios_ToggleDebug
            Debug.Notification("Helios: Target not found")
        EndIf
        ForceCurrentWeather()
    EndIf
EndFunction

Function ForceCurrentWeather()
    Weather currentWeather = Weather.GetCurrentWeather()
            EmittanceUtil.SetWeatherInstant(currentWeather, false)
EndFunction
