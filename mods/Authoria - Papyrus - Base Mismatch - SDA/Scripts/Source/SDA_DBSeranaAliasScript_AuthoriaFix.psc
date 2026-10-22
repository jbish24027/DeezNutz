ScriptName SDA_DBSeranaAliasScript_AuthoriaFix Extends ReferenceAlias

Location Property AbandonedShackLocation Auto
Quest Property DB01 Auto
Quest Property DB02 Auto
Quest Property DB03 Auto
Quest Property DB04 Auto
Quest Property DB04a Auto
Quest Property DB05 Auto
Quest Property DB06 Auto
Quest Property DB07 Auto
Quest Property DB08 Auto
Quest Property DB09 Auto
Quest Property DB10 Auto
Quest Property DB11 Auto
Quest Property DBDestroy Auto
Quest Property DarkBrotherhood02a Auto
Location Property DarkBrotherhoodSanctuaryLocation Auto
Location Property DawnstarSanctuaryLocation Auto
Location Property DragonBridgeLocation Auto
Location Property KatariahLocation Auto
Location Property MarkarthLocation Auto
Bool Property OnUpdateRegistered Auto
Location Property RaldbtharLocation Auto
Location Property RiftenHonorhallOrphanageLocation Auto
Location Property RiftenRaggedFlagonLocation Auto
Scene Property SDA_DB01MeetingAventus Auto
Scene Property SDA_DB02EnteringHonorfall Auto
Scene Property SDA_DB03KillGrelod Auto
Scene Property SDA_DB04ExitAventusHouse Auto
Scene Property SDA_DB05ShackExit Auto
Scene Property SDA_DB06DestroyDB Auto
Scene Property SDA_DB07DestroyDB2 Auto
Scene Property SDA_DB08DestroyDB3 Auto
Scene Property SDA_DB09JoinDB Auto
Scene Property SDA_DB10MuiriQuestStart Auto
Scene Property SDA_DB11MuiriQuestPt2 Auto
Scene Property SDA_DB12EnterDungeon Auto
Scene Property SDA_DB13KillAlain Auto
Scene Property SDA_DB14QuestComplete Auto
Scene Property SDA_DB15WhisperStart Auto
Scene Property SDA_DB16VolunruudStart Auto
Scene Property SDA_DB17VolunruudEnter Auto
Scene Property SDA_DB18KillEmperor Auto
Scene Property SDA_DB19RiftenStart Auto
Scene Property SDA_DB20Amulet Auto
Scene Property SDA_DB21Wedding Auto
Scene Property SDA_DB22EnteringSolitude Auto
Scene Property SDA_DB23Escaped Auto
Scene Property SDA_DB24GaiusStart Auto
Scene Property SDA_DB25KillGaius Auto
Scene Property SDA_DB26FindCicero Auto
Scene Property SDA_DB27DawnstarSanctuary Auto
Scene Property SDA_DB28KillCicero Auto
Scene Property SDA_DB29Gourmet Auto
Scene Property SDA_DB30KillGourmet Auto
Scene Property SDA_DB31KillEmperor01 Auto
Scene Property SDA_DB32EnterSolitude Auto
Scene Property SDA_DB33Escape Auto
Scene Property SDA_DB34ArriveSanctuary Auto
Scene Property SDA_DB35Aftermath Auto
Scene Property SDA_DB36Start Auto
Scene Property SDA_DB37End Auto
ReferenceAlias Property SeranaAlias Auto
sda_teleportmainscript Property SilentTP Auto
Location Property SolitudeCastleDourEmperorsTowerLocation Auto
Location Property SolitudeCastleDourLocation Auto
Location Property SolitudeLocation Auto
Location Property VolunruudLocation Auto
Location Property WindhelmLocation Auto
pdbentrancequestscript Property DBEntrance Auto
DLC1_NPCMentalModelScript Property MM Auto
Faction Property PlayerBedOwnership Auto
ObjectReference Property SDA_ShackMarker Auto
Quest Property SDA_SleepingQuest Auto
Scene Property SDA_SleepingQuestScene Auto
Spell Property SDA_UndressSpell Auto

Event OnUpdate()
EndEvent

Event OnLocationChange(Location akOldLoc, Location akNewLoc)
	Actor Serana = SeranaAlias.GetActorReference()
	If Serana && Serana.IsPlayerTeammate()
		If DB01.GetStage() == 20 && Self.GetOwningQuest().GetStage() == 0
			SilentTP.SDA_SilentTeleport()
			Utility.Wait(4.0)
			SDA_DB01MeetingAventus.Start()
			Self.GetOwningQuest().SetStage(10)
		ElseIf DB01.GetStage() == 20 && Self.GetOwningQuest().GetStage() <= 10 && akNewLoc == RiftenHonorhallOrphanageLocation
			SilentTP.SDA_SilentTeleport()
			Utility.Wait(4.0)
			SDA_DB02EnteringHonorfall.Start()
			Self.GetOwningQuest().SetStage(20)
		ElseIf DB01.IsCompleted() && Self.GetOwningQuest().GetStage() <= 30
			SilentTP.SDA_SilentTeleport()
			Utility.Wait(3.0)
			SDA_DB04ExitAventusHouse.Start()
			Self.GetOwningQuest().SetStage(40)
			SleepRegister()
		EndIf
	EndIf
EndEvent

Event OnCellLoad()
	Debug.Trace("Cell loaded, checking OnUpdate status", 0)
	If OnUpdateRegistered == True
		Self.StopChain()
	EndIf
EndEvent

Function StartChain()
	Self.RegisterForSingleUpdate(5.0)
	OnUpdateRegistered = True
EndFunction

Function StopChain()
	Self.UnregisterforUpdate()
	OnUpdateRegistered = False
EndFunction

Function SleepRegister()
	Self.RegisterForSleep()
	Debug.Trace("Registered for SDA DB sleep!", 0)
EndFunction

Event OnSleepStart(Float afSleepStartTime, Float afDesiredSleepEndTime)
	Actor Serana = SeranaAlias.GetActorReference()
	If Serana && DBEntrance && DBEntrance.pSleepyTime == 1
		Debug.Trace("Stopping SDA sleep stuff if it is playing and moving Serana to shack marker", 0)
		SDA_SleepingQuestScene.Stop()
		Utility.Wait(0.2)
		SDA_SleepingQuest.Reset()
		Utility.Wait(1.0)
		Serana.SetFactionRank(PlayerBedOwnership, -2)
		Serana.DispelSpell(SDA_UndressSpell)
		Serana.MoveTo(SDA_ShackMarker, 0.0, 0.0, 0.0, True)
		MM.Wait()
	EndIf
EndEvent