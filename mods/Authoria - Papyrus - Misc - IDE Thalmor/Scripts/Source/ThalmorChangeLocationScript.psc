Scriptname ThalmorChangeLocationScript extends ReferenceAlias  

Event OnLocationChange(Location akOldLoc, Location akNewLoc)
	Actor SelfRef = Self.GetActorRef()
	Actor LorcalinRef = Lorcalin.GetActorRef()
	Actor RulindilRef = Rulindil.GetActorRef()
	Actor JdatharrRef = Jdatharr.GetActorRef()
	Actor EstormoRef = Estormo.GetActorRef()
	Actor ElenwenRef = Elenwen.GetActorRef()
	Actor ValmirRef = Valmir.GetActorRef()
	Actor GissurRef = Gissur.GetActorRef()
	Actor ShavariRef = Shavari.GetActorRef()

	if SolitudeFreeform07.GetStage() >= 10 && SolitudeFreeform07.GetStage() <= 20 && LorcalinRef
		LorcalinRef.AddToFaction(WEPlayerEnemy)
		LorcalinRef.MoveTo(LorcalinMarker)
		LorcalinRef.EvaluatePackage()
		LorcalinRef.SetAV("Aggression", 2)
	elseif SolitudeFreeform07.GetStage() > 20 && LorcalinRef && LorcalinRef.IsInFaction(WEPlayerEnemy)
		LorcalinRef.RemoveFromFaction(WEPlayerEnemy)
		LorcalinRef.SetAV("Aggression", 0)
	endif

	if MQ201.GetStage() >= 10 && MQ201.GetStage() <= 180 && RulindilRef
		RulindilRef.MoveTo(RulindilMarker)
		RulindilRef.EvaluatePackage()
	elseif MQ201.GetStage() > 180 && RulindilRef && RulindilRef.IsInFaction(MQ201ThalmorCombatFaction)
		RulindilRef.RemoveFromFaction(MQ201ThalmorCombatFaction)
	endif

	if MQ201Malborn.GetStage() >= 10 && JdatharrRef
		JdatharrRef.Disable()
	endif

	if MG06.GetStage() >= 40 && MG07.GetStage() < 50 && EstormoRef
		EstormoRef.Disable()
		EstormoRef.GetActorBase().SetEssential(0)
	endif

	if akNewLoc == SolitudeCastleDourLocation
		if CWSiegeObj.IsRunning() == 0 && Tullius && Tullius.IsDead() == 0 && Tullius.IsInLocation(SolitudeCastleDourLocation) && ElenwenRef && ElenwenRef.IsDead() == 0 && MQ201.IsRunning() == 0 && Tullius.GetCurrentScene() == None
			int Random = Utility.RandomInt(0, 10)
			if Random < 5
				if aaThalmorElenwenTulliusBanterGlobal.Value == 0
					ElenwenRef.MoveTo(CastleDour)
					aaThalmorElenwenTulliusScene1.Start()
				elseif aaThalmorElenwenTulliusBanterGlobal.Value <= 2
					Random = Utility.RandomInt(0, 5)
					if Random == 2 && aaThalmorElenwenTulliusBanter2.Value == 0
						ElenwenRef.MoveTo(CastleDour)
						aaThalmorElenwenTulliusScene2.Start()
					elseif Random == 3 && aaThalmorElenwenTulliusBanter3.Value == 0
						ElenwenRef.MoveTo(CastleDour)
						aaThalmorElenwenTulliusScene3.Start()
					endif
				endif
			endif
		endif
	elseif akOldLoc == SolitudeCastleDourLocation
		if ElenwenRef && ElenwenRef.IsInLocation(SolitudeCastleDourLocation)
			ElenwenRef.MoveTo(ElenwenMarker)
		endif
	elseif SelfRef && SelfRef.GetParentCell() == SolitudeJusticiarHeadquarters
		if CWSiegeObj.IsRunning() == 0 && ElenwenRef && ElenwenRef.IsDead() == 0 && MQ201.IsRunning() == 0
			int Random1 = Utility.RandomInt(0, 10)
			int Threshold
			if MQ201.IsCompleted() == 0 && (MG08.IsCompleted() || MG01.IsCompleted() == 0)
				Threshold = 3
			else
				Threshold = 6
			endif
			if Random1 < Threshold
				ElenwenRef.MoveTo(ThalmorHQ)
				ElenwenRef.AddToFaction(aaThalmorElenwenTulliusFaction)
			endif
		endif
	endif

	if akOldLoc == ForelhostLocation
		if ValmirRef && ValmirRef.IsDead() == 0 && dunForelhost.GetStageDone(130) == 1
			ValmirRef.SetOutfit(ThalmorOutfit)
			ValmirRef.MoveTo(ThalmorHQ)
			ValmirRef.AddToFaction(ThalmorFaction)
		elseif ValmirRef && ValmirRef.IsDead() == 0 && dunForelhost.GetStageDone(120) == 1
			ValmirRef.MoveTo(MG07GhostEnableParent)
			ValmirRef.Kill()
		endif
	endif

	if MQ201.GetStage() >= 100 && GissurRef && GissurRef.GetActorBase().IsEssential()
		GissurRef.GetActorBase().SetEssential(False)
	endif

	if MQ202.GetStage() >= 10 && ShavariRef && ShavariRef.GetActorBase().IsEssential()
		ShavariRef.GetActorBase().SetEssential(False)
	endif

EndEvent

Quest Property SolitudeFreeform07  Auto  

ReferenceAlias Property Lorcalin  Auto  

ObjectReference Property LorcalinMarker  Auto  

Faction Property WEPlayerEnemy  Auto  

ReferenceAlias Property Rulindil  Auto  

ObjectReference Property RulindilMarker  Auto  

Quest Property MQ201  Auto  

Faction Property MQ201ThalmorCombatFaction  Auto  

ReferenceAlias Property Jdatharr  Auto  

Quest Property MQ201Malborn  Auto  

ReferenceAlias Property Estormo  Auto  

Quest Property mg06  Auto  

Quest Property MG07  Auto  

ObjectReference Property EstormoMarker  Auto  

Location Property SolitudeCastleDourLocation  Auto  

ReferenceAlias Property Elenwen  Auto  

Actor Property Tullius  Auto  

Quest Property CWSiegeObj  Auto  

ObjectReference Property CastleDour  Auto  

Faction Property aaThalmorElenwenTulliusFaction  Auto  

Scene Property aaThalmorElenwenTulliusScene1  Auto  

GlobalVariable Property aaThalmorElenwenTulliusBanterGlobal  Auto  

ObjectReference Property ElenwenMarker  Auto  

GlobalVariable Property aaThalmorElenwenTulliusBanter2  Auto  

Scene Property aaThalmorElenwenTulliusScene2  Auto  

Cell Property SolitudeJusticiarHeadquarters  Auto  

ObjectReference Property ThalmorHQ  Auto  

Quest Property MG01  Auto  

Quest Property MG08  Auto  

Scene Property aaThalmorElenwenTulliusScene3  Auto  

GlobalVariable Property aaThalmorElenwenTulliusBanter3  Auto  

ReferenceAlias Property Valmir  Auto  

Location Property ForelhostLocation  Auto  

Quest Property dunForelhost  Auto  

Outfit Property ThalmorOutfit  Auto  

Faction Property ThalmorFaction  Auto  

ObjectReference Property MG07GhostEnableParent  Auto  
ReferenceAlias Property Gissur  Auto  

ReferenceAlias Property Shavari  Auto  

Quest Property MQ202  Auto  
