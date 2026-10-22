;/ Decompiled by Champollion V1.0.1
Source   : _HolidaySkyUIConfig.psc
Modified : 2015-04-10 14:07:56
Compiled : 2015-04-10 14:07:59
User     : Leng Sok
Computer : LENGSOK-LAPTOP
/;
scriptName selectyourseasonskyuiconfig extends SKI_ConfigBase

;-- Properties --------------------------------------
selectyourseasonquestscript property SYSQuest auto

;-- Variables ---------------------------------------
String[] StartDateList
Int CurrentMonthOption
Int StartDateOption
Int CurrentDayOption
Int StartDate
String[] Pages
String[] Month
Float MaxDayCurrentMonth = 28.0000

;-- Functions ---------------------------------------

function ApplySettings()
	if StartDate == 1
		SYSQuest.GameMonth.SetValue(SYSQuest.CurrentMonth as Float)
		SYSQuest.GameDay.SetValue(SYSQuest.CurrentDay as Float)
		StartDate = -1
	elseIf StartDate == 2
		SYSQuest.RandomDateandTime()
		StartDate = 0
	endIf
	SYSQuest.CheckDate()
	; Authoria: tell Holidays the date changed, so its decorations follow the new date right away
	Quest holidayQuest = Game.GetFormFromFile(0x0000F059, "Holidays.esp") as Quest
	if holidayQuest
		_HolidayQuestScript holidayScript = holidayQuest as _HolidayQuestScript
		if holidayScript
			holidayScript.CheckDate()
		endIf
	endIf
endFunction

function OnOptionSliderAccept(Int Option, Float value)
	if Option == CurrentDayOption
		SYSQuest.CurrentDay = value as Int
		self.SetSliderOptionValue(CurrentDayOption, SYSQuest.CurrentDay as Float, "{0}", false)
	endIf
	self.ForcePageReset()
endFunction

function OnOptionMenuAccept(Int Option, Int Index)

	if Option == StartDateOption
		StartDate = Index
		self.SetMenuOptionValue(StartDateOption, StartDateList[StartDate], false)
	elseIf Option == CurrentMonthOption
		SYSQuest.CurrentMonth = Index
		self.SetMenuOptionValue(CurrentMonthOption, Month[SYSQuest.CurrentMonth], false)
		SYSQuest.CurrentDay = 17
	endIf
	self.ForcePageReset()
endFunction

function OnOptionSliderOpen(Int Option)
	if Option == CurrentDayOption
		self.SetSliderDialogStartValue(SYSQuest.CurrentDay as Float)
		self.SetSliderDialogDefaultValue(SYSQuest.CurrentDay as Float)
		self.SetSliderDialogRange(1.00000, MaxDayCurrentMonth)
		self.SetSliderDialogInterval(1.00000)
	endIf
endFunction

; Skipped compiler generated GotoState

function OnConfigClose()
	self.ApplySettings()
endFunction

; Skipped compiler generated GetState

function OnConfigInit()
	ModName = "$Select Your Season"
	Pages = new String[1]
	Pages[0] = "$General"
	Month = new String[12]
	Month[0] = "$Morning Star (Jan)"
	Month[1] = "$Sun's Dawn (Feb)"
	Month[2] = "$First Seed (Mar)"
	Month[3] = "$Rain's Hand (Apr)"
	Month[4] = "$Second Seed (May)"
	Month[5] = "$Mid Year (Jun)"
	Month[6] = "$Sun's Height (Jul)"
	Month[7] = "$Last Seed (Aug)"
	Month[8] = "$Heartfire (Sep)"
	Month[9] = "$Frostfall (Oct)"
	Month[10] = "$Sun's Dusk (Nov)"
	Month[11] = "$Evening Star (Dec)"
	StartDateList = new String[3]
	StartDateList[0] = "$Default Start Date"
	StartDateList[1] = "$Manual Start Date"
	StartDateList[2] = "$Random Start Date"
	SYSQuest.CheckDate()
endFunction

function OnOptionMenuOpen(Int Option)
	if Option == StartDateOption
		self.SetMenuDialogOptions(StartDateList)
		self.SetMenuDialogStartIndex(StartDate)
		self.SetMenuDialogDefaultIndex(0)
	elseIf Option == CurrentMonthOption
		self.SetMenuDialogOptions(Month)
		self.SetMenuDialogStartIndex(SYSQuest.CurrentMonth)
		self.SetMenuDialogDefaultIndex(SYSQuest.CurrentMonth)
	endIf
endFunction

function OnPageReset(String Page)
	MaxDayCurrentMonth = SYSQuest.MaxDay(SYSQuest.CurrentMonth)
	if Page == "$General"
		self.SetCursorFillMode(self.TOP_TO_BOTTOM)
		if StartDate > -1 && utility.GetCurrentGameTime() < 1
			StartDateOption = self.AddMenuOption("", StartDateList[StartDate], 0)
		else
			self.AddEmptyOption()
		endIf
		self.SetCursorPosition(1)
		if StartDate != 1
			self.AddTextOption("$Current Date", Month[SYSQuest.CurrentMonth], self.OPTION_FLAG_DISABLED)
			self.AddTextOption("", SYSQuest.CurrentDay as String, self.OPTION_FLAG_DISABLED)
		else
			CurrentMonthOption = self.AddMenuOption("$Current Date", Month[SYSQuest.CurrentMonth], 0)
			CurrentDayOption = self.AddSliderOption("", SYSQuest.CurrentDay as Float, "{0}", 0)
		endIf
	endIf
endFunction
